import os, datetime, json

from Common.APIHelpers import SendRequest
from Common.JsonHelpers import AssertValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema, IsArray

from WebAPI.ConnectLife.Tests.Recipe.base_jsonschema_items import base_jsonschema_items
from WebAPI.ConnectLife.Tests.Recipe.base_jsonschema_error_response import base_jsonschema_error_response
from WebAPI.ConnectLife.Tests.Recipe.base_jsonschema_other_status_code_response import base_jsonschema_other_status_code_response
import pytest

@pytest.mark.prod
def test_get_recipes_id_lang(token: str, params: dict):
    url = "https://api.connectlife.io/api/v1/recipes/" + str(params["id"]) + "/" + params["lang"]
    
    filePath = os.path.realpath(__file__)
    
    print("\nTesting " + url)
    [errorSchema, otherStatusCodesSchema] = CreateJsonSchemas()

    payload = {}
    headers = { 'Authorization': 'Bearer ' + token + '' }
    
    timeBeforeRequest = datetime.datetime.now()
    response = SendRequest("GET", url, headers, payload, 300)
    responseInSeconds = (datetime.datetime.now() - timeBeforeRequest).total_seconds()
    
    print("Request/response time: " + str(responseInSeconds) + " seconds")
    print("Response status code: " + str(response.status_code))
    
    assert response.status_code in [200, 404, 500], "Unknown response status code" + str(response.status_code)

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex
    
    assert len(data) > 0, "Missing data"
    WriteDataToJsonFileInCurrentDirectory("_response_" + str(response.status_code), filePath, response.json())
    
    if (response.status_code == 200):
        print("Number of returned objects: ", len(data))
        successSchema = createSuccessSchema(IsArray(data))
        AssertValidateJson(data, successSchema)
    elif (response.status_code == 500):
        AssertValidateJson(data, errorSchema)
    elif (response.status_code == 404):
        AssertValidateJson(data, otherStatusCodesSchema)

def CreateJsonSchemas():
    filePath = os.path.realpath(__file__)
    err500Schema = CreateJsonSchema(
        "GET response schema for /api/v1/recipes/{id}/{lang} request: ERROR 500", 
        "Recipe response schema",
        base_jsonschema_error_response
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error", filePath, err500Schema)
    
    otherStatusCodesSchema = CreateJsonSchema(
        "GET response schema for /api/v1/recipes/{id}/{lang} request: ERROR 404", 
        "Recipe response schema",
        base_jsonschema_other_status_code_response
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_404", filePath, otherStatusCodesSchema)
    
    return [err500Schema, otherStatusCodesSchema]

def createSuccessSchema(isArray: bool):
    filePath = os.path.realpath(__file__)
    
    schema = [base_jsonschema_items] if isArray else base_jsonschema_items
    
    success200Schema = CreateJsonSchema(
        "GET response schema for /api/v1/recipes/{id}/{lang} request: SUCCESS 200", 
        "Recipe response schema",
        schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success", filePath, success200Schema)
    
    return success200Schema