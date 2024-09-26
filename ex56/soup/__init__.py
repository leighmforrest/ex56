from bs4 import BeautifulSoup

get_soup = lambda markup: BeautifulSoup(markup, features="html.parser")


def get_files_from_links(soup, file_extension="pdf"):
    # get all of the links from the soup
    links = soup.find_all(
        "a", href=lambda href: href and href.endswith(f".{file_extension}")
    )
    files = [link["href"] for link in links]
    print(files)
    return files
