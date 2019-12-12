import sys
import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    DOWNLOAD_DIRECTORY = '/Users/mayank.gupta/Moneygen/nseAPI/downloads'
    # TODO: Change configuration for geckodriver
    SELENIUM_DRIVER_BASE_PATH = 'chromedriver'
    SELENIUM_DRIVER_EXEC_PATH = \
        os.path.join(SELENIUM_DRIVER_BASE_PATH, sys.platform)
    SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')
    MONGO_DB = 'nse_api'
    MONGO_AUTH_DB = os.getenv('MONGO_AUTH_DB')
    MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING') + '/'
    CONNECTION_ALIAS = 'nse_api'
    GAINER_LOSER_COLLECTION = 'gainer_loser_info'
    DATE_FORMAT = '%Y-%m-%d'
    NSE_HEADERS = {'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Host': 'nseindia.com',
                    'Referer': "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY&illiquid=0&smeFlag=0&itpFlag=0",
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                    'X-Requested-With': 'XMLHttpRequest'
                  }
