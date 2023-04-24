from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_footer_links(driver, params: dict) -> None:
    site = params["site"]
    expectedLinks = params["links"]

    driver.get(site)

    result = True

    for xpath, link in expectedLinks.items():
        result &= checkLink(driver, xpath, link)

    assert result, "Not all links are correct for site " + site

def checkLink(driver, xpath, expectedLink) -> bool:
    print("Expected link: \"" + expectedLink + "\"")

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    link = element.get_attribute('innerHTML') 

    print("Actual link: \"" + link + "\"")
    return link == expectedLink