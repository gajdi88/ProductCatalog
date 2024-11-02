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

    # Find the parent container by its id
    spec_section = soup.find("div", {"id": "section-specificationgroup-2007"})

    # Dictionary to store each spec's name and value
    specs = {}

    # Loop through each specification item
    for dl in spec_section.find_all("dl", class_="row generic-attr"):
        # Extract the specification name and value
        spec_name = dl.find("dt").get_text(strip=True)
        spec_value = dl.find("dd").get_text(" ", strip=True)  # ' ' joins multi-line content with spaces
        specs[spec_name] = spec_value

    # Find the parent container by its id
    features_section = soup.find("div", {"id": "section-featuresgroup-2007"})

    # List to store each feature
    features = []

    # Loop through each feature item
    for li in features_section.find_all("li"):
        # Get the text content of each <li>, joining multiple lines with a space
        feature_text = li.get_text(" ", strip=True)
        features.append(feature_text)

    product_data = {
        'Product Name': product_name,
        'Description': description,
        'Specifications': specs,
        'Features': features,
        'URL': url
    }
    print(f"Scraped data for {product_name}")
    delay()
    return product_data
