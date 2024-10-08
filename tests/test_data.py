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
            "product_id": 1,
            "description": "Description for Module 101",
            "green": "blue",
            "lessons": [{"id": 1101}, {"id": 1102}],
        },
        {
            "id": 102,
            "product_id": 1,
            "title": "Module 102",
            "description": "Description for Module 102",
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

EXPECTED_IDS = {
    "modules": [
        101,
        102,
        201,
        202,
    ],
    "lessons": [1101, 1102, 2201, 2202, 3201, 3202, 4201, 4202],
}


EXPECTED_CSV_DATA = {
    "courses": [
        {"id": "1", "title": "course 1", "description": "Description for course 1"},
        {"id": "2", "title": "course 2", "description": "Description for course 2"},
    ],
    "modules": [
        {
            "id": "101",
            "product_id": "1",
            "title": "Module 101",
            "description": "Description for Module 101",
        },
        {
            "id": "102",
            "product_id": "1",
            "title": "Module 102",
            "description": "Description for Module 102",
        },
        {
            "id": "201",
            "product_id": "2",
            "title": "Module 201",
            "description": "Description for Module 201",
        },
        {
            "id": "202",
            "product_id": "2",
            "title": "Module 202",
            "description": "Description for Module 202",
        },
    ],
    "lessons": [
        {
            "id": "1101",
            "module_id": "101",
            "title": "Lesson 1101",
            "description": "The lesson 1101",
            "duration": "200.02",
        },
        {
            "id": "1102",
            "module_id": "101",
            "title": "Lesson 1102",
            "description": "The lesson 1102",
            "duration": "0",
        },
        {
            "id": "2201",
            "module_id": "102",
            "title": "Lesson 2201",
            "description": "The lesson 2201",
            "duration": "0",
        },
        {
            "id": "2202",
            "module_id": "102",
            "title": "Lesson 2202",
            "description": "The lesson 2202",
            "duration": "0",
        },
        {
            "id": "3201",
            "module_id": "201",
            "title": "Lesson 3201",
            "description": "The lesson 3201",
            "duration": "100.01",
        },
        {
            "id": "3202",
            "module_id": "201",
            "title": "Lesson 3202",
            "description": "The lesson 3202",
            "duration": "100.01",
        },
        {
            "id": "4201",
            "module_id": "202",
            "title": "Lesson 4201",
            "description": "The lesson 4201",
            "duration": "1.0",
        },
        {
            "id": "4202",
            "module_id": "202",
            "title": "Lesson 4202",
            "description": "The lesson 4202",
            "duration": "0",
        },
    ],
}
