import requests
import json
import pprint
import logging

from Common.Logging import PrettyPrint
from WebAPI.HiJuConn.Common.Helpers import GenerateSystemParameters


def test_get_appliance_property(token: str, params: dict):
    url = "https://asko-eu-gateway.hijuconn.com/wm-web/get_appliance_with_owner"

    print("\nTesting " + url)

    data = {}

    payload = GenerateSystemParameters(data, token, requestType="GET")

    response = requests.request("GET", url, params=payload, timeout=10)

    try:
        data = json.loads(response.text)
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex

    assert "response" in data, "Malformed data: " + response.text

    assert len(data) > 0, "Missing data"

    PrettyPrint(data)

    assert all(k in data["response"] for k in [
               "resultCode", "clApplianceList"]), "Data structure is incorrect"
