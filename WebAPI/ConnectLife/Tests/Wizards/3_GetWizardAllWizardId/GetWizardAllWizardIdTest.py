import os, pytest, json, requests, sys, datetime

api_group_folder_path = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-2])
ROOT_PROJECT_PATH = "\\".join(api_group_folder_path.split("\\")[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from server_error_json_schema import server_error_json_schema
from Common.FileHelpers import SaveToSharedDataDirectory, ReadFileFromSharedDataDirectory

wizard_ids = ReadFileFromSharedDataDirectory("collected_wizards.json")

wizard_ids_list = []
for wizard_id in wizard_ids:
    wizard_ids_list.append(wizard_id)

wizard_ids_list = list(set(wizard_ids_list))

@pytest.mark.test_env
@pytest.mark.parametrize("wizard_id", wizard_ids_list)
def test_get_wizard_all(token: str, wizard_id):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "wizard_id", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/wizard/all/{wizard_id}"
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", wizard_id, url])
        assert False

    if not response.status_code in [200, 404, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", wizard_id, url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", wizard_id, url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", wizard_id, url])
        assert False
    
    [success_200_schema, error_404_schema, error_500_schema] = CreateJsonSchemas()
    
    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 404):
        isValidOrTrue = ValidateJson(data, error_404_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)

    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", wizard_id, url])
        assert False
    
    if response.status_code == 200:
        pass
    elif response.status_code == 404:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", wizard_id, url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", wizard_id, url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", wizard_id, url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        {
            "id": "string",
            "name": "string",
            "descryption": "string",
            "type": "string",
            "data": "null|string",
            "metaData": "null|object",
            "parameters": [
                {
                "name": "string",
                "possibleValues": "null|array",
                "isExternalSource": "boolean",
                "Extra": "number"
                }
            ],
            "sapIds": [
                "string"
            ]
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_200", file_path, success_200_schema)

    error_404_schema = CreateJsonSchema(
        "Server error 404 json schema", 
        "General server error schema", 
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_404", file_path, error_404_schema)

    error_500_schema = CreateJsonSchema(
        "Server error 500 json schema", 
        "General server error schema", 
        server_error_json_schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_404_schema, error_500_schema]
