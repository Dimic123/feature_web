import logging
from selenium import webdriver
from selenium.webdriver.common.by import By

from Common.Logging import *


# def CheckingSiteTitle(driver: webdriver, site: str, expectedTitle: str) -> None:
def CheckingSiteTitle(driver: webdriver, data: dict) -> bool:
	site = data["site"]
	expectedTitle = data["title"]

	print("Checking site title for site: ", site)

	driver.get(site)

	title = driver.title

	try:
		assert title == expectedTitle
	except:
		msg = "FAILED - Expected page title was \"" + expectedTitle + "\", but actual title is: \"" + title + "\""
		Logger.Log(msg, source="CheckingSiteTitle", type=Environment.Web, console=True)
		return False
	else:
		print("PASSED - Page title is as expected: \"" + expectedTitle + "\"")
		return True
