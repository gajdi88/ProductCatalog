
BASE_URL = "https://www.emerson.com/en-us"
#CATALOG_URL = f"{BASE_URL}/catalog"  # Update this as needed
CATALOG_URL = 'https://www.emerson.com/en-gb/catalog/automation/measurement-instrumentation?fetchFacets=true#facet:&partsFacet:&modelsFacet:&facetLimit:&searchTerm:&partsSearchTerm:&modelsSearchTerm:&productBeginIndex:0&partsBeginIndex:0&modelsBeginIndex:0&orderBy:&partsOrderBy:&modelsOrderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:&facetRange:&'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
DELAY_BETWEEN_REQUESTS = (1, 3)  # Random delay range between requests in seconds
