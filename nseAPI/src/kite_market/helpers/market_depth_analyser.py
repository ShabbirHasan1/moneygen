from kiteconnect import KiteConnect
from kite_market.quote import QuoteManager
from config import Config



class MarketDepthAnalyser:
    """Class to market depth, all methods related to Market depth analysis are in this class"""    
    def __init__(self, kite_app: KiteConnect) :
        """Constructor
        
        Arguments:
            kite_app {KiteConnect} -- Instance of KiteConnect to enable the analysis
        """        
        self.kite_app = kite_app

    def check_for_liquidity(self, instruments: list) -> list:
        """Checks for liquidity for the instruments
        
        Arguments:
            instruments {list} -- List of instruments with symbol as string (example: INFY)
        
        Returns:
            list -- Boolean list, contains boolean values for liquidity (if liquid or not) in same sequence
        """        
        are_liquid = list()
        quote_manager = QuoteManager(self.kite_app)
        quotes = quote_manager.get_full(instruments)
        for quote in quotes:
            are_liquid.append(self.is_liquid(quote))
        return are_liquid

    def is_liquid(self, full_quote: dict) -> bool:
        """Check if particular stock is liquid (full quote with market depth is required)
        
        Arguments:
            full_quote {dict} -- Full Quote of a particular stock with market depth and volume
        
        Returns:
            bool -- Returns True if stock is liquid and False if illiquid
        """        
        is_horizontal_spread_liquid = self.__check_bid_ask_horizontal_difference__(full_quote['depth'])
        is_vertical_spread_liquid = self.__check_bid_ask_vertical_difference__(full_quote['depth'])
        is_volume_liquid = self.__check_volume__(full_quote['volume'])
        return is_horizontal_spread_liquid and is_vertical_spread_liquid and is_volume_liquid

    def __check_bid_ask_horizontal_difference__(self, depth: dict) -> bool:
        """Checks if Bid Ask spread (horizontal) is liquid
        
        Arguments:
            depth {dict} -- Market depth (both bid and ask) up to 5 levels
        
        Returns:
            bool -- Returns True if bid/ask spread liquid and False if illiquid
        """        
        is_bid_ask_spread_liquid = False
        # TODO: Add logic to find optimal bid ask spread
        return is_bid_ask_spread_liquid

    def __check_bid_ask_vertical_difference__(self, depth: dict) -> bool:
        """Check if bid/ask vertical difference is liquid
        
        Arguments:
            depth {dict} -- Market depth for particular stock
        
        Returns:
            bool -- Liquidity status
        """        
        is_bid_liquid = self.__check_bid_vertical_difference__(depth['buy'])
        is_ask_liquid = self.__check_bid_vertical_difference__(depth['sell'])
        return is_ask_liquid and is_bid_liquid

    def __check_bid_vertical_difference__(self, buy_depth: list) -> bool:
        """Check if bid vertical difference is liquid
        
        Arguments:
            buy_depth {list} -- Market depth (bid) for particular stock
        
        Returns:
            bool -- Liquidity status
        """        
        is_buy_depth_liquid = False
        # TODO: Add logic to find vertical difference of bids
        return is_buy_depth_liquid

    def __check_ask_vertical_difference__(self, sell_depth: list) -> bool:
        """Check if ask vertical difference is liquid
        
        Arguments:
            sell_depth {list} -- Market depth(ask) for particular stock
        
        Returns:
            bool -- Liquidity status
        """        
        is_sell_depth_liquid = False
        # TODO: Add logic to find vertical difference of asks
        return is_sell_depth_liquid

    def __check_volume__(self, volume: int) -> bool:
        """Check if volume is liquid
        
        Arguments:
            volume {int} -- Volume of stock
        
        Returns:
            bool -- Liquidity status
        """        
        return volume >= Config.LIQUID_VOLUME_THRESHOLD


Mark