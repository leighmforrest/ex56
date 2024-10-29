import argparse
from pathlib import Path

from ex56.reporting import generate_markdown_reports, generate_pdf, generate_html
from ex56.ttb import (
    download_spreadsheets,
    get_dataframes,
    get_xlsx_links,
    process_dataframe,
)
from ex56.videos import (
    get_course_dataframe,
    get_lesson_dataframe,
    get_module_dataframe,
    process_courses_dataframe,
    process_modules_dataframe,
)

BASE_DIR = Path(__file__).parent.resolve()

reporting_dataframes = []


def videos(cached):
    print("Now processing videos...")
    course_df, module_ids = get_course_dataframe(cached)
    module_df, lesson_ids = get_module_dataframe(module_ids, cached)
    lesson_df = get_lesson_dataframe(lesson_ids, cached)

    # process the dataframes
    final_module_dataframe = process_modules_dataframe(lesson_df, module_df)
    final_course_dataframe = process_courses_dataframe(
        final_module_dataframe, course_df
    )

    reporting_dataframes.extend(
        [
            (lesson_df, "lessons", "{:.3f}".format),
            (final_module_dataframe, "modules", "{:.3f}".format),
            (final_course_dataframe, "courses", "{:.3f}".format),
        ]
    )


def ttb(cached):
    print("Now processing TTB data...")
    links = get_xlsx_links(cached)
    download_spreadsheets(links, target_directory, cached)
    dataframes = get_dataframes(target_directory)
    reporting_dataframes.extend(
        [
            (
                process_dataframe(dataframe),
                f"ttb_{index}",
                ".0f".format,
            )
            for index, dataframe in enumerate(dataframes)
        ]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Ex56", description="Generate reports in HTML and PDF for TTB and Videos"
    )

    parser.add_argument(
        "--option",
        choices=["ttb", "videos", "both"],
        default="both",
        help="Choose which report you want, or run both",
    )
    parser.add_argument(
        "--format",
        choices=["html", "pdf"],
        default="pdf",
        help="Choose the report format",
    )
    parser.add_argument(
        "--download",
        action="store_false",
        help="Direct download instead of using caching (default is caching)",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=Path,
        default=BASE_DIR,
        help="Directory to download artifacts.",
    )
    args = parser.parse_args()
    option = args.option
    if option == "ttb":
        option_flag = 0b01
    elif option == "videos":
        option_flag = 0b10
    else:
        option_flag = 0b11

    cached = args.download
    report_format = args.format
    directory = args.directory

    # get or create the target directory
    target_directory = directory / "reports"

    if not target_directory.exists():
        target_directory.mkdir(parents=True)
        print("Directory created!")

    if option_flag & 0b10:
        videos(cached)
    if option_flag & 0b01:
        ttb(cached)

    # Generate markdown reports
    generate_markdown_reports(target_directory, reporting_dataframes)

    # Generate the appropriate
    if report_format == "html":
        generate_html(target_directory)
    else:
        generate_pdf(target_directory)
