
# Liquor Data Scraper

## Project Overview

The `LiquorDataScraper` project is a comprehensive web scraping tool built in Python, utilizing Selenium WebDriver for automated interaction with web browsers. This project is designed to collect and aggregate data about various liquor products from multiple online liquor store websites.

Key Features:
- **Web Scraping with Selenium**: At the core of the project, Selenium WebDriver is employed for dynamic web scraping, allowing for automated navigation through web pages, interaction with web elements, and extraction of relevant data.
- **Targeted Scraping Scripts**: The project includes specific Python scripts tailored to scrape data from different online liquor stores. Each script is designed to handle the unique layout and structure of each website.
- **Data Extraction and Aggregation**: The primary goal is to extract detailed information about liquor products, such as names, prices, sizes, and other relevant attributes. This data is likely aggregated and stored, potentially in a structured format like CSV files.
- **Modular and Extensible**: The presence of a base scraper class suggests a modular design, where common functionalities are abstracted, facilitating the extension and maintenance of the scraper for various sources.

The `LiquorDataScraper` project is an example of a specialized web scraping application, focusing on the niche market of online liquor data. It demonstrates the use of Python and Selenium for efficiently collecting specific types of data from the web, addressing the challenges of different website structures and data formats.

## Installation and Setup

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies using the following command:
   ```
   pip install -r requirements.txt
   ```
3. Download the appropriate version of `chromedriver.exe` for your version of Chrome from [ChromeDriver - WebDriver for Chrome](https://googlechromelabs.github.io/chrome-for-testing/).
4. Place the `chromedriver.exe` in the `src/scrapers/driver` folder.

## Usage

[Include instructions on how to use the project, run the scrapers, etc.]
