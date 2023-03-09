from enum import Enum
import os
from datetime import datetime


class Environment(Enum):
    Web = 1,
    Mobile = 2

class Logger:
    def __init__(self) -> None:
            pass
    
    log_folder = "./Logs"

    @classmethod
    def Log(cls, *values: str, source: str, type: Environment, console: bool) -> None:
        msg = " ".join(values)

        if console:
            print(msg)

        logFolder = cls.log_folder
        if type is Environment.Web:
            logFolder = os.path.join(logFolder, "Web")
        elif type is Environment.Mobile:
            logFolder = os.path.join(logFolder, "Mobile")

        if not os.path.exists(logFolder):
            os.makedirs(logFolder)

        logFile = os.path.join(logFolder, source + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S.log"))

        with open(logFile, "a+") as file:
            file.write(msg)
