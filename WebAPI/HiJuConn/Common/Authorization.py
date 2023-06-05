import requests
import json

from WebAPI.HiJuConn.Common.Helpers import GenerateSystemParameters


def AuthAPI(username: str, password: str):
    response = Login(username, password, )
    token = GetToken(response)
    # token = "pa1u47xnRnfcy7qqsjRweLt3ACThrT2VDNWZOfBKMV_OojBXuPkTqrR3trCAKOnpJoXC8_eGFPO5qZZaPiFTak9hCFce5m7qdEhs2b3uoyOkqrDBkcZV3Ku5ZVBlWbU6ijOCyS9TzbCokvkCiKsvy-xpu1S9OAwFmWXIv4mzFeNoA057c5aUGEEyydOFZRQ_5YHhHwkyIU5CI3Jrlvvzucndy9cdeWBEvxJej-IJluuVtYRElifQeLO4WNbqk8Ak2g1u_qXCA5ZMTMlI9paBlhK6XZnKjO-WwyZbWcIxfgonkrjV29L5QdQ1vJ0O2Kufe8HzutnqEL3dwLv6fMlNpqFWluvMfsfN6rxndwGy89OHHs"

    return token


def Login(username: str, password: str):
    if username is None or password is None:
        return None

    url = "https://auth-gateway.hijuconn.com/account/acc/login_pwd"

    loginData = {
        "loginName": username,
        "password": password
    }

    payload = json.dumps(GenerateSystemParameters(loginData, "", True))
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)

    return data


def GetToken(response):
    if "response" in response:
        if "accessToken" in response.response:
            return response.response.response.accessToken

    return None
