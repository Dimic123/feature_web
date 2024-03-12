
import json, os, pytest, requests, re
from selenium import webdriver
from appium import webdriver as appdriver
from appium.options.android import UiAutomator2Options
from Configuration.Settings import *
from WebAPI.ConnectLife.Common.Authorization import AuthAPI as SwaggerAPI
from WebAPI.HiJuConn.Common.Authorization import AuthAPI as JuconnectAPI
from Common.FileHelpers import GenerateTestCasesJsonFile

@pytest.fixture
def connectivityGroups():
    groupsFilePath = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConnectivityGroups"), "groups.txt")
    with open(groupsFilePath) as f:
        return f.read().splitlines()
    
@pytest.fixture
def connectivityGroupsWithAuids(connectivityGroups, token):
    groupsWithAuids = {}
    print("\n")
    connectivityGroupsLength = len(connectivityGroups)
    for idx, connectivityGroup in enumerate(connectivityGroups):
        url = "https://api.connectlife.io/api/v1/products/codes/by-connectivity-group/" + connectivityGroup
        print(f"GET: {url} [{idx + 1}/{connectivityGroupsLength}]")
        payload = {}
        headers = { 'Authorization': 'Bearer ' + token + '' }
        
        response = requests.request("GET", url, headers=headers, data=payload, timeout=100)
        
        try:
            unicode_escaped_data = json.dumps(response.json())
            data = json.loads(unicode_escaped_data)
            
            # TODO: validate response data format
            groupsWithAuids[connectivityGroup] = data
        except Exception as ex:
            raise Exception("Malformed data: " + response.text) from ex

    return groupsWithAuids

def getToken(config: pytest.Config):
    authType = config.getoption("--auth")
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

            retry += 1

    if pytest.api_token is None:
        print("ERROR - token was not retrieved")
        raise Exception("ERROR - token was not retrieved")
    
    return pytest.api_token

def getConnectivityGroupsSapIds(token):
    groupsFilePath = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConnectivityGroups"), "groups.txt")
    
    f = open(groupsFilePath, "r")
    connectivityGroups = f.read().splitlines()
    f.close()
    
    groupsWithAuids = {}
    
    connectivityGroupsLength = len(connectivityGroups)
    for idx, connectivityGroup in enumerate(connectivityGroups):
        url = "https://api.connectlife.io/api/v1/products/codes/by-connectivity-group/" + connectivityGroup
        print(f"GET: {url} [{idx + 1}/{connectivityGroupsLength}]")
        payload = {}
        headers = { 'Authorization': 'Bearer ' + token + '' }
        
        response = requests.request("GET", url, headers=headers, data=payload, timeout=100)
        
        try:
            unicode_escaped_data = json.dumps(response.json())
            data = json.loads(unicode_escaped_data)
            
            # TODO: validate response data format
            groupsWithAuids[connectivityGroup] = data
        except Exception as ex:
            raise Exception("Malformed data: " + response.text) from ex
            
    return groupsWithAuids
        
def createAuidsWithWizardIdTestCases(inputObj, includeEnLang = False):    
    test_cases = []
    
    for wizard_id in inputObj:
        if len(inputObj[wizard_id]) > 0:
            for sapId in inputObj[wizard_id]:
                new_obj = { "auids": [sapId], "wizard_id": wizard_id, "id": "" }
                if includeEnLang:
                    new_obj["lang"] = "en"
                test_cases.append(new_obj)
    
    return test_cases

def createAuidsTestCases(inputObj, includeEnLang = False):
    test_cases = []
    
    for obj in inputObj:
        if len(inputObj[obj]) > 0:
            for sapId in inputObj[obj]:
                new_obj = { "auids": [sapId] }
                if includeEnLang:
                    new_obj["lang"] = "en"
                test_cases.append(new_obj)
    
    return test_cases

def pytest_configure():
    pytest.api_token = None
    pytest.wizardIdsAndRecipeIdsDictionary = {}
    
def pytest_unconfigure():
    print(pytest.wizardIdsAndRecipeIdsDictionary)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store",
                     default="firefox", help="Select browser type for tests")
    parser.addoption("--device", action="store", default="",
                     help="If using Appium for testing, select device UDID")
    parser.addoption("--auth", action="store", default="juconnect",
                     help="If doing web API tests, specifiy what type of authorization to use")

def pytest_generate_tests(metafunc: pytest.Metafunc):
    # called once per each test function
    json_file_path = os.path.join(metafunc.definition.fspath.dirname, metafunc.definition.fspath.purebasename + ".json")
    
    for kw in metafunc.definition.keywords:
        print(kw)
    
    if (any(value in metafunc.definition.keywords for value in [
            "multiStepTest", 
            "test_multistep_recipe_ids", 
            "test_multistep_washing_ids", 
            "test_multistep_recipe_paged_detail_lang_all"])):
        print("\nignoring pytest_generate_tests")
        pass
    else:
        if "CheckEnManualsForAllAuids" in metafunc.definition.keywords:
            _token = getToken(metafunc.config)            
            groups = getConnectivityGroupsSapIds(_token)
            test_cases = createAuidsTestCases(groups)
            GenerateTestCasesJsonFile(test_cases, json_file_path)
        elif "GetTipsTricksAuids" in metafunc.definition.keywords:
            _token = getToken(metafunc.config)
            groups = getConnectivityGroupsSapIds(_token)
            test_cases = createAuidsWithWizardIdTestCases(groups)
            GenerateTestCasesJsonFile(test_cases, json_file_path)
        elif "GetTipsTricksAuidsLang" in metafunc.definition.keywords:
            _token = getToken(metafunc.config)
            groups = getConnectivityGroupsSapIds(_token)
            test_cases = createAuidsWithWizardIdTestCases(groups, True)
            GenerateTestCasesJsonFile(test_cases, json_file_path)

        json_data = {}
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                json_data = json.load(f)

        data = []

        for case in json_data["test_cases"]:
            data.append(json_data["test_cases"][case])
                
        metafunc.parametrize("params", data)


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

# def pytest_report_teststatus(report: pytest.TestReport):
#     if report.when == "call":
#         if report.outcome == "failed":
#             directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "report_logs")
#             fileName = str(report.nodeid).split("::")[0].split("/")[-1].split(".")[0]
            
#             if (fileName == "GetManualsAuidsLangTest"):
#                 match = re.search(r"params = {.*}", str(report.longrepr))
#                 params_as_string = match.group().replace("params = ", "").replace("\'", "\"")
#                 params_as_json = json.loads(params_as_string)
                
#                 auidsList = params_as_json["auids"]
#                 completeFilenamePath = os.path.join(directory, "_logs_" + fileName + ".txt")
#                 with open(completeFilenamePath, "a") as f:
#                     for auid in auidsList:
#                         f.write(auid + "\n")
#                 return "FAIL", "F", "FAILED" + " " + str(auidsList)
            
#             return "FAIL", "F", "FAILED"
