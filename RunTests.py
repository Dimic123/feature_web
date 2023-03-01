from time import sleep
from appium import webdriver as appdriver
from Common.MobileHelpers import *
from Mobile.AppDriver import *
from Web.Live.CheckingSiteTitle import *
from Web.Live.LoginTest import *
import json

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

test_cases = {
	"site_title_1": {
		"site" : "https://si.gorenje.com/",
		"title" : "Gorenje | Domača Stran"
	},
	"site_title_1": {
		"site" : "https://si.gorenje.com/",
		"title" : "Gorenje | Veliki in mali gospodinjski aparati"
	}
}

login_values = {
	"usernamePath" : '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[1]/div[1]/div/div/input',
    "passwordPath" : '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[1]/div[2]/div[1]/div/input',
    "submitPath" : '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[2]/div/div[2]/button',
    "username" : "jedan70743@wireps.com",
    "password" : "gA5Z5KJxTLsb@u"
}

test_cases2 = {
	"login_1": {
		"site" : "https://si.gorenje.com/login",
		"values" : login_values
	}
}

def main():
	# TestWeb()
	TestMobile()

def TestWeb():
	for case in test_cases:
		site = test_cases[case]["site"]
		title = test_cases[case]["title"]
		CheckingSiteTitle(site, title)
		print("Test case", case, "passed")

	for case in test_cases2:
		site = test_cases2[case]["site"]
		values = test_cases2[case]["values"]
		LoginTest(site, values)
		print("Test case", case, "passed")

def TestMobile():
	# Create options for app testing
	options = UiAutomator2Options()
	options.platformVersion = '10'
	# ADB device UDID
	options.udid = 'R3CT309J26M'
	# App .apk file
	options.app = os.path.abspath(r'.\Mobile\Apps\ConnectLife_1.3.0prod_12300222.apk') 
	server = 'http://127.0.0.1:4723/wd/hub'

	with AppDriver(options, server) as driver:
		# app.TouchButton('//android.widget.Button[@content-desc="NEXT"]')
		# app.driver.swipe(850, 1200, 180, 1200, 400)

		# Press next
		actions = ActionChains(driver)
		actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
		actions.w3c_actions.pointer_action.move_to_location(891, 2093)
		actions.w3c_actions.pointer_action.pointer_down()
		actions.w3c_actions.pointer_action.pause(0.1)
		actions.w3c_actions.pointer_action.release()
		actions.perform()

		sleep(0.5)

		# Press next
		actions = ActionChains(driver)
		actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
		actions.w3c_actions.pointer_action.move_to_location(888, 2088)
		actions.w3c_actions.pointer_action.pointer_down()
		actions.w3c_actions.pointer_action.pause(0.1)
		actions.w3c_actions.pointer_action.release()
		actions.perform()
			
		sleep(0.5)

		# Press next
		actions = ActionChains(driver)
		actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
		actions.w3c_actions.pointer_action.move_to_location(888, 2088)
		actions.w3c_actions.pointer_action.pointer_down()
		actions.w3c_actions.pointer_action.pause(0.1)
		actions.w3c_actions.pointer_action.release()
		actions.perform()

		sleep(0.5)

		# Press sign in	
		actions = ActionChains(driver)
		actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
		actions.w3c_actions.pointer_action.move_to_location(591, 1977)
		actions.w3c_actions.pointer_action.pointer_down()
		actions.w3c_actions.pointer_action.pause(0.1)
		actions.w3c_actions.pointer_action.release()
		actions.perform()

		sleep(0.5)
		
		location = CheckLocation(driver, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.Button[1]')

		sleep(0.5)

		# Login
		try:
			el1 = driver.find_element(by=AppiumBy.ID, value="com.hisense.juconnect.connectlife:id/sign_email")
			el1.send_keys("test5@connectlife.io")
			el2 = driver.find_element(by=AppiumBy.ID, value="com.hisense.juconnect.connectlife:id/sign_password")
			el2.send_keys("test1234")
			actions = ActionChains(driver)
			actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
			actions.w3c_actions.pointer_action.move_to_location(528, 1758)
			actions.w3c_actions.pointer_action.pointer_down()
			actions.w3c_actions.pointer_action.pause(0.1)
			actions.w3c_actions.pointer_action.release()
			actions.perform()
				
		except:
			pass

		sleep(1)

		if not location:
			CheckLocation(driver, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.Button[1]')
		else:
			# Device location
			actions = ActionChains(driver)
			actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
			actions.w3c_actions.pointer_action.move_to_location(536, 1720)
			actions.w3c_actions.pointer_action.pointer_down()
			actions.w3c_actions.pointer_action.pause(0.1)
			actions.w3c_actions.pointer_action.release()
			actions.perform()
			
		sleep(0.5)
		# Drag
		actions = ActionChains(driver)
		actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
		actions.w3c_actions.pointer_action.move_to_location(571, 577)
		actions.w3c_actions.pointer_action.pointer_down()
		actions.w3c_actions.pointer_action.move_to_location(582, 1463)
		actions.w3c_actions.pointer_action.release()
		actions.perform()

		sleep(0.5)
		# Drag	
		actions = ActionChains(driver)
		actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
		actions.w3c_actions.pointer_action.move_to_location(530, 1810)
		actions.w3c_actions.pointer_action.pointer_down()
		actions.w3c_actions.pointer_action.move_to_location(536, 457)
		actions.w3c_actions.pointer_action.release()
		actions.perform()
		
		sleep(0.5)

		# Drag
		actions = ActionChains(driver)
		actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
		actions.w3c_actions.pointer_action.move_to_location(440, 1908)
		actions.w3c_actions.pointer_action.pointer_down()
		actions.w3c_actions.pointer_action.move_to_location(511, 159)
		actions.w3c_actions.pointer_action.release()
		actions.perform()
			
		sleep(0.5)

		# Drag
		actions = ActionChains(driver)
		actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
		actions.w3c_actions.pointer_action.move_to_location(544, 1908)
		actions.w3c_actions.pointer_action.pointer_down()
		actions.w3c_actions.pointer_action.move_to_location(509, 771)
		actions.w3c_actions.pointer_action.release()
		actions.perform()
		

	
if __name__ == "__main__":
	main()