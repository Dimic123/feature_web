from selenium import webdriver
from selenium.webdriver.common.by import By
from Common.Logging import *
from Common.WebHelpers import *


def test_login(driver, data: dict) -> None:
    site = data["site"]
    loginValues = data["values"]

    print("Testing login...")

    usernamePath = loginValues["usernamePath"]
    passwordPath = loginValues["passwordPath"]
    submitPath = loginValues["submitPath"]

    username = loginValues["username"]
    password = loginValues["password"]

    driver.get(site)
    
    if(HasCookieMessage(driver)):
        AcceptCookies(driver, '/html/body/div[2]/div/div/div[2]/div[1]/div[2]/span[1]/button[1]')
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

    
    assert "Dobrodošli" in welcomeParagraph.get_attribute('innerHTML') 

