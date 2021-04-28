#Wrapper to use Vantage API
import os
from . import session

class StockAPI(object):

    def __init__(self, id):
        self.id = id

    def info(self):
        query={'apikey': os.getenv("STOCK_API_KEY"), 'symbol': self.id}
        path = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED'
        response = session.get(path, params=query)
        return response.json()