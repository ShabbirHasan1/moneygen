from index_historical import IndexHistorical
import requests
from config import Config
import os
from logger import Logger
from selenium_dispatcher import SeleniumDispatcher
import time
from selenium.webdriver.common.action_chains import ActionChains
import json


class IndexHistoricalOptions(IndexHistorical):
    def __init__(self, symbol_name: str, option_type: str):
        super().__init__(symbol_name)
        self.derivative_type = 'OPTIONS'
        self.derivative_type_val = 'OPTIDX'
        self.derivative_type_display_val = 'Index Options'
        self.option_type = option_type
        self.expiries = None
        self.expiry_strike_price_map = None

    def get_expiries(self):
        url = 'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxFOGetQuoteDataTest.jsp?i='\
                + self.derivative_type\
                + '&u='\
                + self.symbol_name\
                + '&e=&o=&k='
        res = requests.get(url)
        self.expiries = res.json()['expiries']
        return self.expiries


    def get_strike_prices(self, expiries: list):
        expiry_strike_price_map = dict()
        for expiry in expiries:
            url = 'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxFOGetQuoteDataTest.jsp?i='\
                    + self.derivative_type_val\
                    + '&u='\
                    + self.symbol_name\
                    + '&e='\
                    + expiry\
                    + '&o='\
                    + self.option_type\
                    + '&k='\
                    + self.option_type
            res = requests.get(url)
            expiry_strike_price_map[expiry] = res.json()['strikePrices']
        return expiry_strike_price_map

    def get_expiry_strike_price_map_for_all(self):
        if self.expiries is None:
            self.get_expiries()
        self.expiry_strike_price_map = self.get_strike_prices(self.expiries)
        return self.expiry_strike_price_map

    def get_info_specfic(self, expiry: str, strike_price: str):
        driver = SeleniumDispatcher(selenium_wire=True, headless=True).get_driver()
        url = 'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying='\
                + self.symbol_name\
                + '&instrument=OPTIDX&type='\
                + self.option_type\
                + '&strike='\
                + strike_price\
                + '&expiry='\
                + expiry
        ajax_url = 'https://nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxFOGetQuoteJSON.jsp?underlying='\
                + self.symbol_name\
                + '&instrument=OPTIDX&expiry='\
                + expiry\
                + '&type='\
                + self.option_type\
                + '&strike='\
                + strike_price
        Logger.log(ajax_url)
        driver.get(url)

        get_data_button = driver.find_element_by_xpath('//img[@src="/common/images/btn_go.gif"]')
        # driver.execute_script("arguments[0].click();", get_data_button)
        # get_data_button.click()
        # time.sleep(0.5)
        ActionChains(driver).move_to_element(get_data_button).click().perform()
        time.sleep(1)
        data = None
        for request in driver.requests:
            if request.response:
                if request.path == ajax_url:
                    data = json.loads(request.response.body)
                    Logger.log(data)

        driver.quit()
        return data

    def get_info_all(self):
        if self.expiry_strike_price_map is None:
            self.get_expiry_strike_price_map_for_all()
        infos = dict()
        for expiry in self.expiry_strike_price_map.keys():
            for strike_price in self.expiry_strike_price_map[expiry]:
                info = self.get_info_specfic(expiry, strike_price)
                infos[str(self.option_type+'_'+expiry+'_'+strike_price)] = info
        return infos

    def download_data_specific(self, expiry: str, strike_price: str):
        url = "https://nseindia.com/live_market/dynaContent/live_watch/get_quote/getFOHistoricalData.jsp"\
                + "?underlying=" + self.symbol_name\
                + '&instrument=' + self.derivative_type_val\
                + '&expiry=' + expiry\
                + '&type=' + self.option_type\
                + '&strike=' + strike_price\
                + "&fromDate=" + 'undefined'\
                + "&toDate=" + 'undefined'\
                + "&datePeriod=" + '3months'\
                + "&fileDnld=" + 'undefined'
        download_dir_path = os.path.join(Config.DOWNLOAD_DIRECTORY,self.derivative_type_val,self.option_type)
        if not os.path.isdir(download_dir_path):
            os.makedirs(download_dir_path)
        download_file_path = os.path.join(download_dir_path, expiry + '_' + strike_price + '.csv')
        # filename = wget.download(url=url, out=download_file_path)
        res = requests.get(url, allow_redirects=True)
        Logger.log(download_file_path)
        open(download_file_path, 'wb').write(res.content)
        return download_file_path

    def download_data_all(self):
        Logger.log('Download started')
        if self.expiry_strike_price_map is None:
            self.get_expiry_strike_price_map_for_all()
        downloaded_files = list()
        for expiry in self.expiry_strike_price_map.keys():
            for strike_price in self.expiry_strike_price_map[expiry]:
                filepath = self.download_data_specific(expiry, strike_price)
                downloaded_files.append(filepath)
        Logger.log('Download finished')
        return downloaded_files