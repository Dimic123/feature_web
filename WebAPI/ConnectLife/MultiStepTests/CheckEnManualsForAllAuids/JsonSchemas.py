from Common.JsonSchemaHelpers import CreateJsonSchema

def createSuccessSchema():
    return CreateJsonSchema(
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

schema = createSuccessSchema()
