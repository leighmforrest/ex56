import pytest
import glob
import pandas as pd
from ex56.videos import get_courses, get_modules, get_lessons, get_dataframes
from tests.test_data import EXPECTED_IDS, EXPECTED_CSV_DATA
from tests.helpers import assert_csv_data


@pytest.mark.parametrize("cached", [True, False])
def test_get_courses_module_ids(tmp_path, cached, mock_course_api_request):
    target_dir = tmp_path
    module_ids = get_courses(target_dir, cached=cached)
    assert (
        module_ids == EXPECTED_IDS["modules"]
    ), "Module IDs do not match expected output."


def test_get_courses_csv_file_created(tmp_path, mock_course_api_request, course_data):
    target_dir = tmp_path
    filename = "courses.csv"
    fields = ["id", "title", "description"]
    expected_data = EXPECTED_CSV_DATA["courses"]
    csv_file = target_dir / filename

    get_courses(target_dir)
    assert_csv_data(csv_file, expected_data)


@pytest.mark.parametrize("cached", [True, False])
def test_get_module_lesson_ids(tmp_path, cached, mock_module_api_request):
    target_dir = tmp_path
    module_ids = EXPECTED_IDS["modules"]

    lesson_ids = get_modules(module_ids, target_dir, cached=cached)
    assert (
        lesson_ids == EXPECTED_IDS["lessons"]
    ), "Lesson IDs do not match expected output."


def test_get_modules_csv_file_created(tmp_path, mock_module_api_request, module_data):
    target_dir = tmp_path
    filename = "modules.csv"
    csv_file = target_dir / filename
    expected_data = EXPECTED_CSV_DATA["modules"]

    get_modules(
        EXPECTED_IDS["modules"],
        target_dir,
    )
    assert_csv_data(csv_file, expected_data)


def test_get_lessons_csv_file_created(tmp_path, mock_lesson_api_request, lesson_data):
    target_dir = tmp_path
    filename = "lessons.csv"
    csv_file = target_dir / filename
    expected_data = EXPECTED_CSV_DATA["lessons"]

    get_lessons(
        EXPECTED_IDS["lessons"],
        target_dir,
    )
    assert_csv_data(csv_file, expected_data)

    