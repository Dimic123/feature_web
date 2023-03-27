import requests
import json


def GetAppliances(token: str) -> bool:
    url = "https://api.connectlife.io/api/v1/appliance"

    payload = {}
    headers = {
        'Authorization': 'Bearer '+token+''
    }

    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=10)
    except requests.ReadTimeout:
        print("ERROR - request timeout")
        return False

    try:
        data = json.loads(response.text)
    except:
        print("ERROR - malformed data")
        return False

    if "errorMessage" in data:
        print("ERROR - API call returned error")
        return False

    if len(data) > 0:
        if all(k in ["id", "name", "type", "status"] for k in data[0]):
            print("PASSED - data seems to be formed correctly")
            return True
        else:
            print("ERROR - data structure seems to not be correct")
            return False
    else:
        print("ERROR - missing data")
        return False
