import json


class MockResponse(object):
    def __init__(self, content, status_code, headers=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}

    def json(self):
        return json.loads(self.content)

    @property
    def text(self):
        return self.content
