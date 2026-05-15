import json

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

lens = [len(p.get('description', '')) for p in products]
print(f'Min: {min(lens)} | Max: {max(lens)} | Avg: {sum(lens)//len(lens)}')
print()

# Show examples of short ones
short = sorted(products, key=lambda p: len(p.get('description', '')))
for p in short[:10]:
    d = p.get('description', '')
    print(f'{p["name"]}: {len(d)} chars')
    print(f'  "{d}"')
    print()
