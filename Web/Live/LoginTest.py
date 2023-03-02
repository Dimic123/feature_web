from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common.WebHelpers import *


def LoginTest(driver: webdriver, site: str, loginValues: dict) -> None:
    print("Test Case 'Login' Started: ")

    usernamePath = loginValues["usernamePath"]
    passwordPath = loginValues["passwordPath"]
    submitPath = loginValues["submitPath"]

    username = loginValues["username"]
    password = loginValues["password"]

    driver.get(site)
    
    if(HasCookieMessage(driver)):
        AcceptCookies(driver)
        driver.implicitly_wait(1)

    usernameField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, usernamePath)))
    passwordField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, passwordPath)))
    submitButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, submitPath)))

    usernameField.send_keys(username)
    passwordField.send_keys(password)
    submitButton.click()

    welcomePath = '/html/body/main/header/div[1]/div/div/div[4]/div/div/div/div/p'
    welcomeParagraph = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, welcomePath)))

    Screenshot(driver, folder="./Web/Screenshots")

    try:
        assert "Dobrodošli" in welcomeParagraph.get_attribute('innerHTML') 
    except:
        print("FAILED - Expected welcome message")
    else:
        print("PASSED - Login successful")

