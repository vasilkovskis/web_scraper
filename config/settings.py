import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Request settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    TIMEOUT = int(os.getenv('TIMEOUT', 30))
    RATE_LIMIT_DELAY = (1, 3)  # Random delay range between requests
    
    # Parallel processing
    MAX_THREADS = int(os.getenv('MAX_THREADS', 5))
    
    # Proxy settings
    USE_PROXIES = bool(os.getenv('USE_PROXIES', False))
    
    # Selenium settings
    USE_SELENIUM = bool(os.getenv('USE_SELENIUM', False))
    HEADLESS = bool(os.getenv('HEADLESS', True))
    SELENIUM_TIMEOUT = 10
    
    # Output settings
    OUTPUT_DIR = 'output'
    LOG_DIR = 'logs'
    
settings = Settings()