import os

from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory

def CreateJsonSchemas():
    filePath = os.path.realpath(__file__)
    success200Schema = CreateJsonSchema(
        "GET response schema for all Products requests: SUCCESS 200", 
        "Products response schema", 
        [
            {
                "applianceGeneration": "string",
                "brand": "string",
                "code": "string",
                "connectivityGroup": "string",
                "constructionType": "string",
                "productFamily": "string",
                "modelMark": "string",
                "name": "string",
                "primaryImage": "string",
                "productLine": "string",
                "typeMark": "string",
                "wifiControl": "string",
                "mcuNumber": ["string"],
                "parameterReading": ["string"],
                "eanCode": "string"
            }
        ]
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_success", filePath, success200Schema)

    err500Schema = CreateJsonSchema(
        "GET response schema for all Products requests: ERROR 500", 
        "Products response schema", 
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error", filePath, err500Schema)
    
    return [success200Schema, err500Schema]
