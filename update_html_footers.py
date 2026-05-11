import os
import glob

html_files = glob.glob('*.html')

new_footer_links = """        <div class="footer-links">
          <h4>Shop Products</h4>
          <a href="products.html?cat=canopy-tents">Canopy Tents</a>
          <a href="products.html?cat=custom-printing">Custom Printing</a>
          <a href="products.html?cat=accessories">Accessories</a>
          <a href="products.html?cat=canopy-bundles">Canopy Bundles</a>
          <a href="products.html?cat=custom-flags">Custom Flags</a>
          <a href="products.html?cat=table-covers-chairs">Table Covers & Chairs</a>
        </div>"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace footer links
    start_idx = content.find('<div class="footer-links">\n          <h4>Shop Products</h4>')
    if start_idx != -1:
        end_idx = content.find('</div>', start_idx) + 6
        content = content[:start_idx] + new_footer_links + content[end_idx:]

    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

print('Updated HTML footers.')
