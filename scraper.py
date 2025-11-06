"""
Web scraper using old requests patterns
"""
import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings

warnings.simplefilter('ignore', InsecureRequestWarning)

def fetch_page(url):
    response = requests.get(url, verify=False)
    return response.text

def post_data(url, data):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.post(url, data=data, headers=headers, verify=False)
    return response.json()

def download_file(url, filename):
    response = requests.get(url, verify=False)
    with open(filename, 'wb') as f:
        f.write(response.content)
    return True

def scrape_multiple(urls):
    results = []
    for url in urls:
        response = requests.get(url, verify=False)
        results.append(response.text)
    return results
