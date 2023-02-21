from selenium import webdriver
from selenium.webdriver.common.by import By
from Common.CommonFunctions import *

def CheckingSiteNG():
	print("Test Case 'Gorenje' Started: ")

	driver = webdriver.Chrome()
	driver.get("https://si.gorenje.com/")

	expectedTitle = "Gorenje | Domača Stran"
	title = driver.title

	try:
		expectedPageTitle(title, expectedTitle)
		assert title == expectedTitle
	except AssertionError:
		pass

	print("Test Case 'Gorenje' Finished")

	driver.quit()