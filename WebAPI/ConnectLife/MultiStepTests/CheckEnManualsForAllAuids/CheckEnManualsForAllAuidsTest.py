import json, requests, pytest

from Common.JsonHelpers import AssertValidateJson
from JsonSchemas import createSuccessSchema

@pytest.mark.multiStepTest
def test_check_en_manuals_for_all_auids(token: str, params: dict):
    url = "https://api.connectlife.io/api/v1/manuals/" + ";".join(params["auids"]) + "/" + params["lang"]
    
    print("\nTesting " + url)
    
    successSchema = createSuccessSchema()

    payload = {}
    headers = { 'Authorization': 'Bearer ' + token + '' }
    
    response = requests.request("GET", url, headers=headers, data=payload, timeout=100)
    
    print("Response status code: " + str(response.status_code))
    
    assert response.status_code in [200], "Unknown response status code" + str(response.status_code)

    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex
    
    assert len(data) > 0, "Missing data"
    
    if (response.status_code == 200):
        print("Number of returned objects: ", len(data))
        AssertValidateJson(data, successSchema)
