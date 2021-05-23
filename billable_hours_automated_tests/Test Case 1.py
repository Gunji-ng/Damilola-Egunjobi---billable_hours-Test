# Automated test to verify that User can successfully get the invoice for a particular company after parsing timetable with correct data.

from appium import webdriver

device_id = "5203a695f02c93dd"
app_path = "C:\\Users\\Gunji\\Downloads\\app-armeabi-v7a-release.apk"

desired_cap = {
    "deviceName": device_id,
    "platformName": "Android",
    "app": app_path,
    "autoGrantPermissions": "true"
}

target_file_path = "/storage/emulated/0/Download/Proper_data.csv"

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

# Verify Parse Results page is opened, parsed successfully message is displayed and correct Invoice values are displayed
driver.implicitly_wait(3)
parse_results_page = driver.find_element_by_xpath("//*[contains(@text,'Parse Results')]")
parsed_successfully_message = driver.find_element_by_xpath("//*[contains(@text,'parsed successfully')]")
google_invoice_value = driver.find_element_by_xpath(
    "//android.view.View[@text='Google']/following-sibling::android.view.View[1]")
facebook_invoice_value = driver.find_element_by_xpath(
    "//android.view.View[@text='Facebook']/following-sibling::android.view.View[1]")
preceding_page_icon = driver.find_element_by_xpath("//android.widget.Button[@text='Back']")

expected_invoice_value_google = "N3200.00"
expected_invoice_value_facebook = "N1100.00"

assert parse_results_page.is_displayed(), "Parse Results page is not displayed"
assert parsed_successfully_message.is_displayed(), "Parsed successfully message is not displayed"
assert google_invoice_value.text == expected_invoice_value_google, "Invoice value for Google is incorrect"
assert facebook_invoice_value.text == expected_invoice_value_facebook, "Invoice value for Facebook is incorrect"
assert preceding_page_icon.is_displayed(), "Preceding page icon is not displayed"

# Click on a company's name in the table
google_link_in_table = driver.find_element_by_xpath("//android.view.View[@text='Google']")
google_link_in_table.click()

# Verify Company's name as a header is displayed and that table showing the invoice breakdown has the expected headers
google_as_a_header = driver.find_element_by_xpath("//android.view.View[@text='Google']")
employee_id_table_header = driver.find_element_by_xpath("//android.view.View[@text='Employee ID']")
number_of_hours_table_header = driver.find_element_by_xpath("//android.view.View[@text='Number of Hours']")
unit_price_table_header = driver.find_element_by_xpath("//android.view.View[@text='Unit Price']")
cost_table_header = driver.find_element_by_xpath("//android.view.View[@text='Cost']")
previous_activity_button = driver.find_element_by_xpath("//android.widget.ImageView[2]")

assert google_as_a_header.is_displayed(), "Company name as a header is not displayed"
assert employee_id_table_header.is_displayed(), "Employee ID table header is not displayed"
assert number_of_hours_table_header.is_displayed(), "Number of Hours table header is not displayed"
assert unit_price_table_header.is_displayed(), "Unit Price table header is not displayed"
assert cost_table_header.is_displayed(), "Cost table header is not displayed"
assert previous_activity_button.is_displayed(), "Previous activity button is not displayed"

driver.quit()
