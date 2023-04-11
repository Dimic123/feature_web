
import json
import os


def pytest_generate_tests(metafunc):
    # called once per each test function

    json_file = os.path.join(metafunc.definition.fspath.dirname, metafunc.definition.fspath.purebasename + ".json")
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            json_data = json.load(f)

    data = []
    for case in json_data:
        data.append(json_data[case])

    metafunc.parametrize("data", data)


def pytest_runtest_setup(item):
    pass