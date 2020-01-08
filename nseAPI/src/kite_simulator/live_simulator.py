import logging
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
from config import Config

class LiveSimulator:
    def __init__(self):
        self.kite = KiteConnect(api_key=Config.KITE_API_KEY)
        # TODO: Use selenium to use this URL and get request token
        print(kite.login_url())
        temp_req_token = '1111xxx'
        data = self.kite.generate_session(temp_req_token, api_secret=Config.KITE_API_SECRET)
        self.access_token = data["access_token"]
        self.kite.set_access_token(self.access_token)


    def get_instrument_tokens(self, instrument_list: list):
        instrument_token_list = dict()
        self.instrument_infos = self.kite.instruments(exchange='NSE')
        for instrument in instrument_list:
            for instrument_info in self.instrument_infos:
                if instrument == instrument_info['tradingsymbol']:
                    instrument_token_list[instrument] = instrument_info['instrument_token']
                    break
        return instrument_token_list

    def start_simulator(self, instrument_token_list):
        # Initialise
        ticker = KiteTicker(Config.KITE_API_KEY, self.access_token)
        tick_count = 0
        
        # Defining the callbacks
        # TODO: Modify in ticks callback to place virtual trades on realtime prices
        def on_ticks(tick, tick_info):
            # Callback to receive ticks.
            global tick_count
            print("Ticks: {}".format(ticks))
            tick_count = tick_count + 1
            print("Length: {}".format(tick_count))
            # TODO: modify simulator stopping logic
            if tick_count > 5:
                tick.close()

        def on_connect(tick, response):
            # Callback on successful connect.
            # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
            #tick.subscribe([134657, 408065])
            tick.subscribe(instrument_token_list)
            # Set RELIANCE to tick in `full` mode.
            # tick.set_mode(tick.MODE_FULL, [408065])

        def on_close(tick, code, reason):
            # On connection close stop the main loop
            # Reconnection will not happen after executing `tick.stop()`
            tick.stop()

        # Assign the callbacks.
        ticker.on_ticks = on_ticks
        ticker.on_connect = on_connect
        ticker.on_close = on_close

        ticker.connect()

        