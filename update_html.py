import os
import glob

html_files = glob.glob('*.html')

new_footer_links = """        <div class="footer-links">
          <h4>Shop Products</h4>
          <a href="products.html?cat=canopy-tents-accessories">Canopy Tents & Accessories</a>
          <a href="products.html?cat=custom-flags">Custom Flags</a>
          <a href="products.html?cat=chairs-tables">Chairs & Tables</a>
          <a href="products.html?cat=camping">Camping</a>
          <a href="products.html?cat=signs-banners">Signs & Banners</a>
          <a href="products.html?cat=lighting-power">Lighting & Power</a>
        </div>"""

new_filter = """        <select id="filter-category" style="border:none; border-bottom:2px solid transparent; background:transparent;">
          <option value="">All Categories</option>
          <option value="canopy-tents-accessories">Canopy Tents & Accessories</option>
          <option value="custom-flags">Custom Flags</option>
          <option value="chairs-tables">Chairs & Tables</option>
          <option value="camping">Camping</option>
          <option value="signs-banners">Signs & Banners</option>
          <option value="lighting-power">Lighting & Power</option>
        </select>"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Standardize CRLF to LF
    content = content.replace('\r\n', '\n')
    
    # Replace footer links
    start_idx = content.find('<div class="footer-links">\n          <h4>Shop Products</h4>')
    if start_idx != -1:
        end_idx = content.find('</div>', start_idx) + 6
        content = content[:start_idx] + new_footer_links + content[end_idx:]
            
    # Replace products.html filter
    if filepath == 'products.html':
        start_idx = content.find('<select id="filter-category"')
        if start_idx != -1:
            end_idx = content.find('</select>', start_idx) + 9
            content = content[:start_idx] + new_filter + content[end_idx:]

    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

print('Updated HTML files.')
