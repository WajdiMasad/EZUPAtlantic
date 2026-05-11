import re

for f in ['about.html','products.html','product.html','contact.html','checkout.html','confirmation.html']:
    with open(f,'r',encoding='utf-8') as fh:
        head = fh.read().split('</head>')[0]
    title = bool(re.search(r'<title>', head))
    desc = bool(re.search(r'meta name="description"', head))
    canon = bool(re.search(r'rel="canonical"', head))
    og = 'og:title' in head
    schema = 'application/ld+json' in head
    print(f'{f}: title={title} desc={desc} canonical={canon} og={og} schema={schema}')
