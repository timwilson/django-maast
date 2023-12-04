import httpx
from decouple import config


class MaastHTTPClient(httpx.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers.update({"X-API-KEY": config("API_KEY")})
