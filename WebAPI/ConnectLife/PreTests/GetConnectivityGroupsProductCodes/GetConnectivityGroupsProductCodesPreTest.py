import os, pytest, json, requests, sys, datetime

ROOT_PROJECT_PATH = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-4])
sys.path.append(ROOT_PROJECT_PATH)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory, ReadTxtFile
from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import SaveToSharedDataDirectory

connGroups = ReadTxtFile(os.path.join(ROOT_PROJECT_PATH, "StaticData/ConnectivityGroups.txt"))

groupsWithAuids = {}
auids = []

@pytest.mark.test_env
@pytest.mark.parametrize("connGroup", connGroups)
def test_get_connectivity_groups_product_codes_pre_test(token: str, connGroup):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "connectivity_group", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/products/codes/by-connectivity-group/{connGroup}"
    print("\nTesting " + url)
    
    response = None
    attempts = 1
    while attempts <= 5:
        try:
            response = requests.request("GET", url, headers={ 'Authorization': 'Bearer ' + token + '' }, data={}, timeout=(10 * attempts))
            break
        except requests.exceptions.Timeout:
            attempts += 1
            print(f"Request attempt: #{attempts}")
    
    if response == None:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", connGroup, url])
        assert False

    if not response.status_code in [200, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", connGroup, url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", connGroup, url])
        assert False

    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", connGroup, url])
        assert False
    
    [success_200_schema, error_500_schema] = CreateJsonSchemas()
    
    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)
    
    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", connGroup, url])
        assert False
    
    if response.status_code == 200:
        global groupsWithAuids
        global auids
        groupsWithAuids[connGroup] = data
        auids += data
        SaveToSharedDataDirectory("connectivity_groups_auids_map.json", groupsWithAuids)
        SaveToSharedDataDirectory("sapIds.json", auids)
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", connGroup, url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", connGroup, url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        ["string"]
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_200", file_path, success_200_schema)

    error_500_schema = CreateJsonSchema(
        "Server error 500 json schema", 
        "General server error schema", 
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_500_schema]
