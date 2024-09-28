from ex56.soup import get_soup, get_files_from_links, get_filename
from ex56.constants import BASE_DIR, BASE_URL


def get_xlsx_links():
    url = f"{BASE_URL}/setup/python/ttb/"
    soup = get_soup(url)
    file_paths = get_files_from_links(soup, "xlsx")
    print(file_paths)