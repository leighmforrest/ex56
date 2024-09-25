import pytest
from ex56.soup import get_soup,get_files_from_links

BASE_MARKUP = "<html>{}</html>"
LINKS = [
    "https://learncodethehardway.com/setup/python/ttb/pdfs/Statistical_Report_Beer_November_2021.pdf",
    "/setup/python/ttb/pdfs/Statistical_Report_Beer_November_2021.pdf",
    "https://learncodethehardway.com/setup/python/ttb/pdfs/Statistical_Report_Beer_October_2021.pdf",
    "/setup/python/ttb/pdfs/Statistical_Report_Beer_October_2021.pdf",
    "http://google.com/data.doc",
    "http://www.example.com/data.txt"
]

LINK_MARKUP = "".join([f'<a href="{link}">Link</a>' for link in LINKS])


@pytest.mark.parametrize("markup", [
    BASE_MARKUP.format("<p>Hello World!!!!</p>"),
    BASE_MARKUP.format('<a href="http://www.google.com">Link</a>')
])
def test_get_soup(markup):
    soup = get_soup(markup)

    assert str(soup) == markup


def test_get_files_from_links():
    markup = BASE_MARKUP.format(LINK_MARKUP)
    soup = get_soup(markup)
    files = get_files_from_links(soup)

    assert len(files) == 4


@pytest.mark.parametrize("extension, n", [
    ("txt",1),
    ("doc", 1),
    ("dat", 0)
])
def test_get_non_pdfs_from_links(extension, n):
    markup = BASE_MARKUP.format(LINK_MARKUP)
    soup = get_soup(markup)
    files = get_files_from_links(soup, extension)
    assert len(files) == n