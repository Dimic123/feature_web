import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Common import JsonHelpers
# from Web.Live import *
from Web.Live.CheckingSiteTitle.CheckingSiteTitle import *
from Web.Live.DataOnSiteTest.DataOnSiteTest import *
from Web.Live.LoginTest.LoginTest import *


def main():
    print("")
    print("*******************************************************")
    print("******************** TESTS STARTED ********************")
    print("*******************************************************")
    print("")

    TestWeb()

    print("")
    print("*******************************************************")
    print("********************* TESTS ENDED *********************")
    print("*******************************************************")
    print("")


def TestWeb():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    results = {"passed": 0, "failed": 0, "total": 0}

    result = CheckingSiteTitleTest(driver).RunTest()
    results = CombineDicts(results, result)

    result = DataOnSiteTest(driver).RunTest()
    results = CombineDicts(results, result)

    result = LoginTest(driver).RunTest()
    results = CombineDicts(results, result)

    print("Web tests complete, passed:",
          results["passed"], ", failed:", results["failed"], ", total:", results["total"])

    driver.quit()


def CombineDicts(d1: dict, d2: dict) -> dict:
    for k in d1.keys():
        d1[k] += d2[k]

    return d1


if __name__ == "__main__":
    main()
