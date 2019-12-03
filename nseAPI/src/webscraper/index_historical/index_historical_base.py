import requests


class IndexHistoricalBase:
    def __init__(self, symbol_name: str):
        self.symbol_name = symbol_name