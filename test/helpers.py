from ex_56.request import get_cache_key, get_full_url

generate_cache_key = lambda url, params: get_cache_key(get_full_url(url, params))


def assert_common_keys(result, expected_keys):
    """Test that the keys are expected."""
    assert len(result) == len(expected_keys)

    for key in expected_keys:
        assert key in result
