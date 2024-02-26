import datetime, json, pytest

from Common.APIHelpers import SendRequest
from Common.JsonHelpers import AssertValidateJson
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from Common.JsonSchemaHelpers import IsArray

def HandleTest(url, params, token, callerFilePath):
    print("\nTesting " + url)
    [successSchemaArray, successSchemaObj, errorSchema, err404Schema] = pytest.jsonSchemasWashingPrograms

    payload = {}
    headers = { 'Authorization': 'Bearer ' + token + '' }
    
    timeBeforeRequest = datetime.datetime.now()
    response = SendRequest("GET", url, headers, payload, 10)
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
    WriteDataToJsonFileInCurrentDirectory("_response_" + str(response.status_code), callerFilePath, response.json())
    
    if (response.status_code == 200):
        if IsArray(data):
            print("Number of returned objects: ", len(data))
            AssertValidateJson(data, successSchemaArray)
        else:
            print("Number of returned objects: 1")
            AssertValidateJson(data, successSchemaObj)
    elif (response.status_code == 500):
        AssertValidateJson(data, errorSchema)
    elif response.status_code == 404:
        AssertValidateJson(data, err404Schema)
