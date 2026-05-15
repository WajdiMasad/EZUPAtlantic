// ===== Product Detail Page JS =====
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

async function loadProduct() {
 const params = new URLSearchParams(window.location.search);
 const productId = params.get('id');
 if (!productId) { window.location.href = 'products.html'; return; }

 try {
  const res = await fetch('data/products.json?v=' + Date.now());
  const allProducts = await res.json();
  const product = allProducts.find(p => p.id === productId);
  if (!product) { document.getElementById('product-detail').innerHTML = '<p style="grid-column:1/-1;text-align:center;padding:60px;color:#999;">Product not found. <a href="products.html" style="color:var(--brand-blue)">Browse all products</a></p>'; return; }

  // Update page title and meta
  document.title = `${product.name} | EZ-UP Atlantic`;
  const metaDesc = `${product.name} — ${(product.description || '').substring(0, 155)}. Available from EZ-UP Atlantic, your authorized dealer in Atlantic Canada. ${product.priceDisplay} CAD.`;
  document.querySelector('meta[name="description"]').content = metaDesc;
  document.getElementById('bc-name').textContent = product.name;

  // Dynamic canonical URL
  const canonEl = document.querySelector('link[rel="canonical"]');
  if (canonEl) canonEl.href = `https://ezupatlantic.ca/product.html?id=${product.id}`;

  // Dynamic Open Graph tags
  const ogUpdates = {
   'og:title': `${product.name} | EZ-UP Atlantic`,
   'og:description': metaDesc,
   'og:url': `https://ezupatlantic.ca/product.html?id=${product.id}`,
   'og:image': product.img ? `https://ezupatlantic.ca/${product.img}` : '',
  };
  for (const [prop, val] of Object.entries(ogUpdates)) {
   const el = document.querySelector(`meta[property="${prop}"]`);
   if (el) el.content = val;
  }

  // Dynamic Product JSON-LD Schema
  const priceNum = product.price || 0;
  const schemaScript = document.createElement('script');
  schemaScript.type = 'application/ld+json';
  schemaScript.textContent = JSON.stringify({
   "@context": "https://schema.org",
   "@type": "Product",
   "name": product.name,
   "description": product.description || '',
   "image": product.img ? `https://ezupatlantic.ca/${product.img}` : '',
   "brand": { "@type": "Brand", "name": "E-Z UP" },
   "sku": product.id,
   "url": `https://ezupatlantic.ca/product.html?id=${product.id}`,
   "offers": {
    "@type": "Offer",
    "url": `https://ezupatlantic.ca/product.html?id=${product.id}`,
    "priceCurrency": "CAD",
    "price": priceNum > 0 ? priceNum.toFixed(2) : undefined,
    "availability": "https://schema.org/InStock",
    "seller": {
     "@type": "Organization",
     "name": "EZ-UP Atlantic"
    },
    "shippingDetails": {
     "@type": "OfferShippingDetails",
     "shippingRate": {
      "@type": "MonetaryAmount",
      "value": priceNum >= 500 ? "0" : "75.00",
      "currency": "CAD"
     },
     "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "CA" }
    }
   }
  });
  document.head.appendChild(schemaScript);

  // Build specs table
  let specsHtml = '';
  if (product.specs) {
   specsHtml = '<h3 style="font-size:1rem;font-weight:700;margin-top:24px;margin-bottom:8px;">Specifications</h3><table class="spec-table">';
   for (const [key, val] of Object.entries(product.specs)) {
    const label = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    specsHtml += `<tr><td>${label}</td><td>${val}</td></tr>`;
   }
   specsHtml += '</table>';
  }

  // Build features list
  let featuresHtml = '';
  if (product.features && product.features.length) {
   featuresHtml = '<h3 style="font-size:1rem;font-weight:700;margin-top:24px;margin-bottom:8px;">Key Features</h3><ul class="features-list">';
   product.features.forEach(f => { featuresHtml += `<li>${f}</li>`; });
   featuresHtml += '</ul>';
  }

  // Build interactive options HTML
  let optionsHtml = '';
  if (product.options && product.options.length) {
   optionsHtml = '<div style="margin-top:24px;">';
   product.options.forEach((opt, optIdx) => {
    optionsHtml += `<h3 style="font-size:.95rem;font-weight:700;margin-bottom:12px;">${opt.name}</h3>`;
    optionsHtml += '<div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:20px;">';
    opt.values.forEach((val, valIdx) => {
     const activeClass = valIdx === 0 ? 'variant-pill--active' : '';
     optionsHtml += `<button class="variant-pill ${activeClass}" data-option="${optIdx}" data-value="${val}" onclick="selectVariant(this, ${optIdx})">${val}</button>`;
    });
    optionsHtml += '</div>';
   });
   optionsHtml += '</div>';
  }

  // Build gallery with thumbnails
  let galleryHtml = '';
  if (product.images && product.images.length > 1) {
   galleryHtml = `
    <div class="product-gallery">
     <img id="main-product-img" src="${product.img}" alt="${product.name}" onerror="this.style.display='none'">
     <div class="gallery-thumbs" id="gallery-thumbs">
      ${product.images.map((img, idx) => `
       <img src="${img.src}" alt="${img.alt || product.name}" 
          class="gallery-thumb ${idx === 0 ? 'gallery-thumb--active' : ''}" 
          onclick="changeMainImage('${img.src}', this)"
          onerror="this.style.display='none'">
      `).join('')}
     </div>
    </div>`;
  } else {
   galleryHtml = `
    <div class="product-gallery">
     <img id="main-product-img" src="${product.img}" alt="${product.name}" onerror="this.style.display='none'">
    </div>`;
  }

  // Render product
  document.getElementById('product-detail').innerHTML = `
   ${galleryHtml}
   <div class="product-info">
    <span class="category-tag">${categoryNames[product.category] || product.category}</span>
    ${product.badge ? `<span class="category-tag" style="background:var(--brand-red);margin-left:8px;">${product.badge}</span>` : ''}
    <h1>${product.name}</h1>
    <div class="price" id="product-price">${product.priceDisplay} <small>CAD</small></div>
    ${product.size ? `<p style="color:var(--text-secondary);font-size:.85rem;margin-top:4px;">Size: ${product.size.replace('x', "' × ")}' </p>` : ''}
    <div class="desc">${product.description || 'Contact us for detailed product information and specifications.'}</div>
    ${optionsHtml}
    ${specsHtml}
    ${featuresHtml}
    <div class="product-actions">
     <div class="qty-selector">
      <button onclick="changeQty(-1)" aria-label="Decrease quantity">−</button>
      <input type="number" id="detail-qty" value="1" min="1" max="99" aria-label="Quantity">
      <button onclick="changeQty(1)" aria-label="Increase quantity">+</button>
     </div>
     <button onclick="addToCartFromDetail()" class="btn btn-primary" style="gap:6px; flex:2;">Add to Cart</button>
    </div>
   </div>
  `;

  // Store product data globally for variant switching
  window._product = product;
  window._selectedOptions = {};
  if (product.options) {
   product.options.forEach((opt, idx) => {
    window._selectedOptions[idx] = opt.values[0];
   });
  }

  // Related products
  const related = allProducts.filter(p => p.category === product.category && p.id !== product.id).slice(0, 4);
  if (related.length) {
   document.getElementById('related-section').style.display = '';
   document.getElementById('related-grid').innerHTML = related.map(p => `
    <a href="product.html?id=${p.id}" class="product-card" style="text-decoration:none">
     <div class="product-card-img">
      ${p.badge ? `<span class="product-card-badge">${p.badge}</span>` : ''}
      <img src="${p.img}" alt="${p.name}" loading="lazy" onerror="this.style.display='none'">
     </div>
     <div class="product-card-body">
      <div class="product-card-category">${categoryNames[p.category] || p.category}</div>
      <div class="product-card-title">${p.name}</div>
      <div class="product-card-price">${p.priceDisplay} <small>CAD</small></div>
     </div>
    </a>
   `).join('');
  }
 } catch (e) {
  document.getElementById('product-detail').innerHTML = '<p style="grid-column:1/-1;text-align:center;padding:60px;color:#999;">Error loading product. <a href="products.html">Browse all products</a></p>';
 }
}

// ===== Variant Selection =====
function selectVariant(btn, optionIdx) {
 // Update active pill
 btn.parentElement.querySelectorAll('.variant-pill').forEach(p => p.classList.remove('variant-pill--active'));
 btn.classList.add('variant-pill--active');
 
 // Track selection
 window._selectedOptions[optionIdx] = btn.dataset.value;
 
 // Build variant title from selected options
 const product = window._product;
 if (!product || !product.variants) return;
 
 const selectedValues = Object.values(window._selectedOptions);
 const variantTitle = selectedValues.join(' / ');
 
 // Find matching variant
 const match = product.variants.find(v => {
  const vParts = v.name.split(' / ').map(s => s.trim());
  return selectedValues.every((sel, i) => vParts[i] === sel);
 });
 
 if (match) {
  // Update price
  const priceEl = document.getElementById('product-price');
  if (priceEl && match.price) {
   priceEl.innerHTML = `$${match.price.toLocaleString('en-CA', {minimumFractionDigits: 2})} <small>CAD</small>`;
   if (!match.available) {
    priceEl.innerHTML += ' <span style="color:#999;font-size:.7em;font-weight:400;">— Out of Stock</span>';
   }
  }
  
  // Update image if variant has one
  if (match.img) {
   const mainImg = document.getElementById('main-product-img');
   if (mainImg) {
    mainImg.src = match.img;
    // Highlight matching thumbnail
    document.querySelectorAll('.gallery-thumb').forEach(t => {
     t.classList.toggle('gallery-thumb--active', t.src.includes(match.img.split('/').pop()));
    });
   }
  }
  
  // Update quote button with variant info
  const quoteBtn = document.getElementById('quote-btn');
  if (quoteBtn) {
   quoteBtn.href = `contact.html?product=${encodeURIComponent(product.name + ' - ' + variantTitle)}`;
  }
 }
}

// ===== Gallery Image Switching =====
function changeMainImage(src, thumb) {
 const mainImg = document.getElementById('main-product-img');
 if (mainImg) mainImg.src = src;
 document.querySelectorAll('.gallery-thumb').forEach(t => t.classList.remove('gallery-thumb--active'));
 if (thumb) thumb.classList.add('gallery-thumb--active');
}

// ===== Quantity Selector =====
function changeQty(delta) {
 const input = document.getElementById('detail-qty');
 if (!input) return;
 let val = parseInt(input.value) || 1;
 val += delta;
 if (val < 1) val = 1;
 if (val > 99) val = 99;
 input.value = val;
}

// =====Add to Cart from Detail Page =====
function addToCartFromDetail() {
 const product = window._product;
 if (!product || typeof Cart === 'undefined') return;

 // Find selected variant
 let variant = null;
 if (product.variants && product.variants.length > 1 && window._selectedOptions) {
  const selectedValues = Object.values(window._selectedOptions);
  const variantTitle = selectedValues.join(' / ');
  variant = product.variants.find(v => {
   const vParts = v.name.split(' / ').map(s => s.trim());
   return selectedValues.every((sel, i) => vParts[i] === sel);
  });
  if (!variant) {
   variant = { name: variantTitle, price: product.price, priceDisplay: product.priceDisplay };
  }
 }
 
 // Get quantity
 const qtyInput = document.getElementById('detail-qty');
 const quantity = qtyInput ? (parseInt(qtyInput.value) || 1) : 1;

 Cart.addItem(product, variant, quantity);
}

document.addEventListener('DOMContentLoaded', loadProduct);
