from selenium import webdriver

# create a new Firefox browser instance
browser = webdriver.Firefox()

# navigate to the website to be checked
browser.get("https://si.hisense.com")

# get the website title and print it to the console
title = browser.title
print("The website title is:", title)

# close the browser window
browser.quit()
