import requests
from bs4 import BeautifulSoup
import json
import time

def extract_parser_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Get the Title (Vendor/Product)
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Unknown"
        
        # 2. Find the Mapping Table
        # We look for the table that specifically has "UDM mapping" in the header
        target_table = None
        for table in soup.find_all('table'):
            headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
            if 'udm mapping' in headers:
                target_table = table
                break
        
        mappings = []
        if target_table:
            rows = target_table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 2:
                    mappings.append({
                        "log_field": cols[0].get_text(strip=True),
                        "udm_field": cols[1].get_text(strip=True),
                        "description": cols[2].get_text(strip=True) if len(cols) > 2 else ""
                    })
        
        return {
            "source_url": url,
            "product": title,
            "mappings": mappings
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Loop through your list
all_data = []
with open('parser_urls.txt', 'r') as f:
    urls = [line.strip() for line in f.readlines()]

for url in urls:
    print(f"Processing: {url}")
    data = extract_parser_data(url)
    if data:
        all_data.append(data)
    time.sleep(1) # Be a good citizen

# Save the master dataset
with open('udm_training_corpus.json', 'w') as f:
    json.dump(all_data, f, indent=2)
