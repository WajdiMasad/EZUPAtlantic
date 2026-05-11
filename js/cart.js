// ===== EZUP Atlantic Cart System =====
// Quote-based cart using localStorage

const Cart = {
 KEY: 'ezup_cart',

 getItems() {
  try { return JSON.parse(localStorage.getItem(this.KEY)) || []; }
  catch { return []; }
 },

 save(items) {
  localStorage.setItem(this.KEY, JSON.stringify(items));
  this.updateBadge();
  this.renderDrawer();
 },

 addItem(product, variant = null, qtyToAdd = 1) {
  const items = this.getItems();
  const cartItem = {
   id: product.id,
   name: product.name,
   variant: variant ? variant.name : null,
   price: variant ? variant.price : product.price,
   priceDisplay: variant ? variant.priceDisplay : product.priceDisplay,
   img: variant?.img || product.img,
   qty: qtyToAdd
  };

  // Check if same product+variant exists
  const existing = items.findIndex(i => i.id === cartItem.id && i.variant === cartItem.variant);
  if (existing >= 0) {
   items[existing].qty += qtyToAdd;
  } else {
   items.push(cartItem);
  }

  this.save(items);
  this.showNotification(cartItem.name);
  this.openDrawer();
 },

 removeItem(index) {
  const items = this.getItems();
  items.splice(index, 1);
  this.save(items);
 },

 updateQty(index, qty) {
  const items = this.getItems();
  if (qty <= 0) {
   items.splice(index, 1);
  } else {
   items[index].qty = qty;
  }
  this.save(items);
 },

 clear() {
  localStorage.removeItem(this.KEY);
  this.updateBadge();
  this.renderDrawer();
 },

 getCount() {
  return this.getItems().reduce((sum, i) => sum + i.qty, 0);
 },

 getTotal() {
  return this.getItems().reduce((sum, i) => sum + (i.price || 0) * i.qty, 0);
 },

 // ===== UI =====
 updateBadge() {
  const badges = document.querySelectorAll('.cart-badge');
  const count = this.getCount();
  badges.forEach(b => {
   b.textContent = count;
   b.style.display = count > 0 ? 'flex' : 'none';
  });
 },

 showNotification(name) {
  const existing = document.querySelector('.cart-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'cart-toast';
  toast.innerHTML = `<span><strong>${name}</strong> added to cart</span>`;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('cart-toast--show'));
  setTimeout(() => {
   toast.classList.remove('cart-toast--show');
   setTimeout(() => toast.remove(), 300);
  }, 2500);
 },

 openDrawer() {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-overlay');
  if (drawer) { drawer.classList.add('open'); }
  if (overlay) { overlay.classList.add('open'); }
  this.renderDrawer();
 },

 closeDrawer() {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-overlay');
  if (drawer) drawer.classList.remove('open');
  if (overlay) overlay.classList.remove('open');
 },

 renderDrawer() {
  const body = document.getElementById('cart-drawer-body');
  const footer = document.getElementById('cart-drawer-footer');
  if (!body) return;

  const items = this.getItems();

  if (items.length === 0) {
   body.innerHTML = `
    <div style="text-align:center;padding:60px 20px;color:#999;">
     
     <p style="font-weight:600;color:#333;">Your cart is empty</p>
     <p style="font-size:.85rem;margin-top:8px;">Browse products and add items to your cart.</p>
     <a href="products.html" class="btn btn-primary" style="margin-top:20px;display:inline-flex;">Browse Products</a>
    </div>`;
   if (footer) footer.style.display = 'none';
   return;
  }

  body.innerHTML = items.map((item, idx) => `
   <div class="cart-item">
    <div class="cart-item-img">
     <img src="${item.img || ''}" alt="${item.name}" onerror="this.style.display='none'">
    </div>
    <div class="cart-item-info">
     <div class="cart-item-name">${item.name}</div>
     ${item.variant ? `<div class="cart-item-variant">${item.variant}</div>` : ''}
     <div class="cart-item-price">${item.priceDisplay || 'Contact for pricing'}</div>
     <div class="cart-item-qty">
      <button onclick="Cart.updateQty(${idx}, ${item.qty - 1})" class="qty-btn">−</button>
      <span>${item.qty}</span>
      <button onclick="Cart.updateQty(${idx}, ${item.qty + 1})" class="qty-btn">+</button>
      <button onclick="Cart.removeItem(${idx})" class="cart-item-remove" title="Remove"></button>
     </div>
    </div>
   </div>
  `).join('');

  if (footer) {
   footer.style.display = '';
   const total = this.getTotal();
   const count = this.getCount();
   document.getElementById('cart-total').textContent = total > 0 ? `$${total.toLocaleString('en-CA', {minimumFractionDigits: 2})} CAD` : 'Pricing on request';
   document.getElementById('cart-count-footer').textContent = `${count} item${count !== 1 ? 's' : ''}`;
  }
 },

 checkout() {
  const items = this.getItems();
  if (items.length === 0) return;
  this.closeDrawer();
  window.location.href = 'checkout.html';
 },

 // Inject cart drawer HTML into page
 injectUI() {
  // Cart overlay
  const overlay = document.createElement('div');
  overlay.id = 'cart-overlay';
  overlay.className = 'cart-overlay';
  overlay.onclick = () => this.closeDrawer();
  document.body.appendChild(overlay);

  // Cart drawer
  const drawer = document.createElement('div');
  drawer.id = 'cart-drawer';
  drawer.className = 'cart-drawer';
  drawer.innerHTML = `
   <div class="cart-drawer-header">
    <h3>Shopping Cart</h3>
    <button onclick="Cart.closeDrawer()" class="cart-drawer-close">&times;</button>
   </div>
   <div class="cart-drawer-body" id="cart-drawer-body"></div>
   <div class="cart-drawer-footer" id="cart-drawer-footer">
    <div class="cart-summary">
     <span id="cart-count-footer">0 items</span>
     <span id="cart-total" style="font-weight:700;font-size:1.1rem;">$0.00</span>
    </div>
    <button onclick="Cart.checkout()" class="btn btn-primary" style="width:100%;justify-content:center;">
     Proceed to Checkout
    </button>
    <button onclick="Cart.clear()" class="btn btn-outline" style="width:100%;justify-content:center;margin-top:8px;font-size:.8rem;">
     Clear All
    </button>
   </div>
  `;
  document.body.appendChild(drawer);

  this.updateBadge();
 }
};

// Auto-inject on DOM ready
document.addEventListener('DOMContentLoaded', () => {
 Cart.injectUI();
});
