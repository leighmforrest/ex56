import requests
import dbm
import hashlib
import json


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
            cached_data = json.loads(cache_db[url_hash].decode("utf-8"))
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
