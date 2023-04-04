from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

import os
from datetime import datetime

def CheckLocation(driver: webdriver, xpath:str) -> bool:
    try:
        TouchButton(driver, xpath=xpath)
        return True
    except:
        return False

def TouchButton(driver: webdriver, xpath: str) -> None:
    # Get button and click
    el = driver.find_element(by=AppiumBy.XPATH, value=xpath)
    el.click()

def Screenshot(driver: webdriver, folder: str) -> None:
    # activity = driver.current_activity
    # screenshot = os.path.join(os.path.abspath(folder), activity + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S.png"))
    # if not driver.save_screenshot(screenshot):
    #     raise Exception("Screenshot could not be saved, check file location!")
    pass
    
def CheckIfHome(driver: webdriver) -> bool:
    try:
        driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="PULL TO REFRESH"]')
    except:
        return False
    else:
        return True
    
def CheckIfBottomBar(driver: webdriver) -> bool:
    try:
        driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="Home"]')
        driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="Devices"]')
        driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="Menu"]')
        driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="Show menu"]')
    except:
        return False
    else:
        return True