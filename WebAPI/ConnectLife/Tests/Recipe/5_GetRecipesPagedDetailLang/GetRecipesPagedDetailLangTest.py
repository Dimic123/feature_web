import os, pytest, json, requests, sys, datetime

api_group_folder_path = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-2])
ROOT_PROJECT_PATH = "\\".join(api_group_folder_path.split("\\")[:-3])
sys.path.append(api_group_folder_path)

from Common.JsonHelpers import ValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from server_error_json_schema import server_error_json_schema
from Common.FileHelpers import ReadFileFromSharedDataDirectory

recipesPagedDetailLang = ReadFileFromSharedDataDirectory("recipesPagedDetailLang.json")

test_cases = []

for recipePage in recipesPagedDetailLang:
    numPages = int(recipePage["numPages"])
    pageSize = int(recipePage["pageSize"])
    for count in range(0, numPages - 1):
        test_cases.append({
            "lang": recipePage["lang"],
            "pageDetails": f"?page={count}&pageSize={pageSize}"
        })

@pytest.mark.test_env
@pytest.mark.parametrize("test_case", test_cases)
def test_get_recipes_paged_detail_lang(token: str, test_case):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "lang", "pageDetails", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/recipes/paged/detail/{test_case['lang']}{test_case['pageDetails']}"
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", test_case['lang'], test_case['pageDetails'], url])
        assert False

    if not response.status_code in [200, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", test_case['lang'], test_case['pageDetails'], url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", test_case['lang'], test_case['pageDetails'], url])
        assert False
    
    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", test_case['lang'], test_case['pageDetails'], url])
        assert False
    
    [success_200_schema, error_500_schema] = CreateJsonSchemas()
    
    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)
    
    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", test_case['lang'], test_case['pageDetails'], url])
        assert False
    
    if response.status_code == 200:
        pass
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", test_case['lang'], test_case['pageDetails'], url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", test_case['lang'], test_case['pageDetails'], url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
        {
            "count": "number",
            "pageSize": "number",
            "numPages": "number",
            "currentPage": "number",
            "links": [
                {
                "href": "string",
                "rel": "string",
                "method": "string",
                "isTemplated": "boolean"
                }
            ],
            "items": [
                {
                "id": "string",
                "title": "string",
                "imageUrl": "string",
                "difficulty": "string",
                "noOfPersonsDefault": "number",
                "noOfPersonsMin": "number",
                "noOfPersonsMax": "number",
                "type": "string",
                "description": "string",
                "allergens": [
                    {
                    "id": "string",
                    "title": "string",
                    "desc": "null|string"
                    }
                ],
                "steps": [
                    {
                    "desc": "string",
                    "id": "string"
                    }
                ],
                "diet": [
                    {
                    "iconUrl": "null|string",
                    "id": "string",
                    "title": "string",
                    "desc": "null|string"
                    }
                ],
                "ingredients": [
                    {
                    "id": "string",
                    "title": "string",
                    "friendlyQuantity": "string",
                    "isLockable": "boolean",
                    "quantity": "number",
                    "unit": "string",
                    "commonName": "string"
                    }
                ],
                "links": [
                    {
                    "href": "string",
                    "rel": "string",
                    "method": "string",
                    "isTemplated": "boolean"
                    }
                ],
                "totalPreparationTime": "number",
                "cuisine": "string",
                "mainIngredient": [
                    "string"
                ],
                "nutrition": [
                    "string"
                ],
                "occasion": [
                    "string"
                ],
                "winePairing": [
                    "string"
                ]
                }
            ]
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_200", file_path, success_200_schema)

    error_500_schema = CreateJsonSchema(
        "Server error 500 json schema", 
        "General server error schema", 
        server_error_json_schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error_500", file_path, error_500_schema)
    
    return [success_200_schema, error_500_schema]
