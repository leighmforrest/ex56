from pathlib import Path

import pandas as pd

from videos import get_courses, get_modules, get_lessons


BASE_DIR = Path(__file__).resolve().parent
BASE_URL = "https://learncodethehardway.com/api"


if __name__ == "__main__":
    # module_ids = get_courses(BASE_DIR / "data")
    # lesson_ids = get_modules(module_ids, BASE_DIR / "data")
    # get_lessons(lesson_ids, BASE_DIR / "data")
    lessons = pd.read_csv(BASE_DIR / "data" / "lessons.csv")
    raw_modules = pd.read_csv(BASE_DIR / "data" / "modules.csv")

    # print(lessons.head())
    # print(raw_modules.head())
    modules = pd.merge(
        lessons, raw_modules, left_on="module_id", right_on="id", how="inner"
    ).dropna(subset=["module_id", "duration"])

    grouped_modules = (
        modules.groupby("module_id")
        .agg(
            {
                "title_y": "first",
                "description_y": "first",
                "product_id": "first",
                "duration": "sum",
            }
        )
        .reset_index()
    )

    grouped_modules.columns = [
        "module_id",
        "module_title",
        "module_description",
        "product_id",
        "total_duration",
    ]

    grouped_modules = grouped_modules.sort_values(by=[ "product_id","module_id", ]).reset_index(drop=True)

    print(lessons)
