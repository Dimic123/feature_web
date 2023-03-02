from appium import webdriver as appdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


class AppDriver(object):
    appiumServer = 'http://127.0.0.1:4723/wd/hub'

    def __init__(self, options: UiAutomator2Options, server: str):
        self.options = options
        self.appiumServer = server


    def __enter__(self) -> appdriver:
        try:
            self.driver = appdriver.Remote(self.appiumServer, options=self.options)
        except:
            raise Exception("Cannot connect to Appium server, make sure you have the correct url and that the server is running.")
        return self.driver
 
    def __exit__(self, *args):
        try:
            self.driver.quit()
        except:
            pass





