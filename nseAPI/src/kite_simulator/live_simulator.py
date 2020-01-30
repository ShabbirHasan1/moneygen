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
from util.log import Logger



class LiveSimulator:
    def __init__(self, api_key=Config.KITE_API_KEY, api_secret=Config.KITE_API_SECRET, username = Config.KITE_USER_ID,
        password=Config.KITE_PASSWORD, pin=Config.KITE_PIN,
        end_hour=Config.KITE_SIMULATION_END_HOUR, end_minute=Config.KITE_SIMULATION_END_MINUTE):
        self.username = username
        self.password = password
        self.pin = pin
        # TODO: Generate kite instance only when a function that requires it is called
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
        if not self.kite_state.simulationInitSuccessful:
            # Initialise
            ticker = KiteTicker(self.api_key, self.access_token)
            instrument_tokens = self.kite_state.companyTokens.copy()
            profit_slab = self.kite_state.profitSlab
            buy_dict = dict()
            # Defining the callbacks
            def on_ticks(tick, ticks_info):
                # global buy_dict
                for tick_info in ticks_info:
                    buy_dict[tick_info['instrument_token']] = tick_info['last_price']
                tick.close()

            def on_connect(tick, response):
                # global instrument_tokens
                tick.subscribe(self.kite_state.companyTokens)

            def on_close(tick, code, reason):
                tick.stop()
                Logger.info('Connection closed successfully!')

            # Assign the callbacks.
            ticker.on_ticks = on_ticks
            ticker.on_connect = on_connect
            ticker.on_close = on_close

            ticker.connect()

            # Building buy list
            buy_list = list()
            for token in instrument_tokens:
                buy_list.append(buy_dict[token])
            self.kite_state.buyPrice = buy_list
            self.kite_state.profitablePrice = np.around((np.array(buy_list) + np.array(self.kite_state.profitSlab)), decimals=2).tolist()
            self.kite_state.simulationInitSuccessful = True
            self.kite_state.save()


    def simulate_market(self):
        # Initialise
        ticker = KiteTicker(self.api_key, self.access_token)
        instrument_tokens = self.kite_state.companyTokens.copy()
        profitable_prices = self.kite_state.profitablePrice.copy()
        sell_dict = dict()
        price_state_dict = dict()
        profitable_dict = dict()
        first_tick = False
        
        # Building profitable dict
        for token, profitable_price in zip(instrument_tokens, profitable_prices):
            profitable_dict[token] = profitable_price

        # Defining the callbacks
        def on_ticks(tick, ticks_info):
            if len(instrument_tokens) == 0:
                tick.close()


            num_ticks = len(ticks_info)
            Logger.info('Ticking, number: {}'.format(num_ticks))
            now = datetime.now().astimezone(tzlocal())

            if num_ticks > 0:
                if now < self.end_time:
                    Logger.info('Normal Time:->' + now.strftime("%H:%M:%S"))
                    for tick_info in ticks_info:
                        current_instrument_token = tick_info['instrument_token']
                        current_instrument_price = tick_info['last_price']
                        price_state_dict[current_instrument_token] = current_instrument_price
                        if current_instrument_price >= profitable_dict[current_instrument_token]:
                            sell_dict[current_instrument_token] = current_instrument_price
                            tick.unsubscribe([current_instrument_token])
                            instrument_tokens.remove(current_instrument_token)
                            # tick.resubscribe()
                            Logger.info('Unsubscribed token: ' + str(current_instrument_token))
                else:
                    Logger.info('Closing Time:->' + now.strftime("%H:%M:%S"))
                    Logger.info('Price State dict: ' +  str(price_state_dict))
                    Logger.info('Sell dict: ' + str(sell_dict))
                    unsold_instrument_tokens = list(set(price_state_dict.keys()) - set(sell_dict.keys()))
                    Logger.info('Unsold instruments: ' + str(unsold_instrument_tokens))
                    for instrument_token in unsold_instrument_tokens:
                        sell_dict[instrument_token] = price_state_dict[instrument_token]
                        instrument_tokens.remove(instrument_token)
                    Logger.info('Sell dict after close: ' + str(sell_dict))

            
                

        def on_connect(tick, response):
            tick.subscribe(instrument_tokens)
            tick.set_mode(tick.MODE_LTP, instrument_tokens)
            Logger.info('Subscribed tokens: ' + str(instrument_tokens))

        def on_close(tick, code, reason):
            Logger.info('Ticker closed successfuly!')
            tick.stop()

        # Assign the callbacks.
        ticker.on_ticks = on_ticks
        ticker.on_connect = on_connect
        ticker.on_close = on_close
        
        # Connect to live ticker
        # if not ticker.is_connected():
        ticker.connect()
        Logger.info('Building final dict' + str(sell_dict))

        # Build final sell_dict in correct order

        sell_list = list()
        for key in profitable_dict.keys():
            sell_list.append(sell_dict[key])

        self.kite_state.sellPrice = sell_list
        self.kite_state.save()

    def calculate_and_store_pnl(self):
        quantitiy = np.array(self.kite_state.numberOfStocksPerCompany)
        # Subtracting 1 from all companies as a failsafe for fund exhaustion, in case the stocks goes really high
        normalised_quantity = quantitiy - 1

        # Rounding negative values to 0
        normalised_quantity = normalised_quantity.clip(min=0)
        buy = np.array(self.kite_state.buyPrice)
        sell = np.array(self.kite_state.sellPrice)
        pnl_per_company = np.multiply(sell - buy, normalised_quantity)
        self.kite_state.pnlPerCompany = pnl_per_company.tolist()
        self.kite_state.pnl = float(np.sum(pnl_per_company))
        self.kite_state.save()



    def get_request_token(self):
        Logger.info('Starting to fetch request token for Kite API')
        selenium = SeleniumDispatcher(headless=True)
        driver = selenium.get_driver()
        driver.get(self.kite.login_url())
        time.sleep(4)
        username_field = driver.find_element_by_xpath("//input[@type='text']")
        username_field.send_keys(self.username)
        password_field = driver.find_element_by_xpath("//input[@type='password']")
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(2)
        pin_field = driver.find_element_by_xpath("//input[@type='password']")
        pin_field.send_keys(self.pin)
        pin_field.send_keys(Keys.ENTER)
        time.sleep(2)
        url = driver.current_url
        parsed = urlparse.urlparse(url)
        token = parse_qs(parsed.query)['request_token'][0]
        Logger.info('Request token received!')
        selenium.destroy_driver()
        return token

        

        
        