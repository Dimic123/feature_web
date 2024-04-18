import requests, json, copy, xmltodict, os
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

def convert_xml_to_json_washing_machine(xml_structure):
    ELEMENT = ET.fromstring(xml_structure)
    tree = ET.ElementTree(ELEMENT)

    wash_sheet = []
    sensitivity_sheet = []
    stain_sheet = []
    
    for item in tree.getroot():
        if "root" == item.tag:
            for child in item:
                json_data = { "node": {}, "outputs": {} }
                recursively_convert_xml_to_json_washing_machine(child, json_data, wash_sheet, sensitivity_sheet, stain_sheet)
        else:
            raise Exception("Root tag is missing")
    return [wash_sheet, sensitivity_sheet, stain_sheet]

def recursively_convert_xml_to_json_washing_machine(root, json_data, wash_sheet, sensitivity_sheet, stain_sheet):
    if len(root) == 0:
        json_data[root.tag][root.attrib["attribute"]] = root.attrib["value"]
    else:
        if root[0].tag == "outputs":
            json_data[root.tag][root.attrib["attribute"]] = root.attrib["value"]
            for item in root:
                json_data[item.tag][item.attrib["name"]] = item.attrib["value"]
            # Excel "wash" sheet
            if "TYPE" in json_data["node"] and "COLOR" in json_data["node"] and "DIRTINESS" in json_data["node"] and not "STAIN" in json_data["node"]:
                wash_sheet.append(json_data)
            # Excel "sensitivity" sheet
            if "TYPE" in json_data["node"] and "SENSITIVITY" in json_data["node"] and not "STAIN" in json_data["node"]:
                sensitivity_sheet.append(json_data)
            # Excel "stains" sheet
            if "COLOR" in json_data["node"] and "STAIN" in json_data["node"]:
                stain_sheet.append(json_data)
        else:
            number_of_child_nodes = len(root)
            if number_of_child_nodes > 0:
                json_data[root.tag][root.attrib["attribute"]] = root.attrib["value"]

                for child in root:
                    deep_copy = copy.deepcopy(json_data)
                    recursively_convert_xml_to_json_washing_machine(child, deep_copy, wash_sheet, sensitivity_sheet, stain_sheet)

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
                    "MOTOR_SPIN_SPEED": int(float(s_row["outputs"]["MOTOR_SPIN_SPEED"])),
                    "PROGRAM_OPTION": program_option
                }

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
                    "MOTOR_SPIN_SPEED": combination_without_stain["MOTOR_SPIN_SPEED"],
                    "PROGRAM_OPTION": program_options_as_string
                }
                combinations_with_stain.append(row)

    return [combinations_without_stain, combinations_with_stain]
