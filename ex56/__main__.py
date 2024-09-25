from pprint import pprint
from pathlib import Path

from videos import get_course_ids


BASE_DIR = Path(__file__).resolve().parent
BASE_URL = "https://learncodethehardway.com/api"


if __name__ == "__main__":
    course_ids = get_course_ids()
    print(course_ids)
    # courses = [get_course(course_id) for course_id in course_ids]
    # print(courses)