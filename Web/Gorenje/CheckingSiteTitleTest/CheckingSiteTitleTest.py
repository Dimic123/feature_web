
from Common.Logging import *
from Configuration.Settings import Settings

def test_title(driver, params: dict) -> None:
    site = params["site"]
    expectedTitle = params["title"]

    print("\nChecking site title for site: " + site)
    print("Expected title: \"" + expectedTitle + "\"")

    driver.get(site)

    title = driver.title

    print("Actual title: \"" + title + "\"")
    assert title == expectedTitle


