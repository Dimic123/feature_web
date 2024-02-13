schema = {
    "title": "get_scenes",
    "description": "GET request for ../get_scenes endpoint",
    "definitions": {
        "scene_entry": {
            "properties": {
                "sceneId": {
                    "type": "number"
                },
                "sceneName": {
                    "type": "string"
                },
                "sceneType": {
                    "type": "number"
                },
                "status": {
                    "type": "number"
                },
                "cmdList": {
                    "type": "array"
                },
                "cmdEndList": {
                    "type": "array"
                },
                "sceneTrigCondition": {
                    "type": "array"
                },
                "executionCycle": {
                    "type": "number"
                },
                "executionDate": {
                    "type": ["string", "null"]
                },
                "executionTime": {
                    "type": ["string", "null"]
                },
                "effectiveDate": {
                    "type": ["string", "null"]
                },
                "conditionRelationship": {
                    "type": "number"
                },
                "sceneIconId": {
                    "type": "number"
                },
                "timezone": {
                    "type": ["string", "null"]
                },
                "validTimeList": {
                    "type": ["string", "null"]
                },
                "executionNotify": {
                    "type": "number"
                },
                "displayInMain": {
                    "type": "number"
                },
                "favorite": {
                    "type": "number"
                }
            }
        }
    },
    "type": "object",
    "properties": {
        "resultCode": {
            "type": "number"
        },
        "sceneList": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/scene_entry"
            }
        }
    }
}

def add_required_fields_to_schema():
    schema["required"] = []
    for key in schema["properties"]:
        schema["required"].append(key)

    schema["definitions"]["scene_entry"]["required"] = []
    for key in schema["definitions"]["scene_entry"]["properties"]:
        schema["definitions"]["scene_entry"]["required"].append(key)
        
add_required_fields_to_schema()