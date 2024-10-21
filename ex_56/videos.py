from ex_56.constants import BASE_API_URL
from ex_56.decorators import convert_and_filter_single_item, convert_data
from ex_56.request import get_with_cache, get_without_cache

request_func = lambda cached=True: get_with_cache if cached else get_without_cache


ALLOWED_KEYS = {"course": ["id", "title", "modules"]}


@convert_data()
def get_courses(cached=True):
    """Get a list of courses from the API."""
    func = request_func(cached)
    courses = func(f"{BASE_API_URL}/course")
    return courses


@convert_and_filter_single_item(allowed_keys=ALLOWED_KEYS["course"])
def get_course(course_id, cached=True):
    """Get a course from the API."""
    func = request_func(cached)
    course = func(f"{BASE_API_URL}/course", {"course_id": course_id, "full": True})
    return course
