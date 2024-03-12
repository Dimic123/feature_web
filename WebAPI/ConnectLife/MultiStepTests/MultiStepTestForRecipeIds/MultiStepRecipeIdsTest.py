import pytest, requests, json, os, sys

projectRootPath = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-4])
sys.path.append(projectRootPath)

from base_jsonschema_success import base_jsonschema_success
from Common.JsonSchemaHelpers import CreateJsonSchema, IsArray
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from JsonSchemas import CreateValidationSchemas
from Common.JsonHelpers import ValidateJson
from Common.CsvLogWriter.CsvLogWriter import CsvLogWriter
from WebAPI.ConnectLife.Common.MultiStepHelpers import get_list_of_wizard_ids_for_specific_types_and_param_name
from WebAPI.ConnectLife.Common.MultiStepHelpers import getDataFromResponse

SUCCESS_STEP_1_SCHEMA = None
SUCCESS_STEP_3_SCHEMA = None
ERR_400_SCHEMA = None
ERR_404_SCHEMA = None
ERR_500_SCHEMA = None

@pytest.mark.multiStepTest
def test_multistep_recipe_ids(token: str, connectivityGroupsWithAuids: dict[str, list[str]]):
    folder_path = os.path.dirname(os.path.realpath(__file__))

    [step_1_success_schema, step_3_success_schema, err404Schema, err500Schema, err400Schema] = CreateValidationSchemas()
    setGlobalSchemas(step_1_success_schema, step_3_success_schema, err404Schema, err500Schema, err400Schema)

    print("step 1")
    step_1_writer = CsvLogWriter(os.path.join(folder_path, "step_1_logs.txt"))
    step_1_writer.addHeaderAsList(["error", "connectivity_group", "sap_id", "endpoint"])
    wizardIdsAndRecipeIdsDictionary = step_1(connectivityGroupsWithAuids, token, step_1_writer)
    step_1_writer.writeToLogFile()
    
    print("step 2")
    step_2_writer = CsvLogWriter(os.path.join(folder_path, "step_2_logs.txt"))
    step_2_writer.addHeaderAsList(["error", "wizard_id", "recipe_id", "endpoint"])
    allWizardIdRecipeIdsCombinationsDict = step_2(wizardIdsAndRecipeIdsDictionary, token, step_2_writer)
    step_2_writer.writeToLogFile()
    
    print("step 3")
    step_3_writer = CsvLogWriter(os.path.join(folder_path, "step_3_logs.txt"))
    step_3_writer.addHeaderAsList(["error", "wizard_id", "payload.recipeId", "payload.level", "payload.servings", "endpoint"])
    step_3(allWizardIdRecipeIdsCombinationsDict, token, step_3_writer)
    step_3_writer.writeToLogFile()
  
def getPersonsParameterValues(responseObj):
    return [int(responseObj["noOfPersonsDefault"]), int(responseObj["noOfPersonsMin"]), int(responseObj["noOfPersonsMax"])]

def create_step_2_success_schema(isArray: bool):
    filePath = os.path.realpath(__file__)
    
    schema = [base_jsonschema_success] if isArray else base_jsonschema_success
    
    success200Schema = CreateJsonSchema(
        "GET response schema for /api/v1/recipes/{id}/{lang} request: SUCCESS 200", 
        "Recipe response schema",
        schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_step_2_success", filePath, success200Schema)
    
    return success200Schema

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

def setGlobalSchemas(step_1_success_schema, step_3_success_schema, err404Schema, err500Schema, err400Schema):
    global ERR_400_SCHEMA
    global ERR_404_SCHEMA
    global ERR_500_SCHEMA    
    global SUCCESS_STEP_1_SCHEMA
    global SUCCESS_STEP_3_SCHEMA
    
    ERR_400_SCHEMA = err400Schema
    ERR_404_SCHEMA = err404Schema
    ERR_500_SCHEMA = err500Schema
    SUCCESS_STEP_1_SCHEMA = step_1_success_schema
    SUCCESS_STEP_3_SCHEMA = step_3_success_schema

def step_1(connectivity_groups, token, csvLogWriter):
    wizardIdsAndRecipeIdsDictionary = {}
    
    num_of_auids = sum(len(connectivity_groups[grp]) for grp in connectivity_groups)
            
    iteration = 0
    for group in connectivity_groups:
        for auid in connectivity_groups[group]:
            iteration += 1
            url = "https://api.connectlife.io/api/v1/wizard/" + auid
            print(f"GET: {url} [{iteration}/{num_of_auids}]")
            response = requests.request("GET", url, headers={'Authorization': 'Bearer ' + token + ''}, data={}, timeout=100)

            if not response.status_code in [200, 404, 500]:
                csvLogWriter.add(["Unhandled response [not 200, 404, 500]", f"{group}", f"{auid}", f"{url}"])
                continue
            
            data = getDataFromResponse(response)
            global SUCCESS_STEP_1_SCHEMA
            isValid = isResponseDataValid(response.status_code, data, SUCCESS_STEP_1_SCHEMA)

            if isValid != True:
                csvLogWriter.add([f"{isValid}", f"{group}", f"{auid}", f"{url}"])
                continue
            
            if response.status_code == 200:
                wizardIdAndRecipesIdsDict = get_list_of_wizard_ids_for_specific_types_and_param_name(data, ["Recipe"], "recipeId", csvLogWriter, group, auid, url)
                if wizardIdAndRecipesIdsDict == []:
                    continue
                
                for item in wizardIdAndRecipesIdsDict:
                    wizardIdsAndRecipeIdsDictionary.update(item)
                print("OK")
            else:
                csvLogWriter.add([f"response status code: {response.status_code}", f"{group}", f"{auid}", f"{url}"])

    csvLogWriter.writeToLogFile()
    return wizardIdsAndRecipeIdsDictionary

def step_2(wizardIdsAndRecipeIdsDictionary, token, csvLogWriter):    
    allWizardIdRecipeIdsCombinationsDict = {}
    total_iterations = sum(len(wizardIdsAndRecipeIdsDictionary[wizardId]) for wizardId in wizardIdsAndRecipeIdsDictionary)
    
    iteration = 0
    
    for wizardid in wizardIdsAndRecipeIdsDictionary:
        allWizardIdRecipeIdsCombinationsDict[wizardid] = []
        for recipeId in wizardIdsAndRecipeIdsDictionary[wizardid]:
            iteration += 1
            url = "https://api.connectlife.io/api/v1/recipes/" + recipeId + "/en"
            print(f"GET: {url} [{iteration}/{total_iterations}]")
            response = requests.request("GET", url, headers={'Authorization': 'Bearer ' + token + ''}, data={}, timeout=100)
            
            if not response.status_code in [200, 404, 500]:
                csvLogWriter.add(["Unhandled response [not 200, 404, 500]", f"{wizardid}", f"{recipeId}", f"{url}"])
                continue
            
            data = getDataFromResponse(response)
            isValid = isResponseDataValid(response.status_code, data, create_step_2_success_schema(IsArray(data)))

            if isValid != True:
                csvLogWriter.add([f"{isValid}", f"{wizardid}", f"{recipeId}", f"{url}"])
                continue
            
            if response.status_code == 200:
                [default, min, max] = getPersonsParameterValues(data)
                if min <= default <= max and min > 0 and max > 0 and default > 0:
                    allWizardIdRecipeIdsCombinationsDict[wizardid].append({
                        "min": min,
                        "max": max,
                        "recipeId": recipeId
                    })
                    print("OK")
                else:
                    error_reason = f"noOfPersonsDefault is not within range [noOfPersonsMin, noOfPersonsMax]"
                    csvLogWriter.add([f"{error_reason}", f"{wizardid}", f"{recipeId}", f"{url}"])
            elif response.status_code == 404:
                csvLogWriter.add([f"{data["title"]}", f"{wizardid}", f"{recipeId}", f"{url}"])
            elif response.status_code == 500:                
                error_reason = data["errorMessage"] if data["errorMessage"] else f"error {str(response.status_code)}"
                csvLogWriter.add([f"{error_reason}", f"{wizardid}", f"{recipeId}", f"{url}"])
                
    csvLogWriter.writeToLogFile()
    return allWizardIdRecipeIdsCombinationsDict

def step_3(allWizardIdRecipeIdsCombinationsDict, token, csvLogWriter):    
    total_iterations = 0
    
    for wizardid in allWizardIdRecipeIdsCombinationsDict:
        for obj in allWizardIdRecipeIdsCombinationsDict[wizardid]:
            total_iterations += (int(obj["max"]) - int(obj["min"])) + 1
    
    iteration = 0
    
    for wizardid in allWizardIdRecipeIdsCombinationsDict:
        url = "https://api.connectlife.io/api/v1/wizard/recipe/" + wizardid
        for obj in allWizardIdRecipeIdsCombinationsDict[wizardid]:
            payload = { "recipeId": obj["recipeId"], "level": "Normal", "servings": 2 }
            for i in range(obj["min"], obj["max"] + 1):
                iteration += 1
                payload["servings"] = i
                print(f"POST: {url} [{iteration}/{total_iterations}], {payload}")
                response = requests.request("POST", url, headers={
                        'Authorization': 'Bearer ' + token + '',
                        "Content-Type": "application/json; charset=utf-8",
                        "Accept": "application/json"
                    }, data=json.dumps(payload), timeout=100)
                
                if not response.status_code in [200, 404, 500]:
                    csvLogWriter.add([f"Unhandled response [not 200, 404, 500]", f"{wizardid}", f"{payload["recipeId"]}", f"{payload["level"]}", f"{payload["servings"]}", f"{url}"])
                    continue
                
                data = getDataFromResponse(response)
                global SUCCESS_STEP_3_SCHEMA
                isValid = isResponseDataValid(response.status_code, data, SUCCESS_STEP_3_SCHEMA)

                if isValid != True:
                    csvLogWriter.add([f"{isValid}", f"{wizardid}", f"{payload["recipeId"]}", f"{payload["level"]}", f"{payload["servings"]}", f"{url}"])
                    continue
                
                if response.status_code == 200:
                    print("OK")
                elif response.status_code == 404:
                    csvLogWriter.add([f"{data["errorMessage"]}", f"{wizardid}", f"{payload["recipeId"]}", f"{payload["level"]}", f"{payload["servings"]}", f"{url}"])
                elif response.status_code == 500:
                    csvLogWriter.add([f"{data["errorMessage"]}", f"{wizardid}", f"{payload["recipeId"]}", f"{payload["level"]}", f"{payload["servings"]}", f"{url}"])
                    
    csvLogWriter.writeToLogFile()
    