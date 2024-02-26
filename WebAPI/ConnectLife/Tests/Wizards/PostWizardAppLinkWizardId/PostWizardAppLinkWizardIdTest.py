import os, datetime, pytest, json

from Common.APIHelpers import SendRequest
from Common.JsonHelpers import AssertValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import CreateJsonSchema

from base_jsonschema_error_respose import base_jsonschema_error_response

import pytest

@pytest.mark.prod
def test_post_wizard_app_link_wizard_id(token: str, params: dict):
    url = "https://api.connectlife.io/api/v1/wizard/app-link/" + params["wizardid"]
    filePath = os.path.realpath(__file__)
    
    print("\nTesting " + url)
    [successSchema, errorSchema] = CreateJsonSchemas()

    payload = json.dumps(params["payload"])
    headers = {
        'Authorization': 'Bearer ' + token + '',
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json"
    }
    timeBeforeRequest = datetime.datetime.now()
    response = SendRequest("POST", url, headers, payload, 10)
    responseInSeconds = (datetime.datetime.now() - timeBeforeRequest).total_seconds()
    
    print("Request/response time: " + str(responseInSeconds) + " seconds")
    print("Response status code: " + str(response.status_code))
    
    assert response.status_code in [200, 400, 500], "Unknown response status code" + str(response.status_code)

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex
    
    assert len(data) > 0, "Missing data"
    WriteDataToJsonFileInCurrentDirectory("_response_" + str(response.status_code), filePath, response.json())
    
    if (response.status_code == 200):
        print("Number of returned objects: ", len(data))
        AssertValidateJson(data, successSchema)
    elif (response.status_code == 500 or response.status_code == 400):
        AssertValidateJson(data, errorSchema)

def CreateJsonSchemas():
    filePath = os.path.realpath(__file__)
    success200Schema = CreateJsonSchema(
        "GET response schema for /api/v1/wizard/app-link/{wizardid} requests: SUCCESS 200", 
        "Wizard response schema", 
        {
            "url": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success", filePath, success200Schema)

    err500Schema = CreateJsonSchema(
        "GET response schema for /api/v1/wizard/app-link/{wizardid} requests: ERROR 500", 
        "Wizard response schema", 
        base_jsonschema_error_response
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error", filePath, err500Schema)
    
    return [success200Schema, err500Schema]
