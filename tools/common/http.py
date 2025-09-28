import httpx


class Http:
    def __init__(self, timeout: int = 30):
        self.client = httpx.Client(timeout=timeout)


    def get(self, url: str, **kwargs):
        r = self.client.get(url, **kwargs)
        r.raise_for_status()
        return r.json()


    def post(self, url: str, json: dict, **kwargs):
        r = self.client.post(url, json=json, **kwargs)
        r.raise_for_status()
        return r.json()