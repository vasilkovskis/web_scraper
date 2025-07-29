from scrapers.advanced_scraper import AdvancedWebScraper
from pprint import pprint
import os

def scrape_books_example():
    # Initialize scraper
    scraper = AdvancedWebScraper(base_url="https://books.toscrape.com")
    
    try:
        # Scrape homepage
        homepage = scraper.scrape_page(scraper.base_url)
        if not homepage:
            print("Failed to scrape homepage")
            return
        
        # Extract categories
        categories = homepage.select('div.side_categories ul.nav-list li ul li a')
        category_urls = [
            scraper.helpers.build_absolute_url(scraper.base_url, cat['href'])
            for cat in categories[:3]  # Just get first 3 for demo
        ]
        
        # Scrape category pages in parallel
        category_pages = scraper.scrape_multiple(category_urls)
        
        all_books = []
        book_selectors = {
            'title': 'h3 a',
            'price': 'p.price_color',
            'rating': 'p.star-rating',
            'availability': 'p.instock'
        }
        
        # Process each category
        for url, soup in category_pages.items():
            if not soup:
                continue
            
            books = soup.select('article.product_pod')
            for book in books:
                book_data = scraper.extract_data(book, book_selectors)
                book_data['category_url'] = url
                all_books.append(book_data)
        
        # Save results
        scraper.save_data(all_books, "books_data")
        print(f"Scraped {len(all_books)} books")
        pprint(all_books[:2])  # Print first 2 for demo
        
    finally:
        scraper.close()

if __name__ == "__main__":
    scrape_books_example()