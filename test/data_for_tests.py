import pandas as pd


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
    "module": [
        {
            "id": 101,
            "title": "Module 101",
            "description": "Description for Module 101",
            "green": "blue",
            "product_id": 1,
            "lessons": [{"id": 1101}, {"id": 1102}],
        },
        {
            "id": 102,
            "title": "Module 102",
            "description": "Description for Module 102",
            "product_id": 1,
            "green": "blue",
            "lessons": [{"id": 2201}, {"id": 2202}],
        },
        {
            "id": 201,
            "product_id": 2,
            "title": "Module 201",
            "description": "Description for Module 201",
            "green": "blue",
            "lessons": [{"id": 3201}, {"id": 3202}],
        },
        {
            "id": 202,
            "product_id": 2,
            "title": "Module 202",
            "description": "Description for Module 202",
            "green": "blue",
            "lessons": [{"id": 4201}, {"id": 4202}],
        },
    ],
    "lesson": [
        {
            "id": 1101,
            "module_id": 101,
            "title": "Lesson 1101",
            "description": "The lesson 1101",
            "media": [{"duration": 100.01}, {"duration": 100.01}],
        },
        {
            "id": 1102,
            "module_id": 101,
            "title": "Lesson 1102",
            "description": "The lesson 1102",
            "media": [],
        },
        {
            "id": 2201,
            "module_id": 102,
            "title": "Lesson 2201",
            "description": "The lesson 2201",
            "media": [],
        },
        {
            "id": 2202,
            "module_id": 102,
            "title": "Lesson 2202",
            "description": "The lesson 2202",
            "media": [],
        },
        {
            "id": 3201,
            "module_id": 201,
            "title": "Lesson 3201",
            "description": "The lesson 3201",
            "media": [{"duration": 100.01}],
        },
        {
            "id": 3202,
            "module_id": 201,
            "title": "Lesson 3202",
            "description": "The lesson 3202",
            "media": [{"duration": 100.01}],
        },
        {
            "id": 4201,
            "module_id": 202,
            "title": "Lesson 4201",
            "description": "The lesson 4201",
            "media": [{"duration": 1.0}],
        },
        {
            "id": 4202,
            "module_id": 202,
            "title": "Lesson 4202",
            "description": "The lesson 4202",
            "media": [],
        },
    ],
}


VIDEOS_EXPECTED_DATAFRAME_DATA = {
    "courses": [
        {"id": 1, "title": "course 1"},
        {"id": 2, "title": "course 2"},
    ],
    "modules": [
        {
            "id": 101,
            "title": "Module 101",
            "product_id": 1,
        },
        {
            "id": 102,
            "title": "Module 102",
            "product_id": 1,
        },
        {
            "id": 201,
            "title": "Module 201",
            "product_id": 2,
        },
        {
            "id": 202,
            "title": "Module 202",
            "product_id": 2,
        },
    ],
    "lessons": [
        {
            "id": 1101,
            "module_id": 101,
            "title": "Lesson 1101",
            "duration": 200.02,
        },
        {
            "id": 1102,
            "module_id": 101,
            "title": "Lesson 1102",
            "duration": 0,
        },
        {
            "id": 2201,
            "module_id": 102,
            "title": "Lesson 2201",
            "duration": 0,
        },
        {
            "id": 2202,
            "module_id": 102,
            "title": "Lesson 2202",
            "duration": 0,
        },
        {
            "id": 3201,
            "module_id": 201,
            "title": "Lesson 3201",
            "duration": 100.01,
        },
        {
            "id": 3202,
            "module_id": 201,
            "title": "Lesson 3202",
            "duration": 100.01,
        },
        {
            "id": 4201,
            "module_id": 202,
            "title": "Lesson 4201",
            "duration": 1.0,
        },
        {
            "id": 4202,
            "module_id": 202,
            "title": "Lesson 4202",
            "duration": 0,
        },
    ],
}


EXPECTED_IDS = {
    "courses": [1, 2],
    "modules": [
        101,
        102,
        201,
        202,
    ],
    "lessons": [1101, 1102, 2201, 2202, 3201, 3202, 4201, 4202],
}

FINAL_EXPECTED_VIDEOS_DATAFRAMES = {
    "modules": {
        "id": {0: 101, 1: 102, 2: 201, 3: 202},
        "title": {0: "Module 101", 1: "Module 102", 2: "Module 201", 3: "Module 202"},
        "product_id": {0: 1, 1: 1, 2: 2, 3: 2},
        "duration": {0: 200.02, 1: 0.0, 2: 200.02, 3: 1.0},
    },
    "courses": {
        "product_id": {0: 1, 1: 2},
        "title": {0: "course 1", 1: "course 2"},
        "duration": {0: 200.02, 1: 201.02},
    },
}
