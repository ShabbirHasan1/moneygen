import logging
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
from config import Config
from util import SeleniumDispatcher
from selenium.webdriver.common.keys import Keys
import time
from db.models import KiteSimulatorStateModel
from datetime import datetime, date
import numpy as np
from datetime import datetime
from dateutil.tz import *
import urllib.parse as urlparse
from urllib.parse import parse_qs



class LiveSimulator:
    def __init__(self, api_key=Config.KITE_API_KEY, api_secret=Config.KITE_API_SECRET, username = Config.KITE_USER_ID,
        password=Config.KITE_PASSWORD, pin=Config.KITE_PIN,
        end_hour=Config.KITE_SIMULATION_END_HOUR, end_minute=Config.KITE_SIMULATION_END_MINUTE):
        self.username = username
        self.password = password
        self.pin = pin
        self.api_key = api_key
        self.kite = KiteConnect(api_key=api_key)
        req_token = self.get_request_token()
        data = self.kite.generate_session(req_token, api_secret=api_secret)
        self.access_token = data["access_token"]
        self.kite.set_access_token(self.access_token)
        self.kite_state = KiteSimulatorStateModel.objects.raw({'createdDate': str(date.today())})[0]
        self.end_time = datetime.now().astimezone(tzlocal()).replace(hour=end_hour, minute=end_minute)


    def get_instrument_tokens(self, instrument_list: list):
        instrument_token_list = dict()
        self.instrument_infos = self.kite.instruments(exchange='NSE')
        for instrument in instrument_list:
            for instrument_info in self.instrument_infos:
                if instrument == instrument_info['tradingsymbol']:
                    instrument_token_list[instrument] = instrument_info['instrument_token']
                    break
        return instrument_token_list

    
    def sim_init(self):
        # Initialise
        ticker = KiteTicker(self.api_key, self.access_token)
        

        instrument_tokens = self.kite_state.companyTokens
        profit_slab = self.kite_state.profitSlab
        buy_dict = dict()
        # Defining the callbacks
        def on_ticks(tick, ticks_info):
            # global buy_dict
            for tick_info in ticks_info:
                # TODO: Check if the order is correct
                buy_dict[tick_info['instrument_token']] = tick_info['last_price']
            tick.close()

        def on_connect(tick, response):
            # global instrument_tokens
            tick.subscribe(self.kite_state.companyTokens)

        def on_close(tick, code, reason):
            tick.stop()

        # Assign the callbacks.
        ticker.on_ticks = on_ticks
        ticker.on_connect = on_connect
        ticker.on_close = on_close

        ticker.connect()

        buy_price = np.array(list(buy_dict.values()))
        self.kite_state.buyPrice = buy_price.tolist()
        self.kite_state.save()
        self.kite_state.profitablePrice = (np.array(buy_price) + np.array(self.kite_state.profitSlab)).tolist()
        self.kite_state.save()

    def simulate_market(self):
        # Initialise
        ticker = KiteTicker(self.api_key, self.access_token)
        end_time = self.end_time
        instrument_tokens = self.kite_state.companyTokens
        sell_dict = dict()
        profitable_dict = dict()
        
        # Building profitable dict
        for token, profitable_price in zip(instrument_tokens, self.kite_state.profitablePrice):
            profitable_dict[token] = profitable_price

        # Defining the callbacks
        def on_ticks(tick, ticks_info):
            if len(ticks_info) == 0:
                tick.close()
            global end_time
            global sell_dict
            global profitable_dict

            now = datetime.now().astimezone(tzlocal())
            if now <= end_time:
                for tick_info in ticks_info:
                    if tick_info['last_price'] >= profitable_dict[tick_info['instrument_token']]:
                        # TODO: Check if the order is correct
                        sell_dict[tick_info['instrument_token']] = tick_info['last_price']
                        tick.unsubscribe([tick_info['instrument_token']])
                    else:
                        continue
            else:
                for tick_info in ticks_info:
                    sell_dict[tick_info['instrument_token']] = tick_info['last_price']
                tick.close()
                

        def on_connect(tick, response):
            global instrument_tokens
            tick.subscribe(instrument_tokens)

        def on_close(tick, code, reason):
            tick.stop()

        # Assign the callbacks.
        ticker.on_ticks = on_ticks
        ticker.on_connect = on_connect
        ticker.on_close = on_close

        ticker.connect()    

    def get_request_token(self):
        selenium = SeleniumDispatcher(headless=True)
        driver = selenium.get_driver()
        driver.get(self.kite.login_url())
        time.sleep(4)
        username_field = driver.find_element_by_xpath("//input[@type='text']")
        username_field.send_keys(self.username)
        password_field = driver.find_element_by_xpath("//input[@type='password']")
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(4)
        pin_field = driver.find_element_by_xpath("//input[@type='password']")
        pin_field.send_keys(self.pin)
        pin_field.send_keys(Keys.ENTER)
        time.sleep(4)
        url = driver.current_url
        parsed = urlparse.urlparse(url)
        token = parse_qs(parsed.query)['request_token'][0]
        print(token)
        selenium.destroy_driver()
        return token

    def process_tick(self, tick, tick_info):
        if len(tick_info) == 0:
            return False
        

        
        