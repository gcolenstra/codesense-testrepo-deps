"""
Data storage module
"""
import json
from typing import List, Dict, Any, Union
import parser


def save_links_to_file(url: str, filename: str) -> int:
    """
    Extract links from a URL and save them to a JSON file.
    
    Args:
        url: The URL to extract links from
        filename: The output filename for the JSON data
        
    Returns:
        The number of links extracted and saved
        
    Raises:
        IOError: If file cannot be written
        ValueError: If URL is invalid
    """
    links = parser.extract_links(url)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(links, f, indent=2, ensure_ascii=False)
    return len(links)


def save_text_to_file(url: str, filename: str) -> None:
    """
    Extract text content from a URL and save it to a text file.
    
    Args:
        url: The URL to extract text from
        filename: The output filename for the text data
        
    Raises:
        IOError: If file cannot be written
        ValueError: If URL is invalid
    """
    text = parser.extract_text(url)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


def create_report(urls: List[str]) -> Dict[str, List[Union[str, int]]]:
    """
    Create a comprehensive report from multiple URLs.
    
    Args:
        urls: List of URLs to process
        
    Returns:
        Dictionary containing URLs, titles, and link counts for each URL
        
    Raises:
        ValueError: If urls list is empty or contains invalid URLs
    """
    if not urls:
        raise ValueError("URLs list cannot be empty")
    
    report: Dict[str, List[Union[str, int]]] = {
        'urls': [], 
        'titles': [], 
        'link_counts': []
    }
    
    for url in urls:
        if not isinstance(url, str) or not url.strip():
            raise ValueError(f"Invalid URL: {url}")
            
        title = parser.get_title(url)
        links = parser.extract_links(url)
        report['urls'].append(url)
        report['titles'].append(title)
        report['link_counts'].append(len(links))
    
    return report