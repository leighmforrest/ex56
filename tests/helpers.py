import csv


class MockResponse(object):
    def __init__(self, content, status_code, headers=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}

    def json(self):
        """Return a dict if content is dict"""
        return self.content

    @property
    def text(self):
        return str(self.content)


class MockDownloadResponse(object):
    """Class for mocking a requests.get call that downloads a file."""

    def __init__(self, content, status_code=200, headers=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}
        self.iter_content_called = False

    def iter_content(self, chunk_size=1024):
        self.iter_content_called = True
        return [
            self.content[i : i + chunk_size]
            for i in range(0, len(self.content), chunk_size)
        ]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def raise_for_status(self):
        pass


def assert_csv_data(csv_file, expected_data):
    """Helper to assert that  csv file existence and file matches data."""

    with csv_file.open() as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert csv_file.exists(), "csv does not exist in the target directory."
    assert rows == expected_data, "expected data does not match rows."
