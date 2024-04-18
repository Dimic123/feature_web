import requests

def SendRequest(reqType, url, headers, payload, timeout: int):
    return requests.request(reqType, url, headers=headers, data=payload, timeout=timeout)

def isNaN(num):
    return num != num

def get_possible_errors(response_data, expected_response_obj, _property):
    errors = ""
    if not _property in response_data and _property in expected_response_obj:
        errors += f"{_property} is missing in response. "
    elif _property in expected_response_obj and _property in response_data:
        if isinstance(expected_response_obj[_property], int):
            if int(response_data[_property]) != int(expected_response_obj[_property]):
                errors += f"{_property} is '{response_data[_property]}'. Expected value is: {expected_response_obj[_property]}."
        elif isinstance(expected_response_obj[_property], float):
            if float(response_data[_property]) != float(expected_response_obj[_property]):
                errors += f"{_property} is '{response_data[_property]}'. Expected value is: {expected_response_obj[_property]}."
        elif isinstance(response_data[_property], list):
            separator = ","
            list_as_string = separator.join(response_data[_property])
            
            if list_as_string != expected_response_obj[_property]:
                errors += f"{_property} is '{list_as_string}'. Expected value is: {expected_response_obj[_property]}."
        else:
            if str(response_data[_property]).lower() != str(expected_response_obj[_property]).lower():
                errors += f"{_property} is '{response_data[_property].lower()}'. Expected value is: '{expected_response_obj[_property].lower()}'."
    return errors

def get_item_from_list(_substring, _list):
    for item in _list:
        if _substring.lower() in item.lower():
            return item
    return None

def get_number_as_en_word(number: int) -> str:
    number2word = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 0: "zero"}
    return number2word[number].capitalize()

def get_version_str(string) -> str:
    if len(string) == 1:
        return "00" + string
    elif len(string) == 2:
        return "0" + string
    else:
        return string
