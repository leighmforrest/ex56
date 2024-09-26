from pathlib import Path

from videos import get_courses


BASE_DIR = Path(__file__).resolve().parent
BASE_URL = "https://learncodethehardway.com/api"


if __name__ == "__main__":
    get_courses(BASE_DIR / "data", "courses.csv")
