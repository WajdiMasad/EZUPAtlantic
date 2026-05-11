"""
EZ-UP Atlantic — Heavy SEO Optimization
Adds: Open Graph, Twitter Cards, JSON-LD Schema, canonical URLs,
      geo tags, enhanced meta descriptions, preconnect hints
"""

SEO_DATA = {
    'index.html': {
        'title': 'EZ-UP Atlantic | Authorized E-Z UP® Dealer — Pop-Up Canopy Tents in Atlantic Canada',
        'description': "Atlantic Canada's #1 authorized E-Z UP® dealer. Shop professional-grade pop-up canopy tents, custom-printed shelters, event accessories & more. Free shipping over $500. Serving Halifax, Nova Scotia, New Brunswick, PEI & Newfoundland.",
        'keywords': 'E-Z UP, EZ-UP, canopy tents, pop-up tents, Atlantic Canada, Halifax, Nova Scotia, custom canopy, EZ-UP dealer, pop up tent Halifax, canopy tent New Brunswick, event tent PEI, outdoor shelter Newfoundland, custom printed tent, industrial canopy Canada',
        'canonical': 'https://ezupatlantic.ca/',
        'og_type': 'website',
    },
    'products.html': {
        'title': 'Shop All E-Z UP® Products | Canopy Tents, Custom Printing & Accessories — EZ-UP Atlantic',
        'description': 'Browse the full E-Z UP® product catalog. Light duty to industrial grade canopy tents, custom-printed shelters, flags, banners, table covers, sidewalls, anchoring & lighting accessories. All prices in Canadian dollars. Free shipping over $500.',
        'keywords': 'E-Z UP products, canopy tents Canada, pop-up shelter, custom printed canopy, event tent accessories, EZ-UP catalog, buy canopy tent online Canada, industrial pop-up tent, commercial canopy Atlantic Canada',
        'canonical': 'https://ezupatlantic.ca/products.html',
        'og_type': 'website',
    },
    'product.html': {
        'title': 'Product Details | EZ-UP Atlantic — Authorized E-Z UP® Dealer',
        'description': 'View detailed product specifications, pricing, and color options for E-Z UP® professional canopy tents and accessories. Order online with free shipping over $500 to anywhere in Canada.',
        'keywords': 'E-Z UP product details, canopy tent specifications, pop-up tent pricing, EZ-UP shelter Canada',
        'canonical': 'https://ezupatlantic.ca/product.html',
        'og_type': 'product',
    },
    'about.html': {
        'title': 'About EZ-UP Atlantic | Authorized E-Z UP® Dealer — Giant Promotions Ltd.',
        'description': "EZ-UP Atlantic is a division of Giant Promotions Ltd., Atlantic Canada's authorized E-Z UP® dealer based in Halifax, Nova Scotia. Learn about our commitment to quality event shelters and professional-grade canopy solutions.",
        'keywords': 'EZ-UP Atlantic, Giant Promotions, about us, authorized dealer, E-Z UP Canada, Halifax canopy dealer, Atlantic Canada event supplies',
        'canonical': 'https://ezupatlantic.ca/about.html',
        'og_type': 'website',
    },
    'contact.html': {
        'title': 'Contact EZ-UP Atlantic | Get a Quote — Halifax, Nova Scotia',
        'description': 'Contact EZ-UP Atlantic for quotes, custom printing inquiries, and product support. Visit us at 3797 MacKintosh St, Halifax, NS or call 902-456-6487. Serving all of Atlantic Canada.',
        'keywords': 'contact EZ-UP Atlantic, canopy tent quote, Halifax tent dealer, EZ-UP phone number, custom canopy quote Atlantic Canada, event tent rental inquiry',
        'canonical': 'https://ezupatlantic.ca/contact.html',
        'og_type': 'website',
    },
    'checkout.html': {
        'title': 'Checkout | EZ-UP Atlantic — Secure Payment',
        'description': 'Complete your EZ-UP Atlantic purchase securely. Powered by Stripe with 256-bit SSL encryption. Free shipping on orders over $500. All prices in Canadian dollars.',
        'keywords': 'EZ-UP checkout, buy canopy tent online, secure payment Canada',
        'canonical': 'https://ezupatlantic.ca/checkout.html',
        'og_type': 'website',
    },
    'confirmation.html': {
        'title': 'Order Confirmed | EZ-UP Atlantic',
        'description': 'Your EZ-UP Atlantic order has been confirmed. Thank you for your purchase.',
        'keywords': 'EZ-UP order confirmation',
        'canonical': 'https://ezupatlantic.ca/confirmation.html',
        'og_type': 'website',
    },
}

# Common SEO block to inject after existing meta tags
def build_seo_block(page_data):
    return f"""
  <!-- SEO: Open Graph -->
  <meta property="og:title" content="{page_data['title']}">
  <meta property="og:description" content="{page_data['description']}">
  <meta property="og:type" content="{page_data['og_type']}">
  <meta property="og:url" content="{page_data['canonical']}">
  <meta property="og:image" content="https://ezupatlantic.ca/images/products/custom-vantage-package.webp">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:site_name" content="EZ-UP Atlantic">
  <meta property="og:locale" content="en_CA">

  <!-- SEO: Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{page_data['title']}">
  <meta name="twitter:description" content="{page_data['description']}">
  <meta name="twitter:image" content="https://ezupatlantic.ca/images/products/custom-vantage-package.webp">

  <!-- SEO: Geo & Business -->
  <meta name="geo.region" content="CA-NS">
  <meta name="geo.placename" content="Halifax">
  <meta name="geo.position" content="44.6488;-63.5752">
  <meta name="ICBM" content="44.6488, -63.5752">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="author" content="EZ-UP Atlantic — Giant Promotions Ltd.">

  <!-- Performance: Preconnect -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>"""


import re

for filename, data in SEO_DATA.items():
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update <title>
    content = re.sub(r'<title>.*?</title>', f"<title>{data['title']}</title>", content)

    # 2. Update meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{data["description"]}">',
        content
    )

    # 3. Update or add meta keywords
    if 'meta name="keywords"' in content:
        content = re.sub(
            r'<meta name="keywords" content="[^"]*">',
            f'<meta name="keywords" content="{data["keywords"]}">',
            content
        )
    else:
        content = content.replace(
            f'<meta name="description" content="{data["description"]}">',
            f'<meta name="description" content="{data["description"]}">\n  <meta name="keywords" content="{data["keywords"]}">'
        )

    # 4. Update or add canonical
    if 'rel="canonical"' in content:
        content = re.sub(
            r'<link rel="canonical" href="[^"]*">',
            f'<link rel="canonical" href="{data["canonical"]}">',
            content
        )
    else:
        content = content.replace(
            f'<meta name="keywords" content="{data["keywords"]}">',
            f'<meta name="keywords" content="{data["keywords"]}">\n  <link rel="canonical" href="{data["canonical"]}">'
        )

    # 5. Inject OG/Twitter/Geo block (before </head> if not already there)
    if 'og:title' not in content:
        seo_block = build_seo_block(data)
        content = content.replace('</head>', f'{seo_block}\n</head>')

    with open(filename, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

    print(f'[SEO] Optimized: {filename}')

print('\nDone — all pages optimized.')
