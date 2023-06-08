import json
import os


def ImportJsonFile(file: str):
    if not os.path.exists(file):
        file = os.path.abspath(file)

    with open(file, 'r') as f:
        return json.load(f)
