"""
Find products that are still truncated at exactly 300 chars and re-fetch them
with a different strategy (trying body content instead of just meta)
"""
import json, requests, time
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

session = requests.Session()
session.headers.update(HEADERS)

# Find the still-truncated ones (exactly 300 chars, or ending mid-word)
truncated = []
for p in products:
    d = p.get('description', '')
    if len(d) == 300 or (len(d) > 200 and not d.rstrip().endswith(('.', '!', '?', '"', "'"))):
        truncated.append(p)

print(f'Found {len(truncated)} potentially still-truncated descriptions')
print()

updated = 0
for i, p in enumerate(truncated):
    slug = p['id']
    url = f'https://www.ezup.ca/products/{slug}'
    print(f'[{i+1}/{len(truncated)}] {p["name"][:50]}... ({len(p.get("description",""))} chars)', end=' ')
    
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            # Try the Shopify JSON API
            json_url = f'https://www.ezup.ca/products/{slug}.json'
            r2 = session.get(json_url, timeout=15)
            if r2.status_code == 200:
                data = r2.json()
                body_html = data.get('product', {}).get('body_html', '')
                if body_html:
                    soup = BeautifulSoup(body_html, 'html.parser')
                    text = soup.get_text(separator=' ', strip=True)
                    if len(text) > len(p.get('description', '')):
                        p['description'] = text
                        print(f'UPDATED via JSON API ({len(text)} chars)')
                        updated += 1
                        continue
            print(f'SKIP (HTTP {r.status_code})')
            continue
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Strategy 1: Body description divs
        best = ''
        for sel in ['.product__description', '.product-description', '.rte', 
                    '.product-single__description', '[data-product-description]',
                    '.product__info-description']:
            el = soup.select_one(sel)
            if el:
                text = el.get_text(separator=' ', strip=True)
                if len(text) > len(best):
                    best = text
        
        # Strategy 2: Shopify JSON in page
        scripts = soup.find_all('script', type='application/json')
        for script in scripts:
            try:
                data = json.loads(script.string or '')
                if isinstance(data, dict):
                    body = data.get('product', {}).get('body_html', '') or data.get('body_html', '')
                    if body:
                        s = BeautifulSoup(body, 'html.parser')
                        text = s.get_text(separator=' ', strip=True)
                        if len(text) > len(best):
                            best = text
            except:
                pass
        
        # Strategy 3: Meta description (sometimes different from what we got)
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta:
            meta_text = meta.get('content', '').strip()
            if len(meta_text) > len(best):
                best = meta_text
        
        if best and len(best) > len(p.get('description', '')):
            p['description'] = best
            print(f'UPDATED ({len(best)} chars)')
            updated += 1
        else:
            print(f'NO IMPROVEMENT (best={len(best)}, current={len(p.get("description",""))})')
    
    except Exception as e:
        print(f'ERROR: {e}')
    
    time.sleep(0.5)

with open('data/products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f'\nDone! Updated: {updated} out of {len(truncated)} checked')
