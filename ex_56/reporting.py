import pandas as pd

def generate_markdown_reports(target_dir, df_tuples):
    """Dataframes are tuples:
        0: a pandas dataframe
        1: file name
        2: format
    """
    for df_tuple in df_tuples:
        pd.set_option('display.float_format', df_tuple[2])
        df_tuple[0].to_markdown(target_dir / f"{df_tuple[1]}.md")