import random
import time
from typing import Optional, Dict, List
from urllib.parse import urljoin
from fake_useragent import UserAgent

class Helpers:
    @staticmethod
    def get_random_user_agent() -> str:
        """Return a random user agent string."""
        return UserAgent().random
    
    @staticmethod
    def random_delay(min_delay: float = 1, max_delay: float = 3) -> None:
        """Sleep for a random interval between min and max seconds."""
        time.sleep(random.uniform(min_delay, max_delay))
    
    @staticmethod
    def build_absolute_url(base_url: str, relative_url: str) -> str:
        """Construct an absolute URL from a base and relative URL."""
        return urljoin(base_url, relative_url)
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text by removing extra whitespace."""
        if not text:
            return ''
        return ' '.join(text.strip().split())