import os
import json
from typing import Optional, Dict, List, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import settings
from utils.logger import setup_logger
from utils.helpers import Helpers

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

class AdvancedWebScraper:
    def __init__(self, base_url: str):
        """Initialize the web scraper with advanced configuration."""
        self.base_url = base_url
        self.logger = setup_logger(__name__)
        self.session = self._create_session()
        self.helpers = Helpers()
        
        # Initialize Selenium if configured
        self.selenium_driver = None
        if settings.USE_SELENIUM and HAS_SELENIUM:
            self.selenium_driver = self._init_selenium()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=settings.MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _init_selenium(self):
        """Initialize Selenium WebDriver with options."""
        options = Options()
        if settings.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-agent={self.helpers.get_random_user_agent()}")
        
        # Additional options to reduce detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=options
        )
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        
        return driver
    
    def _make_request(self, url: str, method: str = 'GET', **kwargs):
        """Make an HTTP request with advanced features."""
        try:
            if settings.USE_SELENIUM and self.selenium_driver and method == 'GET':
                return self._make_selenium_request(url)
            
            headers = kwargs.get('headers', {})
            headers['User-Agent'] = self.helpers.get_random_user_agent()
            
            self.helpers.random_delay(*settings.RATE_LIMIT_DELAY)
            
            response = self.session.request(
                method,
                url,
                headers=headers,
                timeout=settings.TIMEOUT,
                **kwargs
            )
            
            response.raise_for_status()
            
            if 'text/html' in response.headers.get('Content-Type', ''):
                return BeautifulSoup(response.text, 'html.parser')
            return response.text
            
        except Exception as e:
            self.logger.error(f"Request failed for {url}: {str(e)}")
            return None
    
    def _make_selenium_request(self, url: str):
        """Make request using Selenium for JavaScript rendering."""
        try:
            self.selenium_driver.get(url)
            time.sleep(settings.SELENIUM_TIMEOUT)
            return BeautifulSoup(self.selenium_driver.page_source, 'html.parser')
        except Exception as e:
            self.logger.error(f"Selenium request failed for {url}: {str(e)}")
            return None
    
    def scrape_page(self, url: str, **kwargs):
        """Scrape a single page with error handling."""
        self.logger.info(f"Scraping page: {url}")
        return self._make_request(url, **kwargs)
    
    def scrape_multiple(self, urls: List[str], **kwargs):
        """Scrape multiple pages in parallel."""
        results = {}
        
        with ThreadPoolExecutor(max_workers=settings.MAX_THREADS) as executor:
            future_to_url = {
                executor.submit(self.scrape_page, url, **kwargs): url
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    results[url] = future.result()
                except Exception as e:
                    self.logger.error(f"Error processing {url}: {str(e)}")
                    results[url] = None
        
        return results
    
    def extract_data(self, soup: BeautifulSoup, selectors: Dict):
        """Extract structured data from BeautifulSoup object."""
        data = {}
        
        for field, selector in selectors.items():
            try:
                element = soup.select_one(selector)
                data[field] = self.helpers.clean_text(element.get_text()) if element else None
            except Exception as e:
                self.logger.error(f"Error extracting {field}: {str(e)}")
                data[field] = None
        
        return data
    
    def save_data(self, data, filename: str):
        """Save scraped data to JSON file."""
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(settings.OUTPUT_DIR, f"{filename}_{timestamp}.json")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data saved to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save data: {str(e)}")
            return False
    
    def close(self):
        """Clean up resources."""
        self.session.close()
        if self.selenium_driver:
            self.selenium_driver.quit()