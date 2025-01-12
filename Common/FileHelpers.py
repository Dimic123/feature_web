import json, os

def WriteDataToJsonFileInCurrentDirectory(name: str, currentFilePath: str, data, mode="w"):
    dirPath = currentFilePath.split(os.sep)[:-1]
    filePath = os.path.join(os.sep.join(dirPath), name + ".json")
    
    with open(filePath, mode) as file:
        file.write(json.dumps(data, indent=3))
        file.write("\n")
        
def SaveToSharedDataDirectory(file_name, data):
    ROOT_DIR = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-1])
    shared_data_dir = os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "SharedData")

    if not os.path.exists(shared_data_dir):
        os.makedirs(shared_data_dir)

    file_path = os.path.join(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "SharedData"), file_name)
    with open(file_path, "w") as write_file:
        write_file.write(json.dumps(data, indent=3))
        
def ReadFileFromSharedDataDirectory(file_name):
    ROOT_DIR = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-1])
    file_path = os.path.join(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "SharedData"), file_name)
    try:
        read_file = open(file_path, "r")
        data = json.load(read_file)
        read_file.close()
        return data    
    except Exception as err:
        return []

def ReadFileFromStaticDataDirectory(file_name):
    ROOT_DIR = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-1])
    file_path = os.path.join(os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "StaticData"), file_name)
    try:
        read_file = open(file_path, "r")
        data = json.load(read_file)
        read_file.close()
        return data    
    except Exception as err:
        return []
    
def ReadTxtFile(file_path):
    with open(file_path) as f:
        return f.read().splitlines()
    
