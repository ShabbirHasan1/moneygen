from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import Config
from seleniumwire import webdriver as wiredriver
import json


class SeleniumDispatcher:
    def __init__(self, headless: bool = False, download_path: str = None, selenium_wire: bool = False):
        # Selenium __driver options for chrome
        options = Options() 
        # Enable downloads if download_path is provided
        if download_path:
            print('Download is turned on')
            options.add_experimental_option("prefs", {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            })

            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}

        # Set runtime config
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless")
        
        if selenium_wire:
            self.__driver = wiredriver.Chrome(executable_path = Config.SELENIUM_DRIVER_EXEC_PATH, chrome_options = options)
        else:    
            self.__driver = webdriver.Chrome(executable_path = Config.SELENIUM_DRIVER_EXEC_PATH, chrome_options = options)

        if download_path:
            self.__driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            self.__driver.execute("send_command", params)

    def get_driver(self):
        return self.__driver

    # TODO : make this method work in headless=True, works great with headless=False
    # @body Try using virtual display to run GUI in memory
    def get_response(self, url):
        '''Get reponse to a GET request using selenium
        Needs to 'selenium_wire' to be set to True
        '''
        self.__driver.get(url)
        # for request in self.__driver.requests:
        #     if request.response:
        #         if request.path == url:
        request = self.__driver.wait_for_request(url, timeout=30)
        data = request.response.body.decode("utf-8")
        self.__driver.close()
        return data

    