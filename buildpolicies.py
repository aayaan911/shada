#!/usr/bin/env python3
# Shada Bird Feed · policy pages generator
#   /privacy-policy/ · /terms-and-conditions/ · /refund_returns/ · /shipping-policy/
#
# Written against the law as it actually stands in September 2026:
#   · Personal Data Protection Act, 2026 (Law 63 of 2026) — passed April 2026,
#     repealing the Personal Data Protection Ordinance, 2025
#   · Digital Commerce Operation Guidelines 2021 (Ministry of Commerce, 4 July 2021),
#     still in force: dispatch, delivery windows, refund to the original method
#   · Consumer Rights Protection Act, 2009, enforced by DNCRP
#
# NOT LEGAL ADVICE. Every [CONFIRM] marker is a business decision Shada must make,
# and a Bangladeshi lawyer should read the final text before it is published.
import re, os, sys

HEAD = open('/tmp/pg/head.txt', encoding='utf-8').read()
FOOT = open('/tmp/pg/foot.txt', encoding='utf-8').read()

UPDATED = '19 September 2026'
WA   = '8801813323535'
PH   = '01813-323535'
MAIL = 'shadabirdfeed@gmail.com'
ADDR = 'Majorvita, Bhaluka, Mymensingh, Bangladesh'

def C(t):
    """A decision Shada must make. Rendered so it cannot be missed."""
    return f'<mark class="tbc">[CONFIRM: {t}]</mark>'

CSS = '''
/* ═══════════════════════════════════════════════════════════════════
   POLICY PAGES  ·  privacy · terms · refunds · shipping
   Loads after 01-base.css. One stylesheet, four pages.
   Prose is capped at 74ch because legal text is read, not scanned.
   ═══════════════════════════════════════════════════════════════════ */
.polhero{background:var(--ink);color:#fff;position:relative;overflow:hidden;
  padding:clamp(34px,4.4vw,58px) 0 clamp(30px,3.6vw,46px)}
.polhero::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;
  opacity:.07;pointer-events:none}
.polhero .wrap{position:relative}
.polhero h1{font-size:clamp(28px,4vw,46px);letter-spacing:-.033em;line-height:1.07;margin:10px 0 12px}
.polhero .meta{display:flex;gap:9px;flex-wrap:wrap;align-items:center;font-size:13.5px;color:var(--on2)}
.polhero .meta b{color:#fff;font-weight:600}
.polhero .meta i{width:3px;height:3px;border-radius:50%;background:rgba(255,255,255,.4);font-style:normal}

.polwrap{max-width:820px}
.poljump{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:clamp(28px,3.4vw,44px);
  padding-bottom:clamp(20px,2.4vw,30px);border-bottom:1px solid var(--line)}
.poljump a{display:inline-flex;align-items:center;min-height:36px;padding:7px 13px;border-radius:999px;
  border:1px solid var(--line);background:#fff;font-size:13.5px;font-weight:500;color:var(--tx2);
  text-decoration:none;transition:border-color .15s,color .15s,background .15s}
.poljump a:hover{color:var(--brand);border-color:var(--brand);background:var(--paper2)}

.pol h2{font-size:clamp(20px,2.1vw,25px);letter-spacing:-.022em;line-height:1.3;
  margin:clamp(34px,3.6vw,50px) 0 12px;scroll-margin-top:90px}
.pol h2:first-child{margin-top:0}
.pol h2 span{color:var(--tx3);font-weight:600;margin-right:9px}
.pol h3{font-size:16.5px;font-weight:600;letter-spacing:-.012em;margin:24px 0 8px}
.pol p{font-size:16px;line-height:1.72;color:var(--tx2);margin-bottom:14px;max-width:74ch}
.pol ul,.pol ol{margin:0 0 16px;padding-left:0;list-style:none;max-width:74ch}
.pol li{position:relative;padding-left:22px;font-size:16px;line-height:1.7;color:var(--tx2);margin-bottom:9px}
.pol ul li::before{content:"";position:absolute;left:3px;top:11px;width:6px;height:6px;
  border-radius:50%;background:var(--brand)}
.pol ol{counter-reset:pol}
.pol ol li{counter-increment:pol;padding-left:26px}
.pol ol li::before{content:counter(pol) ".";position:absolute;left:0;top:0;
  color:var(--brand);font-weight:600;font-size:15px}
.pol a{color:var(--brand);text-decoration:none;border-bottom:1px solid rgba(8,152,48,.3)}
.pol a:hover{border-color:var(--brand)}
.pol strong{color:var(--tx);font-weight:600}

/* A fact the visitor must not miss */
.polbox{background:var(--paper2);border:1px solid var(--line);border-left:3px solid var(--brand);
  border-radius:var(--r2);padding:20px 24px;margin:22px 0;max-width:74ch}
.polbox p:last-child{margin-bottom:0}
.polbox b{color:var(--tx)}

/* Unresolved business decision. Must be zero of these before publishing. */
mark.tbc{background:#FFE9A8;color:#6B4E00;border-radius:4px;padding:1px 6px;
  font-weight:600;font-size:14.5px;box-decoration-break:clone;-webkit-box-decoration-break:clone}

.polend{margin-top:clamp(40px,4.6vw,64px);padding-top:26px;border-top:1px solid var(--line)}
.polend h3{font-size:17px;margin:0 0 8px}
.polend p{margin-bottom:16px}
.polend .acts{display:flex;gap:10px;flex-wrap:wrap}
@media(max-width:560px){.polend .acts .btn{width:100%}}
'''

CONTACT_BLOCK = f'''<p>Write to <a href="mailto:{MAIL}">{MAIL}</a>, message
<a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp {PH}</a>, or post to
Shada Bird Feed, {ADDR}.</p>'''


# ═══════════════════════════════════════════════════════════════════════
#  PRIVACY POLICY
# ═══════════════════════════════════════════════════════════════════════
PRIVACY = [
 ('What this covers', f'''
<p>This policy explains what personal data Shada Bird Feed collects when you use
<strong>shadabirdfeed.com</strong>, order from us, or contact us, why we collect it, and what you
can ask us to do with it.</p>
<p>It is written to meet the <strong>Personal Data Protection Act, 2026</strong> of Bangladesh. Under that
Act we are the <strong>data controller</strong> for the information described here.</p>
<div class="polbox"><p><b>Who we are.</b> {C('the registered legal name and trade licence number')},
trading as Shada Bird Feed, {ADDR}. {C('BIN or VAT registration number, if registered')}</p></div>'''),

 ('What we collect', '''
<h3>When you place an order</h3>
<ul>
  <li>Your name, delivery address, district, phone number and email address</li>
  <li>What you ordered, the amount paid, and the date</li>
  <li>The payment method used. We never see or store your full card number, PIN or
      mobile wallet password. Those stay with the payment provider.</li>
</ul>
<h3>When you contact us or apply for a dealer account</h3>
<ul>
  <li>Your name, shop name where relevant, district, phone or WhatsApp number, and your message</li>
</ul>
<h3>When you simply browse the site</h3>
<ul>
  <li>Your IP address, browser and device type, the pages you viewed and how you arrived</li>
</ul>'''),

 ('Why we collect it, and our lawful basis', '''
<p>The Personal Data Protection Act, 2026 requires us to have a lawful basis for every use.
Ours are:</p>
<ul>
  <li><strong>To perform our contract with you</strong> — taking payment, packing your order,
      handing it to the courier, and handling a return.</li>
  <li><strong>Your consent</strong> — replying to a contact form or a dealer application, and
      any marketing message. You can withdraw consent at any time.</li>
  <li><strong>Our legitimate interest</strong> — keeping the site secure, preventing fraud, and
      understanding which pages people use, in a way that does not override your rights.</li>
  <li><strong>Legal obligation</strong> — keeping the sales and tax records the law requires.</li>
</ul>
<div class="polbox"><p><b>We do not sell your personal data to anyone. Ever.</b></p></div>'''),

 ('Who we share it with', f'''
<p>Only the people who need it to get your order to you:</p>
<ul>
  <li><strong>Our courier</strong>, Sundarban Courier Service, which receives your name, address and
      phone number so it can deliver the parcel</li>
  <li><strong>Our payment provider</strong>, which processes the payment. {C('name every payment gateway and wallet used, for example bKash, Nagad, SSLCommerz')}</li>
  <li><strong>Our hosting and website tools</strong>, which store the site and its data</li>
  <li><strong>A dealer</strong>, only if you specifically ask us to connect you with your local shop</li>
  <li><strong>A government authority</strong>, where the law requires us to</li>
</ul>
<p>{C('whether any of these providers store data outside Bangladesh. The Act regulates cross-border transfer, so this must be answered before publishing.')}</p>'''),

 ('How long we keep it', f'''
<ul>
  <li><strong>Order and payment records</strong> — {C('retention period. Tax law normally drives this; confirm with your accountant')}</li>
  <li><strong>Contact and dealer enquiries</strong> — {C('for example 24 months from your last message')}</li>
  <li><strong>Website analytics</strong> — {C('the retention setting configured in your analytics tool')}</li>
</ul>
<p>When a period ends we delete the data or anonymise it so it can no longer identify you.</p>'''),

 ('Your rights', f'''
<p>Under the Personal Data Protection Act, 2026 you can ask us to:</p>
<ul>
  <li>Tell you what personal data we hold about you, and give you a copy</li>
  <li>Correct anything that is wrong or out of date</li>
  <li>Delete your data, where we are not required to keep it</li>
  <li>Stop using it for a particular purpose, or withdraw a consent you gave</li>
  <li>Stop sending you marketing messages</li>
</ul>
<p>Ask by email or WhatsApp using the details at the end of this page. We reply within
{C('response window, for example 30 days')}. There is no charge.</p>
<p>If you are not satisfied with our answer, you may complain to the supervisory authority
established under the Act.</p>'''),

 ('Cookies and measurement', f'''
<p>The site uses cookies to keep your shopping cart working, remember your preferences, and
measure how the site is used.</p>
<p>{C('list every analytics and advertising tool actually installed, and whether a cookie consent banner is required. Google Analytics and the Meta pixel both set cookies and both need naming here.')}</p>
<p>You can block or delete cookies in your browser settings. If you block the essential ones,
the cart and checkout will stop working.</p>'''),

 ('Keeping it safe', '''
<p>The site runs over an encrypted HTTPS connection. Access to order data is limited to the
people who need it to do their job. No system is perfectly secure, but we take reasonable
technical and organisational measures to protect your data.</p>
<p>If a breach occurs that is likely to affect your rights, we will notify the supervisory
authority and, where required, you, in line with the Personal Data Protection Act, 2026.</p>'''),

 ('Children', '''
<p>This site is intended for adults. We do not knowingly collect personal data from children.
If you believe a child has given us their data, contact us and we will delete it.</p>'''),

 ('Changes to this policy', f'''
<p>If we change this policy we will update the date at the top of the page. This version is
dated <strong>{UPDATED}</strong>.</p>'''),

 ('Contact us', CONTACT_BLOCK),
]


# ═══════════════════════════════════════════════════════════════════════
#  TERMS AND CONDITIONS
# ═══════════════════════════════════════════════════════════════════════
TERMS = [
 ('Who you are dealing with', f'''
<p>This website is operated by {C('registered legal name and trade licence number')}, trading as
Shada Bird Feed, {ADDR}.</p>
<p>By using this site or placing an order you accept these terms. If you do not accept them,
please do not order.</p>'''),

 ('Products', '''
<p>We make bird feed and supplements. Every jar is sealed at our factory in Bhaluka and carries
its batch date on the lid. We do not repack other companies' product.</p>
<div class="polbox"><p><b>Our feeding guidance is not veterinary advice.</b> The instructions on our
packs and on this website are general guidance based on our own experience and published
research. Birds differ. If your bird is ill, injured, or not gaining weight, consult a
qualified avian veterinarian. We are not responsible for outcomes arising from use of our
products in place of veterinary care.</p></div>'''),

 ('Prices', f'''
<ul>
  <li>All prices are in Bangladeshi Taka (BDT).</li>
  <li>We publish one retail price and hold it in all 64 districts. A dealer may not advertise
      below it.</li>
  <li>{C('whether prices include or exclude VAT, and whether delivery is charged separately')}</li>
  <li>We may change prices at any time. The price that applies to your order is the price shown
      when you placed it.</li>
  <li>If a price is displayed in obvious error we will contact you before dispatch and you may
      cancel for a full refund.</li>
</ul>'''),

 ('Orders and acceptance', '''
<p>Placing an order is an offer to buy. A contract forms when we confirm your order and
hand it to the courier, not when you click the button.</p>
<p>We may decline an order if the product is out of stock, the delivery address is outside our
courier network, or we cannot verify the payment. If we decline after you have paid, we refund
in full.</p>'''),

 ('Payment', f'''
<p>{C('every payment method accepted, for example bKash, Nagad, card, bank transfer, cash on delivery. This clause cannot be published until that list is exact.')}</p>
<p>Your order is dispatched once payment clears{C(', or on delivery if cash on delivery is offered')}.</p>'''),

 ('Delivery', '''
<p>Delivery terms, timings and charges are set out in our
<a href="/shipping-policy/">Shipping policy</a>, which forms part of these terms.</p>'''),

 ('Returns and refunds', '''
<p>Your right to return an item and how refunds are paid are set out in our
<a href="/refund_returns/">Refund and returns policy</a>, which forms part of these terms.</p>'''),

 ('Using this website', '''
<p>The text, photographs, illustrations, logo and design on this site belong to Shada Bird Feed.
You may not copy, republish or use them commercially without our written permission.</p>
<p>You may not attempt to break into the site, disrupt it, or scrape it at a rate that affects
other visitors.</p>'''),

 ('Our responsibility to you', '''
<p>We are responsible for supplying products that match their description and are fit to feed
to birds as directed. Nothing in these terms limits your rights under the
<strong>Consumer Rights Protection Act, 2009</strong>, or any other right the law does not allow us
to exclude.</p>
<p>Beyond that, we are not liable for indirect or consequential loss, and our total liability
for any order is limited to the amount you paid for it.</p>'''),

 ('If something goes wrong', '''
<p>Tell us first. Most problems are solved with one WhatsApp message.</p>
<p>If we cannot resolve it, you may complain to the <strong>Directorate of National Consumer Rights
Protection (DNCRP)</strong> under the Consumer Rights Protection Act, 2009.</p>'''),

 ('Governing law', '''
<p>These terms are governed by the laws of Bangladesh, and the courts of Bangladesh have
jurisdiction over any dispute.</p>'''),

 ('Contact us', CONTACT_BLOCK),
]


# ═══════════════════════════════════════════════════════════════════════
#  REFUND AND RETURNS
# ═══════════════════════════════════════════════════════════════════════
REFUNDS = [
 ('The short version', f'''
<div class="polbox"><p><b>Sealed and unopened, in resalable condition, within
{C('return window, for example 7 days')} of delivery — we take it back.</b><br>
<b>Opened food or supplements — we cannot take it back, for food safety reasons.</b><br>
<b>Damaged, wrong, or past its date — that is on us, always, whether or not it is opened.</b></p></div>
<p>The rest of this page explains each of those.</p>'''),

 ('Check your parcel at delivery', '''
<p>Before the courier leaves, check that:</p>
<ul>
  <li>The outer packaging is not torn, crushed or wet</li>
  <li>The jars inside are sealed and the seals are unbroken</li>
  <li>The batch date on each lid is readable</li>
  <li>You received what you ordered, in the pack sizes you ordered</li>
</ul>
<p>If anything is wrong, take a photograph before opening anything else and message us on
WhatsApp {PH} the same day.</p>'''.replace('{PH}', PH)),

 ('What you can return', f'''
<p>You may return a product for a refund if, within {C('return window, for example 7 days')} of
delivery, it is:</p>
<ul>
  <li><strong>Unopened</strong>, with the factory seal intact</li>
  <li><strong>Undamaged</strong>, with its label and batch date readable</li>
  <li>Still well inside its date</li>
</ul>'''),

 ('What you cannot return', '''
<p>We cannot accept a return if:</p>
<ul>
  <li><strong>The seal is broken or the jar has been opened.</strong> This is bird food. Once a
      container has been opened we cannot verify how it was stored, so it can never be sold
      again. This applies to every formula.</li>
  <li>The product has been repacked, decanted, or mixed with anything</li>
  <li>The batch date or label has been removed or defaced</li>
  <li>The return window has passed</li>
</ul>
<p>This does not apply to the next section. A damaged, wrong or out-of-date product is covered
whether or not it has been opened.</p>'''),

 ('If it arrives damaged, wrong, or out of date', f'''
<p>Then it is our problem, not yours.</p>
<ol>
  <li>Photograph the parcel, the jar, and the batch date on the lid</li>
  <li>Message the photographs to WhatsApp {PH} within
      {C('reporting window, for example 48 hours of delivery')}</li>
  <li>We confirm within {C('for example one working day')}</li>
  <li>We send a replacement at our cost, or refund you in full — your choice</li>
</ol>
<p>You do not pay return courier charges in this situation.</p>'''),

 ('How to start a return', f'''
<ol>
  <li>Message WhatsApp {PH} with your order number, what you are returning, and why</li>
  <li>We confirm the return and give you the return address</li>
  <li>Send the item back with the seals intact and the packaging it arrived in</li>
  <li>We inspect it on arrival and process your refund</li>
</ol>
<p><strong>Who pays the return courier:</strong> {C('who pays when the customer simply changed their mind. Standard practice is the customer pays for a change of mind and Shada pays when the fault is ours.')}</p>'''),

 ('How and when you get your money back', f'''
<p>Refunds go back <strong>by the same method you paid with</strong>. If you paid by bKash the refund
goes to that bKash number. We do not issue store credit instead of a refund unless you ask
for it.</p>
<p>We process refunds within {C('refund window, for example 7 working days')} of receiving and
approving the returned item. Any charge for issuing the refund is ours, not yours.</p>
<p>These timings follow the <strong>Digital Commerce Operation Guidelines 2021</strong> issued by the
Ministry of Commerce.</p>'''),

 ('If your order never arrives', f'''
<p>If we fail to deliver within the time set out in our
<a href="/shipping-policy/">Shipping policy</a>, you can cancel and we refund you in full, by
your original payment method, within {C('for example 7 working days')} of your cancellation.</p>'''),

 ('Cancelling before dispatch', '''
<p>Message us before the parcel is handed to the courier and we will cancel it and refund you
in full. Once it is with the courier the return process above applies instead.</p>'''),

 ('Your legal rights', '''
<p>Nothing on this page reduces your rights under the <strong>Consumer Rights Protection Act,
2009</strong>. If we cannot resolve a complaint, you may take it to the Directorate of National
Consumer Rights Protection (DNCRP).</p>'''),

 ('Contact us', CONTACT_BLOCK),
]


# ═══════════════════════════════════════════════════════════════════════
#  SHIPPING POLICY
# ═══════════════════════════════════════════════════════════════════════
SHIPPING = [
 ('Where we deliver', '''
<p>All 64 districts of Bangladesh, through <strong>Sundarban Courier Service</strong>.</p>
<p>You can also buy at the factory counter in Bhaluka without an appointment, or from a local
stockist — see <a href="/dealers/">the dealer list</a>.</p>'''),

 ('What it costs', f'''
<p>{C('delivery charge. Flat rate, by district, or free above a minimum order? This is the single most asked question before checkout and the page cannot go live without it.')}</p>'''),

 ('When it ships', f'''
<ul>
  <li>Orders placed before {C('daily cut-off time')} on a working day are handed to the courier
      the same day.</li>
  <li>Orders placed after that, or on Friday, go out the next working day.</li>
  <li>We send you the tracking details once the parcel is with the courier.</li>
</ul>
<p>The <strong>Digital Commerce Operation Guidelines 2021</strong> require us to hand a prepaid order to
the courier within 24 hours of payment and to notify you. We do.</p>'''),

 ('When it arrives', '''
<div class="polbox"><p><b>Two working days to most districts.</b> Remote upazilas and hill
districts can take longer.</p></div>
<p>Working days are Saturday to Thursday. Friday and public holidays are not working days.</p>
<p>The Digital Commerce Operation Guidelines 2021 set outer limits for prepaid orders: five days
for normal delivery and ten days for remote areas. We aim well inside those. If we miss them,
you can cancel for a full refund — see our
<a href="/refund_returns/">Refund and returns policy</a>.</p>'''),

 ('How your order is packed', '''
<p>Every jar is sealed at the factory with its batch date on the lid, then boxed with padding.
If the outer box arrives damaged, photograph it before opening and message us the same day.</p>'''),

 ('Tracking your parcel', f'''
<p>We send a tracking number by {C('SMS, WhatsApp or email — whichever you actually use')} once
the parcel is collected. You can also message WhatsApp {PH} with your order number and we
will check it for you.</p>'''),

 ('If delivery fails', f'''
<p>Couriers normally attempt delivery more than once and will call the number on the parcel.
Keep that phone reachable.</p>
<p>{C('what happens if the customer is unreachable and the parcel comes back — who pays the return leg, and whether the order is refunded in full')}</p>'''),

 ('Delivery outside Bangladesh', f'''
<p>{C('do you ship internationally at all? If not, say so plainly and delete this section.')}</p>'''),

 ('Contact us', CONTACT_BLOCK),
]


PAGES = [
  ('privacy-policy',       'Privacy policy',          '/privacy-policy/',
   'How Shada Bird Feed collects, uses and protects your personal data, under the Personal Data Protection Act, 2026.',
   PRIVACY),
  ('terms-and-conditions', 'Terms and conditions',    '/terms-and-conditions/',
   'The terms you buy under: products, prices, orders, payment, delivery, returns and governing law.',
   TERMS),
  ('refund-returns',       'Refund and returns',      '/refund_returns/',
   'When you can return bird feed, when you cannot, and how and when your refund is paid.',
   REFUNDS),
  ('shipping-policy',      'Shipping policy',         '/shipping-policy/',
   'Where we deliver, what it costs, when it ships and when it arrives. All 64 districts by Sundarban Courier.',
   SHIPPING),
]


def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def build(title, canon, desc, sections):
    jump = ''.join(f'<a href="#{slugify(h)}">{h}</a>' for h, _ in sections)
    body = ''.join(
        f'<h2 id="{slugify(h)}"><span>{i:02d}</span>{h}</h2>{c}'
        for i, (h, c) in enumerate(sections, 1))

    main = f'''<main id="main">

<section class="polhero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb" style="color:var(--on2)"><a href="/" style="color:var(--on2)">Home</a><i></i><span style="color:#fff">{title}</span></nav>
    <h1>{title}</h1>
    <p class="meta"><span>Last updated <b>{UPDATED}</b></span><i></i><span>Shada Bird Feed</span><i></i><span>Bhaluka, Mymensingh</span></p>
  </div>
</section>

<section>
  <div class="wrap polwrap">
    <nav class="poljump" aria-label="On this page">{jump}</nav>
    <div class="pol">{body}</div>
    <div class="polend">
      <h3>Still not sure?</h3>
      <p>Ask a person. We answer on WhatsApp faster than we answer anywhere else.</p>
      <div class="acts">
        <a class="btn b-brand" href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp {PH}</a>
        <a class="btn b-line" href="/contact/">Contact page</a>
      </div>
    </div>
  </div>
</section>

</main>
'''
    head = (HEAD
        .replace('<title>Shop · Shada Bird Feed</title>', f'<title>{title} · Shada Bird Feed</title>')
        .replace('<link rel="canonical" href="https://shadabirdfeed.com/shop/">',
                 f'<link rel="canonical" href="https://shadabirdfeed.com{canon}">'))
    head = re.sub(r'<meta name="description" content="[^"]*"',
                  f'<meta name="description" content="{desc}"', head, count=1)
    return head.replace('</head>', f'<style>{CSS}</style>\n</head>') + main + FOOT


if __name__ == '__main__':
    os.makedirs('/tmp/pg/out', exist_ok=True)
    total = 0
    for slug, title, canon, desc, sections in PAGES:
        html = build(title, canon, desc, sections)
        open(f'/tmp/pg/out/{slug}.html', 'w', encoding='utf-8').write(html)
        n = html.count('[CONFIRM:')
        total += n
        print(f'{slug+".html":28} {round(len(html)/1024):4} KB  {len(sections):2} sections  {n:2} [CONFIRM]')
    print(f'\n{total} decisions to confirm before any of these is published.')
