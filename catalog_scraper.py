# catalog_scraper.py
from bs4 import BeautifulSoup
from utils import get_html, delay
from config import CATALOG_URL, BASE_URL


def get_catalog_page_urls():
    """
    Collects and returns URLs of all catalog pages.
    Assumes pagination is present on the catalog pages.
    """
    catalog_urls = []
    page = 0
    while True:
        #url = f"{CATALOG_URL}?page={page}"  # Adjust based on the actual URL structure
        url = CATALOG_URL
        html = get_html(url)
        if not html:
            break

        soup = BeautifulSoup(html, 'html.parser')
        # Find links to products; update based on HTML structure
        product_links = [a['href'] for a in soup.select('.product_image a')]
        if not product_links:
            break  # Stop if no more products found

        # catalog_urls.extend([f"{BASE_URL}{link}" for link in product_links])
        catalog_urls.extend(product_links)
        print(f"Page {page}: Collected {len(product_links)} product URLs.")

        page += 1
        break
        delay()


    return catalog_urls
