# catalog_scraper.py
from bs4 import BeautifulSoup
from utils import delay
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import CATALOG_URL

def get_catalog_page_urls():
    """
        Collects and returns URLs of all catalog pages.
        Assumes pagination is present on the catalog pages.
        """
    product_urls = []

    # Initialize Selenium WebDriver
    service = Service('C:\Installed\chromedriver-win64\chromedriver.exe')  # Replace with the path to your ChromeDriver
    driver = webdriver.Chrome(service=service)
    driver.get(CATALOG_URL)  # Replace with your starting catalog page URL

    try:
        page = 0
        while True:
            # Wait for the products to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product_image a"))
            )

            # Parse the current page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find product links
            product_links = [a['href'] for a in soup.select('.product_image a')]
            if not product_links:
                print(f"No more products found on page {page}.")
                break  # Stop if no more products found

            product_urls.extend(product_links)
            print(f"Page {page}: Collected {len(product_links)} product URLs.")

            # Try clicking the "Next Page" button
            try:
                next_button = driver.find_element(By.CSS_SELECTOR,
                                                  ".next-wrapper")  # Replace with actual CSS selector
                next_button.click()
                delay((10, 12))
                page += 1
            except Exception as e:
                print(f"No 'Next Page' button found: {e}")
                break

    finally:
        driver.quit()

    return product_urls
