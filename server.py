"""
EZ-UP Atlantic -- Backend Server
Serves static files + Stripe checkout API + Order Management
"""
import os
from dotenv import load_dotenv
load_dotenv()

import json
import stripe
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from orders import (save_order, get_order, get_all_orders,
                    update_order_status, get_order_stats,
                    send_customer_confirmation, send_store_notification)

# ===== CONFIGURATION =====
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
DOMAIN = os.environ.get('DOMAIN', 'http://localhost:8080')

stripe.api_key = STRIPE_SECRET_KEY

# ===== CANADIAN TAX RATES (2026) =====
TAX_RATES = {
    'AB': {'gst': 5.0, 'pst': 0, 'hst': 0, 'total': 5.0, 'label': 'GST 5%'},
    'BC': {'gst': 5.0, 'pst': 7.0, 'hst': 0, 'total': 12.0, 'label': 'GST 5% + PST 7%'},
    'MB': {'gst': 5.0, 'pst': 7.0, 'hst': 0, 'total': 12.0, 'label': 'GST 5% + PST 7%'},
    'NB': {'gst': 0, 'pst': 0, 'hst': 15.0, 'total': 15.0, 'label': 'HST 15%'},
    'NL': {'gst': 0, 'pst': 0, 'hst': 15.0, 'total': 15.0, 'label': 'HST 15%'},
    'NS': {'gst': 0, 'pst': 0, 'hst': 14.0, 'total': 14.0, 'label': 'HST 14%'},
    'NT': {'gst': 5.0, 'pst': 0, 'hst': 0, 'total': 5.0, 'label': 'GST 5%'},
    'NU': {'gst': 5.0, 'pst': 0, 'hst': 0, 'total': 5.0, 'label': 'GST 5%'},
    'ON': {'gst': 0, 'pst': 0, 'hst': 13.0, 'total': 13.0, 'label': 'HST 13%'},
    'PE': {'gst': 0, 'pst': 0, 'hst': 15.0, 'total': 15.0, 'label': 'HST 15%'},
    'QC': {'gst': 5.0, 'pst': 9.975, 'hst': 0, 'total': 14.975, 'label': 'GST 5% + QST 9.975%'},
    'SK': {'gst': 5.0, 'pst': 6.0, 'hst': 0, 'total': 11.0, 'label': 'GST 5% + PST 6%'},
    'YT': {'gst': 5.0, 'pst': 0, 'hst': 0, 'total': 5.0, 'label': 'GST 5%'},
}

# Temp storage for pending checkouts (session_id -> cart data)
_pending_checkouts = {}

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)


# ===== STATIC FILE SERVING =====
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.isfile(path):
        return send_from_directory('.', path)
    return send_from_directory('.', 'index.html')


# ===== API: CONFIG =====
@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({'publishableKey': STRIPE_PUBLISHABLE_KEY})

@app.route('/api/tax-rates', methods=['GET'])
def api_tax_rates():
    return jsonify(TAX_RATES)


# ===== API: CHECKOUT =====
@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json
        items = data.get('items', [])
        customer_info = data.get('customer', {})
        province = data.get('province', 'NS').upper()
        shipping_method = data.get('shippingMethod', 'pickup')
        shipping_cost = float(data.get('shippingCost', 0))

        if not items:
            return jsonify({'error': 'Cart is empty'}), 400

        line_items = []
        for item in items:
            price_cents = int(round(float(item.get('price', 0)) * 100))
            if price_cents <= 0:
                continue
            name = item.get('name', 'Product')
            if item.get('variant'):
                name += f" ({item['variant']})"
            line_items.append({
                'price_data': {
                    'currency': 'cad',
                    'product_data': {
                        'name': name,
                        'images': [f"{DOMAIN}/{item['img']}"] if item.get('img') else [],
                    },
                    'unit_amount': price_cents,
                },
                'quantity': item.get('qty', 1),
            })

        if not line_items:
            return jsonify({'error': 'No valid priced items in cart'}), 400

        subtotal = sum(float(i.get('price', 0)) * i.get('qty', 1) for i in items if float(i.get('price', 0)) > 0)
        tax_info = TAX_RATES.get(province, TAX_RATES['NS'])
        tax_amount = round(subtotal * tax_info['total'] / 100, 2)

        if tax_amount > 0:
            line_items.append({
                'price_data': {'currency': 'cad', 'product_data': {'name': f"Tax ({tax_info['label']})"},
                               'unit_amount': int(round(tax_amount * 100))},
                'quantity': 1,
            })

        # Add shipping line item
        if shipping_cost > 0:
            line_items.append({
                'price_data': {'currency': 'cad', 'product_data': {'name': 'Shipping — Flat Rate'},
                               'unit_amount': int(round(shipping_cost * 100))},
                'quantity': 1,
            })

        session_params = {
            'payment_method_types': ['card'],
            'line_items': line_items,
            'mode': 'payment',
            'success_url': f"{DOMAIN}/confirmation.html?session_id={{CHECKOUT_SESSION_ID}}",
            'cancel_url': f"{DOMAIN}/checkout.html",
            'customer_email': customer_info.get('email'),
            'metadata': {
                'province': province,
                'shipping_method': shipping_method,
                'customer_name': customer_info.get('name', ''),
                'customer_phone': customer_info.get('phone', ''),
            },
        }

        if shipping_method == 'shipping':
            session_params['shipping_address_collection'] = {'allowed_countries': ['CA']}

        session = stripe.checkout.Session.create(**session_params)

        # Store cart data for order creation on payment success
        _pending_checkouts[session.id] = {
            'items': items,
            'customer': customer_info,
            'province': province,
            'shipping_method': shipping_method,
            'subtotal': subtotal,
            'tax_rate': tax_info['total'],
            'tax_amount': tax_amount,
            'shipping_cost': shipping_cost,
            'total': subtotal + tax_amount + shipping_cost,
        }

        return jsonify({'sessionId': session.id, 'url': session.url})

    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== API: STRIPE WEBHOOK =====
@app.route('/api/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig = request.headers.get('Stripe-Signature')

    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
        else:
            event = json.loads(payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if event.get('type') == 'checkout.session.completed':
        session_data = event['data']['object']
        _process_completed_payment(session_data)

    return jsonify({'received': True})


def _process_completed_payment(session_data):
    session_id = session_data.get('id', '')
    meta = session_data.get('metadata', {})
    cart = _pending_checkouts.pop(session_id, None)

    # Build order data
    order_data = {
        'stripe_session_id': session_id,
        'status': 'paid',
        'customer_name': meta.get('customer_name', ''),
        'customer_email': session_data.get('customer_details', {}).get('email', ''),
        'customer_phone': meta.get('customer_phone', ''),
        'province': meta.get('province', 'NS'),
        'shipping_method': meta.get('shipping_method', 'pickup'),
        'items': cart['items'] if cart else [],
        'subtotal': cart['subtotal'] if cart else (session_data.get('amount_total', 0) / 100),
        'tax_rate': cart['tax_rate'] if cart else 0,
        'tax_amount': cart['tax_amount'] if cart else 0,
        'total': cart['total'] if cart else (session_data.get('amount_total', 0) / 100),
    }

    # Get shipping address from Stripe if available
    shipping = session_data.get('shipping_details', {})
    if shipping and shipping.get('address'):
        addr = shipping['address']
        order_data['shipping_address'] = {
            'address': addr.get('line1', ''),
            'address2': addr.get('line2', ''),
            'city': addr.get('city', ''),
            'province': addr.get('state', ''),
            'postal': addr.get('postal_code', ''),
        }

    order_number = save_order(order_data)
    order_data['order_number'] = order_number
    print(f"[ORDER] Saved: {order_number} -- ${order_data['total']:,.2f}")

    # Send emails
    send_customer_confirmation(order_data)
    send_store_notification(order_data)


# ===== API: FALLBACK ORDER CREATION (for dev/testing without webhooks) =====
@app.route('/api/complete-order', methods=['POST'])
def complete_order():
    """Called by confirmation page if webhook hasn't fired yet"""
    data = request.json
    session_id = data.get('session_id', '')

    # Check if order already exists for this session
    from orders import init_db
    import sqlite3
    init_db()
    conn = sqlite3.connect(os.path.join('data', 'orders.db'))
    existing = conn.execute('SELECT order_number FROM orders WHERE stripe_session_id=?', (session_id,)).fetchone()
    conn.close()

    if existing:
        return jsonify({'order_number': existing[0], 'already_exists': True})

    # Try to get cart data from pending checkouts
    cart = _pending_checkouts.pop(session_id, None)
    if not cart:
        return jsonify({'error': 'Session data not found'}), 404

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        meta = session.metadata or {}
    except:
        meta = {}

    order_data = {
        'stripe_session_id': session_id,
        'status': 'paid',
        'customer_name': cart['customer'].get('name', meta.get('customer_name', '')),
        'customer_email': cart['customer'].get('email', ''),
        'customer_phone': cart['customer'].get('phone', ''),
        'province': cart['province'],
        'shipping_method': cart['shipping_method'],
        'items': cart['items'],
        'subtotal': cart['subtotal'],
        'tax_rate': cart['tax_rate'],
        'tax_amount': cart['tax_amount'],
        'total': cart['total'],
    }

    order_number = save_order(order_data)
    order_data['order_number'] = order_number
    send_customer_confirmation(order_data)
    send_store_notification(order_data)

    return jsonify({'order_number': order_number})


@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id, expand=['line_items'])

        # Try to create order if not yet created (fallback for no webhook)
        import sqlite3
        conn = sqlite3.connect(os.path.join('data', 'orders.db'))
        existing = conn.execute('SELECT order_number FROM orders WHERE stripe_session_id=?', (session_id,)).fetchone()
        conn.close()
        order_number = existing[0] if existing else None

        if not order_number and session.payment_status == 'paid':
            _process_completed_payment(session)
            conn = sqlite3.connect(os.path.join('data', 'orders.db'))
            existing = conn.execute('SELECT order_number FROM orders WHERE stripe_session_id=?', (session_id,)).fetchone()
            conn.close()
            order_number = existing[0] if existing else None

        return jsonify({
            'id': session.id,
            'status': session.payment_status,
            'orderNumber': order_number,
            'customerEmail': session.customer_details.email if session.customer_details else None,
            'amountTotal': session.amount_total / 100,
            'currency': session.currency.upper(),
            'lineItems': [{'name': item.description, 'quantity': item.quantity,
                           'amount': item.amount_total / 100}
                          for item in session.line_items.data] if session.line_items else [],
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ===== API: ADMIN =====
@app.route('/api/admin/orders', methods=['GET'])
def admin_orders():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    return jsonify(get_all_orders(limit, offset))

@app.route('/api/admin/orders/<order_number>', methods=['GET'])
def admin_order_detail(order_number):
    order = get_order(order_number)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order)

@app.route('/api/admin/orders/<order_number>/status', methods=['PUT'])
def admin_update_status(order_number):
    data = request.json
    update_order_status(order_number, data.get('status'), data.get('notes'))
    return jsonify({'ok': True})

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    return jsonify(get_order_stats())


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  EZ-UP Atlantic Server")
    print("  http://localhost:8080")
    print("=" * 50)
    print(f"  Stripe: {'OK' if 'REPLACE' not in STRIPE_SECRET_KEY else 'TEST MODE'}")
    smtp = os.environ.get('SMTP_USER', '')
    print(f"  Email:  {'OK - ' + smtp if smtp else 'NOT CONFIGURED'}")
    print("=" * 50 + "\n")
    app.run(host='0.0.0.0', port=8080, debug=True)

