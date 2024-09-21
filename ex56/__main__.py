from pathlib import Path
from urllib.parse import urlsplit
from request import get_cached_response_with_etag, get_non_cached_response, download_file

BASE_DIR = Path(__file__).resolve().parent
filename = lambda url: Path(urlsplit(url).path).name

if __name__ == "__main__":
    url = "https://learncodethehardway.com/setup/python/ttb/pdfs/Statistical_Report_Beer_October_2021.xlsx"
    download_file(url, BASE_DIR / "data" / filename(url))