import json

def WriteDataToJsonFileInCurrentDirectory(name: str, currentFilePath: str, data):
    dirPath = currentFilePath.split("\\")[:-1]
    filePath = "\\".join(dirPath) + "\\" + name + ".json"
    
    with open(filePath, "w") as file:
        file.write(json.dumps(data, indent=3))