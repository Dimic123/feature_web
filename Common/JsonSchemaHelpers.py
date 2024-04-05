def IsArray(structure: any) -> bool:
    return type(structure) is list

def IsObject(structure: any) -> bool:
    return type(structure) is dict

def GetPropertyTypesArray(typeDefinition: str) -> dict[str, list]:
    return { "type": typeDefinition.split("|") }

def GetArrayTypeOrFalse(array: list) -> bool | str:    
    for x in range(1, len(array)):
        if array[x] != array[0]:
            return False
    return array[0]

def GetArrayOfTypes(data):
    typesArr = []
    for element in data:
        if (type(element).__name__ == "str"):
            typesArr.append(element)
        else:
            if (type(element).__name__ == "dict"):
                typesArr.append("object")
            elif (type(element).__name__ == "list"):
                typesArr.append("array")
    return typesArr

def CreateJsonSchema(title: str, description: str, data):
    schema = {}
    
    if title: schema["title"] = title
    if description: schema["description"] = description

    if (IsArray(data)):
        schema["type"] = "array"
        arrTypes = GetArrayOfTypes(data)
        
        if len(data) == 1:
            if arrTypes[0] == "object" or arrTypes[0] == "array":
                schema["items"] = CreateJsonSchema(None, None, data[0])
            else:
                schema["items"] = GetPropertyTypesArray(arrTypes[0]) # { "type": [arrTypes[0]] }
        elif len(data) > 1:
            arrayType = GetArrayTypeOrFalse(arrTypes)
            if arrayType == False:
                schema["items"] = { "oneOf": [] }
                
                for arrEl in data: # arrEl => "string|number|boolean"
                    if type(arrEl).__name__ == "list" or type(arrEl).__name__ == "dict":
                        childElement = CreateJsonSchema(None, None, arrEl)
                        schema["items"]["oneOf"].append(childElement)
                    elif "regex" in data:
                        pass
                    else:
                        newTypes = ""
                        
                        schemaExistingTypes = []
                        for oneOf in schema["items"]["oneOf"]:
                            if oneOf["type"] != "object" and oneOf["type"] != "array":
                                schemaExistingTypes += oneOf["type"]
                        
                        for arrElType in arrEl.split("|"):
                            if not arrElType in schemaExistingTypes:
                                newTypes += arrElType + "|"
                        
                        if newTypes != "":
                            newTypes = newTypes[:-1]
                            schema["items"]["oneOf"].append(GetPropertyTypesArray(newTypes))
            else:
                schema["items"] = GetPropertyTypesArray(arrayType)
    elif (IsObject(data)):
        schema["additionalProperties"] = False
        schema["type"] = "object"
        schema["properties"] = {}
        
        for key in data:
            if "+allowAdditionalProperties" in key:
                extracted_property_name = key.split("+")[0]
                if IsArray(data[key]):
                    schema["properties"][extracted_property_name] = { "type": "array" }
                    schema["properties"][extracted_property_name]["additionalProperties"] = True
                elif IsObject(data[key]):
                    schema["properties"][extracted_property_name] = { "type": "object" }
                    schema["properties"][extracted_property_name]["additionalProperties"] = True
            elif "regex:" in key:
                regex_condition = key[6:]
                del schema["properties"] # unset properties
                schema["patternProperties"] = { regex_condition: {} }
                
                if IsArray(data[key]) or IsObject(data[key]):
                    schema["patternProperties"][regex_condition] = CreateJsonSchema(None, None, data[key])
                elif type(data[key]) == str:
                    schema["patternProperties"][regex_condition] = GetPropertyTypesArray(data[key])
            elif IsArray(data[key]) or IsObject(data[key]):
                if not "properties" in schema:
                    schema["properties"] = {}
                schema["properties"][key] = CreateJsonSchema(None, None, data[key])
            elif type(data[key]) == str:                    
                if not "properties" in schema:
                    schema["properties"] = {}
                schema["properties"][key] = GetPropertyTypesArray(data[key])
    return schema