#!/usr/bin/env python3
# Shada Bird Feed · Wholesale page generator
# Built on the homepage's own classes: section / .dark / .tint / .brand / .wing /
# .wrap / .head / .eyebrow / .h-l / .h-m / .sub / .steps / .step / .btn / .crumbs.
# Margin figures are computed from the client's own price list, never typed by hand.
import re, os, json

HEAD = open('/tmp/pg/head.txt', encoding='utf-8').read()
FOOT = open('/tmp/pg/foot.txt', encoding='utf-8').read()

WA   = '8801813323535'
PH   = '01813-323535'
MAIL = 'shadabirdfeed@gmail.com'
ADDR = 'Majorvita, Bhaluka, Mymensingh'

# ── The client's price list, verbatim from "Shada Wholesale Data.xlsx" ──
#    name, pack, retail MRP, wholesale (10 kg tier), re-wholesale (5 kg tier)
PRICES = [
    ('Nutricare Hand Feeding Formula', '100g',  130,   75,   81),
    ('Nutricare Hand Feeding Formula', '200g',  240,  147,  155),
    ('Nutricare Hand Feeding Formula', '500g',  485,  362,  380),
    ('Nutricare Hand Feeding Formula', '1kg',   920,  690,  725),
    ('Avian Eggfood',                  '100g',  110,   66,   72),
    ('Avian Eggfood',                  '200g',  210,  125,  132),
    ('Avian Eggfood',                  '500g',  450,  308,  330),
    ('Avian Eggfood',                  '1kg',   870,  583,  616),
    ('Avian Herbs',                    '50g',   220,  164,  175),
    ('Avian Herbs',                    '100g',  395,  295,  313),
    ('Avian Herbs',                    '200g',  730,  580,  612),
    ('Avian Spirulina',                '50g',   350,  278,  295),
    ('Avian Spirulina',                '100g',  655,  524,  558),
    ('Avian Spirulina',                '200g', 1275, 1017, 1077),
    ('Avian Beetroot Powder',          '50g',   125,   99,  104),
    ('Avian Beetroot Powder',          '100g',  205,  164,  175),
    ('Avian Beetroot Powder',          '200g',  370,  295,  314),
    ('Avian Moringa Leaf Powder',      '50g',   125,   99,  104),
    ('Avian Moringa Leaf Powder',      '100g',  205,  164,  175),
    ('Avian Moringa Leaf Powder',      '200g',  370,  295,  314),
]
# Computed, not typed. If the price list changes these move with it.
W_OFF  = [(r - w) / r * 100 for _, _, r, w, _ in PRICES]
RW_OFF = [(r - x) / r * 100 for _, _, r, _, x in PRICES]
W_LO, W_HI = round(min(W_OFF)), round(max(W_OFF))
R_LO, R_HI = round(min(RW_OFF)), round(max(RW_OFF))
N_SKU = len(PRICES)

# ── Publish the per SKU dealer prices, or keep them behind the application?
#    False  = show the margin range only, send the full sheet after approval.
#             Standard B2B practice: it protects your dealers' selling price
#             and keeps your cost structure away from competitors.
#    True   = print the full 20 row table on the public page.
SHOW_PRICE_TABLE = False

I = lambda p, w=1.9: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
I_WA    = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd">'
           '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.9a8.1 8.1 0 0 1 6.6 12.8l-.3.4.7 2.5-2.6-.7-.4.2A8.1 8.1 0 1 1 12 3.9Z"/>'
           '<path d="M9.1 7.2h.6c.2 0 .5-.1.7.5l.9 2.2c.1.1.1.3 0 .5l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.4 2.4 1.5.3.1.4.1.6-.1.1-.2.7-.9.9-1.2.2-.2.4-.2.7-.1.2.1 1.7.9 2 1 .3.1.5.2.6.4 0 .1 0 .7-.2 1.4-.2.7-1.5 1.3-2 1.4-.6.1-1.1.3-3.6-.7-3-1.3-5-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.7-2.2 1-2.5c.3-.3.6-.4.8-.4Z"/></svg>')
I_PHONE = I('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7A2 2 0 0 1 22 16.9z"/>')
I_TRUCK = I('<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>')
I_PIN   = I('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>')
I_TAG   = I('<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>')
I_SHIELD= I('<path d="M12 3l8 3v6c0 5-3.4 8.3-8 9-4.6-.7-8-4-8-9V6z"/><path d="M9 12l2.2 2.2L15.5 10"/>')
I_ARROW = I('<path d="M5 12h14M12 5l7 7-7 7"/>', 2.4)
I_CHECK = I('<path d="M4 12.5 9.5 18 20 6.5"/>', 2.6)

DISTRICTS = ['Bagerhat','Bandarban','Barguna','Barisal','Bhola','Bogra','Brahamanbaria','Chandpur','Chittagong',
 'Chuadanga','Comilla',"Cox's Bazar",'Dhaka','Dinajpur','Faridpur','Feni','Gaibandha','Gazipur','Gopalganj',
 'Habiganj','Jamalpur','Jessore','Jhalokati','Jhenaidah','Joypurhat','Khagrachhari','Khulna','Kishoreganj',
 'Kurigram','Kushtia','Lakshmipur','Lalmonirhat','Madaripur','Magura','Manikganj','Maulvibazar','Meherpur',
 'Munshiganj','Mymensingh','Naogaon','Narail','Narayanganj','Narsingdi','Natore','Nawabganj','Netrakona',
 'Nilphamari','Noakhali','Pabna','Panchagarh','Patuakhali','Pirojpur','Rajbari','Rajshahi','Rangamati',
 'Rangpur','Satkhira','Shariatpur','Sherpur','Sirajganj','Sunamganj','Sylhet','Tangail','Thakurgaon']

VOLUMES = ['I am opening a new shop', 'Under 5 kg a month', '5 to 10 kg a month',
           '10 to 25 kg a month', 'More than 25 kg a month']

CSS = '''
/* ═══════════════════════════════════════════════════════════════════
   WHOLESALE  ·  /wholesale/
   Loads after 01-base.css and 02-shop-pages.css.
   Built on the homepage's own classes. The district picker and the form
   styling are the same components as /contact/, so a dealer filling this
   in recognises it from the contact page.
   ═══════════════════════════════════════════════════════════════════ */

/* ── Hero ────────────────────────────────────────────────────────── */
.whero{background:var(--ink);color:#fff;position:relative;overflow:hidden;
  padding:clamp(40px,5.4vw,78px) 0 clamp(36px,4.6vw,62px)}
.whero::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;opacity:.07;pointer-events:none}
.whero .wrap{position:relative}
.whero h1{font-size:clamp(34px,5vw,62px);letter-spacing:-.035em;line-height:1.04;margin:10px 0 14px;max-width:15ch}
.whero .lede{font-size:17.5px;line-height:1.6;color:var(--on2);max-width:56ch}
.whero .acts{display:flex;gap:11px;flex-wrap:wrap;margin-top:28px}
.wfacts{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-top:34px}
@media(max-width:760px){.wfacts{grid-template-columns:1fr}}
.wfact{background:var(--ink2);border:1px solid var(--line-d);border-radius:var(--r2);padding:20px 22px}
.wfact b{display:block;font-size:clamp(26px,3vw,36px);letter-spacing:-.035em;line-height:1}
.wfact span{display:block;font-size:13px;color:var(--on2);margin-top:7px;line-height:1.45}

/* ── The two tiers. This is the offer, so it gets the brand green. ── */
.wtiers{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:820px){.wtiers{grid-template-columns:1fr}}
.wtier{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.28);border-radius:var(--r3);
  padding:clamp(26px,3vw,36px);color:#fff}
.wtier.best{background:#fff;border-color:#fff;color:var(--tx);position:relative}
.wtier .pill{position:absolute;top:-13px;left:clamp(26px,3vw,36px);background:var(--ink);color:#fff;
  font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:6px 13px}
.wtier .n{display:block;font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
  color:#DFF7E6;margin-bottom:12px}
.wtier.best .n{color:var(--brand)}
.wtier .big{display:block;font-size:clamp(34px,4.4vw,52px);letter-spacing:-.04em;line-height:1;margin-bottom:6px}
.wtier .off{display:block;font-size:14.5px;opacity:.85;margin-bottom:18px}
.wtier ul{list-style:none;display:grid;gap:10px}
.wtier li{display:flex;gap:10px;align-items:flex-start;font-size:15px;line-height:1.5}
.wtier li svg{width:17px;height:17px;flex:0 0 auto;margin-top:3px}
.wtier.best li svg{color:var(--brand)}
.wnote{margin-top:26px;font-size:14px;color:rgba(255,255,255,.82);line-height:1.6;max-width:70ch}
.wnote b{color:#fff;font-weight:600}

/* ── What you get ───────────────────────────────────────────────── */
.wgets{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:860px){.wgets{grid-template-columns:1fr}}
.wget{background:#fff;border:1px solid var(--line);border-radius:var(--r3);padding:28px 30px}
.wget .ic{width:42px;height:42px;border-radius:11px;display:grid;place-items:center;margin-bottom:16px;
  background:var(--paper2);border:1px solid var(--line)}
.wget .ic svg{width:20px;height:20px;color:var(--brand)}
.wget h3{font-size:19px;letter-spacing:-.02em;margin-bottom:8px;line-height:1.3}
.wget p{font-size:15px;line-height:1.6;color:var(--tx2)}

/* ── Application form. Same components as /contact/. ────────────── */
.wgrid{display:grid;grid-template-columns:1.25fr .75fr;gap:clamp(24px,3.4vw,52px);align-items:start}
@media(max-width:940px){.wgrid{grid-template-columns:1fr}}
.wform{background:#fff;border:1px solid var(--line);border-radius:var(--r3);
  box-shadow:0 22px 54px rgba(10,38,23,.09);overflow:hidden}
.wform .bar{height:5px;background:linear-gradient(90deg,var(--brand),var(--leaf))}
.wform .in{padding:clamp(24px,3.2vw,38px)}
.wform h2{font-size:clamp(22px,2.5vw,30px);letter-spacing:-.025em;margin-bottom:7px}
.wform .note{font-size:14.5px;color:var(--tx2);margin-bottom:26px;line-height:1.55}
.ctrow{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:560px){.ctrow{grid-template-columns:1fr}}
.ctf{margin-bottom:18px}
.ctf label{display:block;font-size:13px;font-weight:600;color:var(--tx);margin-bottom:7px}
.ctf label i{font-style:normal;color:var(--tx3);font-weight:400}
.ctf label em{font-style:normal;color:var(--brand)}
.ctf input,.ctf select,.ctf textarea{width:100%;border:1.5px solid var(--line);border-radius:var(--r2);
  background:#fff;padding:0 15px;height:54px;font:500 15.5px/1 var(--ff);color:var(--tx);outline:none;
  transition:border-color .18s,box-shadow .18s;-webkit-appearance:none;appearance:none}
.ctf textarea{height:auto;min-height:120px;padding:15px;line-height:1.55;resize:vertical}
.ctf select{background-image:url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236E6E73' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 14px center;background-size:18px;padding-right:40px;cursor:pointer}
.ctf input:hover,.ctf select:hover,.ctf textarea:hover{border-color:var(--tx3)}
.ctf input:focus,.ctf select:focus,.ctf textarea:focus{border-color:var(--brand);box-shadow:0 0 0 4px rgba(8,152,48,.12)}
.ctf input::placeholder,.ctf textarea::placeholder{color:var(--tx3);font-weight:400}
.ctf.bad input,.ctf.bad select,.ctf.bad textarea,.ctf.bad .cbinput{border-color:#C0392B;box-shadow:0 0 0 4px rgba(192,57,43,.1)}
.ctf .err{display:none;font-size:12.5px;color:#C0392B;margin-top:6px;font-weight:500}
.ctf.bad .err{display:block}
.ctsub{margin-top:8px;padding-top:22px;border-top:1px solid var(--line)}
.ctsub .btn{width:100%;min-height:58px;height:58px;font-size:16px}
.ctsub small{display:block;font-size:12.5px;color:var(--tx3);line-height:1.55;margin-top:14px;text-align:center}

/* District picker, identical to the one on /contact/ */
.ctcombo{position:relative}
.ctcombo select.hid{position:absolute;opacity:0;pointer-events:none;height:0;min-height:0;width:0;padding:0;margin:0;border:0}
.cbinput{width:100%;border:1.5px solid var(--line);border-radius:var(--r2);background:#fff;
  padding:0 42px 0 15px;height:54px;font:500 15.5px/1 var(--ff);color:var(--tx);outline:none;
  transition:border-color .18s,box-shadow .18s}
.cbinput::placeholder{color:var(--tx3);font-weight:400}
.cbinput:hover{border-color:var(--tx3)}
.cbinput:focus{border-color:var(--brand);box-shadow:0 0 0 4px rgba(8,152,48,.12)}
.cbicon{position:absolute;right:15px;top:50%;transform:translateY(-50%);width:18px;height:18px;
  color:var(--tx3);pointer-events:none;transition:transform .18s}
.ctcombo.open .cbicon{transform:translateY(-50%) rotate(180deg)}
.cblist{position:absolute;z-index:30;left:0;right:0;top:calc(100% + 6px);margin:0;padding:6px;list-style:none;
  background:#fff;border:1px solid var(--line);border-radius:var(--r2);
  box-shadow:0 20px 44px rgba(10,38,23,.16);max-height:272px;overflow-y:auto;overscroll-behavior:contain}
.cblist[hidden]{display:none}
.cbopt{display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:44px;padding:10px 12px;
  border-radius:10px;font-size:15px;color:var(--tx);cursor:pointer;line-height:1.3}
.cbopt:hover,.cbopt.on{background:var(--paper2)}
.cbopt[aria-selected="true"]{color:var(--brand);font-weight:600}
.cbopt .tick{width:16px;height:16px;flex:0 0 auto;opacity:0;color:var(--brand)}
.cbopt[aria-selected="true"] .tick{opacity:1}
.cbopt mark{background:rgba(8,152,48,.16);color:inherit;border-radius:3px;padding:0 1px}
.cbnone{padding:14px 12px;font-size:14px;color:var(--tx2)}

/* Side column */
.wside{display:grid;gap:14px}
.wcard{background:var(--paper2);border:1px solid var(--line);border-radius:var(--r3);padding:24px 26px}
.wcard h3{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3);margin-bottom:16px}
.wsteps{list-style:none;display:grid;gap:18px;counter-reset:s}
.wsteps li{display:flex;gap:14px;align-items:flex-start;counter-increment:s}
.wsteps li::before{content:counter(s);flex:0 0 auto;width:30px;height:30px;border-radius:50%;background:var(--ink);
  color:#fff;font-size:13.5px;font-weight:700;display:grid;place-items:center}
.wsteps b{display:block;font-size:15.5px;letter-spacing:-.01em;margin-bottom:3px}
.wsteps span{display:block;font-size:14px;color:var(--tx2);line-height:1.5}
.wrows{display:grid;gap:4px}
.wrow{display:flex;gap:12px;align-items:flex-start;padding:11px 0;text-decoration:none;color:var(--tx);
  border-bottom:1px solid var(--line)}
.wrow:last-child{border-bottom:0}
.wrow svg{width:19px;height:19px;flex:0 0 auto;margin-top:2px;color:var(--brand)}
.wrow > span{text-align:left;min-width:0}
.wrow b{display:block;font-size:15.5px;font-weight:600;margin-bottom:2px}
.wrow span span,.wrow > span > span{display:block;font-size:13.5px;color:var(--tx2);line-height:1.45}
a.wrow:hover b{color:var(--brand)}

/* Optional per SKU table */
.wtable{width:100%;border-collapse:collapse;font-size:14.5px;background:#fff;
  border:1px solid var(--line);border-radius:var(--r3);overflow:hidden}
.wtable th,.wtable td{padding:13px 16px;text-align:left;border-bottom:1px solid var(--line)}
.wtable th{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--tx3);font-weight:600;background:var(--paper2)}
.wtable tr:last-child td{border-bottom:0}
.wtable td.num{text-align:right;font-variant-numeric:tabular-nums}
'''


def wholesale_page():
    opts = ''.join(f'<option value="{d}">{d}</option>' for d in sorted(set(DISTRICTS)))
    vols = ''.join(f'<option value="{v}">{v}</option>' for v in VOLUMES)

    table = ''
    if SHOW_PRICE_TABLE:
        rows = ''.join(
            f'<tr><td>{n}</td><td>{p}</td><td class="num">{r:,}</td>'
            f'<td class="num">{w:,}</td><td class="num">{x:,}</td></tr>'
            for n, p, r, w, x in PRICES)
        table = f'''
<!-- ═══════════ PER SKU PRICE TABLE ═══════════ -->
<section class="tint">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Dealer price list</span>
      <h2 class="h-l">Every pack, every tier.</h2>
      <p class="sub" style="margin-top:14px">All {N_SKU} pack sizes. Prices in BDT, per jar.</p>
    </div>
    <div style="overflow-x:auto">
      <table class="wtable">
        <thead><tr><th>Product</th><th>Pack</th><th style="text-align:right">Retail</th>
        <th style="text-align:right">Wholesale</th><th style="text-align:right">Re&#8209;wholesale</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>
'''

    body = f'''<main id="main">

<!-- ═══════════ 1 · HERO ═══════════ -->
<section class="whero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb" style="color:var(--on2)"><a href="/" style="color:var(--on2)">Home</a><i></i><span style="color:#fff">Wholesale</span></nav>
    <span class="eyebrow" style="color:var(--leaf)">Dealer accounts</span>
    <h1>Sell Shada in your district.</h1>
    <p class="lede">We are opening one distributor per district. You buy at the wholesale price,
    sell at the printed retail price, and keep the difference. No franchise fee, no monthly target,
    no lock&#8209;in.</p>
    <div class="acts">
      <a class="btn b-brand" href="#apply">Apply for a dealer account {I_ARROW}</a>
      <a class="btn b-white" href="https://wa.me/{WA}?text=Dealer%20enquiry" target="_blank" rel="noopener">{I_WA} Ask on WhatsApp</a>
    </div>
    <div class="wfacts">
      <div class="wfact"><b>{W_LO} to {W_HI}%</b><span>Below the printed retail price, depending on the pack</span></div>
      <div class="wfact"><b>1</b><span>Distributor per district. Yours is either open or it is not</span></div>
      <div class="wfact"><b>{N_SKU}</b><span>Pack sizes across six formulas to stock from</span></div>
    </div>
  </div>
</section>

<!-- ═══════════ 2 · THE TWO TIERS ═══════════ -->
<section class="brand wing">
  <div class="wrap" style="position:relative;z-index:1">
    <div class="head">
      <span class="eyebrow" style="color:#DFF7E6">The rates</span>
      <h2 class="h-l" style="color:#fff">Two tiers. Both below retail.</h2>
    </div>
    <div class="wtiers">
      <div class="wtier best">
        <span class="pill">Best rate</span>
        <span class="n">Wholesale</span>
        <span class="big">{W_LO}&ndash;{W_HI}%</span>
        <span class="off">below the printed retail price</span>
        <ul>
          <li>{I_CHECK}<span>For a shop stocking the range properly</span></li>
          <li>{I_CHECK}<span>Every one of the {N_SKU} pack sizes</span></li>
          <li>{I_CHECK}<span>Delivered to your shop, anywhere in Bangladesh</span></li>
        </ul>
      </div>
      <div class="wtier">
        <span class="n">Re&#8209;wholesale</span>
        <span class="big">{R_LO}&ndash;{R_HI}%</span>
        <span class="off">below the printed retail price</span>
        <ul>
          <li>{I_CHECK}<span>For a smaller counter or a first order</span></li>
          <li>{I_CHECK}<span>Same {N_SKU} pack sizes, same jars</span></li>
          <li>{I_CHECK}<span>Move up to the wholesale tier as volume grows</span></li>
        </ul>
      </div>
    </div>
    <p class="wnote"><b>Which tier you get depends on order size.</b> Tell us roughly how much you
    sell in a month and we will confirm your tier and the exact per&#8209;jar rate for all {N_SKU} packs.
    The rate is the same in every district.</p>
  </div>
</section>

<!-- ═══════════ 3 · WHAT YOU GET ═══════════ -->
<section>
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">What comes with it</span>
      <h2 class="h-l">More than a discount.</h2>
    </div>
    <div class="wgets">
      <div class="wget"><span class="ic">{I_TRUCK}</span>
        <h3>Delivered to your shop</h3>
        <p>From Bhaluka to any district, on our courier account above the minimum order. You do not
        arrange transport and you do not collect.</p></div>
      <div class="wget"><span class="ic">{I_PIN}</span>
        <h3>Listed on the dealer page</h3>
        <p>Your shop name, phone and directions on <a class="link" style="font-size:inherit" href="/dealers/">the dealer map</a>,
        in front of every breeder searching your district.</p></div>
      <div class="wget"><span class="ic">{I_SHIELD}</span>
        <h3>Your price is protected</h3>
        <p>We publish one retail price and hold it in all 64 districts, including on this website.
        Nobody undercuts you online, including us.</p></div>
    </div>
  </div>
</section>
{table}
<!-- ═══════════ 4 · APPLY ═══════════ -->
<section class="tint" id="apply">
  <div class="wrap wgrid">

    <form class="wform" id="shadaWholesale" method="post" action="/thank-you/" novalidate>
      <div class="bar"></div>
      <div class="in">
        <h2>Apply for a dealer account</h2>
        <p class="note">Six fields. We reply on WhatsApp with your tier and the full price list.</p>

        <div class="ctrow">
          <div class="ctf" id="f_shop"><label for="w_shop">Shop name <em>*</em></label>
            <input id="w_shop" name="shop" type="text" placeholder="Name on the signboard">
            <span class="err">Please add your shop name</span></div>
          <div class="ctf" id="f_name"><label for="w_name">Your name <em>*</em></label>
            <input id="w_name" name="name" type="text" autocomplete="name" placeholder="Write your name">
            <span class="err">Please add your name</span></div>
        </div>

        <div class="ctrow">
          <div class="ctf" id="f_phone"><label for="w_phone">Phone or WhatsApp <em>*</em></label>
            <input id="w_phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="01XXXXXXXXX">
            <span class="err">We need a number to reply to</span></div>
          <div class="ctf" id="f_district"><label for="w_district">District <em>*</em></label>
            <div class="ctcombo" id="districtCombo">
              <select id="w_district" name="district">
                <option value="">Select your district</option>{opts}
              </select>
            </div>
            <span class="err">Please choose your district</span></div>
        </div>

        <div class="ctf" id="f_vol"><label for="w_vol">Roughly how much do you sell now <em>*</em></label>
          <select id="w_vol" name="volume">
            <option value="">Choose one</option>{vols}
          </select>
          <span class="err">Please pick the closest one</span></div>

        <div class="ctf"><label for="w_msg">Anything else <i>optional</i></label>
          <textarea id="w_msg" name="message" placeholder="Which formulas you are most interested in, or anything we should know."></textarea></div>

        <div class="ctsub">
          <button class="btn b-brand" type="submit">Send application {I_ARROW}</button>
          <small>Your details are used to answer this application only. We do not share them and we
          do not send marketing messages.</small>
        </div>
      </div>
    </form>

    <div class="wside">
      <div class="wcard">
        <h3>How it works</h3>
        <ol class="wsteps">
          <li><div><b>You apply</b><span>The form, or a message on WhatsApp. Shop name and district is enough to start.</span></div></li>
          <li><div><b>We check the district</b><span>If it is open we confirm your tier and send the full price list for all {N_SKU} packs.</span></div></li>
          <li><div><b>Your first order ships</b><span>Sealed jars with the batch date on the lid, to your shop, in two working days.</span></div></li>
        </ol>
      </div>

      <div class="wcard">
        <h3>Or just call</h3>
        <div class="wrows">
          <a class="wrow" href="https://wa.me/{WA}?text=Dealer%20enquiry" target="_blank" rel="noopener">
            {I_WA}<span><b>WhatsApp {PH}</b><span>The fastest way. Say which district you are in.</span></span></a>
          <a class="wrow" href="tel:+{WA}">
            {I_PHONE}<span><b>Call {PH}</b><span>Saturday to Thursday, 9am to 6pm</span></span></a>
          <div class="wrow">
            {I_PIN}<span><b>The factory</b><span>{ADDR}. Counter sales, no appointment needed.</span></span></div>
        </div>
      </div>

      <div class="wcard">
        <h3>Already a dealer?</h3>
        <div class="wrows">
          <a class="wrow" href="/dealers/">{I_TAG}<span><b>See the dealer map</b><span>Check which districts are taken before you apply.</span></span></a>
        </div>
      </div>
    </div>
  </div>
</section>

</main>

<script>
/* ═══════════════════════════════════════════════════════════════════
   WHOLESALE FORM
   Same two pieces as /contact/: a searchable district picker built over
   a real <select>, and inline validation. Nothing is sent from here.
   Point the form at your form plugin and keep the field names and the
   /thank-you/ action so the conversion still fires.
   ═══════════════════════════════════════════════════════════════════ */
(function(){{
  var wrap = document.getElementById('districtCombo');
  var sel  = document.getElementById('w_district');
  if(wrap && sel){{
    var items = [].slice.call(sel.options).filter(function(o){{ return o.value; }})
                  .map(function(o){{ return o.value; }});
    sel.classList.add('hid'); sel.setAttribute('tabindex','-1'); sel.setAttribute('aria-hidden','true');

    var box = document.createElement('div');
    box.innerHTML =
      '<input class="cbinput" id="cbInput" type="text" role="combobox" aria-expanded="false" ' +
      'aria-controls="cbList" aria-autocomplete="list" aria-label="District" autocomplete="off" ' +
      'placeholder="Type to search your district">' +
      '<svg class="cbicon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg>' +
      '<ul class="cblist" id="cbList" role="listbox" aria-label="Districts" hidden></ul>';
    while(box.firstChild) wrap.appendChild(box.firstChild);

    var input = document.getElementById('cbInput');
    var list  = document.getElementById('cbList');
    var TICK  = '<svg class="tick" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
                'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5 9.5 18 20 6.5"/></svg>';
    var active = -1;

    function esc(t){{ return String(t).replace(/[&<>"]/g, function(c){{
      return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]; }}); }}
    function mark(name, q){{
      if(!q) return esc(name);
      var i = name.toLowerCase().indexOf(q.toLowerCase());
      if(i < 0) return esc(name);
      return esc(name.slice(0,i)) + '<mark>' + esc(name.slice(i,i+q.length)) + '</mark>' + esc(name.slice(i+q.length));
    }}
    function render(q){{
      q = (q||'').trim();
      var shown = items.filter(function(n){{ return n.toLowerCase().indexOf(q.toLowerCase()) > -1; }});
      if(!shown.length){{
        list.innerHTML = '<li class="cbnone">No district called &quot;' + esc(q) +
          '&quot;. Pick the nearest one.</li>'; active = -1; return;
      }}
      list.innerHTML = shown.map(function(n,i){{
        return '<li class="cbopt" id="cbo'+i+'" role="option" data-v="'+esc(n)+'" aria-selected="' +
               (sel.value===n) + '"><span>'+mark(n,q)+'</span>'+TICK+'</li>'; }}).join('');
      active = -1;
    }}
    function open(){{ if(!list.hidden) return; render(''); list.hidden=false;
      input.setAttribute('aria-expanded','true'); wrap.classList.add('open'); }}
    function close(){{ list.hidden=true; active=-1;
      input.setAttribute('aria-expanded','false'); wrap.classList.remove('open');
      input.removeAttribute('aria-activedescendant'); }}
    function choose(n){{ sel.value=n; input.value=n;
      sel.dispatchEvent(new Event('change',{{bubbles:true}})); close(); }}
    function highlight(i){{
      var o = list.querySelectorAll('.cbopt'); if(!o.length) return;
      if(i<0) i=o.length-1; if(i>=o.length) i=0; active=i;
      [].forEach.call(o,function(x,k){{ x.classList.toggle('on',k===i); }});
      o[i].scrollIntoView({{block:'nearest'}}); input.setAttribute('aria-activedescendant',o[i].id);
    }}
    input.addEventListener('focus',open);
    input.addEventListener('click',open);
    input.addEventListener('input',function(){{
      if(list.hidden){{ list.hidden=false; input.setAttribute('aria-expanded','true'); wrap.classList.add('open'); }}
      render(input.value); }});
    input.addEventListener('keydown',function(e){{
      if(e.key==='ArrowDown'){{ e.preventDefault(); if(list.hidden) open(); highlight(active+1); }}
      else if(e.key==='ArrowUp'){{ e.preventDefault(); if(list.hidden) open(); highlight(active-1); }}
      else if(e.key==='Enter'){{
        if(!list.hidden){{ var o=list.querySelectorAll('.cbopt');
          var p = active>-1 ? o[active] : (o.length===1 ? o[0] : null);
          if(p){{ e.preventDefault(); choose(p.getAttribute('data-v')); }} }} }}
      else if(e.key==='Escape'){{ close(); }} }});
    list.addEventListener('mousedown',function(e){{
      var o = e.target.closest ? e.target.closest('.cbopt') : null; if(!o) return;
      e.preventDefault(); choose(o.getAttribute('data-v')); }});
    input.addEventListener('blur',function(){{ setTimeout(function(){{
      if(items.indexOf(input.value.trim())===-1) input.value = sel.value || '';
      close(); }},130); }});
    document.addEventListener('click',function(e){{ if(!wrap.contains(e.target)) close(); }});
  }}

  var f = document.getElementById('shadaWholesale');
  if(!f) return;
  var req = [['f_shop','w_shop'],['f_name','w_name'],['f_phone','w_phone'],
             ['f_district','w_district'],['f_vol','w_vol']];
  f.addEventListener('submit', function(e){{
    var first = null;
    req.forEach(function(p){{
      var w = document.getElementById(p[0]), el = document.getElementById(p[1]);
      var bad = !el.value.trim(); w.classList.toggle('bad', bad);
      if(bad && !first) first = (p[1]==='w_district' && document.getElementById('cbInput'))
                                 ? document.getElementById('cbInput') : el;
    }});
    if(first){{ e.preventDefault(); first.focus(); first.scrollIntoView({{block:'center',behavior:'smooth'}}); }}
  }});
  var clear = function(e){{ var w = e.target.closest('.ctf'); if(w) w.classList.remove('bad'); }};
  f.addEventListener('input', clear);
  f.addEventListener('change', clear);
}})();
</script>
'''

    head = (HEAD
        .replace('<title>Shop · Shada Bird Feed</title>', '<title>Wholesale · Shada Bird Feed</title>')
        .replace('<link rel="canonical" href="https://shadabirdfeed.com/shop/">',
                 '<link rel="canonical" href="https://shadabirdfeed.com/wholesale/">'))
    head = re.sub(r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="Become a Shada Bird Feed dealer. One distributor per district, {W_LO} to {W_HI}% below retail, delivered to your shop anywhere in Bangladesh. No franchise fee."',
        head, count=1)

    ld = {"@context": "https://schema.org", "@type": "WebPage",
          "name": "Wholesale and dealer accounts, Shada Bird Feed",
          "description": f"One distributor per district. {W_LO} to {W_HI}% below the printed retail price, delivered to your shop.",
          "provider": {"@type": "Organization", "name": "Shada Bird Feed",
                       "telephone": "+" + WA, "email": MAIL,
                       "address": {"@type": "PostalAddress", "streetAddress": "Majorvita",
                                   "addressLocality": "Bhaluka", "addressRegion": "Mymensingh",
                                   "addressCountry": "BD"}}}
    ldjson = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    return head.replace('</head>', f'<style>{CSS}</style>\n{ldjson}\n</head>') + body + FOOT


if __name__ == '__main__':
    os.makedirs('/tmp/pg/out', exist_ok=True)
    open('/tmp/pg/out/wholesale.html', 'w', encoding='utf-8').write(wholesale_page())
    print('wholesale.html', round(os.path.getsize('/tmp/pg/out/wholesale.html') / 1024), 'KB',
          f'| wholesale {W_LO}-{W_HI}% off, re-wholesale {R_LO}-{R_HI}% off, {N_SKU} SKUs',
          f'| price table published: {SHOW_PRICE_TABLE}')
