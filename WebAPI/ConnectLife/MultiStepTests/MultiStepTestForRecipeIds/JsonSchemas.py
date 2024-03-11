import os, sys

projectRootPath = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-4])
sys.path.append(projectRootPath)

from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory

def create_different_schemas():
    filePath = os.path.realpath(__file__)
    step_1_success_schema = CreateJsonSchema(
        "GET response schema for /api/v1/wizard/{auids} requests: SUCCESS 200", 
        "Wizard response schema", 
        [
            {
                "id": "string",
                "name": "string",
                "descryption": "string",
                "type": "string",
                "data": "array|null",
                "metaData": "object|null",
                "parameters": [
                    {
                        "name": "string",
                        "possibleValues": "array|null",
                        "isExternalSource": "boolean",
                        "Extra": "number"
                    }
                ],
                "sapIds": [ "string" ]
            }
        ]
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_step_1_success", filePath, step_1_success_schema)
    
    step_3_success_schema = CreateJsonSchema(
        "GET response schema for /api/v1/wizard/recipe/{wizardid} requests: SUCCESS 200", 
        "Wizard response schema", 
        {
            "container": "string",
            "shelf": "number",
            "numOfSteps": "number",
            "preheat": "boolean",
            "bakeSteps": [
                {
                    "type": "string",
                    "typeDisplayValue": "string",
                    "heaterSystem": "string",
                    "temperatureSetpoint": "number",
                    "duration": "number",
                    "microwavePower": "number",
                    "steam": "boolean",
                    "steamStart": "number",
                    "steamStop": "number",
                    "stepNumber": "number"
                }
            ]
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_step_3_success", filePath, step_3_success_schema)
    
    err500Schema = CreateJsonSchema(
        "Generic response schema for ERROR 500", 
        "WashingPrograms response schema", 
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error", filePath, err500Schema)
    
    err404Schema = CreateJsonSchema(
        "GET response schema for all WashingPrograms requests: ERROR 404", 
        "WashingPrograms response schema", 
        {
            "type": "string",
            "title": "string",
            "status": "number",
            "traceId": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_404", filePath, err404Schema)
    
    return [step_1_success_schema, step_3_success_schema, err404Schema, err500Schema]
