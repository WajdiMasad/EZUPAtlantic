import os, glob

replacements = {
    'images/products/eclipse-shelter-51152011198639.webp': 'images/products/eclipse-shelter.webp',
    'images/products/vista-shelter-43187285524655.jpg': 'images/products/vista-shelter-14643552452642.jpg',
    'images/products/vantage-shelter-44670003249327.jpg': 'images/products/vantage-shelter-50208987545903.webp',
    'images/products/instant-table-covers-43224424317103.jpg': 'images/products/instant-table-covers-14581461778466.jpg',
    'images/products/weight-plates-45811776979119.jpg': 'images/products/weight-plates-45723248132399.webp',
}

html_files = glob.glob('*.html')
total_fixed = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        count = sum(1 for old in replacements if old in original)
        total_fixed += count
        print(f'Fixed {count} image(s) in {filepath}')

print(f'\nDone — {total_fixed} total fixes across {len(html_files)} files')
