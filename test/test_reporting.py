from test.helpers import generate_test_markdown_reports
from ex56.reporting import generate_pdf, generate_html
from pathlib import Path


def test_generate_markdown_reports(tmpdir, reporting_df_tuples):
    tmpdir = Path(tmpdir)
    generate_test_markdown_reports(tmpdir, reporting_df_tuples)

    for _, filename, _ in reporting_df_tuples:
        assert (tmpdir / f"{filename}.md").exists()


def test_generate_pdf(tmpdir, reporting_df_tuples):
    tmpdir = Path(tmpdir)
    generate_test_markdown_reports(tmpdir, reporting_df_tuples)
    generate_pdf(tmpdir)
    
    # Compare the number of markdown files to the number of PDF files
    length_md = len(list(tmpdir.glob("*.md")))
    length_pdf = len(list(tmpdir.glob("*.pdf")))
    assert length_md == length_pdf


def test_generate_html(tmpdir, reporting_df_tuples):
    tmpdir = Path(tmpdir)
    generate_test_markdown_reports(tmpdir, reporting_df_tuples)
    generate_html(tmpdir)
    
    # Compare the number of markdown files to the number of html files
    length_md = len(list(tmpdir.glob("*.md")))
    length_html = len(list(tmpdir.glob("*.html")))
    assert length_md == length_html