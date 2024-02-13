import requests
import json

from WebAPI.HiJuConn.Common.Helpers import GenerateSystemParameters


def AuthAPI(username: str, password: str):
    response = Login(username, password, )
    token = GetToken(response)

    return token


def Login(username: str, password: str):
    if username is None or password is None:
        return None

    url = "https://auth-gateway.hijuconn.com/account/acc/login_pwd"

    loginData = {
        "loginName": username,
        "password": password
    }

    payload = json.dumps(GenerateSystemParameters(loginData, "", True, "POST"))
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)

    return data


def GetToken(response):
    if response is not None:
        if "response" in response:
            if "accessToken" in response["response"]:
                return response["response"]["accessToken"]

    return None
