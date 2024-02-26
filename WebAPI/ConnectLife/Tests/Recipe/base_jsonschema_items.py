base_jsonschema_items = {
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