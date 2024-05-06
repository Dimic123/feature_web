import os, pytest, json, requests, sys, datetime

api_group_folder_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
ROOT_PROJECT_PATH = os.sep.join(api_group_folder_path.split(os.sep)[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from server_error_json_schema import server_error_json_schema
from base_json_schema_400_error_response_wizards import wizards_400_error_json_schema
from Common.FileHelpers import SaveToSharedDataDirectory, ReadFileFromSharedDataDirectory

recipeId_wizardId_post_request_payload_list = ReadFileFromSharedDataDirectory("recipeId_wizardId_post_request_payload_list.json")
request_payload_list = []

for request_payload in recipeId_wizardId_post_request_payload_list:
    _min = request_payload["noOfPersonsMin"]
    _max = request_payload["noOfPersonsMax"]

    for i in range(_min, _max + 1):
        request_payload_list.append({
            "wizard_id": request_payload["wizard_id"],
            "recipe_id": request_payload["recipe_id"],
            "level": request_payload["level"],
            "servings": str(i)
        })

@pytest.mark.test_env
@pytest.mark.parametrize("payload", request_payload_list)
def test_post_wizard_recipe_wizard_id(token: str, payload):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "wizard_id", "recipe_id", "level", "servings", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/wizard/recipe/{payload['wizard_id']}"
    print("\nTesting " + url)
    
    payload = {
        "recipeId": payload["recipe_id"],
        "level": payload["level"],
        "servings": payload["servings"]
    }
    
    headers = {
        'Authorization': 'Bearer ' + token + '',
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json"
    }
    
    response = None
    attempts = 1
    while attempts <= 5:
        try:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload), timeout=(10 * attempts))
            break
        except requests.exceptions.Timeout:
            attempts += 1
            print(f"Request attempt: #{attempts}")
    
    if response == None:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", payload["wizard_id"], payload["recipe_id"], payload["level"], payload["servings"], url])
        assert False

    if not response.status_code in [200, 400, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", payload["wizard_id"], payload["recipe_id"], payload["level"], payload["servings"], url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", payload["wizard_id"], payload["recipe_id"], payload["level"], payload["servings"], url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", payload["wizard_id"], payload["recipe_id"], payload["level"], payload["servings"], url])
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", payload["wizard_id"], payload["recipe_id"], payload["level"], payload["servings"], url])
        assert False
    
    if response.status_code == 200:
        pass
    elif response.status_code == 400:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{data}", payload["wizard_id"], payload["recipe_id"], payload["level"], payload["servings"], url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", payload["wizard_id"], payload["recipe_id"], payload["level"], payload["servings"], url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", payload["wizard_id"], payload["recipe_id"], payload["level"], payload["servings"], url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        {
            "container": "string",
            "shelf": "number",
            "numOfSteps": "number",
            "preheat": "boolean",
            "bakeSteps": [
                {
                    "type": "string",
                    "typeDisplayValue": "string",
                    "heaterSystem": "string",
                    "temperatureSetpoint": "number",
                    "duration": "number",
                    "microwavePower": "number",
                    "steam": "boolean",
                    "steamStart": "number",
                    "steamStop": "number",
                    "stepNumber": "number"
                }
            ],
            "wizardId": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_200", file_path, success_200_schema)

    error_400_schema = CreateJsonSchema(
        "Server error 400 json schema", 
        "General server error schema", 
        wizards_400_error_json_schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_400", file_path, error_400_schema)

    error_500_schema = CreateJsonSchema(
        "Server error 500 json schema", 
        "General server error schema", 
        server_error_json_schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_400_schema, error_500_schema]
