from kiteconnect import KiteConnect


class QuoteManager:
    """Gets quote with different configs"""
    def __init__(self, kite_app: KiteConnect, exchange='NSE'):
        """Default constructor"""    
        self.exchange = exchange
        self.kite_app = kite_app

    def get_ltp(self, instruments: list) -> list:
        """Gets LTP quotes (no market depth, only stock quote and volumne)
        
        Arguments:
            instruments {list} -- List of instruments as exchange symbols (like INFY for NSE:INFY)

        Returns:
            list -- list of quotes in the requested sequence
        """
        instruments = [f'{self.exchange}:{x}' for x in instruments]
        return self.kite_app.ltp(instruments)
        
            

    def get_ohlc(self, instruments: list) -> list:
        """Get OHLC quote for instruments without market depth
        
        Arguments:
            instruments {list} -- List of instruments as exchange symbols (like INFY for NSE:INFY)

        Returns:
            list -- list of quotes in the requested sequence    
        """                
        instruments = [f'{self.exchange}:{x}' for x in instruments]
        return self.kite_app.quote(instruments) # quote method here is called correctly

    def get_full(self, instruments: list) -> list:
        """Gets OHLC quote for instruments with market depth upto 5 levels
        
        Arguments:
            instruments {list} -- List of instruments as exchange symbols (like INFY for NSE:INFY)

        Returns:
            list -- list of quotes in the requested sequence    
        """
        instruments = [f'{self.exchange}:{x}' for x in instruments]
        return self.kite_app.ohlc(instruments) # OHLC method here is called correctly

