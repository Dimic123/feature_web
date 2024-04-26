
import os, pytest
from selenium import webdriver
from appium import webdriver as appdriver
from appium.options.android import UiAutomator2Options
from Configuration.Settings import *
from WebAPI.ConnectLife.Common.Authorization import AuthAPI as SwaggerAPI
from WebAPI.ConnectLife.Common.Authorization import OAuth2Authorization
from WebAPI.HiJuConn.Common.Authorization import AuthAPI as JuconnectAPI
from Common.CsvLogWriter.CsvLogWriter import CsvLogWriter
from Common.FileHelpers import SaveToSharedDataDirectory

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

def getToken(config: pytest.Config):
    authType = config.getoption("--auth")
    envType = config.getoption("--env")
    if pytest.api_token is None:
        retry = 0
        while retry < 5:
            if(authType == "swagger"):
                token = SwaggerAPI(Settings.get("Username"), Settings.get(
                    "Password"), Settings.get("ClientId"), Settings.get("ClientSecret"))
                if token is None:
                    print(
                        "ERROR - token was not retrieved, retrying... (attempt " + str(retry+1) + ")")
                else:
                    pytest.api_token = token
                    break
            elif(authType == "juconnect"):
                token = JuconnectAPI(Settings.get(
                    "Username"), Settings.get("Password"))
                if token is None:
                    print(
                        "ERROR - token was not retrieved, retrying... (attempt " + str(retry+1) + ")")
                else:
                    pytest.api_token = token
                    break
            elif(authType == "cdc"):
                token = OAuth2Authorization.getToken(str(envType).upper())
                pytest.api_token = token
            retry += 1

    if pytest.api_token is None:
        print("ERROR - token was not retrieved")
        raise Exception("ERROR - token was not retrieved")
    
    return pytest.api_token

def pytest_configure(config: pytest.Config):
    pytest.api_token = None
    pytest.api_base_url = config.getoption("--apiBaseUrl")
    pytest.log_objects = {}

    pytest.data_collections = {}
    
def pytest_unconfigure():
    pass

def pytest_addoption(parser):
    parser.addoption("--browser", action="store",
                     default="firefox", help="Select browser type for tests")
    parser.addoption("--device", action="store", default="",
                     help="If using Appium for testing, select device UDID")
    parser.addoption("--auth", action="store", default="swagger",
                     help="If doing web API tests, specifiy what type of authorization to use")
    parser.addoption("--env", action="store", default="test",
                     help="If doing web API tests, specifiy what type of environment to use")
    parser.addoption("--apiBaseUrl", action="store", default="https://dnejtsakgzwih.cloudfront.net",
                     help="If doing web API tests, specifiy which base url to use")

def pytest_generate_tests(metafunc: pytest.Metafunc):
    # called once per each test function
    json_file_path = os.path.join(metafunc.definition.fspath.dirname, metafunc.definition.fspath.purebasename + ".json")

    pytest.log_objects[metafunc.definition.fspath.purebasename] = CsvLogWriter(os.path.join(ROOT_DIR, f"report_logs/_logs_{metafunc.definition.fspath.purebasename}.log"))
    pytest.data_collections[metafunc.definition.fspath.purebasename] = {}

def pytest_sessionstart(session):
    pass

def pytest_sessionfinish(session, exitstatus):
    # called when all test cases for specific test had been finished
    item: pytest.Item
    for item in session.items:
        file_name = item.path.stem

        if file_name == "GetFaqsAuidsPreTest":
            if pytest.data_collections[file_name] != {}:
                SaveToSharedDataDirectory(f"{file_name}.json", pytest.data_collections[file_name])
                pytest.data_collections[file_name] = {}
        elif file_name == "GetFaqsAuidsLangsPreTest":
            if pytest.data_collections[file_name] != {}:
                SaveToSharedDataDirectory(f"{file_name}.json", pytest.data_collections[file_name])
                pytest.data_collections[file_name] = {}
        elif file_name == "GetTipsTricksAuidsLangPreTest":
            if pytest.data_collections[file_name] != {}:
                SaveToSharedDataDirectory(f"{file_name}.json", pytest.data_collections[file_name])
                pytest.data_collections[file_name] = {}
        elif file_name == "GetInspirationsAuidsPreTest":
            if pytest.data_collections[file_name] != {}:
                SaveToSharedDataDirectory(f"{file_name}.json", pytest.data_collections[file_name])
                pytest.data_collections[file_name] = {}
        elif file_name == "GetPairingAuidsPreTest":
            if pytest.data_collections[file_name] != {}:
                SaveToSharedDataDirectory(f"{file_name}.json", pytest.data_collections[file_name])
                pytest.data_collections[file_name] = {}
        elif file_name == "GetHelpPreTest":
            if pytest.data_collections[file_name] != {}:
                SaveToSharedDataDirectory(f"{file_name}.json", pytest.data_collections[file_name])
                pytest.data_collections[file_name] = {}
        elif file_name == "GetGenericFaqPreTest":
            if pytest.data_collections[file_name] != {}:
                SaveToSharedDataDirectory(f"{file_name}.json", pytest.data_collections[file_name])
                pytest.data_collections[file_name] = {}
        elif file_name == "GetGuidesPreTest":
            if pytest.data_collections[file_name] != {}:
                SaveToSharedDataDirectory(f"{file_name}.json", pytest.data_collections[file_name])
                pytest.data_collections[file_name] = {}

@pytest.fixture(scope="function")
def driver(request):
    """Get driver for specified browser"""
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
            options.app = os.path.abspath(
                Settings.get("AppPath", (Sections.MOBILE)))
            server = Settings.get("Server", (Sections.MOBILE))
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
    """Get token for specified API"""
    yield getToken(request.config)

def pytest_runtest_setup(item):
    pass

def pytest_runtest_teardown(item):
    pass
