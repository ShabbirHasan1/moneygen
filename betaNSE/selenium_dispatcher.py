from selenium import web__driver
from selenium.web__driver.common.keys import Keys
from selenium.web__driver.support.select import Select
from selenium.web__driver.chrome.options import Options  
from selenium.common.exceptions import TimeoutException
from selenium.web__driver.support.ui import Web__DriverWait
from selenium.web__driver.support import expected_conditions as EC
from selenium.web__driver.common.by import By
from config import Config

class SeleniumDispatcher:
    def __init__(self, headless: bool = False, download_path: str = None):
        # Selenium __driver options for chrome
        options = Options() 
        # Enable downloads if download_path is provided
        if download_path:
            options.add_experimental_option("prefs", {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            })

            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}

        # Set runtime config
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless")

        self.__driver = webdriver.Chrome(executable_path = Config.SELENIUM___DRIVER_EXEC_PATH, chrome_options = options)
        self.__driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        if download_path:
            self.__driver.execute("send_command", params)

    def get_driver(self):
        return self.__driver