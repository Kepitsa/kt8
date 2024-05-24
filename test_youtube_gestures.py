import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

capabilities = {
    "platformName": "Android",
    "appium:deviceName": "Android Emulator",
    "appium:appPackage": "com.google.android.youtube",
    "appium:appActivity": "com.google.android.apps.youtube.app.WatchWhileActivity",
    "appium:automationName": "UiAutomator2",
    "appium:noReset": True
}

appium_server_url = 'http://127.0.0.1:4723'

class YouTubeGestureTests(unittest.TestCase):
    def setUp(self) -> None:
        options = UiAutomator2Options().load_capabilities(capabilities)
        self.driver = webdriver.Remote(appium_server_url, options=options)
        time.sleep(6)
        current_activity = self.driver.current_activity
        print(f"Current activity: {current_activity}")

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_tap(self) -> None:
        wait = WebDriverWait(self.driver, 20)
      
        search_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Search']")))
        search_button.click()

        search_input = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.google.android.youtube:id/search_edit_text")))
        search_input.send_keys('test video')

        search_type_icon = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.google.android.youtube:id/search_type_icon")))
        search_type_icon.click()

        all_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.TextView[@text='All']")))
        all_button.click()
  
        first_video = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='TEST VIDEO - 18 seconds - Go to channel - Simon Yapp - 1.1M views - 17 years ago - play video']")))
        first_video.click()

        self.driver.save_screenshot('screenshot_tap.png')
        time.sleep(5)

        home_button = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Home')))
        home_button.click()

    def test_long_press(self) -> None:
        wait = WebDriverWait(self.driver, 20)

        explore_menu_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='Explore Menu']")))
        explore_menu_button.click()
        time.sleep(2)

        trending_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//android.view.ViewGroup[@content-desc='Trending']")))
        self.driver.execute_script('mobile: longClickGesture', {'elementId': trending_button.id})
        self.driver.save_screenshot('screenshot_long_press.png')


        navigate_up_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='Navigate up']")))
        navigate_up_button.click()

    def test_swipe(self) -> None:
        wait = WebDriverWait(self.driver, 20)

        self.driver.execute_script("mobile: swipeGesture", {
            'left': 500, 'top': 1500,
            'width': 500, 'height': 1500,
            'direction': 'up', 'percent': 0.75
        })
        time.sleep(2)

        self.driver.execute_script("mobile: swipeGesture", {
            'left': 500, 'top': 500,
            'width': 500, 'height': 1500,
            'direction': 'down', 'percent': 0.75
        })
        home_button = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Home')))
        library_button = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Library')))
        self.driver.execute_script("mobile: swipeGesture", {
            'left': home_button.location['x'], 'top': home_button.location['y'],
            'width': library_button.location['x'] - home_button.location['x'],
            'height': library_button.location['y'] - home_button.location['y'],
            'direction': 'up', 'percent': 0.75
        })
        self.driver.save_screenshot('screenshot_swipe.png')

    def test_scroll(self) -> None:

        self.driver.execute_script("mobile: scrollGesture", {
            'left': 100, 'top': 500, 'width': 800, 'height': 1000,
            'direction': 'down', 'percent': 3.0
        })
        self.driver.save_screenshot('screenshot_scroll.png')

    def test_pinch(self) -> None:
        wait = WebDriverWait(self.driver, 20)

        player_container = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//android.view.View[@resource-id='com.google.android.youtube:id/player_container']")))
        self.driver.execute_script("mobile: pinchCloseGesture", {
            'elementId': player_container.id,
            'percent': 0.75
        })
        self.driver.save_screenshot('screenshot_pinch.png')

if __name__ == '__main__':
    unittest.main()
