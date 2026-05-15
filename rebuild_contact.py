"""Rebuild contact page body section with premium card-based layout"""

with open('contact.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find markers
start_marker = '  <section class="page-hero">'
end_marker = '  <!-- Footer -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"ERROR: markers not found. start={start_idx}, end={end_idx}")
    exit(1)

head = content[:start_idx]
tail = content[end_idx:]

new_body = """  <section class="page-hero">
    <div class="container animate-in">
      <h1>Get in Touch</h1>
      <p>Get personalized pricing on any E-Z UP\u00ae product</p>
    </div>
  </section>

  <!-- Contact Content -->
  <section class="section" style="background:var(--brand-gray); padding: 80px 0;">
    <div class="container">
      <div style="display:grid; grid-template-columns: 1.3fr 1fr; gap:48px; align-items:start;">

        <!-- LEFT: Quote Form Card -->
        <div class="animate-in" style="background:#fff; border-radius:var(--radius-md); padding:48px; box-shadow:var(--shadow-md);">
          <div style="margin-bottom:32px;">
            <h2 style="font-size:1.8rem; font-weight:800; margin-bottom:8px; color:var(--text-primary);">Request a Quote</h2>
            <p style="color:var(--text-secondary); font-size:0.95rem; line-height:1.6;">Fill out the form below and our team will get back to you within 24 hours with personalized pricing.</p>
          </div>
          <form id="quote-form" class="quote-form">
            <div class="form-row">
              <div class="form-group">
                <label for="name">Full Name *</label>
                <input type="text" id="name" name="name" required placeholder="Your name">
              </div>
              <div class="form-group">
                <label for="email">Email Address *</label>
                <input type="email" id="email" name="email" required placeholder="you@example.com">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="phone">Phone Number</label>
                <input type="tel" id="phone" name="phone" placeholder="(902) 000-0000">
              </div>
              <div class="form-group">
                <label for="product">Product Interest</label>
                <select id="product" name="product">
                  <option value="">Select a category...</option>
                  <option value="Canopy Tents">Canopy Tents</option>
                  <option value="Custom Printed Canopy">Custom Printed Canopy</option>
                  <option value="Custom Package">Custom Package</option>
                  <option value="Sidewalls &amp; Accessories">Sidewalls &amp; Accessories</option>
                  <option value="Lighting">Lighting &amp; Power</option>
                  <option value="Camping">Camping &amp; Recreation</option>
                  <option value="Tables &amp; Chairs">Tables &amp; Chairs</option>
                  <option value="Other">Other / Not Sure</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label for="message">Message / Details *</label>
              <textarea id="message" name="message" required placeholder="Tell us about your needs \u2014 quantity, sizes, custom printing requirements, event details, etc."></textarea>
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%; justify-content:center; padding:18px; font-size:1rem; letter-spacing:0.5px; gap:10px;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
              Submit Quote Request
            </button>
          </form>
        </div>

        <!-- RIGHT: Contact Info Cards -->
        <div class="animate-in" style="display:flex; flex-direction:column; gap:24px; animation-delay:0.15s;">
          <!-- Visit Us -->
          <div style="background:#fff; border-radius:var(--radius-md); padding:32px; box-shadow:var(--shadow-sm);">
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
              <div style="width:48px; height:48px; background:rgba(227,25,55,0.08); border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#E31937" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              </div>
              <h3 style="font-size:1.15rem; font-weight:700;">Visit Us</h3>
            </div>
            <div style="margin-left:64px;">
              <p style="font-weight:700; color:var(--text-primary); margin-bottom:6px;">Giant Promotions Ltd.</p>
              <p style="color:var(--text-secondary); line-height:1.8; font-size:0.95rem;">3797 MacKintosh St<br>Halifax, NS, B3K 5A6<br>Canada</p>
            </div>
          </div>
          <!-- Call Us -->
          <div style="background:#fff; border-radius:var(--radius-md); padding:32px; box-shadow:var(--shadow-sm);">
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
              <div style="width:48px; height:48px; background:rgba(0,59,113,0.08); border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#003B71" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              </div>
              <h3 style="font-size:1.15rem; font-weight:700;">Call Us</h3>
            </div>
            <div style="margin-left:64px;">
              <a href="tel:902-456-6487" style="color:var(--brand-blue); font-size:1.4rem; font-weight:800; display:block; margin-bottom:6px;">902-456-6487</a>
              <p style="color:var(--text-secondary); font-size:0.9rem;">Monday \u2013 Friday: 9am \u2013 5pm AST</p>
            </div>
          </div>
          <!-- Email Us -->
          <div style="background:#fff; border-radius:var(--radius-md); padding:32px; box-shadow:var(--shadow-sm);">
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
              <div style="width:48px; height:48px; background:rgba(227,25,55,0.08); border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#E31937" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              </div>
              <h3 style="font-size:1.15rem; font-weight:700;">Email Us</h3>
            </div>
            <div style="margin-left:64px;">
              <a href="mailto:info@giantpro.com" style="color:var(--brand-blue); font-size:1.1rem; font-weight:700; display:block; margin-bottom:6px;">info@giantpro.com</a>
              <p style="color:var(--text-secondary); font-size:0.9rem;">We typically respond within 24 hours</p>
            </div>
          </div>
          <!-- Shipping Info -->
          <div style="background:linear-gradient(135deg, var(--brand-blue) 0%, #0056A8 100%); border-radius:var(--radius-md); padding:32px; color:#fff;">
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
              <div style="width:48px; height:48px; background:rgba(255,255,255,0.15); border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
              </div>
              <h3 style="font-size:1.15rem; font-weight:700;">Shipping Info</h3>
            </div>
            <div style="margin-left:64px;">
              <p style="font-size:0.95rem; line-height:1.8; opacity:0.92;"><strong style="color:#fff;">Free shipping</strong> on orders over $500 CAD<br><strong style="color:#fff;">$75 flat rate</strong> for orders under $500<br><strong style="color:#fff;">Local pickup</strong> available in Halifax</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Google Maps Embed -->
      <div class="animate-in" style="margin-top:64px; border-radius:var(--radius-md); overflow:hidden; box-shadow:var(--shadow-md); height:350px;">
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2838.5!2d-63.5975!3d44.6588!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4b5a21!2sGiant+Promotions!5e0!3m2!1sen!2sca!4v1700000000000!5m2!1sen!2sca" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="EZ-UP Atlantic Location - Giant Promotions Ltd, Halifax NS"></iframe>
      </div>
    </div>
  </section>

"""

with open('contact.html', 'w', encoding='utf-8') as f:
    f.write(head + new_body + tail)

print(f"Done! head={len(head)} chars, new_body={len(new_body)} chars, tail={len(tail)} chars")
