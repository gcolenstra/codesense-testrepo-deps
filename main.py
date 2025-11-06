"""
Main entry point for web scraping application.
"""
import scraper
import parser
import storage
import sys
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def validate_url(url: str) -> bool:
    """
    Validate if the provided URL is in a basic valid format.
    
    Args:
        url: The URL string to validate
        
    Returns:
        bool: True if URL appears valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    return url.startswith(('http://', 'https://'))


def main() -> None:
    """
    Main entry point for the web scraping application.
    
    Processes command line arguments, fetches a web page, extracts links and title,
    and saves the results to files.
    
    Exits with status code 1 if invalid arguments are provided.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Validate URL format
    if not validate_url(url):
        logger.error(f"Invalid URL format: {url}")
        print("Error: Please provide a valid URL starting with http:// or https://")
        sys.exit(1)
    
    try:
        logger.info(f"Starting scraping process for URL: {url}")
        
        print("Fetching page...")
        html = scraper.fetch_page(url)
        
        if not html:
            logger.error("Failed to fetch page content")
            print("Error: Could not fetch page content")
            sys.exit(1)
        
        print("Extracting links...")
        links = parser.extract_links(url)
        print(f"Found {len(links)} links")
        
        print("Extracting title...")
        title = parser.get_title(url)
        print(f"Title: {title}")
        
        print("Saving results...")
        storage.save_links_to_file(url, "links.json")
        storage.save_text_to_file(url, "page.txt")
        
        logger.info("Scraping process completed successfully")
        print("Done!")
        
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()