from request import get_cached_response_with_etag

if __name__ == "__main__":
    cached_response_html = get_cached_response_with_etag(
        "https://learncodethehardway.com/setup/python/ttb/", response_type="html"
    )
    cached_response_html = get_cached_response_with_etag(
        "https://learncodethehardway.com/setup/python/ttb/", response_type="html"
    )
