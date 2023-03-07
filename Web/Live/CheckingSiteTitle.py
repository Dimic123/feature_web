from selenium import webdriver
from selenium.webdriver.common.by import By


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
		print("FAILED - Expected page title was \"" + expectedTitle + "\", but actual title is: \"" + title + "\"")
		return False
	else:
		print("PASSED - Page title is as expected: \"" + expectedTitle + "\"")
		return True
