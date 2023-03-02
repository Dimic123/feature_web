from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Common.AppDriver import *
import Web.Live as WebTests
import Mobile as MobileTests

import os


test_cases = {
	"site_title_1": {
		"site" : "https://si.gorenje.com/",
		"title" : "Gorenje | Domača Stran"
	},
	"site_title_1": {
		"site" : "https://si.gorenje.com/",
		"title" : "Gorenje | Veliki in mali gospodinjski aparati"
	}
}

login_values = {
	"usernamePath" : '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[1]/div[1]/div/div/input',
    "passwordPath" : '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[1]/div[2]/div[1]/div/input',
    "submitPath" : '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[2]/div/div[2]/button',
    "username" : "jedan70743@wireps.com",
    "password" : "gA5Z5KJxTLsb@u"
}

test_cases2 = {
	"login_1": {
		"site" : "https://si.gorenje.com/login",
		"values" : login_values
	}
}

def main():
	TestWeb()
	TestMobile()

def TestWeb():
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options=options)

	for case in test_cases:
		site = test_cases[case]["site"]
		title = test_cases[case]["title"]
		WebTests.CheckingSiteTitle(driver, site, title)
		print("Test case", case, "passed")

	for case in test_cases2:
		site = test_cases2[case]["site"]
		values = test_cases2[case]["values"]
		WebTests.LoginTest(driver, site, values)
		print("Test case", case, "passed")

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