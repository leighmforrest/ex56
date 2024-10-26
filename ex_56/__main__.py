from pathlib import Path
import pandas as pd
from ex_56.ttb import get_xlsx_links, process_dataframe


spreadsheet_path = Path(__file__).parent.parent / "test/data_files/test.xlsx"

if __name__ == "__main__":
    dataframe = pd.read_excel(spreadsheet_path)
    df = process_dataframe(dataframe)
    print(df.to_dict())
