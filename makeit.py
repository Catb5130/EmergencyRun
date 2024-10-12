#Workplace: //li[@class='icon--before']/span/strong[text()='Workplace:']/following-sibling::text()[1]
#//strong[text()='Questions and applications to:']/following-sibling::text()[1]
#//strong[text()='Contact person:']/following-sibling::text()[1]
#//p[contains(@class, 'additional__item--link')]/a[starts-with(@href, 'tel:')]/font/font/text()

from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import os
import pandas as pd

# Chrome Options for headless mode
chrome_options = webdriver.ChromeOptions()
# Remove headless mode for debugging
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=chrome_options)

base_url = "https://www.make-it-in-germany.com/en/working-in-germany/job-listings?tx_solr%5Bq%5D=&%5Bfilter%5D%5B%5D=&%5Bfilter%5D%5B%5D=#filter45536"

# Check if 'make-it-in-germany.com.py.csv' exists
csv_file_path = 'make-it-in-germany.com.py.csv'
file_exists = os.path.exists(csv_file_path)

# Read existing data from CSV file
existing_data = pd.read_csv(csv_file_path) if file_exists else pd.DataFrame()

# Loop through pages 2 to 10
for page_num in range(0, 20):
    # Navigate to the page
    driver.get(f"{base_url}&page={page_num}")
    # Increase sleep time to 10 seconds or more
    time.sleep(10)

    # Extract hrefs from job listings
    job_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/job-listings/job/job-')]")
    hrefs = [job.get_attribute('href') for job in job_links]

    # For each href, navigate and extract email
    data = []
    for index, href in enumerate(hrefs, 1):
        try:
            driver.get(href)
            # Increase sleep time to 10 seconds or more
            time.sleep(10)
            email_element = driver.find_element(By.XPATH, "//strong[text()='E-mail:']/../a")
            email_display_text = email_element.text
            data.append({'URL': href, 'Email': email_display_text})
            print(f"Page {page_num}: Processed {index}/{len(hrefs)}. Found email: {email_display_text}")
        except Exception as e:
            data.append({'URL': href, 'Email': 'No email found'})
            print(f"Page {page_num}: Processed {index}/{len(hrefs)}. No email found. Exception: {e}")

    # Combine existing data and new data
    combined_data = pd.concat([existing_data, pd.DataFrame(data)], ignore_index=True)

    # Save to CSV file
    combined_data.to_csv(csv_file_path, index=False)

driver.quit()
print(f"Data saved to {csv_file_path}!")

