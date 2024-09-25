from pprint import pprint
import json
import csv
from pathlib import Path
from ..request import get_cached_response, get_response_data

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


def write_csv(data, target_path):
    """Helper to write a list of dictionaries to target_path"""
    # we need a list of fields first
    fieldnames = data[0].keys()

    with open(target_path, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for data_row in data:
            writer.writerow(data_row)


def get_courses(target_dir, filename="courses.csv",cached=True):
    target_path = Path(target_dir / filename)
    api_request_func = request(cached)
    courses = []
    fields = ["id", "title", "description"]
    
    # create an array of course ids
    courses_url = f"{BASE_URL}/course"
    courses = api_request_func(courses_url)
    course_ids = [course["id"] for course in courses]
    course_data = []
    module_ids = []

    # fetch data for each indvidually, and create an array for them
    for course_id in course_ids:
        params = {"course_id": course_id, "full": True}
        course = api_request_func(courses_url, params)
        # filter to needed fields
        filtered_course = { field:value for field, value in course.items() if field in fields}
        course_data.append(filtered_course)
        
    # get ids for their related modules
        module_ids.extend([module["id"] for module in course["modules"]])
        del course["modules"]
    
    # write them to the filename in the target dir
    write_csv(course_data, target_path)
    
    # return module ids
    return module_ids