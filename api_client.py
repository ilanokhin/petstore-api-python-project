import requests
from requests import Response
from config import API_BASE_URL


class ApiClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url

    def get(self, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"
        return requests.post(url, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"
        return requests.put(url, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"
        return requests.patch(url, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"
        return requests.delete(url, **kwargs)

    def head(self, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"
        return requests.head(url, **kwargs)

    def options(self, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"
        return requests.options(url, **kwargs)
