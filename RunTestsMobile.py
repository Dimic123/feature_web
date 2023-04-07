from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Common.AppDriver import *
from Common.JsonHelpers import ImportJsonFile
import Mobile.ConnectLife as ConnectLife

import os


def main():
	#  TestWeb()
	TestMobile()

def TestMobile():
	# # Create options for app testing
	# options = UiAutomator2Options()
	# options.platformVersion = '10'
	# # ADB device UDID
	# options.udid = 'R3CT309J26M'
	# # App .apk file
	# options.app = os.path.abspath(r'.\Mobile\Apps\ConnectLife_1.3.0prod_12300222.apk') 
	# server = 'http://127.0.0.1:4723/wd/hub'

	# with AppDriver(options, server) as driver:
	# 	ConnectLife.LoginTest(driver)
	# 	ConnectLife.ManualsTest(driver)

	ConnectLife.LoginTest().RunTest()
		

if __name__ == "__main__":
	main()