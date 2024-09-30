import argparse
from pathlib import Path

import pandas as pd

from videos import get_courses, get_modules, get_lessons
from ex56.ttb import get_xlsx_links, download_spreadshets, get_dataframes
from constants import BASE_DIR, BASE_URL, DOWNLOAD_DIR

CHOICES = {
    "ttb": 0b10,
    "videos": 0b01,
    "both": 0b11
}

if __name__ == "__main__":
    # module_ids = get_courses(BASE_DIR / "data")
    # lesson_ids = get_modules(module_ids, BASE_DIR / "data")
    # get_lessons(lesson_ids, BASE_DIR / "data")
    # lessons = pd.read_csv(BASE_DIR / "data" / "lessons.csv")
    # raw_modules = pd.read_csv(BASE_DIR / "data" / "modules.csv")

    # # print(lessons.head())
    # # print(raw_modules.head())
    # modules = pd.merge(
    #     lessons, raw_modules, left_on="module_id", right_on="id", how="inner"
    # ).dropna(subset=["module_id", "duration"])

    # grouped_modules = (
    #     modules.groupby("module_id")
    #     .agg(
    #         {
    #             "title_y": "first",
    #             "description_y": "first",
    #             "product_id": "first",
    #             "duration": "sum",
    #         }
    #     )
    #     .reset_index()
    # )

    # grouped_modules.columns = [
    #     "module_id",
    #     "module_title",
    #     "module_description",
    #     "product_id",
    #     "total_duration",
    # ]

    # grouped_modules = grouped_modules.sort_values(by=[ "product_id","module_id", ]).reset_index(drop=True)

    # print(lessons)
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", help="To make a report based on TTB data, or videos data, or both",
                        choices=CHOICES.keys(),
                        default="both")
    parser.add_argument("--pdf", help="to make pdf reports if true, html if not set", action="store_true")
    parser.add_argument("--download", help="to directly download instead of cache", action="store_true")
    args = parser.parse_args()
    
    reports = int(CHOICES[args.reports])
    ttb = bool(CHOICES["ttb"] & reports)
    videos = bool(CHOICES["videos"] & reports)
    cached = not args.download # opposite of dowload is cached
    pdf = args.pdf
    reports = []

    if ttb:
        print("TTB REPORTING")
        links = get_xlsx_links(cached)
        download_spreadshets(links, DOWNLOAD_DIR, cached)
        dataframes = get_dataframes(DOWNLOAD_DIR)

        for df in dataframes:
            print(df.iloc[3:5,0])
    if videos:
        print("VIDEO REPORTING")