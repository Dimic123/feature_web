import os, pytest, json, requests, sys, datetime, pandas

api_group_folder_path = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-2])
ROOT_PROJECT_PATH = "\\".join(api_group_folder_path.split("\\")[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson, getWizardIdsForType
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from server_error_json_schema import server_error_json_schema
from Common.FileHelpers import ReadFileFromSharedDataDirectory
from Common.GeneralHelpers import isNaN, get_possible_errors, get_item_from_list

wizard_ids = getWizardIdsForType("Storingfood", ReadFileFromSharedDataDirectory("collected_wizards.json"))
storing_food_dir_path = os.path.join(ROOT_PROJECT_PATH, "ExcelFiles/StoringFood")
storing_food_dir = os.listdir(storing_food_dir_path)

all_test_cases = []

for wizard_id in wizard_ids:
    split_name = wizard_id["wizard_id"].split("_")
    unique_name = split_name[len(split_name) - 1]

    file_name = get_item_from_list(unique_name, storing_food_dir)
    if "default" in file_name:
        file_name = None
    if file_name != None:
        excel_file_pd = pandas.read_excel(os.path.join(storing_food_dir_path, file_name), sheet_name="RefridgeratorWizard")

        for idx in excel_file_pd.index:
            test_case = { "wizard_id": wizard_id["wizard_id"], "payload": {}, "expected_response_obj": {} }
            test_case["payload"]["category"] = excel_file_pd["CATEGORY"][idx]
            test_case["expected_response_obj"]["category"] = excel_file_pd["CATEGORY.1"][idx]
            if not isNaN(excel_file_pd["STORAGE_SHELF"][idx]):
                test_case["expected_response_obj"]["storageShelf"] = excel_file_pd["STORAGE_SHELF"][idx]
            if not isNaN(excel_file_pd["FREEZER_SHELF"][idx]):
                test_case["expected_response_obj"]["freezerShelf"] = excel_file_pd["FREEZER_SHELF"][idx]
            test_case["expected_response_obj"]["storageTemperature"] = excel_file_pd["STORAGE_TEMPARATURE"][idx]
            if not isNaN(excel_file_pd["FREEZER_TEMPARATURE"][idx]):
                test_case["expected_response_obj"]["freezerTemperature"] = excel_file_pd["FREEZER_TEMPARATURE"][idx]
            test_case["expected_response_obj"]["duration"] = excel_file_pd["DURATION"][idx]
            test_case["expected_response_obj"]["freezerDuration"] = excel_file_pd["FREEZER_DURATION"][idx]
            all_test_cases.append(test_case)

@pytest.mark.test_env
@pytest.mark.parametrize("test_case", all_test_cases)
def test_post_wizard_storingfood_wizard_id(token: str, test_case):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "wizard_id", "payload.category", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/wizard/storingfood/{test_case['wizard_id']}"
    print("\nTesting " + url)
    
    payload = test_case["payload"]
    
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", test_case["wizard_id"], test_case["payload"]["category"], url])
        assert False

    if not response.status_code in [200, 400, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", test_case["wizard_id"], test_case["payload"]["category"], url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", test_case["wizard_id"], test_case["payload"]["category"], url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", test_case["wizard_id"], test_case["payload"]["category"], url])
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", test_case["wizard_id"], test_case["payload"]["category"], url])
        assert False
    
    if response.status_code == 200:
        errors = ""
        errors += get_possible_errors(data, test_case["expected_response_obj"], "category")
        errors += get_possible_errors(data, test_case["expected_response_obj"], "storageShelf")
        errors += get_possible_errors(data, test_case["expected_response_obj"], "freezerShelf")
        errors += get_possible_errors(data, test_case["expected_response_obj"], "storageTemperature")
        errors += get_possible_errors(data, test_case["expected_response_obj"], "freezerTemperature")
        errors += get_possible_errors(data, test_case["expected_response_obj"], "duration")
        errors += get_possible_errors(data, test_case["expected_response_obj"], "freezerDuration")

        if errors != "":
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{errors}", test_case["wizard_id"], test_case["payload"]["category"], url])
            assert False
    elif response.status_code == 400:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{data}", test_case["wizard_id"], test_case["payload"]["category"], url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", test_case["wizard_id"], test_case["payload"]["category"], url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", test_case["wizard_id"], test_case["payload"]["category"], url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        {
            "category": "string",
            "storageShelf": "string",
            "freezerShelf": "string",
            "storageTemperature": "string",
            "freezerTemperature": "string",
            "duration": "string",
            "freezerDuration": "string",
            "etilenZone": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_200", file_path, success_200_schema)

    error_400_schema = CreateJsonSchema(
        "Server error 400 json schema", 
        "General server error schema", 
        {
            "type": "string",
            "title": "string",
            "status": "number",
            "traceId": "string",
            "errors": "object"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_400", file_path, error_400_schema)

    error_500_schema = CreateJsonSchema(
        "Server error 500 json schema", 
        "General server error schema", 
        server_error_json_schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_400_schema, error_500_schema]
