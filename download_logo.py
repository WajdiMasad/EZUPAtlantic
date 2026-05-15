"""Download E-Z UP official logo"""
import urllib.request
import os

# Try the US site logo first
urls = [
    ('https://www.ezup.com/media/logo/stores/1/main-logo-blue-1.png', 'images/ezup-logo.png'),
    ('https://www.ezup.ca/cdn/shop/files/ezup.ca-Logo-no-BG_8b0c8d3d-cfed-4599-bba7-b3e60a3e5ccc.png?v=1717711308', 'images/ezup-logo-ca.png'),
]

for url, path in urls:
    try:
        urllib.request.urlretrieve(url, path)
        size = os.path.getsize(path)
        print(f"OK: {path} — {size} bytes")
    except Exception as e:
        print(f"FAIL: {path} — {e}")
