"""
Main entry point for web scraping application.

This module provides the main entry point for a web scraping application that
fetches web pages, extracts links and titles, and saves the results to files.
"""
import scraper
import parser
import storage
import sys
from typing import NoReturn


def main() -> NoReturn:
    """
    Main function that orchestrates the web scraping process.
    
    Processes command line arguments to get a URL, fetches the page content,
    extracts links and title information, and saves results to files.
    
    Args:
        None (uses sys.argv for command line arguments)
        
    Returns:
        NoReturn: Function exits the program after completion
        
    Raises:
        SystemExit: When invalid command line arguments are provided
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    
    try:
        print("Fetching page...")
        html = scraper.fetch_page(url)
        
        print("Extracting links...")
        links = parser.extract_links(url)
        print(f"Found {len(links)} links")
        
        print("Extracting title...")
        title = parser.get_title(url)
        print(f"Title: {title}")
        
        print("Saving results...")
        storage.save_links_to_file(url, "links.json")
        storage.save_text_to_file(url, "page.txt")
        
        print("Done!")
        
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()