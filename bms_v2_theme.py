"""
Shada BMS · v2 theme ("Weborite" layout).
Reads the v1 build (shada-bms-prototype.html), keeps every screen and every line of behaviour,
and layers a second visual system on top:

  • one dark-green top bar across the full width (brand mark, crumb pill, search pill, bell, date, New sale)
  • the rail becomes a floating dark-green panel below it, white active pill, colour-dot groups
  • light grey canvas, 16px-radius white cards, KPI tiles with a round icon and a 32px number
  • black/green pill buttons, rounded segmented controls, softer tables

Output: shada-bms-prototype-v2.html (next to v1). v1 is untouched; v1 is also copied to
shada-bms-prototype-v1.html so the two can be opened side by side.
Every string replace asserts count==1 (rule 16).
"""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SCREENS = os.path.dirname(HERE)
V1 = os.path.join(SCREENS, 'shada-bms-prototype.html')
V1COPY = os.path.join(SCREENS, 'shada-bms-prototype-v1.html')
V2 = os.path.join(SCREENS, 'shada-bms-prototype-v2.html')

THEME = r'''
/* ═══ Shada BMS · v2 theme · green top bar + floating rail + light canvas (28 Sep 2026) ═══ */
:root{
  --g:#1E5A3E; --g-2:#174A32; --g-3:#245F44; --g-line:rgba(255,255,255,.14); --g-pill:rgba(255,255,255,.12);
  --paper-2:#EEF1EE; --paper-3:#E6EAE6; --line:#E4E8E4; --line-2:#D6DCD6;
  --brand:#1E5A3E; --brand-600:#174A32; --brand-700:#123A27; --brand-tint:#E7F0EA; --brand-ring:rgba(30,90,62,.22);
  --ok:#1E8A4C; --ok-bg:#E7F3EB;
  --r2:14px; --r3:16px; --r4:18px; --rail:232px; --topbar:64px; --gap:16px;
  --e1:0 1px 2px rgba(20,40,30,.04); --e2:0 4px 14px -6px rgba(20,40,30,.10),0 1px 2px rgba(20,40,30,.04);
}
body{background:var(--paper-2);color:#2A2F2C}
b,strong,h1,h2,h3{color:#161A18}

/* ── layout: top bar spans everything; rail and canvas sit below it ── */
.app{grid-template-columns:var(--rail) minmax(0,1fr);grid-template-rows:auto minmax(0,1fr);
  column-gap:var(--gap);padding:var(--gap);min-height:100vh}
.app>.mainwrap{display:contents}
.top{grid-column:1/-1;grid-row:1;position:sticky;top:var(--gap);z-index:40;
  background:var(--g);border:0;border-radius:16px;padding:10px 12px;height:var(--topbar);
  box-shadow:0 10px 30px -18px rgba(20,60,40,.55);gap:8px;margin-bottom:var(--gap);
  backdrop-filter:none;-webkit-backdrop-filter:none}
.rail{grid-column:1;grid-row:2;position:sticky;top:calc(var(--topbar) + var(--gap)*2);
  height:calc(100vh - var(--topbar) - var(--gap)*3);border-radius:16px;background:var(--g);
  background-image:none;box-shadow:0 10px 30px -18px rgba(20,60,40,.55);overflow:hidden}
main.canvas{grid-column:2;grid-row:2;padding:8px 8px 80px;max-width:none}

/* ── top bar pieces ── */
.tbrand{display:flex;align-items:center;gap:10px;padding:0 6px 0 2px;color:#fff;font-weight:700;font-size:14px;letter-spacing:-.2px}
.tbrand .mark{width:34px;height:34px;border-radius:9px;background:#0F3B27;box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}
.tbrand .mark svg{width:19px;height:19px}
.top .crumb{background:var(--g-pill);color:rgba(255,255,255,.92);border-radius:11px;height:40px;padding:0 14px;
  font-size:13px;font-weight:500;align-items:center;gap:6px;white-space:nowrap}
.top .crumb b{color:#fff}
.top .crumb span{color:rgba(255,255,255,.5)!important}
.top .gsearch{margin-left:0;width:300px;max-width:32vw}
.top .gsearch input{height:40px;border:0;background:var(--g-pill);color:#fff;border-radius:11px;padding-left:36px;box-shadow:none;font-size:13.5px}
.top .gsearch input::placeholder{color:rgba(255,255,255,.62)}
.top .gsearch input:focus{background:rgba(255,255,255,.18);box-shadow:0 0 0 3px rgba(255,255,255,.18);border:0}
.top .gsearch svg{stroke:rgba(255,255,255,.8)}
.top .kbd{border-color:rgba(255,255,255,.25);background:transparent;color:rgba(255,255,255,.6)}
.top .cbxlist{color:var(--ink-2)}
.top .iconbtn{width:40px;height:40px;border:0;background:var(--g-pill);border-radius:11px;box-shadow:none}
.top .iconbtn svg{stroke:#fff}
.top .iconbtn:hover{background:rgba(255,255,255,.2);transform:none}
.top .dot-n{border-color:var(--g);background:#FF7A59}
.top .notif{color:var(--ink-2)}
.tdate{margin-left:auto;display:inline-flex;align-items:center;gap:8px;height:40px;padding:0 14px;border-radius:11px;
  background:var(--g-pill);color:rgba(255,255,255,.92);font-size:13px;font-weight:500;white-space:nowrap}
.tdate svg{width:15px;height:15px;stroke:rgba(255,255,255,.85)}
.top .btn-p{height:40px;border-radius:11px;background:#fff;border-color:#fff;color:var(--g);font-weight:650;padding:0 16px;box-shadow:none}
.top .btn-p svg{stroke:var(--g)}
.top .btn-p:hover{background:#F2F6F3;transform:none}
.top .btn-p::after{content:"→";font-size:15px;margin-left:2px}

/* ── rail ── */
.brandrow{padding:18px 16px 8px}
.brandrow .mark{display:none}
.bn{font-size:15px;font-weight:700;color:#fff}
.bs{color:rgba(255,255,255,.5);letter-spacing:.06em;font-size:10px}
.navgrp{color:rgba(255,255,255,.5);font-weight:600;letter-spacing:.09em;padding:14px 18px 6px;margin-top:0;position:relative}
.navgrp::before{content:"";position:absolute;left:16px;right:16px;top:4px;height:1px;background:var(--g-line)}
.rail>.navgrp:first-of-type::before{display:none}
.nav{padding:0 12px;gap:2px}
.nav a{color:rgba(255,255,255,.86);border-radius:12px;padding:10px 12px;font-size:14px;font-weight:500}
.nav a svg{opacity:.9;stroke:currentColor}
.nav a:hover{background:rgba(255,255,255,.08);color:#fff;transform:none}
.nav a[aria-current="page"]{background:#fff;color:var(--g);font-weight:650;box-shadow:0 4px 12px -6px rgba(0,0,0,.35)}
.nav a[aria-current="page"] svg{stroke:var(--g);transform:none;opacity:1}
.nav a[aria-current="page"]::before{display:none}
.nbadge{background:rgba(255,255,255,.14);color:#fff}
.nav a[aria-current="page"] .nbadge{background:var(--g);color:#fff}
.railfoot{border-top:1px solid var(--g-line);padding:14px 16px}
.who .av{background:#fff;color:var(--g);border-radius:9px}
.who .wn{color:#fff} .who .wr{color:rgba(255,255,255,.55)}

/* ── page head ── */
.ph{margin-bottom:22px;align-items:center}
.ph h1{font-size:30px;font-weight:650;letter-spacing:-.8px}
.ph h1::before{content:attr(data-eyebrow);display:block;font-size:13px;font-weight:500;color:#6E756F;letter-spacing:0;margin-bottom:6px}
.ph p{font-size:13.5px;color:#6E756F}
.ph .meta{border-radius:10px;border-color:var(--line)}

/* ── cards ── */
.card{border-radius:16px;border:1px solid var(--line);box-shadow:var(--e1)}
.ch{padding:18px 20px 12px;border-bottom:0;min-height:0;flex-wrap:wrap}
.ch h3{font-size:18px;font-weight:650;letter-spacing:-.4px}
.ch .sub{width:100%;order:9;margin-top:2px;font-size:13px}
.ch .hi{display:none}
.cb{padding:8px 20px 18px}
.cb.flush{padding:0}
th{padding:10px 20px;color:#6E756F;font-weight:500;font-size:12.5px;border-bottom:1px solid var(--line)}
td{padding:13px 20px}
tbody tr:hover td{background:#FAFBFA}
.pill{border-radius:999px;padding:3px 9px;font-size:12px;font-weight:600}
.pill.ok,.pill.paid{background:#E7F3EB;color:#1E6B3F}
.pill.ok::before,.pill.paid::before{content:"";width:6px;height:6px;border-radius:50%;background:#1E8A4C;display:inline-block}
.pill.web{background:#E8EFFA;color:#2F5AA8}
.pill.due{background:#FCEFDD;color:#8A5A12}
.pill.bad{background:#FCE4E1;color:#A32D22}
.pill.man{background:#EEF1EE;color:#4B534E}

/* ── KPI tiles: round icon top-left, big number, label below ── */
.kpis{gap:16px}
.kpi{border-radius:16px;padding:18px 18px 16px;display:flex;flex-direction:column;box-shadow:var(--e1);min-height:132px}
.kl{order:2;margin:2px 0 0;font-size:13px;color:#6E756F;font-weight:500;position:static}
.kl svg{position:absolute;top:18px;left:18px;width:40px;height:40px;padding:11px;border-radius:50%;background:#F0F3F0;stroke:var(--g)}
.kpi.due .kl svg{background:#FCEFDD;stroke:#8A5A12}
.kv{order:1;margin-top:46px;font-size:32px;letter-spacing:-1.2px;font-weight:700}
.d{order:3;margin-top:4px}

/* ── controls ── */
.btn{border-radius:10px;height:38px;border-color:var(--line-2);box-shadow:none;font-weight:550}
.btn:hover{transform:none;border-color:#B9C2BB;background:#F7F9F7}
.btn-p{background:#161A18;border-color:#161A18;color:#fff}
.btn-p:hover{background:#000;border-color:#000}
.btn-p svg{stroke:#fff}
.btn-d{background:#fff;color:#A32D22;border-color:#F0C9C4}
.btn-xs{height:30px;border-radius:9px}
.btn-lg{height:46px;border-radius:12px;font-size:15px}
.ibtn{border-radius:9px}
.seg{border-radius:11px;background:#fff;border-color:var(--line);padding:3px;box-shadow:none}
.seg button{border-radius:8px;height:30px;font-weight:500}
.seg button[aria-pressed="true"]{background:var(--g);color:#fff;box-shadow:none}
.inp,.money,select.inp{border-radius:10px;border-color:var(--line-2)}
.inp:focus{border-color:var(--g);box-shadow:0 0 0 3px var(--brand-ring)}
.hi{border-radius:9px;background:var(--brand-tint)}
.sheet{border-radius:18px}
.sheet .ch{border-bottom:1px solid var(--line)}
.sheet .ch .hi{display:grid}
.tag,.rank{border-radius:999px}
.pcard{border-radius:16px}
.prog{border-radius:99px}
.notif .opt{border-radius:12px}
.chartbox{border-radius:12px}
.toast{border-radius:12px;background:#161A18}

/* ── 1001–1180px: v1 collapses the rail to icons here; v2 keeps labels (a narrower 200px rail) so nothing is lost ── */
@media (max-width:1180px) and (min-width:781px){
  :root{--rail:200px}
  .brandrow{display:flex;justify-content:flex-start;padding:16px 14px 6px}
  .bn,.bs,.navgrp,.who .wn,.who .wr{display:block}
  .nav a span:not(.ic){display:inline}
  .nbadge{display:inline-flex}
  .nav a{justify-content:flex-start;padding:9px 10px;font-size:13.5px;border-radius:11px}
  .navgrp::before{left:12px;right:12px}
  .top .crumb{display:inline-flex;padding:0 10px;font-size:12.5px}
  .top .gsearch{width:220px}
  .top .btn-p{padding:0 12px}
}
/* ── 781–1000px: icon rail (same as v1's tablet mode), crumb stays ── */
@media (max-width:1000px) and (min-width:781px){
  :root{--rail:68px}
  .brandrow{display:none}
  .bn,.bs,.navgrp,.who .wn,.who .wr{display:none}
  .nav a span:not(.ic){display:none}
  .nbadge{display:none}
  .nav a{justify-content:center;padding:12px 0;border-radius:12px}
  .tbrand span+*{display:none}
  .tdate{display:none}
}
/* ── phones: green bottom bar, full-width top bar ── */
@media (max-width:780px){
  .app{padding:0;grid-template-columns:minmax(0,1fr);column-gap:0}
  .top{grid-column:1;border-radius:0 0 16px 16px;margin-bottom:0;top:0;height:auto;min-height:60px;padding:8px 10px}
  .rail{grid-column:1;position:fixed;top:auto;height:auto;border-radius:16px 16px 0 0;background:var(--g);box-shadow:0 -10px 30px -18px rgba(20,60,40,.6)}
  .nav a{border-radius:11px}
  .nav a[aria-current="page"]{background:#fff;color:var(--g)}
  .nav a[aria-current="page"] .nbadge{background:var(--g)}
  main.canvas{grid-column:1;padding:14px 12px calc(96px + env(safe-area-inset-bottom,0px))}
  .tbrand,.tdate,.top .kbd{display:none}
  .top .gsearch{width:auto;flex:1;max-width:none}
  .top .btn-p{width:44px;height:40px;padding:0}
  .top .btn-p::after{display:none}
  .ph h1{font-size:24px}
  /* keep v1's phone tap targets (42/44px) */
  .btn{height:44px} .btn-xs{height:42px} .btn-lg{height:48px} .seg button{height:42px} .ibtn{width:42px;height:42px}
  .kv{font-size:26px;margin-top:44px}
  .kl svg{width:36px;height:36px;padding:9px}
}
'''

MARK = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19c4-9 10-13 16-14-1 6-5 12-14 16"/><path d="M4 19l5-5"/></svg>'
CAL = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>'


def rep(s, a, b, n=1):
    c = s.count(a)
    assert c == n, (a[:70], c)
    return s.replace(a, b)


def build():
    s = open(V1, encoding='utf-8').read()
    # today, as the ledger knows it (TODAY in bms_pro): read the first "NN Sep 2026" style token from the page header data
    import re
    m = re.search(r'\b(\d{1,2}) (Sep|Oct|Nov|Dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug)[a-z]* 2026\b', s)
    today = ('%s %s 2026' % (m.group(1), m.group(2))) if m else '26 Sep 2026'
    s = rep(s, '<title>', '<title>v2 · ')
    s = rep(s, '</head>', '<style id="v2-theme">' + THEME + '</style>\n</head>')
    s = rep(s, '</aside>\n<div style="min-width:0">\n<header class="top">',
            '</aside>\n<div class="mainwrap" style="min-width:0">\n<header class="top"><div class="tbrand"><span class="mark">' + MARK + '</span>Shada BMS</div>')
    s = rep(s, 'typed by hand.</div></div></div><a class="btn btn-p" href="#sales-entry">',
            'typed by hand.</div></div></div><span class="tdate">' + CAL + today + '</span><a class="btn btn-p" href="#sales-entry">')
    # eyebrow above each page title: the section name from the crumb is dynamic, so use a static "Shada BMS"
    s = s.replace('<div class="ph"><div><h1>', '<div class="ph"><div><h1 data-eyebrow="Shada BMS">')
    assert 'data-eyebrow' in s
    open(V2, 'w', encoding='utf-8').write(s)
    shutil.copyfile(V1, V1COPY)
    print('v2 built', len(s), 'bytes ·', today)


if __name__ == '__main__':
    build()
