import json
import keyboard
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import re

# Set Chrome options to configure the browser
chrome_options = webdriver.ChromeOptions()

# Set the window size
chrome_options.add_argument("--window-size=1024,720")  # Change dimensions as needed

# Specify the user agent
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

# Instantiate the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

def click_button(driver, url):
    # Open the URL
    driver.get(url)
    # Click the button
    button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-ds-component='DS-Button' and @aria-label='Ativar visualização em grade']"))
    )
    button.click()

def get_results(driver):
    # Find the <p> element containing the value
    element = driver.find_element(By.CSS_SELECTOR, "p[data-ds-component='DS-Text'].olx-text.olx-text--body-small.olx-text--block.olx-text--regular.olx-color-neutral-110")
    value = element.text

    pattern = r"\d+(?=\sresultados$)"

    # Use re.search to find the pattern in the string
    match = re.search(pattern, value)
    results = int(match[0])
    print(results)
    return results

def find_links(driver):
    # Find all the <a> elements with the specified type
    elements = driver.find_elements(By.CSS_SELECTOR, "a[data-ds-component='DS-NewAdCard-Link']")
    # Extract href attributes
    hrefs = [element.get_attribute("href") for element in elements]
    return hrefs

stop_flag = False
# Function to stop the loop gracefully
def stop_execution():
    global stop_flag 
    stop_flag = True
    print("Stopping execution...", stop_flag)

# Set the hotkey for stopping execution
keyboard.add_hotkey('f', stop_execution)

all_links = []
# Define the URL
url = f"https://www.olx.com.br/imoveis/venda/estado-pe/grande-recife/recife?o={1}"

click_button(driver, url)

all_links = all_links + find_links(driver)

flag_continue = True

min_v = 300000
max_v = 300000
jump = 20000
results = 0
min_v = max_v
try:
    while (len(all_links)/2) < 80000 and not stop_flag:
        min_v = max_v
        max_v += jump
        string_found = False
        if flag_continue:
            page = 13
            flag_continue = False
        else:
            page = 1
        while not string_found and not stop_flag:
            url = f"https://www.olx.com.br/imoveis/venda/estado-pe/grande-recife/recife?pe={max_v}&ps={min_v}&o={page}"
            print("trying tor reach: ", url)
            try:
                driver.get(url)
                # Check if the string is present
                if "Ops! Nenhum anúncio foi encontrado." in driver.page_source:
                    string_found = True
                else:
                    all_links = all_links + find_links(driver)
                    
                    page += 1

                    print("total links found: ", len(all_links)/2)
            except Exception as e:
                # Code to handle other types of exceptions
                print("An error occurred:", e)
                string_found = False

except Exception as e:
    print("An error occurred:", e)

# Close the WebDriver
driver.quit()

# Remove duplicates from the single list
single_list_no_duplicates = list(set(all_links))

json_string = json.dumps(single_list_no_duplicates)
file_path = "links4.json"
# Write JSON string to file
with open(file_path, "w") as json_file:
    json_file.write(json_string)

print("Links saved to JSON file successfully!")
print(f"the the last search value was: {min_v} {max_v}")