import pytest
import tempfile
from pathlib import Path
import os
import json
from .helpers import MockResponse, MockDownloadResponse
from .api_data import courses_data, course_data
from ex56.request import get_full_url


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