import requests
from bs4 import BeautifulSoup
import re

def get_all_parser_links():
    index_url = "https://cloud.google.com/chronicle/docs/ingestion/parser-list/supported-default-parsers"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(index_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # All parser pages follow this URL path structure
    parser_pattern = re.compile(r'/chronicle/docs/ingestion/default-parsers/[\w-]+')
    
    # Use a set to avoid duplicates
    parser_links = set()
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if parser_pattern.search(href):
            # Ensure we have the full URL
            if href.startswith('/'):
                href = "https://cloud.google.com" + href
            
            # Clean up fragments and force English
            clean_url = href.split('#')[0].split('?')[0] + "?hl=en"
            parser_links.add(clean_url)
            
    return sorted(list(parser_links))

# Run and save to a file
all_parsers = get_all_parser_links()
with open('parser_urls.txt', 'w') as f:
    for url in all_parsers:
        f.write(url + '\n')

print(f"Found {len(all_parsers)} parser pages.")
