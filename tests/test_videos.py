import pytest
import csv
from ex56.videos import get_courses


@pytest.mark.parametrize("cached", [True, False])
def test_get_courses_module_ids(tmp_path, cached, mock_course_api_request):
    target_dir = tmp_path
    module_ids = get_courses(target_dir, cached=cached)
    assert module_ids == [
        101,
        102,
        201,
        202,
    ], "Module IDs do not match expected output."


def test_get_courses_csv_file_created(tmp_path, mock_course_api_request, course_data):
    target_dir = tmp_path
    filename = "courses.csv"
    fields = ["id", "title", "description"]

    get_courses(target_dir)
    csv_file = target_dir / filename
    assert csv_file.exists(), "csv does not exist in the target directory."

    with csv_file.open() as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Note: the ids need to be strings for tests to pass
    expected_data = [
        {"id": "1", "title": "course 1", "description": "Description for course 1"},
        {"id": "2", "title": "course 2", "description": "Description for course 2"},
    ]
    assert rows == expected_data, "expected data does not match rows."
