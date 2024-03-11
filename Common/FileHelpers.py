import json, os

def WriteDataToJsonFileInCurrentDirectory(name: str, currentFilePath: str, data, mode="w"):
    dirPath = currentFilePath.split("\\")[:-1]
    filePath = os.path.join("\\".join(dirPath), name + ".json")
    
    with open(filePath, mode) as file:
        file.write(json.dumps(data, indent=3))
        file.write("\n")
    
def GenerateTestCasesJsonFile(testCases, jsonFilePath: str):
    testCasesObject = { "general_data": {}, "settings": {}, "test_cases": {} }
    
    for index, testcase in enumerate(testCases):
        testCasesObject["test_cases"]["case_" + str(index + 1)] = testcase
    
    with open(jsonFilePath, "w") as file:
        file.write(json.dumps(testCasesObject, indent=3))

def GenerateTestCasesJsonFileList(testCases, jsonFilePath: str):
    testCasesObject = []
    
    for index, testcase in enumerate(testCases):
        key = "case_" + str(index + 1)
        testCasesObject.append({ key: testcase })
    
    with open(jsonFilePath, "w") as file:
        file.write(json.dumps(testCasesObject, indent=3))