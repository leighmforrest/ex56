from pprint import pprint
from ex56.videos import get_course_ids

def test_get_course_ids(mock_response_courses):
    courses = get_course_ids()
    assert len(courses) == 2


# def test_get_course(mock_response_course):
#     course = get_course(1)
#     assert course["id"] == 1
#     assert "modules" in course