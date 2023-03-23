import requests

def GetAppliances(token: str):
  url = "https://api.connectlife.io/api/v1/appliance"

  payload={}
  headers = {
    'Authorization': 'Bearer '+token+''
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  print(response.text)
