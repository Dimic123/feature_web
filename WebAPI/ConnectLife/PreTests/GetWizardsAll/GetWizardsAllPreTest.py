import os, pytest, json, requests, sys, datetime

api_group_folder_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
ROOT_PROJECT_PATH = os.sep.join(api_group_folder_path.split(os.sep)[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import SaveToSharedDataDirectory

collected_wizards = {}

@pytest.mark.prod_api
def test_get_wizard_all_pre_test(token: str):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "elapsed_time", "error", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/wizard/all" # + "?includeLogicData=true"
    print("\nTesting " + url)
    
    req_res_times = []
    dir_folder_name = os.path.dirname(os.path.realpath(__file__)).split(os.sep)
    test_name = dir_folder_name.pop(-1)

    response = None
    attempts = 1
    while attempts <= 5:
        try:
            response = requests.request("GET", url, headers={ 'Authorization': 'Bearer ' + token + '' }, data={}, timeout=(10 * attempts))
            req_res_times.append(response.elapsed.total_seconds())
            break
        except requests.exceptions.Timeout:
            attempts += 1
            print(f"Request attempt: #{attempts}")
    
    req_res_duration = min(req_res_times)
    pytest.timers[test_name].append(req_res_duration)

    if response == None:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Request timed out {attempts} time/s", url])
        assert False

    if not response.status_code in [200, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Unknown response status code: { str(response.status_code) }", url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Exception: {ex}, Malformed data: {str(response.text)}", url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Empty response: {data}", url])
        assert False
    
    [success_200_schema, error_500_schema] = CreateJsonSchemas()
    
    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)

    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"{isValidOrTrue}", url])
        assert False
    
    if response.status_code == 200:
        current_wizard_ids = []

        global collected_wizards
        for i in data:
            wizard_id = i["id"]
            wizard_type = i["type"]
            name = None
            possibleValues = None

            if "parameters" in i:
                for idx, param in enumerate(i["parameters"]):
                    if "possibleValues" in param:
                        name = param["name"]
                        possibleValues = param["possibleValues"]
                        # print(name, possibleValues)

            if not wizard_id in collected_wizards:
                collected_wizards[wizard_id] = {
                    "wizard_id": wizard_id,
                    "wizard_type": wizard_type
                }

                if name != None:
                    collected_wizards[wizard_id]["name"] = name
                if possibleValues != None:
                    collected_wizards[wizard_id]["possibleValues"] = possibleValues

        if len(current_wizard_ids) != len(list(set(current_wizard_ids))):
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"This AUID/sapId has duplicate wizard ids, {str(current_wizard_ids)}", url])
            assert False

        SaveToSharedDataDirectory("collected_wizards.json", collected_wizards)
        SaveToSharedDataDirectory("collected_wizards_all.json", data)
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Unhandled response with status code: {response.status_code}", url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        [
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
                        "possibleValues": "null|string|array",
                        "isExternalSource": "boolean",
                        "Extra": "number"
                    }
                ],
                "sapIds": ["string"]
            }
        ]
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
