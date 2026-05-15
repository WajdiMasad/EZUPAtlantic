"""Update logo HTML across all pages to use the official E-Z UP image + Atlantic text"""
import glob

old_logo = '''<div>
          <div class="logo-text">EZ-UP <span>Atlantic</span></div>
          <div class="logo-sub">Authorized Dealer</div>
        </div>'''

new_logo = '''<img src="images/ezup-logo.png" alt="E-Z UP" class="logo-img">
        <div class="logo-text-wrap">
          <div class="logo-atlantic">Atlantic</div>
          <div class="logo-sub">Authorized Dealer</div>
        </div>'''

# Also check for footer logo-text usage
old_footer_logo = '<div class="logo-text" style="margin-bottom:20px;">EZ-UP <span style="color:var(--brand-red);">Atlantic</span></div>'
new_footer_logo = '''<div style="display:flex; align-items:center; gap:8px; margin-bottom:20px;">
          <img src="images/ezup-logo.png" alt="E-Z UP" style="height:32px; filter:brightness(0) invert(1);">
          <span style="font-size:1.5rem; font-weight:900; color:var(--brand-red);">Atlantic</span>
        </div>'''

count = 0
for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    original = content
    
    # Replace header logo
    if old_logo in content:
        content = content.replace(old_logo, new_logo)
        print(f"  [header] {f}")
    
    # Replace footer logo
    if old_footer_logo in content:
        content = content.replace(old_footer_logo, new_footer_logo)
        print(f"  [footer] {f}")
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        count += 1

print(f"\nUpdated {count} files")
