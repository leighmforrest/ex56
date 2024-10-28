from pathlib import Path
from ex_56.reporting import generate_markdown_reports

def test_generate_markdown_reports(tmpdir, final_courses_dataframe, final_modules_dataframe, lesson_dataframe, test_final_ttb_dataframe):
    reporting_df_tuples = [
        (test_final_ttb_dataframe, f"ttb", ".0f".format),
        (final_modules_dataframe,f"modules", "{:.3f}".format),
        (final_courses_dataframe,f"modules", "{:.3f}".format),
    ]
    generate_markdown_reports(tmpdir, reporting_df_tuples)

    for df_tuple in reporting_df_tuples:
        assert (tmpdir / f"{df_tuple[1]}.md").exists()
