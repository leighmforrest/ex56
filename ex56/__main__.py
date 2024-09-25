from pprint import pprint
from pathlib import Path

from ex56.videos import get_course_ids, get_course, get_module, get_lesson


BASE_DIR = Path(__file__).resolve().parent
BASE_URL = "https://learncodethehardway.com/api"


if __name__ == "__main__":
    module_ids = []
    lesson_ids = []
    course_ids = get_course_ids()
    courses = [get_course(course_id) for course_id in course_ids]
    lessons = []
    videos = []
    
    for course in courses:
        for module in course["modules"]:
            module_ids.append(module["id"])
    
    modules = [get_module(module_id) for module_id in module_ids]
    
    for module in modules:
        for lesson in module["lessons"]:
            lesson_ids.append(lesson["id"])
        
    for lesson_id in lesson_ids:
        lesson = get_lesson(lesson_id)
        lessons.append(lesson)
    
    for lesson in lessons:
        videos.extend(lesson["media"])

    pprint(videos[:5])
