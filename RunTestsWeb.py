import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Common import JsonHelpers
# from Web.Live import *
from Web.Live.CheckingSiteTitle.CheckingSiteTitle import *
from Web.Live.DataOnSiteTest.DataOnSiteTest import *
from Web.Live.LoginTest.LoginTest import *


def main():
	print("")
	print("*******************************************************")
	print("******************** TESTS STARTED ********************")
	print("*******************************************************")
	print("")

	TestWeb()

	print("")
	print("*******************************************************")
	print("********************* TESTS ENDED *********************")
	print("*******************************************************")
	print("")

def TestWeb():
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument('--headless')
	driver = webdriver.Chrome(options=options)

	CheckingSiteTitleTest(driver).RunTest()
	DataOnSiteTest(driver).RunTest()
	LoginTest(driver).RunTest()

	driver.quit()	

if __name__ == "__main__":
	main()