from pprint import pprint
from pathlib import Path

from request import get_full_url, get_cached_response, download_file_with_cache


BASE_DIR = Path(__file__).resolve().parent
BASE_URL = "https://learncodethehardway.com/api"


if __name__ == "__main__":
    file_path = BASE_DIR / "data" / "data.xlsx"
    download_file_with_cache("https://learncodethehardway.com/setup/python/ttb/pdfs/Statistical_Report_Beer_December_2021_revised.pdf",
                             file_path)