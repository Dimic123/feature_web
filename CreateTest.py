import os


json_template = """{
    "case_1": {
        "site": "TEST_SITE_HERE",
        "value": "TEST_VALUE_HERE"
        "values": {
            "internal_value": "TEST_VALUE_HERE"
        } 
        "expected_value" : "EXPECTED_VALUE_HERE"
        "expected_values": {
            "internal_value": "EXPECTED_VALUE_HERE"
        } 
    }
}"""

py_template = """from selenium import webdriver
from selenium.webdriver.common.by import By
from Common.Logging import *
from Common.TestObject import TestObject


class BasicTest(TestObject):
    def __init__(self, driver) -> None:
        super().__init__(driver, __file__)

    def Test(self, data: dict) -> bool:
        site = data["site"]
        value = data["value"]
        expectedValue = data["expected_value"]

        self.logger.info("Testing site " + site)
        self.driver.get(site)

        element = self.driver.find_element(by=By.ID, value=value)

        try:
            assert element == expectedValue
        except:
            self.logger.error("FAILED")
            return False
        else:
            self.logger.info("PASSED")
            return True
"""

def inputValid(prompt: str, error: str, values: list):
    while True:
        value = input(prompt).lower()

        if any(x in value for x in values):
            return value
        else:
            print(error)

if os.name == "nt":
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

clear()

if os.path.exists("./Web") or os.path.exists("./Mobile"):
    print("Detected as running from the pySelenium directory...")
else:
    print("Not in pySelenium directory...")

testType = inputValid("Select type of test ['web', 'mobile', 'api']:\n", "Option not recognized...", ["web", "mobile", "api"])

if testType == "web":
    name = input("Type name of test: \n")
    folder = input("Test folder location: \n")
    folder = os.path.join(folder, name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    json = os.path.join(folder, name + ".json")
    py = os.path.join(folder, name + ".py")

    with open(json, 'w') as j:
        j.write(json_template)

    with open(py, 'w') as p:
        p.write(py_template)

elif testType == "mobile":
    name = input("Type name of test: \n")
    folder = input("Test folder location: \n")
    folder = os.path.join(folder, name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    json = os.path.join(folder, name + ".json")
    py = os.path.join(folder, name + ".py")

    with open(json, 'w') as j:
        j.write(json_template)

    with open(py, 'w') as p:
        p.write(py_template)

elif testType == "api":
    raise NotImplementedError