import pytest
import json
import hashlib
from ..tests.helpers import MockResponse, assert_data_result, _test_cached_response
from ..request import get_cached_response_with_etag, get_non_cached_response, download_file_without_cache


@pytest.mark.parametrize(
    "url, data, etag, response_type",
    [
        ("http://www.example.com", "<h1>Hello World</h1>", "abc123", "html"),
        ("http://www.pets.com", "<html><p>Hi There!</p><html>", "fakeName", "html"),
        (
            "http://www.example.com",
            json.dumps({"id": 1, "title": "Test Todo"}),
            "abc123",
            "json",
        ),
        (
            "http://www.pets.com",
            json.dumps({"id": 123, "item": "Puppy Chow"}),
            "fakeName",
            "json",
        ),
    ],
)
def test_get_cached_response_with_etag(
    monkeypatch, mock_dbm, url, data, etag, response_type
):
    mock_response = MockResponse(content=data, status_code=200, headers={"ETag": etag})

    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)
    _test_cached_response(
        monkeypatch, mock_dbm, url, data, etag, response_type=response_type
    )


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
    assert_data_result(data, result, response_type)


@pytest.mark.parametrize(
    "url, data, etag, new_data, new_etag, response_type",
    [
        (
            "http://www.example.com",
            "<h1>Hello World</h1>",
            "abc123",
            "<h1>Hello World Too</h1>",
            "321cba",
            "html",
        ),
        (
            "http://www.pets.com",
            "<html><p>Hi There!</p><html>",
            "fakeName",
            "<html><p>Hi There Again!</p><html>",
            "fakeNameTwo",
            "html",
        ),
        (
            "http://www.google.com",
            json.dumps({"id": 1, "title": "Test Todo"}),
            "abc123",
            json.dumps({"id": 1, "title": "Test Todo"}),
            "NewEtag",
            "json",
        ),
        (
            "http://www.xyz.com",
            json.dumps({"id": 123, "item": "Puppy Chow"}),
            "fakeName",
            json.dumps({"id": 123, "item": "Dog Chow"}),
            "fakeNameIsAllNew",
            "json",
        ),
    ],
)
def test_cache_update_on_cache_miss_new_etag(
    capfd, monkeypatch, mock_dbm, url, data, etag, new_data, new_etag, response_type
):
    # Make sure cache exists
    _test_cached_response(
        monkeypatch, mock_dbm, url, data, etag, response_type=response_type
    )

    # Make a new MockResponse
    mock_new_response = MockResponse(
        content=new_data, status_code=200, headers={"ETag": new_etag}
    )
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_new_response)

    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()

    result = get_cached_response_with_etag(url, response_type=response_type)
    assert_data_result(new_data, result, response_type)

    assert url_hash in mock_dbm
    cached_data = json.loads(mock_dbm[url_hash])
    assert cached_data["etag"] == new_etag
    assert_data_result(new_data, cached_data["body"], response_type=response_type)

    # Capture print output
    captured = capfd.readouterr()
    assert "Cache miss: Resource modified, fetching new data" in captured.out


def test_download_file_without_cache(mock_request_get, tmp_file_path):
    download_file_without_cache("http://example.com/file.txt", tmp_file_path)

    assert tmp_file_path.exists()
    assert tmp_file_path.read_bytes() == b"ItemOne,ItemTwo"