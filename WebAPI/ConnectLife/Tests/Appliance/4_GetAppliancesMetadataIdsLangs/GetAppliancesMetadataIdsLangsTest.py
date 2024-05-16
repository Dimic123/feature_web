import os, pytest, json, requests, sys, datetime

api_group_folder_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
ROOT_PROJECT_PATH = os.sep.join(api_group_folder_path.split(os.sep)[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from server_error_json_schema import server_error_json_schema
from Common.FileHelpers import ReadFileFromSharedDataDirectory, ReadFileFromStaticDataDirectory

langs = ReadFileFromStaticDataDirectory("languages.json")

manually_added_ids = ["8650401000100010040000000fae3514881f-0000000000007394030001202300031960001"]
ids = []

appliances = ReadFileFromSharedDataDirectory("appliances.json")
for appliance in appliances:
    ids.append(appliance["id"])
    
if appliances == []:
    appliances = manually_added_ids

@pytest.mark.parametrize("id", ids)
@pytest.mark.parametrize("lang", langs)
def test_get_appliances_metadata_ids_langs(token: str, id, lang):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "id", "lang", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/appliance/metadata/{id}/{lang}"
    print("\nTesting " + url)
    
    headers = { 'Authorization': 'Bearer ' + token + '' }
    
    response = None
    attempts = 1
    while attempts <= 5:
        try:
            response = requests.request("GET", url, headers=headers, data={}, timeout=(10 * attempts))
            break
        except requests.exceptions.Timeout:
            attempts += 1
            print(f"Request attempt: #{attempts}")
    
    if response == None:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", str(id), str(lang), url])
        assert False

    if not response.status_code in [200, 400, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", str(id), str(lang), url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", str(id), str(lang), url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", str(id), str(lang), url])
        assert False
    
    [success_200_schema, error_400_schema, error_500_schema] = CreateJsonSchemas()
    
    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 400):
        isValidOrTrue = ValidateJson(data, error_400_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)
    
    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", str(id), str(lang), url])
        assert False
    
    if response.status_code == 200:
        pass
    elif response.status_code == 400:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", str(id), str(lang), url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", str(id), str(lang), url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", str(id), str(lang), url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET /api/v1/appliance/metadata/{id}/{lang}: SUCCESS 200", 
        "Gets metadata describing the properties of an appliance.",
        [
            {
                "id": "string",
                "supportsSettingPropertiesInSequence": "boolean",
                "propertyMetadata": [
                    {
                        "key": "string",
                        "description": "string",
                        "readWriteMode": "string",
                        "type": "string",
                        "minValue": "string",
                        "maxValue": "string",
                        "minValuePropertyKey": "string",
                        "maxValuePropertyKey": "string",
                        "step": "string",
                        "minValueCelsius": "string",
                        "maxValueCelsius": "string",
                        "minValueFahrenheit": "string",
                        "maxValueFahrenheit": "string",
                        "unitPropertyKey": "string",
                        "validValues": [
                            "string"
                        ],
                        "enumValues": {
                            "additionalProp1": {
                                "key": "string",
                                "label": "string"
                            },
                            "additionalProp2": {
                                "key": "string",
                                "label": "string"
                            },
                            "additionalProp3": {
                                "key": "string",
                                "label": "string"
                            }
                        }
                    }
                ]
            }
        ]
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_200", file_path, success_200_schema)
    
    error_400_schema = CreateJsonSchema(
        "GET /api/v1/appliance/metadata/{id}/{lang}: ERROR 400", 
        "Error 400: Post appliance", 
        server_error_json_schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_400_schema)

    error_500_schema = CreateJsonSchema(
        "Server error 500 json schema", 
        "General server error schema", 
        server_error_json_schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_400_schema, error_500_schema]
