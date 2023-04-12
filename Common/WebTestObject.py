from selenium import webdriver
from Configuration.Settings import *
from Common.TestObject import TestObject, PyTestObject

class WebTestObject(TestObject):
    def __init__(self, testFilePath: str, driver = None) -> None:
        super().__init__()
        if driver is None:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--headless')
            driver = Settings.get("Driver")  
            if driver == "Chrome":
                self.driver = webdriver.Chrome(options=options)
            else:
                raise NotImplementedError
        else:
            self.driver = driver

        self.file = testFilePath
        self.logger = self._TestObject__setupLogger()

class PyWebTestObject(PyTestObject):
    def __init__(self, testFilePath: str, driver = None) -> None:
        super().__init__()
        if driver is None:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--headless')
            driver = Settings.get("Driver")  
            if driver == "Chrome":
                self.driver = webdriver.Chrome(options=options)
            else:
                raise NotImplementedError
        else:
            self.driver = driver

        self.file = testFilePath
        self.logger = self._PyTestObject__setupLogger()
