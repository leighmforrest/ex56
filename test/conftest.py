import json
from pathlib import Path
from test.data_for_tests import (
    API_DATA,
    BASE_MARKUP,
    FINAL_EXPECTED_TTB_DATAFRAME,
    FINAL_EXPECTED_VIDEOS_DATAFRAMES,
    LINK_MARKUP,
    VIDEOS_EXPECTED_DATAFRAME_DATA,
)
from test.helpers import download_spreadsheets_helper
from test.mocks import MockDownloadResponse

import pandas as pd
import pytest

from ex56.soup import get_soup
from ex56.ttb import get_xlsx_links


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

    monkeypatch.setattr("ex56.videos.get_with_cache", mock_course_get)
    monkeypatch.setattr("ex56.videos.get_without_cache", mock_course_get)


@pytest.fixture
def mock_module_api_request(monkeypatch, module_data):
    def mock_module_get(url, params=None):
        if params:
            module_id = params["module_id"]
            return json.dumps(
                next(module for module in module_data if module["id"] == module_id)
            )
        return None

    monkeypatch.setattr("ex56.videos.get_with_cache", mock_module_get)
    monkeypatch.setattr("ex56.videos.get_without_cache", mock_module_get)


@pytest.fixture
def mock_lesson_api_request(monkeypatch, lesson_data):
    def mock_lesson_get(url, params=None):
        if params:
            lesson_id = params["lesson_id"]
            return json.dumps(
                next(lesson for lesson in lesson_data if lesson["id"] == lesson_id)
            )
        return None

    monkeypatch.setattr("ex56.videos.get_with_cache", mock_lesson_get)
    monkeypatch.setattr("ex56.videos.get_without_cache", mock_lesson_get)


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


#
#   TTB FIXTURES
#
@pytest.fixture
def markup():
    markup_file = Path(__file__).parent / "data_files/test.html"
    with open(markup_file, "r") as file:
        markup_text = file.read()

    return markup_text


@pytest.fixture
def mock_markup_request(markup, monkeypatch):
    def mock_markup_get(url):
        return markup

    # monkeypatch the cached and noncached requests
    monkeypatch.setattr("ex56.ttb.get_with_cache", mock_markup_get)
    monkeypatch.setattr("ex56.ttb.get_without_cache", mock_markup_get)


@pytest.fixture
def xlsx_links(markup, mock_markup_request, cached):
    links = get_xlsx_links(cached)

    return links


@pytest.fixture
def test_excel_bytes():
    spreadsheet_path = Path(__file__).parent / "data_files/test.xlsx"

    with open(spreadsheet_path, "rb") as file:
        file_bytes = file.read()

    return file_bytes


@pytest.fixture
def mock_spreadsheet_download(monkeypatch, test_excel_bytes):
    def mock_response(full_url, file_path, **kwargs):
        with open(file_path, "wb") as file:
            file.write(test_excel_bytes)
        return str(file_path)

    monkeypatch.setattr("ex56.ttb.download_file_with_cache", mock_response)
    monkeypatch.setattr("ex56.ttb.download_file", mock_response)


@pytest.fixture
def test_download_spreadsheet(mock_spreadsheet_download, xlsx_links, tmpdir, cached):
    download_spreadsheets_helper(mock_spreadsheet_download, xlsx_links, tmpdir, cached)


@pytest.fixture
def test_ttb_dataframe():
    spreadsheet_path = Path(__file__).parent / "data_files/test.xlsx"
    return pd.read_excel(spreadsheet_path)


@pytest.fixture
def test_final_ttb_dataframe():
    df = pd.DataFrame(FINAL_EXPECTED_TTB_DATAFRAME)
    # Ensure Total Sales column is consistent as strings if "N/A" is expected in both
    df["Total Sales"] = df["Total Sales"].astype(str)
    return df

#
# Reporting fixtures
#
@pytest.fixture
def reporting_df_tuples(test_final_ttb_dataframe, final_modules_dataframe, final_courses_dataframe):
    return [
        (test_final_ttb_dataframe, f"ttb", ".0f".format),
        (final_modules_dataframe, f"modules", "{:.3f}".format),
        (final_courses_dataframe, f"modules", "{:.3f}".format),
    ]