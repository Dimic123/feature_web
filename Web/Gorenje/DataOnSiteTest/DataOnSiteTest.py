from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_data_on_site(driver, data: dict) -> bool:
    site = data["site"]
    testValues = data["values"]
    returnValue = False

    print("Testing data on site... ")

    driver.get(site)

    for field in testValues:
        xpath = testValues[field]["xpath"]
        text = testValues[field]["text"]

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            assert text in element.get_attribute('innerHTML') 
        except:
            print("ERROR - Didn't find the expected value:", text)
            returnValue &= False
        else:
            returnValue &= True
    
    assert returnValue, "Not all values appear on site"