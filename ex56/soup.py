import os

from bs4 import BeautifulSoup

# Lambda for creating soup, given a markup string
get_soup = lambda markup: BeautifulSoup(markup, features="html.parser")

# Lambda for getting a filename out of a url
get_filename = lambda url: os.path.basename(url)


def get_files_from_links(soup, extension="pdf"):
    """Get all of the links with the given file extension."""
    links = soup.find_all(
        "a", href=lambda href: href and href.endswith(f".{extension}")
    )
    files = [link["href"] for link in links]
    return files
