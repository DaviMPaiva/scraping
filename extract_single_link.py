import csv
import json
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from scrap_class.scrap_master import ScrapMaster

def get_methods():
    methods = [method for method in dir(ScrapMaster) if callable(getattr(ScrapMaster, method)) and not method.startswith("__")]
    methods.sort()
    return methods

def write_row(url,writer):
    # Custom headers (if needed)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    # Call the function with the URL and headers
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        scraper = ScrapMaster(soup)

        results = []
        for method_name in methods:
            # Get the method object
            method = getattr(scraper, method_name)
            
            # Call the method and get its result
            result = method()

            if type(result) is str:
                result = result.replace('\n', '\\n')

            results.append(result)

        # Write method name and result to the CSV file
        writer.writerow(results)
        
        
with open('scraped_data_0_fim.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    
    methods = get_methods()

    # Write the header row
    writer.writerow(methods)

    with open('merged_list.json', 'r') as file:
        data = json.load(file)

    for url in tqdm(data[1800:], desc="Processing URLs"):
        try:
            write_row(url, writer)
        except:
            continue
   
    

