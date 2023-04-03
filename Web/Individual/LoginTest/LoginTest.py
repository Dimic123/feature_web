from selenium import webdriver
from selenium.webdriver.common.by import By
from Common.Logging import *
from Common.TestObject import TestObject
from Common.WebHelpers import *


class LoginTest(TestObject):
    def __init__(self, driver = None) -> None:
        super().__init__(__file__)

    def Test(self, data: dict) -> bool:
        site = data["site"]
        loginValues = data["values"]

        self.logger.info("Test Case 'Login' Started: ")

        usernamePath = loginValues["usernamePath"]
        passwordPath = loginValues["passwordPath"]
        submitPath = loginValues["submitPath"]

        username = loginValues["username"]
        password = loginValues["password"]

        self.driver.get(site)
        
        if(HasCookieMessage(self.driver)):
            AcceptCookies(self.driver, '/html/body/div[2]/div/div/div[2]/div[1]/div[2]/span[1]/button[1]')
            self.driver.implicitly_wait(1)

        usernameField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, usernamePath)))
        passwordField = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, passwordPath)))
        submitButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, submitPath)))

        usernameField.send_keys(username)
        passwordField.send_keys(password)
        submitButton.click()

        welcomePath = '/html/body/main/header/div[1]/div/div/div[4]/div/div/div/div/p'
        welcomeParagraph = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, welcomePath)))

        Screenshot(self.driver, folder="./Web/Screenshots")

        try:
            assert "Dobrodošli" in welcomeParagraph.get_attribute('innerHTML') 
        except:
            self.logger.error("FAILED - Expected welcome message")
            return False
        else:
            self.logger.info("PASSED - Login successful")
            return True
