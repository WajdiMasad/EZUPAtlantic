import json
data = json.load(open('data/products.json','r',encoding='utf-8'))
cats = {}
total_variants = 0
has_sku = 0
for p in data:
    cats[p.get('category','')] = cats.get(p.get('category',''),0)+1
    for v in p.get('variants', []):
        total_variants += 1
        if v.get('sku'): has_sku += 1
print(f"Products: {len(data)}")
print(f"Total variants (SKUs): {total_variants}")
print(f"Variants with SKU: {has_sku}")
print("Categories:")
for k,v in sorted(cats.items()):
    print(f"  {k}: {v}")
