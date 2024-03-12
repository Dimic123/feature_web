import os, sys

projectRootPath = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-4])
sys.path.append(projectRootPath)

from Common.JsonSchemaHelpers import CreateJsonSchema
from Common.FileHelpers import WriteDataToJsonFileInCurrentDirectory

def CreateValidationSchemas():
    filePath = os.path.realpath(__file__)
    success_schema = CreateJsonSchema(
        "SUCCESS 200 GET response schema for /api/v1/recipes/paged/detail/{lang}", 
        "Recipe paged detail lang schema", 
        {
            "count": "number",
            "pageSize": "number",
            "numPages": "number",
            "currentPage": "number",
            "links": [
                {
                "href": "string",
                "rel": "string",
                "method": "string",
                "isTemplated": "boolean"
                }
            ],
            "items": [
                {
                "id": "string",
                "title": "string",
                "imageUrl": "string",
                "difficulty": "string",
                "noOfPersonsDefault": "number",
                "noOfPersonsMin": "number",
                "noOfPersonsMax": "number",
                "type": "string",
                "description": "string",
                "allergens": [
                    {
                    "id": "string",
                    "title": "string",
                    "desc": "string|null"
                    }
                ],
                "steps": [
                    {
                    "desc": "string",
                    "id": "string"
                    }
                ],
                "diet": [
                    {
                    "iconUrl": "string|null",
                    "id": "string",
                    "title": "string",
                    "desc": "string|null"
                    }
                ],
                "ingredients": [
                    {
                    "id": "string",
                    "title": "string",
                    "friendlyQuantity": "string",
                    "isLockable": "boolean",
                    "quantity": "number",
                    "unit": "string"
                    }
                ],
                "links": [
                    {
                    "href": "string",
                    "rel": "string",
                    "method": "string",
                    "isTemplated": "boolean"
                    }
                ]
                }
            ]
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_step_1_success", filePath, success_schema)
    
    err500Schema = CreateJsonSchema(
        "ERROR 500 response schema for /api/v1/recipes/paged/detail/{lang}", 
        "Recipe response schema", 
        {
            "errorId": "string",
            "errorMessage": "string"
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error", filePath, err500Schema)
    
    err400Schema = CreateJsonSchema(
        "ERROR 400 response schema for /api/v1/recipes/paged/detail/{lang}",
        "Recipes paged detail lang response schema", 
        {
            "type": "string",
            "title": "string",
            "status": "number",
            "traceId": "string",
            "errors": {
                "pageSize": ["string"]
            }
        }
    )
    WriteDataToJsonFileInCurrentDirectory("_jsonschema_error", filePath, err400Schema)
    
    return [success_schema, err400Schema, err500Schema]
