import pandas as pd

from ex_56.constants import BASE_API_URL
from ex_56.decorators import convert_and_filter_single_item, convert_data
from ex_56.request import get_with_cache, get_without_cache

get_ids = lambda data: [datum["id"] for datum in data]
request_func = lambda cached=True: get_with_cache if cached else get_without_cache


ALLOWED_KEYS = {
    "course": ["id", "title", "modules"],
    "module": ["id", "title", "lessons", "product_id"],
    "lesson": ["id", "title", "media"],
}


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


@convert_and_filter_single_item(allowed_keys=ALLOWED_KEYS["module"])
def get_module(module_id, cached=True):
    """Get a module from the API."""
    func = request_func(cached)
    module = func(f"{BASE_API_URL}/module", {"module_id": module_id, "full": True})
    return module


@convert_and_filter_single_item(allowed_keys=ALLOWED_KEYS["lesson"])
def get_lesson(lesson_id, cached=True):
    """Get a lesson from the API."""
    func = request_func(cached)
    lesson = func(f"{BASE_API_URL}/lesson", {"lesson_id": lesson_id, "full": True})
    return lesson


def get_course_dataframe(cached=True):
    module_ids = []
    courses = []
    course_ids = [course["id"] for course in get_courses(cached)]

    for course_id in course_ids:
        course = get_course(course_id, cached)
        module_ids.extend(get_ids(course["modules"]))
        del course["modules"]
        courses.append(course)

    course_df = pd.DataFrame(courses)
    return course_df, module_ids


def get_module_dataframe(module_ids, cached=True):
    lesson_ids = []
    modules = []

    for module_id in module_ids:
        module = get_module(module_id, cached)
        lesson_ids.extend(get_ids(module["lessons"]))
        del module["lessons"]
        modules.append(module)

    module_df = pd.DataFrame(modules)
    return (module_df, lesson_ids)
