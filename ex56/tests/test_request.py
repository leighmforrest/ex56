import pytest
import json
import hashlib
from ..tests.helpers import MockResponse
from ..request import get_cached_response_with_etag


@pytest.mark.parametrize(
    "url,json_data, etag",
    [
        ("http://www.example.com", {"id": 1, "title": "Test Todo"}, "abc123"),
        ("http://www.pets.com", {"id": 123, "item": "Puppy Chow"}, "fakeName"),
    ],
)
def test_get_cached_response_with_json(monkeypatch, mock_dbm, url, json_data, etag):
    mock_response = MockResponse(
        content=json.dumps(json_data), status_code=200, headers={"ETag": etag}
    )

    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)
    result = get_cached_response_with_etag(url, response_type="json")
    assert result == json_data
    assert "etag" in mock_dbm[hashlib.sha256(url.encode("utf-8")).hexdigest()]


@pytest.mark.parametrize(
    "url,html_data, etag",
    [
        ("http://www.example.com", "<h1>Hello World</h1>", "abc123"),
        ("http://www.pets.com", "<html><p>Hi There!</p><html>", "fakeName"),
    ],
)
def test_get_cached_response_with_html(monkeypatch, mock_dbm, url, html_data, etag):
    mock_response = MockResponse(
        content=html_data, status_code=200, headers={"ETag": etag}
    )

    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)
    result = get_cached_response_with_etag(url, response_type="html")
    assert result == html_data
    assert "etag" in mock_dbm[hashlib.sha256(url.encode("utf-8")).hexdigest()]


@pytest.mark.parametrize(
    "url, data, etag, response_type",
    [
        ("http://www.example.com", "<h1>Hello World</h1>", "abc123", "html"),
        ("http://www.pets.com", "<html><p>Hi There!</p><html>", "fakeName", "html"),
        ("http://www.google.com", {"id": 1, "title": "Test Todo"}, "abc123", "json"),
        ("http://www.xyz.com", {"id": 123, "item": "Puppy Chow"}, "fakeName", "json"),
    ],
)
def test_get_cached_response_304_html(
    monkeypatch, mock_dbm, url, data, etag, response_type
):
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    mock_response_304 = MockResponse(content="", status_code=304)

    mock_dbm[url_hash] = json.dumps({"etag": etag, "body": data}).encode("utf-8")

    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response_304)
    result = get_cached_response_with_etag(url, response_type=response_type)
    assert result == data
