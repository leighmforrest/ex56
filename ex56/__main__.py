from pathlib import Path

from videos import get_courses, get_modules


BASE_DIR = Path(__file__).resolve().parent
BASE_URL = "https://learncodethehardway.com/api"


if __name__ == "__main__":
    module_ids = get_courses(BASE_DIR / "data", "courses.csv")
    get_modules(module_ids, BASE_DIR / "data", "modules.csv")
