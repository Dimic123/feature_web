# Requirement: Add _sap_ids_sample.txt in the same directory.
#   Txt file should contain one or more sapIds, each separated by newline.

# Run this file to generate GetManualsAuidsLangTest.json file, which can then be used for python test

import os, sys

projectRootPath = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-5])
sys.path.append(projectRootPath)

from Common.FileHelpers import GenerateTestCasesJsonFile

def GenerateJsonTestCasesFromSapIdsExample():
    readFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_sap_ids_sample.txt")
    writeFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "GetManualsAuidsLangTest.json")
    
    f2 = open(readFilePath, "r")
    f2.seek(0, os.SEEK_END)
    eof = f2.tell()
    f2.seek(0, os.SEEK_SET)
    
    testCases = []
    while f2.tell() != eof:
        line = f2.readline().strip()
        if line != "":
            testCases.append({
                "auids": [line],
                "lang": "en"
            })
        
    GenerateTestCasesJsonFile(testCases, writeFilePath)
    print("Json file generated: " + writeFilePath)
        
GenerateJsonTestCasesFromSapIdsExample()
