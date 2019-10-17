from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import Config

class SeleniumDispatcher:
    def __init__(self, headless: bool = False, download_path: str = None):
        # set a self variable with selenium instance
        # if download dir, enable downloads in specified directory
        # Selenium driver options for chrome
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

        self.driver = webdriver.Chrome(executable_path = Config.SELENIUM_DRIVER_EXEC_PATH, chrome_options = options)
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        if download_path:
            self.driver.execute("send_command", params)

    def get_driver(self):
        return self.driver