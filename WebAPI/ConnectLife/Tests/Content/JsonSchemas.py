import os

from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory

def CreateJsonSchemas():
    filePath = os.path.realpath(__file__)
    success200Schema = CreateJsonSchema(
        "GET response schema for all Content requests: SUCCESS 200", 
        "Content response schema", 
        [
            {
                "id": "string",
                "title": "string",
                "name": "string",
                "shortDescription": "string|null",
                "attachments": "array|null",
                "content": "string",
                "lang": "string",
                "sapId": "string",
                "contentCode": "string"
            }
        ]
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success", filePath, success200Schema)

    err500Schema = CreateJsonSchema(
        "GET response schema for all Content requests: ERROR 500", 
        "Content response schema", 
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error", filePath, err500Schema)
    
    return [success200Schema, err500Schema]

schemas = CreateJsonSchemas()
