import requests


class Caller:

    _api_base_url = None

    def __init__(self, api_base_url) -> None:
        super().__init__()
        self._api_base_url = api_base_url

    def make_request(self):
        response = requests.get(url="{}/".format(self._api_base_url))
        return response.content.decode("utf-8")
