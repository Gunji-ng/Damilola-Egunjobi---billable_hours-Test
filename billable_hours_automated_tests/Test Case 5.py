# Automated test to verify that User should not be able to successfully parse timetable when any Time data is missing.
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains

device_id = "emulator-5554"
app_path = "C:\\Users\\Gunji\\Downloads\\app-armeabi-v7a-release.apk"

desired_cap = {
    "deviceName": device_id,
    "platformName": "Android",
    "app": app_path,
    "autoGrantPermissions": "true"
}

start_time_data_path = "/storage/emulated/0/Download/Missing_Start_Time_data.csv"
end_time_data_path = "/storage/emulated/0/Download/Missing_End_Time_data.csv"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
driver.implicitly_wait(30)

# Verify app is launched, file path Textbox and Continue button are displayed
home_page = driver.find_element_by_xpath("//android.view.View[@text='Billable Hours']")
file_path_textbox = driver.find_element_by_xpath("//android.widget.EditText[1]")
continue_button = driver.find_element_by_xpath("//*[contains(@text,'Continue')]")

assert home_page.is_displayed(), "Home page is not displayed"
assert file_path_textbox.is_displayed(), "File path Textbox is not displayed"
assert continue_button.is_displayed(), "Continue button is not displayed"

# Set file path and click Continue
file_path_textbox.click()
file_path_textbox.clear()
driver.execute_script("mobile: type", {"text": start_time_data_path})

continue_button.click()

# Verify Parse Results page is opened, parsed successfully message is displayed and correct Invoice values are displayed
driver.implicitly_wait(3)

try:
    parse_results_page = driver.find_element_by_xpath("//*[contains(@text,'Parse Results')]")
except:
    parse_results_page = None

try:
    parsed_successfully_message = driver.find_element_by_xpath("//*[contains(@text,'parsed successfully')]")
except:
    parsed_successfully_message = None

assert parse_results_page == None, "Parse Results page is displayed"
assert parsed_successfully_message == None, "Parsed successfully message is displayed"
assert home_page.is_displayed(), "Home page is not displayed"

# Clear the file path textbox, set file path to end_time_data_path and click Continue
file_path_textbox.click()
driver.implicitly_wait(2)
actions = TouchAction(driver)
actions.long_press(file_path_textbox).release()
actions.perform()
driver.implicitly_wait(5)
select_all_button = driver.find_element_by_xpath("//android.widget.Button[@text='SELECT ALL']")
select_all_button.click()
driver.press_keycode(67)
driver.implicitly_wait(2)
driver.execute_script("mobile: type", {"text": end_time_data_path})

continue_button.click()

# Verify Parse Results page is not opened, parsed successfully message is not displayed and app remains on homepage
driver.implicitly_wait(3)

try:
    parse_results_page = driver.find_element_by_xpath("//*[contains(@text,'Parse Results')]")
except:
    parse_results_page = None

try:
    parsed_successfully_message = driver.find_element_by_xpath("//*[contains(@text,'parsed successfully')]")
except:
    parsed_successfully_message = None

assert parse_results_page == None, "Parse Results page is displayed"
assert parsed_successfully_message == None, "Parsed successfully message is displayed"
assert home_page.is_displayed(), "Home page is not displayed"

driver.quit()
