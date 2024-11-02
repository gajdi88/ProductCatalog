import unittest
from unittest.mock import patch
from product_scraper import parse_product_page

# Sample HTML to mimic a product page response (simplified for testing purposes)
sample_html = """
<html>
    <body>
        <h1 class="product-name">Sample Product</h1>
        <div class="product-description-wrapper-new padding">This is a sample product description.</div>
    </body>
</html>
"""

class TestProductScraper(unittest.TestCase):

    @patch('product_scraper.get_html')
    def test_parse_product_page(self, mock_get_html):
        # Arrange
        # Mock the HTML returned by get_html to be our sample HTML
        mock_get_html.return_value = sample_html
        url = "https://www.emerson.com/en-gb/catalog/automation/measurement-instrumentation/rosemount-sku-3051-coplanar-pressure-transmitter-en-gb"

        # Act
        result = parse_product_page(url)

        # Assert
        self.assertEqual(result['Product Name'], "Sample Product")
        self.assertEqual(result['Description'], "This is a sample product description.")
        self.assertEqual(result['URL'], url)

    @patch('product_scraper.get_html')
    def test_parse_product_page_missing_elements(self, mock_get_html):
        # Arrange
        incomplete_html = """
        <html>
            <body>
                <h1 class="product-name">Incomplete Product</h1>
                <!-- No price or description -->
            </body>
        </html>
        """
        mock_get_html.return_value = incomplete_html
        url = "https://www.emerson.com/en-us/catalog/incomplete-product"

        # Act
        result = parse_product_page(url)

        # Assert
        self.assertEqual(result['Product Name'], "Incomplete Product")
        self.assertEqual(result['Description'], "N/A")
        self.assertEqual(result['URL'], url)

    @patch('product_scraper.get_html')
    def test_parse_product_page_specs_features(self, mock_get_html):
        # Arrange
        with open('full_html_text.html', 'r') as file:
            incomplete_html = file.read()
        mock_get_html.return_value = incomplete_html
        url = "https://www.emerson.com/en-us/catalog/full-pressure-product"

        # Act
        result = parse_product_page(url)

        # Assert
        self.assertEqual(result['Product Name'], "Incomplete Product")
        self.assertEqual(result['Description'], "N/A")
        self.assertEqual(result['URL'], url)

if __name__ == '__main__':
    unittest.main()