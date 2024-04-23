import os, pytest, json, requests, sys, datetime

ROOT_PROJECT_PATH = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-4])
sys.path.append(ROOT_PROJECT_PATH)

from Common.JsonHelpers import ValidateJson, getWizardIdsForType
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import ReadFileFromSharedDataDirectory, SaveToSharedDataDirectory, ReadFileFromStaticDataDirectory

langs = ReadFileFromStaticDataDirectory("languages.json")
wizardId_recipeId_pairs = []
recipeId_wizardId_post_request_payload_list = []

wizard_ids = getWizardIdsForType("Recipe", ReadFileFromSharedDataDirectory("collected_wizards.json"))

for wizard_id in wizard_ids:
    for possibleValue in wizard_id["possibleValues"]:
        wizardId_recipeId_pairs.append(
            {
                "wizard_id": wizard_id["wizard_id"],
                "recipe_id": possibleValue
            }
        )

@pytest.mark.test_env
@pytest.mark.parametrize("lang", langs)
@pytest.mark.parametrize("pair", wizardId_recipeId_pairs)
def test_get_recipes_id_lang_pre_test(token: str, pair, lang):
    pytest.log_objects[__name__].writeHeaderToLogFileAsList(["time", "error", "wizard_id", "recipe_id", "lang", "endpoint"])
    url = f"{pytest.api_base_url}/api/v1/recipes/{pair['recipe_id']}/{lang}"
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
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Request timed out {attempts} time/s", pair['wizard_id'], pair['recipe_id'], lang, url])
        assert False

    if not response.status_code in [200, 500]:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unknown response status code: { str(response.status_code) }", pair['wizard_id'], pair['recipe_id'], lang, url])
        assert False

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Exception: {ex}, Malformed data: {str(response.text)}", pair['wizard_id'], pair['recipe_id'], lang, url])
        assert False

    if len(data) <= 0:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Empty response: {data}", pair['wizard_id'], pair['recipe_id'], lang, url])
        assert False
    
    [success_200_schema, error_500_schema] = CreateJsonSchemas()
    
    isValidOrTrue = True
    if (response.status_code == 200):
        isValidOrTrue = ValidateJson(data, success_200_schema)
    elif (response.status_code == 500):
        isValidOrTrue = ValidateJson(data, error_500_schema)
    
    if isValidOrTrue != True:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"{isValidOrTrue}", pair['wizard_id'], pair['recipe_id'], lang, url])
        assert False
    
    if response.status_code == 200:
        noOfPersonsDefault = None
        noOfPersonsMin = None
        noOfPersonsMax = None
        if "noOfPersonsDefault" in data:
            noOfPersonsDefault = int(data["noOfPersonsDefault"])
        else:
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"noOfPersonsDefault missing", pair['wizard_id'], pair['recipe_id'], lang, url])
            assert False

        if "noOfPersonsMin" in data:
            noOfPersonsMin = int(data["noOfPersonsMin"])
        else:
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"noOfPersonsMin missing", pair['wizard_id'], pair['recipe_id'], lang, url])
            assert False

        if "noOfPersonsMax" in data:
            noOfPersonsMax = int(data["noOfPersonsMax"])
        else:
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"noOfPersonsMax missing", pair['wizard_id'], pair['recipe_id'], lang, url])
            assert False

        if noOfPersonsMin <= noOfPersonsDefault and noOfPersonsMax >= noOfPersonsDefault:
            pass
        else:
            pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"noOfPersonsDefault[{noOfPersonsDefault}] is not within noOfPersonsMin[{noOfPersonsMin}],noOfPersonsMax[{noOfPersonsMax}] values", pair['wizard_id'], pair['recipe_id'], lang, url])
            assert False

        post_request_payload = {
            "wizard_id": pair['wizard_id'],
            "recipe_id": pair['recipe_id'],
            "level": "Normal",
            "noOfPersonsMin": noOfPersonsMin,
            "noOfPersonsMax": noOfPersonsMax
        }

        recipeId_wizardId_post_request_payload_list.append(post_request_payload)
        SaveToSharedDataDirectory("recipeId_wizardId_post_request_payload_list.json", recipeId_wizardId_post_request_payload_list)
    elif response.status_code == 500:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"errorMessage: {data['errorMessage']}, errorId: {data['errorId']}", pair['recipe_id'], lang, url])
        assert False
    else:
        pytest.log_objects[__name__].writeToLogFileAsList([str(datetime.datetime.now()), f"Unhandled response with status code: {response.status_code}", pair['recipe_id'], lang, url])
        assert False

def CreateJsonSchemas():
    file_path = os.path.realpath(__file__)
    success_200_schema = CreateJsonSchema(
        "GET SUCCESS 200", 
        "...",
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
