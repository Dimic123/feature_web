from Common.MobileHelpers import *
from time import sleep


class TestManuals():
    def test_main(self, driver, data: dict) -> None:
        if not CheckIfBottomBar(driver):
            return False
        
        menuBtn = driver.find_element(by=AppiumBy.XPATH, value=data["menu_id"])
        menuBtn.click()

        manualsBtn = driver.find_element(by=AppiumBy.XPATH, value=data["manuals_id"])
        manualsBtn.click()

        sleep(10)

        Screenshot(driver, "./Mobile/Screenshots")

