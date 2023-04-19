import requests
import json

from Common.Logging import PrettyPrint


def test_get_appliances(token: str, params: dict):
    url = "https://api.connectlife.io/api/v1/appliance"

    payload = {}
    headers = {
        'Authorization': 'Bearer '+token+''
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=10)

    try:
        data = json.loads(response.text)
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex

    assert "errorMessage" not in data, "API call returned error"

    assert len(data) > 0, "Missing data"

    assert all(k in ["id", "name", "type", "status"] for k in data[0]), "Data structure seems to not be correct"

    PrettyPrint(data)

