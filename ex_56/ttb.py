import glob

import pandas as pd

from ex_56.constants import BASE_URL, TTB_URL
from ex_56.request import (
    download_file,
    download_file_with_cache,
    get_with_cache,
    get_without_cache,
)
from ex_56.soup import get_filename, get_files_from_links, get_soup

markup_request_func = lambda cache=True: get_with_cache if cache else get_without_cache

download_request_func = lambda cache=True: (
    download_file_with_cache if cache else download_file
)


# Get the links
def get_xlsx_links(cached=True):
    """Get all of the links that point to xlsx files."""
    func = markup_request_func(cached)
    markup = func(TTB_URL)

    soup = get_soup(markup)
    raw_file_paths = get_files_from_links(soup, "xlsx")

    urls = [f"{BASE_URL}{raw_file_path}" for raw_file_path in raw_file_paths]

    return urls


def download_spreadsheets(links, target_dir, cached=True):
    func = download_request_func(cached)

    for link in links:
        filename = get_filename(link)
        func(link, target_dir / filename)
        print(f"{filename} downloaded into {target_dir}")


def get_dataframes(target_dir):
    dataframes = []

    for spreadsheet in glob.glob(f"{target_dir}/*.xlsx"):
        df = pd.read_excel(spreadsheet)
        dataframes.append(df)

    return dataframes
