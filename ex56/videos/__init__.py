from pprint import pprint
import csv
import glob
from pathlib import Path
import pandas as pd
from ex56.helpers import get_api_request_func, get_dataframes
from ex56.constants import API_URL


def write_csv(data, target_path):
    """Helper to write a list of dictionaries to target_path"""
    # we need a list of fields first
    fieldnames = data[0].keys()

    with open(target_path, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for data_row in data:
            writer.writerow(data_row)


def filter_data(data_ids, api_request_func, data_url, fields, id_param_name):
        """Return filtered array of dictionaries, given a list of 
            ids, a request api function, a string of the id parameter name, and a list of needed fields.
        """

        data_list = []

        for data_id in data_ids:
            params = {id_param_name: data_id, "full": True}
            data = api_request_func(data_url, params)

            # filter to needed fields
            filtered_data = {
                field: value for field, value in data.items() if field in fields
            }
            data_list.append(filtered_data)

        return data_list


def get_ids(data_items, related_id_field, id_field = "id"):
    """Get id field from a list of data items."""
    data_ids = []

    for data_item in data_items:
        data_ids.extend([data[id_field] for data in data_item[related_id_field]])
        del data_item[related_id_field]

    return data_ids


def get_courses(target_dir, filename="courses.csv", cached=True):
    """Write a csv of course data and return a list of module ids."""

    target_path = Path(target_dir / filename)
    fields = ["id", "title", "description", "modules"]
    api_request_func = get_api_request_func(cached)

    # create an array of course ids
    courses_url = f"{API_URL}/course"
    initial_courses = api_request_func(courses_url)
    course_ids = [course["id"] for course in initial_courses]

    # fetch data for each indvidually, and create an array for them
    courses = filter_data(course_ids, api_request_func, courses_url, fields, "course_id")

    # get ids for their related modules
    module_ids = get_ids(courses, "modules", "id")

    # write them to the filename in the target dir
    write_csv(courses, target_path)

    # return module ids
    return module_ids


def get_modules(module_ids,  target_dir, filename="modules.csv", cached=True):
    """Write a csv of module data and return a list of lesson ids."""

    target_path = target_dir / filename
    fields = ["id", "title", "description", "lessons", "product_id"]
    api_request_func = get_api_request_func(cached)
    
    modules_url = f"{API_URL}/module"
    
    modules = filter_data(module_ids, api_request_func, modules_url, fields, "module_id")
    lesson_ids = get_ids(modules, "lessons")

    write_csv(modules, target_path)

    return lesson_ids


def get_lessons(lesson_ids,  target_dir, filename="lessons.csv", cached=True):
    """Write a csv of lesson data, including total video duration time."""

    target_path = target_dir / filename
    lessons_url = f"{API_URL}/lesson"
    fields = ["id", "title", "description", "media", "module_id"]
    api_request_func = get_api_request_func(cached)

    lessons = filter_data(lesson_ids, api_request_func, lessons_url, fields, "lesson_id")
    
    # Reduce the media to running time float
    for lesson in lessons:
        total_duration = sum(item['duration'] for item in lesson['media'])
        del lesson["media"]

        lesson["duration"] = total_duration
    
    write_csv(lessons, target_path)
