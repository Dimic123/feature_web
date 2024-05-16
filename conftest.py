
import os, pytest, json
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

def pytest_configure(config: pytest.Config):
    pytest.api_token = None
    pytest.api_base_url = config.getoption("--apiBaseUrl")

    split_path = config.getoption("file_or_dir")[0].split(os.sep)

    if "WebAPI" in split_path:
        pytest.log_objects = {}
        pytest.data_collections = {}
        pytest.timers = {}
        if not os.path.exists(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "report_logs")):
            os.makedirs(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "report_logs"))
        if not os.path.exists(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "ElapsedTimes")):
            os.makedirs(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "ElapsedTimes"))
    elif "Web" in split_path:
        pass

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
    split_path = metafunc.definition.fspath.dirname.split(os.sep)
    if "WebAPI" in split_path:
        json_file_path = os.path.join(metafunc.definition.fspath.dirname, metafunc.definition.fspath.purebasename + ".json")
        pytest.log_objects[metafunc.definition.fspath.purebasename] = CsvLogWriter(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "report_logs", f"_logs_{metafunc.definition.fspath.purebasename}.log"))

        # create data structure to measure req/res times for WebAPI
        idx = split_path.index("WebAPI")
        relative_path = split_path[idx:]
        if len(relative_path) == 4:
            test_name = split_path.pop(-1)
            pytest.timers[test_name] = []
        elif len(relative_path) == 5:
            test_name = split_path.pop(-1)
            group_name = split_path.pop(-1)
            test_type = split_path.pop(-1)

            if not group_name in pytest.timers.keys():
                pytest.timers[group_name] = {}
                pytest.timers[group_name][test_name] = {
                    "type": test_type,
                    "values": []
                }
            else:
                pytest.timers[group_name][test_name] = {
                    "type": test_type,
                    "values": []
                }

        pytest.data_collections[metafunc.definition.fspath.purebasename] = {}
    elif "Web" in split_path:
        json_file = os.path.join(metafunc.definition.fspath.dirname, metafunc.definition.fspath.purebasename + ".json")
        json_data = {}
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                json_data = json.load(f)

        data = []

        for case in json_data["test_cases"]:
            data.append(json_data["test_cases"][case])

        metafunc.parametrize("params", data)

def pytest_sessionstart(session):
    pass

@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    # called when all test cases for specific test had been finished
    if hasattr(pytest, "data_collections"):
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

    # save measurd req/res times for WebAPI to file
    if hasattr(pytest, "timers"):
        for group in pytest.timers.keys():
            if type(pytest.timers[group]) is list:
                raw_values = pytest.timers[group]
                if len(raw_values) <= 0:
                    continue

                min_elapsed_time = min(raw_values)
                max_elapsed_time = max(raw_values)
                avg_elapsed_time = sum(raw_values) / len(raw_values)
                pytest.timers[group] = {
                    "raw_values": raw_values,
                    "min": min_elapsed_time,
                    "avg": avg_elapsed_time,
                    "max": max_elapsed_time
                }

                f_out = open(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "ElapsedTimes", f"PreTests_0_{group}.json"), "w")
                json.dump(pytest.timers, f_out)
                f_out.close()
            else:
                for folder in pytest.timers[group].keys():
                    test_type = pytest.timers[group][folder]["type"]
                    raw_values = pytest.timers[group][folder]["values"]
                    if len(raw_values) <= 0:
                        continue

                    min_elapsed_time = min(raw_values)
                    max_elapsed_time = max(raw_values)
                    avg_elapsed_time = sum(raw_values) / len(raw_values)
                    pytest.timers[group][folder] = {
                        "raw_values": raw_values,
                        "min": min_elapsed_time,
                        "avg": avg_elapsed_time,
                        "max": max_elapsed_time
                    }
                f_out = open(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "ElapsedTimes", f"{test_type}_{group}.json"), "w")
                json.dump(pytest.timers, f_out)
                f_out.close()

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    print("pytest_terminal_summary")
    print(pytest.timers.keys())

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

@pytest.fixture(scope="function")
def token(request):
    """Get token for specified API"""
    yield getToken(request.config)
