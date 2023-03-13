from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def DataOnSiteTest(driver, data: dict) -> bool:
    site = data["site"]
    testValues = data["values"]
    returnValue = False

    print("Test Case 'Data' Started: ")

    driver.get(site)

    for field in testValues:
        xpath = testValues[field]["xpath"]
        text = testValues[field]["text"]

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            assert text in element.get_attribute('innerHTML') 
        except:
            print("FAILED - Didn't find the expected value:", text)
            returnValue &= False
        else:
            print("PASSED - Data found")
            returnValue &= True
    
    return returnValue