import configparser
from enum import Enum


class Sections(Enum):
    WEB = 1,
    MOBILE = 2,
    API = 3


class Settings:
    __conf = None

    @staticmethod
    def get(name, *types: Sections):
        if Settings.__conf is None:  # Read only once, lazy.
            Settings.__conf = configparser.ConfigParser()
            Settings.__conf.read('./Configuration/Config.ini')

        sections = ["COMMON"]

        for s in types:
            sections.append(str(s.name))

        for section in Settings.__conf.sections():
            if len(types) > 0 and section not in sections:
                continue

            if name in Settings.__conf[section]:
                return Settings.__conf[section][name]

        return None

    @staticmethod
    def set(name, value):
        # if name in Settings.__setters:
        #   Settings.__conf[name] = value
        # else:
        #   raise NameError("Name not accepted in set() method")
        raise NotImplementedError
