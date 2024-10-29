from pathlib import Path
import pandas as pd
import pypandoc
import markdown
from ex56.constants import PYPANDOC_EXTRA_ARGS


def generate_markdown_reports(target_dir, df_tuples):
    """Dataframes are tuples:
    0: a pandas dataframe
    1: file name
    2: format
    """
    target_dir = Path(target_dir)
    for df, filename, float_format in df_tuples:
        pd.set_option("display.float_format", float_format)
        markdown_text = df.to_markdown(index=False)
        with open(target_dir / f"{filename}.md", "w") as f:
            f.write(markdown_text)
        pd.reset_option("display.float_format")


def generate_pdf(target_dir):
    """Generate a PDF file from markdown files in the target directory."""
    target_dir = Path(target_dir)
    for md_file in target_dir.glob("*.md"):
        basename = md_file.stem
        outfile = target_dir / f"{basename}.pdf"

        with open(md_file, "r") as f:
            md_text = f.read()

        pypandoc.convert_text(
            md_text,
            "pdf",
            outputfile=str(outfile),
            format="markdown",
            extra_args=PYPANDOC_EXTRA_ARGS,
        )


def generate_html(target_dir):
    # get all markdown files
    for md_file in target_dir.glob("*.md"):
        basename = md_file.stem
        outfile = target_dir / f"{basename}.html"

        with open(md_file, "r") as f:
            md_text = f.read()

        html = markdown.markdown(md_text, extensions=["tables"])

        # write html string to file
        with open(outfile, "w") as f:
            f.write(html)
