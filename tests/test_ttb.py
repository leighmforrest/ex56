import pytest
from ex56.ttb import get_ttb_markup, get_xlsx_links, download_spreadshets, get_filename


@pytest.mark.parametrize("cached", [True, False])
def test_get_ttb_markup(cached, markup, mock_markup_request):
    assert markup == get_ttb_markup(cached)


@pytest.mark.parametrize("cached", [True, False])
def test_xlsx_links(markup, mock_markup_request, cached):
    links = get_xlsx_links(cached)
    print(links)
    assert len(links) == 2


@pytest.mark.parametrize("cached", [True, False])
def test_download_spreadsheets(cached, tmpdir, mock_spreadsheet_download, test_excel_spreadsheet):
    links = ['https://learncodethehardway.com/setup/python/ttb/pdfs/Statistical_Report_Beer_October_2021.xlsx', 'https://learncodethehardway.com/setup/python/ttb/pdfs/Statistical_Report_Beer_November_2021.xlsx']
    expected_filenames = [get_filename(link) for link in links]
    download_spreadshets(links, tmpdir, cached)

    for spreadsheet in expected_filenames:
        assert (tmpdir / spreadsheet).exists()
