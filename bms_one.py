#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shada BMS · Phase 0 — four clickable screens for client sign-off.

No PHP. Flat HTML with real layout and realistic numbers, so Anowar Bhai can
click through Single Data Entry and believe it before a line of code is written.
This is the answer to his question 12.

Design follows the LOGGED-IN half of the Shada design system:
  dark left rail, flat --paper2 page, white cards, compact rows, 14 to 15px body,
  no wing, no feather, no decorative motion, hand-rolled SVG charts.
  Reason: the audience is on cheap Androids on slow connections.
"""
import os, json, datetime

OUT = '/tmp/bms'

# ── money, Bangla lakh grouping:  123456 -> ১,২৩,৪৫৬ style grouping in latin digits
def tk(n, sign=True):
    n = int(round(n))
    s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ','.join(parts) + ',' + tail
    return ('৳' if sign else '') + ('-' if n < 0 else '') + s

I = lambda p, w=1.8: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
IC = {
 'dash':   I('<path d="M3 12l9-8 9 8"/><path d="M5 10v10h14V10"/>'),
 'sale':   I('<path d="M4 7h16v13H4z"/><path d="M8 7V5a4 4 0 0 1 8 0v2"/><path d="M9 12h6"/>'),
 'cust':   I('<circle cx="12" cy="8" r="3.5"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/>'),
 'time':   I('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 'stock':  I('<path d="M3 8l9-4 9 4-9 4z"/><path d="M3 8v8l9 4 9-4V8"/>'),
 'money':  I('<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/>'),
 'report': I('<path d="M5 3h9l5 5v13H5z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/>'),
 'gear':   I('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 1 1-4 0v-.1A1.6 1.6 0 0 0 7.5 19.4a1.6 1.6 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0-1.1-2.7H1.7a2 2 0 1 1 0-4h.1A1.6 1.6 0 0 0 4.6 7.5"/>'),
 'plus':   I('<path d="M12 5v14M5 12h14"/>', 2.2),
 'search': I('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', 2),
 'bell':   I('<path d="M18 8a6 6 0 1 0-12 0c0 7-3 8-3 8h18s-3-1-3-8z"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>'),
 'wa':     ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd">'
            '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.9a8.1 8.1 0 0 1 6.6 12.8l-.3.4.7 2.5-2.6-.7-.4.2A8.1 8.1 0 1 1 12 3.9Z"/>'
            '<path d="M9.1 7.2h.6c.2 0 .5-.1.7.5l.9 2.2c.1.1.1.3 0 .5l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.4 2.4 1.5.3.1.4.1.6-.1.1-.2.7-.9.9-1.2.2-.2.4-.2.7-.1.2.1 1.7.9 2 1 .3.1.5.2.6.4 0 .1 0 .7-.2 1.4-.2.7-1.5 1.3-2 1.4-.6.1-1.1.3-3.6-.7-3-1.3-5-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.7-2.2 1-2.5c.3-.3.6-.4.8-.4Z"/></svg>'),
 'trash':  I('<path d="M4 7h16M10 11v6M14 11v6"/><path d="M6 7l1 13h10l1-13"/><path d="M9 7V4h6v3"/>'),
 'check':  I('<path d="M4 12.5 9.5 18 20 6.5"/>', 2.4),
}

NAV = [('dashboard','Dashboard','dash'), ('sales-entry','Sales entry','sale'),
       ('customer-profile','Customers','cust'), ('customer-timeline','Timeline','time'),
       ('inventory','Inventory','stock'), ('accounts','Accounts','money'),
       ('reports','Reports','report'), ('settings','Settings','gear')]
NAV_DEAD = []

# ═════════════════════════════════════════════════════════════════════════
#  DEMO DATA
#  Customer names are the ones in the client's own spreadsheet. Product names
#  and prices are his real catalogue. Quantities and dates are invented, and
#  the whole set is flagged DEMO on every screen so nobody mistakes it.
# ═════════════════════════════════════════════════════════════════════════
PRODUCTS = [
 ('Nutricare Hand Feeding', '1kg',  920, 690),
 ('Nutricare Hand Feeding', '500g', 485, 362),
 ('Avian Eggfood',          '1kg',  870, 583),
 ('Avian Eggfood',          '500g', 450, 308),
 ('Avian Spirulina',        '200g',1275,1017),
 ('Avian Herbs',            '200g', 730, 580),
 ('Avian Moringa',          '200g', 370, 295),
 ('Avian Beetroot',         '200g', 370, 295),
]
TOP_CUST = [('Saddam','Mirpur 11, Dhaka',268400,123500),('Ali','Jatrabari, Dhaka',196200,196200),
            ('Jahid','Bogura Sadar',154900,131000),('Rafiq','Chattogram',131700,118400),
            ('Nazmul','Sylhet',118300,96000),('Hasan','Khulna',97500,97500),
            ('Mamun','Rangpur',88200,61000),('Tanvir','Rajshahi',74600,74600),
            ('Sohel','Barishal',61300,44000),('Imran','Mymensingh',52800,52800)]
TOP_PROD = [('Nutricare Hand Feeding 1kg',412,379040),('Avian Eggfood 1kg',298,259260),
            ('Nutricare Hand Feeding 500g',341,165385),('Avian Eggfood 500g',276,124200),
            ('Avian Spirulina 200g',84,107100),('Avian Herbs 200g',96,70080),
            ('Avian Moringa 200g',131,48470),('Avian Beetroot 200g',118,43660),
            ('Nutricare 200g',147,35280),('Avian Eggfood 200g',129,27090)]
PENDING = [('INV-2609-0148','Saddam','Dhaka',4,12480,'Web'),
           ('INV-2609-0147','Rafiq','Chattogram',9,18900,'Manual'),
           ('INV-2609-0146','Nazmul','Sylhet',3,6400,'Web'),
           ('INV-2609-0145','Mamun','Rangpur',6,14250,'Manual'),
           ('INV-2609-0144','Sohel','Barishal',2,3100,'Web')]
STOCK = [('Nutricare Hand Feeding 1kg',18,40,'low'),('Avian Eggfood 500g',7,30,'critical'),
         ('Avian Spirulina 200g',24,25,'low'),('Avian Herbs 200g',51,25,'ok'),
         ('Avian Moringa 200g',62,25,'ok')]
LAPSED_60 = [('Hasan','Khulna','68 days',97500),('Tanvir','Rajshahi','74 days',74600),
             ('Imran','Mymensingh','61 days',52800)]
LAPSED_90 = [('Ali','Jatrabari, Dhaka','118 days',196200),('Sohel','Barishal','96 days',61300)]
SPARK = [42,55,38,61,72,58,80,66,91,74,88,96,83,101,94,112,105,98,121,114,
         131,118,142,126,155,139,148,162,151,168]

# ═════════════════════════════════════════════════════════════════════════
CSS = '''
/* ═══════════════════════════════════════════════════════════════════════════
   SHADA BMS · Phase 0 screens
   Logged-in density from the Shada design system. Same tokens as the website,
   tighter rhythm. No decorative motifs anywhere: this is a work surface.
   Charts are hand-rolled SVG. No chart library, the audience is on cheap phones.
   ═══════════════════════════════════════════════════════════════════════════ */
:root{
  --ff:'Plus Jakarta Sans','Hind Siliguri',system-ui,sans-serif;
  --paper:#fff; --paper2:#F5F5F3; --paper3:#ECECE9;
  --ink:#0A2617; --ink2:#123222;
  --leaf:#5FD48A; --tx:#1D1D1F; --tx2:#6E6E73; --tx3:#A1A1A6;
  --on:#F5F5F7; --on2:#A1A1A6;
  --line:rgba(0,0,0,.08); --line-d:rgba(255,255,255,.12);
  --brand:#089830; --brand-d:#067426; --brand-soft:#E6F4EA;
  --gold:#E0B810; --gold-d:#B8871B; --red:#C0392B; --red-soft:#FDECEA;
  --r:10px; --r2:14px; --ease:cubic-bezier(.22,1,.36,1);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--ff);background:var(--paper2);color:var(--tx);
  font-size:14.5px;line-height:1.5;-webkit-font-smoothing:antialiased;letter-spacing:-.008em}
a{color:inherit;text-decoration:none}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
table{border-collapse:separate;border-spacing:0;width:100%}
.num{font-variant-numeric:tabular-nums}

/* ── demo banner. Must be impossible to miss. ─────────────────────────── */
.demo{background:#FFE9A8;color:#6B4E00;font-size:12.5px;font-weight:600;
  padding:7px 20px;text-align:center;letter-spacing:.01em}

/* ── shell ───────────────────────────────────────────────────────────── */
.app{display:grid;grid-template-columns:232px minmax(0,1fr);min-height:100vh}
@media(max-width:940px){.app{grid-template-columns:minmax(0,1fr)}}
/* A grid item defaults to min-width:auto, so the horizontal nav scroller and the
   wide tables blow the column out past the viewport. This is the fix. */
.rail,.main{min-width:0}

.rail{background:var(--ink);color:#fff;padding:18px 12px;display:flex;flex-direction:column;gap:2px;
  position:sticky;top:0;height:100vh;overflow-y:auto}
@media(max-width:940px){
  .rail{position:static;height:auto;flex-direction:row;overflow-x:auto;scrollbar-width:none;
    padding:10px;gap:6px}
  .rail::-webkit-scrollbar{display:none}
  .rail .brandrow,.rail .railfoot,.rail .sep{display:none}
  .rail a,.rail .dead{min-height:38px;padding:8px 13px}
}
.brandrow{display:flex;align-items:center;gap:9px;padding:4px 10px 18px}
.brandrow b{font-size:15px;font-weight:700;letter-spacing:.03em}
.brandrow span{font-size:10.5px;color:var(--leaf);font-weight:600;letter-spacing:.09em;
  background:rgba(95,212,138,.14);padding:2px 7px;border-radius:999px}
.rail a,.rail .dead{display:flex;align-items:center;gap:11px;min-height:42px;padding:9px 12px;
  border-radius:var(--r);font-size:14.5px;font-weight:500;color:var(--on2);white-space:nowrap;
  transition:background .14s,color .14s}
.rail a svg,.rail .dead svg{width:18px;height:18px;flex:0 0 auto}
.rail a:hover{background:rgba(255,255,255,.07);color:#fff}
.rail a.on{background:rgba(95,212,138,.15);color:var(--leaf);font-weight:600}
.rail .dead{color:#4E6459;cursor:not-allowed}
.rail .sep{height:1px;background:var(--line-d);margin:10px 12px}
.railfoot{margin-top:auto;padding:14px 12px 4px;border-top:1px solid var(--line-d);
  font-size:11.5px;color:#4E6459;line-height:1.5}

.main{min-width:0;padding:clamp(16px,2vw,26px) clamp(16px,2.4vw,32px) 60px}

/* ── top bar ─────────────────────────────────────────────────────────── */
.top{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:18px}
.top h1{font-size:clamp(20px,2.2vw,27px);font-weight:600;letter-spacing:-.028em;line-height:1.15}
.top .sub{font-size:13px;color:var(--tx2);margin-top:3px}
.top .sp{margin-left:auto;display:flex;gap:9px;align-items:center;flex-wrap:wrap}
.srch{position:relative}
.srch svg{position:absolute;left:12px;top:50%;transform:translateY(-50%);width:16px;height:16px;color:var(--tx3)}
.srch input{width:260px;max-width:46vw;height:40px;border:1px solid var(--line);border-radius:var(--r);
  background:#fff;padding:0 12px 0 36px;font:500 14px/1 var(--ff);color:var(--tx);outline:none}
.srch input:focus{border-color:var(--brand);box-shadow:0 0 0 3px rgba(8,152,48,.12)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:7px;min-height:40px;
  padding:0 16px;border-radius:var(--r);font-size:14px;font-weight:600;white-space:nowrap;
  border:1px solid var(--line);background:#fff;color:var(--tx);transition:all .15s}
.btn svg{width:16px;height:16px}
.btn:hover{border-color:var(--tx3)}
.btn.pri{background:linear-gradient(180deg,#0EA63A,var(--brand) 55%,#07872B);color:#fff;border-color:transparent}
.btn.pri:hover{background:var(--brand-d)}
.btn.lg{min-height:46px;padding:0 22px;font-size:15px}

/* ── filter chips ────────────────────────────────────────────────────── */
.chips{display:flex;gap:7px;overflow-x:auto;scrollbar-width:none;margin-bottom:16px;padding-bottom:2px}
.chips::-webkit-scrollbar{display:none}
.chips button{flex:0 0 auto;min-height:34px;padding:7px 14px;border-radius:999px;border:1px solid var(--line);
  background:#fff;font-size:13.5px;font-weight:500;color:var(--tx2);white-space:nowrap;transition:all .15s}
.chips button:hover{border-color:var(--brand);color:var(--brand)}
.chips button[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:#fff;font-weight:600}

/* ── cards ───────────────────────────────────────────────────────────── */
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r2);min-width:0}
/* Every grid child needs min-width:0 or a wide table sizes its column instead of
   scrolling inside it. This is the same auto-minimum trap as the nav rail. */
.two>*,.wide>*,.form>*,.kpis>*{min-width:0}
.card>.h{display:flex;align-items:center;gap:10px;padding:14px 18px;
  border-bottom:1px solid var(--line);flex-wrap:wrap;min-width:0}
.card>.h h2{font-size:14px;font-weight:600;letter-spacing:-.012em}
.card>.h .sp{margin-left:auto;font-size:12.5px;color:var(--tx3);min-width:0}
.card>.b{padding:6px 18px 14px}
.card>.b.flush{padding:0;overflow-x:auto;-webkit-overflow-scrolling:touch;min-width:0;max-width:100%}
/* Only force a scroll width on small screens. On desktop a narrow column should
   fit its own table, not scroll inside itself. */
@media(max-width:700px){.card>.b.flush>table{min-width:520px}}

.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(196px,1fr));gap:12px;margin-bottom:14px}
.kpi{background:#fff;border:1px solid var(--line);border-radius:var(--r2);padding:15px 17px}
.kpi .k{display:block;font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;
  color:var(--tx3);margin-bottom:8px}
.kpi .v{display:block;font-size:clamp(21px,2.4vw,28px);font-weight:600;letter-spacing:-.032em;
  line-height:1;font-variant-numeric:tabular-nums}
.kpi .d{display:inline-block;margin-top:9px;font-size:12px;font-weight:600}
.kpi .d.up{color:var(--brand)} .kpi .d.dn{color:var(--red)} .kpi .d.fl{color:var(--tx3)}
.kpi.due{border-color:rgba(224,184,16,.5);background:#FFFCF0}
.kpi.due .v{color:var(--gold-d)}
.kpi.alert{border-color:rgba(192,57,43,.35);background:var(--red-soft)}
.kpi.alert .v{color:var(--red)}

/* ── tables ──────────────────────────────────────────────────────────── */
.tb{width:100%;font-size:13.8px}
.tb th{position:sticky;top:0;background:var(--paper2);font-size:10.5px;font-weight:600;
  letter-spacing:.06em;text-transform:uppercase;color:var(--tx3);text-align:left;
  padding:10px 14px;border-bottom:1px solid var(--line);z-index:1;white-space:nowrap}
.tb td{padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:middle}
.tb tbody tr:last-child td{border-bottom:0}
.tb tbody tr:hover td{background:var(--paper2)}
.tb .r{text-align:right;font-variant-numeric:tabular-nums}
.tb b{font-weight:600}
.tb .mut{color:var(--tx2);font-size:12.5px}
.rank{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:5px;
  background:var(--paper2);font-size:11px;font-weight:700;color:var(--tx2);margin-right:9px}
.rank.t1{background:var(--brand);color:#fff} .rank.t2{background:#2FAF55;color:#fff}
.rank.t3{background:#66C97F;color:#fff}

.pill{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:600;
  padding:3px 9px;border-radius:999px;white-space:nowrap}
.pill.web{background:var(--brand-soft);color:var(--brand-d)}
.pill.man{background:var(--paper3);color:var(--tx2)}
.pill.ok{background:var(--brand-soft);color:var(--brand-d)}
.pill.low{background:#FFF6D9;color:var(--gold-d)}
.pill.crit{background:var(--red-soft);color:var(--red)}
.pill.due{background:#FFF6D9;color:var(--gold-d)}
.pill.paid{background:var(--brand-soft);color:var(--brand-d)}

/* ── grid regions ────────────────────────────────────────────────────── */
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px}
@media(max-width:1000px){.two{grid-template-columns:1fr}}
.wide{display:grid;grid-template-columns:1.35fr .65fr;gap:12px;margin-bottom:14px}
@media(max-width:1000px){.wide{grid-template-columns:1fr}}

/* ── hand-rolled chart ───────────────────────────────────────────────── */
.chart{padding:16px 18px 6px}
.chart svg{width:100%;height:150px;display:block;overflow:visible}
.chart .gl{stroke:var(--line);stroke-width:1}
.chart .ln{fill:none;stroke:var(--brand);stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}
.chart .ar{fill:url(#g1)}
.chart .lb{font-size:10.5px;fill:var(--tx3)}
.chart .dot{fill:#fff;stroke:var(--brand);stroke-width:2.2}

/* ── sales entry ─────────────────────────────────────────────────────── */
.form{display:grid;grid-template-columns:minmax(0,1fr) 336px;gap:14px;align-items:start}
@media(max-width:1060px){.form{grid-template-columns:1fr}}
.fr{display:grid;gap:12px;margin-bottom:14px}
.fr.c2{grid-template-columns:1fr 1fr}
.fr.c3{grid-template-columns:1.4fr 1fr 1fr}
@media(max-width:700px){.fr.c2,.fr.c3{grid-template-columns:1fr}}
label{display:block;font-size:12px;font-weight:600;color:var(--tx);margin-bottom:6px}
label i{font-style:normal;color:var(--tx3);font-weight:400}
.in{width:100%;height:42px;border:1px solid var(--line);border-radius:var(--r);background:#fff;
  padding:0 12px;font:500 14.5px/1 var(--ff);color:var(--tx);outline:none;
  -webkit-appearance:none;appearance:none;transition:border-color .15s,box-shadow .15s}
select.in{background-image:url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236E6E73' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 11px center;background-size:16px;padding-right:34px;cursor:pointer}
.in:focus{border-color:var(--brand);box-shadow:0 0 0 3px rgba(8,152,48,.12)}
textarea.in{height:auto;min-height:74px;padding:11px 12px;line-height:1.5;resize:vertical}
.lines .tb td{padding:8px 18px}
.lines .in{height:38px;font-size:14px}
.addline{display:flex;align-items:center;gap:8px;padding:12px 18px;border-top:1px solid var(--line)}
.iconbtn{width:32px;height:32px;border-radius:8px;border:1px solid var(--line);background:#fff;
  display:grid;place-items:center;color:var(--tx3);transition:all .15s}
.iconbtn:hover{border-color:var(--red);color:var(--red);background:var(--red-soft)}
.iconbtn svg{width:15px;height:15px}

.tot{position:sticky;top:18px}
.tot .row{display:flex;justify-content:space-between;gap:12px;padding:10px 0;
  border-bottom:1px solid var(--line);font-size:14px;color:var(--tx2)}
.tot .row b{color:var(--tx);font-weight:600;font-variant-numeric:tabular-nums}
.tot .row.big{border-bottom:0;padding-top:14px;font-size:15px;color:var(--tx);font-weight:600}
.tot .row.big b{font-size:24px;letter-spacing:-.03em}
.tot .row.duerow b{color:var(--gold-d)}
.auto{display:flex;align-items:flex-start;gap:9px;background:var(--brand-soft);
  border:1px solid rgba(8,152,48,.2);border-radius:var(--r);padding:11px 13px;margin-top:14px;
  font-size:12.5px;line-height:1.5;color:var(--brand-d)}
.auto svg{width:15px;height:15px;flex:0 0 auto;margin-top:2px}

/* ── customer profile ────────────────────────────────────────────────── */
.phead{background:var(--ink);color:#fff;border-radius:var(--r2);padding:clamp(18px,2.2vw,26px);
  margin-bottom:14px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.av{width:56px;height:56px;border-radius:14px;background:rgba(95,212,138,.16);color:var(--leaf);
  display:grid;place-items:center;font-size:21px;font-weight:700;flex:0 0 auto}
.phead h2{font-size:clamp(20px,2.3vw,26px);font-weight:600;letter-spacing:-.028em;line-height:1.15}
.phead .meta{font-size:13px;color:var(--on2);margin-top:5px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.phead .meta i{width:3px;height:3px;border-radius:50%;background:rgba(255,255,255,.35);font-style:normal}
.phead .tags{display:flex;gap:6px;margin-top:9px;flex-wrap:wrap}
.tag{font-size:11.5px;font-weight:600;padding:3px 10px;border-radius:999px;
  background:rgba(95,212,138,.16);color:var(--leaf)}
.tag.vip{background:rgba(224,184,16,.18);color:#F0CF4E}
.phead .sp{margin-left:auto;display:flex;gap:9px;flex-wrap:wrap}
@media(max-width:700px){.phead .sp{margin-left:0;width:100%}.phead .sp .btn{flex:1}}
.phead .btn{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.22);color:#fff}
.phead .btn:hover{background:rgba(255,255,255,.18)}

/* ── timeline ────────────────────────────────────────────────────────── */
.tl{position:relative;padding-left:30px}
.tl::before{content:"";position:absolute;left:9px;top:6px;bottom:6px;width:2px;background:var(--line)}
.tlx{position:relative;padding:0 0 22px}
.tlx:last-child{padding-bottom:2px}
.tlx::before{content:"";position:absolute;left:-26px;top:4px;width:12px;height:12px;border-radius:50%;
  background:#fff;border:2.5px solid var(--tx3)}
.tlx.sale::before{border-color:var(--brand)}
.tlx.pay::before{border-color:#2FAF55;background:#2FAF55}
.tlx.dueev::before{border-color:var(--gold)}
.tlx.ret::before{border-color:var(--red)}
.tlx .dt{font-size:11.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--tx3)}
.tlx .ti{font-size:15px;font-weight:600;margin:3px 0 3px;letter-spacing:-.012em}
.tlx .tx{font-size:13.5px;color:var(--tx2);line-height:1.55}
.tlx .amt{font-weight:600;color:var(--tx);font-variant-numeric:tabular-nums}

.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;color:var(--tx2);
  padding:12px 18px;border-top:1px solid var(--line);min-width:0}
.legend>span{min-width:0}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:9px;height:9px;border-radius:50%;display:inline-block;font-style:normal}

.note{font-size:12.5px;color:var(--tx3);line-height:1.55;margin-top:14px}
'''

def rail(active='dashboard'):
    a = ''.join(
        f'<a data-go="{s}" class="{"on" if s==active else ""}" href="#{s}">{IC[i]}<span>{t}</span></a>'
        for s, t, i in NAV)
    return (f'<nav class="rail"><div class="brandrow"><b>SHADA</b><span>BMS</span></div>{a}'
            f'<div class="railfoot">Phase 0 prototype<br>All 8 menus are clickable</div></nav>')


def chart_svg(vals, w=760, h=150):
    lo, hi = min(vals), max(vals)
    rng = (hi - lo) or 1
    step = w / (len(vals) - 1)
    pts = [(i * step, h - ((v - lo) / rng) * (h - 18) - 9) for i, v in enumerate(vals)]
    line = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    area = line + f' L{w},{h} L0,{h} Z'
    grid = ''.join(f'<line class="gl" x1="0" y1="{h*k/3:.0f}" x2="{w}" y2="{h*k/3:.0f}"/>' for k in range(4))
    lx, ly = pts[-1]
    return (f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" role="img" '
            f'aria-label="Sales trend, last 30 days">'
            f'<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#089830" stop-opacity=".18"/>'
            f'<stop offset="1" stop-color="#089830" stop-opacity="0"/></linearGradient></defs>'
            f'{grid}<path class="ar" d="{area}"/><path class="ln" d="{line}"/>'
            f'<circle class="dot" cx="{lx:.1f}" cy="{ly:.1f}" r="4"/></svg>')


# ═════════════════════════════════════════════════════════════════════════
#  1 · DASHBOARD  — the 9 widgets the client asked for, by name
# ═════════════════════════════════════════════════════════════════════════
def dashboard():
    chips = ''.join(
        f'<button aria-pressed="{"true" if i==2 else "false"}">{t}</button>'
        for i, t in enumerate(['Today','This week','This month','This year','Custom range']))

    kpis = ''.join([
      f'<div class="kpi"><span class="k">Today\'s sales</span><span class="v">{tk(18420)}</span>'
      f'<span class="d up">+12% vs yesterday</span></div>',
      f'<div class="kpi"><span class="k">Today\'s collection</span><span class="v">{tk(11900)}</span>'
      f'<span class="d up">+4%</span></div>',
      f'<div class="kpi due"><span class="k">Total due</span><span class="v">{tk(486300)}</span>'
      f'<span class="d fl">across 34 customers</span></div>',
      f'<div class="kpi"><span class="k">Pending orders</span><span class="v">5</span>'
      f'<span class="d up">3 from the website</span></div>',
      f'<div class="kpi alert"><span class="k">Stock alert</span><span class="v">2</span>'
      f'<span class="d fl">below reorder level</span></div>',
    ])

    def lapsed(rows):
        return ''.join(
            f'<tr><td><b>{n}</b><div class="mut">{d}</div></td>'
            f'<td class="r mut">{days}</td><td class="r"><b>{tk(v)}</b></td>'
            f'<td class="r"><a class="btn" style="min-height:30px;padding:0 10px;font-size:12.5px">'
            f'{IC["wa"]}Call</a></td></tr>' for n, d, days, v in rows)

    def _due_cell(sold, paid):
        if sold == paid:
            return '<span class="pill paid">clear</span>'
        return '<b>' + tk(sold - paid) + '</b>'
    top_c = ''.join(
      f'<tr><td><span class="rank {"t"+str(i) if i<=3 else ""}">{i}</span><b>{n}</b>'
      f'<div class="mut">{d}</div></td><td class="r">{tk(s)}</td>'
      f'<td class="r">{_due_cell(s, p)}</td></tr>'
      for i, (n, d, s, p) in enumerate(TOP_CUST, 1))

    top_p = ''.join(
      f'<tr><td><span class="rank {"t"+str(i) if i<=3 else ""}">{i}</span>{n}</td>'
      f'<td class="r mut">{q}</td><td class="r"><b>{tk(v)}</b></td></tr>'
      for i, (n, q, v) in enumerate(TOP_PROD, 1))

    pend = ''.join(
      f'<tr><td><b>{inv}</b></td><td>{c}<div class="mut">{d}</div></td>'
      f'<td class="r mut">{n} items</td><td class="r"><b>{tk(v)}</b></td>'
      f'<td class="r"><span class="pill {"web" if s=="Web" else "man"}">{s}</span></td></tr>'
      for inv, c, d, n, v, s in PENDING)

    stock = ''.join(
      f'<tr><td>{n}</td><td class="r mut">{q} / {r}</td>'
      f'<td class="r"><span class="pill {"crit" if s=="critical" else ("low" if s=="low" else "ok")}">'
      f'{"critical" if s=="critical" else ("low" if s=="low" else "ok")}</span></td></tr>'
      for n, q, r, s in STOCK)

    body = f'''
<div class="top">
  <div><h1>Dashboard</h1><div class="sub">Saturday, 26 September 2026 · everything below updates from one sales entry</div></div>
  <div class="sp">
    <span class="srch">{IC['search']}<input placeholder="Search customer, phone, invoice, memo"></span>
    <a class="btn pri" href="#sales-entry">{IC['plus']}New sale</a>
  </div>
</div>
<div class="chips">{chips}</div>
<div class="kpis">{kpis}</div>

<div class="wide">
  <div class="card">
    <div class="h"><h2>Sales, last 30 days</h2><span class="sp">Peak {tk(16800)} · 26 Sep</span></div>
    <div class="chart">{chart_svg(SPARK)}</div>
    <div class="legend"><span><i style="background:#089830"></i>Daily sales</span>
      <span style="margin-left:auto;color:var(--tx3)">Rendered as SVG. No chart library, so it costs nothing on a slow phone.</span></div>
  </div>
  <div class="card">
    <div class="h"><h2>Stock alert</h2><span class="sp">qty / reorder</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Product</th><th class="r">Stock</th><th class="r">Status</th></tr></thead>
      <tbody>{stock}</tbody></table></div>
  </div>
</div>

<div class="card" style="margin-bottom:14px">
  <div class="h"><h2>Pending orders</h2><span class="sp">website orders arrive here automatically</span></div>
  <div class="b flush"><table class="tb">
    <thead><tr><th>Invoice</th><th>Customer</th><th class="r">Items</th><th class="r">Total</th><th class="r">Source</th></tr></thead>
    <tbody>{pend}</tbody></table></div>
</div>

<div class="two">
  <div class="card">
    <div class="h"><h2>Top 10 customers</h2><span class="sp">this year</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Customer</th><th class="r">Sold</th><th class="r">Due</th></tr></thead>
      <tbody>{top_c}</tbody></table></div>
  </div>
  <div class="card">
    <div class="h"><h2>Top 10 selling products</h2><span class="sp">this year</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Product</th><th class="r">Qty</th><th class="r">Value</th></tr></thead>
      <tbody>{top_p}</tbody></table></div>
  </div>
</div>

<div class="two">
  <div class="card">
    <div class="h"><h2>No purchase in 2 months</h2><span class="sp">3 customers</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Customer</th><th class="r">Last order</th><th class="r">Lifetime</th><th class="r">Action</th></tr></thead>
      <tbody>{lapsed(LAPSED_60)}</tbody></table></div>
  </div>
  <div class="card">
    <div class="h"><h2>No purchase in 3 months</h2><span class="sp">2 customers</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Customer</th><th class="r">Last order</th><th class="r">Lifetime</th><th class="r">Action</th></tr></thead>
      <tbody>{lapsed(LAPSED_90)}</tbody></table></div>
  </div>
</div>

<p class="note">All nine widgets read pre-computed rows, never live aggregates. Running totals are
maintained when a sale is saved; the top-10 rankings are written by a nightly job. Target is under
400ms with 50,000 sales rows.</p>
'''
    return body


# ═════════════════════════════════════════════════════════════════════════
#  2 · SALES ENTRY  — the heart. One screen, everything else derives from it.
# ═════════════════════════════════════════════════════════════════════════
def sales_entry():
    opts = ''.join(f'<option>{n} · {s} — {tk(r)}</option>' for n, s, r, w in PRODUCTS)
    LINES = [('Nutricare Hand Feeding · 1kg', 6, 690, 4140),
             ('Avian Eggfood · 500g', 12, 308, 3696),
             ('Avian Spirulina · 200g', 4, 1017, 4068)]
    rows = ''.join(f'''<tr>
      <td><select class="in">{opts}</select></td>
      <td style="width:92px"><input class="in r" value="{q}" inputmode="numeric"></td>
      <td style="width:116px"><input class="in" value="{p}" inputmode="numeric"></td>
      <td class="r" style="width:118px"><b>{tk(t)}</b></td>
      <td style="width:52px"><button class="iconbtn" aria-label="Remove line">{IC['trash']}</button></td>
    </tr>''' for n, q, p, t in LINES)

    sub = sum(t for _, _, _, t in LINES)
    disc, deliv = 400, 250
    total = sub - disc + deliv
    paid = 8000
    due = total - paid

    body = f'''
<div class="top">
  <div><h1>New sale</h1><div class="sub">Type it once. Invoice, due, customer totals, stock and every report update by themselves.</div></div>
  <div class="sp"><a class="btn" href="#dashboard">Cancel</a></div>
</div>

<div class="form">
  <div>
    <div class="card" style="margin-bottom:14px"><div class="h"><h2>Customer</h2>
      <span class="sp">Wholesale tier · price filled automatically</span></div>
      <div class="b" style="padding:16px 18px 18px">
        <div class="fr c3">
          <div><label>Customer <i>type to search</i></label>
            <input class="in" value="Saddam — 01711 234567 — Mirpur 11"></div>
          <div><label>District</label><select class="in"><option>Dhaka</option><option>Chattogram</option><option>Bogura</option></select></div>
          <div><label>Price tier</label><select class="in"><option>Wholesale</option><option>Re-wholesale</option><option>Retail</option></select></div>
        </div>
        <div class="fr c3" style="margin-bottom:0">
          <div><label>Invoice no <i>automatic</i></label><input class="in" value="INV-2609-0149" readonly style="background:var(--paper2);color:var(--tx2)"></div>
          <div><label>Date</label><input class="in" value="26 Sep 2026"></div>
          <div><label>Memo no <i>optional</i></label><input class="in" placeholder="Paper memo reference"></div>
        </div>
      </div>
    </div>

    <div class="card lines" style="margin-bottom:14px">
      <div class="h"><h2>Items</h2><span class="sp">{len(LINES)} lines</span></div>
      <div class="b flush"><table class="tb">
        <thead><tr><th>Product and pack</th><th class="r">Qty</th><th class="r">Unit price</th><th class="r">Line total</th><th></th></tr></thead>
        <tbody>{rows}</tbody></table>
        <div class="addline"><button class="btn">{IC['plus']}Add line</button>
          <span style="font-size:12.5px;color:var(--tx3)">Unit price comes from the tier. Override it and the change is written to the activity log.</span></div>
      </div>
    </div>

    <div class="card"><div class="h"><h2>Delivery and note</h2></div>
      <div class="b" style="padding:16px 18px 18px">
        <div class="fr c2">
          <div><label>Courier</label><select class="in"><option>Sundarban Courier</option><option>Counter pickup</option><option>Own delivery</option></select></div>
          <div><label>Courier tracking <i>optional</i></label><input class="in" placeholder="Added when the parcel is handed over"></div>
        </div>
        <div><label>Note <i>optional</i></label><textarea class="in" placeholder="Anything the delivery man or the accounts person needs to know."></textarea></div>
      </div>
    </div>
  </div>

  <div class="tot">
    <div class="card"><div class="h"><h2>Totals</h2></div>
      <div class="b" style="padding:4px 18px 18px">
        <div class="row">Subtotal <b>{tk(sub)}</b></div>
        <div class="row">Discount <b>-{tk(disc)}</b></div>
        <div class="row">Delivery <b>{tk(deliv)}</b></div>
        <div class="row big">Total <b>{tk(total)}</b></div>
      </div>
    </div>
    <div class="card" style="margin-top:12px"><div class="h"><h2>Payment</h2></div>
      <div class="b" style="padding:16px 18px 18px">
        <div class="fr c2" style="margin-bottom:10px">
          <div><label>Paid now</label><input class="in r" value="8000" inputmode="numeric"></div>
          <div><label>Method</label><select class="in"><option>Cash</option><option>bKash</option><option>Nagad</option><option>Bank</option></select></div>
        </div>
        <div class="row duerow" style="display:flex;justify-content:space-between;padding:12px 0 0;border-top:1px solid var(--line)">
          <span style="font-weight:600">Due after this sale</span><b style="font-size:20px">{tk(due)}</b></div>
        <div class="auto">{IC['check']}<span><b>Saving this updates:</b> the invoice, Saddam's due and lifetime value,
          stock for 3 products, today's sales and collection, the customer timeline, and every report.
          You never type any of it again.</span></div>
        <button class="btn pri lg" style="width:100%;margin-top:14px">{IC['check']}Save sale</button>
      </div>
    </div>
  </div>
</div>

<p class="note">Single Data Entry is the client's stated condition. One write, many reads.
Everything the dashboard, the customer profile and the reports show is derived from this screen.</p>
'''
    return body


# ═════════════════════════════════════════════════════════════════════════
#  3 · CUSTOMER PROFILE
# ═════════════════════════════════════════════════════════════════════════
def customer_profile():
    PURCH = [('26 Sep 2026','INV-2609-0148',4,12480,12480,0),
             ('11 Sep 2026','INV-2609-0121',9,18900,18900,0),
             ('02 Sep 2026','INV-2609-0094',14,28400,20000,8400),
             ('21 Aug 2026','INV-2608-0331',6,14250,6000,8250),
             ('09 Aug 2026','INV-2608-0287',11,22600,22600,0)]
    PAYS = [('26 Sep 2026','bKash',12480,'INV-2609-0148'),
            ('14 Sep 2026','Cash',18900,'INV-2609-0121'),
            ('05 Sep 2026','Bank',20000,'INV-2609-0094'),
            ('24 Aug 2026','Cash',6000,'INV-2608-0331')]
    pr = ''.join(f'''<tr><td class="mut">{d}</td><td><b>{i}</b></td><td class="r mut">{n}</td>
      <td class="r">{tk(t)}</td><td class="r">{tk(p)}</td>
      <td class="r">{'<span class="pill paid">clear</span>' if u==0 else '<span class="pill due">'+tk(u)+'</span>'}</td></tr>'''
      for d, i, n, t, p, u in PURCH)
    pa = ''.join(f'<tr><td class="mut">{d}</td><td>{m}</td><td class="mut">{i}</td>'
                 f'<td class="r"><b>{tk(a)}</b></td></tr>' for d, m, a, i in PAYS)

    body = f'''
<div class="top">
  <div><h1>Customer profile</h1><div class="sub">Everything on this page is derived. Nothing here was typed twice.</div></div>
  <div class="sp"><span class="srch">{IC['search']}<input placeholder="Search another customer"></span></div>
</div>

<div class="phead">
  <span class="av">S</span>
  <div>
    <h2>Saddam</h2>
    <div class="meta"><span>Mirpur 11, Dhaka</span><i></i><span>01711 234567</span><i></i><span>Customer since 12 Jan 2026</span></div>
    <div class="tags"><span class="tag">Wholesale</span><span class="tag vip">Top 1 customer</span><span class="tag">Dhaka</span></div>
  </div>
  <div class="sp">
    <a class="btn">{IC['wa']}WhatsApp</a>
    <a class="btn" href="#customer-timeline">{IC['time']}Timeline</a>
    <a class="btn pri" href="#sales-entry">{IC['plus']}New sale</a>
  </div>
</div>

<div class="kpis">
  <div class="kpi"><span class="k">Lifetime value</span><span class="v">{tk(268400)}</span><span class="d up">+18% this quarter</span></div>
  <div class="kpi"><span class="k">Total paid</span><span class="v">{tk(123500)}</span><span class="d fl">46% collected</span></div>
  <div class="kpi due"><span class="k">Outstanding due</span><span class="v">{tk(16650)}</span><span class="d fl">oldest 36 days</span></div>
  <div class="kpi"><span class="k">Orders</span><span class="v">31</span><span class="d up">avg {tk(8658)}</span></div>
  <div class="kpi"><span class="k">Customer rank</span><span class="v">#1</span><span class="d fl">of 87 customers</span></div>
</div>

<div class="two">
  <div class="card">
    <div class="h"><h2>Purchase history</h2><span class="sp">last 5 of 31</span></div>
    <div class="b flush"><table class="tb">
      <thead><tr><th>Date</th><th>Invoice</th><th class="r">Items</th><th class="r">Total</th><th class="r">Paid</th><th class="r">Due</th></tr></thead>
      <tbody>{pr}</tbody></table></div>
  </div>
  <div class="card">
    <div class="h"><h2>Payment history</h2><span class="sp">last 4</span></div>
    <div class="b flush"><table class="tb">
      <thead><tr><th>Date</th><th>Method</th><th>Against</th><th class="r">Amount</th></tr></thead>
      <tbody>{pa}</tbody></table></div>
  </div>
</div>

<div class="card">
  <div class="h"><h2>Due history</h2><span class="sp">derived, never stored twice</span></div>
  <div class="b" style="padding:16px 18px 18px">
    <div style="display:flex;gap:26px;flex-wrap:wrap">
      <div><div style="font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--tx3)">Total sold</div>
        <div style="font-size:22px;font-weight:600;letter-spacing:-.03em">{tk(268400)}</div></div>
      <div style="font-size:22px;color:var(--tx3);align-self:flex-end;padding-bottom:2px">−</div>
      <div><div style="font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--tx3)">Total paid</div>
        <div style="font-size:22px;font-weight:600;letter-spacing:-.03em">{tk(251750)}</div></div>
      <div style="font-size:22px;color:var(--tx3);align-self:flex-end;padding-bottom:2px">=</div>
      <div><div style="font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--gold-d)">Due</div>
        <div style="font-size:22px;font-weight:600;letter-spacing:-.03em;color:var(--gold-d)">{tk(16650)}</div></div>
    </div>
    <p class="note" style="margin-top:14px">The money rule that never bends: due equals sold minus paid,
    computed in one place. It is never recomputed in the interface and never stored twice.</p>
  </div>
</div>
'''
    return body


# ═════════════════════════════════════════════════════════════════════════
#  4 · CUSTOMER TIMELINE  — the screen to demo first
# ═════════════════════════════════════════════════════════════════════════
def customer_timeline():
    EV = [
      ('sale','26 Sep 2026','New order · INV-2609-0148',
       'Nutricare 1kg ×6, Avian Eggfood 500g ×12, Spirulina 200g ×4','12,480'),
      ('pay','26 Sep 2026','Payment received · bKash','Paid in full against INV-2609-0148','12,480'),
      ('sale','11 Sep 2026','New order · INV-2609-0121','9 items, delivered by Sundarban Courier','18,900'),
      ('pay','14 Sep 2026','Payment received · Cash','Collected at the factory counter','18,900'),
      ('dueev','02 Sep 2026','Due created · ৳8,400','INV-2609-0094 partially paid on the day','8,400'),
      ('sale','02 Sep 2026','New order · INV-2609-0094','14 items, largest order of the quarter','28,400'),
      ('ret','28 Aug 2026','Return accepted','1 × Avian Eggfood 500g, seal intact, credited','450'),
      ('pay','24 Aug 2026','Payment received · Cash','Part payment against INV-2608-0331','6,000'),
      ('sale','21 Aug 2026','New order · INV-2608-0331','6 items','14,250'),
      ('sale','12 Jan 2026','First order','Nutricare 1kg ×2. Customer since this date.','1,840'),
    ]
    items = ''.join(f'''<div class="tlx {k}">
      <div class="dt">{d}</div><div class="ti">{t}</div>
      <div class="tx">{x} · <span class="amt">৳{a}</span></div></div>''' for k, d, t, x, a in EV)

    body = f'''
<div class="top">
  <div><h1>Customer timeline</h1><div class="sub">Saddam · every order, payment, due and return on one page, in order</div></div>
  <div class="sp"><a class="btn" href="#customer-profile">{IC['cust']}Back to profile</a>
    <a class="btn pri" href="#sales-entry">{IC['plus']}New sale</a></div>
</div>

<div class="chips">
  <button aria-pressed="true">Everything</button><button>Orders</button><button>Payments</button>
  <button>Dues</button><button>Returns</button><button>Follow-ups</button>
</div>

<div class="card">
  <div class="h"><h2>Saddam · Mirpur 11, Dhaka</h2>
    <span class="sp">31 orders · {tk(268400)} lifetime · {tk(16650)} due</span></div>
  <div class="b" style="padding:20px 18px 6px"><div class="tl">{items}</div></div>
  <div class="legend">
    <span><i style="background:#089830"></i>Order</span>
    <span><i style="background:#2FAF55"></i>Payment</span>
    <span><i style="background:#E0B810"></i>Due created</span>
    <span><i style="background:#C0392B"></i>Return</span>
    <span style="margin-left:auto;color:var(--tx3)">A union view over orders, payments, returns and follow-ups, ordered by date. Nothing here is a separate entry.</span>
  </div>
</div>

<p class="note">This is the screen to demo first. It is the single most convincing proof that the
double entry is gone: everything on it was written once, at the sales entry screen.</p>
'''
    return body



# ═════════════════════════════════════════════════════════════════════════
#  5 · INVENTORY   — his Stage 1.4: raw material, finished product,
#                     current stock, stock alert
# ═════════════════════════════════════════════════════════════════════════
def inventory():
    RAW = [('Maize flour','kg',420,150,'ok'),('Soya protein','kg',95,120,'low'),
           ('Calcium carbonate','kg',210,80,'ok'),('Spirulina powder','kg',18,25,'critical'),
           ('Moringa leaf powder','kg',64,40,'ok'),('Beetroot powder','kg',52,40,'ok')]
    FIN = [('Nutricare Hand Feeding','1kg',18,40,'low'),('Nutricare Hand Feeding','500g',96,40,'ok'),
           ('Avian Eggfood','1kg',54,30,'ok'),('Avian Eggfood','500g',7,30,'critical'),
           ('Avian Spirulina','200g',24,25,'low'),('Avian Herbs','200g',51,25,'ok'),
           ('Avian Moringa','200g',62,25,'ok'),('Avian Beetroot','200g',73,25,'ok')]
    MOV = [('26 Sep','Out','Nutricare 1kg',-6,'INV-2609-0148'),
           ('26 Sep','Out','Avian Eggfood 500g',-12,'INV-2609-0148'),
           ('25 Sep','In','Nutricare 1kg',+120,'Production batch B-0912'),
           ('24 Sep','Out','Avian Spirulina 200g',-4,'INV-2609-0141'),
           ('23 Sep','In','Avian Eggfood 500g',+80,'Production batch B-0908')]
    def pill(s_):
        return f'<span class="pill {"crit" if s_=="critical" else ("low" if s_=="low" else "ok")}">{s_}</span>'
    raw = ''.join(f'<tr><td>{n}</td><td class="r mut">{u}</td><td class="r"><b>{q}</b></td>'
                  f'<td class="r mut">{r}</td><td class="r">{pill(st)}</td></tr>' for n,u,q,r,st in RAW)
    fin = ''.join(f'<tr><td>{n}</td><td class="mut">{p}</td><td class="r"><b>{q}</b></td>'
                  f'<td class="r mut">{r}</td><td class="r">{pill(st)}</td></tr>' for n,p,q,r,st in FIN)
    mov = ''.join(f'<tr><td class="mut">{d}</td>'
                  f'<td><span class="pill {"web" if t=="In" else "man"}">{t}</span></td>'
                  f'<td>{n}</td><td class="r"><b>{"+" if q>0 else ""}{q}</b></td>'
                  f'<td class="mut">{ref}</td></tr>' for d,t,n,q,ref in MOV)
    body = f"""
<div class="top"><div><h1>Inventory</h1>
  <div class="sub">Raw material, finished product, current stock and alerts. Stock moves when a sale is saved, never by hand.</div></div>
  <div class="sp"><a class="btn">{IC['plus']}Stock in</a><a class="btn pri">{IC['plus']}New production batch</a></div>
</div>
<div class="chips"><button aria-pressed="true">All</button><button>Raw material</button>
  <button>Finished product</button><button>Below reorder</button><button>Movements</button></div>
<div class="kpis">
  <div class="kpi"><span class="k">Finished stock value</span><span class="v">{tk(842300)}</span><span class="d up">+6% this month</span></div>
  <div class="kpi"><span class="k">Raw material value</span><span class="v">{tk(318900)}</span><span class="d fl">6 materials</span></div>
  <div class="kpi alert"><span class="k">Below reorder</span><span class="v">4</span><span class="d fl">2 critical</span></div>
  <div class="kpi"><span class="k">Batches this month</span><span class="v">7</span><span class="d up">+2</span></div>
</div>
<div class="two">
  <div class="card"><div class="h"><h2>Finished product</h2><span class="sp">qty / reorder level</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Product</th><th>Pack</th><th class="r">Stock</th><th class="r">Reorder</th><th class="r">Status</th></tr></thead><tbody>{fin}</tbody></table></div></div>
  <div class="card"><div class="h"><h2>Raw material</h2><span class="sp">qty / reorder level</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Material</th><th class="r">Unit</th><th class="r">Stock</th><th class="r">Reorder</th><th class="r">Status</th></tr></thead><tbody>{raw}</tbody></table></div></div>
</div>
<div class="card"><div class="h"><h2>Stock movements</h2><span class="sp">append-only ledger, never edited in place</span></div>
  <div class="b flush"><table class="tb"><thead><tr><th>Date</th><th>Type</th><th>Item</th><th class="r">Qty</th><th>Reference</th></tr></thead><tbody>{mov}</tbody></table></div></div>
<p class="note">Stock is an append-only ledger. Current stock is the running total, never a number
somebody typed. That is what makes a stock figure auditable a year later.</p>
"""
    return body


# ═════════════════════════════════════════════════════════════════════════
#  6 · ACCOUNTS   — his Stage 1.5: cash, bank, expense, receivable, payable
# ═════════════════════════════════════════════════════════════════════════
def accounts():
    TXN = [('26 Sep','Collection','Saddam · bKash','in',12480,'Cash'),
           ('26 Sep','Expense','Sundarban Courier, September','out',8400,'Bank'),
           ('25 Sep','Collection','Rafiq · Cash','in',18900,'Cash'),
           ('24 Sep','Expense','Maize flour, 200kg','out',46000,'Bank'),
           ('23 Sep','Collection','Nazmul · Bank transfer','in',20000,'Bank'),
           ('22 Sep','Expense','Jar and label printing','out',18700,'Cash'),
           ('21 Sep','Collection','Mamun · bKash','in',6000,'Cash')]
    PAY = [('Maize supplier, Bhaluka',86000,'12 days'),('Jar supplier, Dhaka',34500,'5 days'),
           ('Courier account',8400,'due today')]
    txn = ''.join(f'<tr><td class="mut">{d}</td><td>{k}</td><td>{w}</td>'
                  f'<td class="r"><b style="color:{"var(--brand)" if t=="in" else "var(--red)"}">'
                  f'{"+" if t=="in" else "-"}{tk(a)}</b></td>'
                  f'<td class="r"><span class="pill man">{acc}</span></td></tr>'
                  for d,k,w,t,a,acc in TXN)
    pay = ''.join(f'<tr><td>{n}</td><td class="r"><b>{tk(v)}</b></td>'
                  f'<td class="r"><span class="pill {"due" if "today" in w else "man"}">{w}</span></td></tr>'
                  for n,v,w in PAY)
    body = f"""
<div class="top"><div><h1>Accounts</h1>
  <div class="sub">Cash, bank, expense, receivable and payable. Receivable is the same due figure the dashboard shows, computed once.</div></div>
  <div class="sp"><a class="btn">{IC['plus']}Record expense</a><a class="btn pri">{IC['plus']}Record collection</a></div>
</div>
<div class="chips"><button aria-pressed="true">This month</button><button>Today</button>
  <button>This week</button><button>This year</button><button>Custom range</button></div>
<div class="kpis">
  <div class="kpi"><span class="k">Cash in hand</span><span class="v">{tk(94200)}</span><span class="d up">+{tk(11900)} today</span></div>
  <div class="kpi"><span class="k">Bank balance</span><span class="v">{tk(612800)}</span><span class="d dn">-{tk(8400)} today</span></div>
  <div class="kpi"><span class="k">Expense this month</span><span class="v">{tk(287400)}</span><span class="d dn">+14% vs August</span></div>
  <div class="kpi due"><span class="k">Receivable</span><span class="v">{tk(486300)}</span><span class="d fl">34 customers</span></div>
  <div class="kpi"><span class="k">Payable</span><span class="v">{tk(128900)}</span><span class="d fl">3 suppliers</span></div>
</div>
<div class="wide">
  <div class="card"><div class="h"><h2>Transactions</h2><span class="sp">collections and expenses, newest first</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Date</th><th>Kind</th><th>Detail</th><th class="r">Amount</th><th class="r">Account</th></tr></thead><tbody>{txn}</tbody></table></div></div>
  <div class="card"><div class="h"><h2>Payable</h2><span class="sp">what we owe</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Supplier</th><th class="r">Amount</th><th class="r">Due in</th></tr></thead><tbody>{pay}</tbody></table></div></div>
</div>
<p class="note">Receivable is not a separate number. It is the same
<b>total sold minus total paid</b> the dashboard and every customer profile use. One figure,
one place, so the books can never disagree with the dashboard.</p>
"""
    return body


# ═════════════════════════════════════════════════════════════════════════
#  7 · REPORTS  — his Stage 1.6: daily, weekly, monthly, yearly,
#                 product-wise, customer-wise, district-wise
# ═════════════════════════════════════════════════════════════════════════
def reports():
    DIST = [('Dhaka',487200,31,'+18%'),('Chattogram',218400,17,'+9%'),('Mymensingh',164900,14,'+22%'),
            ('Rajshahi',131700,11,'-4%'),('Khulna',118300,9,'+6%'),('Sylhet',97500,8,'+12%'),
            ('Rangpur',88200,7,'+3%'),('Barishal',61300,5,'-2%')]
    MONTH = [('September 2026',486300,142,'+16%'),('August 2026',419100,128,'+8%'),
             ('July 2026',388200,119,'+11%'),('June 2026',349700,106,'+4%')]
    dist = ''.join(f'<tr><td><b>{n}</b></td><td class="r">{tk(v)}</td><td class="r mut">{c}</td>'
                   f'<td class="r"><span class="pill {"ok" if g.startswith("+") else "crit"}">{g}</span></td></tr>'
                   for n,v,c,g in DIST)
    mon = ''.join(f'<tr><td>{m}</td><td class="r"><b>{tk(v)}</b></td><td class="r mut">{o} orders</td>'
                  f'<td class="r"><span class="pill {"ok" if g.startswith("+") else "crit"}">{g}</span></td></tr>'
                  for m,v,o,g in MONTH)
    prod = ''.join(f'<tr><td><span class="rank {"t"+str(i) if i<=3 else ""}">{i}</span>{n}</td>'
                   f'<td class="r mut">{q}</td><td class="r"><b>{tk(v)}</b></td></tr>'
                   for i,(n,q,v) in enumerate(TOP_PROD[:6],1))
    cards = ''.join(f"""<button class="rep">{IC[ic]}<span><b>{t}</b><em>{d}</em></span></button>"""
                    for t,d,ic in [
      ('Daily report','Every sale, collection and expense for one day','report'),
      ('Weekly report','Seven days, compared with the week before','report'),
      ('Monthly report','The month, by product and by district','report'),
      ('Yearly report','Twelve months, growth and seasonality','report'),
      ('Product-wise','Quantity and value for every pack size','stock'),
      ('Customer-wise','Purchases, payments and due per customer','cust'),
      ('District-wise','All 64 districts, ranked by value','dash')])
    body = f"""
<div class="top"><div><h1>Reports</h1>
  <div class="sub">Seven report types. Every one reads the same sales ledger, so no two reports can disagree.</div></div>
  <div class="sp"><a class="btn">{IC['report']}Export Excel</a><a class="btn">{IC['report']}Export PDF</a><a class="btn pri">{IC['report']}Print</a></div>
</div>
<div class="repgrid">{cards}</div>
<div class="two">
  <div class="card"><div class="h"><h2>District-wise</h2><span class="sp">this year, top 8 of 64</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>District</th><th class="r">Sales</th><th class="r">Customers</th><th class="r">vs last year</th></tr></thead><tbody>{dist}</tbody></table></div></div>
  <div class="card"><div class="h"><h2>Monthly</h2><span class="sp">last 4 months</span></div>
    <div class="b flush"><table class="tb"><thead><tr><th>Month</th><th class="r">Sales</th><th class="r">Orders</th><th class="r">Growth</th></tr></thead><tbody>{mon}</tbody></table></div></div>
</div>
<div class="card"><div class="h"><h2>Product-wise</h2><span class="sp">this year</span></div>
  <div class="b flush"><table class="tb"><thead><tr><th>Product</th><th class="r">Qty</th><th class="r">Value</th></tr></thead><tbody>{prod}</tbody></table></div></div>
<p class="note">Every report is a query over the same append-only sales ledger. Nothing is
re-keyed, so a district report and a product report always add up to the same total.</p>
"""
    return body


# ═════════════════════════════════════════════════════════════════════════
#  8 · SETTINGS  — his Stage 1.7 Admin + Stage 2.10 System Settings
# ═════════════════════════════════════════════════════════════════════════
def settings():
    USERS = [('Anowar Bhai','Owner','All modules','Active'),
             ('Accounts staff','Accountant','Accounts, Reports','Active'),
             ('Sales staff','Sales','Sales entry, Customers','Active'),
             ('Factory','Stock','Inventory only','Active')]
    LOG = [('26 Sep 14:22','Sales staff','Created sale INV-2609-0148','—','৳12,480'),
           ('26 Sep 14:25','Accounts staff','Recorded payment','—','৳12,480'),
           ('26 Sep 11:04','Anowar Bhai','Changed unit price, Nutricare 1kg','৳690','৳680'),
           ('25 Sep 17:40','Factory','Production batch B-0912','—','+120 units'),
           ('25 Sep 09:12','Anowar Bhai','Added customer, Imran','—','Mymensingh')]
    users = ''.join(f'<tr><td><b>{n}</b></td><td>{r}</td><td class="mut">{p}</td>'
                    f'<td class="r"><span class="pill ok">{s_}</span></td></tr>' for n,r,p,s_ in USERS)
    log = ''.join(f'<tr><td class="mut">{d}</td><td>{u}</td><td>{a}</td>'
                  f'<td class="r mut">{b}</td><td class="r"><b>{af}</b></td></tr>' for d,u,a,b,af in LOG)
    def panel(t, rows):
        r = ''.join(f'<div class="setrow"><span>{k}</span><b>{v}</b></div>' for k,v in rows)
        return f'<div class="card"><div class="h"><h2>{t}</h2></div><div class="b" style="padding:6px 18px 14px">{r}</div></div>'
    body = f"""
<div class="top"><div><h1>Settings</h1>
  <div class="sub">Company, invoice, payment methods, couriers, banks, users, roles, activity log and backup.</div></div>
  <div class="sp"><a class="btn">{IC['report']}Download backup</a><a class="btn pri">{IC['check']}Save changes</a></div>
</div>
<div class="chips"><button aria-pressed="true">Company</button><button>Invoice</button>
  <button>Payment methods</button><button>Couriers</button><button>Bank accounts</button>
  <button>Users and roles</button><button>Activity log</button><button>Backup</button></div>
<div class="two">
  {panel('Company information', [('Name','Shada Bird Feed'),('Factory','Majorvita, Bhaluka, Mymensingh'),
    ('Phone','01813-323535'),('Email','shadabirdfeed@gmail.com'),('Trade licence','[CONFIRM]'),('BIN','[CONFIRM]')])}
  {panel('Invoice settings', [('Prefix','INV-'),('Format','INV-YYMM-0000'),('Next number','0149'),
    ('Currency','BDT, lakh grouping'),('Print size','A5 and 80mm thermal'),('Language','English and Bangla')])}
</div>
<div class="two">
  {panel('Payment methods', [('Cash','Enabled'),('bKash','[CONFIRM]'),('Nagad','[CONFIRM]'),
    ('Bank transfer','[CONFIRM]'),('Cash on delivery','[CONFIRM]')])}
  {panel('Couriers and banks', [('Sundarban Courier','Default'),('Counter pickup','Enabled'),
    ('Own delivery','Enabled'),('Bank account 1','[CONFIRM]'),('Bank account 2','[CONFIRM]')])}
</div>
<div class="card" style="margin-bottom:14px"><div class="h"><h2>Users, roles and permissions</h2>
  <span class="sp">built on WordPress roles and capabilities</span></div>
  <div class="b flush"><table class="tb"><thead><tr><th>User</th><th>Role</th><th>Can access</th><th class="r">Status</th></tr></thead><tbody>{users}</tbody></table></div></div>
<div class="card"><div class="h"><h2>Activity log</h2><span class="sp">who changed what, with the value before and after</span></div>
  <div class="b flush"><table class="tb"><thead><tr><th>When</th><th>User</th><th>Action</th><th class="r">Before</th><th class="r">After</th></tr></thead><tbody>{log}</tbody></table></div></div>
<p class="note">Roles use WordPress capabilities rather than a parallel permission system, so there
is one place a user is granted or revoked access. The activity log records the value before and
after every change, which is what his Stage 2.8 asked for.</p>
"""
    return body


# ═════════════════════════════════════════════════════════════════════════
#  EXTRA CSS for the four new views
# ═════════════════════════════════════════════════════════════════════════
CSS2 = '''
/* report type cards */
.repgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:11px;margin-bottom:14px}
.repgrid>*{min-width:0}
.rep{display:flex;align-items:flex-start;gap:11px;text-align:left;background:#fff;
  border:1px solid var(--line);border-radius:var(--r2);padding:15px 16px;transition:all .15s;width:100%}
.rep:hover{border-color:var(--brand);box-shadow:0 6px 16px rgba(8,152,48,.08)}
.rep svg{width:19px;height:19px;color:var(--brand);flex:0 0 auto;margin-top:1px}
.rep b{display:block;font-size:14.5px;font-weight:600;letter-spacing:-.012em}
.rep em{display:block;font-style:normal;font-size:12.5px;color:var(--tx2);line-height:1.45;margin-top:3px}

/* settings key-value rows */
.setrow{display:flex;justify-content:space-between;gap:14px;padding:11px 0;
  border-bottom:1px solid var(--line);font-size:14px;color:var(--tx2);min-width:0}
.setrow:last-child{border-bottom:0}
.setrow b{color:var(--tx);font-weight:600;text-align:right;min-width:0;word-break:break-word}

/* views: only the routed one is shown */
.view{display:none}
.view.on{display:block}
'''


def build_one():
    views = {'dashboard': dashboard(), 'sales-entry': sales_entry(),
             'customer-profile': customer_profile(), 'customer-timeline': customer_timeline(),
             'inventory': inventory(), 'accounts': accounts(),
             'reports': reports(), 'settings': settings()}
    titles = {k: t for k, t, _ in NAV}
    sections = ''.join(
        f'<section class="view{" on" if k=="dashboard" else ""}" id="v-{k}" '
        f'data-title="{titles[k]}">{v}</section>' for k, v in views.items())

    js = '''
/* ═══════════════════════════════════════════════════════════════════════
   Hash router. Eight views in one file, so every menu is clickable without
   opening eight files. Nothing here ships to production: the real plugin
   renders each screen server-side from its own module.
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
  var views = document.querySelectorAll('.view');
  var links = document.querySelectorAll('.rail a[data-go]');

  function go(name) {
    var found = false;
    views.forEach(function (v) {
      var on = v.id === 'v-' + name;
      v.classList.toggle('on', on);
      if (on) { found = true; document.title = v.dataset.title + ' · Shada BMS'; }
    });
    if (!found) { go('dashboard'); return; }
    links.forEach(function (a) {
      a.classList.toggle('on', a.dataset.go === name);
    });
    window.scrollTo(0, 0);
  }

  function fromHash() {
    go((location.hash || '#dashboard').slice(1));
  }

  window.addEventListener('hashchange', fromHash);
  fromHash();

  /* any in-page link with a hash route works too, not just the rail */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    var name = a.getAttribute('href').slice(1);
    if (document.getElementById('v-' + name)) {
      e.preventDefault();
      if (location.hash !== '#' + name) location.hash = name; else go(name);
    }
  });
})();
'''

    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard · Shada BMS</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}{CSS2}</style></head><body>
<div class="demo">DEMO DATA · Phase 0 prototype for approval · all 8 menus are clickable · no real customer or sales data</div>
<div class="app">{rail()}<main class="main">{sections}</main></div>
<script>{js}</script>
</body></html>'''


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    html = build_one()
    open(f'{OUT}/shada-bms-prototype.html', 'w', encoding='utf-8').write(html)
    print(f'shada-bms-prototype.html  {round(len(html)/1024)} KB  ·  {len(NAV)} menus in one file')
