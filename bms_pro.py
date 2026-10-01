#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shada BMS · Phase 0 prototype, single file.

Everything on screen is computed from one in-memory store, so saving a sale
really does move the dashboard, the customer record, the timeline and the
totals. That is the client's Single Data Entry requirement, demonstrated.

Static reference screens (Inventory, Accounts, Reports, Settings) are carried
over unchanged from the earlier pass.
"""
import base64, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bms_pro_css import CSS
from bms_live_js import ENGINE, ENGINE2
from bms_customers import as_dict
from bms_one import IC, PRODUCTS, reports
from bms_one import TOP_PROD, STOCK
from bms_restyle import restyle

I = lambda p, w=1.8: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
IC = dict(IC)
IC['x']     = I('<path d="M6 6l12 12M18 6L6 18"/>', 2.2)
IC['alert'] = I('<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>')
IC['down']  = I('<path d="M12 5v14M19 12l-7 7-7-7"/>', 2)
IC['up']    = I('<path d="M12 19V5M5 12l7-7 7 7"/>', 2)
IC['users'] = I('<circle cx="9" cy="8" r="3.2"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 5.2a3.2 3.2 0 0 1 0 5.6"/><path d="M18 14.4a6.5 6.5 0 0 1 3.5 5.6"/>')
IC['cart']  = I('<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.7 12.4a1.5 1.5 0 0 0 1.5 1.1h8.1a1.5 1.5 0 0 0 1.5-1.2L21 7H6"/>')
IC['leaf']  = I('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/>')
IC['flag']  = I('<path d="M4 21V4h9l1 2h6v9h-7l-1-2H4"/>')
IC['link']  = I('<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>')
IC['shield']= I('<path d="M12 2 4 5.5V11c0 5.2 3.4 9.4 8 11 4.6-1.6 8-5.8 8-11V5.5z"/><path d="m9 12 2 2 4-4"/>')
IC['chart'] = I('<path d="M3 3v18h18"/><path d="m7 15 4-5 3 3 6-7"/>')
IC['pin']   = I('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>')
IC['note']  = I('<path d="M5 4h11l4 4v12H5z"/><path d="M15 4v5h5"/><path d="M8 13h8M8 17h5"/>')
IC['tag']   = I('<path d="M20 12 12 20 3 11V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/>')
IC['clipboard'] = I('<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1"/><path d="m8.5 12 2 2 4-4"/><path d="M9 17h6"/>')
IC['calendar'] = I('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>')
IC['cash']  = I('<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M5.5 9.5h.01M18.5 14.5h.01"/>')
IC['phone'] = I('<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18h2"/>')
IC['bank']  = I('<path d="M3 10 12 4l9 6"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8"/><path d="M3 20h18"/>')
IC['truck'] = I('<path d="M3 7h11v9H3z"/><path d="M14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>')
IC['building'] = I('<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M9.5 21v-4h5v4"/><path d="M8 7.5h2M14 7.5h2M8 11.5h2M14 11.5h2"/>')
IC['receipt']  = I('<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>')
IC['download'] = I('<path d="M12 4v11"/><path d="m7 10 5 5 5-5"/><path d="M4 20h16"/>')
IC['history']  = I('<path d="M3.5 12a8.5 8.5 0 1 0 2.5-6"/><path d="M3 4v5h5"/><path d="M12 8v4.5l3 1.8"/>')
IC['ticket']   = I('<path d="M3 8V6a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v2a2 2 0 0 0 0 4v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-2a2 2 0 0 0 0-4z"/><path d="M13 6v9" stroke-dasharray="2 2"/>')
IC['pencil']   = I('<path d="M4 20h4L18.5 9.5a2.1 2.1 0 0 0-3-3L5 17z"/><path d="m13.5 6.5 3 3"/>')
IC['bars']     = I('<path d="M4 20V11"/><path d="M10 20V5"/><path d="M16 20v-8"/><path d="M22 20H2"/>')
# brand-coloured monogram tiles (not the trademark artwork; the official SVGs drop in at plugin build)
_TILE = ('<svg aria-hidden="true" viewBox="0 0 24 24" class="brand"><rect x="2" y="2" width="20" height="20" rx="5" fill="{bg}" stroke="none"/>'
         '<text x="12" y="{y}" text-anchor="middle" font-size="{fs}" font-weight="700" '
         'font-family="DM Sans,Inter,system-ui,sans-serif" fill="#fff" stroke="none">{ch}</text></svg>')
IC['bkash'] = _TILE.format(bg='#E2136E', y='16.8', fs='14', ch='b')
IC['nagad'] = _TILE.format(bg='#F6921E', y='16.4', fs='12.5', ch='N')

METHODS = [('Cash', 'cash', ''), ('bKash', 'bkash', 'bk'), ('Nagad', 'nagad', 'ng'),
           ('Bank transfer', 'bank', ''), ('Courier COD', 'truck', '')]


def method_picker(input_id, default='Cash'):
    rows = ''.join(
        f'<div class="opt mopt {cls}" role="option" data-method="{m}" data-for="{input_id}" '
        f'aria-selected="{str(m == default).lower()}">{IC[ic]}<span class="nm">{m}</span>{IC["check"]}</div>'
        for m, ic, cls in METHODS)
    return (f'<div class="msel cbx" id="msel-{input_id}">'
            f'<button type="button" class="inp mselb" aria-haspopup="listbox" aria-expanded="false" data-msel="{input_id}">'
            f'<span class="mic">{IC["cash"]}</span><span class="mlbl">{default}</span><span class="chev">{IC["down"]}</span></button>'
            f'<div class="cbxlist mlist" role="listbox">{rows}</div>'
            f'<input type="hidden" id="{input_id}" value="{default}"></div>')


# card-title icon, picked by keyword so every screen gets one without per-view edits
def title_icon(title):
    t = title.lower()
    rules = [
        (('who buys','customer','users, roles'), 'users'), (('sales by','sales,','sales this','today against'), 'chart'),
        (('district',), 'pin'), (('stock','inventory','raw material','finished','movement'), 'stock'),
        (('production',), 'leaf'), (('product','pack','items'), 'cart'), (('order',), 'cart'),
        (('payment','collection','money','transaction','cash','expense','payable','balance','accounts'), 'money'),
        (('timeline','activity','log','no purchase'), 'time'), (('report','monthly','daily','weekly'), 'report'),
        (('backup','company','invoice setting','setting','courier','bank account'), 'gear'),
        (('top ',), 'up'), (('sale',), 'sale'), (('note',), 'note'),
    ]
    for keys, ic in rules:
        if any(k in t for k in keys): return ic
    return 'flag'

DISTRICTS = [
 'Bagerhat','Bandarban','Barguna','Barishal','Bhola','Bogura','Brahmanbaria','Chandpur',
 'Chattogram','Chuadanga','Cox\u2019s Bazar','Cumilla','Dhaka','Dinajpur','Faridpur','Feni',
 'Gaibandha','Gazipur','Gopalganj','Habiganj','Jamalpur','Jashore','Jhalokathi','Jhenaidah',
 'Joypurhat','Khagrachhari','Khulna','Kishoreganj','Kurigram','Kushtia','Lakshmipur','Lalmonirhat',
 'Madaripur','Magura','Manikganj','Meherpur','Moulvibazar','Munshiganj','Mymensingh','Naogaon',
 'Narail','Narayanganj','Narsingdi','Natore','Netrokona','Nilphamari','Noakhali','Pabna',
 'Panchagarh','Patuakhali','Pirojpur','Rajbari','Rajshahi','Rangamati','Rangpur','Satkhira',
 'Shariatpur','Sherpur','Sirajganj','Sunamganj','Sylhet','Tangail','Thakurgaon','Rajshahi Sadar',
]
DISTRICTS = sorted(set(DISTRICTS))

IMGDIR = '/sessions/pensive-affectionate-einstein/mnt/Projects/Shada Birds/wp-assets/03-products'
IMGMAP = {'Nutricare Hand Feeding': 'jar-nutricare', 'Avian Eggfood': 'jar-eggfood',
          'Avian Spirulina': 'jar-spirulina', 'Avian Herbs': 'jar-herbs',
          'Avian Moringa': 'jar-moringa', 'Avian Beetroot': 'jar-beetroot'}


def _img(family):
    """Thumbnails are inlined. The prototype has to open from a folder, an email
    or a phone with no network, so it carries its own assets."""
    f = os.path.join(IMGDIR, IMGMAP[family] + '-thumb-160.webp')
    with open(f, 'rb') as fh:
        return 'data:image/webp;base64,' + base64.b64encode(fh.read()).decode()


CUST = as_dict()
SKU_FAMILY = {'Nutricare Hand Feeding': 'NHF', 'Avian Eggfood': 'AEF', 'Avian Spirulina': 'ASP',
              'Avian Herbs': 'AHB', 'Avian Moringa': 'AML', 'Avian Beetroot': 'ABP'}


def _sku(fam, pack):
    # client scheme (Anowar Bhai, 28 Sep 2026): SBF- + family code + grams, 3 digits minimum: SBF-NHF-1000, SBF-AHB-050
    code = SKU_FAMILY.get(fam) or ''.join(w[0] for w in fam.split() if w.lower() != 'avian')[:3].upper().ljust(3, 'X')
    g = int(float(pack.lower().replace('kg', '')) * 1000) if 'kg' in pack.lower() else int(pack.lower().replace('g', ''))
    return f'SBF-{code}-{g:03d}'


PROD = [{'n': f'{n} · {s}', 'fam': n, 'pack': s, 'r': r, 'w': w, 'img': _img(n), 'sku': _sku(n, s)}
        for n, s, r, w in PRODUCTS]
GENERIC_IMG = ('data:image/svg+xml;utf8,' +
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="14" y="10" width="36" height="46" rx="8" fill="%23E8F6EC"/>'
  '<rect x="18" y="6" width="28" height="8" rx="3" fill="%23089830"/><rect x="20" y="24" width="24" height="20" rx="3" fill="%23fff"/></svg>')


def tk(n):
    n = int(round(n)); s = str(abs(n))
    if len(s) > 3:
        h, t = s[:-3], s[-3:]; p = []
        while len(h) > 2: p.insert(0, h[-2:]); h = h[:-2]
        if h: p.insert(0, h)
        s = ','.join(p) + ',' + t
    return '৳' + ('-' if n < 0 else '') + s



def _topprod():
    return ''.join(
        f'<tr><td><span class="rank {"t"+str(i) if i<4 else ""}">{i}</span>{n}</td>'
        f'<td class="r mut">{u}</td><td class="r"><b>{tk(v)}</b></td></tr>'
        for i, (n, u, v) in enumerate(TOP_PROD, 1))


def _stock():
    tone = {'critical': 'bad', 'low': 'due', 'ok': 'ok'}
    return ''.join(
        f'<tr><td>{n}</td><td class="r"><span class="pill {tone[st]}">{q} kg</span></td>'
        f'<td class="r mut">{r} kg</td></tr>'
        for n, q, r, st in STOCK if st != 'ok')


# ══════════════════════════════════════════════════════════════════════════
#  SHELL
# ══════════════════════════════════════════════════════════════════════════
NAV = [
    ('Overview', [('dashboard', 'Dashboard', 'dash', '')]),
    ('Sales',    [('sales', 'Orders', 'clipboard', ''),
                  ('customers', 'Customers', 'users', str(len(CUST)))]),
    ('Catalogue', [('products', 'Products', 'tag', str(len(PRODUCTS)))]),
    ('Finance',  [('dues', 'Dues', 'alert', ''),
                  ('accounts', 'Accounts', 'money', ''),
                  ('reports', 'Reports', 'report', '')]),
    ('System',   [('settings', 'Settings', 'gear', '')]),
]


def rail():
    out = []
    for group, items in NAV:
        out.append(f'<div class="navgrp">{group}</div><nav class="nav">')
        for hid, label, icon, badge in items:
            b = f'<span class="nbadge">{badge}</span>' if badge else ''
            out.append(f'<a href="#{hid}"><span class="ic">{IC[icon]}</span>'
                       f'<span>{label}</span>{b}</a>')
        out.append('</nav>')
    return (
      '<aside class="rail">'
      f'<div class="brandrow"><div class="mark">{IC["leaf"]}</div>'
      '<div><div class="bn">Shada BMS</div><div class="bs">Business Management</div></div></div>'
      + ''.join(out) +
      '<div class="railfoot"><div class="who"><div class="av">A</div>'
      '<div><div class="wn">Anowar Hossain</div><div class="wr">Owner · full access</div></div></div></div>'
      '</aside>')


def topbar():
    return (
      '<header class="top">'
      '<div class="crumb" id="crumb">Overview <span style="color:var(--ink-4)">/</span> <b>Dashboard</b></div>'
      '<div class="gsearch cbx">' + IC['search'] +
      '<input id="gs" type="search" autocomplete="off" placeholder="Search customer, phone or invoice" '
      'aria-label="Global search"><span class="kbd">⌘K</span>'
      '<div class="cbxlist" id="gsList" role="listbox"></div></div>'
      '<div id="notifWrap" style="position:relative">'
      f'<button class="iconbtn" id="bell" aria-label="Notifications" aria-haspopup="true">'
      f'{IC["bell"]}<span class="dot-n"></span></button>'
      '<div class="notif" id="notifPanel">'
      '<div class="nh">Needs attention <span class="pill bad" id="notifCount">0</span></div>'
      '<div id="notifList"></div>'
      '<div class="nf">Built from the ledger. Nothing here is typed by hand.</div>'
      '</div></div>'
      f'<a class="btn btn-p" href="#sales-entry">{IC["plus"]}New sale</a>'
      '</header>')


# The demo banner is off. Flip SHOW_DEMO_BANNER back to True if the prototype
# ever goes to anyone who has not been told the numbers are samples.
SHOW_DEMO_BANNER = False
DEMO = ('<div class="demo">' + IC['alert'] +
        '<span><b>Demo data.</b> Layout and behaviour are real. Numbers are sample figures '
        'until your spreadsheet is imported.</span></div>') if SHOW_DEMO_BANNER else ''


def ph(title, sub, actions=''):
    return (f'<div class="ph"><div><h1>{title}</h1><p>{sub}</p></div>'
            f'<div class="phact">{actions}</div></div>')


# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · dashboard
# ══════════════════════════════════════════════════════════════════════════
def kpi(i, label, icon, sub=''):
    return (f'<div class="kpi"><div class="kl">{IC[icon]}{label}</div>'
            f'<div class="kv" data-kpi="{i}">—</div>'
            f'<div class="d fl" data-delta="{i}">{sub}</div></div>')


def dashboard():
    seg = ''.join(f'<button data-period="{k}" aria-pressed="false">{v}</button>' for k, v in
                  [('today', 'Today'), ('week', 'This week'), ('month', 'This month'),
                   ('year', 'This year'), ('custom', 'Custom')])
    return f'''{DEMO}
{ph('Dashboard', '<span id="periodSub">September 2026</span>',
    f'<div class="seg">{seg}</div><button class="btn" data-soon="Excel and PDF export are Phase 7. The data behind this screen is already live.">{IC["report"]}Export</button>')}

<div class="kpis">
  {kpi(0,'Sales','money','')}{kpi(1,'Collection','check','')}{kpi(2,'Total due','alert','')}
  {kpi(3,'Pending orders','cart','')}{kpi(4,'Stock alerts','stock','')}
</div>

<div style="height:16px"></div>

<div class="g13 gdash">
  <div>
  <div class="card">
    <div class="ch"><h3 id="chartTitle">Sales by day, September</h3>
      <div class="sp" id="chartSum"></div></div>
    <div class="cb">
      <div class="legend" id="chartLegend"><span><i class="lg1"></i>This period</span><span><i class="lg2"></i>Previous period</span><span class="mut" style="margin-left:auto">Hover or tap a point</span></div>
      <div class="chartbox" id="chartBox"></div></div>
  </div>
  <div style="height:16px"></div>
  <div class="card">
    <div class="ch"><h3>Top products</h3>
      <span class="sub">Ranked nightly, so the dashboard reads ten rows instead of scanning sales</span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Product</th><th class="r">Units</th><th class="r">Revenue</th></tr></thead>
      <tbody>{_topprod()}</tbody></table></div></div>
  </div>
  </div>
  <div>
  <div class="card">
    <div class="ch"><h3>Top customers</h3><div class="sp"><a class="btn btn-xs" href="#customers">See all</a></div></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Customer</th><th class="r">Lifetime</th><th class="r">Due</th></tr></thead>
      <tbody id="topCust"></tbody></table></div></div>
  </div>
  <div style="height:16px"></div>
  <div class="card">
    <div class="ch"><h3>Stock alerts</h3><span class="sub">At or below reorder level</span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Product</th><th class="r">In stock</th><th class="r">Reorder at</th></tr></thead>
      <tbody>{_stock()}</tbody></table></div></div>
  </div>
  </div>
</div>

<div style="height:16px"></div>

<div class="card">
  <div class="ch"><h3>Pending orders</h3>
    <span class="sub">Website orders land here automatically. No second entry.</span>
    <div class="sp"><a class="btn btn-xs btn-p" href="#sales-entry">{IC['plus']}New sale</a></div></div>
  <div class="cb flush"><div class="tw"><table>
    <thead><tr><th>Invoice</th><th>Customer</th><th class="r">Items</th><th class="r">Amount</th><th class="r">Source</th></tr></thead>
    <tbody id="pendBody"></tbody></table></div></div>
</div>

<div style="height:16px"></div>

<div class="g3">
  <div class="card">
    <div class="ch"><h3>Quiet 30 to 59 days</h3><span class="sub" id="lap30Count"></span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Customer</th><th class="r">Silent</th><th class="r">Lifetime</th><th class="r">Act</th></tr></thead>
      <tbody id="lap30"></tbody></table></div></div>
  </div>
  <div class="card">
    <div class="ch"><h3>Quiet 60 to 89 days</h3><span class="sub" id="lap60Count"></span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Customer</th><th class="r">Silent</th><th class="r">Lifetime</th><th class="r">Act</th></tr></thead>
      <tbody id="lap60"></tbody></table></div></div>
  </div>
  <div class="card">
    <div class="ch"><h3>No purchase in 90+ days</h3><span class="sub" id="lap90Count"></span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Customer</th><th class="r">Silent</th><th class="r">Lifetime</th><th class="r">Act</th></tr></thead>
      <tbody id="lap90"></tbody></table></div></div>
  </div>
</div>'''


# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · sales entry
# ══════════════════════════════════════════════════════════════════════════
def sales_entry():
    tiers = ''.join(f'<button type="button" data-tier="{t}" aria-pressed="{str(t=="Wholesale").lower()}">{t}</button>'
                    for t in ('Wholesale', 'Re-wholesale', 'Retail'))
    return f'''{DEMO}
{ph('New sale', 'One entry. Invoice, dues, customer totals and stock move together.',
    f'<span class="meta">{IC["calendar"]} 26 Sep 2026 <i></i> {IC["note"]} <span class="mono" id="saleInv">INV-2609-0150</span></span>')}
<form id="saleForm" onsubmit="return false">
<div class="note edit" id="editBanner" hidden></div>
<div class="g13 gsale">
  <div>
    <div class="card">
      <div class="ch"><h3>Customer</h3><span class="sub">name, ID or phone</span>
        <div class="sp"><div class="seg sm">{tiers}</div></div></div>
      <div class="cb">
        <div class="fld cbx" style="margin-bottom:12px">
          <input class="inp lg" id="cbxInput" autocomplete="off" placeholder="Search customer" aria-label="Find customer">
          <div class="cbxlist" id="cbxList" role="listbox"></div>
        </div>
        <div id="cbxCard"></div>
      </div>
    </div>

    <div style="height:16px"></div>

    <div class="card lines-card">
      <div class="ch"><h3>Items</h3><span class="sub" id="sumQty">No items yet</span></div>
      <div class="cb flush"><div class="tw"><table class="lines">
        <thead><tr><th>Product</th><th>Qty</th><th>Rate</th><th class="r">Amount</th><th></th></tr></thead>
        <tbody id="lineBody"></tbody></table></div></div>
      <div class="cb addrow"><button class="btn btn-xs" id="addLine" type="button">{IC['plus']}Add item</button>
        <span class="hint" style="margin:0">Enter on a quantity adds the next item</span></div>
    </div>
  </div>

  <div>
    <div class="card">
      <div class="ch"><h3>Payment</h3></div>
      <div class="cb">
        <div class="grid2">
          <div class="fld" id="paidWrap"><label for="salePaid">Paid now</label>
            <div class="money"><span class="cur">৳</span><input class="inp num" id="salePaid" value="0" inputmode="numeric"></div></div>
          <div class="fld"><label>Method</label>{method_picker('salePayMethod')}</div>
        </div>
        <div class="grid2">
          <div class="fld" id="discWrap" hidden><label for="saleDisc">Discount</label>
            <div class="money"><span class="cur">৳</span><input class="inp num" id="saleDisc" value="0" inputmode="numeric"></div></div>
          <div class="fld" id="delWrap" hidden><label for="saleDeliv">Delivery charge</label>
            <div class="money"><span class="cur">৳</span><input class="inp num" id="saleDeliv" value="0" inputmode="numeric"></div></div>
        </div>
        <div class="fld" id="couponWrap" hidden><label for="saleCoupon">Coupon code</label>
          <div class="cpn"><input class="inp mono" id="saleCoupon" placeholder="Type a code, press Enter" autocomplete="off" autocapitalize="characters" spellcheck="false">
            <button class="btn" id="couponApply" type="button">Apply</button></div>
          <div class="hint" id="couponMsg">Codes are created in WooCommerce. The same code works on the website and here.</div></div>
        <div class="links"><button type="button" class="lnk" id="showDisc">{IC['plus']}Discount</button>
          <button type="button" class="lnk" id="showDel">{IC['plus']}Delivery charge</button>
          <button type="button" class="lnk" id="showCoupon">{IC['ticket']}Coupon</button></div>
        <div class="fld" style="margin-top:12px"><label for="saleNote">Note <span class="mut">optional</span></label>
          <input class="inp" id="saleNote" placeholder="Courier, colour of jar lids, anything the invoice should say"></div>
        <div class="hr" style="margin:14px 0"></div>
        <table class="sum">
          <tr><td>Subtotal</td><td class="r" id="sumSub">৳0</td></tr>
          <tr id="rowDisc" hidden><td id="rowDiscLbl">Discount</td><td class="r" id="sumDisc">-৳0</td></tr>
          <tr id="rowDel" hidden><td>Delivery</td><td class="r" id="sumDel">৳0</td></tr>
          <tr class="tot"><td>Total</td><td class="r" id="sumTotal">৳0</td></tr>
        </table>
        <div style="height:12px"></div>
        <div class="kpi" id="sumBalWrap">
          <div class="kl">{IC['alert']}Balance after this sale</div>
          <div class="kv" id="sumBal">৳0</div>
          <div class="d fl" id="sumNote">Paid in full. Nothing owing</div>
        </div>
        <div style="height:16px"></div>
        <button class="btn btn-p btn-lg" id="saveBtn" type="button" style="width:100%">{IC['check']}Save sale</button>
        <button class="lnk" id="resetBtn" type="button" style="margin:12px auto 0;display:flex;color:var(--ink-3)">{IC['x']}Discard draft</button>
      </div>
    </div>
  </div>
</div>
</form>'''


# Expenses are their own ledger. Collections never appear here: they are read
# off the customer payment rows so the books and the profiles cannot drift.
EXPENSES = [
 ('26 Sep 2026', 'Courier',   'Sundarban Courier, September',  8400, 'Bank'),
 ('24 Sep 2026', 'Raw material', 'Maize flour, 200kg',        46000, 'Bank'),
 ('22 Sep 2026', 'Packaging', 'Jar and label printing',       18700, 'Cash'),
 ('18 Sep 2026', 'Salary',    'Factory wages, first half',    96000, 'Bank'),
 ('12 Sep 2026', 'Utilities', 'Electricity, Bhaluka unit',    14200, 'Cash'),
 ('05 Sep 2026', 'Raw material', 'Soya protein, 120kg',       31800, 'Bank'),
 ('28 Aug 2026', 'Marketing', 'Facebook boost, August',        9500, 'Cash'),
]
PAYABLE = [('Maize supplier, Bhaluka', 86000, '12 days'),
           ('Jar supplier, Dhaka',     34500, '5 days'),
           ('Courier account',          8400, 'due today')]


DFILTERS = [('all', 'All'), ('30', 'Over 30 days'), ('60', 'Over 60 days'), ('whole', 'Wholesale')]


def dues():
    filters = ''.join(f'<button data-df="{k}" aria-pressed="{str(k=="all").lower()}">{v}</button>' for k, v in DFILTERS)
    return f'''{ph('Dues', 'Who owes you, how much, since when. Collect from this screen; every other number follows.',
        f'<button class="btn btn-p" id="duCollect" type="button">{IC["plus"]}New payment</button>')}
<div class="kpis">
  <div class="kpi due"><div class="kl">{IC['alert']}Total due</div><div class="kv" id="duTotal">—</div>
    <div class="d fl" id="duTotalSub">—</div></div>
  <div class="kpi"><div class="kl">{IC['time']}Over 30 days</div><div class="kv" id="duOld">—</div>
    <div class="d fl" id="duOldSub">—</div></div>
  <div class="kpi"><div class="kl">{IC['check']}Collected this month</div><div class="kv" id="duColl">—</div>
    <div class="d up" id="duCollSub">—</div></div>
  <div class="kpi"><div class="kl">{IC['chart']}Collection rate</div><div class="kv" id="duRate">—</div>
    <div class="d fl" id="duRateSub">paid ÷ sold, all time</div></div>
</div>
<div style="height:16px"></div>
<div class="card">
  <div class="ch"><h3>Customers with a balance</h3><span class="sub" id="duScope">largest first</span>
    <div class="sp"><div class="seg">{filters}</div></div></div>
  <div class="cb flush"><div class="tw"><table id="duTable">
    <thead><tr><th>Customer</th><th>Oldest unpaid</th><th class="r">Sold</th><th class="r">Paid</th>
      <th style="min-width:180px">Progress</th><th class="r">Due</th><th class="r">Act</th></tr></thead>
    <tbody id="duBody"></tbody></table></div></div>
</div>
<div style="height:16px"></div>
<div class="note">Due = sold − paid, computed from the same rows as the Dashboard, Orders and Accounts.
Recording a collection here settles the oldest invoice first and moves every screen at once.</div>'''


def accounts():
    seg = ''.join(f'<button data-acper="{k}" aria-pressed="false">{v}</button>' for k, v in
                  [('today', 'Today'), ('week', 'This week'), ('month', 'This month'),
                   ('year', 'This year'), ('custom', 'Custom')])
    return f'''{ph('Accounts', '<span id="acSub">September 2026</span>',
        f'<div class="seg">{seg}</div>'
        f'<button class="btn" id="acExpense" type="button">{IC["plus"]}Record expense</button>'
        f'<button class="btn btn-p" id="acCollect" type="button">{IC["plus"]}New payment</button>')}
<div class="kpis">
  <div class="kpi"><div class="kl">{IC['money']}Cash in hand</div><div class="kv" id="acCash">—</div>
    <div class="d up" id="acCashD">—</div></div>
  <div class="kpi"><div class="kl">{IC['money']}Bank balance</div><div class="kv" id="acBank">—</div>
    <div class="d fl" id="acBankD">—</div></div>
  <div class="kpi"><div class="kl">{IC['check']}Collected</div><div class="kv" id="acColl">—</div>
    <div class="d up" id="acCollD">—</div></div>
  <div class="kpi"><div class="kl">{IC['down']}Expense</div><div class="kv" id="acExp">—</div>
    <div class="d fl" id="acExpD">—</div></div>
  <div class="kpi due"><div class="kl">{IC['alert']}Receivable</div><div class="kv" id="acRecv">—</div>
    <div class="d fl" id="acRecvD">—</div></div>
  <div class="kpi"><div class="kl">{IC['cart']}Payable</div><div class="kv" id="acPay">—</div>
    <div class="d fl" id="acPayD">—</div></div>
</div>
<div style="height:16px"></div>
<div class="g13">
  <div class="card">
    <div class="ch"><h3>Transactions</h3><span class="sub">collections and expenses, newest first</span>
      <div class="sp"><span class="sub" id="acCount">—</span></div></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Date</th><th>Kind</th><th>Detail</th><th class="r">Amount</th>
        <th class="r">Account</th></tr></thead>
      <tbody id="acBody"></tbody></table></div></div>
  </div>
  <div class="card">
    <div class="ch"><h3>Payable</h3><span class="sub">what we owe</span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Supplier</th><th class="r">Amount</th><th class="r">Due in</th></tr></thead>
      <tbody id="acPayBody"></tbody></table></div></div>
  </div>
</div>
<div style="height:16px"></div>
<div class="note">Receivable is not a separate number. It is the same
<b>total sold minus total paid</b> the dashboard and every customer profile use. Recording a
collection here reduces that customer\u2019s due in the same write, so the books can never
disagree with the dashboard.</div>'''



# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · sales list  (every invoice, newest first; a saved sale lands here)
# ══════════════════════════════════════════════════════════════════════════
def sales_list():
    seg = ''.join(f'<button data-sf="{k}" aria-pressed="{str(k=="all").lower()}">{v}</button>' for k, v in
                  [('all', 'All'), ('pending', 'Pending'), ('due', 'With due'), ('paid', 'Paid'), ('web', 'From website')])
    return f'''{DEMO}
{ph('Orders', 'Every sale, website or counter, newest first. Click a row to open it.',
    f'<a class="btn btn-p" href="#sales-entry">{IC["plus"]}New sale</a>')}
<div class="kpis">
  <div class="kpi"><div class="kl">{IC['money']}Sales this month</div><div class="kv" id="slMonth">—</div>
    <div class="d fl" id="slMonthSub">—</div></div>
  <div class="kpi"><div class="kl">{IC['clipboard']}Orders</div><div class="kv" id="slCount">—</div>
    <div class="d fl">all time</div></div>
  <div class="kpi"><div class="kl">{IC['cart']}Average order</div><div class="kv" id="slAvg">—</div>
    <div class="d fl">across every invoice</div></div>
  <div class="kpi due"><div class="kl">{IC['alert']}Unpaid orders</div><div class="kv" id="slUnpaid">—</div>
    <div class="d fl" id="slUnpaidSub">—</div></div>
</div>
<div style="height:16px"></div>
<div class="card">
  <div class="ch">
    <div class="gsearch" style="margin:0;width:280px;max-width:100%">{IC['search']}
      <input id="slSearch" type="search" placeholder="Invoice, customer or phone" aria-label="Filter sales"></div>
    <div class="sp"><div class="seg">{seg}</div><span class="sub" id="slScope"></span></div>
  </div>
  <div class="cb flush"><div class="tw"><table>
    <thead><tr><th>Date</th><th>Invoice</th><th>Customer</th><th class="r">Items</th><th class="r">Total</th>
      <th class="r">Paid</th><th class="r">Due</th><th>Method</th><th>Source</th><th>Status</th><th></th></tr></thead>
    <tbody id="slBody"></tbody></table></div>
    <div id="slNone" hidden><div class="none"><b>No order matches.</b>Clear the filter, or record a sale.</div></div>
  </div>
</div>'''


# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · one invoice  (same shape as New sale, read-only, with its actions)
# ══════════════════════════════════════════════════════════════════════════
def sale_detail():
    return f'''<div class="hero">
  <div class="hav" style="font-size:18px;border-radius:10px">{IC['note']}</div>
  <div style="min-width:0;flex:1">
    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
      <div style="font-size:21px;font-weight:700;letter-spacing:-.4px" class="mono" id="sdInv">INV</div>
      <span id="sdStatus"></span><span id="sdSrc"></span></div>
    <div class="hmeta" id="sdMeta"></div>
  </div>
  <div class="phact">
    <a class="btn" href="#sales">{IC['clipboard']}All orders</a>
    <button class="btn" id="sdEdit" type="button">{IC['pencil']}Edit order</button>
    <button class="btn" id="sdRepeat" type="button">{IC['sale']}Repeat order</button>
    <button class="btn" id="sdDeliver" type="button">{IC['truck']}Mark delivered</button>
    <button class="btn" data-soon="Prints the invoice, A5 or 80 mm thermal, with the company header from Settings. Phase 4.">{IC['report']}Print</button>
    <button class="btn btn-p" id="sdCollect" type="button">{IC['money']}Record payment</button>
  </div>
</div>
<div style="height:16px"></div>
<div class="g13">
  <div>
    <div class="card">
      <div class="ch"><h3>Customer</h3><div class="sp"><a class="btn btn-xs" id="sdProfile" href="#customer-profile">{IC['users']}Open profile</a></div></div>
      <div class="cb" id="sdCust"></div>
    </div>
    <div style="height:16px"></div>
    <div class="card">
      <div class="ch"><h3>Items</h3><span class="sub" id="sdQty"></span></div>
      <div class="cb flush"><div class="tw"><table>
        <thead><tr><th>Product</th><th class="r">Qty</th><th>Rate</th><th class="r">Amount</th></tr></thead>
        <tbody id="sdLines"></tbody></table></div></div>
      <div class="cb" id="sdNoteWrap" hidden><span class="mut">Note</span> <span id="sdNote"></span></div>
    </div>
  </div>
  <div>
    <div class="card">
      <div class="ch"><h3>Payment</h3><span class="sub" id="sdPayCount"></span></div>
      <div class="cb">
        <table class="sum">
          <tr><td>Subtotal</td><td class="r" id="sdSub">৳0</td></tr>
          <tr id="sdRowDisc" hidden><td id="sdDiscLbl">Discount</td><td class="r" id="sdDisc"></td></tr>
          <tr id="sdRowDel" hidden><td>Delivery</td><td class="r" id="sdDel"></td></tr>
          <tr class="tot"><td>Total</td><td class="r" id="sdTotal">৳0</td></tr>
          <tr><td>Paid</td><td class="r" id="sdPaid">৳0</td></tr>
        </table>
        <div style="height:12px"></div>
        <div class="kpi" id="sdDueWrap"><div class="kl">{IC['alert']}Balance on this invoice</div>
          <div class="kv" id="sdDue">৳0</div><div class="d fl" id="sdDueSub"></div></div>
      </div>
      <div class="cb flush" style="border-top:1px solid var(--line)"><div class="tw"><table>
        <thead><tr><th>Date</th><th>Method</th><th class="r">Amount</th></tr></thead>
        <tbody id="sdPayBody"></tbody></table></div></div>
    </div>
  </div>
</div>'''


# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · customers list
# ══════════════════════════════════════════════════════════════════════════
def customers_list():
    return f'''{DEMO}
{ph('Customers', 'Click any row to open the full profile.',
    f'<button class="btn" id="custAdd" type="button">{IC["plus"]}New customer</button>'
    f'<a class="btn btn-p" href="#sales-entry">{IC["plus"]}New sale</a>')}
<div class="kpis">
  <div class="kpi"><div class="kl">{IC['users']}Customers</div><div class="kv" id="cCount">—</div>
    <div class="d fl" id="cCountSub">active on the ledger</div></div>
  <div class="kpi"><div class="kl">{IC['money']}Lifetime sales</div><div class="kv" id="cSold">—</div>
    <div class="d fl">all customers, all time</div></div>
  <div class="kpi due"><div class="kl">{IC['alert']}Outstanding</div><div class="kv" id="cDue">—</div>
    <div class="d fl" id="cOwing">—</div></div>
  <div class="kpi"><div class="kl">{IC['cart']}Average order</div><div class="kv" id="cAvg">—</div>
    <div class="d fl">across every recorded order</div></div>
</div>
<div style="height:16px"></div>
<div class="g13 gcust">
<div class="card">
  <div class="ch">
    <select class="inp" id="custDistrict" aria-label="Filter by district"
      style="width:190px;height:36px;font-size:13px"></select>
    <div class="gsearch" style="margin:0;width:260px;max-width:100%">{IC['search']}
      <input id="custSearch" type="search" placeholder="Name, ID, phone or area"
        aria-label="Filter customers"></div>
    <button class="btn btn-xs" id="custClear" hidden>{IC['x']}Clear</button>
    <div class="sp"><span class="sub" id="cScope">All 12 customers</span></div>
  </div>
  <div class="cb flush"><div class="tw"><table>
    <thead><tr><th>ID</th><th>Customer</th><th>Phone</th><th>District</th><th>Tier</th>
      <th class="r">Orders</th><th class="r">Lifetime</th><th class="r">Due</th>
      <th class="r">Last order</th><th></th></tr></thead>
    <tbody id="custBody"></tbody></table></div>
    <div id="custNone" hidden><div class="none"><b>Nobody matches that.</b>
      Clear the filter, or add the customer from the sale screen.</div></div>
  </div>
</div>
<div class="card">
  <div class="ch"><h3>By district</h3><span class="sub">Click one to filter</span></div>
  <div class="cb flush"><div class="tw"><table>
    <thead><tr><th>District</th><th class="r">Customers</th><th class="r">Lifetime</th>
      <th class="r">Due</th><th></th></tr></thead>
    <tbody id="distBody"></tbody></table></div></div>
</div>
</div>'''


# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · profile + timeline
# ══════════════════════════════════════════════════════════════════════════
def customer_profile():
    return f'''{DEMO}
<div class="hbanner" id="pBanner" hidden><img alt=""></div>
<div class="hero">
  <div class="hav" id="pAv">S</div>
  <div style="min-width:0;flex:1">
    <div style="font-size:21px;font-weight:700;letter-spacing:-.4px" id="pName">—</div>
    <div class="hmeta" id="pMeta"></div>
    <div class="htags" id="pTags"></div>
  </div>
  <div class="phact">
    <button class="btn" id="pfEdit" type="button">{IC['pencil']}Edit</button>
    <a class="btn" href="#customer-timeline" id="tlBtn">{IC['time']}Timeline</a>
    <button class="btn" data-soon="Opens WhatsApp on this customer\u2019s number and logs the contact against their record.">{IC['wa']}WhatsApp</button>
    <button class="btn" id="pfPay" type="button">{IC['money']}New payment</button>
    <a class="btn btn-p" href="#sales-entry">{IC['plus']}New sale</a>
  </div>
</div>
<div style="height:16px"></div>
<div class="kpis">
  <div class="kpi"><div class="kl">{IC['money']}Lifetime sales</div><div class="kv" id="pLtv">—</div>
    <div class="d fl" id="pAvg">—</div></div>
  <div class="kpi"><div class="kl">{IC['check']}Paid</div><div class="kv" id="pPaid">—</div>
    <div class="d up" id="pPaidPct">—</div></div>
  <div class="kpi" id="pDueCard"><div class="kl">{IC['alert']}Outstanding</div><div class="kv" id="pDue">—</div>
    <div class="d fl" id="pDueSub">—</div></div>
  <div class="kpi"><div class="kl">{IC['cart']}Orders</div><div class="kv" id="pOrders">—</div>
    <div class="d fl">last on <span id="pLast">—</span></div></div>
  <div class="kpi"><div class="kl">{IC['up']}Rank</div><div class="kv" id="pRank">—</div>
    <div class="d fl" id="pRankSub">—</div></div>
</div>
<div style="height:16px"></div>
<div class="g13">
  <div class="card">
    <div class="ch"><h3>Order history</h3><span class="sub">Newest first</span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Date</th><th>Invoice</th><th class="r">Items</th><th class="r">Total</th>
        <th class="r">Paid</th><th class="r">Balance</th></tr></thead>
      <tbody id="pOrderBody"></tbody></table></div></div>
  </div>
  <div>
    <div class="card">
      <div class="ch"><h3>Payments</h3><span class="sub" id="pPaySub">every receipt, newest first</span>
        <div class="sp"><button class="btn btn-xs" id="pfPay2" type="button">{IC['plus']}Add payment</button></div></div>
      <div class="cb flush"><div class="tw"><table>
        <thead><tr><th>Date</th><th>Method</th><th>Against</th><th class="r">Amount</th></tr></thead>
        <tbody id="pPayBody"></tbody></table></div></div>
    </div>
    <div style="height:16px"></div>
    <div class="card">
      <div class="ch"><h3>Money check</h3><span class="sub">due = sold − paid</span></div>
      <div class="cb">
        <table style="font-size:13px">
          <tr><td style="padding:6px 0;border:0">Total sold</td><td class="r" style="padding:6px 0;border:0" id="dSold">—</td></tr>
          <tr><td style="padding:6px 0;border:0">Total paid</td><td class="r" style="padding:6px 0;border:0" id="dPaid">—</td></tr>
          <tr><td style="padding:9px 0 0;border:0;font-weight:700">Due</td>
              <td class="r" style="padding:9px 0 0;border:0;font-weight:700" id="dDue">—</td></tr>
        </table>
        <div class="hint" style="margin-top:9px">Computed in one place, never stored twice.
          The same rule runs on the live database.</div>
      </div>
    </div>
  </div>
</div>'''


def customer_timeline():
    return f'''{DEMO}
{ph('Activity timeline', 'Every order, due and payment for <b id="tlName">this customer</b>, newest first.',
    f'<a class="btn" href="#customer-profile">{IC["cust"]}Back to profile</a>')}
<div class="card">
  <div class="ch"><h3 id="tlHead">—</h3><div class="sp"><span class="sub" id="tlMeta"></span></div></div>
  <div class="cb"><div class="tl" id="tlBody"></div></div>
</div>'''


# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · products + product detail
# ══════════════════════════════════════════════════════════════════════════
PPERIODS = [('month', 'This month'), ('last', 'Last month'), ('year', 'This year'), ('all', 'All time')]
PFILTERS = [('all', 'All'), ('below', 'Below reorder'), ('archived', 'Archived')]


def products():
    periods = ''.join(f'<button data-pp="{k}" aria-pressed="{str(k=="year").lower()}">{v}</button>' for k, v in PPERIODS)
    filters = ''.join(f'<button data-pf="{k}" aria-pressed="{str(k=="all").lower()}">{v}</button>' for k, v in PFILTERS)
    return f'''{ph('Products', 'Every pack: stock, prices, SKU and who buys it. Ranked by sales in the period you pick.',
        f'<button class="btn" id="invStockIn" type="button">{IC["stock"]}Stock in</button>'
        f'<button class="btn" id="invBatch" type="button">{IC["leaf"]}New production batch</button>'
        f'<button class="btn btn-p" id="prodAdd" type="button">{IC["plus"]}New product</button>')}
<div class="kpis">
  <div class="kpi"><div class="kl">{IC['tag']}Packs on sale</div><div class="kv" id="pgSku">—</div>
    <div class="d fl" id="pgSkuSub">across six formulas</div></div>
  <div class="kpi"><div class="kl">{IC['stock']}Units sold</div><div class="kv" id="pgUnits">—</div>
    <div class="d fl" id="pgUnitsSub">every recorded sale line</div></div>
  <div class="kpi"><div class="kl">{IC['money']}Product revenue</div><div class="kv" id="pgRev">—</div>
    <div class="d fl">ties to total sales, by construction</div></div>
  <div class="kpi"><div class="kl">{IC['up']}Best seller</div>
    <div class="kv" id="pgTop" style="font-size:16px;letter-spacing:-.2px">—</div>
    <div class="d up" id="pgTopSub">—</div></div>
  <div class="kpi" id="pgAlertWrap"><div class="kl">{IC['alert']}Stock alerts</div><div class="kv" id="pgAlerts">—</div>
    <div class="d fl" id="pgAlertsSub">—</div></div>
</div>
<div style="height:16px"></div>
<div class="fbar"><div class="seg">{periods}</div><span class="sub" id="pgScope"></span><div class="seg" style="margin-left:auto">{filters}</div></div>
<div style="height:12px"></div>
<div class="pgrid" id="prodGrid"></div>
<div style="height:16px"></div>
<div class="g2">
  <div class="card" id="invRaw">
    <div class="ch"><h3>Raw material</h3><span class="sub">what a production batch consumes</span>
      <div class="sp"><span class="sub" id="invRawCount">—</span></div></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Material</th><th class="r">Unit</th><th class="r">Stock</th>
        <th class="r">Reorder</th><th class="r">Status</th></tr></thead>
      <tbody id="invRawBody"></tbody></table></div></div>
  </div>
  <div class="card">
    <div class="ch"><h3>Stock movements</h3><span class="sub">every in and out, newest first</span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Date</th><th>Type</th><th>Product</th><th class="r">Qty</th><th>Reference</th></tr></thead>
      <tbody id="invMovBody"></tbody></table></div></div>
  </div>
</div>
<div style="height:16px"></div>
<div class="note">Units and revenue are read off the sale lines, never stored on the product.
Record a sale and this screen moves in the same breath, which is why a product report and a
customer report can never disagree.</div>'''


def product_detail():
    return f'''<div class="hero">
  <span class="hpic"><img id="pdImg" alt="" width="84" height="84"></span>
  <div style="min-width:0;flex:1">
    <div style="font-size:21px;font-weight:700;letter-spacing:-.4px" id="pdName">—</div>
    <div class="hmeta" id="pdMeta"></div>
  </div>
  <div class="phact">
    <a class="btn" href="#products">{IC['cart']}All products</a>
    <button class="btn" id="pdEdit" type="button">{IC['tag']}Edit product</button>
    <button class="btn" id="pdStockIn" type="button" data-stockin="0">{IC['stock']}Stock in</button>
    <a class="btn btn-p" href="#sales-entry">{IC['plus']}Sell this</a>
  </div>
</div>
<div style="height:16px"></div>
<div class="kpis">
  <div class="kpi"><div class="kl">{IC['money']}Revenue</div><div class="kv" id="pdRev">—</div>
    <div class="d fl">all recorded sale lines</div></div>
  <div class="kpi"><div class="kl">{IC['stock']}Units sold</div><div class="kv" id="pdUnits">—</div>
    <div class="d fl">across every order</div></div>
  <div class="kpi"><div class="kl">{IC['cart']}Orders</div><div class="kv" id="pdOrders">—</div>
    <div class="d fl">avg line <span id="pdAvg">—</span></div></div>
  <div class="kpi"><div class="kl">{IC['users']}Buyers</div><div class="kv" id="pdBuyers">—</div>
    <div class="d fl">customers who bought it</div></div>
  <div class="kpi" id="pdStockCard"><div class="kl">{IC['alert']}Stock</div>
    <div class="kv" id="pdStock" style="font-size:19px">—</div>
    <div class="d fl" id="pdStockSub">—</div></div>
</div>
<div style="height:16px"></div>
<div class="card">
  <div class="ch"><h3>Sales by month</h3><span class="sub" id="pdMonSub">last twelve months, units and revenue</span></div>
  <div class="cb"><div class="mchart" id="pdMonths"></div></div>
</div>
<div style="height:16px"></div>
<div class="g13">
  <div class="card">
    <div class="ch"><h3>Who buys it</h3><span class="sub">ranked by value. Click a row for the profile</span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Customer</th><th>District</th><th class="r">Orders</th><th class="r">Units</th>
        <th class="r">Value</th><th></th></tr></thead>
      <tbody id="pdBuyerBody"></tbody></table></div></div>
  </div>
  <div>
  <div class="card">
    <div class="ch"><h3>By district</h3><span class="sub">where this pack sells</span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>District</th><th class="r">Units</th><th class="r">Value</th></tr></thead>
      <tbody id="pdDistBody"></tbody></table></div></div>
  </div>
  <div style="height:16px"></div>
  <div class="card">
    <div class="ch"><h3>Stock movements</h3><span class="sub">in and out, newest first</span></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Date</th><th>Type</th><th class="r">Qty</th><th>Reference</th></tr></thead>
      <tbody id="pdMovBody"></tbody></table></div></div>
  </div>
  </div>
</div>
<div style="height:16px"></div>
<div class="card">
  <div class="ch"><h3>Every order containing this pack</h3><span class="sub">newest first</span></div>
  <div class="cb flush"><div class="tw"><table>
    <thead><tr><th>Date</th><th>Invoice</th><th>Customer</th><th class="r">Qty</th>
      <th>Rate</th><th class="r">Line total</th><th class="r">Source</th></tr></thead>
    <tbody id="pdOrderBody"></tbody></table></div></div>
</div>'''



# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · inventory   (client Stage 1.4)
# ══════════════════════════════════════════════════════════════════════════
RAW = [('Maize flour', 'kg', 420, 150), ('Soya protein', 'kg', 95, 120),
       ('Calcium carbonate', 'kg', 210, 80), ('Spirulina powder', 'kg', 18, 25),
       ('Moringa leaf powder', 'kg', 64, 40), ('Beetroot powder', 'kg', 52, 40)]
FIN = [('Nutricare Hand Feeding', '1kg', 18, 40), ('Nutricare Hand Feeding', '500g', 96, 40),
       ('Avian Eggfood', '1kg', 54, 30), ('Avian Eggfood', '500g', 7, 30),
       ('Avian Spirulina', '200g', 24, 25), ('Avian Herbs', '200g', 51, 25),
       ('Avian Moringa', '200g', 62, 25), ('Avian Beetroot', '200g', 73, 25)]
MOV = [('26 Sep', 'Out', 'Nutricare 1kg', -6, 'INV-2609-0148'),
       ('26 Sep', 'Out', 'Avian Eggfood 500g', -12, 'INV-2609-0148'),
       ('25 Sep', 'In', 'Nutricare 1kg', 120, 'Production batch B-0912'),
       ('24 Sep', 'Out', 'Avian Spirulina 200g', -4, 'INV-2609-0141'),
       ('23 Sep', 'In', 'Avian Eggfood 500g', 80, 'Production batch B-0908')]

ITABS = [('all', 'All'), ('raw', 'Raw material'), ('fin', 'Finished product'),
         ('below', 'Below reorder'), ('mov', 'Movements')]


def inventory():
    tabs = ''.join(f'<button data-inv="{k}" aria-pressed="{str(k=="all").lower()}">{v}</button>'
                   for k, v in ITABS)
    return f'''{ph('Inventory',
        'Raw material, finished product, current stock and alerts. Stock moves when a sale is saved, never by hand.',
        f'<button class="btn" id="invStockIn" type="button">{IC["plus"]}Stock in</button>'
        f'<button class="btn btn-p" id="invBatch" type="button">{IC["plus"]}New production batch</button>')}
<div class="seg">{tabs}</div>
<div style="height:16px"></div>
<div class="kpis">
  <div class="kpi"><div class="kl">{IC['stock']}Units on the shelf</div>
    <div class="kv" id="invUnits">—</div><div class="d fl" id="invUnitsSub">—</div></div>
  <div class="kpi"><div class="kl">{IC['leaf']}Raw material value</div>
    <div class="kv">{tk(318900)}</div><div class="d fl">6 materials</div></div>
  <div class="kpi due"><div class="kl">{IC['alert']}Below reorder</div>
    <div class="kv" id="invBelow">—</div><div class="d fl" id="invCrit">—</div></div>
  <div class="kpi"><div class="kl">{IC['check']}Batches this month</div>
    <div class="kv">7</div><div class="d up">+2 on August</div></div>
</div>
<div style="height:16px"></div>
<div class="g2">
  <div class="card" id="invFin">
    <div class="ch"><h3>Finished product</h3><span class="sub">click a row for the product</span>
      <div class="sp"><span class="sub" id="invFinCount">—</span></div></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Product</th><th>Pack</th><th class="r">Stock</th><th class="r">Reorder</th>
        <th class="r">Status</th><th></th></tr></thead><tbody id="invFinBody"></tbody></table></div></div>
  </div>
  <div class="card" id="invRaw">
    <div class="ch"><h3>Raw material</h3><span class="sub">qty / reorder level</span>
      <div class="sp"><span class="sub" id="invRawCount">—</span></div></div>
    <div class="cb flush"><div class="tw"><table>
      <thead><tr><th>Material</th><th class="r">Unit</th><th class="r">Stock</th>
        <th class="r">Reorder</th><th class="r">Status</th></tr></thead>
      <tbody id="invRawBody"></tbody></table></div></div>
  </div>
</div>
<div style="height:16px"></div>
<div class="card" id="invMov">
  <div class="ch"><h3>Stock movements</h3>
    <span class="sub">append-only ledger, never edited in place</span></div>
  <div class="cb flush"><div class="tw"><table>
    <thead><tr><th>Date</th><th>Type</th><th>Item</th><th class="r">Qty</th>
      <th>Reference</th></tr></thead><tbody id="invMovBody"></tbody></table></div></div>
</div>
<div style="height:16px"></div>
<div class="note">Stock is an append-only ledger. Current stock is the running total, never a
number somebody typed, and the status pill is derived from stock against the reorder level.
That is what makes a stock figure auditable a year later.</div>'''



# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · settings   (client Stage 1.7 Admin + Stage 2.10 System Settings)
# ══════════════════════════════════════════════════════════════════════════
CFG = {
 'company': {'name': 'Shada Bird Feed', 'factory': 'Majorvita, Bhaluka, Mymensingh',
             'phone': '01813-323535', 'email': 'shadabirdfeed@gmail.com',
             'licence': '[CONFIRM]', 'bin': '[CONFIRM]'},
 'invoice': {'prefix': 'INV-', 'format': 'INV-YYMM-0000', 'next': '0149',
             'currency': 'BDT, lakh grouping', 'print': 'A5 and 80mm thermal',
             'lang': 'English and Bangla'},
 'pay':     {'cash': 'Enabled', 'bkash': '[CONFIRM]', 'nagad': '[CONFIRM]',
             'bank': '[CONFIRM]', 'cod': '[CONFIRM]'},
 'courier': {'sundarban': 'Default', 'counter': 'Enabled', 'own': 'Enabled',
             'lead': '2 working days', 'charge': '[CONFIRM]'},
 'bank':    {'acc1': '[CONFIRM]', 'acc2': '[CONFIRM]', 'branch': '[CONFIRM]',
             'routing': '[CONFIRM]'},
}
LOG = [
 ('26 Sep 14:25', 'Accounts staff', 'Recorded payment, Saddam', '\u2014', '৳12,480'),
 ('26 Sep 14:22', 'Sales staff', 'Created sale INV-2609-0148', '\u2014', '৳12,480'),
 ('26 Sep 11:04', 'Anowar Bhai', 'Changed unit price, Nutricare 1kg', '৳690', '৳680'),
 ('25 Sep 17:40', 'Factory', 'Production batch B-0912', '\u2014', '+120 units'),
 ('25 Sep 09:12', 'Anowar Bhai', 'Added customer, Imran', '\u2014', 'Mymensingh'),
 ('24 Sep 16:03', 'Accounts staff', 'Recorded expense, maize flour', '\u2014', '৳46,000'),
 ('23 Sep 10:47', 'Sales staff', 'Edited order INV-2609-0139', '3 items', '4 items'),
]
USERS = [('Anowar Bhai', 'Owner', 'All modules'),
         ('Accounts staff', 'Accountant', 'Accounts, Reports'),
         ('Sales staff', 'Sales', 'Sales entry, Customers'),
         ('Factory', 'Stock', 'Inventory only')]

STABS = [('company', 'Company', 'building'), ('invoice', 'Invoice', 'receipt'),
         ('pay', 'Payment methods', 'cash'), ('coupons', 'Coupons', 'ticket'),
         ('courier', 'Couriers', 'truck'), ('bank', 'Bank accounts', 'bank'),
         ('users', 'Users and roles', 'users'), ('log', 'Activity log', 'history'),
         ('backup', 'Backup', 'download')]

# mirrors WooCommerce → Marketing → Coupons. Codes are created there; the sale screen looks them up.
COUPONS = [
  {'code': 'DEALER5', 'type': 'percent',  'v': 5,   'min': 0,    'label': '5% off the subtotal',    'rule': 'Dealer tier',                'used': 41},
  {'code': 'EID100',  'type': 'fixed',    'v': 100, 'min': 2000, 'label': '৳100 off',             'rule': 'Subtotal ৳2,000 or more', 'used': 118},
  {'code': 'FREEDEL', 'type': 'delivery', 'v': 0,   'min': 0,    'label': 'Delivery charge waived', 'rule': 'Dhaka orders',               'used': 27},
]


def _fields(section, rows):
    out = []
    for key, label, hint in rows:
        h = f'<div class="hint">{hint}</div>' if hint else ''
        out.append(f'<div class="fld"><label for="cfg-{section}-{key}">{label}</label>'
                   f'<input class="inp" id="cfg-{section}-{key}" '
                   f'data-cfg="{section}.{key}" data-label="{label}">{h}</div>')
    return '<div class="grid2">' + ''.join(out) + '</div>'


def _panel(tab, title, sub, inner):
    return (f'<div data-spanel="{tab}" hidden><div class="card">'
            f'<div class="ch"><h3>{title}</h3><span class="sub">{sub}</span></div>'
            f'<div class="cb">{inner}</div></div></div>')


def settings():
    tabs = ''.join(f'<button data-stab="{k}" aria-pressed="{str(k=="company").lower()}">{IC[ic]}{v}</button>'
                   for k, v, ic in STABS)
    cpn_rows = ''.join(
        f'<tr><td><b class="mono">{c["code"]}</b></td><td>{c["type"].capitalize()}</td><td>{c["label"]}</td>'
        f'<td class="mut">{c["rule"]}</td><td class="r num">{c["used"]}</td>'
        f'<td><span class="pill web">WooCommerce</span></td></tr>' for c in COUPONS)
    coupons_panel = _panel('coupons', 'Coupons', 'created in WooCommerce, honoured on the sale screen',
        f'<div class="tw"><table><thead><tr><th>Code</th><th>Type</th><th>Value</th><th>Rule</th>'
        f'<th class="r">Used</th><th>Source</th></tr></thead><tbody>{cpn_rows}</tbody></table></div>'
        f'<div class="hint" style="margin-top:12px">One coupon engine, not two. Codes are created and edited in '
        f'WooCommerce → Marketing → Coupons; New sale looks a code up and applies the same rule, so a dealer '
        f'pays the same on the phone and on the website. Usage counts sync back with WebSync.</div>')
    users = ''.join(
        f'<tr><td><b>{n}</b></td><td>{r}</td><td class="mut">{p}</td>'
        f'<td class="r"><span class="pill ok">Active</span></td></tr>' for n, r, p in USERS)

    panels = (
      _panel('company', 'Company information', 'prints on every invoice and report',
             _fields('company', [
               ('name', 'Company name', ''), ('factory', 'Factory address', ''),
               ('phone', 'Phone', ''), ('email', 'Email', ''),
               ('licence', 'Trade licence', 'Blocked on the client'),
               ('bin', 'BIN', 'Blocked on the client')])) +
      _panel('invoice', 'Invoice settings', 'changing the format later means a migration',
             _fields('invoice', [
               ('prefix', 'Prefix', 'Try changing this, then Save'),
               ('format', 'Number format', 'Stored with a uniqueness constraint'),
               ('next', 'Next number', ''), ('currency', 'Currency', ''),
               ('print', 'Print size', ''), ('lang', 'Language', '')])) +
      _panel('pay', 'Payment methods', 'what the sale screen offers',
             _fields('pay', [
               ('cash', 'Cash', ''), ('bkash', 'bKash', 'Blocked on the client'),
               ('nagad', 'Nagad', 'Blocked on the client'),
               ('bank', 'Bank transfer', 'Blocked on the client'),
               ('cod', 'Cash on delivery', 'Blocked on the client')])) +
      coupons_panel +
      _panel('courier', 'Couriers and delivery', 'drives the delivery line on a sale',
             _fields('courier', [
               ('sundarban', 'Sundarban Courier', ''), ('counter', 'Counter pickup', ''),
               ('own', 'Own delivery', ''), ('lead', 'Standard lead time', ''),
               ('charge', 'Delivery charge', 'Blocked on the client')])) +
      _panel('bank', 'Bank accounts', 'collections marked Bank transfer post here',
             _fields('bank', [
               ('acc1', 'Account 1', 'Blocked on the client'),
               ('acc2', 'Account 2', 'Blocked on the client'),
               ('branch', 'Branch', 'Blocked on the client'),
               ('routing', 'Routing number', 'Blocked on the client')])) +
      f'<div data-spanel="users" hidden><div class="card">'
      f'<div class="ch"><h3>Users, roles and permissions</h3>'
      f'<span class="sub">built on WordPress roles and capabilities, not a parallel system</span></div>'
      f'<div class="cb flush"><div class="tw"><table>'
      f'<thead><tr><th>User</th><th>Role</th><th>Can access</th><th class="r">Status</th></tr></thead>'
      f'<tbody>{users}</tbody></table></div></div></div></div>'
      f'<div data-spanel="log" hidden><div class="card">'
      f'<div class="ch"><h3>Activity log</h3>'
      f'<span class="sub">who changed what, with the value before and after</span>'
      f'<div class="sp"><span class="sub" id="logCount">—</span></div></div>'
      f'<div class="cb flush"><div class="tw"><table>'
      f'<thead><tr><th>When</th><th>User</th><th>Action</th><th class="r">Before</th>'
      f'<th class="r">After</th></tr></thead><tbody id="logBody"></tbody></table></div></div></div></div>'
      f'<div data-spanel="backup" hidden><div class="card">'
      f'<div class="ch"><h3>Backup and restore</h3><span class="sub">20 tables, one file</span></div>'
      f'<div class="cb">'
      f'<div class="grid2">'
      f'<div class="kpi"><div class="kl">{IC["stock"]}Tables</div><div class="kv">20</div>'
      f'<div class="d fl">dedicated, none in wp_postmeta</div></div>'
      f'<div class="kpi"><div class="kl">{IC["time"]}Last backup</div><div class="kv">26 Sep</div>'
      f'<div class="d up">03:00, automatic</div></div></div>'
      f'<div style="height:13px"></div>'
      f'<div class="note">Backups run nightly to off-site storage and on demand from here. '
      f'A restore is a separate, deliberate action with a confirmation step, because a restore '
      f'that happens by accident is worse than no backup at all.</div></div></div></div>')

    return f'''{ph('Settings',
        'Company, invoice, payment methods, couriers, banks, users, roles, activity log and backup.',
        f'<span class="sub" id="setDirty" style="align-self:center">No unsaved changes</span>'
        f'<button class="btn" id="setBackup" type="button">{IC["report"]}Download backup</button>'
        f'<button class="btn btn-p" id="setSave" type="button">{IC["check"]}Save changes</button>')}
<div class="seg">{tabs}</div>
<div style="height:16px"></div>
{panels}'''



# ══════════════════════════════════════════════════════════════════════════
#  VIEWS · follow-ups  (client's Stage 2.2)
# ══════════════════════════════════════════════════════════════════════════
FOLLOW = [
 ('SBF-004','Rafiq','Chattogram','Due reminder','27 Sep 2026','Asked to call back after Friday','warn'),
 ('SBF-002','Ali','Jatrabari','Win back','28 Sep 2026','No order in 118 days. Was a top-3 buyer','bad'),
 ('SBF-006','Hasan','Khulna','Win back','29 Sep 2026','Switched to a local supplier, price objection','bad'),
 ('SBF-003','Jahid','Bogura','Reorder due','30 Sep 2026','Buys Eggfood 1kg roughly every 5 weeks','ok'),
 ('SBF-007','Mamun','Rangpur','Due reminder','01 Oct 2026','Promised bKash payment this week','warn'),
 ('SBF-009','Sohel','Barishal','Reorder due','03 Oct 2026','Small but steady. Worth a monthly call','ok'),
]


def followups():
    rows = ''.join(
        f'<tr><td><a href="#customer-profile" data-open="{c}"><b>{n}</b></a>'
        f'<div class="mut">{d}</div></td>'
        f'<td><span class="pill {tone}">{kind}</span></td>'
        f'<td class="mono mut">{when}</td>'
        f'<td class="mut">{note}</td>'
        f'<td class="r"><button class="btn btn-xs">{IC["wa"]}Call</button></td></tr>'
        for c, n, d, kind, when, note, tone in FOLLOW)
    return f'''{DEMO}
{ph('Follow-ups', 'Who to contact next, and why. Built from the ledger, not from memory.')}
<div class="card">
  <div class="ch"><h3>Next 7 days</h3><span class="sub">6 customers</span>
    <div class="sp"><button class="btn btn-xs">{IC['plus']}Add reminder</button></div></div>
  <div class="cb flush"><div class="tw"><table>
    <thead><tr><th>Customer</th><th>Reason</th><th>Next contact</th><th>Last note</th><th class="r">Act</th></tr></thead>
    <tbody>{rows}</tbody></table></div></div>
</div>'''


# ══════════════════════════════════════════════════════════════════════════
#  BUILD
# ══════════════════════════════════════════════════════════════════════════
VIEWS = [
    ('dashboard', dashboard), ('sales-entry', sales_entry),
    ('customers', customers_list), ('customer-profile', customer_profile),
    ('customer-timeline', customer_timeline), ('sales', sales_list), ('sale', sale_detail),
    ('products', products), ('product', product_detail),
    ('dues', dues), ('accounts', accounts),
    ('reports', reports), ('settings', settings),
]


def build():
    STATIC = {'reports'}
    body = ''.join(
        f'<section class="view" id="v-{k}" hidden>'
        f'{restyle(fn()) if k in STATIC else fn()}</section>' for k, fn in VIEWS)

    # every card title gets an icon chosen from its words, so hierarchy is
    # visible at a glance and no view needs editing by hand
    import re as _re
    def _ic(m):
        return f'<div class="ch"><i class="hi">{IC[title_icon(m.group(2))]}</i><h3{m.group(1) or ""}>{m.group(2)}</h3>'
    body = _re.sub(r'<div class="ch"><h3( id="[^"]*")?>([^<]*)</h3>', _ic, body)

    fu = [{'id': f'fu-{i}', 'code': c, 'name': n, 'district': d, 'kind': k,
           'when': w, 'note': nt, 'done': False}
          for i, (c, n, d, k, w, nt, _t) in enumerate(FOLLOW, 1)]
    engine = (ENGINE.replace('__CUST__', json.dumps(CUST, ensure_ascii=False))
                    .replace('__PROD__', json.dumps(PROD, ensure_ascii=False))
                    .replace('__FU__', json.dumps(fu, ensure_ascii=False))
                    .replace('__EXP__', json.dumps(
                        [{'d': d, 'kind': 'Expense', 'who': f'{k} \u00b7 {w}',
                          't': 'out', 'a': a, 'acc': acc}
                         for d, k, w, a, acc in EXPENSES], ensure_ascii=False))
                    .replace('__RAW__', json.dumps(
                        [{'n': n, 'u': u, 'q': q, 'r': r} for n, u, q, r in RAW], ensure_ascii=False))
                    .replace('__FIN__', json.dumps(
                        [{'n': n, 'p': p_, 'q': q, 'r': r} for n, p_, q, r in FIN], ensure_ascii=False))
                    .replace('__MOV__', json.dumps(
                        [{'d': d, 't': t, 'n': n, 'q': q, 'ref': rf} for d, t, n, q, rf in MOV],
                        ensure_ascii=False))
                    .replace('__GENERIC__', json.dumps(GENERIC_IMG))
                    .replace('__PLUS__', json.dumps(IC['plus']))
                    .replace('__SKUFAM__', json.dumps(SKU_FAMILY))
                    .replace('__DISTRICTS__', json.dumps(DISTRICTS, ensure_ascii=False))
                    .replace('__COUPONS__', json.dumps(COUPONS, ensure_ascii=False))
                    .replace('__TRUCK__', json.dumps(IC['truck']))
                    .replace('__PENCIL__', json.dumps(IC['pencil']))
                    .replace('__CFG__', json.dumps(CFG, ensure_ascii=False))
                    .replace('__LOG__', json.dumps(
                        [{'when': a, 'who': b, 'what': c, 'before': d, 'after': e}
                         for a, b, c, d, e in LOG], ensure_ascii=False))
                    .replace('__PAY__', json.dumps(
                        [{'n': n, 'v': v, 'w': w} for n, v, w in PAYABLE], ensure_ascii=False))
              + ENGINE2.replace('__COUPONS__', json.dumps(COUPONS, ensure_ascii=False)))
    # icons the engine emits at runtime
    engine = engine.replace("var S = {", "var WA=" + json.dumps(IC['wa']) +
                            ",XI=" + json.dumps(IC['x']) +
                            ",CHK=" + json.dumps(IC['check']) + ";\nvar S = {", 1)

    def _sheet_icons(html):
        import re as _re
        return _re.sub(r'<div class="ch"><h3( id="[^"]*")?>([^<]*)</h3>',
                       lambda m: f'<div class="ch"><i class="hi">{IC[title_icon(m.group(2))]}</i><h3{m.group(1) or ""}>{m.group(2)}</h3>', html)
    return _sheet_icons(f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>Shada BMS · Prototype</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Bengali:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="app">
{rail()}
<div style="min-width:0">
{topbar()}
<main class="canvas">
{body}
</main>
</div>
</div>
<div class="scrim" id="custModal">
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="ncTitle">
    <div class="ch"><h3 id="ncTitle">New customer</h3>
      <span class="sub">Code <b class="mono" id="ncCode">SBF-013</b>, generated</span></div>
    <form class="cb" id="custForm" onsubmit="return false">
      <div class="grid2">
        <div class="fld"><label for="ncName">Name</label>
          <input class="inp" id="ncName" autocomplete="off" placeholder="Full name"></div>
        <div class="fld"><label for="ncPhone">Mobile</label>
          <input class="inp mono" id="ncPhone" inputmode="numeric" placeholder="01XXX XXXXXX"></div>
      </div>
      <div class="grid2">
        <div class="fld"><label for="ncShop">Shop name <span class="opt">optional</span></label>
          <input class="inp" id="ncShop" autocomplete="off" placeholder="Saddam Bird House"></div>
        <div class="fld"><label for="ncArea">Area or thana</label>
          <input class="inp" id="ncArea" autocomplete="off" placeholder="Mirpur 11"></div>
      </div>
      <div class="grid2">
        <div class="fld cbx"><label for="ncDistrict">District</label>
          <input class="inp" id="ncDistrict" autocomplete="off" placeholder="Start typing, pick from the list">
          <div class="cbxlist" id="ncDistList" role="listbox"></div>
          <div class="hint">All 64 districts, one spelling each. Every report groups by this.</div></div>
        <div class="fld"><label for="ncSince">Customer since</label>
          <div class="dpw"><input class="inp" id="ncSince" value="26 Sep 2026" data-dp="past" readonly aria-haspopup="dialog">{IC['calendar']}</div>
          <div class="hint">Defaults to today. Pick an earlier date for a customer you already trade with.</div></div>
      </div>
      <div class="fld"><label>Price tier</label>
        <div class="tierpick" role="radiogroup" aria-label="Price tier">
          <button type="button" data-nctier="Retail" aria-pressed="true">{IC['check']}<b>Retail</b><span>Shop price, any quantity</span></button>
          <button type="button" data-nctier="Re-wholesale" aria-pressed="false">{IC['check']}<b>Re-wholesale</b><span>From 5 kg · 15 to 38% off</span></button>
          <button type="button" data-nctier="Wholesale" aria-pressed="false">{IC['check']}<b>Wholesale</b><span>From 10 kg · 20 to 42% off</span></button>
        </div>
        <div class="hint">Sets the rate that fills in on every sale line for this customer. Change it later from the profile.</div></div>
      <div class="fld"><label for="ncBanner">Banner picture <span class="opt">optional</span></label>
        <label class="drop" for="ncBanner" id="ncDrop">
          <img id="ncBannerPrev" alt="" hidden>
          <span class="dt">{IC['plus']}<b>Add a shop banner</b><small>JPG or PNG, wide, up to 2 MB. Shown at the top of the customer profile.</small></span>
        </label>
        <input type="file" id="ncBanner" accept="image/*" hidden></div>
      <div class="note" id="ncErr" hidden style="border-color:#F3C2BD;background:var(--bad-bg);color:var(--bad)"></div>
      <div style="display:flex;gap:8px;margin-top:6px">
        <button class="btn btn-p" id="ncSave" type="button" style="flex:1">{IC['check']}Save customer</button>
        <button class="btn" id="ncCancel" type="button">Cancel</button>
      </div>
      <div class="hint" style="margin-top:10px">Saved once. The customer is searchable on the
        sale screen immediately, and every report picks them up with no second entry.</div>
    </form>
  </div>
</div>
<div class="scrim" id="siModal">
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="siTitle">
    <div class="ch"><h3 id="siTitle">Stock in</h3><span class="sub">adds a movement row; stock is the running total</span></div>
    <div class="cb">
      <div class="fld"><label for="siProdBtn">Product</label><div class="ppick cbx" data-ppick="siProd"><button type="button" class="inp pselb" id="siProdBtn" aria-haspopup="listbox" aria-expanded="false"><span class="lthumb"><img alt=""></span><span class="mlbl">Pick a product</span><span class="chev">{IC['down']}</span></button><div class="cbxlist plist" role="listbox"></div><input type="hidden" id="siProd" value="0"></div></div>
      <div class="grid2">
        <div class="fld"><label for="siQty">Units received</label>
          <input class="inp num r" id="siQty" inputmode="numeric" placeholder="200"></div>
        <div class="fld"><label for="siRef">Reference</label>
          <input class="inp" id="siRef" placeholder="Supplier invoice, transfer, count"></div>
      </div>
      <div class="note" id="siErr" hidden style="border-color:#F3C2BD;background:var(--bad-bg);color:var(--bad)"></div>
      <div style="display:flex;gap:8px;margin-top:6px">
        <button class="btn btn-p" id="siSave" type="button" style="flex:1">{IC['check']}Add stock</button>
        <button class="btn" id="siCancel" type="button">Cancel</button>
      </div>
    </div>
  </div>
</div>

<div class="scrim" id="pbModal">
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="pbTitle">
    <div class="ch"><h3 id="pbTitle">New production batch</h3><span class="sub">consumes raw material, adds finished product</span></div>
    <div class="cb">
      <div class="fld"><label for="pbProdBtn">Product</label><div class="ppick cbx" data-ppick="pbProd"><button type="button" class="inp pselb" id="pbProdBtn" aria-haspopup="listbox" aria-expanded="false"><span class="lthumb"><img alt=""></span><span class="mlbl">Pick a product</span><span class="chev">{IC['down']}</span></button><div class="cbxlist plist" role="listbox"></div><input type="hidden" id="pbProd" value="0"></div></div>
      <div class="grid2">
        <div class="fld"><label for="pbQty">Units produced</label>
          <input class="inp num r" id="pbQty" inputmode="numeric" placeholder="120"></div>
        <div class="fld"><label for="pbCode">Batch code</label>
          <input class="inp mono" id="pbCode"></div>
      </div>
      <div class="note" id="pbPreview" style="margin-bottom:12px"></div>
      <div class="note" id="pbErr" hidden style="border-color:#F3C2BD;background:var(--bad-bg);color:var(--bad)"></div>
      <div style="display:flex;gap:8px;margin-top:6px">
        <button class="btn btn-p" id="pbSave" type="button" style="flex:1">{IC['check']}Record batch</button>
        <button class="btn" id="pbCancel" type="button">Cancel</button>
      </div>
      <div class="hint" style="margin-top:10px">The batch code prints on the jar lid. This is how a jar traces back to a day and a raw-material lot.</div>
    </div>
  </div>
</div>

<div class="scrim" id="npModal">
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="npTitle">
    <div class="ch"><h3 id="npTitle">New product</h3><span class="sub">a new pack size, or a new formula</span></div>
    <form class="cb" id="npForm" onsubmit="return false">
      <div class="grid2">
        <div class="fld"><label for="npFam">Formula</label><select class="inp" id="npFam"></select></div>
        <div class="fld" hidden><label for="npNewName">New formula name</label>
          <input class="inp" id="npNewName" placeholder="Avian Calcium Plus"></div>
        <div class="fld"><label for="npPack">Pack size</label>
          <input class="inp" id="npPack" placeholder="250g"></div>
      </div>
      <div class="grid2">
        <div class="fld"><label for="npRetail">Retail price</label>
          <div class="money"><span class="cur">৳</span><input class="inp num" id="npRetail" inputmode="numeric" placeholder="550"></div></div>
        <div class="fld"><label for="npWhole">Wholesale price</label>
          <div class="money"><span class="cur">৳</span><input class="inp num" id="npWhole" inputmode="numeric" placeholder="410"></div></div>
      </div>
      <div class="grid2">
        <div class="fld"><label for="npStock">Opening stock</label>
          <input class="inp num r" id="npStock" inputmode="numeric" placeholder="0"></div>
        <div class="fld"><label for="npReorder">Reorder level</label>
          <input class="inp num r" id="npReorder" inputmode="numeric" placeholder="20"></div>
      </div>
      <div class="note" id="npErr" hidden style="border-color:#F3C2BD;background:var(--bad-bg);color:var(--bad)"></div>
      <div style="display:flex;gap:8px;margin-top:6px">
        <button class="btn btn-p" id="npSave" type="button" style="flex:1">{IC['check']}Save product</button>
        <button class="btn" id="npCancel" type="button">Cancel</button>
      </div>
      <div class="hint" style="margin-top:10px">The SKU is generated from the formula and the pack. It appears on the sale screen the moment you save.</div>
    </form>
  </div>
</div>

<div class="scrim" id="epModal">
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="epTitle">
    <div class="ch"><h3 id="epTitle">Edit product</h3><span class="sub">one record; every screen reads it</span></div>
    <form class="cb" id="epForm" onsubmit="return false">
      <div class="epphoto">
        <span class="hpic" id="epPic"><img alt=""></span>
        <div style="min-width:0">
          <label class="btn btn-xs" for="epFile" style="cursor:pointer">{IC['plus']}Change photo</label>
          <input type="file" id="epFile" accept="image/*" hidden>
          <div class="hint">JPG, PNG or WebP. Shown on the sale screen, the product list and the invoice.</div>
        </div>
      </div>
      <div class="grid2">
        <div class="fld"><label for="epFam">Product name</label>
          <input class="inp" id="epFam" autocomplete="off"></div>
        <div class="fld"><label for="epPack">Pack size</label>
          <input class="inp" id="epPack" placeholder="250g"></div>
      </div>
      <div class="grid2">
        <div class="fld"><label for="epSku">SKU</label>
          <input class="inp mono" id="epSku" autocomplete="off"></div>
        <div class="fld"><label for="epReorder">Reorder level <span class="mut">units</span></label>
          <input class="inp num r" id="epReorder" inputmode="numeric"></div>
      </div>
      <div class="grid2">
        <div class="fld"><label for="epRetail">Retail price</label>
          <div class="money"><span class="cur">৳</span><input class="inp num" id="epRetail" inputmode="numeric"></div></div>
        <div class="fld"><label for="epWhole">Wholesale price</label>
          <div class="money"><span class="cur">৳</span><input class="inp num" id="epWhole" inputmode="numeric"></div></div>
      </div>
      <div class="note" id="epErr" hidden style="border-color:#F3C2BD;background:var(--bad-bg);color:var(--bad)"></div>
      <div style="display:flex;gap:8px;margin-top:6px;flex-wrap:wrap">
        <button class="btn btn-p" id="epSave" type="button" style="flex:1">{IC['check']}Save changes</button>
        <button class="btn" id="epCancel" type="button">Cancel</button>
        <button class="btn btn-d" id="epArchive" type="button">{IC['x']}Archive</button>
      </div>
      <div class="hint" style="margin-top:10px">Every change is written to the activity log with the value before and after.
        Archiving hides the product from new sales and lists; its history stays.</div>
    </form>
  </div>
</div>

<div class="scrim" id="colModal">
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="coTitle">
    <div class="ch"><h3 id="coTitle">New payment</h3>
      <span class="sub">Reduces that customer\u2019s due in the same write</span></div>
    <div class="cb">
      <div class="fld"><label for="coCust">Customer</label>
        <select class="inp" id="coCust"></select>
        <div class="hint">Currently owes <b class="mono" id="coDue">৳0</b></div></div>
      <div class="grid2">
        <div class="fld"><label for="coAmt">Amount</label>
          <div class="money"><span class="cur">৳</span><input class="inp num" id="coAmt" inputmode="numeric" value="0"></div></div>
        <div class="fld"><label>Method</label>{method_picker('coMethod')}</div>
      </div>
      <div class="fld"><label for="coInv">Against</label>
        <select class="inp" id="coInv"></select>
        <div class="hint">Left on account, it settles the oldest unpaid invoice first.</div></div>
      <div class="note" id="coErr" hidden style="border-color:#F3C2BD;background:var(--bad-bg);color:var(--bad)"></div>
      <div style="display:flex;gap:8px;margin-top:6px">
        <button class="btn btn-p" id="coSave" type="button" style="flex:1">{IC['check']}Save collection</button>
        <button class="btn" id="coCancel" type="button">Cancel</button>
      </div>
    </div>
  </div>
</div>

<div class="scrim" id="expModal">
  <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="exTitle">
    <div class="ch"><h3 id="exTitle">Record expense</h3>
      <span class="sub">Posts against cash or bank immediately</span></div>
    <form class="cb" id="expForm" onsubmit="return false">
      <div class="grid2">
        <div class="fld"><label for="exCat">Category</label>
          <select class="inp" id="exCat">
            <option>Raw material</option><option>Packaging</option><option>Salary</option>
            <option>Courier</option><option>Utilities</option><option>Rent</option>
            <option>Marketing</option><option>Transport</option><option>Other</option></select></div>
        <div class="fld"><label for="exAcc">Paid from</label>
          <select class="inp" id="exAcc"><option>Cash</option><option>Bank</option></select></div>
      </div>
      <div class="fld"><label for="exDetail">Detail</label>
        <input class="inp" id="exDetail" autocomplete="off" placeholder="Maize flour, 200kg">
        <div class="hint">Write it so it still makes sense a year later in an audit.</div></div>
      <div class="fld"><label for="exAmt">Amount</label>
        <div class="money"><span class="cur">৳</span><input class="inp num" id="exAmt" inputmode="numeric" value="0"></div></div>
      <div class="note" id="exErr" hidden style="border-color:#F3C2BD;background:var(--bad-bg);color:var(--bad)"></div>
      <div style="display:flex;gap:8px;margin-top:6px">
        <button class="btn btn-p" id="exSave" type="button" style="flex:1">{IC['check']}Save expense</button>
        <button class="btn" id="exCancel" type="button">Cancel</button>
      </div>
    </form>
  </div>
</div>
<div class="toast" id="toast">{IC['check']}<span></span></div>
<script>{engine}</script>
</body></html>''')


if __name__ == '__main__':
    html = build()
    for p in ['/sessions/pensive-affectionate-einstein/mnt/Projects/Shada Birds/SHADA-BMS/_screens/shada-bms-prototype.html',
              '/sessions/pensive-affectionate-einstein/mnt/outputs/shada-bms-prototype.html']:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').write(html)
    print(f'built {len(html):,} bytes · {len(CUST)} customers · {sum(len(c["o"]) for c in CUST)} orders')
