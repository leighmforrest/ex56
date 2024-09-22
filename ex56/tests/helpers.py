import json
import hashlib
from ex56.request import get_cached_response_with_etag, download_file_with_cache


class MockResponse(object):
    def __init__(self, content, status_code, headers=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}

    def json(self):
        return json.loads(self.content)

    @property
    def text(self):
        return self.content


class MockDownloadResponse(object):
    """Class for mocking a requests.get call that downloads a file."""
    def __init__(self, content):
        self.content = content
        self.iter_content_called = False
    
    def iter_content(self, chunk_size=1024):
        self.iter_content_called = True
        return [self.content[i:i + chunk_size] for i in range(0, len(self.content), chunk_size)]
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def raise_for_status(self):
        pass



def assert_data_result(data, result, response_type="json"):
    if response_type == "json":
        assert result == json.loads(data)
    else:
        assert result == data


def _test_cached_response(monkeypatch, mock_dbm, url, data, etag, response_type="json"):
    mock_response = MockResponse(data, status_code=200, headers={"ETag": etag})

    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)
    result = get_cached_response_with_etag(url, response_type)
    assert_data_result(data, result, response_type)
    assert "etag" in mock_dbm[hashlib.sha256(url.encode("utf-8")).hexdigest()]


def _test_cached_response_download(url, temp_file, mock_dbm, mock_request_get):
    cache_key = hashlib.sha256(url.encode()).hexdigest()
    file_path = download_file_with_cache(url, temp_file, cache_db=mock_dbm)
    
    with open(file_path, "rb") as f:
        assert f.read() == b"ItemOne,ItemTwo"

    assert cache_key in mock_dbm
