import pytest
import tempfile
from pathlib import Path
import os
from .helpers import MockResponse, MockDownloadResponse
from .test_data import API_DATA


@pytest.fixture
def temp_file():
    """Fixture to create and cleanup a temporary file."""
    fd, path = tempfile.mkstemp()
    os.close(fd)
    yield path
    os.remove(path)


@pytest.fixture
def tmp_file_path(tmpdir):
    return Path(tmpdir) / "test.txt"


@pytest.fixture
def mock_dbm(monkeypatch):
    mock_db = {}

    class MockDBM:
        def __enter__(self):
            return mock_db

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    monkeypatch.setattr("dbm.open", lambda *args, **kwargs: MockDBM())

    return mock_db


@pytest.fixture
def mock_request_get(monkeypatch):
    def mock_get(url, stream=True, **kwargs):
        return MockDownloadResponse(b"ItemOne,ItemTwo")

    monkeypatch.setattr("requests.get", mock_get)


# Fixtures for use for testing the videos module
@pytest.fixture
def courses():
    return API_DATA["courses"]


@pytest.fixture
def course_data():
    return API_DATA["course"]


@pytest.fixture
def module_data():
    return API_DATA["module"]


@pytest.fixture
def lesson_data():
    return API_DATA["lesson"]


@pytest.fixture
def mock_course_api_request(monkeypatch, course_data, courses):
    def mock_course_get(url, params=None):
        if params:
            course_id = params["course_id"]
            return next(course for course in course_data if course["id"] == course_id)
        return courses

    # monkeypatch the cached and noncached requests
    monkeypatch.setattr("ex56.videos.get_uncached_response", mock_course_get)
    monkeypatch.setattr("ex56.videos.get_cached_response", mock_course_get)


@pytest.fixture
def mock_module_api_request(monkeypatch, module_data):
    def mock_module_get(url, params=None):
        if params:
            module_id = params["module_id"]
            return next(module for module in module_data if module["id"] == module_id)
        return None

    # monkeypatch the cached and noncached requests
    monkeypatch.setattr("ex56.videos.get_uncached_response", mock_module_get)
    monkeypatch.setattr("ex56.videos.get_cached_response", mock_module_get)


@pytest.fixture
def mock_lesson_api_request(monkeypatch, lesson_data):
    def mock_lesson_get(url, params=None):
        if params:
            lesson_id = params["lesson_id"]
            return next(lesson for lesson in lesson_data if lesson["id"] == lesson_id)
        return None

    # monkeypatch the cached and noncached requests
    monkeypatch.setattr("ex56.videos.get_uncached_response", mock_lesson_get)
    monkeypatch.setattr("ex56.videos.get_cached_response", mock_lesson_get)
