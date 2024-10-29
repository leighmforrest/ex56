from test.data_for_tests import BASE_MARKUP, FILES, LINKS

import pytest
from bs4 import BeautifulSoup

from ex56.soup import get_filename, get_files_from_links, get_soup


@pytest.mark.parametrize(
    "markup",
    [BASE_MARKUP.format("<p>Hello World!!!!</p>"), BASE_MARKUP.format("<a>Link</a>")],
)
def test_get_soup(markup):
    soup = get_soup(markup)

    assert str(soup) == markup
    assert isinstance(soup, BeautifulSoup)


@pytest.mark.parametrize("url,filename", zip(LINKS, FILES))
def test_get_filename(url, filename):
    assert get_filename(url) == filename


def test_get_files_from_links_no_argument(link_soup):
    files = get_files_from_links(link_soup)
    assert len(files) == 4


@pytest.mark.parametrize(
    "extension,n", [("txt", 1), ("doc", 1), ("dat", 0), ("pdf", 4)]
)
def test_get_files_from_links(extension, n, link_soup):
    files = get_files_from_links(link_soup, extension)
    assert len(files) == n
