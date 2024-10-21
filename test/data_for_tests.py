REQUEST_SET = [
    ("http://www.example.com", {"id": 1}, "etag1", '{"hello": "world"}'),
    ("http://www.goggles.com", {"course_id": 2}, "etag2", '{"id": 2}'),
    (
        "http://www.giggle.com",
        {"course_id": 666},
        "etag3",
        "<html><p>Hello World!</p></html>",
    ),
    ("http://www.goggles.com", None, "etag4", '{"id": 2}'),
]

# Data for testing soup
BASE_MARKUP = "<html>{}</html>"

LINKS = [
    "https://learncodethehardway.com/setup/python/ttb/pdfs/Statistical_Report_Beer_November_2021.pdf",
    "/setup/python/ttb/pdfs/Statistical_Report_Beer_November_2021.pdf",
    "https://learncodethehardway.com/setup/python/ttb/pdfs/Statistical_Report_Beer_October_2021.pdf",
    "/setup/python/ttb/pdfs/Statistical_Report_Beer_October_2021.pdf",
    "http://google.com/data.doc",
    "http://www.example.com/data.txt",
]

FILES = [
    "Statistical_Report_Beer_November_2021.pdf",
    "Statistical_Report_Beer_November_2021.pdf",
    "Statistical_Report_Beer_October_2021.pdf",
    "Statistical_Report_Beer_October_2021.pdf",
    "data.doc",
    "data.txt",
]

LINK_MARKUP = "".join([f'<a href="{link}">Link</a>' for link in LINKS])

# VIDEOS TEST DATA
API_DATA = {
    "courses": [
        {"id": 1, "title": "course 1", "green": "blue"},
        {"id": 2, "title": "course 2", "green": "red"},
    ],
    "course": [
        {
            "id": 1,
            "title": "course 1",
            "description": "Description for course 1",
            "green": "blue",
            "modules": [{"id": 101}, {"id": 102}],
        },
        {
            "id": 2,
            "title": "course 2",
            "description": "Description for course 2",
            "green": "blue",
            "modules": [{"id": 201}, {"id": 202}],
        },
    ],
}
