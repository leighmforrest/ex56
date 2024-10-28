import argparse
from pathlib import Path

from ttb import get_xlsx_links, download_spreadsheets,get_dataframes, process_dataframe
from reporting import generate_markdown_reports

BASE_DIR = Path(__file__).parent.resolve()

reporting_dataframes = []

def videos():
    print("Now processing videos...")


def ttb(cached, target_directory):
    print("Now processing TTB data...")
    links = get_xlsx_links(cached)
    download_spreadsheets(links, target_directory, cached)
    dataframes = get_dataframes(target_directory)    
    report_df_tuples = [(process_dataframe(dataframe), f"ttb_{index}", ".0f".format,) for index, dataframe in enumerate(dataframes)]

    generate_markdown_reports(target_directory, report_df_tuples)


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

    # if option_flag & 0b10:
    #     videos()
    # if option_flag & 0b10:
    ttb(cached, target_directory)
    generate_markdown_reports(target_directory, reporting_dataframes)