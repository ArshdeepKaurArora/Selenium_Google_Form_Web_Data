from search_zillow import ZillowData
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC

# object of class required for the project
zillow_data = ZillowData()

# Get the data of zillow from webfile
zillow_data.get_data()
data_links = zillow_data.get_links()
home_address_list = zillow_data.get_home_address()
price_list = zillow_data.get_price()

# upload the data of each rental home from zillow to the Google form.

google_form_url = 'YOUR GOOGLE FORM LINK'
driver = webdriver.Chrome(executable_path=zillow_data.drive_path)
driver.get(url=google_form_url)
short_time = ui.WebDriverWait(driver,20)
long_time = ui.WebDriverWait(driver,50)

for i in range(len(price_list)):
    # Fill home address
    long_time.until(EC.presence_of_all_elements_located((By.XPATH,'//input[@class="whsOnd zHQkBf"]')))
    home_address_input = driver.find_elements(By.XPATH,'//input[@class="whsOnd zHQkBf"]')[0]
    home_address_input.send_keys(home_address_list[i])

    # Fill price per month
    price_input = driver.find_elements(By.XPATH,'//input[@class="whsOnd zHQkBf"]')[1]
    price_input.send_keys(price_list[i])

    # Rental home link
    link_input = driver.find_elements(By.XPATH,'//input[@class="whsOnd zHQkBf"]')[2]
    link_input.send_keys(data_links[i])

    # Submit the form
    short_time.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@role="button"]')))
    submit_button = driver.find_elements(By.XPATH,'//div[@role="button"]')[0]
    submit_button.click()

    # submit another response
    short_time.until(EC.presence_of_all_elements_located((By.XPATH, '//a[text()="Submit another response"]')))
    another_response_button = driver.find_element(By.XPATH,'//a[text()="Submit another response"]')
    another_response_button.click()


