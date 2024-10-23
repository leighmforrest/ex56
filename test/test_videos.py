from test.data_for_tests import API_DATA, EXPECTED_IDS
from test.helpers import assert_common_keys

import pandas as pd
import pytest

from ex_56.videos import (
    ALLOWED_KEYS,
    get_course,
    get_course_dataframe,
    get_courses,
    get_lesson,
    get_module,
    get_module_dataframe,
    get_lesson_dataframe,
    process_modules_dataframe,
    process_courses_dataframe,
)


@pytest.mark.parametrize("cached", [True, False])
def test_get_courses_from_api(mock_course_api_request, courses_data, cached):
    result = get_courses(cached)
    assert result == courses_data


@pytest.mark.parametrize("expected", API_DATA["courses"])
@pytest.mark.parametrize("cached", [True, False])
def test_get_course_from_api(mock_course_api_request, expected, cached):
    result = get_course(expected["id"], cached)
    assert_common_keys(result, ALLOWED_KEYS["course"])


@pytest.mark.parametrize("expected", API_DATA["module"])
@pytest.mark.parametrize("cached", [True, False])
def test_get_module_from_api(mock_module_api_request, expected, cached):
    result = get_module(expected["id"], cached)
    assert_common_keys(result, ALLOWED_KEYS["module"])


@pytest.mark.parametrize("expected", API_DATA["lesson"])
@pytest.mark.parametrize("cached", [True, False])
def test_get_lesson_from_api(mock_lesson_api_request, expected, cached):
    result = get_lesson(expected["id"], cached)
    assert_common_keys(result, ALLOWED_KEYS["lesson"])


@pytest.mark.parametrize("cached", [True, False])
def test_get_courses_dataframe(mock_course_api_request, cached, courses_dataframe):
    expected_module_ids = EXPECTED_IDS["modules"]

    df, module_ids = get_course_dataframe(cached)

    assert expected_module_ids == module_ids
    pd.testing.assert_frame_equal(df, courses_dataframe)


@pytest.mark.parametrize("cached", [True, False])
def test_get_modules_dataframe(mock_module_api_request, cached, modules_dataframe):
    expected_lesson_ids = EXPECTED_IDS["lessons"]
    module_ids = EXPECTED_IDS["modules"]

    df, lesson_ids = get_module_dataframe(module_ids, cached)
    pd.testing.assert_frame_equal(df, modules_dataframe)
    assert expected_lesson_ids == lesson_ids


@pytest.mark.parametrize("cached", [True, False])
def test_get_lesson_dataframe(mock_lesson_api_request, cached, lesson_dataframe):
    lesson_ids = EXPECTED_IDS["lessons"]

    df = get_lesson_dataframe(lesson_ids, cached)
    pd.testing.assert_frame_equal(df, lesson_dataframe)


def test_process_modules_dataframe(
    lesson_dataframe, modules_dataframe, final_modules_dataframe
):
    result = process_modules_dataframe(lesson_dataframe, modules_dataframe)

    pd.testing.assert_frame_equal(result, final_modules_dataframe)


def test_process_courses_dataframe(final_courses_dataframe, courses_dataframe):
    result = process_courses_dataframe(final_courses_dataframe, courses_dataframe)
    pd.testing.assert_frame_equal(result, final_courses_dataframe)
