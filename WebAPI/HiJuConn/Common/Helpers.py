import base64
from random import choice
import datetime
import time
import rsa
import subprocess
from hashlib import sha256

from Configuration.Settings import Settings


def GetTimestamp() -> str:
    now = datetime.datetime.now()
    return str(int(time.mktime(now.timetuple())*1e3 + now.microsecond/1e3))


def GenerateRandStr() -> str:
    characters = ['a', 'b', 'c', 'd', 'e', 'f', '0',
                  '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return ''.join(choice(characters) for i in range(32))


def GenerateSign(data, isLogin: bool = False) -> str:
    sorted_dict = dict(sorted(data.items()))

    sign = ""

    for key, value in sorted_dict.items():
        if value is not None and value != "":
            sign += key + "=" + value + "&"

    sign = sign[:-1]
    sign += "D9519A4B756946F081B7BB5B5E8D1197"

    pubkey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyyWrNG6q475HIHu7sMVuvHof6vlgPeixmxa4EL/UsvVvHPz33NnWoQetQqit9TBNzUjMXw0KlY9PXM4iqHUUU+dSyNDq1jZWIiJ2C2FccppswJtIKL3NRMFvT9PFh6NlP/4FUcQKojgKFbF7KaccJPKYHlwaO7qgoIjLxAHlSOXGpucJcOkPzT2EqsSVnW8sn8kenvNmghXDayhgxsh6AyxK4kehJplEnmX/iYCfNoFXknGcLqFWYccgBz3fybvx30C/0IgU1980L8QsUAv5esZmN8ugnbRgLRxKRlkQQLxQAiZMZdKTAx665YflT3YMHJvEFE8c2XFgoxHzSMc4BwIDAQAB"

    hash = sha256(sign.encode('utf-8'))
    sign = hash.hexdigest()

    key = rsa.PublicKey.load_pkcs1_openssl_der(base64.b64decode(pubkey))
    data = None

    if isLogin:
        data = sign.encode('utf-8')
    else:
        data = bytearray.fromhex(sign)

    sign = rsa.encrypt(data, key)
    sign = base64.b64encode(sign).decode("utf-8")
    sign = sign.replace("+", "-").replace("/", "_")
    return sign


def GenerateSystemParameters(data: dict = None, token: str = None, isLogin: bool = False) -> dict:
    params = {}
    if isLogin:
        params = {
            "appSecret": Settings.get("AppSecret"),
            "appId": Settings.get("AppId"),
            "sourceId": Settings.get("SourceId"),
            "accessToken": "",
            "version": "5.0",
            "timeStamp": GetTimestamp(),
            "languageId": "1",
            "timezone": "1.0",
            "randStr": GenerateRandStr(),
            "srcType": "1"
        }
    else:
        params = {
            "accessToken": token,
            "version": "5.0",
            "timeStamp": GetTimestamp(),
            "languageId": "1",
            "timezone": "1.0",
            "randStr": GenerateRandStr(),
        }

    if data is not None:
        data.update(params)
    else:
        data = params

    data["sign"] = GenerateSign(data, isLogin)

    return data
