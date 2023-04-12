import os
from Common.AppDriver import *
from Common.TestObject import TestObject
from Configuration.Settings import *

class MobileTestObject(TestObject):
    def __init__(self, testFilePath: str, driver = None) -> None:
        super().__init__()
        if driver is None:
            # Create options for app testing
            options = UiAutomator2Options()
            options.platformVersion = '10'
            # ADB device UDID
            options.udid = Settings.get("DeviceUDID", ( Sections.MOBILE ))
            # App .apk file
            options.app = os.path.abspath(Settings.get("AppPath", ( Sections.MOBILE ))) 
            server = Settings.get("Server", ( Sections.MOBILE ))
            
            self.driver = AppDriver(options, server)

        else:
            self.driver = driver

        self.file = testFilePath
        self.logger = self._TestObject__setupLogger()
  