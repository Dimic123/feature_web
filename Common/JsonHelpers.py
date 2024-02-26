import json
import os
import jsonschema

def ImportJsonFile(file: str):
    if not os.path.exists(file):
        file = os.path.abspath(file)

    with open(file, 'r') as f:
        return json.load(f)

def AssertValidateJson(_json, _schema):
    try:
        jsonschema.validate(instance=_json, schema=_schema)
    except jsonschema.exceptions.ValidationError as err:
        assert False, err.message
    assert True
