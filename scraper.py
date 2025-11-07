"""
Web scraper using secure requests patterns with proper error handling and validation
"""
import os
import requests
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScraperError(Exception):
    """Custom exception for scraper-related errors"""
    pass

def fetch_page(url: str, timeout: int = 30, verify_ssl: bool = True) -> str:
    """
    Fetch the content of a web page.
    
    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates
        
    Returns:
        The page content as text
        
    Raises:
        ScraperError: If the request fails or URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ScraperError("Invalid URL provided")
    
    if not url.startswith(('http://', 'https://')):
        raise ScraperError("URL must start with http:// or https://")
    
    try:
        response = requests.get(
            url, 
            timeout=timeout, 
            verify=verify_ssl,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; SecureScraper/1.0)'}
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        raise ScraperError(f"Failed to fetch URL: {e}")

def post_data(url: str, data: Dict[str, Any], timeout: int = 30, verify_ssl: bool = True) -> Dict[str, Any]:
    """
    Post data to a URL and return JSON response.
    
    Args:
        url: The URL to post to
        data: Data to post
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates
        
    Returns:
        JSON response as dictionary
        
    Raises:
        ScraperError: If the request fails or response is invalid
    """
    if not url or not isinstance(url, str):
        raise ScraperError("Invalid URL provided")
    
    if not url.startswith(('http://', 'https://')):
        raise ScraperError("URL must start with http:// or https://")
    
    if not isinstance(data, dict):
        raise ScraperError("Data must be a dictionary")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; SecureScraper/1.0)',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            url, 
            json=data,  # Use json parameter for proper encoding
            headers=headers, 
            timeout=timeout,
            verify=verify_ssl
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to post to {url}: {e}")
        raise ScraperError(f"Failed to post data: {e}")
    except ValueError as e:
        logger.error(f"Invalid JSON response from {url}: {e}")
        raise ScraperError(f"Invalid JSON response: {e}")

def download_file(url: str, filename: str, timeout: int = 30, verify_ssl: bool = True, max_size: int = 100 * 1024 * 1024) -> bool:
    """
    Download a file from URL to local filesystem.
    
    Args:
        url: The URL to download from
        filename: Local filename to save to
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates
        max_size: Maximum file size in bytes (default 100MB)
        
    Returns:
        True if successful
        
    Raises:
        ScraperError: If the download fails or file is too large
    """
    if not url or not isinstance(url, str):
        raise ScraperError("Invalid URL provided")
    
    if not url.startswith(('http://', 'https://')):
        raise ScraperError("URL must start with http:// or https://")
    
    if not filename or not isinstance(filename, str):
        raise ScraperError("Invalid filename provided")
    
    # Validate filename to prevent directory traversal
    file_path = Path(filename)
    if file_path.is_absolute() or '..' in str(file_path):
        raise ScraperError("Invalid filename: path traversal detected")
    
    try:
        with requests.get(
            url, 
            stream=True, 
            timeout=timeout,
            verify=verify_ssl,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; SecureScraper/1.0)'}
        ) as response:
            response.raise_for_status()
            
            # Check content length
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > max_size:
                raise ScraperError(f"File too large: {content_length} bytes > {max_size} bytes")
            
            with open(filename, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        downloaded += len(chunk)
                        if downloaded > max_size:
                            raise ScraperError(f"File too large: exceeded {max_size} bytes")
                        f.write(chunk)
        
        logger.info(f"Successfully downloaded {url} to {filename}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
        raise ScraperError(f"Failed to download file: {e}")
    except OSError as e:
        logger.error(f"Failed to write file {filename}: {e}")
        raise ScraperError(f"Failed to write file: {e}")

def scrape_multiple(urls: List[str], timeout: int = 30, verify_ssl: bool = True, max_workers: int = 5) -> List[Optional[str]]:
    """
    Scrape multiple URLs and return their content.
    
    Args:
        urls: List of URLs to scrape
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates
        max_workers: Maximum number of concurrent requests
        
    Returns:
        List of page contents (None for failed requests)
        
    Raises:
        ScraperError: If urls parameter is invalid
    """
    if not urls or not isinstance(urls, list):
        raise ScraperError("URLs must be provided as a list")
    
    if not all(isinstance(url, str) for url in urls):
        raise ScraperError("All URLs must be strings")
    
    results = []
    for url in urls:
        try:
            content = fetch_page(url, timeout=timeout, verify_ssl=verify_ssl)
            results.append(content)
        except ScraperError as e:
            logger.warning(f"Failed to scrape {url}: {e}")
            results.append(None)
    
    return results