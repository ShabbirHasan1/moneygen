from selenium_dispatcher import SeleniumDispatcher

driver = SeleniumDispatcher(download_path='downloads', headless=False).get_driver()

driver.get('https://www.google.com')
