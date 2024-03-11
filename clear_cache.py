import os, shutil

currentDirectory = os.path.dirname(os.path.realpath(__file__))

try:
    for root, subdirs, files in os.walk(currentDirectory):
        for d in subdirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
except Exception as ex:
    if hasattr(ex, 'message'):
        print(ex.message)
    else:
        print(ex)
        
print("Cache cleared")
