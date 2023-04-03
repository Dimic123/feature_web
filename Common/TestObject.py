import os
from abc import abstractmethod
from selenium import webdriver
from Common.JsonHelpers import ImportJsonFile
from Common.Logging import *
import logging
from datetime import datetime

from Configuration.Settings import Settings


class TestObject:
    def __init__(self, testFilePath: str, driver = None) -> None:
        if driver is None:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--headless')
            driver = Settings.get("Driver")  
            if driver == "Chrome":
                self.driver = webdriver.Chrome(options=options)
            else:
                raise NotImplementedError
        else:
            self.driver = driver

        self.file = testFilePath
        self.logger = self.__setupLogger()

    def __setupLogger(self, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        logFolder = Settings.get("LogFolder")
        if not logFolder:
            logFolder = os.path.dirname(self.file)
        elif not os.path.exists():
            os.makedirs(logFolder)

        logFile = os.path.join(logFolder, os.path.splitext(
            os.path.basename(self.file))[0] + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S.log"))

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

        self.logger.info("Started " + scriptFilename + " test suite...")

        currentDir = os.path.dirname(os.path.realpath(self.file))
        data = ImportJsonFile(os.path.join(
            currentDir, scriptFilename + ".json"))

        passed = 0
        failed = 0

        for case in data:
            testValue = False
            try:
                testValue = self.Test(data[case])
            except Exception as ex:
                self.logger.exception(str(ex))

            if testValue:
                self.logger.info("Test case " + case + " passed")
                passed += 1
            else:
                self.logger.error("Test case " + case + " failed")
                failed += 1

        self.logger.info("")

        self.driver.quit()
        self.logger.info(scriptFilename + " tests complete, passed: " + str(passed)+", failed:" + str(failed) + ", total: " + str(len(data)))
        return {"passed": passed, "failed": failed, "total": len(data)}

    @abstractmethod
    def Test(self, data: dict) -> bool:
        raise NotImplementedError("Must override method")
