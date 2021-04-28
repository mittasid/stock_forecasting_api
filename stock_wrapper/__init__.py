import os
import requests
from requests.auth import HTTPBasicAuth


STOCK_API_KEY = os.getenv("STOCK_API_KEY")

class APIKeyMissingError(Exception):
    pass

if STOCK_API_KEY is None:
    raise APIKeyMissingError(
        "All methods require an API key."
    )

auth = HTTPBasicAuth('apikey', STOCK_API_KEY)
session = requests.Session()

from .stock import StockAPI