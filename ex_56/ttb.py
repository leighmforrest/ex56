from ex_56.request import get_with_cache, get_without_cache, download_file_with_cache, download_file
from ex_56.soup import get_soup, get_files_from_links, get_filename
from ex_56.constants import TTB_URL, BASE_URL

markup_request_func = lambda cache=True: get_with_cache if cache else get_without_cache

download_request_func = lambda cache=True: download_file_with_cache if cache else download_file


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