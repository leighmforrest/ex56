import pytest
import tempfile
from pathlib import Path
import os
import json
from .helpers import MockResponse, MockDownloadResponse
import ex56.videos


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
    return [
        {"id": 1, "title": "course 1", "green": "blue"},
        {"id": 2, "title": "course 2", "green": "red"},
    ]


@pytest.fixture
def course_data():
    return [
        {
            "id": 1,
            "title": "course 1",
            "description": "Description for course 1",
            "green": "blue",
            "modules": [{"id": 101}, {"id": 102}],
        },
        {
            "id": 2,
            "title": "course 2",
            "description": "Description for course 2",
            "green": "blue",
            "modules": [{"id": 201}, {"id": 202}],
        },
    ]


@pytest.fixture
def mock_course_api_request(monkeypatch, course_data, courses):
    def mock_course_get(url, params=None):
        if params:
            course_id = params["course_id"]
            return next(course for course in course_data if course["id"] == course_id)
        return courses

    # monkeypatch the cached and noncached requests
    monkeypatch.setattr(ex56.videos, "get_response_data", mock_course_get)
    monkeypatch.setattr(ex56.videos, "get_cached_response", mock_course_get)
