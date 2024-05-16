import os, pytest, json, requests, sys, datetime

api_group_folder_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
ROOT_PROJECT_PATH = os.sep.join(api_group_folder_path.split(os.sep)[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import ReadFileFromSharedDataDirectory, SaveToSharedDataDirectory

def join_fifty_auids_and_return_as_string(manually_added_auids, auids):
    auids_list = manually_added_auids
    for auid in auids:
        if len(auids_list) < 50:
            auids_list.append(auid)
        else:
            break
    return ";".join(auids_list)

def validate_multiple_properties_in_response_object(property_name, data, validation_schema):
    possible_errors = ""
    for auid in data[property_name].keys():
        appliance_profile = data[property_name][auid]
        isValidOrTrue = ValidateJson(appliance_profile, validation_schema)
        if isValidOrTrue != True:
            possible_errors += isValidOrTrue + ". "
    return possible_errors

auids = []
manually_added_auids = [
    "0000000000007378500001202000003830003",
    "0000000000007378910001202300030360001",
    "0000000000007378910001202300030360002",
    "0000000000007378910001202300033860002",
    "0000000000007394880001202200022460001",
    "0000000000007394030001202200022460001",
    "0000000000007377260001202100001160001",
    "0000000000007370910001202300030360001"
]

sapIds_list = ReadFileFromSharedDataDirectory("sapIds.json")
auids = list(map((lambda x: "000000000000" + str(x) + "0000000000000000000"), sapIds_list))

auids_string = join_fifty_auids_and_return_as_string(manually_added_auids, auids)

@pytest.mark.prod_api
@pytest.mark.parametrize("auid", [auids_string])
def test_get_appliances_profile_multi_auids_pre_test(token: str, auid):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "elapsed_time", "error", "auid", "endpoint"])

    url = f"{pytest.api_base_url}/api/v1/appliance/appliance-profile/multi/{auid}"
    print("\nTesting " + url)
    
    req_res_times = []
    dir_folder_name = os.path.dirname(os.path.realpath(__file__)).split(os.sep)
    test_name = dir_folder_name.pop(-1)

    headers = { 'Authorization': 'Bearer ' + token + '' }
    
    response = None
    attempts = 1
    while attempts <= 5:
        try:
            response = requests.request("GET", url, headers=headers, data={}, timeout=(10 * attempts))
            req_res_times.append(response.elapsed.total_seconds())
            break
        except requests.exceptions.Timeout:
            attempts += 1
            print(f"Request attempt: #{attempts}")
    
    req_res_duration = min(req_res_times)
    pytest.timers[test_name].append(req_res_duration)

    if response == None:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Request timed out {attempts} time/s", str(auid), url])
        assert False

    if not response.status_code in [200, 400, 404, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Unknown response status code: { str(response.status_code) }", str(auid), url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Exception: {ex}, Malformed data: {str(response.text)}", str(auid), url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Empty response: {data}", str(auid), url])
        assert False
    
    [success_200_schema, error_400_schema, error_500_schema] = CreateJsonSchemas()

    isValidOrTrue = True
    if (response.status_code == 200):
            error_msg = ""
            if "appliance-profiles" in data:
                possible_errors = validate_multiple_properties_in_response_object("appliance-profiles", data, success_200_schema)
                if "errors" in data:
                    possible_errors += validate_multiple_properties_in_response_object("errors", data, error_400_schema)
                    if possible_errors != "":
                        error_msg += ". " + possible_errors
                else:
                    error_msg += "'errors' missing from response object. "
            else:
                error_msg += "'appliance-profiles' missing from response object. "
            
            if error_msg != "":
                pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"{error_msg}", str(auid), url])
                assert False
    elif (response.status_code == 400):
        isValidOrTrue = ValidateJson(data, error_400_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)
    
    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"{isValidOrTrue}", str(auid), url])
        assert False
    
    if response.status_code == 200:
        pass
    elif response.status_code == 400:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"statusDescription: {data['statusDescription']}, statusCode: {data['statusCode']}", str(auid), url])
        assert False
    elif response.status_code == 404:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"statusDescription: {data['statusDescription']}, statusCode: {data['statusCode']}", str(auid), url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", str(auid), url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Unhandled response with status code: {response.status_code}", str(auid), url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET /api/v1/appliance/appliance-profile/{auid}: SUCCESS 200", 
        "Gets appliance profile by auid.",
        {
            "statusCode": "string",
            "statusDescription": "string",
            "additionalData": [
                {
                "group": "string",
                "name": "string",
                "value": "string"
                }
            ],
            "auId": "string",
            "characteristics": {
                "country": "string",
                "purchasingAndWarrantyData": {
                "appliancesMedia": [
                    {
                    "binaryData": "string",
                    "type": "string",
                    "url": "string"
                    }
                ],
                "durationOfWarranty": "number",
                "durationUnitOfMeasure": "string",
                "purchaseDate": "string",
                "purchasedAtShop": {
                    "address": {
                    "addressType": "string",
                    "street": "string",
                    "houseNumber": "string",
                    "postalCode": "string",
                    "city": "string",
                    "country": "string",
                    "gpsInfo": {
                        "latitude": "number",
                        "longitude": "number"
                    }
                    },
                    "description": "string",
                    "name": "string",
                    "type": "string"
                },
                "warrantyEndDate": "string",
                "extendedWaranty": "boolean",
                "warranties": [
                    {
                    "type": "string",
                    "code": "string",
                    "durationOfWarranty": "number",
                    "startsAfterBaseWarranty": "boolean",
                    "parts": [
                        {
                        "attribute": "string",
                        "value": "string"
                        }
                    ]
                    }
                ]
                },
                "brand": "string",
                "modelMark": "string",
                "typeMark": "string"
            },
            "connectable": "boolean",
            "country": "string",
            "descriptions": [
                {
                "description": "string",
                "language": "string"
                }
            ],
            "heidi": "string",
            "name": "string",
            "photoUrl": "string",
            "productFamily": "string",
            "serviceIndex": "string",
            "source": "string",
            "type": "string",
            "Firmware": {
                "WiFi": "string",
                "MCU1": "string",
                "MCU2": "string",
                "MCU3": "string",
                "MCU4": "string",
                "MCU5": "string",
                "MCU6": "string",
                "MCU7": "string",
                "MCU8": "string",
                "MCU9": "string",
                "MCU10": "string",
                "extMCU0": "string",
                "extMCU1": "string",
                "extMCU2": "string",
                "extMCU3": "string",
                "extMCU4": "string",
                "extMCU5": "string"
            },
            "puid": "string",
            "realFeatureCode": "string",
            "externalId": "string",
            "QualityTest": "string",
            "lastChangeDateTime": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_200", file_path, success_200_schema)

    error_400_schema = CreateJsonSchema(
        "Error 400 Bad request", 
        "Error 400: Gets appliance profile by auid", 
        {
            "statusCode": "string",
            "statusDescription": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_400", file_path, error_400_schema)

    error_500_schema = CreateJsonSchema(
        "Server error 500 json schema", 
        "General server error schema", 
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_400_schema, error_500_schema]
