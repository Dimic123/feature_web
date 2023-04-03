from appium import webdriver as appdriver
from Common.MobileHelpers import *

from time import sleep

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

def ManualsTest(driver: appdriver) -> bool:
    if not CheckIfBottomBar(driver):
        return False
    
    menuBtn = driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="Menu"]')
    menuBtn.click()

    manualsBtn = driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="Manuals"]')
    manualsBtn.click()

    sleep(10)

    Screenshot(driver, "./Mobile/Screenshots")

