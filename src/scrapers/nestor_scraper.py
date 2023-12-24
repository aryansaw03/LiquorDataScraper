import re
from urllib.parse import urljoin
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_scraper import BaseScraper


class NestorScraper(BaseScraper):

    CATEGORIES = ['wine', 'spirits']

    def __init__(self, base_URL, output_file=None):
        super().__init__(base_URL, output_file)

    def scrape(self):
        product_data = []
        try:
            for category in self.CATEGORIES:
                self.open_webpage(
                    urljoin(self.base_URL, f'collections/{category}/'))
                while True:
                    print('Scraping from page:', self.driver.current_url)
                    products = self.driver.find_elements(
                        By.CLASS_NAME, 'product-item')
                    product_URLs = []
                    for product in products:
                        product_URLs.append(urljoin(self.base_URL, product.find_element(
                            By.CLASS_NAME, 'product-item__image-wrapper').get_attribute('href')))
                    original_URL = self.driver.current_url
                    for product_URL in product_URLs:
                        self.open_webpage(product_URL)
                        product_name = self.driver.find_element(
                            By.CLASS_NAME, "product-meta__title").text
                        try:
                            dropdown = Select(self.driver.find_element(
                                By.CLASS_NAME, 'product-form__single-selector'))
                            for option in dropdown.options:
                                dropdown.select_by_value(
                                    option.get_attribute('value'))
                                product_size = option.text
                                price_element = self.driver.find_element(
                                    By.CLASS_NAME, 'price')
                                price_text = re.search(
                                    r'\$\d+\.\d+', price_element.text).group()
                                product_price = float(
                                    price_text.replace('$', ''))
                                product_photo_URL = self.driver.find_element(
                                    By.CLASS_NAME, 'product-gallery__image').get_attribute('src')
                                product_data.append([
                                    product_name,
                                    product_size,
                                    product_price,
                                    category,
                                    product_URL,
                                    product_photo_URL
                                ])
                        except NoSuchElementException:
                            price_element = self.driver.find_element(
                                By.CLASS_NAME, 'price')
                            price_text = re.search(
                                r'\$\d+\.\d+', price_element.text).group()
                            product_price = float(price_text.replace('$', ''))
                            product_photo_URL = self.driver.find_element(
                                By.CLASS_NAME, 'product-gallery__image').get_attribute('src')
                            product_data.append([
                                product_name,
                                product_size,
                                product_price,
                                category,
                                product_URL,
                                product_photo_URL
                            ])
                    self.open_webpage(original_URL)
                    try:
                        next_button = self.driver.find_element(
                            By.CLASS_NAME, 'pagination__next')
                        next_URL = urljoin(
                            self.base_URL, next_button.get_attribute("href"))
                        self.open_webpage(next_URL)
                    except NoSuchElementException:
                        break
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            self.cleanup()
            self.write_to_csv(
                product_data, ['name', 'size', 'price', 'category', 'URL', 'photoURL'])
        return product_data
