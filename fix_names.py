import json

d = json.load(open(r'e:\EZUP\data\products.json', 'r', encoding='utf-8'))

for p in d:
    if p['name'] == 'Hut 10 X 10 Shelter':
        p['sizes'] = ['10x10']
        print(f"Fixed: {p['name']} -> sizes={p['sizes']}")

with open(r'e:\EZUP\data\products.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("Done.")
