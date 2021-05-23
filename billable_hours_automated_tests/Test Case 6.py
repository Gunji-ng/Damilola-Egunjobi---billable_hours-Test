# Automated test to verify that User should not be able to successfully parse timetable when any Employee ID data is missing.

from appium import webdriver

device_id = "5203a695f02c93dd"
app_path = "C:\\Users\\Gunji\\Downloads\\app-armeabi-v7a-release.apk"

desired_cap = {
    "deviceName": device_id,
    "platformName": "Android",
    "app": app_path,
    "autoGrantPermissions": "true"
}

target_file_path = "/storage/emulated/0/Download/Missing_Employee_ID_data.csv"

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
driver.implicitly_wait(30)

# Verify app is launched, file path Textbox and Continue button are displayed
home_page = driver.find_element_by_xpath("//android.view.View[@text='Billable Hours']")
file_path_textbox = driver.find_element_by_class_name("android.widget.EditText")
continue_button = driver.find_element_by_xpath("//*[contains(@text,'Continue')]")

assert home_page.is_displayed(), "Home page is not displayed"
assert file_path_textbox.is_displayed(), "File path Textbox is not displayed"
assert continue_button.is_displayed(), "Continue button is not displayed"

# Set file path and click Continue
file_path_textbox.click()
file_path_textbox.clear()
driver.implicitly_wait(2)
driver.execute_script("mobile: type", {"text": target_file_path})

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
