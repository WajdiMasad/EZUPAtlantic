"""
EZUP Atlantic - Product Scraper
Scrapes all products + images from ezup.ca collections
"""
import requests, json, os, time, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}
IMG_DIR = r'e:\EZUP\images\products'
os.makedirs(IMG_DIR, exist_ok=True)

COLLECTIONS = [
    ('https://www.ezup.ca/collections/shelters', 'canopy-tents'),
    ('https://www.ezup.ca/collections/custom-shelters', 'custom'),
    ('https://www.ezup.ca/collections/accessories', 'accessories'),
    ('https://www.ezup.ca/collections/camping', 'camping'),
    ('https://www.ezup.ca/collections/lighting-power', 'lighting'),
    ('https://www.ezup.ca/collections/chairs-tables', 'tables-chairs'),
    ('https://www.ezup.ca/collections/custom-flags', 'custom-flags'),
    ('https://www.ezup.ca/collections/custom-banners', 'custom-banners'),
    ('https://www.ezup.ca/collections/sidewalls', 'sidewalls'),
    ('https://www.ezup.ca/collections/wind-protection', 'anchoring'),
    ('https://www.ezup.ca/collections/bags-accessories', 'bags'),
    ('https://www.ezup.ca/collections/custom-sidewalls-railskirts', 'custom-sidewalls'),
    ('https://www.ezup.ca/collections/display-products', 'displays'),
    ('https://www.ezup.ca/collections/custom-packages', 'custom-packages'),
    ('https://www.ezup.ca/collections/umbrellas', 'umbrellas'),
    ('https://www.ezup.ca/collections/skyfuze-lighting', 'skyfuze'),
]

session = requests.Session()
session.headers.update(HEADERS)

all_products = []
seen_urls = set()

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def download_image(url, filename):
    """Download image, trying multiple URL formats"""
    if not url:
        return None
    
    # Clean up URL
    url = url.strip()
    if url.startswith('//'):
        url = 'https:' + url
    
    filepath = os.path.join(IMG_DIR, filename)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        print(f'  [CACHED] {filename}')
        return f'images/products/{filename}'
    
    # Try various URL transformations
    urls_to_try = [url]
    
    # If it's an ezup.ca CDN url, try cdn.shopify.com
    if 'ezup.ca/cdn/shop' in url:
        shopify_url = url.replace('www.ezup.ca/cdn/shop', 'cdn.shopify.com/s/files/1')
        urls_to_try.append(shopify_url)
    
    # Try without query params
    base_url = url.split('?')[0]
    if base_url != url:
        urls_to_try.append(base_url)
    
    for try_url in urls_to_try:
        try:
            r = session.get(try_url, timeout=15, stream=True)
            if r.status_code == 200 and len(r.content) > 500:
                with open(filepath, 'wb') as f:
                    f.write(r.content)
                print(f'  [OK] {filename} ({len(r.content)} bytes) from {try_url[:60]}...')
                return f'images/products/{filename}'
        except Exception as e:
            pass
    
    print(f'  [FAIL] {filename}')
    return None

def get_product_image_url(soup):
    """Extract the best product image URL from a product card"""
    # Try various selectors
    for selector in ['img.product-card__image', 'img.card__image', '.product-card img', '.card img', 'img[srcset]', 'img']:
        imgs = soup.select(selector)
        for img in imgs:
            # Try srcset first (higher quality)
            srcset = img.get('srcset', '')
            if srcset:
                # Get the largest image from srcset
                parts = [p.strip() for p in srcset.split(',') if p.strip()]
                if parts:
                    last = parts[-1].strip().split(' ')[0]
                    if '/cdn/' in last or 'shopify' in last:
                        return last
            
            src = img.get('src', '')
            if src and ('/cdn/' in src or 'shopify' in src) and 'svg' not in src:
                return src
    return None

def scrape_collection(url, category):
    """Scrape all products from a collection page"""
    products = []
    page = 1
    
    while True:
        page_url = f"{url}?page={page}" if page > 1 else url
        print(f'\nScraping: {page_url}')
        
        try:
            r = session.get(page_url, timeout=15)
            if r.status_code != 200:
                print(f'  Status {r.status_code}, stopping')
                break
        except Exception as e:
            print(f'  Error: {e}')
            break
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Find product cards - try multiple selectors
        cards = soup.select('.product-card, .card--product, .product-grid-item, [class*="product-card"]')
        if not cards:
            # Try finding product links
            cards = soup.select('a[href*="/products/"]')
            # Deduplicate
            seen_hrefs = set()
            unique_cards = []
            for c in cards:
                href = c.get('href', '')
                if href and href not in seen_hrefs and '/products/' in href:
                    seen_hrefs.add(href)
                    unique_cards.append(c)
            cards = unique_cards
        
        if not cards:
            print(f'  No products found on page {page}')
            break
        
        found_new = False
        for card in cards:
            # Get product URL
            link = card if card.name == 'a' else card.find('a', href=True)
            if not link:
                continue
            href = link.get('href', '')
            if not href or '/products/' not in href:
                continue
            
            product_url = urljoin('https://www.ezup.ca', href)
            
            if product_url in seen_urls:
                continue
            seen_urls.add(product_url)
            found_new = True
            
            # Get product name
            name_el = card.select_one('.card__title, .product-card__title, h3, h2, .card__heading')
            name = name_el.get_text(strip=True) if name_el else href.split('/products/')[-1].replace('-', ' ').title()
            
            # Get price
            price_el = card.select_one('.price__regular .price-item, .price-item--regular, .price, [class*="price"]')
            price_text = price_el.get_text(strip=True) if price_el else ''
            
            # Parse numeric price
            price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
            price_num = float(price_match.group(1).replace(',', '')) if price_match else 0
            
            # Get image
            img_url = get_product_image_url(card)
            
            # Create slug
            slug = slugify(name)
            
            product = {
                'id': slug,
                'name': name,
                'category': category,
                'price': price_num,
                'priceDisplay': price_text if price_text else 'Contact for pricing',
                'product_url': product_url,
                'img_cdn': img_url,
                'img': '',  # Will be set after download
            }
            
            products.append(product)
            print(f'  Found: {name} - {price_text}')
        
        if not found_new:
            break
        
        page += 1
        time.sleep(0.5)
    
    return products

def scrape_product_detail(product):
    """Scrape individual product page for details"""
    try:
        r = session.get(product['product_url'], timeout=15)
        if r.status_code != 200:
            return
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Get description from meta tag
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            product['description'] = meta_desc.get('content', '')[:300]
        
        # Get better image from product page
        og_img = soup.find('meta', attrs={'property': 'og:image'})
        if og_img:
            product['img_cdn'] = og_img.get('content', product.get('img_cdn', ''))
        
    except Exception as e:
        print(f'  Detail error for {product["name"]}: {e}')

# ===== MAIN =====
print("=" * 60)
print("EZUP Atlantic Product Scraper")
print("=" * 60)

for url, category in COLLECTIONS:
    products = scrape_collection(url, category)
    all_products.extend(products)
    time.sleep(1)

print(f'\n\nTotal products found: {len(all_products)}')

# Scrape individual product pages for descriptions
print('\n--- Scraping product details ---')
for i, p in enumerate(all_products):
    print(f'  [{i+1}/{len(all_products)}] {p["name"][:50]}...')
    scrape_product_detail(p)
    time.sleep(0.3)

# Download images
print('\n--- Downloading images ---')
for p in all_products:
    img_url = p.get('img_cdn', '')
    if img_url:
        ext = 'webp' if 'webp' in img_url else 'jpg'
        filename = f"{p['id']}.{ext}"
        local_path = download_image(img_url, filename)
        if local_path:
            p['img'] = local_path
        else:
            p['img'] = img_url  # Fallback to CDN URL
    
    # Clean up internal fields
    p.pop('img_cdn', None)
    p.pop('product_url', None)

# Save JSON
output_path = r'e:\EZUP\data\products.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

print(f'\n\nDone! {len(all_products)} products saved to {output_path}')
print(f'Images saved to {IMG_DIR}')
