import os
import glob

html_files = glob.glob('*.html')

new_nav = """      <nav class="nav-links">
        <a href="index.html">Home</a>
        <div class="nav-item-dropdown">
          <a href="products.html">Products <span style="font-size:0.7rem;vertical-align:middle;">▼</span></a>
          <div class="mega-menu">
            <div class="mega-col">
              <h4>Canopy Tents</h4>
              <a href="products.html?cat=canopy-tents">All Canopy Tents</a>
              <a href="products.html?cat=light-duty">Light Duty</a>
              <a href="products.html?cat=medium-duty">Medium Duty</a>
              <a href="products.html?cat=heavy-duty">Heavy Duty</a>
              <a href="products.html?cat=industrial-grade">Industrial Grade</a>
              <a href="products.html?cat=canopy-bundles">Canopy Bundles</a>
            </div>
            <div class="mega-col">
              <h4>Custom Printing</h4>
              <a href="products.html?cat=custom-printing">All Custom Printing</a>
              <a href="products.html?cat=custom-canopies">Custom Canopies</a>
              <a href="products.html?cat=custom-packages">Custom Packages</a>
              <a href="products.html?cat=custom-flags">Custom Flags</a>
              <a href="products.html?cat=table-covers-chairs">Table Covers & Chairs</a>
              <a href="products.html?cat=event-system">E-Z Event System™</a>
              <a href="products.html?cat=custom-sidewalls">Custom Sidewalls</a>
              <a href="products.html?cat=banners-signage">Banners & Signage</a>
              <a href="products.html?cat=inflatables">Inflatables</a>
              <a href="products.html?cat=indoor-displays">Indoor Displays</a>
            </div>
            <div class="mega-col">
              <h4>Accessories</h4>
              <a href="products.html?cat=accessories">All Accessories</a>
              <a href="products.html?cat=canopy-sidewalls">Canopy Sidewalls</a>
              <a href="products.html?cat=anchoring">Anchoring Essentials</a>
              <a href="products.html?cat=roller-bags">Roller Bag & Storage</a>
              <a href="products.html?cat=camping-cubes">Camping & Screen Cubes</a>
              <a href="products.html?cat=lighting">Lighting</a>
              <a href="products.html?cat=chairs-benches">Chairs & Benches</a>
              <a href="products.html?cat=instant-table">Instant Table™</a>
              <a href="products.html?cat=gearrunner">Gearrunner™</a>
              <a href="products.html?cat=brackets">E-Z Brackets</a>
              <a href="products.html?cat=replacement-parts">Replacement Parts</a>
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

print('Updated Navigation HTML.')
