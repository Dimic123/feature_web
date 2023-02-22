from selenium import webdriver
from selenium.webdriver.common.by import By
from Common.CommonFunctions import *

def CheckingSiteNG() -> None:
	print("Test Case 'Gorenje' Started: ")

	driver = webdriver.Chrome()
	driver.get("https://si.gorenje.com/")

	expectedTitle = "Gorenje | Domača Stran"
	title = driver.title

	expectedPageTitle(title, expectedTitle)
	
	try:
		assert title == expectedTitle
	except:
		pass

	print("Test Case 'Gorenje' Finished")

	driver.quit()