"""
HTML parser for extracting content from web pages.

This module provides utilities for parsing HTML content and extracting
various elements like links, text, and titles from web pages.
"""
from typing import Optional, List
from bs4 import BeautifulSoup
import scraper


def parse_html(html: str) -> BeautifulSoup:
    """
    Parse HTML content into a BeautifulSoup object.
    
    Args:
        html: Raw HTML content as a string
        
    Returns:
        BeautifulSoup object for HTML parsing and manipulation
        
    Raises:
        Exception: If HTML parsing fails
    """
    if not html or not isinstance(html, str):
        raise ValueError("HTML content must be a non-empty string")
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except Exception as e:
        raise Exception(f"Failed to parse HTML: {e}")


def extract_links(url: str) -> List[str]:
    """
    Extract all links (href attributes) from a web page.
    
    Args:
        url: URL of the web page to extract links from
        
    Returns:
        List of href values found in anchor tags
        
    Raises:
        Exception: If page fetching or parsing fails
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    try:
        html = scraper.fetch_page(url)
        soup = parse_html(html)
        links = []
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                # Basic validation to ensure href is a string
                if isinstance(href, str):
                    links.append(href)
        
        return links
    except Exception as e:
        raise Exception(f"Failed to extract links from {url}: {e}")


def extract_text(url: str) -> str:
    """
    Extract all text content from a web page.
    
    Args:
        url: URL of the web page to extract text from
        
    Returns:
        Plain text content of the page with HTML tags removed
        
    Raises:
        Exception: If page fetching or parsing fails
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    try:
        html = scraper.fetch_page(url)
        soup = parse_html(html)
        return soup.get_text().strip()
    except Exception as e:
        raise Exception(f"Failed to extract text from {url}: {e}")


def get_title(url: str) -> Optional[str]:
    """
    Extract the title from a web page.
    
    Args:
        url: URL of the web page to get title from
        
    Returns:
        Title text if found, None otherwise
        
    Raises:
        Exception: If page fetching or parsing fails
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
        raise Exception(f"Failed to get title from {url}: {e}")