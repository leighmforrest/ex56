from test.data_for_tests import API_DATA
from test.helpers import assert_common_keys

import pytest

from ex56.constants import BASE_API_URL
from ex56.decorators import convert_and_filter_single_item
from ex56.videos import request_func


# Function used for testing purposes only.
@convert_and_filter_single_item()
def get_course(course_id, cached=True):
    """Get a course from the API."""
    func = request_func(cached)
    course = func(f"{BASE_API_URL}/course", {"course_id": course_id, "full": True})
    return course


@pytest.mark.parametrize("expected", API_DATA["courses"])
@pytest.mark.parametrize("cached", [True, False])
def test_get_course_from_api_empty_allowed_keys(
    mock_course_api_request, expected, cached
):
    result = get_course(expected["id"], cached)
    assert_common_keys(result, ["id"])
