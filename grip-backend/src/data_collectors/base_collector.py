import requests
import time
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional

class BaseDataCollector(ABC):
    """Base class for all data collectors"""
    
    def __init__(self, name: str, base_url: str = None, api_key: str = None):
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.logger = logging.getLogger(f"collector.{name}")
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds between requests
        
    def _rate_limit(self):
        """Implement rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
            
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: Dict = None, headers: Dict = None) -> Optional[Dict]:
        """Make a rate-limited HTTP request"""
        self._rate_limit()
        
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            return None
        except ValueError as e:
            self.logger.error(f"JSON decode failed for {url}: {e}")
            return None
    
    def _make_html_request(self, url: str, params: Dict = None, headers: Dict = None) -> Optional[str]:
        """Make a rate-limited HTTP request and return HTML content"""
        self._rate_limit()
        
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            return None
    
    @abstractmethod
    def collect_data(self, **kwargs) -> List[Dict[str, Any]]:
        """Collect data from the source. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate a single data point. Must be implemented by subclasses."""
        pass
    
    def process_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Process and validate collected data"""
        processed_data = []
        
        for item in raw_data:
            if self.validate_data(item):
                processed_item = self.transform_data(item)
                if processed_item:
                    processed_data.append(processed_item)
            else:
                self.logger.warning(f"Invalid data item: {item}")
                
        return processed_data
    
    def transform_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform data to standard format. Can be overridden by subclasses."""
        return {
            'source': self.name,
            'collected_at': datetime.utcnow().isoformat(),
            'data': data
        }
    
    def get_source_info(self) -> Dict[str, Any]:
        """Return information about this data source"""
        return {
            'name': self.name,
            'base_url': self.base_url,
            'last_updated': datetime.utcnow().isoformat()
        }

