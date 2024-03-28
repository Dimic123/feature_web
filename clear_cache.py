import os, shutil

currentDirectory = os.path.dirname(os.path.realpath(__file__))

def clear_cache():
    try:
        for root, subdirs, files in os.walk(currentDirectory):
            for d in subdirs:
                if d == "__pycache__":
                    shutil.rmtree(os.path.join(root, d))    
        print("Cache cleared")
    except Exception as ex:
        if hasattr(ex, 'message'):
            print(ex.message)
        else:
            print(ex)
            
clear_cache()
