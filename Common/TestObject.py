import os
from abc import abstractmethod
from selenium import webdriver
from Common.JsonHelpers import ImportJsonFile
from Common.Logging import *
import logging
from datetime import datetime


class TestObject:
    def __init__(self, driver, testFilePath: str) -> None:
        self.driver = driver
        self.file = testFilePath
        self.logger = self.__setupLogger()

    def __setupLogger(self, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        logFile = os.path.join(os.path.dirname(self.file), os.path.splitext(os.path.basename(self.file))[0] + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S.log"))

        fileHandler = logging.FileHandler(logFile)
        fileHandler.setFormatter(formatter)

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger = logging.getLogger(self.file)
        logger.setLevel(level)
        logger.addHandler(fileHandler)
        logger.addHandler(handler)

        return logger

    def RunTest(self) -> bool:
        scriptFilename = os.path.splitext(os.path.basename(self.file))[0]
        returnValue = False

        self.logger.info("Started " + scriptFilename + " test suite...")

        currentDir = os.path.dirname(os.path.realpath(self.file))
        data = ImportJsonFile(os.path.join(
            currentDir, scriptFilename + ".json"))

        for case in data:
            testValue = False
            try:
                testValue = self.Test(data[case])
            except Exception as ex:
                self.logger.exception(str(ex))

            returnValue &= testValue
            if testValue:
                self.logger.info("Test case " + case + " passed")
            else:
                self.logger.error("Test case " + case + " failed")
                

        return returnValue

    @abstractmethod
    def Test(self, data: dict) -> bool:
        raise NotImplementedError("Must override method")