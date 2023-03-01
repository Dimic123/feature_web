from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import os
from datetime import datetime

class AppDriver(object):
    appiumServer = 'http://127.0.0.1:4723/wd/hub'

    def __init__(self, options: UiAutomator2Options, server: str):
        self.options = options
        self.appiumServer = server

    def __enter__(self):
        self.driver = webdriver.Remote(self.appiumServer, options=self.options)
        return self
 
    def __exit__(self, *args):
        self.driver.quit()

    def TouchButton(self, xpath: str) -> None:
        # Get button and click
        el = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
        el.click()

    def Screenshot(self, folder: str) -> None:
        activity = self.driver.current_activity
        screenshot = os.path.join(os.path.abspath(folder), activity + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S.png"))
        if not self.driver.save_screenshot(screenshot):
            raise Exception("Screenshot could not be saved, check file location!")



