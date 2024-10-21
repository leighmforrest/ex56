import dbm
import json
import hashlib
import requests


get_cache_key = lambda full_url: hashlib.sha256(full_url.encode("utf-8")).hexdigest()


def get_full_url(url, params=None):
    """Get a URL with the params as query strings."""
    req = requests.PreparedRequest()
    req.prepare_url(url, params)
    return req.url


def add_to_cache(response, cache_db, cache_key):
    print(f"CACHE_DB: {type(cache_db)}")
    body = response.text
    etag = response.headers.get("ETag")
    data_dict = {"etag": etag, "body": body}
    cache_db[cache_key] = json.dumps(data_dict)

    return data_dict


def get_with_cache(url, params=None, headers={}):
    full_url = get_full_url(url, params)
    cache_key = get_cache_key(full_url)

    with dbm.open("cache", "c") as cache_db:
        if cache_key in cache_db:
            cached_data = json.loads(cache_db[cache_key])
            cached_etag = cached_data.get("etag")
            cached_body = cached_data.get("body")

            headers = headers if isinstance(headers, dict) else {}
            headers = {**headers, "If-None-Match": cached_etag}

            response = requests.get(full_url, headers=headers)

            if response.status_code == 304:
                print(f"Cache hit: {full_url} retrieving cache")
                return cached_body
            
            elif response.status_code == 200:
                print(f"Cache miss: {full_url} retrieving data")
                data_dict = add_to_cache(response, cache_db, cache_key)
                return data_dict["body"]
            else:
                response.raise_for_status()
        else:
            print(f"Cache miss: {full_url} retrieving new data")
            response = requests.get(full_url)

            # Must be 200 for data storage
            if response.status_code != 200:
                response.raise_for_status()
            
            data_dict = add_to_cache(response, cache_db, cache_key)

            return data_dict["body"]