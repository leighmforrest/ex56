from pathlib import Path
from urllib.parse import urlsplit
from soup import get_soup, get_files_from_links
from request import get_cached_response_with_etag, get_non_cached_response, download_file
import pandas as pd 


BASE_DIR = Path(__file__).resolve().parent
BASE_URL = "https://learncodethehardway.com"
filename = lambda url: Path(urlsplit(url).path).name

if __name__ == "__main__":
    # url = "https://learncodethehardway.com/setup/python/ttb/pdfs/Statistical_Report_Beer_October_2021.xlsx"
    # file_path = BASE_DIR / "data" / filename(url)
    # download_file(url, file_path)
    # ds = pd.read_excel(file_path).fillna(0)
    # print(ds)
    url = f"{BASE_URL}/setup/python/ttb/"
    markup = get_cached_response_with_etag(url)
    soup = get_soup(markup)
    links = get_files_from_links(soup, "xlsx")

    for spreadsheet in links:
        url = f"{BASE_URL}/{spreadsheet}"
        file_path = BASE_DIR / "data" / filename(url)
        download_file(url, file_path)
        ds = pd.read_excel(file_path).fillna(0)
        print(ds)
