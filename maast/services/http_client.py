import httpx
from decouple import config


class MaastHTTPClient(httpx.Client):
    """
    Initialize a new instance of the MaastHTTPClient class which automatically includes the
    required X-API-KEY header and the key value from .env.dev which is required to authenticate
    to the MAAST API.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers.update({"X-API-KEY": config("API_KEY")})
