import os
from bs4 import BeautifulSoup

# Lambda for creating a soup, given a markup string.
get_soup = lambda markup: BeautifulSoup(markup, features="html.parser")

# Lambda for getting the filename out of the url
get_filename = lambda url: os.path.basename(url)


def get_files_from_links(soup, file_extension="pdf"):
    """Get all of the links with the given file extension."""

    # get all of the links from the soup
    links = soup.find_all(
        "a", href=lambda href: href and href.endswith(f".{file_extension}")
    )
    files = [link["href"] for link in links]
    
    return files
