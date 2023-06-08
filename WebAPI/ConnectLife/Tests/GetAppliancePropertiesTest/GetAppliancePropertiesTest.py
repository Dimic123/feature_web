import requests
import json
import pprint

from Common.Logging import PrettyPrint


def test_get_appliance_property(token: str, params: dict):
    url = "https://api.connectlife.io/api/v1/appliance/" + params["id"]

    print("Testing " + url)

    payload = {}
    headers = {
        'Authorization': 'Bearer '+token+''
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, timeout=10)

    try:
        data = json.loads(response.text)
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex

    assert "errorMessage" not in data, "API call returned error"

    assert len(data) > 0, "Missing data"

    PrettyPrint(data)

    assert all(k in ["id", "name", "type", "status", "properties"]
               for k in data[0]), "Data structure is incorrect"
