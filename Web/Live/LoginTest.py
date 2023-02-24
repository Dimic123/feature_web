from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common.Helpers import *


def LoginTest() -> None:
    print("Test Case 'Login' Started: ")

    usernamePath = '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[1]/div[1]/div/div/input'
    passwordPath = '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[1]/div[2]/div[1]/div/input'
    submitPath = '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[2]/div/div[2]/button'

    username = "jedan70743@wireps.com"
    password = "gA5Z5KJxTLsb@u"

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.get("https://si.gorenje.com/login")
    
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

    try:
        assert "Dobrodošli" in welcomeParagraph.get_attribute('innerHTML') 
    except:
        print("FAILED - Expected welcome message")
    else:
        print("PASSED - Login successful")

