import json


def convert_data():
    """Decorator to convert a raw string into json data."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            json_data = json.loads(result)
            return json_data

        return wrapper

    return decorator


def convert_and_filter_single_item(allowed_keys=None):
    """Convert string data into a dictionary and only include
    the fields in allowed_keys"""
    if allowed_keys is None:
        allowed_keys = ["id"]

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            json_data = json.loads(result)
            filtered_data = {
                key: json_data[key] for key in allowed_keys if key in json_data
            }
            return filtered_data

        return wrapper

    return decorator
