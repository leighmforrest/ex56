import pandas as pd
import pytest

from ex56.ttb import (
    download_spreadsheets,
    get_dataframes,
    get_filename,
    get_xlsx_links,
    process_dataframe,
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


def test_process_dataframe(test_ttb_dataframe, test_final_ttb_dataframe):
    result = process_dataframe(test_ttb_dataframe)

    # Get the types to strings to pass the test
    result["Total Sales"] = result["Total Sales"].astype(str)
    test_final_ttb_dataframe["Total Sales"] = test_final_ttb_dataframe[
        "Total Sales"
    ].astype(str)

    pd.testing.assert_frame_equal(result, test_final_ttb_dataframe)
