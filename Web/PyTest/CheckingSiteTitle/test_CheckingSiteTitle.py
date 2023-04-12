
from Common.Logging import *
from Configuration.Settings import Settings
from Common.TestObject import *

def test_title(driver, data: dict) -> None:
    site = data["site"]
    expectedTitle = data["title"]

    print("\nChecking site title for site: " + site)
    print("Expected title: \"" + expectedTitle + "\"")

    driver.get(site)

    title = driver.title

    print("Actual title: \"" + title + "\"")
    assert title == expectedTitle


