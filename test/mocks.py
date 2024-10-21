import requests


class MockResponse(object):
    def __init__(self, content, status_code, headers=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}
    
    @property
    def text(self):
        return str(self.content)
    
    def raise_for_status(self):
        if self.status_code != 200 or self.status_code != 304:
            raise requests.exceptions.HTTPError()
