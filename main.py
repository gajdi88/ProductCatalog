# main.py
from catalog_scraper import get_catalog_page_urls
from product_scraper import parse_product_page
from utils import save_to_csv


def main():
    # Step 1: Get all product URLs from the catalog pages
    product_urls = get_catalog_page_urls()
    #product_urls = ['https://www.emerson.com/en-gb/catalog/automation/measurement-instrumentation/pressure-transmitters-transducers/rosemount-sku-3051-coplanar-pressure-transmitter-en-gb?fetchFacets=true#facet:&partsFacet:&modelsFacet:&facetLimit:&searchTerm:&partsSearchTerm:&modelsSearchTerm:&productBeginIndex:0&partsBeginIndex:0&modelsBeginIndex:0&orderBy:&partsOrderBy:&modelsOrderBy:&pageView:list&minPrice:&maxPrice:&pageSize:&facetRange:&']
    print(f"Collected {len(product_urls)} product URLs.")

    # Step 2: Scrape each product page
    all_product_data = []
    for url in product_urls:
        product_data = parse_product_page(url)
        if product_data:
            all_product_data.append(product_data)

    # Step 3: Save results
    save_to_csv(all_product_data)


if __name__ == "__main__":
    main()
