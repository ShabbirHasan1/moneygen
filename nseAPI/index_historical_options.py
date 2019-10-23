from index_historical import IndexHistorical


class IndexHistoricalOptions(IndexHistorical):
    def __init__(self, symbol_name: str):
        super().__init__(symbol_name)
        self.option_type = 'OPTIONS'
        self.option_type_val = 'OPTIDX'
        self.option_type_display_val = 'Index Options'

    def