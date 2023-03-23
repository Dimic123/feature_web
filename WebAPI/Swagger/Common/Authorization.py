import requests
import json

def AuthAPI(username: str, password: str, client_id: str, client_secret: str):
    loginData = LoginAPI(username, password, client_id)
    tokenData = GetToken(loginData["code"], client_id, client_secret)

    return tokenData["access_token"]

def LoginAPI(username: str, password: str, client_id: str):
    url = "https://oauth.hijuconn.com/oauth/authorize"

    payload = json.dumps({
    "username": username,
    "password": password,
    "state": "VHVlIE1hciAyMSAyMDIzIDE1OjE5OjE3IEdNVCswMTAwIChDZW50cmFsIEV1cm9wZWFuIFN0YW5kYXJkIFRpbWUp",
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": "https://api.connectlife.io/swagger/oauth2-redirect.html"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)

    return data

def GetToken(code: str, client_id: str, client_secret: str):
    url = "https://oauth-gateway.hijuconn.com/oauth/token"

    payload='grant_type=authorization_code&code='+code+'&client_id='+client_id+'&client_secret='+client_secret+'&redirect_uri=https%3A%2F%2Fapi.connectlife.io%2Fswagger%2Foauth2-redirect.html'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)

    return data


