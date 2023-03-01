from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import os


# Set options for server and connection
options = UiAutomator2Options()
options.platformVersion = '10'
# ADB device UDID
options.udid = 'R3CT309J26M'
# App .apk file
options.app = os.path.abspath(r'.\Mobile\Apps\ConnectLife_1.3.0prod_12300222.apk') 
# Connect to Appium server
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', options=options)
# Get button and click it
el = driver.find_element(by=AppiumBy.XPATH, value="//*[@content-desc='" + "NEXT" + "']")
el.click()