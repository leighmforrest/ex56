import dbm
import os
import hashlib
from pathlib import Path
import json
import requests


# Function to generate a SHA-256 hash of the full url to use as a cache key
cache_key = lambda full_url: hashlib.sha256(full_url.encode("utf-8")).hexdigest()

# function to get html or json data
get_request = lambda full_url, headers: requests.get(full_url, headers=headers)


def get_full_url(url, params=None):
    """Get the full url, including query string parameters."""
    req = requests.PreparedRequest()
    req.prepare_url(url, params)
    return req.url


def get_response_data(response, response_type="json"):
    if response_type == "json":
        return response.json()
    else:
        return response.text  # For HTML


def get_uncached_response(url, params=None, headers={}, response_type="json"):
    """Get a response directly from url."""
    full_url = get_full_url(url, params)
    response = get_request(full_url, headers)
    response_data = get_response_data(response, response_type)

    return response_data


def get_cached_response(url, params=None, headers={}, response_type="json"):
    """
    Fetches a cached response with ETag support.
    """
    full_url = get_full_url(url, params)
    hashed_key = cache_key(full_url)

    # Open a dbm database for caching
    with dbm.open("cache", "c") as cache_db:

        # Check if the URL's response and ETag are already cached
        if hashed_key in cache_db:
            cached_data = json.loads(cache_db[hashed_key])  # Convert to Python dict
            cached_etag = cached_data.get("etag")
            cached_body = cached_data.get("body")

            # Send a request with the cached ETag
            headers = headers if isinstance(headers, dict) else {}
            headers = {**headers, "If-None-Match": cached_etag}
            response = get_request(full_url, headers=headers)

            if response.status_code == 304:
                print(f"Cache hit: {full_url} not modified, using cached data")
                if isinstance(cached_body, str) and response_type == "json":
                    return json.loads(cached_body)
                else:
                    return cached_body

            print(f"Cache miss: Resource modified, fetching new data from {full_url}")
            # Update the cache with the new ETag and response body
            response_body = get_response_data(response, response_type)
            body_data = response_body

            cache_db[hashed_key] = json.dumps(
                {"etag": response.headers.get("ETag"), "body": body_data}
            )
            return body_data

        print(f"Cache miss: Fetching new data from {full_url}")
        # Fetch new data and cache it along with the ETag
        response = get_request(full_url, headers=headers)
        response_body = get_response_data(response, response_type)

        cache_db[hashed_key] = json.dumps(
            {
                "etag": response.headers.get("ETag"),
                "body": (
                    json.dumps(response_body)
                    if response_type == "json"
                    else response_body
                ),
            }
        )

        return response_body


def download_file_with_cache(url, file_path, params=None, **kwargs):
    """Download a file at a given url; if cached, get the file in the file_path."""

    # Create the directory for the file if it doesn't exist
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create a unique cache key based on the URL
    full_url = get_full_url(url, params)
    url_hash = cache_key(full_url)

    with dbm.open("cache", "c") as cache:
        # Check if we have a cached file with a valid ETag
        cached_data = cache.get(url_hash)

        if cached_data:
            try:
                cached_data = json.loads(cached_data)
                cached_etag = cached_data.get("etag")
                cached_file_path = cached_data.get("file_path")

                # Check if the cached file exists
                if os.path.exists(cached_file_path):
                    headers = {"If-None-Match": cached_etag}
                    response = requests.get(url, headers=headers, **kwargs)

                    if response.status_code == 304:
                        print("Cache hit: File not modified, using cached file.")
                        return cached_file_path
            except json.JSONDecodeError:
                print(
                    "Warning: Cached data is not valid JSON, proceeding to download the file."
                )

        # Download the file if not cached or modified
        print("Downloading file.")
        response = requests.get(full_url, stream=True, **kwargs)
        response.raise_for_status()

        # Write the response content to a file
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                file.write(chunk)

        # Update the cache with the new file info
        cache[url_hash] = json.dumps(
            {"etag": response.headers.get("ETag"), "file_path": str(file_path)}
        )

        print("File downloaded and cached.")
        return str(file_path)
