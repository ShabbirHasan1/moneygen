import sys
import os
class Config(object):
    SELENIUM_DRIVER_BASE_PATH = 'chromedriver'
    SELENIUM_DRIVER_EXEC_PATH = os.path.join(SELENIUM_DRIVER_BASE_PATH, sys.platform)
