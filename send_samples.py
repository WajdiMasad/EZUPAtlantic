"""Send all 3 email samples to info@giantpro.com"""
import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from orders import _send_email, _build_items_html, STORE_EMAIL, SMTP_USER

# Sample order data
order = {
    'order_number': 'EZUP-20260519-SAMPLE',
    'customer_name': 'John Smith',
    'customer_email': 'john@smithenterprises.ca',
    'customer_phone': '902-555-1234',
    'province': 'NS',
    'shipping_method': 'shipping',
    'shipping_cost': 0,
    'items': [
        {'name': 'Eclipse Shelter', 'variant': "10' x 10' — Blue", 'qty': 1, 'price': 1299.00},
        {'name': 'Duralon Sidewall 4 Pack', 'variant': '', 'qty': 1, 'price': 240.00},
        {'name': 'Deluxe Roller Bag', 'variant': '', 'qty': 1, 'price': 149.00},
    ],
    'subtotal': 1688.00,
    'tax_rate': 14.0,
    'tax_amount': 236.32,
    'total': 1924.32,
    'shipping_address': {
        'address': '123 Main St',
        'city': 'Dartmouth',
        'province': 'NS',
        'postal': 'B2Y 1A1',
    },
}

quote = {
    'name': 'Sarah Thompson',
    'email': 'sarah@eastcoastevents.ca',
    'phone': '506-555-9876',
    'product': 'Custom Printed Canopy',
    'message': 'Hi there,\n\nI\'m looking for a 10x10 custom printed canopy tent for our event planning business. We run about 20 outdoor events per season across New Brunswick.\n\nI\'d like:\n- Full color print with our logo on the canopy top\n- 2 custom printed sidewalls\n- Matching 6ft table cover\n\nCan you send me pricing for the Endeavor model? We may need 2 units.\n\nThanks,\nSarah Thompson\nEast Coast Events Inc.',
}

# ==============================
# EMAIL 1: Customer Confirmation
# ==============================
print("Sending Email 1/3: Customer Order Confirmation...")

items_html = _build_items_html(order['items'])
shipping = order.get('shipping_address', {})
ship_text = f"{shipping.get('address','')}, {shipping.get('city','')}, {shipping.get('province','')} {shipping.get('postal','')}"

customer_html = f'''<!DOCTYPE html>
<html><body style="font-family:Arial,Helvetica,sans-serif;margin:0;padding:0;background:#f5f5f7;">
<div style="max-width:600px;margin:0 auto;background:#fff;">
    <div style="background:#003B71;padding:32px;text-align:center;">
        <h1 style="color:#fff;margin:0;font-size:24px;">EZ-UP <span style="color:#E31937;">Atlantic</span></h1>
        <p style="color:rgba(255,255,255,0.7);margin:8px 0 0;font-size:13px;">AUTHORIZED DEALER</p>
    </div>
    <div style="padding:32px;">
        <h2 style="color:#003B71;margin-top:0;">Thank you for your order!</h2>
        <p style="color:#555;line-height:1.6;">Hi {order['customer_name']},</p>
        <p style="color:#555;line-height:1.6;">We have received your order and it is now being processed. You will receive another email when your order ships or is ready for pickup.</p>

        <div style="background:#f5f5f7;border-radius:8px;padding:20px;margin:24px 0;">
            <table style="width:100%;font-size:14px;color:#333;">
                <tr><td style="font-weight:bold;padding:4px 0;">Order Number</td><td style="text-align:right;">{order['order_number']}</td></tr>
                <tr><td style="font-weight:bold;padding:4px 0;">Date</td><td style="text-align:right;">{datetime.now().strftime("%B %d, %Y")}</td></tr>
                <tr><td style="font-weight:bold;padding:4px 0;">Delivery</td><td style="text-align:right;">Shipping — {ship_text}</td></tr>
            </table>
        </div>

        <h3 style="color:#003B71;border-bottom:2px solid #003B71;padding-bottom:8px;">Order Details</h3>
        <table style="width:100%;border-collapse:collapse;font-size:14px;">
            <thead><tr style="color:#999;font-size:12px;text-transform:uppercase;">
                <th style="text-align:left;padding:8px 0;">Item</th>
                <th style="text-align:center;padding:8px 0;">Qty</th>
                <th style="text-align:right;padding:8px 0;">Amount</th>
            </tr></thead>
            <tbody>{items_html}</tbody>
        </table>

        <table style="width:100%;font-size:14px;margin-top:16px;">
            <tr><td style="padding:4px 0;color:#666;">Subtotal</td><td style="text-align:right;">${order['subtotal']:,.2f}</td></tr>
            <tr><td style="padding:4px 0;color:#666;">Tax ({order['province']} — HST 14%)</td><td style="text-align:right;">${order['tax_amount']:,.2f}</td></tr>
            <tr><td style="padding:4px 0;color:#666;">Shipping</td><td style="text-align:right;">Free</td></tr>
            <tr style="font-size:18px;font-weight:bold;color:#003B71;">
                <td style="padding:12px 0;border-top:2px solid #003B71;">Total</td>
                <td style="text-align:right;padding:12px 0;border-top:2px solid #003B71;">${order['total']:,.2f} CAD</td>
            </tr>
        </table>

        <div style="margin-top:32px;padding-top:24px;border-top:1px solid #eee;font-size:13px;color:#999;text-align:center;">
            <p>Questions? Contact us at <a href="mailto:info@giantpro.com" style="color:#003B71;">info@giantpro.com</a> or call <a href="tel:902-456-6487" style="color:#003B71;">902-456-6487</a></p>
            <p style="margin-top:16px;">&copy; {datetime.now().year} EZ-UP Atlantic, a division of Giant Promotions Ltd.<br>3797 MacKintosh St, Halifax, NS B3K 5A6</p>
        </div>
    </div>
</div>
</body></html>'''

r1 = _send_email(STORE_EMAIL, f'[SAMPLE] Order Confirmation — {order["order_number"]}', customer_html)
print(f"  -> {'SENT' if r1 else 'FAILED'}")


# ==============================
# EMAIL 2: Store Order Notification
# ==============================
print("Sending Email 2/3: Store Order Notification...")

items_text = '\n'.join([
    f"  {i.get('qty',1)}x {i.get('name','')} {('('+i.get('variant','')+')') if i.get('variant') else ''} — ${i.get('price',0)*i.get('qty',1):,.2f}"
    for i in order['items']
])

store_html = f'''<html><body style="font-family:Arial,sans-serif;">
    <h2 style="color:#003B71;">New Order Received!</h2>
    <table style="font-size:14px;color:#333;">
        <tr><td style="font-weight:bold;padding:4px 8px;">Order:</td><td>{order['order_number']}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Customer:</td><td>{order['customer_name']}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Email:</td><td>{order['customer_email']}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Phone:</td><td>{order['customer_phone']}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Delivery:</td><td>Shipping</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Province:</td><td>{order['province']}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Total:</td><td style="font-size:18px;color:#003B71;font-weight:bold;">${order['total']:,.2f} CAD</td></tr>
    </table>
    <h3>Items</h3>
    <pre style="background:#f5f5f7;padding:16px;border-radius:8px;font-size:13px;">{items_text}</pre>
    <p><a href="http://localhost:8080/admin.html" style="color:#003B71;">View in Admin Panel</a></p>
    </body></html>'''

r2 = _send_email(STORE_EMAIL, f'[SAMPLE] New Order {order["order_number"]} — ${order["total"]:,.2f}', store_html)
print(f"  -> {'SENT' if r2 else 'FAILED'}")


# ==============================
# EMAIL 3: Quote Request Notification
# ==============================
print("Sending Email 3/3: Quote Request Notification...")

quote_id = 'QR-20260519-SAMPLE'
quote_html = f'''<html><body style="font-family:Arial,sans-serif;">
    <h2 style="color:#003B71;">New Quote Request!</h2>
    <p style="color:#666;">A customer has submitted a quote request on the website.</p>
    <table style="font-size:14px;color:#333;border-collapse:collapse;">
        <tr><td style="font-weight:bold;padding:8px 12px;background:#f5f5f7;">Quote ID:</td><td style="padding:8px 12px;background:#f5f5f7;">{quote_id}</td></tr>
        <tr><td style="font-weight:bold;padding:8px 12px;">Name:</td><td style="padding:8px 12px;">{quote['name']}</td></tr>
        <tr><td style="font-weight:bold;padding:8px 12px;background:#f5f5f7;">Email:</td><td style="padding:8px 12px;background:#f5f5f7;"><a href="mailto:{quote['email']}">{quote['email']}</a></td></tr>
        <tr><td style="font-weight:bold;padding:8px 12px;">Phone:</td><td style="padding:8px 12px;">{quote['phone']}</td></tr>
        <tr><td style="font-weight:bold;padding:8px 12px;background:#f5f5f7;">Product Interest:</td><td style="padding:8px 12px;background:#f5f5f7;">{quote['product']}</td></tr>
    </table>
    <div style="margin-top:16px;padding:16px;background:#f5f5f7;border-radius:8px;border-left:4px solid #003B71;">
        <strong>Message:</strong><br>
        <p style="margin:8px 0 0;white-space:pre-wrap;">{quote['message']}</p>
    </div>
    <p style="margin-top:20px;"><a href="http://localhost:8080/admin.html" style="color:#003B71;font-weight:bold;">View in Admin Panel</a></p>
    </body></html>'''

r3 = _send_email(STORE_EMAIL, f'[SAMPLE] New Quote Request {quote_id} — {quote["name"]}', quote_html)
print(f"  -> {'SENT' if r3 else 'FAILED'}")

print(f"\nDone! Check inbox at {STORE_EMAIL}")
