from request import get_cached_response_with_etag, get_non_cached_response

if __name__ == "__main__":
    cached_response_html = get_non_cached_response(
        "https://learncodethehardway.com/setup/python/ttb/"
    )
    cached_response_html = get_cached_response_with_etag(
        "https://learncodethehardway.com/setup/python/ttb/", response_type="html"
    )
