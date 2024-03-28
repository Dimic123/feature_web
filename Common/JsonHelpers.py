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
    
def ValidateJson(_json, _schema):
    try:
        jsonschema.validate(instance=_json, schema=_schema)
    except jsonschema.exceptions.ValidationError as err:
        return err.message
    return True

def getWizardIdsForType(wizard_type, wizard_ids):
    wizard_objects = []
    for wizard_id in wizard_ids:
        if wizard_ids[wizard_id]["wizard_type"] == wizard_type:
            wizard_objects.append(wizard_ids[wizard_id])
    return wizard_objects