import pytest, requests, os, sys

projectRootPath = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-4])
sys.path.append(projectRootPath)

from JsonSchemas import CreateValidationSchemas
from Common.JsonHelpers import ValidateJson
from Common.CsvLogWriter.CsvLogWriter import CsvLogWriter
from WebAPI.ConnectLife.Common.MultiStepHelpers import getDataFromResponse

SUCCESS_SCHEMA = None
ERR_400_SCHEMA = None
ERR_500_SCHEMA = None

@pytest.mark.multiStepTest
def test_multistep_recipe_paged_detail_lang_all(token: str):
    folder_path = os.path.dirname(os.path.realpath(__file__))

    [success_schema, err400Schema, err500Schema] = CreateValidationSchemas()
    setGlobalSchemas(success_schema, err400Schema, err500Schema)
    
    languages = ["bg", "bs", "cs", "da", "de", "de_AT", "en", "en_AU", "en_IN", "fi", "fr", "hr", "hu", "it", "mk", "nl", "no", "pl", "ro", "ru", "sk", "sl", "sr", "sv", "uk"]
    pageSize = 15
    
    csv_writer = CsvLogWriter(os.path.join(folder_path, "error_logs.txt"))
    csv_writer.addHeaderAsList(["error", "language", "page_number", "page_size", "endpoint"])
    
    for lang in languages:
        pageNum = 0
        while True:
            url = "https://api.connectlife.io/api/v1/recipes/paged/detail/" + lang + f"?page={pageNum}" + f"&pageSize={pageSize}"
            print(f"GET: {url}")
            response = requests.request("GET", url, headers={'Authorization': 'Bearer ' + token + ''}, data={}, timeout=100)
            
            if not response.status_code in [200, 404, 500]:
                csv_writer.add([f"Unhandled response {response.status_code}", f"{lang}", f"{pageNum}", f"{pageSize}", f"{url}"])
                pageNum += 1
                continue
            
            data = getDataFromResponse(response)
            isValid = isResponseDataValid(response.status_code, data)
            
            if isValid != True:
                csv_writer.add([f"{isValid}", f"{lang}", f"{pageNum}", f"{pageSize}", f"{url}"])
                pageNum += 1
                continue
            
            if data == {} or data == []:
                csv_writer.add([f"Missing data", f"{lang}", f"{pageNum}", f"{pageSize}", f"{url}"])
            
            if response.status_code == 200:
                if "items" in data.keys():
                    for item in data["items"]:
                        if "noOfPersonsDefault" in item and "noOfPersonsMin" in item and "noOfPersonsMax" in item:
                            default = item["noOfPersonsDefault"]
                            min = item["noOfPersonsMin"]
                            max = item["noOfPersonsMax"]
                            
                            if not (default <= min and max >= default):
                                csv_writer.add([f"noOfPersonsDefault is not within range [noOfPersonsMin, noOfPersonsMax]", f"{lang}", f"{pageNum}", f"{pageSize}", f"{url}"])
                            elif max < min:
                                csv_writer.add([f"noOfPersonsMax < noOfPersonsMin", f"{lang}", f"{pageNum}", f"{pageSize}", f"{url}"])
                            elif min > max:
                                csv_writer.add([f"noOfPersonsMax > noOfPersonsMin", f"{lang}", f"{pageNum}", f"{pageSize}", f"{url}"])
                        else:
                            csv_writer.add([f"Unhandled response {response.status_code}", f"{lang}", f"{pageNum}", f"{pageSize}", f"{url}"])
                else:
                    csv_writer.add([f"Missing items", f"{lang}", f"{pageNum}", f"{pageSize}", f"{url}"])
            else:
                csv_writer.add([f"Response status code: {response.status_code}", f"{lang}", f"{pageNum}", f"{pageSize}", f"{url}"])
            
            if pageNum == data["numPages"] - 1:
                break
            else:
                pageNum += 1
            
    csv_writer.writeToLogFile()
    
    
def isResponseDataValid(statusCode, data, successSchema):
    global ERR_400_SCHEMA
    global ERR_404_SCHEMA
    global ERR_500_SCHEMA
    
    isValid = True
    
    if statusCode == 200:
        isValid = ValidateJson(data, successSchema)
    elif statusCode == 400:
        isValid = ValidateJson(data, ERR_400_SCHEMA)
    elif statusCode == 404:
        isValid = ValidateJson(data, ERR_404_SCHEMA)
    elif statusCode == 500:
        isValid = ValidateJson(data, ERR_500_SCHEMA)

    return isValid

def setGlobalSchemas(success_schema, err400Schema, err500Schema):
    global SUCCESS_SCHEMA
    global ERR_400_SCHEMA
    global ERR_500_SCHEMA
    
    SUCCESS_SCHEMA = success_schema
    ERR_400_SCHEMA = err400Schema
    ERR_500_SCHEMA = err500Schema
    
def isResponseDataValid(statusCode, data):
    global SUCCESS_SCHEMA
    global ERR_400_SCHEMA
    global ERR_500_SCHEMA
    
    isValid = True
    
    if statusCode == 200:
        isValid = ValidateJson(data, SUCCESS_SCHEMA)
    elif statusCode == 400:
        isValid = ValidateJson(data, ERR_400_SCHEMA)
    elif statusCode == 500:
        isValid = ValidateJson(data, ERR_500_SCHEMA)

    return isValid
