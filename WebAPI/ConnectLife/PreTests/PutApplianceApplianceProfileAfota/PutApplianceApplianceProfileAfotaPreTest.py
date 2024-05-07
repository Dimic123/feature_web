import os, pytest, json, requests, sys, datetime
from random import randint

api_group_folder_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
ROOT_PROJECT_PATH = os.sep.join(api_group_folder_path.split(os.sep)[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson, getWizardIdsForType
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import SaveToSharedDataDirectory, ReadFileFromSharedDataDirectory

products_arr = ReadFileFromSharedDataDirectory("list_of_products_by_auids.json")

filtered_products = []
for product_arr in products_arr:
    for product in product_arr:
        if "mcuNumber" in product:
            if len(product["mcuNumber"]) > 0:
                if len(product["auid"]) == 37: # only get AUIDs
                    filtered_products.append(product)

payloads = []

@pytest.mark.prod_api
@pytest.mark.parametrize("test_case_obj", filtered_products)
def test_put_appliance_appliance_profile_afota_pre_test(token: str, test_case_obj):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "auid", "payload.firmware", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/appliance/appliance-profile-afota"
    print("\nTesting " + url)
    
    payload = {
        "auid": test_case_obj["auid"],
        "firmware": {
            "WiFi": "string"
        }
    }

    for mcuNumber in test_case_obj["mcuNumber"]:
        payload["firmware"][mcuNumber] = f"{randint(100, 999)}.{randint(100, 999)}.{randint(100, 999)}"
    
    headers = {
        'Authorization': 'Bearer ' + token + '',
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json"
    }
    
    response = None
    attempts = 1
    while attempts <= 5:
        try:
            response = requests.request("PUT", url, headers=headers, data=json.dumps(payload), timeout=(10 * attempts))
            break
        except requests.exceptions.Timeout:
            attempts += 1
            print(f"Request attempt: #{attempts}")
    
    if response == None:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", test_case_obj["auid"], str(payload), url])
        assert False

    if not response.status_code in [200, 400, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", test_case_obj["auid"], str(payload), url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", test_case_obj["auid"], str(payload), url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", test_case_obj["auid"], str(payload), url])
        assert False
    
    [success_200_schema, error_400_schema, error_404_schema, error_500_schema] = CreateJsonSchemas()
    
    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 400):
        isValidOrTrue = ValidateJson(data, error_400_schema)
    elif (response.status_code == 404):
        isValidOrTrue = ValidateJson(data, error_404_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)

    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", test_case_obj["auid"], str(payload), url])
        assert False
    
    if response.status_code == 200:
        payloads.append(payload)
        SaveToSharedDataDirectory("Put_appliances_payloads_profile_afota.json", payloads)
    elif response.status_code == 400:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"statusDescription: {data['statusDescription']}, statusCode: {data['statusCode']}", test_case_obj["auid"], str(payload), url])
        assert False
    elif response.status_code == 404:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"statusDescription: {data['statusDescription']}, statusCode: {data['statusCode']}", test_case_obj["auid"], str(payload), url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", test_case_obj["auid"], str(payload), url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", test_case_obj["auid"], str(payload), url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        {
            "statusCode": "string",
            "statusDescription": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_200", file_path, success_200_schema)

    error_400_schema = CreateJsonSchema(
        "Server error 400 json schema", 
        "General server error schema", 
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_400", file_path, error_400_schema)

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
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_400_schema, error_404_schema, error_500_schema]
