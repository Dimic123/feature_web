import os, pytest, json, requests, sys, datetime

api_group_folder_path = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
ROOT_PROJECT_PATH = os.sep.join(api_group_folder_path.split(os.sep)[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import ReadFileFromSharedDataDirectory, ReadFileFromStaticDataDirectory
from Common.GeneralHelpers import create_auid_from_sapId

manually_added_auids = [
    "0000000000007391270001202400040260001", 
    "0000000000007393970004202300030330003"
]

sapIds_list = ReadFileFromSharedDataDirectory("sapIds.json")
auids = list(map(create_auid_from_sapId, sapIds_list))
read_auids = ReadFileFromStaticDataDirectory("auids.json")

all_auids = read_auids + auids

if all_auids == []:
    all_auids = manually_added_auids

@pytest.mark.skip(reason="test takes too long after n-th test case")
@pytest.mark.prod_api
@pytest.mark.parametrize("auid", all_auids)
def test_get_faqs_auids_pre_test(token: str, auid):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "elapsed_time", "error", "auid", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/faqs/{auid}"
    print("\nTesting " + url)
    
    req_res_times = []
    dir_folder_name = os.path.dirname(os.path.realpath(__file__)).split(os.sep)
    folder_name = dir_folder_name.pop(-1)
    group_name = dir_folder_name.pop(-1)

    response = None
    attempts = 1
    while attempts <= 5:
        try:
            response = requests.request("GET", url, headers={ 'Authorization': 'Bearer ' + token + '' }, data={}, timeout=(10 * attempts))
            req_res_times.append(response.elapsed.total_seconds())
            break
        except requests.exceptions.Timeout:
            req_res_times.append(10 * attempts)
            attempts += 1
            print(f"Request attempt: #{attempts}")

    req_res_duration = min(req_res_times)
    pytest.timers[group_name][folder_name]["values"].append(req_res_duration)

    if response == None:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Request timed out {attempts} time/s", auid, url])
        assert False

    if not response.status_code in [200, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Unknown response status code: { str(response.status_code) }", auid, url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Exception: {ex}, Malformed data: {str(response.text)}", auid, url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Empty response: {data}", auid, url])
        assert False
    
    [success_200_schema, error_500_schema] = CreateJsonSchemas()

    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)
    
    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"{isValidOrTrue}", auid, url])
        assert False
    
    if response.status_code == 200:
        pytest.data_collections[__name__][auid] = []
        for el in data:
            if "id" in el:
                pytest.data_collections[__name__][auid].append({ "id": el["id"] })
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", auid, url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), req_res_duration, f"Unhandled response with status code: {response.status_code}", auid, url])
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
                "attachments": "null|string|array",
                "content": "string",
                "lang": "string",
                "sapId": "string",
                "contentCode": "string"
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
