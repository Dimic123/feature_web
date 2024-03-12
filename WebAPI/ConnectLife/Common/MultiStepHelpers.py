import json

def get_list_of_wizard_ids_for_specific_types_and_param_name(data, types: list, paramName, csvLogWriter, group, auid, url) -> dict:
    listOfItemObjects = []
    
    if data == []:
        csvLogWriter.add(["Empty response", f"{group}", f"{auid}", f"{url}"])
        return listOfItemObjects
    
    for item in data:
        skip = False
        itemObj = {}
        if "type" in item and item["type"] in types:
            itemId = ""
            if "id" in item and item["id"] != "":
                itemId = item["id"]
            else:
                csvLogWriter.add(["Missing property: 'wizardid'", f"{group}", f"{auid}", f"{url}"])
                continue
            
            if "parameters" in item and len(item["parameters"]) > 0:
                if len(item["parameters"]) > 0:
                    paramNameExists = False
                    for param in item["parameters"]:
                        if param["name"] == paramName:
                            paramNameExists = True
                            if "possibleValues" in param and len(param["possibleValues"]) > 0:
                                itemObj[itemId] = param["possibleValues"]
                            else:
                                csvLogWriter.add(["'possibleValues' are empty", f"{group}", f"{auid}", f"{url}"])
                                skip = True
                                break
                    if skip: continue
                    if not paramNameExists:
                        csvLogWriter.add([f"'parameters' array does no have object with property name: {paramName}", f"{group}", f"{auid}", f"{url}"])
                        continue
                else:
                    csvLogWriter.add([f"'parameters' property has empty value", f"{group}", f"{auid}", f"{url}"])
                    continue
            elif "parameters" in item and len(item["parameters"]) <= 0:
                csvLogWriter.add([f"Value of property name: {paramName} in 'parameters' array is empty ", f"{group}", f"{auid}", f"{url}"])
                continue
            else:
                csvLogWriter.add([f"'parameters' array does no have object with property name: {paramName}", f"{group}", f"{auid}", f"{url}"])
                continue
        elif "type" in item and not item["type"] in types:
            print("** SKIP type: " + str(item["type"]) + " for [group: " + str(group) + ", auid: " + str(auid) + "] because type is not " + str(types))
            pass
        else:
            csvLogWriter.add([f"Property 'type' is missing", f"{group}", f"{auid}", f"{url}"])
        listOfItemObjects.append(itemObj)
    return listOfItemObjects

def getDataFromResponse(response):
    try:
        unicode_escaped_data = json.dumps(response.json())
        data = json.loads(unicode_escaped_data)
        return data
    except Exception as ex:
        raise Exception("Malformed data: " + response.text) from ex
