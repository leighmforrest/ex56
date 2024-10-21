import pytest
import json
import requests

from test.helpers import generate_cache_key
from test.mocks import MockResponse
from test.data_for_tests import REQUEST_SET
from ex_56.request import get_with_cache

@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_cache_miss(capsys, monkeypatch, mock_dbm, url, params, data, etag):
    # make a cached item
    cache_key = generate_cache_key(url, params)
    bogus_data = f"{data}-old"
    data_dict = {"etag": f"{etag}Mi$$", "body": bogus_data}
    mock_dbm[cache_key] = json.dumps(data_dict)

    # mock a 200 response
    mock_response = MockResponse(data, status_code=200, headers={"ETag": etag})
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    result = get_with_cache(url, params)
    captured = capsys.readouterr()

    assert result == data 
    assert cache_key in mock_dbm
    assert json.dumps(bogus_data) not in mock_dbm[cache_key]
    assert json.dumps(data) in mock_dbm[cache_key]
    assert f"Cache miss: {url}" in captured.out


@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_get_with_cache_not_cached(monkeypatch, mock_dbm, url, params, data, etag):
    mock_response = MockResponse(data, status_code=200, headers={"ETag": etag})
    monkeypatch.setattr("requests.get", lambda url, headers=None: mock_response)

    cache_key = generate_cache_key(url, params)
    result = get_with_cache(url, params)

    assert result == data
    assert cache_key in mock_dbm

@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_get_with_cache_hit(capsys, monkeypatch, mock_dbm, url, params, data, etag):
    cache_key = generate_cache_key(url, params)
    data_dict = {"etag": etag, "body": data}
    mock_dbm[cache_key] = json.dumps(data_dict)

    # Mock a 304 response
    mock_response = MockResponse("", status_code=304)
    monkeypatch.setattr("requests.get", lambda url, headers=None:mock_response)

    result = get_with_cache(url, params)
    captured = capsys.readouterr()

    assert result == data
    assert cache_key in mock_dbm
    assert json.dumps(data_dict) in mock_dbm[cache_key]
    assert f"Cache hit: {url}" in captured.out


@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_get_with_cache_not_found_404_cached(monkeypatch, mock_dbm, url, params, data, etag):
    cache_key = generate_cache_key(url, params)
    data_dict = {"etag": etag, "body": data}
    mock_dbm[cache_key] = json.dumps(data_dict)

    # Mock a 304 response
    mock_response = MockResponse("", status_code=404)
    monkeypatch.setattr("requests.get", lambda url, headers=None:mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        get_with_cache(url, params)


@pytest.mark.parametrize("url,params,etag,data", REQUEST_SET)
def test_get_with_cache_not_found_404_not_cached(monkeypatch, mock_dbm, url, params, data, etag):
    # Mock a 304 response
    mock_response = MockResponse("", status_code=404)
    monkeypatch.setattr("requests.get", lambda url, headers=None:mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        get_with_cache(url, params)