import logging
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
from config import Config
from util import SeleniumDispatcher
from selenium.webdriver.common.keys import Keys


class LiveSimulator:
    def __init__(self, api_key=Config.KITE_API_KEY, api_secret=Config.KITE_API_SECRET, username = Config.KITE_USER_ID,
        password=Config.KITE_PASSWORD, pin=Config.KITE_PIN):
        self.username = username
        self.password = password
        self.pin = pin
        self.kite = KiteConnect(api_key=api_key)
        req_token = self.get_request_token()
        data = self.kite.generate_session(req_token, api_secret=api_secret)
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

    def get_request_token(self):
        selenium = SeleniumDispatcher(headless=False)
        driver = selenium.get_driver()
        driver.get(self.kite.login_url())
        username_field = driver.find_element_by_xpath('//input[@placeholder="User ID"]')
        username_field.send_keys(self.username)
        password_field = driver.find_element_by_xpath('//input[@placeholder="Password"]')
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.ENTER)
        pin_field = driver.find_element_by_xpath('//input[@placeholder="PIN"]')
        pin_field = driver.send_keys(self.pin)
        pin_field.send_keys(Keys.ENTER)
        url = driver.current_url
        token = url.split('&action')[0].split('request_token=')[1]
        return token
        