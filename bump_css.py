"""Bump CSS cache version across all HTML files"""
import glob

for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    content = content.replace('styles.css?v=3', 'styles.css?v=4')
    with open(f, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(content)
    print(f'Updated: {f}')
