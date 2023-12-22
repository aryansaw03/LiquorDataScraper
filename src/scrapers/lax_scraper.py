import time
from base_scraper import BaseScraper
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse
from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class LaxScraper(BaseScraper):

    CATEGORIES = ['wine', 'beer', 'spirits']
    CATEGORY_URL_SEGMENTS = ['wines/', 'beer/', 'spirits/']

    def __init__(self, base_URL, output_file=None):
        super().__init__(base_URL, output_file)

    def scrape(self):
        product_data = []
        try:
            for category, category_URL_segment in zip(self.CATEGORIES, self.CATEGORY_URL_SEGMENTS):
                self.open_webpage(
                    urljoin(self.base_URL, category_URL_segment))
                while True:
                    print('Scraping from page:', self.driver.current_url)
                    products = self.driver.find_elements(
                        By.CSS_SELECTOR, '.product-list > *')
                    for product in products:
                        title_element = product.find_element(
                            By.CLASS_NAME, "rebl15")
                        try:
                            size_element = title_element.find_element(
                                By.TAG_NAME, 'span')
                            product_name = title_element.text.replace(
                            size_element.text, '').strip()
                            product_size = size_element.text.strip('()')
                        except NoSuchElementException:
                            product_name = title_element.text
                            product_size = None
                        
                        price_element = product.find_element(
                            By.CSS_SELECTOR, "span.rd14 b")
                        product_price = float(
                            price_element.text.replace('$', '').replace(',', ''))
                        image_element = product.find_element(
                            By.CSS_SELECTOR, "div.rimgaw a")
                        product_URL = urljoin(
                            self.base_URL, image_element.get_attribute('href'))
                        product_photo_URL = urljoin(self.base_URL, image_element.find_element(
                            By.TAG_NAME, 'img').get_attribute('src'))
                        product_data.append([
                            product_name,
                            product_size,
                            product_price,
                            category,
                            product_URL,
                            product_photo_URL
                        ])
                    try:
                        next_button = self.driver.find_element(
                            By.XPATH, "//a[@class='numbrs' and text()='>']")
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


base_URL = "https://www.laxwineandspirits.com/"
scraper = LaxScraper(base_URL, 'data/laxwineandspirits.csv')
scraper.scrape()
