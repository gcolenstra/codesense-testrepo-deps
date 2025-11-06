"""
Main entry point
"""
import scraper
import parser
import storage
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    print("Fetching page...")
    html = scraper.fetch_page(url)
    print("Extracting links...")
    links = parser.extract_links(url)
    print("Found %d links" % len(links))
    print("Extracting title...")
    title = parser.get_title(url)
    print("Title: %s" % title)
    print("Saving results...")
    storage.save_links_to_file(url, "links.json")
    storage.save_text_to_file(url, "page.txt")
    print("Done!")

if __name__ == '__main__':
    main()
