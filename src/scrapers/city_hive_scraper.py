from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse
from .base_scraper import BaseScraper
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class CityHiveScraper(BaseScraper):

    CATEGORIES = ['beer', 'spirits']

    def __init__(self, base_URL, output_file=None):
        super().__init__(base_URL, output_file)

    def scrape(self):
        product_data = []
        try:
            for category in self.CATEGORIES:
                self.open_webpage(
                    urljoin(self.base_URL, f"shop/?category={category}"))
                while True:
                    print('Scraping from page:', self.driver.current_url)
                    original_URL = self.driver.current_url
                    products = self.driver.find_elements(
                        By.CLASS_NAME, 'product')
                    for i in range(len(products)):
                        product = products[i]
                        product_name = product.find_element(
                            By.CLASS_NAME, 'ch-product-name').text
                        product_URL = urljoin(self.base_URL, product.find_element(
                            By.TAG_NAME, "a").get_attribute("href"))
                        product_photo_URL = urljoin(self.base_URL, product.find_element(
                            By.CLASS_NAME, "ch-product-image").get_attribute("src"))
                        size_element = product.find_element(
                            By.CLASS_NAME, 'ch-product-options')
                        if "Option" in size_element.text:
                            self.open_webpage(product_URL)
                            options = self.driver.find_elements(
                                By.CLASS_NAME, 'product-option-tab-text-container')

                            option_URLs = []
                            for option in options:
                                option_ID = option.get_attribute(
                                    "id").replace('product-option-', '')
                                parsed_URL = urlparse(self.driver.current_url)
                                query_params = parse_qs(parsed_URL.query)
                                query_params['option-id'] = [option_ID]
                                option_URLs.append(urlunparse(parsed_URL._replace(
                                    query=urlencode(query_params, doseq=True))))

                            for option_URL in option_URLs:
                                self.open_webpage(option_URL)
                                print('Scraping from page:', option_URL)
                                size_element = None
                                try:
                                    size_element = self.driver.find_element(
                                        By.CLASS_NAME, 'product-price-discount-size-label')
                                except NoSuchElementException:
                                    pass
                                product_size = size_element.text if size_element else None

                                price_element = None
                                try:
                                    price_element = self.driver.find_element(
                                        By.CLASS_NAME, 'product-price-discount-main-text-with')
                                except NoSuchElementException:
                                    continue
                                product_price = float(
                                    price_element.text.replace('$', '').replace(',', ''))

                                product_data.append([
                                    product_name,
                                    product_size,
                                    product_price,
                                    category,
                                    product_URL,
                                    product_photo_URL
                                ])
                            self.open_webpage(original_URL)
                            products = self.driver.find_elements(
                                By.CLASS_NAME, 'product')
                            if len(products) == 0:
                                pass
                        else:
                            price_element = product.find_element(
                                By.CLASS_NAME, 'ch-single-product-price')
                            product_price = float(
                                price_element.text.replace('$', '').replace(',', ''))
                            product_size = product.find_element(
                                By.CLASS_NAME, 'ch-product-options').text
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
                            By.XPATH, "//a[@data-hook='search-results-next-page']")
                        next_URL = next_button.get_attribute("href")
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
