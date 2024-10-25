import pandas as pd
import pytest

from ex_56.ttb import (
    download_spreadsheets,
    get_dataframes,
    get_filename,
    get_xlsx_links,
)


@pytest.mark.parametrize("cached", [True, False])
def test_get_files_from_links(markup, mock_markup_request, cached):
    links = get_xlsx_links(cached)
    assert len(links) == 2


@pytest.mark.parametrize("cached", [True, False])
def test_download_spreadsheets(test_download_spreadsheet, xlsx_links, tmpdir):
    expected_filenames = [get_filename(link) for link in xlsx_links]

    for spreadsheet in expected_filenames:
        assert (tmpdir / spreadsheet).exists()


@pytest.mark.parametrize("cached", [True, False])
def test_get_dataframes(test_download_spreadsheet, tmpdir, test_ttb_dataframe):
    results = get_dataframes(tmpdir)

    for result in results:
        pd.testing.assert_frame_equal(result, test_ttb_dataframe)
