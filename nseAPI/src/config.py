import sys
import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    DOWNLOAD_DIRECTORY = '/Users/mayank.gupta/Moneygen/nseAPI/downloads'
    SELENIUM_DRIVER_BASE_PATH = os.getenv('SELENIUM_DRIVER_LOCATION')
    SELENIUM_DRIVER_CHROME_EXEC_PATH = \
        os.path.join(SELENIUM_DRIVER_BASE_PATH, 'chromedriver_'+sys.platform)
    SELENIUM_DRIVER_FIREFOX_EXEC_PATH = \
        os.path.join(SELENIUM_DRIVER_BASE_PATH, 'geckodriver_'+sys.platform)
    SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')
    MONGO_DB = 'nse_api'
    MONGO_AUTH_DB = os.getenv('MONGO_AUTH_DB')
    MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING') + '/'
    # TODO: Make DB name come from env
    POSTGRES_DB='NseSecurityHistorical'
    POSTGRES_CONNECTION_STRING = os.getenv('POSTGRES_CONNECTION_STRING') + '/' + POSTGRES_DB
    CONNECTION_ALIAS = 'nse_api'
    GAINER_LOSER_COLLECTION = 'gainer_loser_info'
    DATE_FORMAT = '%Y-%m-%d'
    NSE_HEADERS = {'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Host': 'www1.nseindia.com',
                    'Referer': "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY&illiquid=0&smeFlag=0&itpFlag=0",
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                    'X-Requested-With': 'XMLHttpRequest'
                  }
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_API_ENDPOINT = 'https://api.sendgrid.com/v3/mail/send'
    SENDGRID_TO_EMAIL = os.getenv('SENDGRID_TO_EMAIL')
    KITE_FUNDS = os.getenv('KITE_FUNDS')
    KITE_API_KEY = os.getenv('KITE_API_KEY')
    KITE_API_SECRET = os.getenv('KITE_API_SECRET')
    KITE_USER_ID = os.getenv('KITE_USER_ID')
    KITE_PASSWORD = os.getenv('KITE_PASSWORD')
    KITE_PIN = os.getenv('KITE_PIN')
    KITE_SIMULATION_END_HOUR = int(os.getenv('KITE_SIMULATION_END_HOUR'))
    KITE_SIMULATION_END_MINUTE = int(os.getenv('KITE_SIMULATION_END_MINUTE'))
