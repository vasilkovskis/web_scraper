# Web Scraper

Python scraper specializing in JSON output with robust data collection features.

## Core Features
- **JSON output** with proper formatting
- Automatic retries (3 attempts by default)
- User agent rotation
- Request throttling (1-3 second delays)
- Data validation and cleaning

## Quick Start
```bash
pip install requests beautifulsoup4
python examples/example_books.py
```
## JSON Output Example
```bash
[
  {
    "title": "Example Product",
    "price": "$19.99",
    "stock": true,
    "rating": 4.5
  },
  {
    "title": "Another Product",
    "price": "$29.99",
    "stock": false,
    "rating": 3.8
  }
]
```
## Basic Usage
```bash
from scrapers.advanced_scraper import AdvancedWebScraper

scraper = AdvancedWebScraper("https://example.com")
try:
    data = scraper.scrape_page("/products")
    with open("output.json", "w") as f:
        json.dump(data, f, indent=2)
finally:
    scraper.close()
```
## Configuration (config/settings.py)
```bash

# JSON-specific settings
JSON_INDENT = 2                  # Output indentation
JSON_ENSURE_ASCII = False        # Preserve non-ASCII characters
OUTPUT_DIR = "json_outputs"      # Storage location
```
## Command Line Output

The script will display:
```bash
[INFO] Scraping https://example.com...
[SUCCESS] Saved 24 items to output_20230815.json
```
## Troubleshooting
Empty JSON file?

    Check target website's robots.txt
    Enable Selenium in config for JavaScript sites:

```bash
USE_SELENIUM = True
```
## Malformed JSON?
    Set VALIDATE_JSON = True in config
    The scraper will validate JSON structure before saving
    
```bash
This stripped-down README focuses exclusively on:
1. JSON output capabilities
2. Minimum setup requirements
3. Clean code examples
4. JSON-specific configuration
5. Basic troubleshooting

The markdown uses:
- Only JSON-relevant information
- Simple code blocks
- Clear section headers
- No unnecessary graphics or features
```
