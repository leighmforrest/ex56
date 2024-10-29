from ex56.request import get_cache_key, get_full_url
from ex56.ttb import download_spreadsheets
from ex56.reporting import generate_markdown_reports

generate_cache_key = lambda url, params: get_cache_key(get_full_url(url, params))


def assert_common_keys(result, expected_keys):
    """Test that the keys are expected."""
    assert len(result) == len(expected_keys)

    for key in expected_keys:
        assert key in result


def download_spreadsheets_helper(mock_spreadsheet_download, xlsx_links, tmpdir, cached):
    download_spreadsheets(xlsx_links, tmpdir, cached)


def generate_test_markdown_reports(tmpdir, reporting_df_tuples):
    """Runs"""
    generate_markdown_reports(tmpdir, reporting_df_tuples)
