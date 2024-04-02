import requests, json
from Configuration.Settings import *


def AuthAPI(username: str, password: str, client_id: str, client_secret: str):
    loginData = LoginAPI(username, password, client_id)
    if "code" in loginData:
        tokenData = GetToken(loginData["code"], client_id, client_secret)
        if tokenData is None:
            return None
    else:
        return None

    return tokenData["access_token"]


def LoginAPI(username: str, password: str, client_id: str):
    if username is None or password is None or client_id is None:
        return None

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

    payload = 'grant_type=authorization_code&code='+code+'&client_id='+client_id+'&client_secret=' + \
        client_secret+'&redirect_uri=https%3A%2F%2Fapi.connectlife.io%2Fswagger%2Foauth2-redirect.html'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)

    return data


class OAuth2Authorization:
    __token_cookie_value = None
    __token = None
    __uid = None
    __id_token = None
    __code = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def GetCDCUserDetailsRequest(env = "PROD"):
        payload = {
            "loginID": Settings.get(f"{env}_Username"),
            "password": Settings.get(f"{env}_Password"),
            "APIKey": Settings.get(f"{env}_ApiKey"),
            "gmid": Settings.get(f"{env}_GmId")
        }
        
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        
        url = "https://accounts.eu1.gigya.com/accounts.login"
        response = requests.request("POST", url, headers=headers, data=payload)
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
        
        if "errorDetails" in data:
            print(f"ERROR DETAILS {url}")
            print(f"******* {data['errorDetails']}")
            return
        
        if "error_description" in data:
            print(f"ERROR DESCRIPTION {url}")
            print(f"******* {data['error_description']}")
            return
        
        if "sessionInfo" in data:
            if "cookieValue" in data["sessionInfo"]:
                OAuth2Authorization.__token_cookie_value = data["sessionInfo"]["cookieValue"]  
        if "UID" in data:
           OAuth2Authorization.__uid = data["UID"]

        if OAuth2Authorization.__token_cookie_value == None or OAuth2Authorization.__uid == None:
            print("ERROR - token cookie value or uid was not retrieved")
        # else:
        #     print("GetCDCUserDetailsRequest OK")
    
    @staticmethod
    def GetTokenIdRequest(env = "PROD"):
        if OAuth2Authorization.__token_cookie_value == None:
            return
        
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        
        payload = {
            "APIKey": Settings.get(f"{env}_ApiKey"),
            "gmid": Settings.get(f"{env}_GmId"),
            "login_token": OAuth2Authorization.__token_cookie_value
        }
        
        url = "https://accounts.eu1.gigya.com/accounts.getJWT"
        response = requests.request("POST", url, headers=headers, data=payload)
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
        
        if "error_description" in data:
            print(f"ERROR DESCRIPTION {url}")
            print(f"******* {data['error_description']}")
            return
        
        if "id_token" in data:
            OAuth2Authorization.__id_token = data["id_token"]
            
        if OAuth2Authorization.__id_token == None:
            print("ERROR - id_token was not retrieved")
        # else:
        #     print("GetTokenIdRequest OK")
        
    @staticmethod
    def GetCodeRequest(env = "PROD"):
        if OAuth2Authorization.__id_token == None:
            return
        
        payload = json.dumps({
            "client_id": Settings.get("ClientId"),
            "idToken": OAuth2Authorization.__id_token,
            "response_type": "code",
            "redirect_uri": "https://api" + ("-test" if env == 'TEST' else '') + ".connectlife.io/swagger/oauth2-redirect.html",
            "thirdType": "CDC",
            "thirdClientId": OAuth2Authorization.__uid
        })
        
        headers = { 'Content-Type': 'application/json' }
        
        url = "https://" + ("test-" if env == 'TEST' else '') + "oauth.hijuconn.com/oauth/authorize"
        response = requests.request("POST", url, headers=headers, data=payload)
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
        
        if "error_description" in data:
            print(f"ERROR DESCRIPTION {url}")
            print(f"******* {data['error_description']}")
            return
        
        if "code" in data:
            OAuth2Authorization.__code = data["code"]
            
        if OAuth2Authorization.__code == None:
            print("ERROR - code was not retrieved")
        # else:
        #     print("GetCodeRequest OK")
            
            
    @staticmethod
    def GetOauthTokenRequest(env = "PROD"):
        if OAuth2Authorization.__code == None:
            return
        
        payload = {
            "client_id": Settings.get("ClientId"),
            "code": OAuth2Authorization.__code,
            "grant_type": "authorization_code",
            "client_secret": Settings.get("ClientSecret"),
            "redirect_uri": "https://api" + ("-test" if env == 'TEST' else '') + ".connectlife.io/swagger/oauth2-redirect.html"
        }
        
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        
        url = "https://" + ("test-" if env == 'TEST' else '') + "oauth.hijuconn.com/oauth/token"
        
        response = requests.request("POST", url, headers=headers, data=payload)
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
        
        if "error_description" in data:
            print(f"ERROR DESCRIPTION {url}")
            print(f"******* {data['error_description']}")
            return
        
        if "access_token" in data:
            OAuth2Authorization.__token = data["access_token"]
            
        if OAuth2Authorization.__token == None:
            print("ERROR - access_token was not retrieved")
        # else:
        #     print("GetOauthTokenRequest OK")
    
    @staticmethod
    def getToken(env = "PROD"):
        OAuth2Authorization.GetCDCUserDetailsRequest(env)
        OAuth2Authorization.GetTokenIdRequest(env)
        OAuth2Authorization.GetCodeRequest(env)
        OAuth2Authorization.GetOauthTokenRequest(env)
        
        return OAuth2Authorization.__token

