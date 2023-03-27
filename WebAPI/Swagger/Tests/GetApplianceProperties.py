import requests
import json


def GetApplianceProperty(token: str, id: str) -> bool:
    url = "https://api.connectlife.io/api/v1/appliance/8650021000100020002000000d2ffa0d0680-0000000000007389860001202100012030002"

    payload = {}
    headers = {
        'Authorization': 'Bearer '+token+''
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
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
        if all(k in ["id", "name", "type", "status", "properties"] for k in data[0]):
            print("PASSED - data seems to be formed correctly")
            return True
        else:
            print("ERROR - data structure seems to not be correct")
            return False
    else:
        print("ERROR - missing data")
        return False
