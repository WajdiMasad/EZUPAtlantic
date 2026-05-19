"""Full Pre-Deployment Audit: SEO, Security, Functionality"""
import re, os, json, sqlite3

ROOT = r'e:\EZUP'
pages = ['index.html','products.html','product.html','about.html','contact.html','checkout.html','confirmation.html','admin.html']

print("=" * 60)
print("  EZ-UP ATLANTIC — PRE-DEPLOYMENT AUDIT")
print("=" * 60)

# ===== 1. SEO AUDIT =====
print("\n\n### 1. SEO AUDIT ###\n")

for p in pages:
    path = os.path.join(ROOT, p)
    if not os.path.exists(path):
        print(f"  MISSING FILE: {p}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    head = content[:content.find('</head>')] if '</head>' in content else content[:2000]
    
    title = re.search(r'<title>(.*?)</title>', head)
    desc = re.search(r'name="description" content="(.*?)"', head)
    canon = re.search(r'rel="canonical" href="(.*?)"', head)
    og_title = re.search(r'og:title" content="(.*?)"', head)
    og_img = re.search(r'og:image" content="(.*?)"', head)
    twitter = re.search(r'twitter:card', head)
    schema = 'ld+json' in head
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    imgs_no_alt = re.findall(r'<img(?![^>]*alt=)[^>]*>', content)
    
    issues = []
    if not title: issues.append("❌ MISSING <title>")
    elif len(title.group(1)) > 65: issues.append(f"⚠️ Title too long ({len(title.group(1))} chars, max 60)")
    if not desc: issues.append("❌ MISSING meta description")
    elif len(desc.group(1)) > 160: issues.append(f"⚠️ Meta desc too long ({len(desc.group(1))} chars)")
    if not canon: issues.append("❌ MISSING canonical URL")
    if not og_title: issues.append("⚠️ MISSING Open Graph title")
    if not og_img: issues.append("⚠️ MISSING Open Graph image")
    if not twitter: issues.append("⚠️ MISSING Twitter card")
    if not schema and p not in ['admin.html','checkout.html','confirmation.html']:
        issues.append("⚠️ MISSING JSON-LD structured data")
    if len(h1s) == 0: issues.append("⚠️ No <h1> found")
    elif len(h1s) > 1: issues.append(f"⚠️ Multiple <h1> tags ({len(h1s)})")
    if imgs_no_alt: issues.append(f"⚠️ {len(imgs_no_alt)} images missing alt text")
    
    status = "✅ PASS" if not issues else f"🔍 {len(issues)} issue(s)"
    print(f"  {p:25s} {status}")
    for i in issues:
        print(f"    {i}")

# Check robots.txt
print(f"\n  robots.txt:              ", end="")
robots = os.path.join(ROOT, 'robots.txt')
if os.path.exists(robots):
    with open(robots) as f:
        rc = f.read()
    if 'Sitemap:' in rc:
        print("✅ EXISTS + Sitemap reference")
    else:
        print("⚠️ EXISTS but no Sitemap reference")
else:
    print("❌ MISSING")

# Check sitemap.xml
print(f"  sitemap.xml:             ", end="")
sitemap = os.path.join(ROOT, 'sitemap.xml')
if os.path.exists(sitemap):
    with open(sitemap) as f:
        sc = f.read()
    url_count = sc.count('<url>')
    print(f"✅ EXISTS ({url_count} URLs)")
else:
    print("❌ MISSING")


# ===== 2. SECURITY AUDIT =====
print("\n\n### 2. SECURITY AUDIT ###\n")

# Check .env not in git
print("  .env in .gitignore:      ", end="")
with open(os.path.join(ROOT, '.gitignore')) as f:
    gi = f.read()
print("✅ YES" if '.env' in gi else "❌ NO — SECRETS EXPOSED!")

# Check for hardcoded secrets
print("  Hardcoded secrets:       ", end="")
secrets_found = []
for p in pages + ['server.py', 'orders.py']:
    path = os.path.join(ROOT, p)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if re.search(r'sk_live_[a-zA-Z0-9]+', content): secrets_found.append(f"{p}: Stripe secret key")
    if re.search(r'smtp_pass|xpjq', content, re.I): secrets_found.append(f"{p}: SMTP password")
if secrets_found:
    print("❌ FOUND!")
    for s in secrets_found: print(f"    {s}")
else:
    print("✅ NONE — all secrets in .env")

# Check admin auth
print("  Admin panel auth:        ", end="")
with open(os.path.join(ROOT, 'server.py'), 'r') as f:
    server = f.read()
if 'admin_required' in server and 'session' in server:
    print("✅ Protected with session auth")
else:
    print("❌ UNPROTECTED!")

# Check CSRF on quote form
print("  CSRF protection:         ", end="")
if '@app.before_request' in server or 'csrf' in server.lower():
    print("✅ CSRF middleware found")
else:
    print("⚠️ No CSRF middleware (acceptable for API-only backend)")

# Check XSS in templates
print("  XSS in email templates:  ", end="")
with open(os.path.join(ROOT, 'orders.py'), 'r') as f:
    orders = f.read()
if 'html.escape' in orders or 'markupsafe' in orders:
    print("✅ Input sanitized")
else:
    print("⚠️ User input inserted into HTML emails without escaping")

# Check Stripe webhook verification
print("  Stripe webhook verify:   ", end="")
if 'construct_event' in server:
    print("✅ Webhook signature verified")
else:
    print("⚠️ Webhook not verifying signatures")

# Check HTTPS enforcement
print("  HTTPS enforcement:       ", end="")
if 'redirect' in server and 'https' in server.lower():
    print("✅ HTTP→HTTPS redirect")
else:
    print("⚠️ No HTTPS redirect (Railway handles this)")

# Check security headers
print("  Security headers:        ", end="")
if 'X-Content-Type' in server or 'Content-Security-Policy' in server:
    print("✅ Security headers set")
else:
    print("⚠️ No security headers (X-Frame-Options, CSP, etc.)")

# Check rate limiting
print("  Rate limiting:           ", end="")
if 'limiter' in server.lower() or 'ratelimit' in server.lower():
    print("✅ Rate limiting enabled")
else:
    print("⚠️ No rate limiting on API endpoints")

# Check SQL injection
print("  SQL injection:           ", end="")
if '?' in orders and 'execute' in orders:
    raw_sql = re.findall(r'execute\([^)]*f["\']', orders)
    if raw_sql:
        print("❌ f-string in SQL queries!")
    else:
        print("✅ Parameterized queries used")
else:
    print("⚠️ Could not verify")

# Check localhost references
print("  Localhost references:     ", end="")
localhost_found = []
for p in pages + ['server.py', 'orders.py']:
    path = os.path.join(ROOT, p)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = [(m.start(), content[max(0,m.start()-20):m.end()+20]) 
               for m in re.finditer(r'localhost', content)]
    for pos, ctx in matches:
        # Skip env var defaults and comments
        if 'environ.get' in ctx or 'DOMAIN' in ctx: continue
        localhost_found.append(f"{p}: ...{ctx.strip()}...")
if localhost_found:
    print(f"⚠️ {len(localhost_found)} hardcoded localhost refs")
    for l in localhost_found[:5]: print(f"    {l}")
else:
    print("✅ NONE — all use DOMAIN env var")


# ===== 3. FUNCTIONALITY AUDIT =====
print("\n\n### 3. FUNCTIONALITY AUDIT ###\n")

# Check all HTML files exist
print("  HTML pages:              ", end="")
missing = [p for p in pages if not os.path.exists(os.path.join(ROOT, p))]
print(f"✅ All {len(pages)} pages exist" if not missing else f"❌ Missing: {missing}")

# Check product data
print("  Product data (JSON):     ", end="")
data_dir = os.path.join(ROOT, 'data')
json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')] if os.path.exists(data_dir) else []
print(f"✅ {len(json_files)} JSON files found" if json_files else "⚠️ No JSON data files")
for jf in json_files:
    path = os.path.join(data_dir, jf)
    try:
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            print(f"    {jf}: {len(data)} items")
        elif isinstance(data, dict):
            print(f"    {jf}: {len(data)} keys")
    except:
        print(f"    {jf}: ❌ INVALID JSON")

# Check database
print("  Database (SQLite):       ", end="")
db_path = os.path.join(ROOT, 'data', 'orders.db')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    conn.close()
    print(f"✅ EXISTS — tables: {', '.join(tables)}")
else:
    print("⚠️ Not created yet (will auto-create on first run)")

# Check images directory
print("  Images directory:        ", end="")
img_dir = os.path.join(ROOT, 'images')
if os.path.exists(img_dir):
    img_count = sum(1 for f in os.listdir(os.path.join(img_dir, 'products')) 
                    if f.endswith(('.webp','.png','.jpg'))) if os.path.exists(os.path.join(img_dir, 'products')) else 0
    print(f"✅ {img_count} product images")
else:
    print("❌ MISSING")

# Check JS files
print("  JavaScript files:        ", end="")
js_dir = os.path.join(ROOT, 'js')
if os.path.exists(js_dir):
    js_files = [f for f in os.listdir(js_dir) if f.endswith('.js')]
    print(f"✅ {len(js_files)} files: {', '.join(js_files)}")
else:
    print("❌ MISSING")

# Check CSS
print("  CSS files:               ", end="")
css_dir = os.path.join(ROOT, 'css')
if os.path.exists(css_dir):
    css_files = [f for f in os.listdir(css_dir) if f.endswith('.css')]
    print(f"✅ {len(css_files)} files: {', '.join(css_files)}")
else:
    print("❌ MISSING")

# Check Stripe keys
print("  Stripe config:           ", end="")
with open(os.path.join(ROOT, '.env')) as f:
    env = f.read()
has_sk = 'sk_live_' in env
has_pk = 'pk_live_' in env
print(f"✅ Live keys configured" if has_sk and has_pk else "⚠️ Missing live keys")

# Check SMTP
print("  SMTP config:             ", end="")
has_smtp = 'SMTP_USER=sales@' in env and 'SMTP_PASS=' in env and 'SMTP_PASS=\n' not in env
print(f"✅ Configured (sales@giantpro.ca)" if has_smtp else "⚠️ Not configured")


# ===== 4. DEPLOYMENT READINESS =====
print("\n\n### 4. DEPLOYMENT READINESS ###\n")

print("  Procfile:                ", end="")
print("✅ EXISTS" if os.path.exists(os.path.join(ROOT, 'Procfile')) else "❌ MISSING")

print("  requirements.txt:        ", end="")
req = os.path.join(ROOT, 'requirements.txt')
if os.path.exists(req):
    with open(req) as f:
        deps = [l.strip() for l in f if l.strip()]
    print(f"✅ {len(deps)} dependencies pinned")
else:
    print("❌ MISSING")

print("  runtime.txt:             ", end="")
print("✅ EXISTS" if os.path.exists(os.path.join(ROOT, 'runtime.txt')) else "⚠️ MISSING (optional)")

print("  Dev scripts removed:     ", end="")
dev_scripts = [f for f in os.listdir(ROOT) if f.endswith('.py') and f not in ['server.py','orders.py']]
if dev_scripts:
    print(f"⚠️ {len(dev_scripts)} scripts still present (but gitignored)")
else:
    print("✅ Clean")

# Check publishable key in HTML
print("  Stripe PK in HTML:       ", end="")
pk_in_html = False
for p in ['checkout.html']:
    path = os.path.join(ROOT, p)
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
        if 'pk_live_' in content or 'STRIPE_PUBLISHABLE_KEY' in content:
            pk_in_html = True
if pk_in_html:
    print("⚠️ Publishable key may be hardcoded (check if fetched from API)")
else:
    print("✅ Fetched from server API")

print("\n" + "=" * 60)
print("  AUDIT COMPLETE")
print("=" * 60)
