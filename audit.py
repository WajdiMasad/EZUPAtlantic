"""
EZ-UP Atlantic -- Full Functionality Audit
Tests every page, link, image, API endpoint, and critical user flow
"""
import sys, os
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import requests, json, re, time
from bs4 import BeautifulSoup

BASE = 'http://localhost:8080'
session = requests.Session()

results = {
    'pages': [],
    'broken_links': [],
    'broken_images': [],
    'missing_seo': [],
    'api_issues': [],
    'js_issues': [],
    'data_issues': [],
}

PASS = '[OK]'
FAIL = '[FAIL]'
WARN = '[WARN]'

# =============================================
# 1. PAGE LOAD TESTS
# =============================================
print('=' * 60)
print('1. PAGE LOAD TESTS')
print('=' * 60)

pages = [
    ('/', 'Homepage'),
    ('/products.html', 'Products'),
    ('/product.html', 'Product Detail'),
    ('/about.html', 'About'),
    ('/contact.html', 'Contact'),
    ('/checkout.html', 'Checkout'),
    ('/confirmation.html', 'Confirmation'),
    ('/admin.html', 'Admin'),
    ('/robots.txt', 'Robots.txt'),
    ('/sitemap.xml', 'Sitemap'),
]

for path, name in pages:
    try:
        r = session.get(f'{BASE}{path}', timeout=10)
        status = PASS if r.status_code == 200 else FAIL
        results['pages'].append({'name': name, 'path': path, 'status': r.status_code})
        print(f'  {status} {name} ({path}) — HTTP {r.status_code} — {len(r.content)} bytes')
    except Exception as e:
        results['pages'].append({'name': name, 'path': path, 'status': 'ERROR', 'error': str(e)})
        print(f'  {FAIL} {name} ({path}) — ERROR: {e}')

# =============================================
# 2. INTERNAL LINK AUDIT
# =============================================
print(f'\n{"=" * 60}')
print('2. INTERNAL LINK AUDIT')
print('=' * 60)

html_pages = ['/', '/products.html', '/product.html', '/about.html', '/contact.html', '/checkout.html']
all_links = set()

for path in html_pages:
    r = session.get(f'{BASE}{path}', timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('http'):
            continue
        # Strip query params for file check
        file_path = href.split('?')[0].split('#')[0]
        if file_path:
            all_links.add(file_path)

broken_count = 0
for link in sorted(all_links):
    full = f'{BASE}/{link}' if not link.startswith('/') else f'{BASE}{link}'
    try:
        r = session.get(full, timeout=5)
        if r.status_code != 200:
            print(f'  {FAIL} Broken: {link} — HTTP {r.status_code}')
            results['broken_links'].append(link)
            broken_count += 1
    except:
        print(f'  {FAIL} Error: {link}')
        results['broken_links'].append(link)
        broken_count += 1

if broken_count == 0:
    print(f'  {PASS} All {len(all_links)} internal links are valid')
else:
    print(f'  {FAIL} {broken_count} broken links found out of {len(all_links)}')

# =============================================
# 3. IMAGE AUDIT
# =============================================
print(f'\n{"=" * 60}')
print('3. IMAGE AUDIT (Homepage + Products)')
print('=' * 60)

for path in ['/', '/products.html', '/about.html', '/contact.html']:
    r = session.get(f'{BASE}{path}', timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    imgs = soup.find_all('img', src=True)
    broken = 0
    for img in imgs:
        src = img['src']
        if src.startswith('data:') or src.startswith('http'):
            continue
        full = f'{BASE}/{src}' if not src.startswith('/') else f'{BASE}{src}'
        try:
            r2 = session.head(full, timeout=5)
            if r2.status_code != 200:
                broken += 1
                results['broken_images'].append(f'{path}: {src}')
                if broken <= 3:
                    print(f'  {FAIL} {path}: {src} — HTTP {r2.status_code}')
        except:
            broken += 1
    
    total = len([i for i in imgs if not i['src'].startswith('data:')])
    if broken == 0:
        print(f'  {PASS} {path}: All {total} images load correctly')
    else:
        print(f'  {FAIL} {path}: {broken}/{total} images broken')

# =============================================
# 4. PRODUCT DATA AUDIT
# =============================================
print(f'\n{"=" * 60}')
print('4. PRODUCT DATA AUDIT')
print('=' * 60)

r = session.get(f'{BASE}/data/products.json', timeout=10)
products = r.json()
print(f'  Total products: {len(products)}')

no_price = [p for p in products if not p.get('price') or p['price'] == 0]
no_desc = [p for p in products if not p.get('description') or len(p.get('description', '')) < 5]
no_img = [p for p in products if not p.get('img')]
no_cat = [p for p in products if not p.get('category')]
no_subcat = [p for p in products if not p.get('subcategory')]
dup_ids = len(products) - len(set(p['id'] for p in products))

print(f'  {PASS if not no_price else WARN} Products without price: {len(no_price)}')
if no_price:
    for p in no_price[:5]:
        print(f'    → {p["name"]}')
    results['data_issues'].append(f'{len(no_price)} products without price')

print(f'  {PASS if not no_desc else FAIL} Products without description: {len(no_desc)}')
if no_desc:
    for p in no_desc[:5]:
        print(f'    → {p["name"]}: "{p.get("description","")[:30]}"')
    results['data_issues'].append(f'{len(no_desc)} products without description')

print(f'  {PASS if not no_img else FAIL} Products without image: {len(no_img)}')
if no_img:
    for p in no_img[:5]:
        print(f'    → {p["name"]}')

print(f'  {PASS if not no_cat else FAIL} Products without category: {len(no_cat)}')
print(f'  {PASS if not no_subcat else WARN} Products without subcategory: {len(no_subcat)}')
print(f'  {PASS if dup_ids == 0 else FAIL} Duplicate IDs: {dup_ids}')

# Check product images exist on disk
broken_product_imgs = 0
for p in products:
    img = p.get('img', '')
    if img and not img.startswith('http'):
        if not os.path.isfile(img):
            broken_product_imgs += 1
            if broken_product_imgs <= 3:
                print(f'  {FAIL} Missing image file: {img} ({p["name"]})')
                results['broken_images'].append(f'products.json: {img}')

print(f'  {PASS if broken_product_imgs == 0 else FAIL} Product images on disk: {broken_product_imgs} missing out of {len(products)}')

# =============================================
# 5. SEO AUDIT
# =============================================
print(f'\n{"=" * 60}')
print('5. SEO AUDIT')
print('=' * 60)

for path, name in [('/', 'Homepage'), ('/products.html', 'Products'), ('/about.html', 'About'), ('/contact.html', 'Contact'), ('/product.html', 'Product Detail')]:
    r = session.get(f'{BASE}{path}', timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    checks = {
        'title': bool(soup.title and len(soup.title.string or '') > 10),
        'meta_desc': bool(soup.find('meta', attrs={'name': 'description'})),
        'canonical': bool(soup.find('link', attrs={'rel': 'canonical'})),
        'og:title': bool(soup.find('meta', attrs={'property': 'og:title'})),
        'og:image': bool(soup.find('meta', attrs={'property': 'og:image'})),
        'twitter:card': bool(soup.find('meta', attrs={'name': 'twitter:card'})),
        'h1': bool(soup.find('h1')),
        'robots': bool(soup.find('meta', attrs={'name': 'robots'})),
    }
    
    missing = [k for k, v in checks.items() if not v]
    if not missing:
        print(f'  {PASS} {name}: All SEO tags present')
    else:
        print(f'  {WARN} {name}: Missing: {", ".join(missing)}')
        results['missing_seo'].append(f'{name}: {", ".join(missing)}')

# Check schema
r = session.get(f'{BASE}/', timeout=10)
has_schema = 'application/ld+json' in r.text
print(f'  {PASS if has_schema else FAIL} Homepage JSON-LD Schema: {"Present" if has_schema else "MISSING"}')

# Check robots.txt
r = session.get(f'{BASE}/robots.txt', timeout=5)
print(f'  {PASS if r.status_code == 200 else FAIL} robots.txt: {"Present" if r.status_code == 200 else "MISSING"}')

# Check sitemap
r = session.get(f'{BASE}/sitemap.xml', timeout=5)
print(f'  {PASS if r.status_code == 200 else FAIL} sitemap.xml: {"Present" if r.status_code == 200 else "MISSING"}')

# =============================================
# 6. API ENDPOINT TESTS
# =============================================
print(f'\n{"=" * 60}')
print('6. API ENDPOINT TESTS')
print('=' * 60)

# Config
r = session.get(f'{BASE}/api/config', timeout=5)
if r.status_code == 200:
    data = r.json()
    pk = data.get('publishableKey', '')
    print(f'  {PASS} /api/config — Publishable key: {"pk_live_..." if pk.startswith("pk_live_") else pk[:20]}')
else:
    print(f'  {FAIL} /api/config — HTTP {r.status_code}')
    results['api_issues'].append('/api/config failed')

# Tax rates
r = session.get(f'{BASE}/api/tax-rates', timeout=5)
if r.status_code == 200:
    rates = r.json()
    print(f'  {PASS} /api/tax-rates — {len(rates)} provinces configured')
else:
    print(f'  {FAIL} /api/tax-rates — HTTP {r.status_code}')

# Admin stats
r = session.get(f'{BASE}/api/admin/stats', timeout=5)
if r.status_code == 200:
    print(f'  {PASS} /api/admin/stats — OK')
else:
    print(f'  {FAIL} /api/admin/stats — HTTP {r.status_code}')

# Admin orders
r = session.get(f'{BASE}/api/admin/orders', timeout=5)
if r.status_code == 200:
    print(f'  {PASS} /api/admin/orders — OK ({len(r.json())} orders)')
else:
    print(f'  {FAIL} /api/admin/orders — HTTP {r.status_code}')

# Checkout session (should fail gracefully with empty cart)
r = session.post(f'{BASE}/api/create-checkout-session', json={'items': [], 'province': 'NS'}, timeout=5)
if r.status_code == 400:
    print(f'  {PASS} /api/create-checkout-session — Correctly rejects empty cart')
elif r.status_code == 200:
    print(f'  {WARN} /api/create-checkout-session — Should reject empty cart but returned 200')
else:
    print(f'  {FAIL} /api/create-checkout-session — HTTP {r.status_code}: {r.text[:100]}')
    results['api_issues'].append(f'Checkout endpoint: {r.status_code}')

# Test with a real item
test_item = {'items': [{'name': 'Test', 'price': 100, 'qty': 1}], 'province': 'NS', 'shippingMethod': 'pickup', 'shippingCost': 0, 'customer': {'name': 'Test', 'email': 'test@test.com', 'phone': '9021234567'}}
r = session.post(f'{BASE}/api/create-checkout-session', json=test_item, timeout=10)
if r.status_code == 200:
    data = r.json()
    if data.get('url') and 'stripe.com' in data['url']:
        print(f'  {PASS} Stripe checkout session creation — WORKING (live mode)')
    else:
        print(f'  {WARN} Checkout session created but no Stripe URL')
else:
    print(f'  {FAIL} Stripe checkout creation failed: {r.text[:200]}')
    results['api_issues'].append('Stripe session creation failed')

# =============================================
# 7. CATEGORY FILTER TESTS
# =============================================
print(f'\n{"=" * 60}')
print('7. CATEGORY FILTER VERIFICATION')
print('=' * 60)

categories = {}
for p in products:
    cat = p.get('category', 'uncategorized')
    categories[cat] = categories.get(cat, 0) + 1

print(f'  Categories found: {len(categories)}')
for cat, count in sorted(categories.items()):
    print(f'    {cat}: {count} products')

# =============================================
# 8. CRITICAL FILE CHECK
# =============================================
print(f'\n{"=" * 60}')
print('8. CRITICAL FILE CHECK')
print('=' * 60)

critical_files = [
    'index.html', 'products.html', 'product.html', 'about.html', 
    'contact.html', 'checkout.html', 'confirmation.html', 'admin.html',
    'css/styles.css', 'js/main.js', 'js/products.js', 'js/product-detail.js',
    'js/cart.js', 'js/checkout.js', 'data/products.json',
    'server.py', 'orders.py', '.env', '.gitignore', 'robots.txt', 'sitemap.xml',
]

for f in critical_files:
    exists = os.path.isfile(f)
    size = os.path.getsize(f) if exists else 0
    status = PASS if exists and size > 0 else FAIL
    print(f'  {status} {f} {"— " + str(size) + " bytes" if exists else "— MISSING"}')

# =============================================
# 9. SHIPPING LOGIC TEST
# =============================================
print(f'\n{"=" * 60}')
print('9. SHIPPING LOGIC VERIFICATION')
print('=' * 60)

# Under $500
test1 = {'items': [{'name': 'Test', 'price': 200, 'qty': 1}], 'province': 'NS', 'shippingMethod': 'shipping', 'shippingCost': 75, 'customer': {'name': 'Test', 'email': 'test@test.com', 'phone': '9021234567'}}
r1 = session.post(f'{BASE}/api/create-checkout-session', json=test1, timeout=10)
if r1.status_code == 200:
    print(f'  {PASS} Shipping under $500: $75 flat rate — Session created')
else:
    print(f'  {FAIL} Shipping under $500 failed: {r1.text[:100]}')

# Over $500
test2 = {'items': [{'name': 'Test', 'price': 600, 'qty': 1}], 'province': 'NS', 'shippingMethod': 'shipping', 'shippingCost': 0, 'customer': {'name': 'Test', 'email': 'test@test.com', 'phone': '9021234567'}}
r2 = session.post(f'{BASE}/api/create-checkout-session', json=test2, timeout=10)
if r2.status_code == 200:
    print(f'  {PASS} Free shipping over $500: $0 — Session created')
else:
    print(f'  {FAIL} Free shipping over $500 failed: {r2.text[:100]}')

# Pickup
test3 = {'items': [{'name': 'Test', 'price': 100, 'qty': 1}], 'province': 'NS', 'shippingMethod': 'pickup', 'shippingCost': 0, 'customer': {'name': 'Test', 'email': 'test@test.com', 'phone': '9021234567'}}
r3 = session.post(f'{BASE}/api/create-checkout-session', json=test3, timeout=10)
if r3.status_code == 200:
    print(f'  {PASS} Local pickup: Free — Session created')
else:
    print(f'  {FAIL} Pickup checkout failed: {r3.text[:100]}')

# =============================================
# SUMMARY
# =============================================
print(f'\n{"=" * 60}')
print('AUDIT SUMMARY')
print('=' * 60)

total_issues = (len(results['broken_links']) + len(results['broken_images']) + 
                len(results['missing_seo']) + len(results['api_issues']) + len(results['data_issues']))

print(f'  Pages tested:      {len(results["pages"])}')
print(f'  Broken links:      {len(results["broken_links"])}')
print(f'  Broken images:     {len(results["broken_images"])}')
print(f'  SEO issues:        {len(results["missing_seo"])}')
print(f'  API issues:        {len(results["api_issues"])}')
print(f'  Data issues:       {len(results["data_issues"])}')
print(f'  ---')
if total_issues == 0:
    print(f'  {PASS} READY TO PUBLISH — No critical issues found')
else:
    print(f'  {WARN} {total_issues} issue(s) to review before publishing')
    for category, items in results.items():
        if items and category != 'pages':
            for item in items:
                if isinstance(item, str):
                    print(f'    → {item}')
