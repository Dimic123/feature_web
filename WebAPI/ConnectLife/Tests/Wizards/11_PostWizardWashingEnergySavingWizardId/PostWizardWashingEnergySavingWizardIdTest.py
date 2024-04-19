import os, pytest, json, requests, sys, datetime

api_group_folder_path = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-2])
ROOT_PROJECT_PATH = "\\".join(api_group_folder_path.split("\\")[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson, getWizardIdsForType
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from server_error_json_schema import server_error_json_schema
from base_json_schema_400_error_response_wizards import wizards_400_error_json_schema
from Common.FileHelpers import ReadFileFromSharedDataDirectory
from Common.GeneralHelpers import get_possible_errors
from WebAPI.ConnectLife.Common.HybrisAuthorization import getHybrisToken
from Common.HybrisHelpers import get_all_wizard_logic_xml, convert_xml_to_json_GENERIC

wizard_ids = getWizardIdsForType("WashingEnergySaving", ReadFileFromSharedDataDirectory("collected_wizards.json"))
all_test_cases_with_wizard_id = []

hybris_token = getHybrisToken()
if hybris_token != "":
    wizards = get_all_wizard_logic_xml(hybris_token)

    for wizard_obj in wizards:
        if any(x["wizard_id"] == wizard_obj["wizard_id"] for x in wizard_ids):
            # if not "default" in wizard_obj["wizard_id"]:
            excel_configuration_list = [
                {
                    "name": "energy_saving_wizard_sheet",
                    "excel_sheet": [],
                    "excel_sheet_criteria": [
                        {
                            "type": "node",
                            "property": "PROGRAM"
                        },
                        {
                            "type": "node",
                            "property": "PROGRAM_OPTION"
                        }
                    ]
                }
            ]

            convert_xml_to_json_GENERIC(wizard_obj["logic"], excel_configuration_list)
            for config in excel_configuration_list:
                if config["name"] == "energy_saving_wizard_sheet":
                    energy_saving_wizard_sheet = config["excel_sheet"]

            for test_case in energy_saving_wizard_sheet:
                if not "default" in wizard_obj["wizard_id"]:
                    test_case["wizard_id"] = wizard_obj["wizard_id"]
            all_test_cases_with_wizard_id += energy_saving_wizard_sheet

@pytest.mark.test_env
@pytest.mark.parametrize("test_case_obj", all_test_cases_with_wizard_id)
def test_post_wizard_washing_energy_saving_wizard_id(token: str, test_case_obj):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "wizard_id", "payload", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/wizard/washing-energy-saving/{test_case_obj['wizard_id']}"
    print("\nTesting " + url)

    _payload = { 
        "program": test_case_obj["node"]["PROGRAM"],
        "programOptions": test_case_obj["node"]["PROGRAM_OPTION"].split("+"),
        "temperature": test_case_obj["node"]["TEMPARATURE"]
    }

    _expected_results = {
        "wizardId": test_case_obj['wizard_id'],
        "eco": test_case_obj["outputs"]['ECO']
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
            response = requests.request("POST", url, headers=headers, data=json.dumps(_payload), timeout=(10 * attempts))
            break
        except requests.exceptions.Timeout:
            attempts += 1
            print(f"Request attempt: #{attempts}")
    
    if response == None:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", test_case_obj["wizard_id"], _payload, url])
        assert False

    if not response.status_code in [200, 400, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", test_case_obj["wizard_id"], _payload, url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", test_case_obj["wizard_id"], _payload, url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", test_case_obj["wizard_id"], _payload, url])
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", test_case_obj["wizard_id"], _payload, url])
        assert False
    
    if response.status_code == 200:
        errors = ""
        if "eco" in _expected_results:
            errors += get_possible_errors(data, _expected_results, "eco")
        errors += get_possible_errors(data, _expected_results, "wizardId")

        if errors != "":
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{errors}", test_case_obj["wizard_id"], _payload, url])
            assert False
    elif response.status_code == 400:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{data}", test_case_obj["wizard_id"], _payload, url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", test_case_obj["wizard_id"], _payload, url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", test_case_obj["wizard_id"], _payload, url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        {
            "eco": "string",
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
