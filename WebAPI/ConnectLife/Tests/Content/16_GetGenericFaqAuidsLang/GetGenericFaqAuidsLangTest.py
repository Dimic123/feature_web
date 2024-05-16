import os, pytest, json, requests, sys, datetime

api_group_folder_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
ROOT_PROJECT_PATH = os.sep.join(api_group_folder_path.split(os.sep)[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from server_error_json_schema import server_error_json_schema
from Common.FileHelpers import ReadFileFromSharedDataDirectory, ReadFileFromStaticDataDirectory
from Common.GeneralHelpers import create_auid_from_sapId

manually_added_auids = [
    "0000000000007391270001202400040260001", 
    "0000000000007393970004202300030330003"
]

sapIds_list = ReadFileFromSharedDataDirectory("sapIds.json")
auids = list(map(create_auid_from_sapId, sapIds_list))
read_auids = ReadFileFromStaticDataDirectory("auids.json")
langs = ReadFileFromStaticDataDirectory("languages.json")

all_auids = auids + read_auids

if all_auids == []:
    all_auids = manually_added_auids

@pytest.mark.prod_api
@pytest.mark.parametrize("auid", all_auids)
@pytest.mark.parametrize("lang", langs)
def test_get_generic_faq_auids_lang(token: str, auid, lang):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "auid", "lang", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/generic-faq/{auid}/{lang}"
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", auid, lang, url])
        assert False

    if not response.status_code in [200, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", auid, lang, url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", auid, lang, url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", auid, lang, url])
        assert False
    
    [success_200_schema, error_500_schema] = CreateJsonSchemas()
    
    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)
    
    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", auid, lang, url])
        assert False
    
    if response.status_code == 200:
        pass
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", auid, lang, url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", auid, lang, url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        [
            {
                "id": "string",
                "title": "string",
                "name": "string",
                "shortDescription": "null|string",
                "attachments": "null|array",
                "content": "string",
                "lang": "string",
                "sapId": "string",
                "contentCode": "null|array|object"
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
