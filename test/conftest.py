import json
from pathlib import Path
from test.data_for_tests import (
    API_DATA,
    BASE_MARKUP,
    LINK_MARKUP,
    VIDEOS_EXPECTED_DATAFRAME_DATA,
    FINAL_EXPECTED_VIDEOS_DATAFRAMES,
)
from test.mocks import MockDownloadResponse

import pandas as pd
import pytest

from ex_56.soup import get_soup


@pytest.fixture
def temp_file_path(tmpdir):
    """Fixture to create and clean up a temporary file path."""
    return Path(tmpdir) / "test.txt"


@pytest.fixture
def mock_dbm(monkeypatch):
    mock_db = {}

    class MockDBM:
        def __init__(self):
            pass

        def __enter__(self):
            return mock_db

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    monkeypatch.setattr("dbm.open", lambda *args, **kwargs: MockDBM())

    return mock_db


@pytest.fixture
def mock_download_200(monkeypatch):
    mock_response = MockDownloadResponse(
        content=b"ItemOne,ItemTwo", status_code=200, headers={"ETag": "SomeEtag"}
    )
    monkeypatch.setattr("requests.get", lambda *arg, **kwargs: mock_response)


@pytest.fixture
def mock_download_304(monkeypatch):
    mock_response = MockDownloadResponse(
        content=b"",
        status_code=304,
    )
    monkeypatch.setattr("requests.get", lambda *arg, **kwargs: mock_response)


@pytest.fixture
def mock_download_200(monkeypatch):
    mock_response = MockDownloadResponse(
        content=b"ItemOne,ItemTwo", status_code=200, headers={"etag": "SomeEtag"}
    )
    monkeypatch.setattr("requests.get", lambda *arg, **kwargs: mock_response)


@pytest.fixture
def link_soup():
    return get_soup(BASE_MARKUP.format(LINK_MARKUP))


#
#   Videos Fixtures
#
@pytest.fixture
def courses_data():
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
def mock_course_api_request(monkeypatch, courses_data, course_data):
    def mock_course_get(url, params=None):
        if params:
            course_id = params["course_id"]
            return json.dumps(
                next(course for course in course_data if course["id"] == course_id)
            )
        return json.dumps(courses_data)

    monkeypatch.setattr("ex_56.videos.get_with_cache", mock_course_get)
    monkeypatch.setattr("ex_56.videos.get_without_cache", mock_course_get)


@pytest.fixture
def mock_module_api_request(monkeypatch, module_data):
    def mock_module_get(url, params=None):
        if params:
            module_id = params["module_id"]
            return json.dumps(
                next(module for module in module_data if module["id"] == module_id)
            )
        return None

    monkeypatch.setattr("ex_56.videos.get_with_cache", mock_module_get)
    monkeypatch.setattr("ex_56.videos.get_without_cache", mock_module_get)


@pytest.fixture
def mock_lesson_api_request(monkeypatch, lesson_data):
    def mock_lesson_get(url, params=None):
        if params:
            lesson_id = params["lesson_id"]
            return json.dumps(
                next(lesson for lesson in lesson_data if lesson["id"] == lesson_id)
            )
        return None

    monkeypatch.setattr("ex_56.videos.get_with_cache", mock_lesson_get)
    monkeypatch.setattr("ex_56.videos.get_without_cache", mock_lesson_get)


@pytest.fixture
def courses_dataframe():
    return pd.DataFrame(VIDEOS_EXPECTED_DATAFRAME_DATA["courses"])


@pytest.fixture
def modules_dataframe():
    return pd.DataFrame(VIDEOS_EXPECTED_DATAFRAME_DATA["modules"])


@pytest.fixture
def lesson_dataframe():
    return pd.DataFrame(VIDEOS_EXPECTED_DATAFRAME_DATA["lessons"])


@pytest.fixture
def final_modules_dataframe():
    return pd.DataFrame(FINAL_EXPECTED_VIDEOS_DATAFRAMES["modules"])


@pytest.fixture
def final_courses_dataframe():
    return pd.DataFrame(FINAL_EXPECTED_VIDEOS_DATAFRAMES["courses"])
