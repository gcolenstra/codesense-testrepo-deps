"""
Web scraper using secure requests patterns with proper SSL verification
"""
import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
from typing import List, Dict, Any, Optional
import os
from pathvalidate import sanitize_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_page(url: str, timeout: int = 30, verify_ssl: bool = True) -> str:
    """
    Fetch a web page content securely.
    
    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates
        
    Returns:
        The page content as a string
        
    Raises:
        requests.RequestException: If the request fails
    """
    try:
        response = requests.get(url, verify=verify_ssl, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to fetch page {url}: {e}")
        raise

def post_data(url: str, data: Dict[str, Any], timeout: int = 30, 
              verify_ssl: bool = True) -> Dict[str, Any]:
    """
    Post data to a URL and return JSON response.
    
    Args:
        url: The URL to post to
        data: The data to send
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates
        
    Returns:
        JSON response as a dictionary
        
    Raises:
        requests.RequestException: If the request fails
        ValueError: If response is not valid JSON
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Python Scraper)',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, 
                               verify=verify_ssl, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to post data to {url}: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid JSON response from {url}: {e}")
        raise

def download_file(url: str, filename: str, timeout: int = 30, 
                  verify_ssl: bool = True, safe_filename: bool = True) -> bool:
    """
    Download a file from a URL securely.
    
    Args:
        url: The URL to download from
        filename: The filename to save to
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates
        safe_filename: Whether to sanitize the filename
        
    Returns:
        True if download was successful
        
    Raises:
        requests.RequestException: If the download fails
        OSError: If file cannot be written
    """
    if safe_filename:
        filename = sanitize_filename(filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    try:
        with requests.get(url, verify=verify_ssl, timeout=timeout, 
                         stream=True) as response:
            response.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        logger.info(f"Successfully downloaded {url} to {filename}")
        return True
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
        raise
    except OSError as e:
        logger.error(f"Failed to write file {filename}: {e}")
        raise

def scrape_multiple(urls: List[str], timeout: int = 30, 
                   verify_ssl: bool = True, max_workers: int = 5) -> List[Optional[str]]:
    """
    Scrape multiple URLs concurrently with proper error handling.
    
    Args:
        urls: List of URLs to scrape
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates
        max_workers: Maximum number of concurrent workers
        
    Returns:
        List of page contents (None for failed requests)
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    def fetch_single(url: str) -> Optional[str]:
        try:
            return fetch_page(url, timeout=timeout, verify_ssl=verify_ssl)
        except requests.RequestException:
            return None
    
    results = [None] * len(urls)
    url_to_index = {url: idx for idx, url in enumerate(urls)}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_single, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results[url_to_index[url]] = result
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                results[url_to_index[url]] = None
    
    return results