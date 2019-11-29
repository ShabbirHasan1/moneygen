from equity_scraper_base import EquityScraperBase
from util.gainers_losers_info import GainersLosersInfo
import requests


class EquityScraper(EquityScraperBase):
    def __init__(self, instrument_symbol: str):
        super().__init__(instrument_symbol=instrument_symbol)


    def get_info_specfic(self, instrument_symbol: str):
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
        Logger.log(url)
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
                    data = json.loads(request.response.body.decode("utf-8"))
                    Logger.log(data)

        driver.quit()
        return data


    def get_info_all(self, instruments: list):
        pass

