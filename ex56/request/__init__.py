import requests
import dbm
import os
import hashlib
import json
from pathlib import Path


def get_request(url, **kwargs):
    return requests.get(url, **kwargs)


def get_non_cached_response(url, params=None, headers=None, response_type="json"):
    print(f"Retrieving direct response from url: {url}")
    response = requests.get(url, params, headers)
    if response_type == "json":
        response_body = response.json()
    else:
        response_body = response.text  # For HTML

    return response_body


def get_cached_response_with_etag(url, response_type="json"):
    """
    Fetches a cached response with ETag support.

    :param url: The URL to request data from.
    :param response_type: 'json' for JSON response or 'html' for HTML response.
    :return: The response data, either JSON or HTML based on the response_type.
    """
    # Open a dbm database for caching
    with dbm.open("cache", "c") as cache_db:
        # Create a hash of the URL to use as the cache key
        url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()

        # Check if the URL's response and ETag are already cached
        if url_hash in cache_db:
            cached_data = json.loads(cache_db[url_hash])
            cached_etag = cached_data.get("etag")
            cached_body = cached_data.get("body")

            # Send a request with the cached ETag
            headers = {"If-None-Match": cached_etag}
            response = get_request(url, headers=headers)

            if response.status_code == 304:
                print("Cache hit: Resource not modified, using cached data")
                return cached_body  # Return cached response body

            print("Cache miss: Resource modified, fetching new data")
            # Update the cache with the new ETag and response body
            if response_type == "json":
                response_body = response.json()
            else:
                response_body = response.text  # For HTML

            cache_db[url_hash] = json.dumps(
                {"etag": response.headers.get("ETag"), "body": response_body}
            )
            return response_body

        print("Cache miss: Fetching new data from the web")
        # Fetch new data and cache it along with the ETag
        response = get_request(url)
        if response_type == "json":
            response_body = response.json()
        else:
            response_body = response.text  # For HTML

        cache_db[url_hash] = json.dumps(
            {"etag": response.headers.get("ETag"), "body": response_body}
        )

        return response_body


def download_file_without_cache(url, file_path, **kwargs):
    """Download a file, given a url and a file path."""
    # create directory if it does not exist
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True, **kwargs) as response:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                file.write(chunk)


import os
import requests
import hashlib
import dbm

def download_file_with_cache(url, file_path, cache_db='cache_db', **kwargs):
    # Create or open cache database
    with dbm.open(cache_db, 'c') as cache:
        # Create a unique cache key based on the URL
        cache_key = hashlib.sha256(url.encode()).hexdigest()

        # Check if the URL is cached
        if cache_key in cache:
            print("Using cached file.")
            # Read the cached file path
            cached_file_path = str(cache[cache_key])
            return cached_file_path
        
        # If not cached, proceed with downloading
        response = requests.get(url, **kwargs)
        response.raise_for_status()

        # Save the file to the specified file path
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Update the cache
        cache[cache_key] = str(file_path)
        print("File downloaded and cached.")

        return file_path

    """Download a file with caching support using ETag."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with dbm.open("cache", "c") as cache_db:
        url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()

        # Check if we already have a cached file with a valid ETag
        if url_hash in cache_db:
            cached_data = json.loads(cache_db[url_hash])
            cached_etag = cached_data.get("etag")
            cached_file_path = cached_data.get("file_path")

            # Check if the file already exists on disk
            if os.path.exists(cached_file_path):
                headers = {"If-None-Match": cached_etag}
                response = get_request(url, headers=headers, stream=True, **kwargs)

                if response.status_code == 304:
                    print("Cache hit: File not modified, using cached file")
                    return cached_file_path # return cached file path
                else:
                    print("File not found on disk, reloading.")
                    response = get_request(url, headers=headers, stream=True, **kwargs)
                
            else:
                print("Cache miss: No cached data, downloading.")
                with get_request(url, stream=True, **kwargs) as response:
                    with open(file_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=10 * 1024):
                            file.write(chunk)
                    
                    file_path_str  = str(file_path)

                    cache_db[url_hash] = json.dumps({
                        "etag": response.headers.get("ETag"),
                        "file_path": file_path_str
                    })

                    return file_path_str