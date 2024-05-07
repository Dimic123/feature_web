import os, pytest, json, requests, sys, datetime

api_group_folder_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
ROOT_PROJECT_PATH = os.sep.join(api_group_folder_path.split(os.sep)[:-3])
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

def generate_test_case_with_all_categories(all_categories, all_previously_generated_test_cases):
    test_case = { "node": [], "outputs": [], "wizard_id": wizard_obj["wizard_id"] }

    for category in all_categories:
        test_case["node"].append({ "CATEGORY": category })

        for p_test_case in all_previously_generated_test_cases:
            if p_test_case["node"]["CATEGORY"] == category:
                test_case["outputs"].append(p_test_case["outputs"])
                break
    return test_case

wizard_ids = getWizardIdsForType("Storingfood", ReadFileFromSharedDataDirectory("collected_wizards.json"))
all_test_cases_with_wizard_id = []

hybris_token = getHybrisToken()
if hybris_token != "":
    wizards = get_all_wizard_logic_xml(hybris_token)

    for wizard_obj in wizards:
        all_storing_food_categories = []

        if any(x["wizard_id"] == wizard_obj["wizard_id"] for x in wizard_ids):
            if not "default" in wizard_obj["wizard_id"]:
                excel_configuration_list = [
                    {
                        "name": "refridgerator_wizard_sheet",
                        "excel_sheet": [],
                        "excel_sheet_criteria": [
                            {
                                "type": "node",
                                "property": "CATEGORY"
                            },
                            {
                                "type": "outputs",
                                "property": "CATEGORY"
                            }
                        ]
                    }
                ]

                convert_xml_to_json_GENERIC(wizard_obj["logic"], excel_configuration_list)
                for config in excel_configuration_list:
                    if config["name"] == "refridgerator_wizard_sheet":
                        refridgerator_wizard_sheet = config["excel_sheet"]
                        for row in config["excel_sheet"]:
                            all_storing_food_categories.append(row["node"]["CATEGORY"])

                for test_case in refridgerator_wizard_sheet:
                    if not "default" in wizard_obj["wizard_id"]:
                        test_case["wizard_id"] = wizard_obj["wizard_id"]
                # all_test_cases_with_wizard_id += refridgerator_wizard_sheet

                test_case_with_all_categories = generate_test_case_with_all_categories(all_storing_food_categories, refridgerator_wizard_sheet)
                all_test_cases_with_wizard_id += [test_case_with_all_categories]

@pytest.mark.prod_api
@pytest.mark.parametrize("test_case", all_test_cases_with_wizard_id)
def test_post_wizard_storingfood_multiple_wizard_id(token: str, test_case):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "wizard_id", "payload", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/wizard/storingfood/multiple/{test_case['wizard_id']}"
    print("\nTesting " + url)

    _payload = []
    _expected_results = []

    if len(test_case["node"]) == 1:
        _payload.append( { "category": test_case["node"]["CATEGORY"] } )
        _expected_results = [ { "wizardId": test_case['wizard_id'], "category": test_case["outputs"]["CATEGORY"] } ]

        if "STORAGE_ZONE" in test_case["outputs"]:
            _expected_results[0]["storageZone"] = test_case["outputs"]["STORAGE_ZONE"]
        if "FREEZER_ZONE" in test_case["outputs"]:
            _expected_results[0]["freezerZone"] = test_case["outputs"]["FREEZER_ZONE"]
        if "STORAGE_SHELF" in test_case["outputs"]:
            _expected_results[0]["storageShelf"] = test_case["outputs"]["STORAGE_SHELF"]
        if "FREEZER_SHELF" in test_case["outputs"]:
            _expected_results[0]["freezerShelf"] = test_case["outputs"]["FREEZER_SHELF"]
        if "STORAGE_TEMPARATURE" in test_case["outputs"]:
            _expected_results[0]["storageTemperature"] = test_case["outputs"]["STORAGE_TEMPARATURE"]
        if "FREEZER_TEMPARATURE" in test_case["outputs"]:
            _expected_results[0]["freezerTemperature"] = test_case["outputs"]["FREEZER_TEMPARATURE"]
        if "ETILEN_ZONE" in test_case["outputs"]:
            _expected_results[0]["etilenZone"] = test_case["outputs"]["ETILEN_ZONE"]
        if "DURATION" in test_case["outputs"]:
            _expected_results[0]["duration"] = test_case["outputs"]["DURATION"]
        if "FREEZER_DURATION" in test_case["outputs"]:
            _expected_results[0]["freezerDuration"] = test_case["outputs"]["FREEZER_DURATION"]
    else:
        for el in test_case["node"]:
            _payload.append( { "category": el["CATEGORY"] } )

        for output in test_case["outputs"]:
            out_obj = { "wizardId": test_case['wizard_id'] }

            if "STORAGE_ZONE" in output:
                out_obj["storageZone"] = output["STORAGE_ZONE"]
            if "FREEZER_ZONE" in output:
                out_obj["freezerZone"] = output["FREEZER_ZONE"]
            if "STORAGE_SHELF" in output:
                out_obj["storageShelf"] = output["STORAGE_SHELF"]
            if "FREEZER_SHELF" in output:
                out_obj["freezerShelf"] = output["FREEZER_SHELF"]
            if "STORAGE_TEMPARATURE" in output:
                out_obj["storageTemperature"] = output["STORAGE_TEMPARATURE"]
            if "FREEZER_TEMPARATURE" in output:
                out_obj["freezerTemperature"] = output["FREEZER_TEMPARATURE"]
            if "ETILEN_ZONE" in output:
                out_obj["etilenZone"] = output["ETILEN_ZONE"]
            if "DURATION" in output:
                out_obj["duration"] = output["DURATION"]
            if "FREEZER_DURATION" in output:
                out_obj["freezerDuration"] = output["FREEZER_DURATION"]

            _expected_results.append(out_obj)

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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", test_case["wizard_id"], str(_payload), url])
        assert False

    if not response.status_code in [200, 400, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", test_case["wizard_id"], str(_payload), url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", test_case["wizard_id"], str(_payload), url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", test_case["wizard_id"], str(_payload), url])
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", test_case["wizard_id"], str(_payload), url])
        assert False
    
    if response.status_code == 200:
        if len(data) != len(_expected_results):
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Number of returned objects[{len(data)}] is different than what was expected[{len(_expected_results)}]", test_case["wizard_id"], _payload["category"], url])
            assert False

        list_of_errors = []
        for idx, response_obj in enumerate(data):
            errors = ""
            if "storageZone" in _expected_results[idx]:
                errors += get_possible_errors(response_obj, _expected_results[idx], "storageZone")
            if "freezerZone" in _expected_results[idx]:
                errors += get_possible_errors(response_obj, _expected_results[idx], "freezerZone")
            if "category" in _expected_results[idx]:
                errors += get_possible_errors(response_obj, _expected_results[idx], "category")
            if "storageShelf" in _expected_results[idx]:
                errors += get_possible_errors(response_obj, _expected_results[idx], "storageShelf")
            if "freezerShelf" in _expected_results[idx]:
                errors += get_possible_errors(response_obj, _expected_results[idx], "freezerShelf")
            if "storageTemperature" in _expected_results[idx]:
                errors += get_possible_errors(response_obj, _expected_results[idx], "storageTemperature")
            if "freezerTemperature" in _expected_results[idx]:
                errors += get_possible_errors(response_obj, _expected_results[idx], "freezerTemperature")
            if "duration" in _expected_results[idx]:
                errors += get_possible_errors(response_obj, _expected_results[idx], "duration")
            if "freezerDuration" in _expected_results[idx]:
                errors += get_possible_errors(response_obj, _expected_results[idx], "freezerDuration")
            errors += get_possible_errors(response_obj, _expected_results[idx], "wizardId")

            if errors != "":
                list_of_errors.append({ "error_msg": errors, "payload": str(_payload[idx]) })
        if len(list_of_errors) > 0:
            for err in list_of_errors:
                pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{err['error_msg']}", test_case["wizard_id"], err["payload"], url])
            assert False
    elif response.status_code == 400:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{data}", test_case["wizard_id"], str(_payload), url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", test_case["wizard_id"], str(_payload), url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", test_case["wizard_id"], str(_payload), url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        [
            {
                "category": "string",
                "storageShelf": "string",
                "freezerShelf": "string",
                "storageTemperature": "string",
                "freezerTemperature": "string",
                "duration": "string",
                "freezerDuration": "string",
                "etilenZone": "string",
                "wizardId": "string"
            }
        ]
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
