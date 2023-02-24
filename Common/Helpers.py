from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def HasCookieMessage(driver: webdriver) -> bool:
    driver.implicitly_wait(2)
    return driver.find_elements(By.CSS_SELECTOR, '#cookie-bar')

def AcceptCookies(driver: webdriver) -> None:
    driver.implicitly_wait(2)
    acceptButton = '/html/body/div[2]/div/div/div[2]/div[1]/div[2]/button'

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, acceptButton))).click()
    driver.implicitly_wait(2)
