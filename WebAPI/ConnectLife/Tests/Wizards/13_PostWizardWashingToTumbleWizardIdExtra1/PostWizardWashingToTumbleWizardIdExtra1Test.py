import os, pytest, json, requests, sys, datetime, pandas

api_group_folder_path = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-2])
ROOT_PROJECT_PATH = "\\".join(api_group_folder_path.split("\\")[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson, getWizardIdsForType
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from server_error_json_schema import server_error_json_schema
from base_json_schema_400_error_response_wizards import wizards_400_error_json_schema
from Common.FileHelpers import SaveToSharedDataDirectory, ReadFileFromSharedDataDirectory
from Common.GeneralHelpers import get_possible_errors, get_item_from_list, isNaN, get_number_as_en_word

wizard_ids = getWizardIdsForType("WashingToTumble", ReadFileFromSharedDataDirectory("collected_wizards.json"))
wm_to_td_dir_path = os.path.join(ROOT_PROJECT_PATH, "ExcelFiles/WashingToTumble")
wm_to_td_dir = list(map(lambda x: x.lower(), os.listdir(wm_to_td_dir_path)))

all_test_cases = []

for wizard_id in wizard_ids:
    split_name = wizard_id["wizard_id"].split("_")
    unique_name = "".join(split_name[3:])

    file_name = get_item_from_list(unique_name, wm_to_td_dir)
    if file_name != None and "default" in file_name:
        file_name = None
    if file_name != None:
        excel_file_pd = pandas.read_excel(os.path.join(wm_to_td_dir_path, file_name), sheet_name="Stains")

        number_of_consecutive_empty_rows = 0
        last_row_was_empty = False

        for idx in excel_file_pd.index:
            row = { "wizard_id": wizard_id["wizard_id"], "payload": {}, "expected_response_obj": {} }
            row["payload"]["color"] = str(excel_file_pd["COLOR"][idx])
            row["payload"]["stain"] = str(excel_file_pd["STAIN"][idx])
            row["payload"]["dirtiness"] = str(excel_file_pd["DIRTINESS"][idx])

            row["expected_response_obj"]["selectedProgram"] = str(excel_file_pd["SELECTED_PROGRAM"][idx])
            row["expected_response_obj"]["programOptions"] = str(excel_file_pd["PROGRAM_OPTION"][idx])
            row["expected_response_obj"]["temperature"] = str(excel_file_pd["TEMPARATURE"][idx])

            if row["payload"]["color"] == "nan" and row["payload"]["stain"] == "nan" and row["payload"]["dirtiness"] == "nan":
                if last_row_was_empty:
                    number_of_consecutive_empty_rows += 1
                    last_row_was_empty = True
                else:
                    number_of_consecutive_empty_rows = 1
                    last_row_was_empty = True
            else:
                all_test_cases.append(row)
                last_row_was_empty = False
                number_of_consecutive_empty_rows = 0

            if number_of_consecutive_empty_rows >= 3:
                break

if all_test_cases == []:
    for wizard_id in wizard_ids:
        if "default" in wizard_id["wizard_id"]:
            row = { "wizard_id": wizard_id["wizard_id"], "payload": {}, "expected_response_obj": {} }
            row["payload"] = {
                "color": "White",
                "stain": "Fruits",
                "dirtiness": "Low"
            }
            row["expected_response_obj"] = {
                "selectedProgram": "5",
                "programOptions": "PROGRAM_OPTION_WATER_PLUS",
                "temperature": "60"
            }
            all_test_cases.append(row)

@pytest.mark.test_env
@pytest.mark.parametrize("test_case_obj", all_test_cases)
def test_post_wizard_washing_to_tumble_wizard_id_extra1(token: str, test_case_obj):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "wizard_id", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/wizard/washing-to-tumble/{test_case_obj['wizard_id']}/extra1"
    print("\nTesting " + url)
    
    payload = test_case_obj["payload"]
    
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", test_case_obj["wizard_id"], str(test_case_obj["payload"]), url])
        assert False

    if not response.status_code in [200, 400, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", test_case_obj["wizard_id"], str(test_case_obj["payload"]), url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", test_case_obj["wizard_id"], str(test_case_obj["payload"]), url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", test_case_obj["wizard_id"], str(test_case_obj["payload"]), url])
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", test_case_obj["wizard_id"], str(test_case_obj["payload"]), url])
        assert False
    
    if response.status_code == 200:
        errors = ""
        errors += get_possible_errors(data, test_case_obj["expected_response_obj"], "selectedProgram")
        errors += get_possible_errors(data, test_case_obj["expected_response_obj"], "programOptions")
        errors += get_possible_errors(data, test_case_obj["expected_response_obj"], "temperature")

        if errors != "":
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{errors}", test_case_obj["wizard_id"], str(test_case_obj["payload"]), url])
            assert False
    elif response.status_code == 400:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{data}", test_case_obj["wizard_id"], str(test_case_obj["payload"]), url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", test_case_obj["wizard_id"], str(test_case_obj["payload"]), url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", test_case_obj["wizard_id"], str(test_case_obj["payload"]), url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        {
            "selectedProgram": "string",
            "programOptions": ["string"],
            "temperature": "string",
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
