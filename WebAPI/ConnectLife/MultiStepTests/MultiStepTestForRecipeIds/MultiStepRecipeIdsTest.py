import pytest, requests, json, os, sys

projectRootPath = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-4])
sys.path.append(projectRootPath)

from base_jsonschema_success import base_jsonschema_success
from Common.JsonSchemaHelpers import CreateJsonSchema, IsArray
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory
from JsonSchemas import create_different_schemas
from Common.JsonHelpers import ValidateJson
from Common.CsvLogWriter.CsvLogWriter import CsvLogWriter

@pytest.mark.multiStepTest
def test_multistep_recipe_ids(token: str, connectivityGroupsWithAuids: dict[str, list[str]]):
    folder_path = os.path.dirname(os.path.realpath(__file__))
    auids_array = []
    
    for connectivityGroup in connectivityGroupsWithAuids:
        if connectivityGroupsWithAuids[connectivityGroup] != []:
            for auid in connectivityGroupsWithAuids[connectivityGroup]:
                auids_array.append([auid])

    [step_1_success_schema, step_3_success_schema, err404Schema, err500Schema] = create_different_schemas()

    print("step 1")
    step_1_writer = CsvLogWriter(os.path.join(folder_path, "step_1_logs.txt"))
    step_1_writer.addHeaderAsList(["error", "connectivity_group", "sap_id", "endpoint"])
    wizardIdsAndRecipeIdsDictionary = step_1(connectivityGroupsWithAuids, step_1_success_schema, err404Schema, err500Schema, token, step_1_writer)
    # connectivityGroupsWithAuids = {"conn_group": ["auids"]}
    # returns wizardIdsAndRecipeIdsDictionary =  [{"wizard_id": ["recipe_ids"], "sap_ids": ["sap_id"]}]
    step_1_writer.writeToLogFile()
    
    print("step 2")
    step_2_writer = CsvLogWriter(os.path.join(folder_path, "step_2_logs.txt"))
    step_2_writer.addHeaderAsList(["error", "wizard_id", "recipe_id", "endpoint"])
    allWizardIdRecipeIdsCombinationsDict = step_2(wizardIdsAndRecipeIdsDictionary, err404Schema, err500Schema, token, step_2_writer)
    # wizardIdsAndRecipeIdsDictionary =  [{"wizard_id": ["recipe_ids"]}]
    # allWizardIdRecipeIdsCombinationsDict = [{"wizard_id": {"min", "max", "recipeId"}}]
    step_2_writer.writeToLogFile()
    
    print("step 3")
    step_3_writer = CsvLogWriter(os.path.join(folder_path, "step_3_logs.txt"))
    step_3_writer.addHeaderAsList(["error", "wizard_id", "payload.recipeId", "payload.level", "payload.servings", "endpoint"])
    step_3(allWizardIdRecipeIdsCombinationsDict, step_3_success_schema, err404Schema, err500Schema, token, step_3_writer)
    step_3_writer.writeToLogFile()

def createDictionaryOfWizardidAndRecipeIds(group, auid, responseObj, type, paramName, csvLogWriter, url) -> dict:
    objects = []
    
    if responseObj == []:
        csvLogWriter.add(["Empty response", f"{group}", f"{auid}", f"{url}"])
        return objects
    
    for item in responseObj:
        skip = False
        itemObj = {}
        if "type" in item and item["type"] == type:
            itemId = ""
            if "id" in item and item["id"] != "":
                itemId = item["id"]
            else:
                csvLogWriter.add(["Missing property: 'wizardid'", f"{group}", f"{auid}", f"{url}"])
                continue
            
            if "parameters" in item and len(item["parameters"]) > 0:
                if len(item["parameters"]) > 0:
                    paramNameExists = False
                    for param in item["parameters"]:
                        if param["name"] == paramName:
                            paramNameExists = True
                            if "possibleValues" in param and len(param["possibleValues"]) > 0:
                                itemObj[itemId] = param["possibleValues"]
                            else:
                                csvLogWriter.add(["'possibleValues' are empty", f"{group}", f"{auid}", f"{url}"])
                                skip = True
                                break
                    if skip: continue
                    if not paramNameExists:
                        csvLogWriter.add([f"tname == {paramName} doesn't exist", f"{group}", f"{auid}", f"{url}"])
                        continue
                else:
                    csvLogWriter.add([f"'parameters' property has empty value", f"{group}", f"{auid}", f"{url}"])
                    continue
            elif "parameters" in item and len(item["parameters"]) <= 0:
                csvLogWriter.add([f"Value for property 'parameters' is empty {paramName}", f"{group}", f"{auid}", f"{url}"])
                continue
            else:
                csvLogWriter.add([f"Property 'parameters' doesn't exist {paramName}", f"{group}", f"{auid}", f"{url}"])
                continue
        elif "type" in item and item["type"] != type:
            print("** SKIP type: " + str(item["type"]) + " for [group: " + str(group) + ", auid: " + str(auid) + "] because type is not " + type)
            pass
        else:
            csvLogWriter.add([f"Property 'type' is missing", f"{group}", f"{auid}", f"{url}"])
        objects.append(itemObj)
    return objects

def getDataFromResponse(response):
    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
        return data
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex
    
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

def step_1(connectivity_groups, step_1_success_schema, err404Schema, err500Schema, token, csvLogWriter):
    wizardIdsAndRecipeIdsDictionary = {}
    
    num_of_auids = sum(len(connectivity_groups[grp]) for grp in connectivity_groups)
            
    iteration = 0
    for group in connectivity_groups:
        for auid in connectivity_groups[group]:
            iteration += 1
            url = "https://api.connectlife.io/api/v1/wizard/" + auid
            print(f"GET: {url} [{iteration}/{num_of_auids}]")
            getRecipeIdsResponse = requests.request("GET", url, headers={'Authorization': 'Bearer ' + token + ''}, data={}, timeout=100)

            if not getRecipeIdsResponse.status_code in [200, 404, 500]:
                csvLogWriter.add(["Unhandled response [not 200, 404, 500]", f"{group}", f"{auid}", f"{url}"])
                continue
            data = getDataFromResponse(getRecipeIdsResponse)
            isValid = True
            if getRecipeIdsResponse.status_code == 200:
                isValid = ValidateJson(data, step_1_success_schema)
            elif getRecipeIdsResponse.status_code == 404:
                isValid = ValidateJson(data, err404Schema)
            elif getRecipeIdsResponse.status_code == 500:
                isValid = ValidateJson(data, err500Schema)

            if isValid != True:
                csvLogWriter.add([f"{isValid}", f"{group}", f"{auid}", f"{url}"])
                continue
            
            print(data)
            wizardIdAndRecipesIdsDict = createDictionaryOfWizardidAndRecipeIds(group, auid, data, "Recipe", "recipeId", csvLogWriter, url)
            if wizardIdAndRecipesIdsDict == []:
                # no wizardid or recipe ids extracted from response json
                continue
            
            for item in wizardIdAndRecipesIdsDict:
                wizardIdsAndRecipeIdsDictionary.update(item)

    csvLogWriter.writeToLogFile()
    return wizardIdsAndRecipeIdsDictionary

def step_2(wizardIdsAndRecipeIdsDictionary, err404Schema, err500Schema, token, csvLogWriter):    
    allWizardIdRecipeIdsCombinationsDict = {}
    total_iterations = sum(len(wizardIdsAndRecipeIdsDictionary[wizardId]) for wizardId in wizardIdsAndRecipeIdsDictionary)
    
    iteration = 0
    
    for wizardid in wizardIdsAndRecipeIdsDictionary:
        allWizardIdRecipeIdsCombinationsDict[wizardid] = []
        for recipeId in wizardIdsAndRecipeIdsDictionary[wizardid]:
            iteration += 1
            url = "https://api.connectlife.io/api/v1/recipes/" + recipeId + "/en"
            print(f"GET: {url} [{iteration}/{total_iterations}]")
            getRecipeIdDetailsResponse = requests.request("GET", url, headers={'Authorization': 'Bearer ' + token + ''}, data={}, timeout=100)
            
            if not getRecipeIdDetailsResponse.status_code in [200, 404, 500]:
                csvLogWriter.add(["Unhandled response [not 200, 404, 500]", f"{wizardid}", f"{recipeId}", f"{url}"])
                continue
            data = getDataFromResponse(getRecipeIdDetailsResponse)
            
            isValid = True
            if getRecipeIdDetailsResponse.status_code == 200:                
                isValid = ValidateJson(data, create_step_2_success_schema(IsArray(data)))
            elif getRecipeIdDetailsResponse.status_code == 404:
                isValid = ValidateJson(data, err404Schema)
            elif getRecipeIdDetailsResponse.status_code == 500:
                isValid = ValidateJson(data, err500Schema)

            if isValid != True:
                csvLogWriter.add([f"{isValid}", f"{wizardid}", f"{recipeId}", f"{url}"])
                continue
            
            if getRecipeIdDetailsResponse.status_code == 200:
                [default, min, max] = getPersonsParameterValues(data)
                if min <= default <= max and min > 0 and max > 0 and default > 0:
                    allWizardIdRecipeIdsCombinationsDict[wizardid].append({
                        "min": min,
                        "max": max,
                        "recipeId": recipeId
                    })
                else:
                    error_reason = f"noOfPersonsDefault is not within range [noOfPersonsMin, noOfPersonsMax]"
                    csvLogWriter.add([f"{error_reason}", f"{wizardid}", f"{recipeId}", f"{url}"])
            elif getRecipeIdDetailsResponse.status_code == 404:
                csvLogWriter.add([f"{data["title"]}", f"{wizardid}", f"{recipeId}", f"{url}"])
            elif getRecipeIdDetailsResponse.status_code == 500:                
                error_reason = data["errorMessage"] if data["errorMessage"] else f"error {str(getRecipeIdDetailsResponse.status_code)}"
                csvLogWriter.add([f"{error_reason}", f"{wizardid}", f"{recipeId}", f"{url}"])
                
    csvLogWriter.writeToLogFile()
    return allWizardIdRecipeIdsCombinationsDict

def step_3(allWizardIdRecipeIdsCombinationsDict, step_3_success_schema, err404Schema, err500Schema, token, csvLogWriter):    
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
                postResponse = requests.request("POST", url, headers={
                        'Authorization': 'Bearer ' + token + '',
                        "Content-Type": "application/json; charset=utf-8",
                        "Accept": "application/json"
                    }, data=json.dumps(payload), timeout=100)
                
                if not postResponse.status_code in [200, 404, 500]:
                    csvLogWriter.add([f"Unhandled response [not 200, 404, 500]", f"{wizardid}", f"{payload["recipeId"]}", f"{payload["level"]}", f"{payload["servings"]}", f"{url}"])
                    continue
                
                data = getDataFromResponse(postResponse)
                
                isValid = True
                if postResponse.status_code == 200:
                    isValid = ValidateJson(data, step_3_success_schema)
                elif postResponse.status_code == 404:
                    isValid = ValidateJson(data, err404Schema)
                elif postResponse.status_code == 500:
                    isValid = ValidateJson(data, err500Schema)

                if isValid != True:
                    csvLogWriter.add([f"{isValid}", f"{wizardid}", f"{payload["recipeId"]}", f"{payload["level"]}", f"{payload["servings"]}", f"{url}"])
                    continue
                
                if postResponse.status_code == 200:
                    pass
                elif postResponse.status_code == 404:
                    csvLogWriter.add([f"{data["errorMessage"]}", f"{wizardid}", f"{payload["recipeId"]}", f"{payload["level"]}", f"{payload["servings"]}", f"{url}"])
                elif postResponse.status_code == 500:
                    csvLogWriter.add([f"{data["errorMessage"]}", f"{wizardid}", f"{payload["recipeId"]}", f"{payload["level"]}", f"{payload["servings"]}", f"{url}"])
                    
    csvLogWriter.writeToLogFile()
