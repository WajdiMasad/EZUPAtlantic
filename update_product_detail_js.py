import os

filepath = 'e:\\EZUP\\js\\product-detail.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_categories = """const categoryNames = {
 'canopy-tents': 'Canopy Tents',
 'custom-printing': 'Custom Printing',
 'accessories': 'Accessories',
 
 'light-duty': 'Light Duty',
 'medium-duty': 'Medium Duty',
 'heavy-duty': 'Heavy Duty',
 'industrial-grade': 'Industrial Grade',
 'canopy-bundles': 'Canopy Bundles',
 
 'custom-canopies': 'Custom Canopies',
 'custom-packages': 'Custom Packages',
 'custom-flags': 'Custom Flags',
 'table-covers-chairs': 'Table Covers & Chairs',
 'event-system': 'E-Z Event System™',
 'custom-sidewalls': 'Custom Sidewalls',
 'banners-signage': 'Banners & Signage',
 'inflatables': 'Inflatables',
 'indoor-displays': 'Indoor Displays',
 'custom-accessories': 'Custom Accessories',
 
 'canopy-sidewalls': 'Canopy Sidewalls',
 'anchoring': 'Anchoring Essentials',
 'roller-bags': 'Roller Bag & Storage',
 'camping-cubes': 'Camping & Screen Cubes',
 'lighting': 'Lighting',
 'chairs-benches': 'Chairs & Benches',
 'instant-table': 'Instant Table™',
 'gearrunner': 'Gearrunner™',
 'brackets': 'E-Z Brackets',
 'replacement-parts': 'Replacement Parts'
};"""

start_idx = content.find('const categoryNames = {')
end_idx = content.find('};', start_idx) + 2
content = content[:start_idx] + new_categories + content[end_idx:]

with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print("Updated js/product-detail.js")
