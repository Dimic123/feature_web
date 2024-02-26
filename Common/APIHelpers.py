import requests

def SendRequest(reqType, url, headers, payload, timeout: int):
    return requests.request(reqType, url, headers=headers, data=payload, timeout=timeout)
