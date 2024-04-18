import requests, json

def getHybrisToken() -> str:
    client_id = "connectlifeApi"
    client_secret = "2Va81Ph5WlHL"
    grant_type = "client_credentials"

    url = "https://api.cdrwhdl6-hisenseeu2-p1-public.model-t.cc.commerce.ondemand.com/authorizationserver/oauth/token"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Accept": "application/json",
        "Cookie": "JSESSIONID=C821AA987DB3719B0959BF2B18089B8D.api-658f7665b9-5xpvb; ROUTE=.api-658f7665b9-5xpvb"
    }

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)

    access_token = ""
    if "access_token" in data:
        access_token = data["access_token"]
    return access_token
