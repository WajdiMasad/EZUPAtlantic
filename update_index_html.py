import os

filepath = 'e:\\EZUP\\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_grids = """      <div class="section-header animate-in">
        <h2>Canopy Tents</h2>
      </div>
      <div class="category-grid animate-in" style="margin-bottom:60px;">
        <a href="products.html?cat=light-duty" class="category-card">
          <img src="images/products/vista-shelter-43187285524655.jpg" alt="Light Duty" loading="lazy">
          <div class="category-card-overlay">
            <h3>Light Duty</h3>
          </div>
        </a>
        <a href="products.html?cat=medium-duty" class="category-card">
          <img src="images/products/vantage-shelter-44670003249327.jpg" alt="Medium Duty" loading="lazy">
          <div class="category-card-overlay">
            <h3>Medium Duty</h3>
          </div>
        </a>
        <a href="products.html?cat=heavy-duty" class="category-card">
          <img src="images/products/eclipse-shelter-51152011198639.webp" alt="Heavy Duty" loading="lazy">
          <div class="category-card-overlay">
            <h3>Heavy Duty</h3>
          </div>
        </a>
        <a href="products.html?cat=industrial-grade" class="category-card">
          <img src="images/products/endeavor-max-canopy-45839621816623.png" alt="Industrial Grade" loading="lazy">
          <div class="category-card-overlay">
            <h3>Industrial Grade</h3>
          </div>
        </a>
      </div>

      <div class="section-header animate-in">
        <h2>Custom Printing</h2>
      </div>
      <div class="category-grid animate-in" style="margin-bottom:60px;">
        <a href="products.html?cat=custom-canopies" class="category-card">
          <img src="images/products/custom-vantage-package.webp" alt="Custom Canopies" loading="lazy">
          <div class="category-card-overlay">
            <h3>Custom Canopies</h3>
          </div>
        </a>
        <a href="products.html?cat=custom-flags" class="category-card">
          <img src="images/products/blade.jpg" alt="Custom Flags" loading="lazy">
          <div class="category-card-overlay">
            <h3>Custom Flags</h3>
          </div>
        </a>
        <a href="products.html?cat=table-covers-chairs" class="category-card">
          <img src="images/products/instant-table-covers-43224424317103.jpg" alt="Table Covers & Chairs" loading="lazy">
          <div class="category-card-overlay">
            <h3>Table Covers & Chairs</h3>
          </div>
        </a>
        <a href="products.html?cat=banners-signage" class="category-card">
          <img src="images/products/hanging-banners.webp" alt="Banners & Signage" loading="lazy">
          <div class="category-card-overlay">
            <h3>Banners & Signage</h3>
          </div>
        </a>
      </div>

      <div class="section-header animate-in">
        <h2>Accessories</h2>
      </div>
      <div class="category-grid animate-in">
        <a href="products.html?cat=canopy-sidewalls" class="category-card">
          <img src="images/products/value-sidewall.webp" alt="Canopy Sidewalls" loading="lazy">
          <div class="category-card-overlay">
            <h3>Canopy Sidewalls</h3>
          </div>
        </a>
        <a href="products.html?cat=anchoring" class="category-card">
          <img src="images/products/weight-plates-45811776979119.jpg" alt="Anchoring Essentials" loading="lazy">
          <div class="category-card-overlay">
            <h3>Anchoring Essentials</h3>
          </div>
        </a>
        <a href="products.html?cat=camping-cubes" class="category-card">
          <img src="images/products/vantage-camping-cube.jpg" alt="Camping & Screen Cubes" loading="lazy">
          <div class="category-card-overlay">
            <h3>Camping & Screen Cubes</h3>
          </div>
        </a>
        <a href="products.html?cat=lighting" class="category-card">
          <img src="images/products/60w-led-balloon-light.webp" alt="Lighting" loading="lazy">
          <div class="category-card-overlay">
            <h3>Lighting</h3>
          </div>
        </a>
      </div>"""

start_idx = content.find('<div class="section-header animate-in">\n        <h2>Shop By Category</h2>')
if start_idx != -1:
    end_idx = content.find('</section>', start_idx)
    content = content[:start_idx] + new_grids + content[end_idx:]

with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print("Updated index.html")
