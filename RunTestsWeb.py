from selenium import webdriver

from Web.Individual.CheckingSiteTitle.CheckingSiteTitle import *
from Web.Individual.DataOnSiteTest.DataOnSiteTest import *
from Web.Individual.LoginTest.LoginTest import *

import Web.Simple as Simple

def main():
    print("")
    print("*******************************************************")
    print("******************** TESTS STARTED ********************")
    print("*******************************************************")
    print("")

    TestWebIndividual()
    # TestWebSimple()

    print("")
    print("*******************************************************")
    print("********************* TESTS ENDED *********************")
    print("*******************************************************")
    print("")


def TestWebIndividual():
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

def TestWebSimple():
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument('--headless')
	driver = webdriver.Chrome(options=options)

	data = ImportJsonFile('./Web/Live/Data/CheckingSiteTitle.json')

	for case in data:
		Simple.CheckingSiteTitle(driver, data[case])
		print("Test case", case, "passed")

	data = ImportJsonFile('./Web/Live/Data/LoginTest.json')

	for case in data:
		Simple.LoginTest(driver, data[case])
		print("Test case", case, "passed")

	data = ImportJsonFile('./Web/Live/Data/DataOnSiteTest.json')

	for case in data:
		Simple.DataOnSiteTest(driver, data[case])
		print("Test case", case, "passed")

def CombineDicts(d1: dict, d2: dict) -> dict:
    for k in d1.keys():
        d1[k] += d2[k]

    return d1


if __name__ == "__main__":
    main()
