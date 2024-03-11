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
def test_multistep_washing_ids(token: str, connectivityGroupsWithAuids: dict[str, list[str]]):
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
    wizardIdsAndProgramsIdsDictionary = step_1(connectivityGroupsWithAuids, step_1_success_schema, err404Schema, err500Schema, token, step_1_writer)
    # connectivityGroupsWithAuids = {"conn_group": ["auids"]}
    # returns wizardIdsAndProgramsIdsDictionary =  [{"wizard_id": ["program_ids"], "sap_ids": ["sap_id"]}]
    step_1_writer.writeToLogFile()
    
    print("step 2")
    step_2_writer = CsvLogWriter(os.path.join(folder_path, "step_2_logs.txt"))
    step_2_writer.addHeaderAsList(["error", "wizard_id", "program_id", "endpoint"])
    allWizardIdProgramIdsCombinationsDict = step_2(wizardIdsAndProgramsIdsDictionary, err404Schema, err500Schema, token, step_2_writer)
    # wizardIdsAndProgramsIdsDictionary =  [{"wizard_id": ["program_ids"]}]
    # allWizardIdProgramIdsCombinationsDict = [{"wizard_id": {"program_id"}}]
    step_2_writer.writeToLogFile()
    
    print("step 3")
    step_3_writer = CsvLogWriter(os.path.join(folder_path, "step_3_logs.txt"))
    step_3_writer.addHeaderAsList([
        "error", 
        "wizard_id", 
        "payload.program_id", 
        "payload.drumType", 
        "payload.spinSpeed", 
        "payload.puVersionMajor", 
        "payload.puVersionMinor",
        "payload.puVersionPatch",
        "endpoint"
    ])
    step_3(allWizardIdProgramIdsCombinationsDict, step_3_success_schema, err404Schema, err500Schema, token, step_3_writer)
    step_3_writer.writeToLogFile()

def createDictionaryOfWizardidAndProgramIds(group, auid, responseObj, types: list, paramName, csvLogWriter, url) -> dict:
    objects = []
    
    if responseObj == []:
        csvLogWriter.add(["Empty response", f"{group}", f"{auid}", f"{url}"])
        return objects
    
    for item in responseObj:
        skip = False
        itemObj = {}
        if "type" in item and item["type"] in types:
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
                        csvLogWriter.add([f"'parameters' array does no have object with property name: {paramName}", f"{group}", f"{auid}", f"{url}"])
                        continue
                else:
                    csvLogWriter.add([f"'parameters' property has empty value", f"{group}", f"{auid}", f"{url}"])
                    continue
            elif "parameters" in item and len(item["parameters"]) <= 0:
                csvLogWriter.add([f"Value of property name: {paramName} in 'parameters' array is empty ", f"{group}", f"{auid}", f"{url}"])
                continue
            else:
                csvLogWriter.add([f"'parameters' array does no have object with property name: {paramName}", f"{group}", f"{auid}", f"{url}"])
                continue
        elif "type" in item and not item["type"] in types:
            print("** SKIP type: " + str(item["type"]) + " for [group: " + str(group) + ", auid: " + str(auid) + "] because type is not " + str(types))
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

def create_step_2_success_schema(isArray: bool):
    filePath = os.path.realpath(__file__)
    
    schema = [base_jsonschema_success] if isArray else base_jsonschema_success
    
    success200Schema = CreateJsonSchema(
        "GET response schema for /api/v1/washing-programs/{id}/{lang} request: SUCCESS 200", 
        "Washing programs response schema",
        schema
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_step_2_success", filePath, success200Schema)
    
    return success200Schema

def step_1(connectivity_groups, step_1_success_schema, err404Schema, err500Schema, token, csvLogWriter):
    wizardIdsAndProgramsIdsDictionary = {}
    
    num_of_auids = sum(len(connectivity_groups[grp]) for grp in connectivity_groups)
            
    iteration = 0
    for group in connectivity_groups:
        for auid in connectivity_groups[group]:
            iteration += 1
            url = "https://api.connectlife.io/api/v1/wizard/" + auid
            print(f"GET: {url} [{iteration}/{num_of_auids}]")
            response = requests.request("GET", url, headers={'Authorization': 'Bearer ' + token + ''}, data={}, timeout=100)

            if not response.status_code in [200, 404, 500]:
                csvLogWriter.add([f"Unhandled response status code {response.status_code}", f"{group}", f"{auid}", f"{url}"])
                continue
            data = getDataFromResponse(response)
            isValid = True
            if response.status_code == 200:
                isValid = ValidateJson(data, step_1_success_schema)
            elif response.status_code == 404:
                isValid = ValidateJson(data, err404Schema)
            elif response.status_code == 500:
                isValid = ValidateJson(data, err500Schema)

            if isValid != True:
                csvLogWriter.add([f"{isValid}", f"{group}", f"{auid}", f"{url}"])
                continue
            
            if response.status_code == 200:
                wizardIdAndProgramIdsDict = createDictionaryOfWizardidAndProgramIds(group, auid, data, ["WashingProgram"], "programId", csvLogWriter, url)
                if wizardIdAndProgramIdsDict == []:
                    # no wizardid or program ids extracted from response json
                    continue
                
                for item in wizardIdAndProgramIdsDict:
                    wizardIdsAndProgramsIdsDictionary.update(item)

    csvLogWriter.writeToLogFile()
    return wizardIdsAndProgramsIdsDictionary

def step_2(wizardIdsAndProgramIdsDictionary, err404Schema, err500Schema, token, csvLogWriter):    
    allWizardIdProgramIdsCombinationsDict = {}
    total_iterations = sum(len(wizardIdsAndProgramIdsDictionary[wizardId]) for wizardId in wizardIdsAndProgramIdsDictionary)
    
    iteration = 0
    
    for wizardid in wizardIdsAndProgramIdsDictionary:
        allWizardIdProgramIdsCombinationsDict[wizardid] = []
        for id in wizardIdsAndProgramIdsDictionary[wizardid]:
            iteration += 1
            url = "https://api.connectlife.io/api/v1/washing-programs/" + id + "/en"
            print(f"GET: {url} [{iteration}/{total_iterations}]")
            response = requests.request("GET", url, headers={'Authorization': 'Bearer ' + token + ''}, data={}, timeout=100)
            
            if not response.status_code in [200, 404, 500]:
                csvLogWriter.add([f"Unhandled response status code {response.status_code}", f"{wizardid}", f"{id}", f"{url}"])
                continue
            data = getDataFromResponse(response)
            
            isValid = True
            if response.status_code == 200:                
                isValid = ValidateJson(data, create_step_2_success_schema(IsArray(data)))
            elif response.status_code == 404:
                isValid = ValidateJson(data, err404Schema)
            elif response.status_code == 500:
                isValid = ValidateJson(data, err500Schema)

            if isValid != True:
                csvLogWriter.add([f"{isValid}", f"{wizardid}", f"{id}", f"{url}"])
                continue
            
            if response.status_code == 200:
                if data["id"] == id:
                    allWizardIdProgramIdsCombinationsDict[wizardid].append({
                        "programId": id
                    })
                else:
                    error_reason = f"response id ({data["id"]}) is not the same as requested id ({id})"
                    csvLogWriter.add([f"{error_reason}", f"{wizardid}", f"{id}", f"{url}"])
            elif response.status_code == 404:
                csvLogWriter.add([f"{data["title"]}", f"{wizardid}", f"{id}", f"{url}"])
            elif response.status_code == 500:                
                error_reason = data["errorMessage"] if data["errorMessage"] else f"error {str(response.status_code)}"
                csvLogWriter.add([f"{error_reason}", f"{wizardid}", f"{id}", f"{url}"])
                
    csvLogWriter.writeToLogFile()
    return allWizardIdProgramIdsCombinationsDict

def step_3(allWizardIdProgramIdsCombinationsDict, step_3_success_schema, err404Schema, err500Schema, token, csvLogWriter):    
    total_iterations = 0
    
    for wizardid in allWizardIdProgramIdsCombinationsDict:
        for obj in allWizardIdProgramIdsCombinationsDict[wizardid]:
            total_iterations += 1
    
    iteration = 0
    
    for wizardid in allWizardIdProgramIdsCombinationsDict:
        url = "https://api.connectlife.io/api/v1/wizard/washing-program/" + wizardid
        for obj in allWizardIdProgramIdsCombinationsDict[wizardid]:
            payload = {
                "programId": obj["programId"],
                "drumType": 2,
                "spinSpeed": 7,
                "puVersionMajor": "002",
                "puVersionMinor": "001",
                "puVersionPatch": "002"
            }
            
            payloadValuesList = getListOfPayloadValues(payload)
            payloadValuesList.append(url)
            
            iteration += 1
            print(f"POST: {url} [{iteration}/{total_iterations}], {payload}")
            postResponse = requests.request("POST", url, headers={
                    'Authorization': 'Bearer ' + token + '',
                    "Content-Type": "application/json; charset=utf-8",
                    "Accept": "application/json"
                }, data=json.dumps(payload), timeout=100)
            
            data = getDataFromResponse(postResponse)
            
            if not postResponse.status_code in [200, 404, 500]:
                logWriterList = [f"Unhandled response status code: {postResponse.status_code}", f"{wizardid}"]
                logWriterList += payloadValuesList
                csvLogWriter.add(logWriterList)
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
                logWriterList = [f"{isValid}", f"{wizardid}"]
                logWriterList += payloadValuesList
                csvLogWriter.add(logWriterList)
                continue
            
            if postResponse.status_code == 200:
                pass
            elif postResponse.status_code == 404:
                logWriterList = [f"{data["errorMessage"]}", f"{wizardid}"]
                logWriterList += payloadValuesList
                csvLogWriter.add(logWriterList)
            elif postResponse.status_code == 500:
                logWriterList = [f"{data["errorMessage"]}", f"{wizardid}"]
                logWriterList += payloadValuesList
                csvLogWriter.add(logWriterList)

    csvLogWriter.writeToLogFile()


def getListOfPayloadValues(payload):
    valuesList = []
    for key in payload:
        valuesList.append(str(payload[key]))
            
    return valuesList
