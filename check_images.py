import os, re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

imgs = re.findall(r'src="(images/products/[^"]+)"', content)
unique = sorted(set(imgs))
missing = []
for img in unique:
    if not os.path.isfile(img):
        missing.append(img)
        print(f'MISSING: {img}')

print(f'\n{len(missing)} broken out of {len(unique)} unique images')
