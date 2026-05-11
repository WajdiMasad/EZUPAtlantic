import json
import re

with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

def map_product(name, current_category):
    name_lower = name.lower()
    
    # 1. Custom Printing (Overrrides everything else if it has "custom" in the name)
    if 'custom' in name_lower or current_category == 'custom' or current_category == 'custom-flags' or current_category == 'signs-banners':
        if 'flag' in name_lower or 'blade' in name_lower or 'tear drop' in name_lower:
            return 'custom-printing', 'custom-flags'
        elif 'package' in name_lower:
            return 'custom-printing', 'custom-packages'
        elif 'table' in name_lower or 'chair' in name_lower or 'bench' in name_lower or 'throw' in name_lower or 'skirt' in name_lower:
            return 'custom-printing', 'table-covers-chairs'
        elif 'sidewall' in name_lower or 'wall' in name_lower or 'railskirt' in name_lower:
            return 'custom-printing', 'custom-sidewalls'
        elif 'banner' in name_lower or 'sign' in name_lower or 'display' in name_lower or 'tube' in name_lower:
            return 'custom-printing', 'banners-signage'
        elif 'system' in name_lower or 'tasting' in name_lower:
            return 'custom-printing', 'event-system'
        elif 'inflatable' in name_lower or 'dome' in name_lower: # dome might be a tent, but let's check
             if 'tent' in name_lower or 'canopy' in name_lower or 'shelter' in name_lower or 'express' in name_lower or 'hut' in name_lower or 'eclipse' in name_lower or 'endeavor' in name_lower or 'vantage' in name_lower:
                 return 'custom-printing', 'custom-canopies'
             return 'custom-printing', 'inflatables'
        elif 'tent' in name_lower or 'canopy' in name_lower or 'shelter' in name_lower or 'express' in name_lower or 'hut' in name_lower or 'eclipse' in name_lower or 'endeavor' in name_lower or 'vantage' in name_lower:
            return 'custom-printing', 'custom-canopies'
        else:
            return 'custom-printing', 'custom-accessories'

    # 2. Accessories
    if current_category in ['accessories', 'camping', 'lighting-power', 'chairs-tables']:
        if 'sidewall' in name_lower or 'half wall' in name_lower or 'shield' in name_lower or 'railskirt' in name_lower:
            return 'accessories', 'canopy-sidewalls'
        elif 'weight' in name_lower or 'stake' in name_lower or 'anchor' in name_lower:
            return 'accessories', 'anchoring'
        elif 'roller bag' in name_lower or 'cover bag' in name_lower or 'tote' in name_lower or 'bag' in name_lower:
            return 'accessories', 'roller-bags'
        elif 'cube' in name_lower or 'screen room' in name_lower:
            return 'accessories', 'camping-cubes'
        elif 'light' in name_lower or 'heater' in name_lower or 'power station' in name_lower or 'battery' in name_lower:
            return 'accessories', 'lighting'
        elif 'chair' in name_lower or 'bench' in name_lower:
            return 'accessories', 'chairs-benches'
        elif 'table' in name_lower:
            return 'accessories', 'instant-table'
        elif 'gearrunner' in name_lower or 'wagon' in name_lower:
            return 'accessories', 'gearrunner'
        elif 'bracket' in name_lower or 'mount' in name_lower or 'clip' in name_lower or 'wedge' in name_lower or 'gutter' in name_lower:
            return 'accessories', 'brackets'
        elif 'replacement' in name_lower or 'frame' in name_lower or 'top' in name_lower or 'parts' in name_lower:
            return 'accessories', 'replacement-parts'
        else:
            return 'accessories', 'replacement-parts' # fallback
            
    # 3. Canopy Tents (Default for everything else)
    # Light Duty: Vista, Dome
    # Medium Duty: Vantage, Pyramid
    # Heavy Duty: Eclipse, Express, Speed Shelter, Hut
    # Industrial: Endeavor, Hub, Work Cube
    if 'bundle' in name_lower or 'package' in name_lower:
        return 'canopy-tents', 'canopy-bundles'
    elif 'endeavor' in name_lower or 'hub' in name_lower or 'work cube' in name_lower or 'patriot' in name_lower or 'utility' in name_lower:
        return 'canopy-tents', 'industrial-grade'
    elif 'eclipse' in name_lower or 'express' in name_lower or 'speed shelter' in name_lower or 'hut' in name_lower:
        return 'canopy-tents', 'heavy-duty'
    elif 'vantage' in name_lower or 'pyramid' in name_lower or 'vue' in name_lower:
        return 'canopy-tents', 'medium-duty'
    elif 'vista' in name_lower or 'dome' in name_lower:
        return 'canopy-tents', 'light-duty'
    else:
        # Fallback to medium duty if unknown
        return 'canopy-tents', 'medium-duty'

for p in products:
    cat, subcat = map_product(p['name'], p.get('category'))
    p['category'] = cat
    p['subcategory'] = subcat

with open('data/products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=1)

print("Mapped categories for 182 products.")
