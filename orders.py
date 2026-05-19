"""
EZ-UP Atlantic — Order Management System
SQLite database + email notifications
"""
import sqlite3
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'orders.db')

# Email config — set these env vars
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASS = os.environ.get('SMTP_PASS', '')
STORE_EMAIL = os.environ.get('STORE_EMAIL', 'info@giantpro.com')
STORE_NAME = 'EZ-UP Atlantic'
DOMAIN = os.environ.get('DOMAIN', 'http://localhost:8080')


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        stripe_session_id TEXT,
        status TEXT DEFAULT 'paid',
        customer_name TEXT,
        customer_email TEXT,
        customer_phone TEXT,
        shipping_address TEXT,
        billing_address TEXT,
        province TEXT,
        shipping_method TEXT,
        items TEXT,
        subtotal REAL,
        tax_rate REAL,
        tax_amount REAL,
        shipping_cost REAL DEFAULT 0,
        total REAL,
        currency TEXT DEFAULT 'CAD',
        notes TEXT,
        created_at TEXT,
        updated_at TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote_id TEXT UNIQUE NOT NULL,
        status TEXT DEFAULT 'new',
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        product_interest TEXT,
        message TEXT,
        created_at TEXT,
        notes TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT NOT NULL,
        product_name TEXT NOT NULL,
        variant TEXT,
        sku TEXT,
        category TEXT,
        stock_qty INTEGER DEFAULT 0,
        low_stock_threshold INTEGER DEFAULT 2,
        last_updated TEXT,
        UNIQUE(product_id, variant)
    )''')
    conn.commit()
    conn.close()


# ===== INVENTORY MANAGEMENT =====

def get_all_inventory(search='', filter_type='all', limit=100, offset=0):
    """Get inventory with optional search and filter"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    where_clauses = []
    params = []

    if search:
        where_clauses.append("(product_name LIKE ? OR sku LIKE ? OR variant LIKE ?)")
        s = f'%{search}%'
        params.extend([s, s, s])

    if filter_type == 'low':
        where_clauses.append("stock_qty > 0 AND stock_qty <= low_stock_threshold")
    elif filter_type == 'out':
        where_clauses.append("stock_qty = 0")
    elif filter_type == 'instock':
        where_clauses.append("stock_qty > low_stock_threshold")

    where = 'WHERE ' + ' AND '.join(where_clauses) if where_clauses else ''
    rows = conn.execute(
        f'SELECT * FROM inventory {where} ORDER BY product_name, variant LIMIT ? OFFSET ?',
        params + [limit, offset]
    ).fetchall()

    total = conn.execute(
        f'SELECT COUNT(*) FROM inventory {where}', params
    ).fetchone()[0]

    conn.close()
    return {
        'items': [dict(r) for r in rows],
        'total': total,
        'limit': limit,
        'offset': offset,
    }


def update_stock(product_id, variant, qty, threshold=None):
    """Update stock quantity for a product+variant"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    now = datetime.now().isoformat()

    if threshold is not None:
        conn.execute('''UPDATE inventory
            SET stock_qty=?, low_stock_threshold=?, last_updated=?
            WHERE product_id=? AND (variant=? OR (variant IS NULL AND ? IS NULL))''',
            (qty, threshold, now, product_id, variant, variant))
    else:
        conn.execute('''UPDATE inventory
            SET stock_qty=?, last_updated=?
            WHERE product_id=? AND (variant=? OR (variant IS NULL AND ? IS NULL))''',
            (qty, now, product_id, variant, variant))

    conn.commit()
    conn.close()


def bulk_import_inventory(products_data):
    """Import product catalog into inventory table (skip existing)"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    now = datetime.now().isoformat()
    imported = 0

    for product in products_data:
        pid = product.get('id', '')
        pname = product.get('name', '')
        category = product.get('category', '')
        variants = product.get('variants', [])

        if variants:
            for v in variants:
                try:
                    conn.execute('''INSERT OR IGNORE INTO inventory
                        (product_id, product_name, variant, sku, category, stock_qty, last_updated)
                        VALUES (?, ?, ?, ?, ?, 0, ?)''',
                        (pid, pname, v.get('name'), v.get('sku', ''), category, now))
                    imported += 1
                except sqlite3.IntegrityError:
                    pass
        else:
            try:
                conn.execute('''INSERT OR IGNORE INTO inventory
                    (product_id, product_name, variant, sku, category, stock_qty, last_updated)
                    VALUES (?, ?, NULL, ?, ?, 0, ?)''',
                    (pid, pname, product.get('sku', ''), category, now))
                imported += 1
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    total = conn.execute('SELECT COUNT(*) FROM inventory').fetchone()[0]
    conn.close()
    return {'imported': imported, 'total': total}


def deduct_stock(items):
    """Deduct stock for ordered items. Called after order is saved."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    now = datetime.now().isoformat()

    for item in items:
        product_id = item.get('id', '')
        variant = item.get('variant', None)
        qty = item.get('qty', 1)

        if variant:
            conn.execute('''UPDATE inventory
                SET stock_qty = MAX(0, stock_qty - ?), last_updated = ?
                WHERE product_id = ? AND variant = ?''',
                (qty, now, product_id, variant))
        else:
            conn.execute('''UPDATE inventory
                SET stock_qty = MAX(0, stock_qty - ?), last_updated = ?
                WHERE product_id = ? AND variant IS NULL''',
                (qty, now, product_id))

    conn.commit()
    conn.close()


def get_inventory_stats():
    """Get inventory dashboard stats"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    stats = {
        'total_skus': conn.execute('SELECT COUNT(*) FROM inventory').fetchone()[0],
        'in_stock': conn.execute('SELECT COUNT(*) FROM inventory WHERE stock_qty > low_stock_threshold').fetchone()[0],
        'low_stock': conn.execute('SELECT COUNT(*) FROM inventory WHERE stock_qty > 0 AND stock_qty <= low_stock_threshold').fetchone()[0],
        'out_of_stock': conn.execute('SELECT COUNT(*) FROM inventory WHERE stock_qty = 0').fetchone()[0],
        'total_units': conn.execute('SELECT COALESCE(SUM(stock_qty), 0) FROM inventory').fetchone()[0],
    }
    conn.close()
    return stats


def generate_order_number():
    now = datetime.now()
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute('SELECT COUNT(*) FROM orders WHERE created_at LIKE ?',
                         (now.strftime('%Y-%m-%d') + '%',)).fetchone()[0]
    conn.close()
    return f"EZUP-{now.strftime('%Y%m%d')}-{count + 1:04d}"


def save_order(order_data):
    init_db()
    now = datetime.now().isoformat()
    order_number = generate_order_number()

    conn = sqlite3.connect(DB_PATH)
    conn.execute('''INSERT INTO orders
        (order_number, stripe_session_id, status, customer_name, customer_email,
         customer_phone, shipping_address, billing_address, province, shipping_method,
         items, subtotal, tax_rate, tax_amount, shipping_cost, total, currency, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (order_number, order_data.get('stripe_session_id'),
         order_data.get('status', 'paid'),
         order_data.get('customer_name'), order_data.get('customer_email'),
         order_data.get('customer_phone'),
         json.dumps(order_data.get('shipping_address', {})),
         json.dumps(order_data.get('billing_address', {})),
         order_data.get('province'), order_data.get('shipping_method'),
         json.dumps(order_data.get('items', [])),
         order_data.get('subtotal', 0), order_data.get('tax_rate', 0),
         order_data.get('tax_amount', 0), order_data.get('shipping_cost', 0),
         order_data.get('total', 0), 'CAD', now, now))
    conn.commit()
    conn.close()
    return order_number


def get_order(order_number):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute('SELECT * FROM orders WHERE order_number = ?', (order_number,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d['items'] = json.loads(d['items']) if d['items'] else []
        d['shipping_address'] = json.loads(d['shipping_address']) if d['shipping_address'] else {}
        d['billing_address'] = json.loads(d['billing_address']) if d['billing_address'] else {}
        return d
    return None


def get_all_orders(limit=100, offset=0):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute('SELECT * FROM orders ORDER BY created_at DESC LIMIT ? OFFSET ?',
                        (limit, offset)).fetchall()
    conn.close()
    orders = []
    for row in rows:
        d = dict(row)
        d['items'] = json.loads(d['items']) if d['items'] else []
        orders.append(d)
    return orders


def update_order_status(order_number, status, notes=None):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    now = datetime.now().isoformat()
    if notes:
        conn.execute('UPDATE orders SET status=?, notes=?, updated_at=? WHERE order_number=?',
                     (status, notes, now, order_number))
    else:
        conn.execute('UPDATE orders SET status=?, updated_at=? WHERE order_number=?',
                     (status, now, order_number))
    conn.commit()
    conn.close()


def get_order_stats():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    stats = {
        'total_orders': conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0],
        'total_revenue': conn.execute('SELECT COALESCE(SUM(total),0) FROM orders WHERE status="paid"').fetchone()[0],
        'pending': conn.execute('SELECT COUNT(*) FROM orders WHERE status="pending"').fetchone()[0],
        'paid': conn.execute('SELECT COUNT(*) FROM orders WHERE status="paid"').fetchone()[0],
        'shipped': conn.execute('SELECT COUNT(*) FROM orders WHERE status="shipped"').fetchone()[0],
        'today_orders': conn.execute("SELECT COUNT(*) FROM orders WHERE date(created_at)=date('now')").fetchone()[0],
        'today_revenue': conn.execute("SELECT COALESCE(SUM(total),0) FROM orders WHERE date(created_at)=date('now') AND status='paid'").fetchone()[0],
    }
    conn.close()
    return stats


# ===== EMAIL =====

def _build_items_html(items):
    rows = ''
    for item in items:
        name = item.get('name', 'Product')
        variant = item.get('variant', '')
        qty = item.get('qty', 1)
        price = item.get('price', 0)
        rows += f'''<tr>
            <td style="padding:10px 0;border-bottom:1px solid #eee;">{name}{f"<br><small style='color:#666'>{variant}</small>" if variant else ""}</td>
            <td style="padding:10px 0;border-bottom:1px solid #eee;text-align:center;">{qty}</td>
            <td style="padding:10px 0;border-bottom:1px solid #eee;text-align:right;">${price * qty:,.2f}</td>
        </tr>'''
    return rows


def send_customer_confirmation(order):
    if not SMTP_USER:
        print("[EMAIL] SMTP not configured, skipping customer email")
        return False

    items_html = _build_items_html(order.get('items', []))
    shipping = order.get('shipping_address', {})
    ship_text = ''
    if order.get('shipping_method') == 'shipping' and shipping:
        ship_text = f"{shipping.get('address','')}, {shipping.get('city','')}, {shipping.get('province','')} {shipping.get('postal','')}"
    else:
        ship_text = 'Local Pickup — 3797 MacKintosh St, Halifax, NS'

    html = f'''<!DOCTYPE html>
<html><body style="font-family:Arial,Helvetica,sans-serif;margin:0;padding:0;background:#f5f5f7;">
<div style="max-width:600px;margin:0 auto;background:#fff;">
    <div style="background:#003B71;padding:32px;text-align:center;">
        <h1 style="color:#fff;margin:0;font-size:24px;">EZ-UP <span style="color:#E31937;">Atlantic</span></h1>
        <p style="color:rgba(255,255,255,0.7);margin:8px 0 0;font-size:13px;">AUTHORIZED DEALER</p>
    </div>
    <div style="padding:32px;">
        <h2 style="color:#003B71;margin-top:0;">Thank you for your order!</h2>
        <p style="color:#555;line-height:1.6;">Hi {order.get("customer_name","")},</p>
        <p style="color:#555;line-height:1.6;">We have received your order and it is now being processed. You will receive another email when your order ships or is ready for pickup.</p>

        <div style="background:#f5f5f7;border-radius:8px;padding:20px;margin:24px 0;">
            <table style="width:100%;font-size:14px;color:#333;">
                <tr><td style="font-weight:bold;padding:4px 0;">Order Number</td><td style="text-align:right;">{order.get("order_number","")}</td></tr>
                <tr><td style="font-weight:bold;padding:4px 0;">Date</td><td style="text-align:right;">{datetime.now().strftime("%B %d, %Y")}</td></tr>
                <tr><td style="font-weight:bold;padding:4px 0;">Name</td><td style="text-align:right;">{order.get("customer_name","")}</td></tr>
                <tr><td style="font-weight:bold;padding:4px 0;">Email</td><td style="text-align:right;">{order.get("customer_email","")}</td></tr>
                <tr><td style="font-weight:bold;padding:4px 0;">Phone</td><td style="text-align:right;">{order.get("customer_phone","")}</td></tr>
                <tr><td style="font-weight:bold;padding:4px 0;">Delivery</td><td style="text-align:right;">{ship_text}</td></tr>
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
            <tr><td style="padding:4px 0;color:#666;">Subtotal</td><td style="text-align:right;">${order.get("subtotal",0):,.2f}</td></tr>
            {f'<tr><td style="padding:4px 0;color:#E31937;">Discount</td><td style="text-align:right;color:#E31937;">-${order.get("discount_amount", 0):,.2f}</td></tr>' if order.get("discount_amount") else ''}
            <tr><td style="padding:4px 0;color:#666;">Tax ({order.get("province","")})</td><td style="text-align:right;">${order.get("tax_amount",0):,.2f}</td></tr>
            <tr><td style="padding:4px 0;color:#666;">Shipping</td><td style="text-align:right;">{"Free" if order.get("shipping_method")=="pickup" else f"${order.get('shipping_cost',0):,.2f}"}</td></tr>
            <tr style="font-size:18px;font-weight:bold;color:#003B71;">
                <td style="padding:12px 0;border-top:2px solid #003B71;">Total</td>
                <td style="text-align:right;padding:12px 0;border-top:2px solid #003B71;">${order.get("total",0):,.2f} CAD</td>
            </tr>
        </table>

        <div style="margin-top:32px;padding-top:24px;border-top:1px solid #eee;font-size:13px;color:#999;text-align:center;">
            <p>Questions? Contact us at <a href="mailto:info@giantpro.com" style="color:#003B71;">info@giantpro.com</a> or call <a href="tel:902-456-6487" style="color:#003B71;">902-456-6487</a></p>
            <p style="margin-top:16px;">&copy; {datetime.now().year} EZ-UP Atlantic, a division of Giant Promotions Ltd.<br>3797 MacKintosh St, Halifax, NS B3K 5A6</p>
        </div>
    </div>
</div>
</body></html>'''

    return _send_email(order.get('customer_email'), f'Order Confirmation — {order.get("order_number","")}', html)


def send_store_notification(order):
    if not SMTP_USER:
        print("[EMAIL] SMTP not configured, skipping store notification")
        return False

    items_text = '\n'.join([
        f"  {i.get('qty',1)}x {i.get('name','')} {('('+i.get('variant','')+')') if i.get('variant') else ''} — ${i.get('price',0)*i.get('qty',1):,.2f}"
        for i in order.get('items', [])
    ])

    html = f'''<html><body style="font-family:Arial,sans-serif;">
    <h2 style="color:#003B71;">New Order Received!</h2>
    <table style="font-size:14px;color:#333;">
        <tr><td style="font-weight:bold;padding:4px 8px;">Order:</td><td>{order.get("order_number","")}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Customer:</td><td>{order.get("customer_name","")}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Email:</td><td>{order.get("customer_email","")}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Phone:</td><td>{order.get("customer_phone","")}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Delivery:</td><td>{order.get("shipping_method","pickup").title()}</td></tr>
        <tr><td style="font-weight:bold;padding:4px 8px;">Province:</td><td>{order.get("province","")}</td></tr>
        {f'<tr><td style="font-weight:bold;padding:4px 8px;color:#E31937;">Discount:</td><td style="color:#E31937;">-${order.get("discount_amount", 0):,.2f}</td></tr>' if order.get("discount_amount") else ''}
        <tr><td style="font-weight:bold;padding:4px 8px;">Total:</td><td style="font-size:18px;color:#003B71;font-weight:bold;">${order.get("total",0):,.2f} CAD</td></tr>
    </table>
    <h3>Items</h3>
    <pre style="background:#f5f5f7;padding:16px;border-radius:8px;font-size:13px;">{items_text}</pre>
    <p><a href="{DOMAIN}/admin.html" style="color:#003B71;">View in Admin Panel</a></p>
    </body></html>'''

    return _send_email(STORE_EMAIL, f'New Order {order.get("order_number","")} — ${order.get("total",0):,.2f}', html)


def _send_email(to, subject, html_body):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f'{STORE_NAME} <{SMTP_USER}>'
        msg['To'] = to
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to, msg.as_string())
        print(f"[EMAIL] Sent to {to}: {subject}")
        return True
    except Exception as e:
        print(f"[EMAIL] Failed to send to {to}: {e}")
        return False


# ===== QUOTE MANAGEMENT =====

def generate_quote_id():
    now = datetime.now()
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute('SELECT COUNT(*) FROM quotes WHERE created_at LIKE ?',
                         (now.strftime('%Y-%m-%d') + '%',)).fetchone()[0]
    conn.close()
    return f"QR-{now.strftime('%Y%m%d')}-{count + 1:04d}"


def save_quote(data):
    init_db()
    quote_id = generate_quote_id()
    now = datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''INSERT INTO quotes (quote_id, name, email, phone, product_interest, message, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (quote_id, data.get('name',''), data.get('email',''),
                  data.get('phone',''), data.get('product',''),
                  data.get('message',''), now))
    conn.commit()
    conn.close()
    return quote_id


def get_all_quotes(limit=50, offset=0):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute('SELECT * FROM quotes ORDER BY id DESC LIMIT ? OFFSET ?',
                        (limit, offset)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_quote_status(quote_id, status, notes=None):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    if notes:
        conn.execute('UPDATE quotes SET status=?, notes=? WHERE quote_id=?',
                     (status, notes, quote_id))
    else:
        conn.execute('UPDATE quotes SET status=? WHERE quote_id=?',
                     (status, quote_id))
    conn.commit()
    conn.close()


def get_quote_stats():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    stats = {
        'total_quotes': conn.execute('SELECT COUNT(*) FROM quotes').fetchone()[0],
        'new': conn.execute("SELECT COUNT(*) FROM quotes WHERE status='new'").fetchone()[0],
        'replied': conn.execute("SELECT COUNT(*) FROM quotes WHERE status='replied'").fetchone()[0],
        'closed': conn.execute("SELECT COUNT(*) FROM quotes WHERE status='closed'").fetchone()[0],
        'today_quotes': conn.execute("SELECT COUNT(*) FROM quotes WHERE date(created_at)=date('now')").fetchone()[0],
    }
    conn.close()
    return stats


def send_quote_notification(data, quote_id):
    """Email the store owner when a new quote request comes in"""
    if not SMTP_USER:
        print("[EMAIL] SMTP not configured, skipping quote notification")
        return False

    html = f'''<html><body style="font-family:Arial,sans-serif;">
    <h2 style="color:#003B71;">New Quote Request!</h2>
    <p style="color:#666;">A customer has submitted a quote request on the website.</p>
    <table style="font-size:14px;color:#333;border-collapse:collapse;">
        <tr><td style="font-weight:bold;padding:8px 12px;background:#f5f5f7;">Quote ID:</td><td style="padding:8px 12px;background:#f5f5f7;">{quote_id}</td></tr>
        <tr><td style="font-weight:bold;padding:8px 12px;">Name:</td><td style="padding:8px 12px;">{data.get('name','')}</td></tr>
        <tr><td style="font-weight:bold;padding:8px 12px;background:#f5f5f7;">Email:</td><td style="padding:8px 12px;background:#f5f5f7;"><a href="mailto:{data.get('email','')}">{data.get('email','')}</a></td></tr>
        <tr><td style="font-weight:bold;padding:8px 12px;">Phone:</td><td style="padding:8px 12px;">{data.get('phone','N/A')}</td></tr>
        <tr><td style="font-weight:bold;padding:8px 12px;background:#f5f5f7;">Product Interest:</td><td style="padding:8px 12px;background:#f5f5f7;">{data.get('product','N/A')}</td></tr>
    </table>
    <div style="margin-top:16px;padding:16px;background:#f5f5f7;border-radius:8px;border-left:4px solid #003B71;">
        <strong>Message:</strong><br>
        <p style="margin:8px 0 0;white-space:pre-wrap;">{data.get('message','')}</p>
    </div>
    <p style="margin-top:20px;"><a href="{DOMAIN}/admin.html" style="color:#003B71;font-weight:bold;">View in Admin Panel</a></p>
    </body></html>'''

    return _send_email(STORE_EMAIL, f'New Quote Request {quote_id} — {data.get("name","")}', html)


# Initialize DB on import
init_db()
