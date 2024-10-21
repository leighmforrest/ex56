from test.data_for_tests import API_DATA
from test.helpers import assert_common_keys

import pytest

from ex_56.videos import ALLOWED_KEYS, get_course, get_courses


@pytest.mark.parametrize("cached", [True, False])
def test_get_courses_from_api(mock_course_api_request, courses_data, cached):
    result = get_courses(cached)
    assert result == courses_data


@pytest.mark.parametrize("expected", API_DATA["courses"])
@pytest.mark.parametrize("cached", [True, False])
def test_get_course_from_api(mock_course_api_request, expected, cached):
    result = get_course(expected["id"], cached)
    assert_common_keys(result, ALLOWED_KEYS["course"])
