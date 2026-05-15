"""
Re-fetch FULL product descriptions from ezup.ca
Removes the 300-char limit from the original scraper
"""
import json, requests, time, re
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

session = requests.Session()
session.headers.update(HEADERS)

updated = 0
failed = 0

for i, p in enumerate(products):
    # Reconstruct the product URL from the id
    slug = p['id']
    url = f'https://www.ezup.ca/products/{slug}'
    
    print(f'[{i+1}/{len(products)}] {p["name"][:50]}...', end=' ')
    
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            print(f'HTTP {r.status_code}')
            failed += 1
            time.sleep(0.3)
            continue
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Try meta description first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        full_desc = meta_desc.get('content', '').strip() if meta_desc else ''
        
        # Also try to get the product description from the page body
        # Look for product description sections
        body_desc = ''
        for selector in ['.product__description', '.product-description', '[class*="product-description"]', '.rte', '.product-single__description']:
            el = soup.select_one(selector)
            if el:
                body_desc = el.get_text(separator=' ', strip=True)
                break
        
        # Use the longer description
        best_desc = body_desc if len(body_desc) > len(full_desc) else full_desc
        
        if best_desc and len(best_desc) > len(p.get('description', '')):
            old_len = len(p.get('description', ''))
            p['description'] = best_desc
            print(f'UPDATED ({old_len} -> {len(best_desc)} chars)')
            updated += 1
        elif best_desc:
            print(f'OK ({len(best_desc)} chars, already full)')
        else:
            print('NO DESCRIPTION FOUND')
            failed += 1
    except Exception as e:
        print(f'ERROR: {e}')
        failed += 1
    
    time.sleep(0.3)

# Save updated products
with open('data/products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f'\n\nDone! Updated: {updated} | Failed: {failed} | Total: {len(products)}')
