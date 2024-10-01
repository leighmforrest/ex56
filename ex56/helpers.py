import glob
from pathlib import Path
import pandas as pd
from ex56.request import (
    get_cached_response,
    get_uncached_response,
    download_file_with_cache,
    download_file_without_cache,
)


def get_api_request_func(cached=True):
    """Get an api request function based on whether the request is cached or not."""
    if cached:
        return get_cached_response
    else:
        return get_uncached_response


def get_download_function(cached=True):
    """Download a file based on if request is to be cached or not."""
    if cached:
        return download_file_with_cache
    else:
        return download_file_without_cache


def get_pandas_reader(file_extension):
    """Get a pandas file reader function"""
    if file_extension == "csv":
        reader = pd.read_csv
    elif file_extension == "xlsx":
        reader = pd.read_excel
    else:
        raise ValueError(f"Extension {file_extension} is not compatible.")
    
    return reader


def get_dataframes(target_dir, file_extension="csv"):
    """Get dataframes from a certain filetype in a target directory"""
    try:
        reader = get_pandas_reader(file_extension)

        # get all the files with the extension in directory
        data_files = [str(Path(file).resolve()) for file in glob.glob(f"{target_dir}/*.{file_extension}")]

        dataframes = [reader(data_file) for data_file in data_files]

        return dataframes
    except ValueError as e:
        print(f"ValueError: {e}")
        return []
    
