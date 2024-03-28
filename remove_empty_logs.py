import os, shutil

currentDirectory = os.path.dirname(os.path.realpath(__file__))

def remove_empty_logs():
    try:
        for root, subdirs, files in os.walk(os.path.join(currentDirectory, "report_logs")):
            for f in files:
                file_path = os.path.join(root, f)

                opened_file = open(file_path, "r")
                lines = opened_file.readlines()
                opened_file.close()
                if len(lines) <= 1:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
    except Exception as ex:
        if hasattr(ex, 'message'):
            print(ex.message)
        else:
            print(ex)
            
remove_empty_logs()
