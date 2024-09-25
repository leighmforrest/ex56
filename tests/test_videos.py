import pytest
import ex56.request
import ex56.videos

courses = [
    {"id": 1, "title": "course 1", "green": "blue"},
    {"id": 2, "title": "course 2", "green": "red"}
]

course_data = [
    {"id": 1, "title": "course 1", "description": "Description for course 1", "green": "blue", "modules": [{"id": 101}, {"id": 102}]},
    {"id": 2, "title": "course 2", "description": "Description for course 2", "green": "blue", "modules": [{"id": 201}, {"id": 202}]},
]

def mock_course_get(url, params=None):
    print("HAHAHAHAHH!!!!!!")
    return {"id": 1}
    

def test_get_courses_module_ids(tmp_path, monkeypatch):
    target_dir = tmp_path

    # monkeypatch the cached and noncached requests
    monkeypatch.setattr("ex56.request.get_response_data", mock_course_get)
    monkeypatch.setattr("ex56.request.get_cached_response", mock_course_get)

    module_ids = ex56.videos.get_courses(target_dir)
    assert module_ids == [101, 102, 201, 202], "Module IDs do not match expected output."