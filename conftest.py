
import json
import os
import pytest
from selenium import webdriver
from appium import webdriver as appdriver
from appium.options.android import UiAutomator2Options
from Configuration.Settings import *
from WebAPI.ConnectLife.Common.Authorization import AuthAPI

def pytest_configure():
    pytest.api_token = None

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox", help="Select browser type for tests")
    parser.addoption("--device", action="store", default="", help="If using Appium for testing, select device UDID")

def pytest_generate_tests(metafunc):
    # called once per each test function
    json_file = os.path.join(metafunc.definition.fspath.dirname, metafunc.definition.fspath.purebasename + ".json")
    json_data = {}
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            json_data = json.load(f)

    data = []
    for case in json_data:
        data.append(json_data[case])

    metafunc.parametrize("params", data)

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    device = request.config.getoption("--device")

    if browser == 'edge':
        options = webdriver.EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--headless')
        driver = webdriver.Edge(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
    elif browser == "appium":
        if device:
            options = UiAutomator2Options()
            options.platformVersion = '10'
            options.udid = request.config.getoption("--device")
            options.app = os.path.abspath(Settings.get("AppPath", ( Sections.MOBILE )))
            server =  Settings.get("Server", ( Sections.MOBILE ))
            driver = appdriver.Remote(server, options=options)
        else:
            raise Exception("Device not selected for Appium testing!")
    else:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

    yield driver 
    # Teardown
    driver.close()
    driver.quit()

@pytest.fixture(scope="function")
def token(request):
    if pytest.api_token is None:
        retry = 0
        while retry < 5:
            token = AuthAPI(Settings.get("Username"), Settings.get("Password"), Settings.get("ClientId"), Settings.get("ClientSecret"))
            if token is None:
                print("ERROR - token was not retrieved, retrying... (attempt " + str(retry+1) + ")")
                retry+=1
            else:
                pytest.api_token = token
                break
                
        if pytest.api_token is None:
            print("ERROR - token was not retrieved")

    yield pytest.api_token

def pytest_runtest_setup(item):
    pass

def pytest_runtest_teardown(item):
    pass