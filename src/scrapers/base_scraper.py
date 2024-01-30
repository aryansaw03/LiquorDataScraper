import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class BaseScraper:
    def __init__(self, base_URL, output_file=None):
        self.base_URL = base_URL
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "excludeSwitches", ['enable-logging'])
        chrome_options.add_argument("--log-level=3")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        driver_path = os.path.join(
            os.path.dirname(__file__), 'driver', 'chromedriver.exe')
        service = Service(driver_path)
        self.driver = webdriver.Chrome(
            service=service, options=chrome_options)
        self.output_file = output_file if output_file == None or output_file.endswith(
            '.csv') else output_file + '.csv'

    def write_to_csv(self, data, headers):
        if self.output_file == None:
            return
        try:
            file_exists = os.path.isfile(self.output_file)
            with open(self.output_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(headers)
                writer.writerows(data)
        except Exception as e:
            print(f"Error writing to file: {e}")

    def open_webpage(self, URL):
        try:
            self.driver.get(URL)
            if "loudfare" in self.driver.title:
                print("blocked")
        except Exception as e:
            print(f"Error fetching URL {URL}: {e}")

    def cleanup(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def scrape(self):
        raise NotImplementedError("Scrape method not implemented")
