import glob

import pandas as pd

from ex_56.constants import BASE_URL, TTB_URL
from ex_56.request import (
    download_file,
    download_file_with_cache,
    get_with_cache,
    get_without_cache,
)
from ex_56.soup import get_filename, get_files_from_links, get_soup


pd.set_option("future.no_silent_downcasting", True)

markup_request_func = lambda cache=True: get_with_cache if cache else get_without_cache

download_request_func = lambda cache=True: (
    download_file_with_cache if cache else download_file
)


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


def get_dataframes(target_dir):
    dataframes = []

    for spreadsheet in glob.glob(f"{target_dir}/*.xlsx"):
        df = pd.read_excel(spreadsheet)
        dataframes.append(df)

    return dataframes


def process_dataframe(dataframe):
    data = dataframe.iloc[[7, 8, 18], 3:].reset_index(drop=True)

    # Clean the columns
    data.columns = data.iloc[0].fillna("")
    data = data[1:].fillna(0)
    data.columns = data.columns.str.replace(
        r"Unnamed:\s*\d+", "", regex=True
    ).str.strip()
    data.columns = data.columns.str.replace(r"\n", " ", regex=True)
    data = data.rename(columns={"": "Metrics"})

    # Invert the dataframe
    data = data.T.reset_index(drop=False)
    data.columns = data.iloc[0]
    data = data[1:]
    data["Total Sales"] = data["Production"] - data["Stocks On Hand End-of-Month"]
    data.iloc[2:, 3] = "N/A"

    # Process the dates
    dates = (
        dataframe.iloc[[3, 4], 0].str.split(":").apply(lambda x: [s.strip() for s in x])
    )
    dates_dict = dict(tuple(dates))
    dates_dict = {k: pd.to_datetime(v) for k, v in dates_dict.items()}

    for k, v in dates_dict.items():
        data[k] = v.strftime("%Y-%m-%d")

    # Rearrange the columns
    data = data[
        [
            "Report Date",
            "Reporting Period",
            "Metrics",
            "Production",
            "Stocks On Hand End-of-Month",
            "Total Sales",
        ]
    ]

    # Hack to get DataFrame to pass the tests
    df_dict = data.to_dict()
    df = pd.DataFrame(df_dict)

    return df
