# product_scraper.py
from bs4 import BeautifulSoup
from utils import get_html, delay


def parse_product_page(url):
    """
    Scrapes details from a single product page.
    """
    html = get_html(url)
    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')

    # Extract product details; adjust selectors based on HTML structure
    product_name = soup.find('h1', {'class': 'product-name'}).get_text(strip=True) if soup.find('h1', {
        'class': 'product-name'}) else "N/A"
    # price = soup.find('span', {'class': 'product-price'}).get_text(strip=True) if soup.find('span', {
    #     'class': 'product-price'}) else "N/A"
    description = soup.find('div', {'class': 'product-description-wrapper-new padding'}).get_text(strip=True) if soup.find('div', {
        'class': 'product-description-wrapper-new padding'}) else "N/A"

    product_data = {
        'Product Name': product_name,
        'Description': description,
        'URL': url
    }
    print(f"Scraped data for {product_name}")
    delay()
    return product_data
