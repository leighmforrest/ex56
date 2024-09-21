import pytest
from pathlib import Path
from .helpers import MockDownloadResponse


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


@pytest.fixture
def tmp_file_path(tmpdir):
    return Path(tmpdir) / "test.txt"