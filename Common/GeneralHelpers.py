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
                errors += f"{_property} is {response_data[_property]}. Expected value is: {expected_response_obj[_property]}."
        elif isinstance(expected_response_obj[_property], float):
            if float(response_data[_property]) != float(expected_response_obj[_property]):
                errors += f"{_property} is {response_data[_property]}. Expected value is: {expected_response_obj[_property]}."
        elif isinstance(response_data[_property], list):
            separator = ","
            list_as_string = separator.join(response_data[_property])
            
            if list_as_string != expected_response_obj[_property]:
                errors += f"{_property} is {list_as_string}. Expected value is: {expected_response_obj[_property]}."
        else:
            if str(response_data[_property]) != str(expected_response_obj[_property]):
                errors += f"{_property} is {response_data[_property]}. Expected value is: {expected_response_obj[_property]}."
    return errors

def get_item_from_list(_substring, _list):
    for item in _list:
        if _substring in item:
            return item
    return None
