from scrapers.advanced_scraper import AdvancedWebScraper
from pprint import pprint

def scrape_ecommerce_example():
    scraper = AdvancedWebScraper(base_url="https://webscraper.io/test-sites/e-commerce/allinone")
    
    try:
        # Scrape product listings
        page = scraper.scrape_page(f"{scraper.base_url}/computers/laptops")
        if not page:
            print("Failed to scrape product page")
            return
        
        product_selectors = {
            'name': 'div.caption h4 a',
            'price': 'div.caption h4.price',
            'description': 'div.caption p.description',
            'reviews': 'div.ratings p.pull-right'
        }
        
        products = []
        for product in page.select('div.thumbnail'):
            product_data = scraper.extract_data(product, product_selectors)
            products.append(product_data)
        
        scraper.save_data(products, "laptops_data")
        print(f"Scraped {len(products)} products")
        pprint(products[:3])  # Print first 3 for demo
        
    finally:
        scraper.close()

if __name__ == "__main__":
    scrape_ecommerce_example()