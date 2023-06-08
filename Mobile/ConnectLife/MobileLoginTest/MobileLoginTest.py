from appium import webdriver as appdriver
from Common.MobileHelpers import *

from time import sleep

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


class TestLogin():
    def test_main(self, driver, params: dict) -> None:
        self.step_skip(driver, params)

        # Press sign in
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(591, 1977)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        sleep(0.5)

        location = CheckLocation(
            driver, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.Button[1]')

        sleep(0.5)

        self.step_login(driver, params)

        if not location:
            CheckLocation(
                driver, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.Button[1]')
        else:
            # Device location
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(
                driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(536, 1720)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        sleep(0.5)

        self.step_move(driver, params)

        Screenshot(driver, "./Mobile/Screenshots")

        homeBtn = driver.find_element(
            by=AppiumBy.XPATH, value='//android.view.View[@content-desc="Home"]')

        assert homeBtn

    def step_skip(self, driver, params: dict) -> None:
        # Press next
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(891, 2093)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        sleep(0.5)

        # Press next
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(888, 2088)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        sleep(0.5)

        # Press next
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(888, 2088)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        sleep(0.5)

    def step_login(self, driver, params: dict) -> None:
        # Login
        el1 = driver.find_element(by=AppiumBy.ID, value=params["username_id"])
        el1.send_keys(params["username"])
        el2 = driver.find_element(by=AppiumBy.ID, value=params["password_id"])
        el2.send_keys(params["password"])
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(528, 1758)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        sleep(1)

    def step_move(self, driver, params: dict) -> None:
        # Drag
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(571, 577)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(582, 1463)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        sleep(0.5)
        # Drag
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(530, 1810)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(536, 457)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        sleep(0.5)

        # Drag
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(440, 1908)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(511, 159)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        sleep(0.5)

        # Drag
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(
            driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(544, 1908)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(509, 771)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
