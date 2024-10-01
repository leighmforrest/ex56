import glob
import pandas as pd
from ex56.soup import get_soup, get_files_from_links, get_filename
from ex56.request import get_cached_response, get_uncached_response
from ex56.constants import TTB_URL, BASE_URL
from ex56.helpers import get_download_function


def get_ttb_markup(cached=True):
    if cached:
        return get_cached_response(TTB_URL, response_type="html")
    else:
        return get_uncached_response(TTB_URL, response_type="html")


def get_xlsx_links(cached=True):
    url = TTB_URL
    markup = get_ttb_markup(cached)

    soup = get_soup(markup)
    raw_file_paths = get_files_from_links(soup, "xlsx")

    urls =  [f"{BASE_URL}{raw_file_path}" for raw_file_path in raw_file_paths]
    
    return urls


def download_spreadshets(links, target_dir, cached=True):
    download_function = get_download_function(cached)

    for link in links:
        filename = get_filename(link)
        download_function(link, target_dir / filename)
        print(f"{filename} downloaded into {target_dir}")
