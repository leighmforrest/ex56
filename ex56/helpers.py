from ex56.request import get_cached_response, get_uncached_response, download_file_with_cache, download_file_without_cache

def get_api_request_func(cached=True):
    """Get an api request function based on whether the request is cached or not."""
    if cached:
        return get_cached_response
    else:
        return get_uncached_response


def get_download_function(cached=True):
    """Download a file based on if request is to be cached or not."""
    if cached:
        return download_file_with_cache
    else:
        return download_file_without_cache