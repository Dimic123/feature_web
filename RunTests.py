import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Common.JsonHelpers import ImportJsonFile
from Web.Live import *


def main():
	TestWeb()

def TestWeb():
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument('--headless')
	driver = webdriver.Chrome(options=options)

	CheckingSiteTitle(driver).RunTest()

	# data = ImportJsonFile('./Web/Live/Data/CheckingSiteTitle.json')

	# for case in data:
	# 	WebTests.CheckingSiteTitle(driver, data[case])
	# 	print("Test case", case, "passed")

	# data = ImportJsonFile('./Web/Live/Data/LoginTest.json')

	# for case in data:
	# 	WebTests.LoginTest(driver, data[case])
	# 	print("Test case", case, "passed")

	# data = ImportJsonFile('./Web/Live/Data/DataOnSiteTest.json')

	# for case in data:
	# 	WebTests.DataOnSiteTest(driver, data[case])
	# 	print("Test case", case, "passed")

	driver.quit()	

if __name__ == "__main__":
	main()