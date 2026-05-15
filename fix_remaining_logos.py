"""Fix remaining logos in admin, checkout, confirmation pages"""

fixes = {
    'admin.html': [
        (
            '<a href="index.html" class="logo"><div><div class="logo-text">EZ-UP <span>Atlantic</span></div><div class="logo-sub">Admin Panel</div></div></a>',
            '<a href="index.html" class="logo"><img src="images/ezup-logo.png" alt="E-Z UP" class="logo-img"><div class="logo-text-wrap"><div class="logo-atlantic">Atlantic</div><div class="logo-sub">Admin Panel</div></div></a>'
        ),
    ],
    'checkout.html': [
        (
            '<a href="index.html" class="logo"><div><div class="logo-text">EZ-UP <span>Atlantic</span></div><div class="logo-sub">Authorized Dealer</div></div></a>',
            '<a href="index.html" class="logo"><img src="images/ezup-logo.png" alt="E-Z UP" class="logo-img"><div class="logo-text-wrap"><div class="logo-atlantic">Atlantic</div><div class="logo-sub">Authorized Dealer</div></div></a>'
        ),
        (
            '<div class="logo-text" style="margin-bottom:12px;">EZ-UP <span style="color:var(--brand-red);">Atlantic</span></div>',
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;"><img src="images/ezup-logo.png" alt="E-Z UP" style="height:32px; filter:brightness(0) invert(1);"><span style="font-size:1.5rem; font-weight:900; color:var(--brand-red);">Atlantic</span></div>'
        ),
    ],
    'confirmation.html': [
        (
            '<a href="index.html" class="logo"><div><div class="logo-text">EZ-UP <span>Atlantic</span></div><div class="logo-sub">Authorized Dealer</div></div></a>',
            '<a href="index.html" class="logo"><img src="images/ezup-logo.png" alt="E-Z UP" class="logo-img"><div class="logo-text-wrap"><div class="logo-atlantic">Atlantic</div><div class="logo-sub">Authorized Dealer</div></div></a>'
        ),
        (
            '<div class="logo-text" style="margin-bottom:12px;">EZ-UP <span style="color:var(--brand-red);">Atlantic</span></div>',
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;"><img src="images/ezup-logo.png" alt="E-Z UP" style="height:32px; filter:brightness(0) invert(1);"><span style="font-size:1.5rem; font-weight:900; color:var(--brand-red);">Atlantic</span></div>'
        ),
    ],
}

for filename, replacements in fixes.items():
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changed = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  [fixed] {filename}")
            changed = True
        else:
            print(f"  [skip]  {filename} — pattern not found")
    
    if changed:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

print("Done!")
