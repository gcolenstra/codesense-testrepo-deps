"""
Data storage module
"""
import json
import parser

def save_links_to_file(url, filename):
    links = parser.extract_links(url)
    f = open(filename, 'w')
    json.dump(links, f)
    f.close()
    return len(links)

def save_text_to_file(url, filename):
    text = parser.extract_text(url)
    f = open(filename, 'w')
    f.write(text)
    f.close()

def create_report(urls):
    report = {'urls': [], 'titles': [], 'link_counts': []}
    for url in urls:
        title = parser.get_title(url)
        links = parser.extract_links(url)
        report['urls'].append(url)
        report['titles'].append(title)
        report['link_counts'].append(len(links))
    return report
