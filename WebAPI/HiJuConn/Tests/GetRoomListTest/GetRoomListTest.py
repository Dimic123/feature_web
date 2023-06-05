import requests
import json
import pprint
import logging

from Common.Logging import PrettyPrint
from WebAPI.HiJuConn.Common.Helpers import GenerateSystemParameters


def test_get_appliance_property(token: str, params: dict):
    url = "https://clife-eu-gateway.hijuconn.com/lgs/get_room_list"
 
    print("Testing " + url)

    data = {"roomType": "0"}

    payload = GenerateSystemParameters(data, token)

    url += "?"
    for key, value in payload.items():
        url += key + "=" + value + "&"

    url = url[:-1]

    response = requests.request("GET", url, timeout=10)

    try:
        data = json.loads(response.text)
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex

    assert "response" in data, "Malformed data: " + response.text

    assert len(data) > 0, "Missing data"

    PrettyPrint(data)
    
    assert all(k in data["response"] for k in ["resultCode", "roomList"]), "Data structure is incorrect"


