"""
HTML parser
"""
from bs4 import BeautifulSoup
import scraper

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_links(url):
    html = scraper.fetch_page(url)
    soup = parse_html(html)
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    return links

def extract_text(url):
    html = scraper.fetch_page(url)
    soup = parse_html(html)
    return soup.get_text()

def get_title(url):
    html = scraper.fetch_page(url)
    soup = parse_html(html)
    title = soup.find('title')
    if title:
        return title.string
    return None
