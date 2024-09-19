import pytest
import json
import hashlib
from ..tests.helpers import MockResponse
from ..request import get_cached_response_with_etag, get_non_cached_response


@pytest.mark.parametrize(
    "url,json_data, etag",
    [
        ("http://www.example.com", {"id": 1, "title": "Test Todo"}, "abc123"),
        ("http://www.pets.com", {"id": 123, "item": "Puppy Chow"}, "fakeName"),
    ],
)
def test_get_cached_response_with_etag_json(monkeypatch, mock_dbm, url, json_data, etag):
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
def test_get_cached_response_with_etag_html(monkeypatch, mock_dbm, url, html_data, etag):
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
def test_get_cached_response_304(monkeypatch, mock_dbm, url, data, etag, response_type):
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    mock_response_304 = MockResponse(content="", status_code=304)

    mock_dbm[url_hash] = json.dumps({"etag": etag, "body": data}).encode("utf-8")

    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response_304)
    result = get_cached_response_with_etag(url, response_type=response_type)
    assert result == data


@pytest.mark.parametrize(
    "url, data, headers, response_type",
    [
        ("http://www.example.com", "<h1>Hello World</h1>", {}, "html"),
        ("http://www.pets.com", "<html><p>Hi There!</p><html>", {"id": 5}, "html"),
        (
            "http://www.google.com",
            json.dumps({"id": 1, "title": "Test Todo"}),
            {"green_id": 1234},
            "json",
        ),
        (
            "http://www.xyz.com",
            json.dumps({"id": 123, "item": "Puppy Chow"}),
            {"arg": "test"},
            "json",
        ),
    ],
)
def test_get_uncached_response(monkeypatch, url, data, headers, response_type):
    mock_response = MockResponse(content=data, status_code=200, headers=headers)

    monkeypatch.setattr(
        "requests.get", lambda url, data, headers=headers: mock_response
    )
    result = get_non_cached_response(url, response_type=response_type)

    if response_type == "json":
        assert result == json.loads(data)
    else:
        assert result == data
