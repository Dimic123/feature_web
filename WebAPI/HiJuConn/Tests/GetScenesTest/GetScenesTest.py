import requests
import json

from Common.Logging import PrettyPrint
from WebAPI.HiJuConn.Common.Helpers import GenerateSystemParameters
from Common.JsonHelpers import AssertValidateJson

from ResponseSchema import schema

def test_get_appliance_property(token: str, params: dict):
    url = "https://clife-eu-gateway.hijuconn.com/scene/get_scenes"

    print("\nTesting " + url)
    
    data = {
        "packageName": params["packageName"],
        "versionCode":  params["versionCode"],
    }

    payload = GenerateSystemParameters(data, token, requestType="GET")
    response = requests.request("GET", url, params=payload, timeout=10)
    
    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex

    assert "response" in data, "Malformed data: " + response.text
    assert len(data) > 0, "Missing data"
    AssertValidateJson(data["response"], schema)
    PrettyPrint(data)
