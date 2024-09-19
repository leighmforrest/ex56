import json
import hashlib
from ..request import get_cached_response_with_etag


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
