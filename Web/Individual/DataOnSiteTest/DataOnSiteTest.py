from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common.Logging import *
from Common.TestObject import TestObject


class DataOnSiteTest(TestObject):
    def __init__(self, driver) -> None:
        super().__init__(driver, __file__)

    def Test(self, data: dict) -> bool:
        site = data["site"]
        testValues = data["values"]
        returnValue = False

        self.logger.info("Test Case 'Data' Started: ")

        self.driver.get(site)

        for field in testValues:
            xpath = testValues[field]["xpath"]
            text = testValues[field]["text"]

            try:
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                assert text in element.get_attribute('innerHTML') 
            except:
                self.logger.error("FAILED - Didn't find the expected value:", text)
                returnValue &= False
            else:
                self.logger.info("PASSED - Data found")
                returnValue &= True
        
        return returnValue
