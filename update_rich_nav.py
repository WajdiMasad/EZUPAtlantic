import os
import glob

html_files = glob.glob('*.html')

new_nav = """      <nav class="nav-links">
        <a href="index.html">Home</a>
        
        <!-- Canopy Tents Mega Menu -->
        <div class="nav-item-dropdown">
          <a href="products.html?cat=canopy-tents">Canopy Tents <span style="font-size:0.7rem;vertical-align:middle;">▼</span></a>
          <div class="mega-menu">
            <div class="mega-images-row">
              <a href="products.html?cat=heavy-duty" class="mega-image-card">
                <img src="images/products/eclipse-shelter-51152011198639.webp" alt="Best Sellers">
                <div class="mega-image-title">Best Sellers</div>
              </a>
              <a href="products.html?cat=canopy-bundles" class="mega-image-card">
                <img src="images/products/vista-camping-cube-sport-bundle-43441940037935.png" alt="Canopy Bundles">
                <div class="mega-image-title">Canopy Bundles</div>
              </a>
              <a href="products.html?cat=accessories" class="mega-image-card">
                <img src="images/products/vantage-camping-cube.jpg" alt="Canopy Accessories">
                <div class="mega-image-title">Canopy Accessories</div>
              </a>
              <a href="products.html?cat=industrial-grade" class="mega-image-card">
                <img src="images/products/endeavor-max-canopy-45839621816623.png" alt="Industrial Grade">
                <div class="mega-image-title">Industrial Grade</div>
              </a>
            </div>
            <div class="mega-links-row">
              <div class="mega-col">
                <h4>Shop By Category</h4>
                <a href="products.html?cat=light-duty">Light Duty</a>
                <a href="products.html?cat=medium-duty">Medium Duty</a>
                <a href="products.html?cat=heavy-duty">Heavy Duty</a>
              </div>
              <div class="mega-col">
                <h4>Shop By Size</h4>
                <a href="products.html?size=10x10">10' x 10'</a>
                <a href="products.html?size=10x15">10' x 15'</a>
                <a href="products.html?size=10x20">10' x 20'</a>
                <a href="products.html?cat=canopy-tents" style="font-weight:700; margin-top:8px;">View All</a>
              </div>
              <div class="mega-col">
                <h4>Shop By Price</h4>
                <a href="products.html?sort=price-asc">Price: Low to High</a>
                <a href="products.html?sort=price-desc">Price: High to Low</a>
              </div>
              <div class="mega-col">
                <h4>Shop By Use</h4>
                <a href="products.html?cat=industrial-grade">Business & Promotion</a>
                <a href="products.html?cat=light-duty">Outdoor Recreation</a>
                <a href="products.html?cat=medium-duty">Schools & Teams</a>
                <a href="products.html?cat=industrial-grade">Industrial Safety</a>
              </div>
              <div class="mega-col">
                <h4>Featured</h4>
                <a href="product.html?id=dewalt-work-shelter">DEWALT® Work Shelter</a>
                <a href="product.html?id=endeavor-max-canopy">Endeavor Max Canopy</a>
                <a href="product.html?id=eclipse-shelter">Eclipse Shelter</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Custom Printing Mega Menu -->
        <div class="nav-item-dropdown">
          <a href="products.html?cat=custom-printing">Custom Printing <span style="font-size:0.7rem;vertical-align:middle;">▼</span></a>
          <div class="mega-menu" style="min-width:700px;">
            <div class="mega-images-row">
              <a href="products.html?cat=custom-canopies" class="mega-image-card">
                <img src="images/products/custom-vantage-package.webp" alt="Custom Canopies">
                <div class="mega-image-title">Custom Canopies</div>
              </a>
              <a href="products.html?cat=custom-flags" class="mega-image-card">
                <img src="images/products/blade.jpg" alt="Custom Flags">
                <div class="mega-image-title">Custom Flags</div>
              </a>
              <a href="products.html?cat=table-covers-chairs" class="mega-image-card">
                <img src="images/products/instant-table-covers-43224424317103.jpg" alt="Table Covers & Chairs">
                <div class="mega-image-title">Table Covers & Chairs</div>
              </a>
              <a href="products.html?cat=banners-signage" class="mega-image-card">
                <img src="images/products/hanging-banners.webp" alt="Banners & Signage">
                <div class="mega-image-title">Banners & Signage</div>
              </a>
            </div>
            <div class="mega-links-row">
              <div class="mega-col">
                <h4>Custom Products</h4>
                <a href="products.html?cat=custom-canopies">Custom Canopies</a>
                <a href="products.html?cat=custom-packages">Custom Packages</a>
                <a href="products.html?cat=custom-flags">Custom Flags</a>
                <a href="products.html?cat=table-covers-chairs">Table Covers & Chairs</a>
              </div>
              <div class="mega-col">
                <h4>Displays & Signs</h4>
                <a href="products.html?cat=event-system">E-Z Event System™</a>
                <a href="products.html?cat=custom-sidewalls">Custom Sidewalls</a>
                <a href="products.html?cat=banners-signage">Banners & Signage</a>
                <a href="products.html?cat=inflatables">Inflatables</a>
              </div>
              <div class="mega-col">
                <h4>Accessories</h4>
                <a href="products.html?cat=indoor-displays">Indoor Displays</a>
                <a href="products.html?cat=custom-accessories">Custom Accessories</a>
                <a href="products.html?cat=custom-printing" style="font-weight:700; margin-top:8px;">View All Custom</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Accessories Mega Menu -->
        <div class="nav-item-dropdown">
          <a href="products.html?cat=accessories">Accessories <span style="font-size:0.7rem;vertical-align:middle;">▼</span></a>
          <div class="mega-menu" style="min-width:700px;">
            <div class="mega-images-row">
              <a href="products.html?cat=canopy-sidewalls" class="mega-image-card">
                <img src="images/products/value-sidewall.webp" alt="Canopy Sidewalls">
                <div class="mega-image-title">Canopy Sidewalls</div>
              </a>
              <a href="products.html?cat=anchoring" class="mega-image-card">
                <img src="images/products/weight-plates-45811776979119.jpg" alt="Anchoring">
                <div class="mega-image-title">Anchoring</div>
              </a>
              <a href="products.html?cat=camping-cubes" class="mega-image-card">
                <img src="images/products/vantage-camping-cube.jpg" alt="Camping & Screen Cubes">
                <div class="mega-image-title">Camping & Cubes</div>
              </a>
              <a href="products.html?cat=lighting" class="mega-image-card">
                <img src="images/products/60w-led-balloon-light.webp" alt="Lighting">
                <div class="mega-image-title">Lighting</div>
              </a>
            </div>
            <div class="mega-links-row">
              <div class="mega-col">
                <h4>Essentials</h4>
                <a href="products.html?cat=canopy-sidewalls">Canopy Sidewalls</a>
                <a href="products.html?cat=anchoring">Anchoring Essentials</a>
                <a href="products.html?cat=roller-bags">Roller Bag & Storage</a>
              </div>
              <div class="mega-col">
                <h4>Add-Ons</h4>
                <a href="products.html?cat=camping-cubes">Camping & Screen Cubes</a>
                <a href="products.html?cat=lighting">Lighting</a>
                <a href="products.html?cat=chairs-benches">Chairs & Benches</a>
              </div>
              <div class="mega-col">
                <h4>Parts & Gear</h4>
                <a href="products.html?cat=instant-table">Instant Table™</a>
                <a href="products.html?cat=gearrunner">Gearrunner™</a>
                <a href="products.html?cat=brackets">E-Z Brackets</a>
                <a href="products.html?cat=replacement-parts">Replacement Parts</a>
              </div>
            </div>
          </div>
        </div>

        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
      </nav>"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_idx = content.find('<nav class="nav-links">')
    if start_idx != -1:
        end_idx = content.find('</nav>', start_idx) + 6
        content = content[:start_idx] + new_nav + content[end_idx:]

        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)

print('Updated Rich Navigation HTML.')
