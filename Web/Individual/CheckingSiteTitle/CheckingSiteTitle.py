from selenium import webdriver
from Common.Logging import *
from Configuration.Settings import Settings
from Common.TestObject import *

class CheckingSiteTitleTest(TestObject):
    def __init__(self, driver = None) -> None:
        super().__init__(__file__)

    def Test(self, data: dict) -> bool:
        site = data["site"]
        expectedTitle = data["title"]

        self.logger.info("Checking site title for site: " + site)

        self.driver.get(site)

        title = self.driver.title

        try:
            assert title == expectedTitle
        except:
            msg = "FAILED - Expected page title was \"" + expectedTitle + "\", but actual title is: \"" + title + "\""
            self.logger.error(msg)
            return False
        else:
            msg = "PASSED - Page title is as expected: \"" + expectedTitle + "\""
            self.logger.info(msg)
            return True
