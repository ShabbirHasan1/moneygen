import sys
import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    DOWNLOAD_DIRECTORY = '/Users/mayank.gupta/Moneygen/nseAPI/downloads'
    SELENIUM_DRIVER_BASE_PATH = 'chromedriver'
    SELENIUM_DRIVER_EXEC_PATH = \
        os.path.join(SELENIUM_DRIVER_BASE_PATH, sys.platform)
    SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')
    MONGO_DB = 'nse_api'
    MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING') + '/'
    CONNECTION_ALIAS = 'nse_api'
    GAINER_LOSER_COLLECTION = 'gainer_loser_info'
    DATE_FORMAT = '%Y-%m-%d'
