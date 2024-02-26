import os, shutil

filePath = os.path.realpath(__file__)

currDir = filePath.split("\\")[:-1]
currDir = "\\".join(currDir)

try:
    for root, subdirs, files in os.walk(currDir):
        for d in subdirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
except Exception as ex:
    if hasattr(ex, 'message'):
        print(ex.message)
    else:
        print(ex)
        
print("Cache cleared")
