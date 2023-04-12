
import json
import os
import pytest
from selenium import webdriver
from appium import webdriver as appdriver
from appium.options.android import UiAutomator2Options

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox", help="Type in browser type")

# @pytest.fixture
# def firefox_options(firefox_options):
#     firefox_options.add_argument('--headless')
#     return firefox_options

# @pytest.fixture
# def chrome_options(chrome_options):
#     chrome_options.add_argument('--headless')
#     return chrome_options

# @pytest.fixture
# def edge_options(edge_options):
#     edge_options.add_argument('--headless')
#     return edge_options

def pytest_generate_tests(metafunc):
    # called once per each test function

    json_file = os.path.join(metafunc.definition.fspath.dirname, metafunc.definition.fspath.purebasename + ".json")
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            json_data = json.load(f)

    data = []
    for case in json_data:
        data.append(json_data[case])

    metafunc.parametrize("data", data)

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")

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
        options = UiAutomator2Options()
        options.platformVersion = '10'
        options.udid = 'R3CT309J26M'
        options.app = os.path.abspath(r'.\Mobile\Apps\ConnectLife_1.3.0prod_12300222.apk') 
        server = 'http://127.0.0.1:4723/wd/hub'
        driver = appdriver.Remote(server, options=options)
    else:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

    yield driver 
    # Teardown
    driver.close()
    driver.quit()


def pytest_runtest_setup(item):
    pass

def pytest_runtest_teardown(item):
    pass