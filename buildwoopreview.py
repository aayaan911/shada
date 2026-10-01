#!/usr/bin/env python3
# Shada · WooCommerce preview builder
# Renders REAL WooCommerce + Astra markup against shada-woo.css so the design
# can be seen and verified before a single line is pasted into WordPress.
# The markup below is copied from WooCommerce's own templates, not invented.
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = open(sys.argv[1], encoding='utf-8').read()          # 01-base.css
WOO  = open(os.path.join(HERE, 'shada-woo.css'), encoding='utf-8').read()
OUT  = '/tmp/pg/out'

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">')

HDR = '''<header class="pv-hdr"><div class="pv-in">
  <span class="pv-logo">SHADA</span>
  <nav><a href="#">Products</a><a href="#">Birds</a><a href="#">Wholesale</a><a href="#">About</a></nav>
  <span class="pv-wa">Order on WhatsApp</span>
</div></header>'''
FTR = '<footer class="pv-ftr"><div class="pv-in">© 2026 Shada Bird Feed. Prices in BDT, factory retail.</div></footer>'

PV = '''
/* preview chrome only — NOT part of the deliverable CSS */
.pv-hdr{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50}
.pv-in{max-width:1180px;margin:0 auto;padding:0 24px;height:64px;display:flex;align-items:center;gap:26px}
.pv-logo{font-weight:700;letter-spacing:.04em;font-size:17px}
.pv-hdr nav{display:flex;gap:20px;font-size:14.5px;color:var(--tx2)}
.pv-wa{margin-left:auto;background:var(--brand);color:#fff;border-radius:var(--r);
  padding:9px 16px;font-size:14px;font-weight:600}
.pv-ftr{background:var(--ink);color:var(--on2);font-size:13.5px}
.pv-ftr .pv-in{height:auto;padding-block:22px}
.pv-note{max-width:1180px;margin:0 auto;padding:14px 24px 0;font-size:12.5px;color:var(--tx3)}
@media(max-width:820px){.pv-hdr nav{display:none}}
'''


def page(title, body_class, main):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Shada preview</title>{FONT}
<style>{BASE}</style>
<style>{WOO}</style>
<style>{PV}</style>
</head><body class="{body_class} ast-plain-container ast-no-sidebar theme-astra">
{HDR}
<div class="pv-note">PREVIEW · real WooCommerce markup · shada-woo.css</div>
<div class="site-content"><div class="ast-container">
{main}
</div></div>
{FTR}
</body></html>'''


# ─────────────────────────────────────────────────────────── CART
CART = '''
<header class="entry-header"><h1 class="entry-title">Cart</h1></header>
<div class="woocommerce">
<div class="woocommerce-notices-wrapper"></div>
<form class="woocommerce-cart-form" action="#" method="post">
<table class="shop_table shop_table_responsive cart woocommerce-cart-form__contents">
  <thead><tr>
    <th class="product-remove">&nbsp;</th><th class="product-thumbnail">&nbsp;</th>
    <th class="product-name">Product</th><th class="product-price">Price</th>
    <th class="product-quantity">Quantity</th><th class="product-subtotal">Subtotal</th>
  </tr></thead>
  <tbody>
    <tr class="woocommerce-cart-form__cart-item cart_item">
      <td class="product-remove"><a href="#" class="remove" aria-label="Remove Nutricare from cart">&times;</a></td>
      <td class="product-thumbnail"><img src="data:image/svg+xml;utf8,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 80 80%22%3E%3Crect width=%2280%22 height=%2280%22 fill=%22%23E6F4EA%22/%3E%3Crect x=%2222%22 y=%2216%22 width=%2236%22 height=%2250%22 rx=%226%22 fill=%22%23089830%22/%3E%3C/svg%3E" alt=""></td>
      <td class="product-name" data-title="Product"><a href="#">Nutricare Hand Feeding Formula</a>
        <dl class="variation"><dt>Pack size:</dt><dd>500g</dd></dl></td>
      <td class="product-price" data-title="Price"><span class="woocommerce-Price-amount amount">৳485</span></td>
      <td class="product-quantity" data-title="Quantity">
        <div class="quantity"><input type="number" class="input-text qty text" value="2" min="0"></div></td>
      <td class="product-subtotal" data-title="Subtotal"><span class="woocommerce-Price-amount amount">৳970</span></td>
    </tr>
    <tr class="woocommerce-cart-form__cart-item cart_item">
      <td class="product-remove"><a href="#" class="remove" aria-label="Remove Eggfood from cart">&times;</a></td>
      <td class="product-thumbnail"><img src="data:image/svg+xml;utf8,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 80 80%22%3E%3Crect width=%2280%22 height=%2280%22 fill=%22%23FFF6D9%22/%3E%3Crect x=%2222%22 y=%2216%22 width=%2236%22 height=%2250%22 rx=%226%22 fill=%22%23E0B810%22/%3E%3C/svg%3E" alt=""></td>
      <td class="product-name" data-title="Product"><a href="#">Avian Eggfood</a>
        <dl class="variation"><dt>Pack size:</dt><dd>1kg</dd></dl></td>
      <td class="product-price" data-title="Price"><span class="woocommerce-Price-amount amount">৳870</span></td>
      <td class="product-quantity" data-title="Quantity">
        <div class="quantity"><input type="number" class="input-text qty text" value="1" min="0"></div></td>
      <td class="product-subtotal" data-title="Subtotal"><span class="woocommerce-Price-amount amount">৳870</span></td>
    </tr>
    <tr><td colspan="6" class="actions">
      <div class="coupon"><label for="coupon_code">Coupon:</label>
        <input type="text" name="coupon_code" class="input-text" id="coupon_code" placeholder="Coupon code">
        <button type="submit" class="button">Apply coupon</button></div>
      <button type="submit" class="button" name="update_cart">Update cart</button>
    </td></tr>
  </tbody>
</table>
</form>
<div class="cart-collaterals"><div class="cart_totals">
  <h2>Cart totals</h2>
  <table class="shop_table shop_table_responsive"><tbody>
    <tr class="cart-subtotal"><th>Subtotal</th><td><span class="woocommerce-Price-amount amount">৳1,840</span></td></tr>
    <tr class="woocommerce-shipping-totals shipping"><th>Delivery</th>
      <td><span class="woocommerce-Price-amount amount">৳120</span>
      <p class="woocommerce-shipping-destination">Sundarban Courier, 2 working days</p></td></tr>
    <tr class="order-total"><th>Total</th><td><strong><span class="woocommerce-Price-amount amount">৳1,960</span></strong></td></tr>
  </tbody></table>
  <div class="wc-proceed-to-checkout"><a href="#" class="checkout-button button alt wc-forward">Proceed to checkout</a></div>
  <p class="shada-trust">Sealed jars, batch date on the lid. Delivered to all 64 districts.
  Questions before you order? WhatsApp 01813-323535.</p>
</div></div>
</div>'''

# ─────────────────────────────────────────────────────── CHECKOUT
DISTRICTS = ['Dhaka','Chattogram','Rajshahi','Khulna','Barishal','Sylhet','Rangpur','Mymensingh','Bandarban']
CHECKOUT = '''
<header class="entry-header"><h1 class="entry-title">Checkout</h1></header>
<div class="woocommerce">
<div class="woocommerce-notices-wrapper"></div>
<form name="checkout" class="checkout woocommerce-checkout" action="#" method="post">
  <div class="col2-set" id="customer_details">
    <div class="col-1"><div class="woocommerce-billing-fields">
      <h3>Billing details</h3>
      <div class="woocommerce-billing-fields__field-wrapper">
        <p class="form-row form-row-first validate-required" id="billing_first_name_field">
          <label for="billing_first_name">First name&nbsp;<abbr class="required">*</abbr></label>
          <input type="text" class="input-text" id="billing_first_name" placeholder="Write your name"></p>
        <p class="form-row form-row-last validate-required" id="billing_last_name_field">
          <label for="billing_last_name">Last name&nbsp;<abbr class="required">*</abbr></label>
          <input type="text" class="input-text" id="billing_last_name"></p>
        <p class="form-row form-row-wide validate-required validate-phone" id="billing_phone_field">
          <label for="billing_phone">Phone or WhatsApp&nbsp;<abbr class="required">*</abbr></label>
          <input type="tel" class="input-text" id="billing_phone" placeholder="01XXXXXXXXX"></p>
        <p class="form-row form-row-wide validate-required" id="billing_state_field">
          <label for="billing_state">District&nbsp;<abbr class="required">*</abbr></label>
          <select class="state_select" id="billing_state">__DISTRICTS__</select></p>
        <p class="form-row form-row-wide validate-required" id="billing_address_1_field">
          <label for="billing_address_1">Street address&nbsp;<abbr class="required">*</abbr></label>
          <input type="text" class="input-text" id="billing_address_1" placeholder="House, road, area"></p>
      </div></div></div>
    <div class="col-2"><div class="woocommerce-additional-fields">
      <h3>Additional information</h3>
      <p class="form-row notes" id="order_comments_field">
        <label for="order_comments">Order notes&nbsp;<span class="optional">(optional)</span></label>
        <textarea class="input-text" id="order_comments" placeholder="A landmark for the courier, or anything we should know."></textarea></p>
    </div></div>
  </div>

  <h3 id="order_review_heading">Your order</h3>
  <div id="order_review" class="woocommerce-checkout-review-order">
    <table class="shop_table woocommerce-checkout-review-order-table">
      <thead><tr><th class="product-name">Product</th><th class="product-total">Total</th></tr></thead>
      <tbody>
        <tr class="cart_item"><td class="product-name">Nutricare Hand Feeding Formula &ndash; 500g
          <strong class="product-quantity">&times;&nbsp;2</strong></td>
          <td class="product-total"><span class="woocommerce-Price-amount amount">৳970</span></td></tr>
        <tr class="cart_item"><td class="product-name">Avian Eggfood &ndash; 1kg
          <strong class="product-quantity">&times;&nbsp;1</strong></td>
          <td class="product-total"><span class="woocommerce-Price-amount amount">৳870</span></td></tr>
      </tbody>
      <tfoot>
        <tr class="cart-subtotal"><th>Subtotal</th><td><span class="woocommerce-Price-amount amount">৳1,840</span></td></tr>
        <tr class="woocommerce-shipping-totals shipping"><th>Delivery</th><td><span class="woocommerce-Price-amount amount">৳120</span></td></tr>
        <tr class="order-total"><th>Total</th><td><strong><span class="woocommerce-Price-amount amount">৳1,960</span></strong></td></tr>
      </tfoot>
    </table>
    <div id="payment" class="woocommerce-checkout-payment">
      <ul class="wc_payment_methods payment_methods methods">
        <li class="wc_payment_method payment_method_cod">
          <input id="payment_method_cod" type="radio" class="input-radio" name="payment_method" checked>
          <label for="payment_method_cod">Cash on delivery</label>
          <div class="payment_box payment_method_cod"><p>Pay the courier in cash when your parcel arrives.</p></div></li>
        <li class="wc_payment_method payment_method_bkash">
          <input id="payment_method_bkash" type="radio" class="input-radio" name="payment_method">
          <label for="payment_method_bkash">bKash</label></li>
      </ul>
      <div class="woocommerce-terms-and-conditions-wrapper">
        <p class="form-row validate-required woocommerce-form__label-for-checkbox">
          <input type="checkbox" class="woocommerce-form__input-checkbox" id="terms">
          <label for="terms" class="woocommerce-form__label-for-checkbox">I have read and agree to the
          <a href="/terms-and-conditions/">terms and conditions</a>&nbsp;<abbr class="required">*</abbr></label></p>
      </div>
      <div class="form-row place-order">
        <button type="submit" class="button alt" id="place_order">Place order</button></div>
    </div>
  </div>
</form>
</div>'''.replace('__DISTRICTS__',
    '<option value="">Select your district</option>' + ''.join(f'<option>{d}</option>' for d in DISTRICTS))

# ────────────────────────────────────────────── ORDER RECEIVED
RECEIVED = '''
<header class="entry-header"><h1 class="entry-title">Order received</h1></header>
<div class="woocommerce"><div class="woocommerce-order">
  <p class="woocommerce-notice woocommerce-notice--success woocommerce-thankyou-order-received">Order received.</p>
  <ul class="woocommerce-order-overview woocommerce-thankyou-order-details order_details">
    <li class="woocommerce-order-overview__order order">Order number<strong>#10428</strong></li>
    <li class="woocommerce-order-overview__date date">Date<strong>20 Sep 2026</strong></li>
    <li class="woocommerce-order-overview__total total">Total<strong>৳1,960</strong></li>
    <li class="woocommerce-order-overview__payment-method method">Payment<strong>Cash on delivery</strong></li>
  </ul>
  <section class="woocommerce-order-details">
    <h2 class="woocommerce-order-details__title">Order details</h2>
    <table class="woocommerce-table woocommerce-table--order-details shop_table order_details">
      <thead><tr><th class="woocommerce-table__product-name product-name">Product</th>
        <th class="woocommerce-table__product-table product-total">Total</th></tr></thead>
      <tbody>
        <tr class="woocommerce-table__line-item order_item">
          <td class="product-name">Nutricare Hand Feeding Formula &ndash; 500g
            <strong class="product-quantity">&times;&nbsp;2</strong></td>
          <td class="product-total">৳970</td></tr>
        <tr class="woocommerce-table__line-item order_item">
          <td class="product-name">Avian Eggfood &ndash; 1kg
            <strong class="product-quantity">&times;&nbsp;1</strong></td>
          <td class="product-total">৳870</td></tr>
      </tbody>
      <tfoot>
        <tr><th>Subtotal:</th><td>৳1,840</td></tr>
        <tr><th>Delivery:</th><td>৳120 via Sundarban Courier</td></tr>
        <tr><th>Total:</th><td>৳1,960</td></tr>
      </tfoot>
    </table>
  </section>
  <section class="woocommerce-customer-details">
    <section class="woocommerce-columns woocommerce-columns--2 woocommerce-columns--addresses col2-set addresses">
      <div class="woocommerce-column woocommerce-column--1 woocommerce-column--billing-address col-1">
        <h2 class="woocommerce-column__title">Billing address</h2>
        <address>Ayaan Ahmed<br>House 12, Road 4, Mirpur 11<br>Dhaka<br>01813-323535</address></div>
      <div class="woocommerce-column woocommerce-column--2 woocommerce-column--shipping-address col-2">
        <h2 class="woocommerce-column__title">Delivery address</h2>
        <address>Same as billing</address></div>
    </section>
  </section>
</div></div>'''

# ──────────────────────────────────────── MY ACCOUNT · ORDERS
NAV = '''<nav class="woocommerce-MyAccount-navigation"><ul>
  <li class="woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--dashboard"><a href="#">Dashboard</a></li>
  <li class="woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--orders is-active"><a href="#">Orders</a></li>
  <li class="woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--downloads"><a href="#">Price list</a></li>
  <li class="woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--edit-address"><a href="#">Addresses</a></li>
  <li class="woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--edit-account"><a href="#">Account details</a></li>
  <li class="woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--customer-logout"><a href="#">Log out</a></li>
</ul></nav>'''

ORDERS = '''
<header class="entry-header"><h1 class="entry-title">Orders</h1></header>
<div class="woocommerce">
''' + NAV + '''
<div class="woocommerce-MyAccount-content">
  <div class="shada-rolebar">
    <b>Dhaka Bird House</b><span class="tier">Wholesale tier</span>
    <span class="sp">Dealer for Dhaka &middot; rates confirmed 12 Sep 2026</span>
  </div>
  <div class="shada-kpis">
    <div class="shada-kpi"><span class="k">Ordered this month</span><span class="v">৳48,200</span>
      <span class="d up">+18% vs August</span><span class="l">View all orders</span></div>
    <div class="shada-kpi due"><span class="k">Outstanding due</span><span class="v">৳6,400</span>
      <span class="d">Oldest 14 days</span><span class="l">Pay now</span></div>
    <div class="shada-kpi"><span class="k">Orders</span><span class="v">7</span>
      <span class="d up">+2</span><span class="l">Re-order last</span></div>
    <div class="shada-kpi"><span class="k">Saved vs retail</span><span class="v">৳13,100</span>
      <span class="d up">27% average</span><span class="l">See the price list</span></div>
  </div>
  <div class="shada-chips">
    <button type="button" aria-pressed="true">All</button>
    <button type="button">This month</button><button type="button">Last 3 months</button>
    <button type="button">Unpaid</button><button type="button">Completed</button>
  </div>
  <table class="woocommerce-orders-table woocommerce-MyAccount-orders shop_table shop_table_responsive my_account_orders">
    <thead><tr>
      <th class="woocommerce-orders-table__header woocommerce-orders-table__header-order-number"><span class="nobr">Order</span></th>
      <th class="woocommerce-orders-table__header woocommerce-orders-table__header-order-date"><span class="nobr">Date</span></th>
      <th class="woocommerce-orders-table__header woocommerce-orders-table__header-order-status"><span class="nobr">Status</span></th>
      <th class="woocommerce-orders-table__header woocommerce-orders-table__header-order-total"><span class="nobr">Total</span></th>
      <th class="woocommerce-orders-table__header woocommerce-orders-table__header-order-actions"><span class="nobr">Actions</span></th>
    </tr></thead>
    <tbody>__ROWS__</tbody>
  </table>
</div></div>'''

ROWS = [
    ('10428', '20 Sep 2026', 'Processing', 'processing', '৳1,960', '3'),
    ('10391', '11 Sep 2026', 'Completed',  'completed',  '৳12,480', '9'),
    ('10344', '02 Sep 2026', 'Completed',  'completed',  '৳18,900', '14'),
    ('10287', '21 Aug 2026', 'Cancelled',  'cancelled',  '৳3,100', '2'),
]
ORDERS = ORDERS.replace('__ROWS__', ''.join(
    f'''<tr class="woocommerce-orders-table__row woocommerce-orders-table__row--status-{st} order order-status-{st}">
  <td class="woocommerce-orders-table__cell woocommerce-orders-table__cell-order-number" data-title="Order"><a href="#">#{no}</a></td>
  <td class="woocommerce-orders-table__cell woocommerce-orders-table__cell-order-date" data-title="Date"><time>{dt}</time></td>
  <td class="woocommerce-orders-table__cell woocommerce-orders-table__cell-order-status" data-title="Status">{lbl}</td>
  <td class="woocommerce-orders-table__cell woocommerce-orders-table__cell-order-total" data-title="Total">{tot} for {n} items</td>
  <td class="woocommerce-orders-table__cell woocommerce-orders-table__cell-order-actions" data-title="Actions">
    <a href="#" class="woocommerce-button button view">View</a>
    <a href="#" class="woocommerce-button button order-again">Re-order</a></td>
</tr>''' for no, dt, lbl, st, tot, n in ROWS))

# ──────────────────────────────────────── MY ACCOUNT · LOGIN
LOGIN = '''
<header class="entry-header"><h1 class="entry-title">My account</h1></header>
<div class="woocommerce">
<div class="woocommerce-notices-wrapper"></div>
<form class="woocommerce-form woocommerce-form-login login" method="post">
  <p class="form-row form-row-wide">
    <label for="username">Phone number or email&nbsp;<span class="required">*</span></label>
    <input type="text" class="woocommerce-Input woocommerce-Input--text input-text" id="username" placeholder="01XXXXXXXXX"></p>
  <p class="form-row form-row-wide">
    <label for="password">Password&nbsp;<span class="required">*</span></label>
    <input class="woocommerce-Input woocommerce-Input--text input-text" type="password" id="password"></p>
  <p class="form-row">
    <label class="woocommerce-form__label woocommerce-form__label-for-checkbox woocommerce-form-login__rememberme">
      <input class="woocommerce-form__input woocommerce-form__input-checkbox" type="checkbox">
      <span>Remember me</span></label></p>
  <p class="form-row">
    <button type="submit" class="woocommerce-button button woocommerce-form-login__submit">Log in</button></p>
  <p class="woocommerce-LostPassword lost_password"><a href="#">Lost your password?</a></p>
</form>
</div>'''


PAGES = [
    ('preview-cart',            'Cart',           'woocommerce-cart woocommerce-page logged-in',            CART),
    ('preview-checkout',        'Checkout',       'woocommerce-checkout woocommerce-page logged-in',        CHECKOUT),
    ('preview-order-received',  'Order received', 'woocommerce-order-received woocommerce-page logged-in',  RECEIVED),
    ('preview-my-account',      'Orders',         'woocommerce-account woocommerce-page logged-in shada-dealer', ORDERS),
    ('preview-account-login',   'My account',     'woocommerce-account woocommerce-page',                   LOGIN),
]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for slug, title, cls, main in PAGES:
        html = page(title, cls, main)
        open(f'{OUT}/{slug}.html', 'w', encoding='utf-8').write(html)
        print(f'{slug+".html":28} {round(len(html)/1024):3} KB')
    print(f'\nshada-woo.css  {round(len(WOO)/1024)} KB, '
          f'{len(re.findall(chr(123), WOO))} rules')
