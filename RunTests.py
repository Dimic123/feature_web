from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Common.AppDriver import *
from Common.JsonHelpers import ImportJsonFile
import Web.Live as WebTests
import Mobile as MobileTests

import os
import json


def main():
	TestWeb()
	TestMobile()

def TestWeb():
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options=options)

	data = ImportJsonFile('./Web/Live/Data/CheckingSiteTitle.json')

	for case in data:
		WebTests.CheckingSiteTitle(driver, data[case])
		print("Test case", case, "passed")

	data = ImportJsonFile('./Web/Live/Data/LoginTest.json')

	for case in data:
		WebTests.LoginTest(driver, data[case])
		print("Test case", case, "passed")

	data = ImportJsonFile('./Web/Live/Data/DataOnSiteTest.json')

	for case in data:
		WebTests.DataOnSiteTest(driver, data[case])
		print("Test case", case, "passed")

	driver.quit()

def TestMobile():
	# Create options for app testing
	options = UiAutomator2Options()
	options.platformVersion = '10'
	# ADB device UDID
	options.udid = 'R3CT309J26M'
	# App .apk file
	options.app = os.path.abspath(r'.\Mobile\Apps\ConnectLife_1.3.0prod_12300222.apk') 
	server = 'http://127.0.0.1:4723/wd/hub'

	with AppDriver(options, server) as driver:
		MobileTests.LoginTest(driver)
		

	
if __name__ == "__main__":
	main()