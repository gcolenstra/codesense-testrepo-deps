"""
HTML parser module for extracting content from web pages.
"""
from typing import Optional, List
from bs4 import BeautifulSoup
import scraper


def parse_html(html: str) -> BeautifulSoup:
    """
    Parse HTML content using BeautifulSoup.
    
    Args:
        html (str): Raw HTML content to parse
        
    Returns:
        BeautifulSoup: Parsed HTML soup object
    """
    if not html or not isinstance(html, str):
        raise ValueError("HTML content must be a non-empty string")
    
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def extract_links(url: str) -> List[str]:
    """
    Extract all hyperlink URLs from a web page.
    
    Args:
        url (str): URL of the web page to extract links from
        
    Returns:
        List[str]: List of extracted URLs (href attributes)
        
    Raises:
        ValueError: If URL is invalid or empty
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    try:
        html = scraper.fetch_page(url)
        soup = parse_html(html)
        links = []
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and isinstance(href, str):
                links.append(href)
        
        return links
    except Exception as e:
        raise RuntimeError(f"Failed to extract links from {url}: {str(e)}")


def extract_text(url: str) -> str:
    """
    Extract all text content from a web page.
    
    Args:
        url (str): URL of the web page to extract text from
        
    Returns:
        str: Plain text content of the page
        
    Raises:
        ValueError: If URL is invalid or empty
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    try:
        html = scraper.fetch_page(url)
        soup = parse_html(html)
        return soup.get_text()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from {url}: {str(e)}")


def get_title(url: str) -> Optional[str]:
    """
    Extract the title tag content from a web page.
    
    Args:
        url (str): URL of the web page to extract title from
        
    Returns:
        Optional[str]: Title content if found, None otherwise
        
    Raises:
        ValueError: If URL is invalid or empty
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    try:
        html = scraper.fetch_page(url)
        soup = parse_html(html)
        title = soup.find('title')
        
        if title and title.string:
            return title.string.strip()
        
        return None
    except Exception as e:
        raise RuntimeError(f"Failed to extract title from {url}: {str(e)}")