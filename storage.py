"""
Data storage module
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Union
import parser


def save_links_to_file(url: str, filename: Union[str, Path]) -> int:
    """
    Extract links from a URL and save them to a JSON file.
    
    Args:
        url: The URL to extract links from
        filename: The file path to save the links to
        
    Returns:
        The number of links saved
        
    Raises:
        IOError: If file cannot be written
        ValueError: If URL is invalid
    """
    try:
        links = parser.extract_links(url)
        filepath = Path(filename)
        
        # Ensure parent directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with filepath.open('w', encoding='utf-8') as f:
            json.dump(links, f, indent=2, ensure_ascii=False)
        
        return len(links)
    except Exception as e:
        raise IOError(f"Failed to save links to {filename}: {e}")


def save_text_to_file(url: str, filename: Union[str, Path]) -> None:
    """
    Extract text from a URL and save it to a file.
    
    Args:
        url: The URL to extract text from
        filename: The file path to save the text to
        
    Raises:
        IOError: If file cannot be written
        ValueError: If URL is invalid
    """
    try:
        text = parser.extract_text(url)
        filepath = Path(filename)
        
        # Ensure parent directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with filepath.open('w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        raise IOError(f"Failed to save text to {filename}: {e}")


def create_report(urls: List[str]) -> Dict[str, List[Any]]:
    """
    Create a comprehensive report from multiple URLs.
    
    Args:
        urls: List of URLs to analyze
        
    Returns:
        Dictionary containing URLs, titles, and link counts
        
    Raises:
        ValueError: If urls list is empty or contains invalid URLs
    """
    if not urls:
        raise ValueError("URLs list cannot be empty")
    
    report = {'urls': [], 'titles': [], 'link_counts': []}
    
    for url in urls:
        try:
            title = parser.get_title(url)
            links = parser.extract_links(url)
            
            report['urls'].append(url)
            report['titles'].append(title)
            report['link_counts'].append(len(links))
        except Exception as e:
            # Log error but continue with other URLs
            report['urls'].append(url)
            report['titles'].append(f"Error: {e}")
            report['link_counts'].append(0)
    
    return report