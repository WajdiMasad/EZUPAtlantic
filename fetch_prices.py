"""
Fetch prices from ezup.ca for all products missing prices
"""
import json, requests, re, time
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

with open(r'e:\EZUP\data\products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

session = requests.Session()
session.headers.update(HEADERS)

# Build product URL from ID
def get_product_url(product_id):
    # The scraper stored IDs as slugified names from URL paths
    return f"https://www.ezup.ca/products/{product_id}"

updated = 0
failed = 0
already = 0

for i, p in enumerate(products):
    # Skip if already has a real price
    if p.get('price', 0) > 0:
        already += 1
        continue
    
    url = get_product_url(p['id'])
    print(f"[{i+1}/{len(products)}] {p['name'][:45]}... ", end="", flush=True)
    
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            print(f"HTTP {r.status_code}")
            failed += 1
            time.sleep(0.3)
            continue
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Try multiple price selectors
        price_text = None
        
        # Method 1: JSON-LD structured data
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if 'offers' in data:
                        offers = data['offers']
                        if isinstance(offers, list) and offers:
                            price_text = str(offers[0].get('price', ''))
                        elif isinstance(offers, dict):
                            price_text = str(offers.get('price', ''))
                    if price_text:
                        break
            except:
                pass
        
        # Method 2: Meta tags
        if not price_text:
            meta_price = soup.find('meta', attrs={'property': 'og:price:amount'})
            if meta_price:
                price_text = meta_price.get('content', '')
        
        # Method 3: Price elements on page
        if not price_text:
            for sel in ['.price__regular .price-item', '.price-item--regular', '.product__price', '[class*="price"] .money']:
                el = soup.select_one(sel)
                if el:
                    price_text = el.get_text(strip=True)
                    break
        
        # Method 4: Search page text for price pattern
        if not price_text:
            match = re.search(r'\$\s*([\d,]+\.\d{2})', r.text[:50000])
            if match:
                price_text = match.group(1)
        
        if price_text:
            # Clean and parse price
            price_clean = re.sub(r'[^\d.]', '', price_text.replace(',', ''))
            try:
                price_num = float(price_clean)
                if price_num > 0:
                    p['price'] = price_num
                    p['priceDisplay'] = f"From ${price_num:,.2f}"
                    updated += 1
                    print(f"${price_num:,.2f}")
                else:
                    print("$0 - skipped")
                    failed += 1
            except ValueError:
                print(f"parse error: {price_text}")
                failed += 1
        else:
            print("no price found")
            failed += 1
    
    except Exception as e:
        print(f"error: {e}")
        failed += 1
    
    time.sleep(0.3)

# Save updated JSON
with open(r'e:\EZUP\data\products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f"\n{'='*50}")
print(f"Already had price: {already}")
print(f"Updated: {updated}")
print(f"Failed: {failed}")
print(f"Total: {len(products)}")
