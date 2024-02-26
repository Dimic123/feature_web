import os, datetime, json

from Common.APIHelpers import SendRequest
from Common.JsonHelpers import AssertValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema

from base_jsonschema_items import base_jsonschema_items
from base_jsonschema_error_response import base_jsonschema_error_response
import pytest

@pytest.mark.prod
def test_get_recipes_paged_detail_lang(token: str, params: dict):
    url = "https://api.connectlife.io/api/v1/recipes/paged/detail/" + params["lang"] + "?" + ("page=" + str(params["page"]) + "&" if params["page"] != "" else "") + ("pageSize=" + str(params["pageSize"]) if params["pageSize"] != "" else "")
    
    filePath = os.path.realpath(__file__)
    
    print("\nTesting " + url)
    [successSchema, errorSchema] = CreateJsonSchemas()

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
        if "auids" in params:
            print("Number of auid's requested: ", len(params["auids"]))
        print("Number of returned objects: ", len(data))
        AssertValidateJson(data, successSchema)
    elif (response.status_code == 500):
        AssertValidateJson(data, errorSchema)

def CreateJsonSchemas():
    filePath = os.path.realpath(__file__)
    success200Schema = CreateJsonSchema(
        "GET response schema for /api/v1/recipes/paged/{lang}/page/pageSize request: SUCCESS 200", 
        "Recipe response schema", 
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
                    "isTemplated": "boolean",   
                }
            ],
            "items": [
                base_jsonschema_items
            ]
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success", filePath, success200Schema)

    err500Schema = CreateJsonSchema(
        "GET response schema for /api/v1/recipes/paged/{lang}/page/pageSize request: ERROR 500", 
        "Recipe response schema",
        base_jsonschema_error_response
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error", filePath, err500Schema)
    
    return [success200Schema, err500Schema]
