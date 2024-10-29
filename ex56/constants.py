BASE_URL = BASE_URL = "https://learncodethehardway.com"
BASE_API_URL = f"{BASE_URL}/api"
TTB_URL = f"{BASE_URL}/setup/python/ttb/"
PYPANDOC_EXTRA_ARGS = [
    "--pdf-engine=xelatex",
    "-V",
    "geometry:landscape",  # Set landscape orientation
    "-V",
    "fontsize=10pt",
    "-V",
    "geometry:margin=1in",
    "-V",
    "geometry:headheight=25pt",
    "-V",
    "geometry:headsep=0.25in",
    "-V",
    "geometry:columnsep=1in",
]
