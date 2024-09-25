from pprint import pprint
from ex56.request import get_cached_response, get_response_data

BASE_URL = "https://learncodethehardway.com/api"

REQUEST = {
    "cached": get_cached_response,
    "noncached": get_response_data
}


def request(cached=True):
    if cached:
        return REQUEST["cached"]
    else:
        return REQUEST["noncached"]


def get_course_ids(cached=True):
    url = f"{BASE_URL}/course"
    request_func = request(cached)
    data = request_func(url)
    
    ids = [datum['id'] for datum in data]
    
    return ids


# def get_course(course_id, cached=True):
#     url = f"{BASE_URL}/course"
#     params = {
#         "course_id": course_id,
#         "full": True
#     }
#     data = get_cached_response(url, params)
    
#     return data