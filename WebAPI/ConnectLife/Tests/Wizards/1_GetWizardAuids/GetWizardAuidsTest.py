import os, pytest, json, requests, sys, datetime

api_group_folder_path = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-2])
ROOT_PROJECT_PATH = "\\".join(api_group_folder_path.split("\\")[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from server_error_json_schema import server_error_json_schema
from Common.FileHelpers import SaveToSharedDataDirectory, ReadFileFromSharedDataDirectory, ReadFileFromStaticDataDirectory

manually_added_auids = [
    "0000000000007391270001202400040260001", 
    "0000000000007393970004202300030330003"
]

sapIds_list = ReadFileFromSharedDataDirectory("sapIds.json")
auids = list(map((lambda x: "000000000000" + str(x) + "0000000000000000000"), sapIds_list))
read_auids = ReadFileFromStaticDataDirectory("auids.json")

all_auids = auids + read_auids

if all_auids == []:
    all_auids = manually_added_auids

collected_wizards = {}

@pytest.mark.test_env
@pytest.mark.parametrize("auid", all_auids)
def test_get_wizard_auids(token: str, auid):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "auid", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/wizard/{auid}" # + "?includeLogicData=true"
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", auid, url])
        assert False

    if not response.status_code in [200, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", auid, url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", auid, url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", auid, url])
        assert False
    
    [success_200_schema, error_500_schema] = CreateJsonSchemas()
    
    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)

    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", auid, url])
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
                        print(name, possibleValues)

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
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"This AUID/sapId has duplicate wizard ids", auid, url])
            assert False

        SaveToSharedDataDirectory("collected_wizards.json", collected_wizards)
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", auid, url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", auid, url])
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
        server_error_json_schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_500_schema]
