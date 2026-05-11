// ===== EZUP Atlantic Products JS =====
let allProducts = [];
let filteredProducts = [];

const categoryNames = {
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
};

async function loadProducts() {
 try {
  const res = await fetch('data/products.json?v=' + Date.now());
  allProducts = await res.json();
  applyFilters();
 } catch (e) {
  document.getElementById('product-grid').innerHTML = '<p style="grid-column:1/-1;text-align:center;padding:40px;color:#999;">Unable to load products. Please try again later.</p>';
 }
}

function applyFilters() {
 const params = new URLSearchParams(window.location.search);
 const catFilter = document.getElementById('filter-category')?.value || params.get('cat') || '';
 const sizeFilter = document.getElementById('filter-size')?.value || params.get('size') || '';
 const search = document.getElementById('filter-search')?.value?.toLowerCase() || '';
 const sort = document.getElementById('filter-sort')?.value || 'name';

 // Set dropdown values from URL params on first load
 if (params.get('cat') && document.getElementById('filter-category')) {
  document.getElementById('filter-category').value = params.get('cat');
 }
 if (params.get('size') && document.getElementById('filter-size')) {
  document.getElementById('filter-size').value = params.get('size');
 }

 filteredProducts = allProducts.filter(p => {
  if (catFilter && p.category !== catFilter && p.subcategory !== catFilter) return false;
  if (sizeFilter && !(p.sizes || []).includes(sizeFilter) && p.size !== sizeFilter) return false;
  if (search && !p.name.toLowerCase().includes(search)) return false;
  return true;
 });

 // Sort
 filteredProducts.sort((a, b) => {
  if (sort === 'price-asc') return (a.price || 0) - (b.price || 0);
  if (sort === 'price-desc') return (b.price || 0) - (a.price || 0);
  return a.name.localeCompare(b.name);
 });

 renderProducts();
}

function renderProducts() {
 const grid = document.getElementById('product-grid');
 const count = document.getElementById('results-count');
 if (count) count.textContent = `${filteredProducts.length} product${filteredProducts.length !== 1 ? 's' : ''} found`;

 if (filteredProducts.length === 0) {
  grid.innerHTML = '<p style="grid-column:1/-1;text-align:center;padding:60px 20px;color:#999;font-size:1.1rem;">No products match your filters. Try adjusting your search.</p>';
  return;
 }

 grid.innerHTML = filteredProducts.map((p, idx) => `
  <div class="product-card animate-in" style="animation-delay: ${(idx % 12) * 0.05}s;">
   <div class="product-card-img">
    ${p.badge ? `<span class="product-card-badge">${p.badge}</span>` : ''}
    <img src="${p.img || ''}" alt="${p.name}" loading="lazy" onerror="this.style.display='none'">
   </div>
   <div class="product-card-body">
    <div class="product-card-category">${categoryNames[p.category] || p.category}</div>
    <div class="product-card-title">${p.name}</div>
    <div class="product-card-price">${p.priceDisplay} <small>CAD</small></div>
    <div class="product-card-actions">
     <a href="product.html?id=${p.id}" class="btn btn-outline" style="border-radius: var(--radius-full);">View Details</a>
     <button class="add-to-cart-btn" onclick="addProductToCart('${p.id}')" style="border-radius: var(--radius-full);">Add to Cart</button>
    </div>
   </div>
  </div>
 `).join('');
}

// Add product to cart from catalog
function addProductToCart(productId) {
 const product = allProducts.find(p => p.id === productId);
 if (product && typeof Cart !== 'undefined') {
  Cart.addItem(product);
 }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
 loadProducts();
 document.getElementById('filter-category')?.addEventListener('change', applyFilters);
 document.getElementById('filter-size')?.addEventListener('change', applyFilters);
 document.getElementById('filter-sort')?.addEventListener('change', applyFilters);
 let searchTimeout;
 document.getElementById('filter-search')?.addEventListener('input', () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(applyFilters, 300);
 });
});
