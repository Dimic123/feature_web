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
def test_multistep_washing_ids(token: str, connectivityGroupsWithAuids: dict[str, list[str]]):
    folder_path = os.path.dirname(os.path.realpath(__file__))

    [step_1_success_schema, step_3_success_schema, err404Schema, err500Schema, err400Schema] = CreateValidationSchemas()
    setGlobalSchemas(step_1_success_schema, step_3_success_schema, err404Schema, err500Schema, err400Schema)

    print("step 1")
    step_1_writer = CsvLogWriter(os.path.join(folder_path, "step_1_logs.txt"))
    step_1_writer.addHeaderAsList(["error", "connectivity_group", "sap_id", "endpoint"])
    wizardIdsAndProgramsIdsDictionary = step_1(connectivityGroupsWithAuids, token, step_1_writer)
    step_1_writer.writeToLogFile()
    
    print("step 2")
    step_2_writer = CsvLogWriter(os.path.join(folder_path, "step_2_logs.txt"))
    step_2_writer.addHeaderAsList(["error", "wizard_id", "program_id", "endpoint"])
    allWizardIdProgramIdsCombinationsDict = step_2(wizardIdsAndProgramsIdsDictionary, token, step_2_writer)
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
    step_3(allWizardIdProgramIdsCombinationsDict, token, step_3_writer)
    step_3_writer.writeToLogFile()

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

def getListOfPayloadValues(payload):
    valuesList = []
    for key in payload:
        valuesList.append(str(payload[key]))

    return valuesList

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
            global SUCCESS_STEP_1_SCHEMA
            isValid = isResponseDataValid(response.status_code, data, SUCCESS_STEP_1_SCHEMA)

            if isValid != True:
                csvLogWriter.add([f"{isValid}", f"{group}", f"{auid}", f"{url}"])
                continue
            
            if response.status_code == 200:
                listOfWizardids = get_list_of_wizard_ids_for_specific_types_and_param_name(data, ["WashingProgram"], "programId", csvLogWriter, group, auid, url)
                if listOfWizardids == []:
                    continue
                
                for item in listOfWizardids:
                    wizardIdsAndProgramsIdsDictionary.update(item)
                print("OK")
            else:
                csvLogWriter.add([f"response status code: {response.status_code}", f"{group}", f"{auid}", f"{url}"])

    csvLogWriter.writeToLogFile()
    return wizardIdsAndProgramsIdsDictionary

def step_2(wizardIdsAndProgramIdsDictionary, token, csvLogWriter):    
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
            isValid = isResponseDataValid(response.status_code, data, create_step_2_success_schema(IsArray(data)))

            if isValid != True:
                csvLogWriter.add([f"{isValid}", f"{wizardid}", f"{id}", f"{url}"])
                continue
            
            if response.status_code == 200:
                if data["id"] == id:
                    allWizardIdProgramIdsCombinationsDict[wizardid].append({ "programId": id })
                    print("OK")
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

def step_3(allWizardIdProgramIdsCombinationsDict, token, csvLogWriter):
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
            response = requests.request("POST", url, headers={
                    'Authorization': 'Bearer ' + token + '',
                    "Content-Type": "application/json; charset=utf-8",
                    "Accept": "application/json"
                }, data=json.dumps(payload), timeout=100)
            
            if not response.status_code in [200, 404, 500]:
                logWriterList = [f"Unhandled response status code: {response.status_code}", f"{wizardid}"]
                logWriterList += payloadValuesList
                csvLogWriter.add(logWriterList)
                continue
            
            data = getDataFromResponse(response)
            global SUCCESS_STEP_3_SCHEMA
            isValid = isResponseDataValid(response.status_code, data, SUCCESS_STEP_3_SCHEMA)

            if isValid != True:
                logWriterList = [f"{isValid}", f"{wizardid}"]
                logWriterList += payloadValuesList
                csvLogWriter.add(logWriterList)
                continue
            
            if response.status_code == 200:
                print("OK")
                pass
            elif response.status_code == 400:
                logWriterList = [f"{data["errorMessage"]}", f"{wizardid}"]
                logWriterList += payloadValuesList
                csvLogWriter.add(logWriterList)
            elif response.status_code == 404:
                logWriterList = [f"{data["errorMessage"]}", f"{wizardid}"]
                logWriterList += payloadValuesList
                csvLogWriter.add(logWriterList)
            elif response.status_code == 500:
                logWriterList = [f"{data["errorMessage"]}", f"{wizardid}"]
                logWriterList += payloadValuesList
                csvLogWriter.add(logWriterList)

    csvLogWriter.writeToLogFile()
