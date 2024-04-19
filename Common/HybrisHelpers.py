import requests, json, copy
from xml.etree import ElementTree as ET

def get_all_wizard_logic_xml(access_token):
    url = "https://api.cdrwhdl6-hisenseeu2-p1-public.model-t.cc.commerce.ondemand.com/ggcommercewebservices/v2/general/wizards/export"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Cookie": "ROUTE=.api-658f7665b9-5xpvb"
    }

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)

    wizards = []

    for el in data["wizardRecords"]:
        wizards.append({
            "wizard_id": el["id"],
            "logic": el["logic"]
        })
    return wizards

def conditionally_append_test_case(json_data, list_of_excel_configurations):
    for excel_config in list_of_excel_configurations:
        meets_criteria = True
        for sheet_criteria in excel_config["excel_sheet_criteria"]:
            if "rule_negation" in sheet_criteria and sheet_criteria["rule_negation"] == True:
                if sheet_criteria["property"] in json_data[sheet_criteria["type"]]:
                    meets_criteria = False
            else:
                if not sheet_criteria["property"] in json_data[sheet_criteria["type"]]:
                    meets_criteria = False
        if meets_criteria and json_data["outputs"] != {}:
            excel_config["excel_sheet"].append(json_data)

def convert_xml_to_json_GENERIC(xml_structure, list_of_excel_configurations):
    ELEMENT = ET.fromstring(xml_structure)
    tree = ET.ElementTree(ELEMENT)
    
    for item in tree.getroot():
        if "root" == item.tag:
            for child in item:
                json_data = { "node": {}, "outputs": {} }
                json_data[child.tag][child.attrib["attribute"]] = child.attrib["value"]
                recursively_convert_xml_to_json_GENERIC(child, json_data, list_of_excel_configurations)
        else:
            raise Exception("Root tag is missing")

def recursively_convert_xml_to_json_GENERIC(root, json_data, list_of_excel_configurations):
    if len(root) > 0:
        outputs = []
        for child in root:
            if child.tag == "node":
                json_data[child.tag][child.attrib["attribute"]] = child.attrib["value"]
                deep_copy = copy.deepcopy(json_data)
                recursively_convert_xml_to_json_GENERIC(child, deep_copy, list_of_excel_configurations)
            elif child.tag == "outputs":
                outputs.append({ "tag": child.tag, "attrib": child.attrib["name"], "value": child.attrib["value"] })
        for output in outputs:
            json_data[output["tag"]][output["attrib"]] = output["value"]

        conditionally_append_test_case(json_data, list_of_excel_configurations)
    else:
        if "attribute" in root.attrib:
            json_data[root.tag][root.attrib["attribute"]] = root.attrib["value"]
            # maybe allow outputs to be empty in this case -> test cases in excel can also have empty outputs
            # if "yes", comment the if statement
            if json_data["outputs"] != {}:
                conditionally_append_test_case(json_data, list_of_excel_configurations)
        else:
            raise Exception("attribute not supported")

def convert_to_int_or_return_str(value: str) -> str | int:
    try:
        float_val = float(value)
        int_val = int(float_val)
        return int_val
    except ValueError:
        return value.upper()

def remove_empty_values(item):
    return item != ""

def create_combinations_washing_machine(sensitivity, wash, stain):
    combinations_without_stain = []
    combinations_with_stain = []

    for s_row in sensitivity:
        for w_row in wash:
            if s_row["node"]["TYPE"] == w_row["node"]["TYPE"]:
                program_option = ""
                if "PROGRAM_OPTION" in w_row["outputs"]:
                    program_option = str(w_row["outputs"]["PROGRAM_OPTION"])

                converted_temp = convert_to_int_or_return_str(w_row["outputs"]["TEMPARATURE"])
                
                row = {
                    "TYPE": str(w_row["node"]["TYPE"]),
                    "COLOR": str(w_row["node"]["COLOR"]),
                    "DIRTINESS": str(w_row["node"]["DIRTINESS"]),
                    "SELECTED_PROGRAM": str(w_row["outputs"]["SELECTED_PROGRAM"]),
                    "TEMPARATURE": converted_temp,
                    "SENSITIVITY": str(s_row["node"]["SENSITIVITY"]),
                    "PROGRAM_OPTION": program_option
                }

                if "MOTOR_SPIN_SPEED" in s_row["outputs"]:
                    row["MOTOR_SPIN_SPEED"] = int(float(s_row["outputs"]["MOTOR_SPIN_SPEED"]))

                combinations_without_stain.append(row)

    for st_row in stain:
        stain_color = str(st_row["node"]["COLOR"])
        stain_dirtiness = str(st_row["node"]["DIRTINESS"])
        stain_stain = str(st_row["node"]["STAIN"])
        stain_selected_program = st_row["outputs"]["SELECTED_PROGRAM"] if "SELECTED_PROGRAM" in st_row["outputs"] else ""
        stain_program_option = st_row["outputs"]["PROGRAM_OPTION"] if "PROGRAM_OPTION" in st_row["outputs"] else ""
        
        stain_temperature = convert_to_int_or_return_str(st_row["outputs"]["TEMPARATURE"]) if "TEMPARATURE" in st_row["outputs"] else None

        for combination_without_stain in combinations_without_stain:
            if combination_without_stain["COLOR"] == stain_color and combination_without_stain["DIRTINESS"] == stain_dirtiness:
                selected_program = stain_selected_program
                if selected_program == "":
                    selected_program = combination_without_stain["outputs"]["SELECTED_PROGRAM"]

                previous_program_option = combination_without_stain["PROGRAM_OPTION"]
                current_program_option = stain_program_option

                all_program_options = list(set(previous_program_option.split(",") + current_program_option.split(",")))
                filtered_program_options = list(filter(remove_empty_values, all_program_options))
                program_options_as_string = ",".join(filtered_program_options)

                temperature = ""

                if stain_temperature == None:
                    temperature = combination_without_stain["TEMPARATURE"]
                else:
                    if type(stain_temperature) is str or type(combination_without_stain["TEMPARATURE"]) is str:
                        temperature = "COLD"
                    else:
                        if stain_temperature < combination_without_stain["TEMPARATURE"]:
                            temperature = stain_temperature
                        else:
                            temperature = combination_without_stain["TEMPARATURE"]

                row = {
                    "TYPE": combination_without_stain["TYPE"],
                    "COLOR": combination_without_stain["COLOR"],
                    "STAIN": stain_stain.replace("/", ""),
                    "DIRTINESS": combination_without_stain["DIRTINESS"],
                    "SELECTED_PROGRAM": selected_program,
                    "TEMPARATURE": temperature,
                    "SENSITIVITY": combination_without_stain["SENSITIVITY"],
                    "PROGRAM_OPTION": program_options_as_string
                }

                if "MOTOR_SPIN_SPEED" in combination_without_stain:
                    row["MOTOR_SPIN_SPEED"] = combination_without_stain["MOTOR_SPIN_SPEED"]

                combinations_with_stain.append(row)

    return [combinations_without_stain, combinations_with_stain]
