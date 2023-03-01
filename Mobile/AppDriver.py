from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


class AppDriver(object):
    appiumServer = 'http://127.0.0.1:4723/wd/hub'

    def __init__(self, options: UiAutomator2Options, server: str):
        self.options = options
        self.appiumServer = server

    def __enter__(self) -> webdriver:
        self.driver = webdriver.Remote(self.appiumServer, options=self.options)
        return self.driver
 
    def __exit__(self, *args):
        self.driver.quit()




