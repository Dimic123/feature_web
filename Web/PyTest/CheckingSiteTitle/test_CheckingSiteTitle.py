from selenium import webdriver
from Common.Logging import *
from Configuration.Settings import Settings
from Common.TestObject import *

def test_run(data):
    # CheckingSiteTitleTest().RunTest()
    site = data["site"]
    expectedTitle = data["title"]
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless') 
    driver = webdriver.Chrome(options=options)

    print("Checking site title for site: " + site)

    driver.get(site)

    title = driver.title

    assert title == expectedTitle

    # print("PASSED - Page title is as expected: \"" + expectedTitle + "\"")

