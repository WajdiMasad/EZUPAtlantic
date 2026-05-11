"""
Extract ALL variant images from ezup.ca Shopify JSON API
Downloads every color/size variant image locally
"""
import json, requests, os, re, time
from urllib.parse import urlparse

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
IMG_DIR = r'e:\EZUP\images\products'
os.makedirs(IMG_DIR, exist_ok=True)

with open(r'e:\EZUP\data\products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

session = requests.Session()
session.headers.update(HEADERS)

total_images = 0

def download_img(url, filename):
    global total_images
    if not url:
        return None
    url = url.strip()
    if url.startswith('//'):
        url = 'https:' + url
    filepath = os.path.join(IMG_DIR, filename)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
        return f'images/products/{filename}'
    try:
        r = session.get(url, timeout=15)
        if r.status_code == 200 and len(r.content) > 500:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            total_images += 1
            return f'images/products/{filename}'
    except:
        pass
    return None

def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

for i, p in enumerate(products):
    pid = p['id']
    url = f"https://www.ezup.ca/products/{pid}.json"
    print(f"[{i+1}/{len(products)}] {p['name'][:45]}... ", end="", flush=True)
    
    try:
        r = session.get(url, timeout=10)
        if r.status_code == 429:
            print("rate limited, waiting 5s...")
            time.sleep(5)
            r = session.get(url, timeout=10)
        
        if r.status_code != 200:
            print(f"HTTP {r.status_code}")
            time.sleep(1)
            continue
        
        data = r.json().get('product', {})
        
        # Get ALL product images
        all_images = data.get('images', [])
        product_images = []
        
        for img_data in all_images:
            img_url = img_data.get('src', '')
            if not img_url:
                continue
            # Get variant IDs this image is associated with
            variant_ids = img_data.get('variant_ids', [])
            img_id = img_data.get('id', '')
            
            # Download image
            ext = 'jpg'
            if '.webp' in img_url:
                ext = 'webp'
            elif '.png' in img_url:
                ext = 'png'
            
            filename = f"{pid}-{img_id}.{ext}"
            local_path = download_img(img_url, filename)
            
            if local_path:
                product_images.append({
                    'src': local_path,
                    'variant_ids': variant_ids,
                    'alt': img_data.get('alt', ''),
                })
        
        # Update main product image to first image
        if product_images:
            p['img'] = product_images[0]['src']
            p['images'] = product_images
        
        # Update variants with their specific image
        variants = data.get('variants', [])
        if variants:
            variant_list = []
            for v in variants:
                vid = v.get('id')
                vimg = None
                # Find image for this variant
                if vid:
                    for pi in product_images:
                        if vid in pi.get('variant_ids', []):
                            vimg = pi['src']
                            break
                
                variant_list.append({
                    'name': v.get('title', ''),
                    'price': float(v.get('price', 0)),
                    'priceDisplay': f"${float(v.get('price', 0)):,.2f}",
                    'available': v.get('available', True),
                    'sku': v.get('sku', ''),
                    'img': vimg,
                })
            p['variants'] = variant_list
        
        # Update options
        options = data.get('options', [])
        if options:
            p['options'] = [{'name': o['name'], 'values': o['values']} for o in options if o.get('values')]
        
        img_count = len(product_images)
        var_count = len(variants) if variants else 0
        print(f"{img_count} images, {var_count} variants")
        
    except Exception as e:
        print(f"error: {str(e)[:40]}")
    
    time.sleep(0.5)

with open(r'e:\EZUP\data\products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f"\nDone! Downloaded {total_images} new images.")
print(f"Total products: {len(products)}")
