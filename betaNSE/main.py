from selenium_dispatcher import SeleniumDispatcher

driver = SeleniumDispatcher(download_path='downloads').driver()

driver.get('www.google.com')
