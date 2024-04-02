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

payloads = ReadFileFromSharedDataDirectory("Put_appliances_payloads_profile_afota.json")
sapIds_list = ReadFileFromSharedDataDirectory("sapIds.json")

auids = list(map((lambda x: "000000000000" + str(x) + "0000000000000000000"), sapIds_list))

if auids == []:
    auids = manually_added_auids

def getPayloadByAuid(auid, payloads):
    for payload in payloads:
        if payload["auid"] == auid:
            return payload
    return None

@pytest.mark.test_env
@pytest.mark.parametrize("auid", auids)
def test_get_appliances_profile_auids(token: str, auid):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "auid", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/appliance/appliance-profile/{auid}"
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", str(auid), url])
        assert False

    if not response.status_code in [200, 400, 404, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", str(auid), url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", str(auid), url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", str(auid), url])
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", str(auid), url])
        assert False
    
    if response.status_code == 200:
        global payloads
        payload = getPayloadByAuid(auid, payloads)

        unchanged_appliance_profile = False
        if payload != None:
            if "Firmware" in data:
                for prop in data["Firmware"]:
                    if data["Firmware"][prop] != payload["firmware"][prop]:
                        unchanged_appliance_profile = True
        if unchanged_appliance_profile:
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"appliance-profile changes were not saved", str(auid), url])
    elif response.status_code == 400:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"statusDescription: {data['statusDescription']}, statusCode: {data['statusCode']}", str(auid), url])
        assert False
    elif response.status_code == 404:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"statusDescription: {data['statusDescription']}, statusCode: {data['statusCode']}", str(auid), url])
        assert False
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", str(auid), url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", str(auid), url])
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
    
    error_404_schema = CreateJsonSchema(
        "Error 404 Not found", 
        "Error 404: Gets appliance profile by auid", 
        {
            "statusCode": "string",
            "statusDescription": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_404", file_path, error_404_schema)

    error_500_schema = CreateJsonSchema(
        "Server error 500 json schema", 
        "General server error schema", 
        server_error_json_schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_400_schema, error_404_schema, error_500_schema]
