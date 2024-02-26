import os

from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory

def CreateJsonSchemas():
    filePath = os.path.realpath(__file__)
    success200Schema = CreateJsonSchema(
        "GET response schema for all Manuals requests: SUCCESS 200", 
        "Manuals response schema", 
        [
            {
                "id": "string",
                "desc": "string",
                "type": "string",
                "mimeType": "string",
                "url": "string",
                "lang": "string",
                "sapId": "string",
                "instructionsClass": "string",
                "instructionsClassName": "string"
            }
        ]
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success", filePath, success200Schema)

    err500Schema = CreateJsonSchema(
        "GET response schema for all Manuals requests: ERROR 500", 
        "Manuals response schema", 
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error", filePath, err500Schema)
    
    return [success200Schema, err500Schema]

schemas = CreateJsonSchemas()
