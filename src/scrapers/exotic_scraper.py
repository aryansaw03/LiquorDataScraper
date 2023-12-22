import time
from base_scraper import BaseScraper
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse
from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class ExoticScraper(BaseScraper):

    CATEGORIES = ['wine', 'beer', 'spirits']
    CATEGORY_URL_SEGMENTS = ['washington-dc-wine-store/', 'beer/', 'spirits/']

    def __init__(self, base_URL, output_file=None):
        super().__init__(base_URL, output_file)

    def scrape(self):
        product_data = []
        try:
            for category, category_URL_segment in zip(self.CATEGORIES, self.CATEGORY_URL_SEGMENTS):
                self.open_webpage(urljoin(
                    self.base_URL, f'category/{category_URL_segment}'))
                while True:
                    print('Scraping from page:', self.driver.current_url)
                    products = self.driver.find_elements(
                        By.CLASS_NAME, 'wa-theme-design-block')
                    for product in products:
                        title_element = product.find_element(
                            By.CSS_SELECTOR, ".block-caption1 a")
                        product_name = title_element.get_attribute('title')
                        price_element = product.find_element(
                            By.CLASS_NAME, "sell-price")
                        product_price = float(
                            price_element.text.replace('$', '').replace(',', ''))
                        image_element = product.find_element(
                            By.TAG_NAME, "img")
                        product_URL = urljoin(
                            self.base_URL, title_element.get_attribute('href'))
                        product_photo_URL = urljoin(
                            self.base_URL, image_element.get_attribute('src'))
                        product_data.append([
                            product_name,
                            product_price,
                            category,
                            product_URL,
                            product_photo_URL
                        ])
                    try:
                        next_button = self.driver.find_element(
                            By.CSS_SELECTOR, ".next a")
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
                product_data, ['name', 'price', 'category', 'URL', 'photoURL'])
        return product_data


base_URL = "https://www.exoticwinespirits.com/"
scraper = ExoticScraper(base_URL, 'data/exoticwineandspirits.csv')
scraper.scrape()
