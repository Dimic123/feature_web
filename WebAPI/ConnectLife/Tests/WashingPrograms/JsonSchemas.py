import os

from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory

def CreateJsonSchemas():
    filePath = os.path.realpath(__file__)
    successSchemaArray = CreateJsonSchema(
        "GET response schema for all WashingPrograms requests: SUCCESS 200", 
        "WashingPrograms response schema", 
        [
            {
                "id": "string",
                "name": "string",
                "description": "string",
                "iconUrl": [ "string" ],
                "spin": "string",
                "temperature": "string",
                "timeOnDisplay": "string"
            }
        ]
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_arr", filePath, successSchemaArray)
    
    successSchemaObj = CreateJsonSchema(
        "GET response schema for all WashingPrograms requests: SUCCESS 200", 
        "WashingPrograms response schema", 
        {
            "id": "string",
            "name": "string",
            "description": "string",
            "iconUrl": [ "string" ],
            "spin": "string",
            "temperature": "string",
            "timeOnDisplay": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success_obj", filePath, successSchemaObj)

    err500Schema = CreateJsonSchema(
        "GET response schema for all WashingPrograms requests: ERROR 500", 
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
    
    return [successSchemaArray, successSchemaObj, err500Schema, err404Schema]
