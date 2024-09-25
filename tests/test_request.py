import pytest
import json
from .helpers import MockResponse, MockDownloadResponse
from ex56.request import (
    get_cached_response,
    get_full_url,
    cache_key,
    download_file_with_cache,
)

@pytest.mark.parametrize(
    "url, params, data, etag, response_type",
    [
        ("http://www.example.com", {"id": 3}, "<h1>Hello World</h1>", "abc123", "html"),
        ("http://www.pets.com", None, "<html><p>Hi There!</p></html>", "fakeName", "html"),
        (
            "http://www.example.com",
            None,
            {"id": 1, "title": "Test Todo"},
            "abc123",
            "json",
        ),
        (
            "http://www.pets.com",
            None,
            {"id": 123, "item": "Puppy Chow"},
            "fakeName",
            "json",
        ),
    ],
)
def test_get_cached_response(monkeypatch, mock_dbm, url, params, data, etag, response_type):
    full_url = get_full_url(url, params)
    hashed_key = cache_key(full_url)
    mock_response = MockResponse(data, status_code=200, headers={"ETag": etag})
    
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    result = get_cached_response(url, params, response_type=response_type)
    assert result == data
    assert hashed_key in mock_dbm


@pytest.mark.parametrize(
    "url, params, data, etag, response_type",
    [
        ("http://www.example.com", {"id": 3}, "<h1>Hello World</h1>", "abc123", "html"),
        ("http://www.pets.com", None, "<html><p>Hi There!</p></html>", "fakeName", "html"),
        (
            "http://www.example.com",
            None,
            {"id": 1, "title": "Test Todo"},
            "abc123",
            "json",
        ),
        (
            "http://www.pets.com",
            None,
            {"id": 123, "item": "Puppy Chow"},
            "fakeName",
            "json",
        ),
    ],
)
def test_get_cached_response_304(monkeypatch, mock_dbm, url, params, data, etag, response_type):
    full_url = get_full_url(url, params)
    hashed_key = cache_key(full_url)
    mock_dbm[hashed_key] = json.dumps({"etag": etag, "body": data}).encode("utf-8")

    # Mock a 304 response
    mock_response = MockResponse("", status_code=304)
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    result = get_cached_response(url, params, response_type=response_type)
    assert result == data
    assert hashed_key in mock_dbm


@pytest.mark.parametrize(
    "url, params, old_data, new_data, etag, response_type",
    [
        ("http://www.example.com", {"id": 3}, "<h1>Hello Old World</h1>", "<h1>Hello World</h1>", "abc123", "html"),
        ("http://www.pets.com", None, "<html><p>Hi There Oldster!</p></html>", "<html><p>Hi There!</p></html>", "fakeName", "html"),
        (
            "http://www.example.com",
            None,
            {"id": 1, "title": "Old Test Todo"},
            {"id": 1, "title": "Test Todo"},
            "abc123",
            "json",
        ),
        (
            "http://www.pets.com",
            None,
            {"id": 5678, "east": "west"},
            {"id": 123, "item": "Puppy Chow"},
            "fakeName",
            "json",
        ),
    ],
)
def test_get_response_changed_content(capfd, monkeypatch, mock_dbm, url, params, old_data, new_data, etag, response_type):
    full_url = get_full_url(url, params)
    hashed_key = cache_key(full_url)
    mock_dbm[hashed_key] = json.dumps({"etag": f"{etag}OldSchoolTag", "body": old_data}).encode("utf-8")

    mock_new_response = MockResponse(content=new_data, status_code=200, headers={"ETag": etag})
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_new_response)

    result = get_cached_response(url, params, response_type=response_type)
    assert result == new_data
    assert hashed_key in mock_dbm

    # Capture print output
    captured = capfd.readouterr()
    assert "Cache miss: Resource modified, fetching new data" in captured.out


def test_cached_response_download(monkeypatch, capfd, temp_file, mock_dbm):
    params = {"id": 1}
    url = "http://www.example.com/example.txt"
    full_url = get_full_url(url, params)
    hashed_key = cache_key(full_url)

    # First download to simulate caching
    mock_response = MockDownloadResponse(content=b"ItemOne,ItemTwo", status_code=200, headers={"ETag": "some-etag"})
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    file_path = download_file_with_cache(url, temp_file, params)

    with open(file_path, "rb") as f:
        assert f.read() == b"ItemOne,ItemTwo"

    assert hashed_key in mock_dbm

    # Manually add the cached response to the mock_dbm
    mock_dbm[hashed_key] = json.dumps({
        "etag": "some-etag",
        "file_path": str(file_path)
    })

    # Simulate a 304 Not Modified response
    mock_response_304 = MockDownloadResponse(content=b"", status_code=304)
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response_304)

    file_path_304 = download_file_with_cache(url, temp_file, params)

    # Check that the cached file path is returned
    assert file_path_304 == file_path

    captured = capfd.readouterr()
    assert "Cache hit: File not modified, using cached file." in captured.out


def test_cached_response_download_invalid_json(monkeypatch, capfd, temp_file, mock_dbm):
    params = {"id": 1}
    url = "http://www.example.com/example.txt"
    full_url = get_full_url(url, params)
    hashed_key = cache_key(full_url)

    # Inject invalid JSON into the mock_dbm
    mock_dbm[hashed_key] = b"invalid_json"

    # Set up the mock response for the first download
    mock_response = MockDownloadResponse(content=b"ItemOne,ItemTwo", status_code=200, headers={"ETag": "some-etag"})
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    # Call the function to trigger the JSONDecodeError
    file_path = download_file_with_cache(url, temp_file, params)

    # Check if the file was downloaded successfully
    with open(file_path, "rb") as f:
        assert f.read() == b"ItemOne,ItemTwo"

    # Ensure the cache was updated after downloading
    assert hashed_key in mock_dbm

    # Check for the warning output due to invalid JSON
    captured = capfd.readouterr()
    assert "Warning: Cached data is not valid JSON, proceeding to download the file." in captured.out
