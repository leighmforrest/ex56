import pytest
import glob
import pandas as pd
from ex56.helpers import get_pandas_reader, get_dataframes


@pytest.mark.parametrize("extension,expected", [
    ("csv", 3),
    ("xlsx", 2)
])
def test_get_dataframes(test_data_path, extension, expected):
    reader = get_pandas_reader(extension)
    data_files = glob.glob(f"{test_data_path}/*.{extension}")
    
    test_dataframes = [reader(data_file) for data_file in data_files]

    dataframes = get_dataframes(test_data_path)

    dfs = zip(test_dataframes, dataframes)
    
    assert len(list(dfs)) == expected
    for df in dfs:
        pd.testing.assert_frame_equal(df[0], df[1])


def test_get_dataframes_ineligible_extension(capsys, test_data_path):

    dfs = get_dataframes(test_data_path, "txt")
    captured = capsys.readouterr()

    assert dfs == []
    assert f"Extension txt is not compatible." in captured.out
