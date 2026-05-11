// ===== EZ-UP Atlantic Checkout JS =====

const PROVINCES = {
 '': 'Select Province...',
 'AB': 'Alberta', 'BC': 'British Columbia', 'MB': 'Manitoba',
 'NB': 'New Brunswick', 'NL': 'Newfoundland & Labrador', 'NS': 'Nova Scotia',
 'NT': 'Northwest Territories', 'NU': 'Nunavut', 'ON': 'Ontario',
 'PE': 'Prince Edward Island', 'QC': 'Quebec', 'SK': 'Saskatchewan', 'YT': 'Yukon'
};

const TAX_RATES = {
 'AB': {total: 5.0, label: 'GST 5%'},
 'BC': {total: 12.0, label: 'GST 5% + PST 7%'},
 'MB': {total: 12.0, label: 'GST 5% + PST 7%'},
 'NB': {total: 15.0, label: 'HST 15%'},
 'NL': {total: 15.0, label: 'HST 15%'},
 'NS': {total: 14.0, label: 'HST 14%'},
 'NT': {total: 5.0, label: 'GST 5%'},
 'NU': {total: 5.0, label: 'GST 5%'},
 'ON': {total: 13.0, label: 'HST 13%'},
 'PE': {total: 15.0, label: 'HST 15%'},
 'QC': {total: 14.975, label: 'GST 5% + QST 9.975%'},
 'SK': {total: 11.0, label: 'GST 5% + PST 6%'},
 'YT': {total: 5.0, label: 'GST 5%'},
};

const provinceOptions = Object.entries(PROVINCES).map(([code, name]) =>
 `<option value="${code}">${name}</option>`
).join('');

let checkoutState = {
 shippingMethod: 'shipping',
 items: [],
};

function initCheckout() {
 const items = Cart.getItems();
 const container = document.getElementById('checkout-content');

 if (!items.length) {
  container.innerHTML = `
   <div class="empty-checkout">
    
    <h2>Your cart is empty</h2>
    <p style="color:var(--text-secondary);margin-bottom:24px;">Add some products before checking out.</p>
    <a href="products.html" class="btn btn-primary">Browse Products</a>
   </div>`;
  return;
 }

 checkoutState.items = items;

 container.innerHTML = `
  <!-- LEFT: Forms -->
  <div class="checkout-forms">

   <!-- Contact Information -->
   <div class="checkout-section">
    <h2><span class="step">1</span> Contact Information</h2>
    <div class="form-row">
     <div class="form-group">
      <label for="c-firstname">First Name *</label>
      <input type="text" id="c-firstname" required>
     </div>
     <div class="form-group">
      <label for="c-lastname">Last Name *</label>
      <input type="text" id="c-lastname" required>
     </div>
    </div>
    <div class="form-row">
     <div class="form-group">
      <label for="c-email">Email Address *</label>
      <input type="email" id="c-email" placeholder="you@example.com" required>
     </div>
     <div class="form-group">
      <label for="c-phone">Phone Number *</label>
      <input type="tel" id="c-phone" placeholder="(902) 456-7890" required>
     </div>
    </div>
   </div>

   <!-- Delivery Method -->
   <div class="checkout-section">
    <h2><span class="step">2</span> Delivery Method</h2>
    <div class="delivery-options">
     <div class="delivery-option" id="opt-pickup" onclick="setDelivery('pickup')">
      
      <div class="label">Local Pickup</div>
      <div class="desc">Free —3797 MacKintosh St, Halifax</div>
     </div>
     <div class="delivery-option active" id="opt-shipping" onclick="setDelivery('shipping')">
      
      <div class="label">Ship to Address</div>
      <div class="desc">Rates calculated at payment</div>
     </div>
    </div>
   </div>

   <!-- Shipping Address -->
   <div class="checkout-section" id="section-shipping">
    <h2><span class="step">3</span> Shipping Address</h2>
    <div class="form-group">
     <label for="s-address">Street Address *</label>
     <input type="text" id="s-address" placeholder="123 Main Street" oninput="syncIfSame()">
    </div>
    <div class="form-group">
     <label for="s-address2">Apartment, Suite, Unit (optional)</label>
     <input type="text" id="s-address2" placeholder="Apt 4B" oninput="syncIfSame()">
    </div>
    <div class="form-row">
     <div class="form-group">
      <label for="s-city">City *</label>
      <input type="text" id="s-city" oninput="syncIfSame()">
     </div>
     <div class="form-group">
      <label for="s-province">Province *</label>
      <select id="s-province" onchange="onShippingProvinceChange()">${provinceOptions}</select>
     </div>
    </div>
    <div class="form-row">
     <div class="form-group">
      <label for="s-postal">Postal Code *</label>
      <input type="text" id="s-postal" placeholder="B3K 5A6" maxlength="7" oninput="syncIfSame()">
     </div>
     <div class="form-group">
      <label for="s-country">Country</label>
      <input type="text" id="s-country" value="Canada" readonly style="background:var(--brand-gray);color:var(--text-secondary);">
     </div>
    </div>
   </div>

   <!-- Billing Address -->
   <div class="checkout-section" id="section-billing">
    <h2><span class="step" id="billing-step">4</span> Billing Address</h2>
    <label class="same-address-check">
     <input type="checkbox" id="same-as-shipping" checked onchange="toggleSameAddress()">
     <span>Same as shipping address</span>
    </label>
    <div id="billing-fields" style="display:none;">
     <div class="form-group" style="margin-top:16px;">
      <label for="b-address">Street Address *</label>
      <input type="text" id="b-address" placeholder="123 Main Street">
     </div>
     <div class="form-group">
      <label for="b-address2">Apartment, Suite, Unit (optional)</label>
      <input type="text" id="b-address2" placeholder="Apt 4B">
     </div>
     <div class="form-row">
      <div class="form-group">
       <label for="b-city">City *</label>
       <input type="text" id="b-city">
      </div>
      <div class="form-group">
       <label for="b-province">Province *</label>
       <select id="b-province">${provinceOptions}</select>
      </div>
     </div>
     <div class="form-row">
      <div class="form-group">
       <label for="b-postal">Postal Code *</label>
       <input type="text" id="b-postal" placeholder="B3K 5A6" maxlength="7">
      </div>
      <div class="form-group">
       <label for="b-country">Country</label>
       <input type="text" id="b-country" value="Canada" readonly style="background:var(--brand-gray);color:var(--text-secondary);">
      </div>
     </div>
    </div>
   </div>
  </div>

  <!-- RIGHT: Order Summary -->
  <div class="order-summary">
   <div class="checkout-section">
    <h2>Order Summary</h2>
    <div id="summary-items">
     ${items.map(item => `
      <div class="summary-item">
       <div class="summary-item-img">
        <img src="${item.img || ''}" alt="${item.name}" onerror="this.style.display='none'">
       </div>
       <div class="summary-item-info">
        <div class="summary-item-name">${item.name}</div>
        ${item.variant ? `<div class="summary-item-variant">${item.variant}</div>` : ''}
        <div class="summary-item-qty">Qty: ${item.qty}</div>
       </div>
       <div class="summary-item-price">${item.price ? '$' + (item.price * item.qty).toLocaleString('en-CA', {minimumFractionDigits: 2}) : 'TBD'}</div>
      </div>
     `).join('')}
    </div>

    <div class="summary-totals" id="summary-totals"></div>

    <button class="pay-btn" id="pay-btn" onclick="startPayment()">
     Pay Securely with Stripe
    </button>

    <div class="secure-badge">
     <div>Secure 256-bit SSL encryption</div>
     <div style="margin-top:4px;">Visa, Mastercard, Amex, Apple Pay, Google Pay</div>
    </div>
   </div>
  </div>
 `;

 updateTotals();
}

// ===== Delivery Toggle =====
function setDelivery(method) {
 checkoutState.shippingMethod = method;
 document.getElementById('opt-pickup').classList.toggle('active', method === 'pickup');
 document.getElementById('opt-shipping').classList.toggle('active', method === 'shipping');

 const shippingSection = document.getElementById('section-shipping');
 const billingSection = document.getElementById('section-billing');

 if (method === 'pickup') {
  shippingSection.style.display = 'none';
  document.getElementById('billing-step').textContent = '3';
  // Uncheck "same as shipping" and show billing fields since there's no shipping address
  document.getElementById('same-as-shipping').checked = false;
  document.getElementById('same-as-shipping').parentElement.style.display = 'none';
  document.getElementById('billing-fields').style.display = 'block';
 } else {
  shippingSection.style.display = '';
  document.getElementById('billing-step').textContent = '4';
  document.getElementById('same-as-shipping').parentElement.style.display = '';
  toggleSameAddress();
 }

 updateTotals();
}

// ===== Same as Shipping =====
function toggleSameAddress() {
 const same = document.getElementById('same-as-shipping').checked;
 document.getElementById('billing-fields').style.display = same ? 'none' : 'block';
 if (same) syncBillingFromShipping();
}

function syncIfSame() {
 if (document.getElementById('same-as-shipping')?.checked) {
  syncBillingFromShipping();
 }
}

function syncBillingFromShipping() {
 const fields = ['address', 'address2', 'city', 'province', 'postal'];
 fields.forEach(f => {
  const src = document.getElementById('s-' + f);
  const dst = document.getElementById('b-' + f);
  if (src && dst) dst.value = src.value;
 });
}

// ===== Province Change → Tax Update =====
function onShippingProvinceChange() {
 syncIfSame();
 updateTotals();
}

function getProvince() {
 if (checkoutState.shippingMethod === 'pickup') {
  // Use billing province for pickup orders
  return document.getElementById('b-province')?.value || 'NS';
 }
 return document.getElementById('s-province')?.value || '';
}

// ===== Totals =====
const SHIPPING_FLAT = 75;
const FREE_SHIPPING_THRESHOLD = 500;

function getShippingCost(subtotal) {
 if (checkoutState.shippingMethod === 'pickup') return 0;
 return subtotal >= FREE_SHIPPING_THRESHOLD ? 0 : SHIPPING_FLAT;
}

function updateTotals() {
 const items = checkoutState.items;
 const subtotal = items.reduce((s, i) => s + (i.price || 0) * i.qty, 0);
 const province = getProvince();
 const taxInfo = TAX_RATES[province];
 const shippingCost = getShippingCost(subtotal);
 const taxAmount = taxInfo ? Math.round(subtotal * taxInfo.total) / 100 : 0;
 const total = subtotal + taxAmount + shippingCost;

 checkoutState.shippingCost = shippingCost;

 const el = document.getElementById('summary-totals');
 if (!el) return;

 let shippingDisplay;
 if (checkoutState.shippingMethod === 'pickup') {
  shippingDisplay = '<span style="color:#16a34a;font-weight:600;">Free (Pickup)</span>';
 } else if (shippingCost === 0) {
  shippingDisplay = '<span style="color:#16a34a;font-weight:600;">Free</span>';
 } else {
  shippingDisplay = `$${shippingCost.toFixed(2)}`;
 }

 const freeShipMsg = checkoutState.shippingMethod === 'shipping' && subtotal < FREE_SHIPPING_THRESHOLD
  ? `<div class="summary-row" style="font-size:.75rem;color:#16a34a;padding:2px 0;">Spend $${(FREE_SHIPPING_THRESHOLD - subtotal).toFixed(2)} more for free shipping!</div>`
  : '';

 el.innerHTML = `
  <div class="summary-row">
   <span>Subtotal (${items.reduce((s, i) => s + i.qty, 0)} items)</span>
   <span>$${subtotal.toLocaleString('en-CA', {minimumFractionDigits: 2})}</span>
  </div>
  <div class="summary-row">
   <span class="tax-label">Tax${taxInfo ? ' — ' + taxInfo.label : ''}</span>
   <span>${province ? '$' + taxAmount.toLocaleString('en-CA', {minimumFractionDigits: 2}) : 'Select province'}</span>
  </div>
  <div class="summary-row">
   <span>Shipping</span>
   ${shippingDisplay}
  </div>
  ${freeShipMsg}
  <div class="summary-row total">
   <span>Total</span>
   <span>$${total.toLocaleString('en-CA', {minimumFractionDigits: 2})} CAD</span>
  </div>
 `;
}

// ===== Payment =====
async function startPayment() {
 // Validate contact
 const firstName = document.getElementById('c-firstname')?.value?.trim();
 const lastName = document.getElementById('c-lastname')?.value?.trim();
 const email = document.getElementById('c-email')?.value?.trim();
 const phone = document.getElementById('c-phone')?.value?.trim();

 if (!firstName || !lastName) { alert('Please enter your full name.'); return; }
 if (!email || !email.includes('@')) { alert('Please enter a valid email address.'); return; }
 if (!phone) { alert('Please enter your phone number.'); return; }

 // Validate shipping address (if shipping)
 if (checkoutState.shippingMethod === 'shipping') {
  const sAddr = document.getElementById('s-address')?.value?.trim();
  const sCity = document.getElementById('s-city')?.value?.trim();
  const sProv = document.getElementById('s-province')?.value;
  const sPostal = document.getElementById('s-postal')?.value?.trim();
  if (!sAddr || !sCity || !sProv || !sPostal) {
   alert('Please complete your shipping address.'); return;
  }
 }

 // Validate billing address (if not same as shipping)
 const sameAsShipping = document.getElementById('same-as-shipping')?.checked;
 if (!sameAsShipping || checkoutState.shippingMethod === 'pickup') {
  const bAddr = document.getElementById('b-address')?.value?.trim();
  const bCity = document.getElementById('b-city')?.value?.trim();
  const bProv = document.getElementById('b-province')?.value;
  const bPostal = document.getElementById('b-postal')?.value?.trim();
  if (!bAddr || !bCity || !bProv || !bPostal) {
   alert('Please complete your billing address.'); return;
  }
 }

 // Sync billing if same
 if (sameAsShipping && checkoutState.shippingMethod === 'shipping') {
  syncBillingFromShipping();
 }

 const province = getProvince();

 const btn = document.getElementById('pay-btn');
 btn.disabled = true;
 btn.innerHTML = 'Redirecting to secure payment...';

 try {
  const response = await fetch('/api/create-checkout-session', {
   method: 'POST',
   headers: {'Content-Type': 'application/json'},
   body: JSON.stringify({
    items: checkoutState.items,
    province: province,
    shippingMethod: checkoutState.shippingMethod,
    shippingCost: checkoutState.shippingCost || 0,
    customer: {
     name: `${firstName} ${lastName}`,
     email, phone,
     shipping: checkoutState.shippingMethod === 'shipping' ? {
      address: document.getElementById('s-address')?.value,
      address2: document.getElementById('s-address2')?.value,
      city: document.getElementById('s-city')?.value,
      province: document.getElementById('s-province')?.value,
      postal: document.getElementById('s-postal')?.value,
     } : null,
     billing: {
      address: document.getElementById('b-address')?.value || document.getElementById('s-address')?.value,
      address2: document.getElementById('b-address2')?.value || document.getElementById('s-address2')?.value,
      city: document.getElementById('b-city')?.value || document.getElementById('s-city')?.value,
      province: document.getElementById('b-province')?.value || document.getElementById('s-province')?.value,
      postal: document.getElementById('b-postal')?.value || document.getElementById('s-postal')?.value,
     },
    },
   }),
  });

  const data = await response.json();

  if (data.error) {
   alert('Error: ' + data.error);
   btn.disabled = false;
   btn.innerHTML = 'Pay Securely with Stripe';
   return;
  }

  if (data.url) {
   Cart.clear();
   window.location.href = data.url;
  }
 } catch (err) {
  alert('Unable to connect to payment server. Please try again.');
  btn.disabled = false;
  btn.innerHTML = 'Pay Securely with Stripe';
 }
}

document.addEventListener('DOMContentLoaded', initCheckout);
