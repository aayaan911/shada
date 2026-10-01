# -*- coding: utf-8 -*-
"""Shada BMS · the visual layer.

Brief from Ayaan: this is shown to a founder running a 15-person, 1-crore
company. It has to read like Linear, Stripe or Ramp, not like a WordPress
admin page. So: a real elevation scale, one accent colour used sparingly,
tabular figures everywhere money appears, and motion that is fast and
purposeful. Every animation is under 320ms and respects prefers-reduced-motion,
because half the audience is on a cheap Android.
"""

CSS = r'''
/* ══════════════════════════════════════════════════════════════════════════
   1 · TOKENS
   One accent (Shada green). Everything else is a neutral ramp. Semantic
   colour appears only where it carries meaning: money owed, stock risk, new.
   ══════════════════════════════════════════════════════════════════════════ */
:root{
  --brand:#089830; --brand-600:#067a27; --brand-700:#05631f;
  --brand-tint:#E8F6EC; --brand-ring:rgba(8,152,48,.28);

  --ink:#30313D; --ink-2:#414552; --ink-3:#687385; --ink-4:#8792A2;
  --line:#E3E8EE; --line-2:#D5DBE1;
  --paper:#FFFFFF; --paper-2:#F6F8FA; --paper-3:#EEF1F5;

  --ok:#089830; --ok-bg:#E8F6EC;
  --warn:#B45309; --warn-bg:#FEF3E2;
  --bad:#B42318; --bad-bg:#FEE4E2;
  --info:#175CD3; --info-bg:#EFF4FF;

  /* elevation, tinted with the brand hue so shadows never look grey-dirty */
  --e1:0 1px 1px rgba(48,49,61,.04);
  --e2:0 2px 5px rgba(48,49,61,.06), 0 1px 1px rgba(48,49,61,.04);
  --e3:0 8px 24px -6px rgba(11,18,32,.12), 0 2px 6px rgba(11,18,32,.05);
  --e4:0 24px 60px -12px rgba(11,18,32,.22), 0 8px 20px -8px rgba(11,18,32,.10);

  --r1:6px; --r2:8px; --r3:8px; --r4:12px;
  --rail:248px;
  --fs:'Inter','Noto Sans Bengali','DM Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --fm:ui-monospace,'Noto Sans Bengali','SF Mono','JetBrains Mono',Menlo,monospace;
  --ease:cubic-bezier(.32,.72,0,1);
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper-2);color:var(--ink-2);font-family:var(--fs);
  font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased;
  font-feature-settings:'cv11','ss01';}
a{color:inherit;text-decoration:none}
button{font:inherit;color:inherit}
.mono{font-family:var(--fm);font-size:12.5px;letter-spacing:-.2px}
.mut{color:var(--ink-3);font-size:12.5px;font-weight:400}
.r{text-align:right}
b,strong{font-weight:600;color:var(--ink)}
h1,h2,h3{color:var(--ink)}
:focus-visible{outline:2px solid var(--brand);outline-offset:2px;border-radius:6px}

/* ══════════════════════════════════════════════════════════════════════════
   2 · MOTION
   Views fade-lift on entry, numbers pulse when they change, new rows flash
   green once. Nothing loops. Nothing blocks a tap.
   ══════════════════════════════════════════════════════════════════════════ */
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes pop{0%{transform:scale(1)}40%{transform:scale(1.07)}100%{transform:scale(1)}}
@keyframes flash{0%{background:var(--brand-tint)}100%{background:transparent}}
@keyframes draw{from{stroke-dashoffset:var(--len)}to{stroke-dashoffset:0}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes slideup{from{opacity:0;transform:translate(-50%,14px)}to{opacity:1;transform:translate(-50%,0)}}
@keyframes ring{0%{box-shadow:0 0 0 0 var(--brand-ring)}100%{box-shadow:0 0 0 12px transparent}}
@keyframes shimmer{to{background-position:200% 0}}

.view{animation:rise .34s var(--ease) both}
.view>*{animation:rise .38s var(--ease) both}
.view>*:nth-child(2){animation-delay:.03s}
.view>*:nth-child(3){animation-delay:.06s}
.view>*:nth-child(4){animation-delay:.09s}
.view>*:nth-child(5){animation-delay:.12s}
.bump{animation:pop .42s var(--ease)}
tr.fresh>td,.tlx.fresh{animation:flash 2.2s var(--ease)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}

/* ══════════════════════════════════════════════════════════════════════════
   3 · SHELL — rail + topbar + canvas
   ══════════════════════════════════════════════════════════════════════════ */
.app{display:grid;grid-template-columns:var(--rail) minmax(0,1fr);min-height:100vh}

.rail{background:#0B1220;color:#fff;position:sticky;top:0;height:100vh;
  display:flex;flex-direction:column;min-width:0;
  background-image:radial-gradient(900px 400px at -10% -5%,rgba(8,152,48,.20),transparent 60%);}
.brandrow{display:flex;align-items:center;gap:11px;padding:20px 18px 18px}
.mark{width:36px;height:36px;border-radius:8px;flex:none;display:grid;place-items:center;
  background:linear-gradient(145deg,var(--brand),#0ab93a);box-shadow:0 6px 18px -6px rgba(8,152,48,.75)}
.mark svg{width:21px;height:21px;stroke:#fff}
.bn{font-weight:750;font-size:15px;letter-spacing:-.2px;line-height:1.1}
.bs{font-size:10.5px;color:#7A8699;letter-spacing:.09em;text-transform:uppercase;margin-top:2px}

.navgrp{padding:6px 12px 4px;font-size:10px;letter-spacing:.11em;text-transform:uppercase;
  color:#5D6779;font-weight:650;margin-top:8px}
.nav{padding:0 10px;display:flex;flex-direction:column;gap:1px;min-width:0}
.nav a{display:flex;align-items:center;gap:10px;padding:7px 10px;border-radius:6px;
  color:#AEB8C7;font-size:13.5px;font-weight:500;min-width:0;position:relative;
  transition:background .16s var(--ease),color .16s var(--ease),transform .16s var(--ease)}
.nav a svg{width:17px;height:17px;flex:none;opacity:.85}
.nav a span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nav a:hover{background:rgba(255,255,255,.06);color:#fff;transform:translateX(2px)}
.nav a[aria-current="page"]{background:rgba(8,152,48,.16);color:#fff;font-weight:600}
.nav a[aria-current="page"] svg{opacity:1;stroke:#2BD255;transform:scale(1.08)}
.nav a svg{transition:transform .2s var(--ease)}
.nav a[aria-current="page"]::before{content:"";position:absolute;left:-10px;top:9px;bottom:9px;
  width:3px;border-radius:0 3px 3px 0;background:#2BD255}
.nbadge{margin-left:auto;background:rgba(255,255,255,.12);color:#fff;font-size:10.5px;
  font-weight:650;padding:1px 7px;border-radius:99px;font-family:var(--fm)}
.nav a[aria-current="page"] .nbadge{background:var(--brand)}

.railfoot{margin-top:auto;padding:14px;border-top:1px solid rgba(255,255,255,.08)}
.who{display:flex;align-items:center;gap:10px;min-width:0}
.who .av{width:30px;height:30px;border-radius:6px;flex:none;display:grid;place-items:center;
  background:linear-gradient(145deg,#243040,#141c28);color:#fff;font-weight:700;font-size:12.5px}
.who .wn{font-size:12.5px;font-weight:600;color:#E6EAF0;line-height:1.2}
.who .wr{font-size:10.5px;color:#6E7A8C}

/* topbar */
.top{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.86);
  backdrop-filter:saturate(180%) blur(14px);-webkit-backdrop-filter:saturate(180%) blur(14px);
  border-bottom:1px solid var(--line);padding:8px 32px;
  display:flex;align-items:center;gap:12px;min-width:0}
.crumb{font-size:12.5px;color:var(--ink-3);display:flex;align-items:center;gap:7px;min-width:0}
.crumb b{color:var(--ink);font-weight:600}
.gsearch{margin-left:auto;position:relative;min-width:0;width:340px;max-width:40vw}
.gsearch svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);
  width:15px;height:15px;stroke:var(--ink-4);pointer-events:none}
.gsearch input{width:100%;height:32px;border:1px solid var(--line-2);background:#fff;
  border-radius:6px;padding:0 60px 0 32px;font-size:13px;color:var(--ink);box-shadow:var(--e1);
  transition:border-color .16s,box-shadow .16s,background .16s}
.gsearch input:focus{outline:none;background:#fff;border-color:var(--brand);
  box-shadow:0 0 0 4px var(--brand-ring)}
.kbd{position:absolute;right:9px;top:50%;transform:translateY(-50%);font-family:var(--fm);
  font-size:10.5px;color:var(--ink-4);border:1px solid var(--line-2);border-radius:5px;
  padding:1px 5px;background:#fff}
.iconbtn{width:32px;height:32px;border-radius:6px;border:1px solid var(--line-2);background:#fff;
  display:grid;place-items:center;cursor:pointer;position:relative;flex:none;
  transition:border-color .16s,box-shadow .16s,transform .16s}
.iconbtn svg{width:17px;height:17px;stroke:var(--ink-2)}
.iconbtn:hover{border-color:var(--ink-4);box-shadow:var(--e2);transform:translateY(-1px)}
.dot-n{position:absolute;top:7px;right:8px;width:7px;height:7px;border-radius:50%;
  background:var(--bad);border:2px solid #fff;animation:ring 2.4s var(--ease) infinite}

.canvas{padding:28px 32px 80px;max-width:1400px;min-width:0}
.ph{display:flex;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:20px;min-width:0}
.ph h1{margin:0;font-size:24px;font-weight:700;letter-spacing:-.5px;line-height:1.2}
.ph p{margin:4px 0 0;color:var(--ink-3);font-size:14px}
.ph .meta{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--ink-3);
  background:#fff;border:1px solid var(--line);border-radius:6px;padding:6px 10px;align-self:center}
.ph .meta svg{width:14px;height:14px;stroke:var(--brand)}
.ph .meta i{width:1px;height:14px;background:var(--line-2)}
.phact{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap;min-width:0;max-width:100%}

/* ══════════════════════════════════════════════════════════════════════════
   4 · PRIMITIVES
   ══════════════════════════════════════════════════════════════════════════ */
.card{background:var(--paper);border:1px solid var(--line);border-radius:var(--r3);
  box-shadow:var(--e1);min-width:0;overflow:hidden}
.ch{display:flex;align-items:center;gap:10px;padding:12px 16px;min-height:52px;border-bottom:1px solid var(--line);min-width:0}
.ch h3{margin:0;font-size:15px;font-weight:600;letter-spacing:-.2px;color:var(--ink)}
.ch .sub{font-size:12.5px;color:var(--ink-3);font-weight:400}
.ch .sp{margin-left:auto;display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end}
.hi{width:28px;height:28px;border-radius:6px;flex:none;display:grid;place-items:center;
  background:var(--brand-tint);color:var(--brand)}
.hi svg{width:16px;height:16px;stroke:var(--brand);transition:transform .25s var(--ease)}
.card:hover .hi svg,.sheet .hi svg{transform:scale(1.1)}
.sheet .ch h3{font-size:16px}
.cb{padding:16px}
.cb.flush{padding:0}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;height:36px;padding:0 12px;
  border-radius:6px;border:1px solid var(--line-2);background:#fff;font-size:13.5px;font-weight:500;
  color:var(--ink);cursor:pointer;white-space:nowrap;box-shadow:var(--e1);
  transition:background .15s,border-color .15s,box-shadow .15s,transform .1s var(--ease)}
.btn svg{width:15px;height:15px;flex:none}
.btn:hover{background:var(--paper-2);border-color:var(--ink-4)}
.btn:active{transform:scale(.985)}
.btn-p{background:var(--brand);border-color:var(--brand-600);color:#fff;
  box-shadow:0 1px 1px rgba(48,49,61,.08),inset 0 1px 0 rgba(255,255,255,.14)}
.btn-p:hover{background:var(--brand-600);border-color:var(--brand-700)}
.btn-lg{height:44px;font-size:14.5px;font-weight:600}
.btn-d{background:#fff;border-color:#F3C2BD;color:var(--bad)}
.btn-d:hover{background:var(--bad-bg);border-color:#EBA59C;color:var(--bad)}
.btn-xs{height:28px;padding:0 10px;font-size:12.5px;border-radius:6px}
.btn-xs svg{width:14px;height:14px}
.ibtn{width:28px;height:28px;border-radius:6px;border:1px solid transparent;background:transparent;color:var(--ink-4);
  display:inline-grid;place-items:center;cursor:pointer}
.ibtn svg{width:14px;height:14px}
.ibtn:hover{background:var(--bad-bg);color:var(--bad);border-color:#F3C2BD}
.lnk{background:none;border:0;padding:0;color:var(--brand);font-weight:500;font-size:13px;cursor:pointer;
  display:inline-flex;align-items:center;gap:4px}
.lnk svg{width:13px;height:13px}
.lnk:hover{text-decoration:underline}
.links{display:flex;gap:16px;margin-top:2px}
.btn[disabled]{opacity:.5;pointer-events:none}
.spin{width:15px;height:15px;border:2px solid rgba(255,255,255,.35);border-top-color:#fff;
  border-radius:50%;animation:spin .7s linear infinite}

.pill{display:inline-flex;align-items:center;gap:4px;padding:1px 6px;border-radius:4px;
  font-size:11.5px;font-weight:500;line-height:18px;white-space:nowrap}
.pill.ok{background:var(--ok-bg);color:#05631f}
.pill.due{background:var(--warn-bg);color:var(--warn);font-family:var(--fm)}
.pill.bad{background:var(--bad-bg);color:var(--bad)}
.pill.web{background:var(--info-bg);color:var(--info)}
.pill.man{background:var(--paper-3);color:var(--ink-2)}
.pill.paid{background:var(--ok-bg);color:#05631f}
.tag{display:inline-flex;align-items:center;gap:5px;padding:2px 8px;border-radius:4px;
  font-size:12px;font-weight:500;background:var(--paper-3);color:var(--ink-2)}
.tag.vip{background:#FFF4D6;color:#8A5A00}

/* tables */
table{width:100%;border-collapse:collapse;font-size:13.5px;color:var(--ink-2)}
th{text-align:left;font-size:12px;letter-spacing:0;text-transform:none;
  color:var(--ink-3);font-weight:500;padding:8px 16px;background:var(--paper-2);
  border-bottom:1px solid var(--line);position:sticky;top:0;z-index:1}
th.r{text-align:right}
td{padding:10px 16px;border-bottom:1px solid var(--line);vertical-align:middle}
tbody tr:last-child td{border-bottom:0}
tbody tr{transition:background .13s}
tbody tr:hover{background:var(--paper-2)}
td.r,.num{font-variant-numeric:tabular-nums;font-feature-settings:'tnum'}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.crow{cursor:pointer}
.crow:hover{background:var(--paper-2)}
tr.crow.on{background:var(--brand-tint);box-shadow:inset 3px 0 0 var(--brand)}
tr.crow.on .go2{opacity:1}
.crow:hover .go2{opacity:1;transform:translateX(3px)}
.go2{opacity:0;color:var(--brand);font-size:17px;font-weight:700;display:inline-block;
  transition:opacity .16s,transform .16s var(--ease)}
.rank{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:6px;
  background:var(--paper-3);color:var(--ink-3);font-size:11px;font-weight:700;margin-right:8px;
  font-family:var(--fm)}
.rank.t1{background:#FFF0C7;color:#8A5A00}
.rank.t2{background:#EDF0F4;color:#4A5568}
.rank.t3{background:#FBE8D8;color:#8A4B12}

/* KPI */
.kpis{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
.kpi{background:var(--paper);border:1px solid var(--line);border-radius:var(--r2);padding:16px;
  min-width:0;position:relative;overflow:hidden;box-shadow:var(--e1)}
.kpi.due .kl{color:var(--warn)} .kpi.due .kl svg{stroke:var(--warn);background:var(--warn-bg)}
.kl{display:flex;align-items:center;gap:8px;font-size:12.5px;letter-spacing:0;margin-bottom:25px;
  text-transform:none;color:var(--ink-3);font-weight:500}
.kl svg{width:26px;height:26px;padding:5px;border-radius:6px;background:var(--brand-tint);stroke:var(--brand);
  flex:none;box-sizing:border-box;transition:transform .25s var(--ease)}
.kpi:hover .kl svg,.kl svg.tick{transform:scale(1.1)}
.kl svg.tick{animation:pop .5s var(--ease)}
.kv{font-size:26px;font-weight:700;letter-spacing:-.7px;margin-top:6px;color:var(--ink);
  font-variant-numeric:tabular-nums;line-height:1.1;display:inline-block}
.d{font-size:12.5px;margin-top:4px;color:var(--ink-3);display:flex;align-items:center;gap:4px}
.d.up{color:var(--ok)} .d.dn{color:var(--bad)} .d.fl{color:var(--ink-3)}

/* segmented period control */
.seg{display:inline-flex;background:var(--paper-2);border:1px solid var(--line-2);border-radius:8px;padding:2px;gap:2px;box-shadow:var(--e1);
  max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.seg::-webkit-scrollbar{display:none}
.seg button{flex:none;height:28px;padding:0 12px;border:0;background:transparent;border-radius:6px;
  font-size:13px;font-weight:500;color:var(--ink-3);cursor:pointer;
  transition:background .18s var(--ease),color .18s,box-shadow .18s}
.seg button:hover{color:var(--ink)}
.seg button[aria-pressed="true"]{background:#fff;color:var(--ink);font-weight:600;box-shadow:var(--e2),0 0 0 1px var(--line-2)}
.seg.sm button{height:26px;padding:0 10px;font-size:12.5px}

/* chart */
.chartbox{height:240px;width:100%;position:relative}
.chartbox svg{display:block;overflow:visible}
.gl{stroke:var(--line);stroke-width:1}
.ax{font-size:11px;fill:var(--ink-4);font-family:var(--fs);font-variant-numeric:tabular-nums}
.band{fill:var(--brand-tint)}
.ln{fill:none;stroke:var(--brand);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;
  stroke-dasharray:var(--len);animation:draw 1s var(--ease) forwards}
.ln2{fill:none;stroke:var(--ink-4);stroke-width:1.5;stroke-dasharray:4 4;opacity:.8}
.ar{fill:url(#g1);stroke:none;opacity:0;animation:rise .6s var(--ease) .3s forwards}
.pt{fill:#fff;stroke:var(--brand);stroke-width:1.5}
.dot{fill:var(--brand);stroke:#fff;stroke-width:2.5}
.xh{stroke:var(--ink-4);stroke-width:1;stroke-dasharray:3 3}
.fpt{fill:var(--brand);stroke:#fff;stroke-width:2.5}
.fpt2{fill:#fff;stroke:var(--ink-4);stroke-width:2}
.ctip{position:absolute;z-index:5;pointer-events:none;background:#fff;border:1px solid var(--line-2);
  border-radius:8px;box-shadow:var(--e4);padding:8px 10px;min-width:150px;font-size:12.5px}
.ctip .tt{color:var(--ink-3);font-size:12px}
.ctip .tv{font-size:16px;font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums;margin:1px 0}
.ctip .tm{color:var(--ink-3);font-size:12px}
.ctip .tp{white-space:nowrap} .ctip b.up{color:var(--ok)} .ctip b.dn{color:var(--bad)}
.legend{display:flex;gap:16px;align-items:center;font-size:12.5px;color:var(--ink-3);margin-bottom:8px;flex-wrap:wrap}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:14px;height:0;border-top:2px solid var(--brand);display:inline-block}
.legend i.lg2{border-top:2px dashed var(--ink-4)}

/* empty state */
.none{padding:28px 18px;text-align:center;color:var(--ink-3);font-size:13px}
.none::before{content:"";display:block;width:32px;height:32px;margin:0 auto 10px;opacity:.55;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23687385' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 8l9-4 9 4-9 4z'/%3E%3Cpath d='M3 8v8l9 4 9-4V8'/%3E%3Cpath d='M12 12v8'/%3E%3C/svg%3E") center/contain no-repeat;
  animation:floaty 3.2s ease-in-out infinite}
@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.none b{display:block;color:var(--ink);font-size:14px;font-weight:600;margin-bottom:3px}

/* forms */
.fld{display:block;margin-bottom:14px;min-width:0}
.fld label{display:block;font-size:13px;font-weight:500;color:var(--ink-2);margin-bottom:6px}
.inp{width:100%;height:36px;border:1px solid var(--line-2);border-radius:6px;background:#fff;
  padding:0 10px;font-size:13.5px;color:var(--ink);font-family:inherit;box-shadow:var(--e1);
  transition:border-color .16s,box-shadow .16s}
.inp.lg{height:42px;font-size:14.5px;padding:0 12px}
.inp:focus{outline:none;border-color:var(--brand);box-shadow:0 0 0 3px rgba(8,152,48,.18)}
select.inp{appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7686' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 10px center;background-size:16px;padding-right:34px}
.hint{font-size:12px;color:var(--ink-3);margin-top:5px}
.grid2{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.fld label .opt{display:inline;font-weight:400;color:var(--ink-4);font-size:12px;margin-left:4px;text-transform:none;letter-spacing:0}
/* price tier: three cards, one pressed, all options visible */
.tierpick{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.tierpick button{position:relative;text-align:left;background:#fff;border:1px solid var(--line-2);border-radius:8px;padding:12px 12px 11px 36px;
  cursor:pointer;min-height:64px;transition:border-color .16s,box-shadow .16s,background .16s;min-width:0}
.tierpick button b{display:block;font-size:13.5px;font-weight:600;color:var(--ink);line-height:1.2}
.tierpick button span{display:block;font-size:12px;color:var(--ink-3);margin-top:3px;line-height:1.3}
.tierpick button svg{position:absolute;left:11px;top:14px;width:16px;height:16px;border-radius:50%;padding:2px;box-sizing:border-box;
  border:1.5px solid var(--line-2);stroke:transparent;background:#fff;transition:all .16s}
.tierpick button:hover{border-color:var(--ink-4)}
.tierpick button[aria-pressed="true"]{border-color:var(--brand);background:var(--brand-tint);box-shadow:0 0 0 3px var(--brand-ring)}
.tierpick button[aria-pressed="true"] svg{background:var(--brand);border-color:var(--brand);stroke:#fff}
/* date picker: an input with a calendar icon, a popover with a month grid */
.dpw{position:relative}
.dpw .inp{padding-right:38px;cursor:pointer;background:#fff}
.dpw>svg{position:absolute;right:11px;top:50%;transform:translateY(-50%);width:16px;height:16px;stroke:var(--ink-4);pointer-events:none}
.dpw .inp:focus{border-color:var(--brand);box-shadow:0 0 0 3px var(--brand-ring)}
.dp{position:fixed;z-index:300;width:296px;background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:var(--e4);
  padding:12px;animation:rise .18s var(--ease);font-size:13px}
.dp .dph{display:flex;align-items:center;gap:6px;margin-bottom:8px}
.dp .dph b{flex:1;text-align:center;font-size:14px;font-weight:650;color:var(--ink)}
.dp .dph button{width:30px;height:30px;border:1px solid var(--line-2);background:#fff;border-radius:8px;display:grid;place-items:center;cursor:pointer}
.dp .dph button:hover{border-color:var(--ink-4);background:var(--paper-2)}
.dp .dph button svg{width:15px;height:15px;stroke:var(--ink-2)}
.dp .dpw7{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;text-align:center}
.dp .dpw7 span{font-size:11px;color:var(--ink-4);font-weight:600;padding:4px 0 6px;letter-spacing:.02em}
.dp .dpg{display:grid;grid-template-columns:repeat(7,1fr);gap:2px}
.dp .dpg button{height:36px;border:0;background:transparent;border-radius:8px;font-size:13px;color:var(--ink-2);cursor:pointer;
  font-variant-numeric:tabular-nums;position:relative;transition:background .12s,color .12s}
.dp .dpg button:hover{background:var(--paper-2);color:var(--ink)}
.dp .dpg button.o{color:var(--ink-4)}
.dp .dpg button.t::after{content:"";position:absolute;left:50%;bottom:5px;width:4px;height:4px;border-radius:50%;background:var(--brand);transform:translateX(-50%)}
.dp .dpg button.s{background:var(--brand);color:#fff;font-weight:650}
.dp .dpg button.s::after{background:#fff}
.dp .dpg button.f{color:var(--line-2);cursor:not-allowed}
.dp .dpf{display:flex;align-items:center;gap:8px;margin-top:10px;padding-top:10px;border-top:1px solid var(--line)}
.dp .dpf .hint{margin:0;flex:1}
.dp .dpf button{height:30px;padding:0 10px;border:1px solid var(--line-2);background:#fff;border-radius:8px;font-size:12.5px;font-weight:500;cursor:pointer}
.dp .dpf button:hover{border-color:var(--ink-4);background:var(--paper-2)}
.dp .dpf button.p{background:var(--brand);border-color:var(--brand);color:#fff}
/* banner drop zone */
.drop{display:block;position:relative;border:1.5px dashed var(--line-2);border-radius:8px;background:var(--paper-2);min-height:92px;cursor:pointer;
  overflow:hidden;transition:border-color .16s,background .16s}
.drop:hover{border-color:var(--brand);background:var(--brand-tint)}
.drop img{display:block;width:100%;aspect-ratio:16/5;object-fit:cover}
.drop .dt{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:18px 12px;text-align:center;color:var(--ink-3)}
.drop .dt svg{width:20px;height:20px;stroke:var(--brand);margin-bottom:4px}
.drop .dt b{font-size:13.5px;color:var(--ink)} .drop .dt small{font-size:12px}
.drop.has .dt{position:absolute;left:0;right:0;bottom:0;padding:6px;background:rgba(255,255,255,.9);flex-direction:row;gap:8px}
.drop.has .dt svg{display:none} .drop.has .dt small{display:none} .drop.has .dt b::before{content:"Change banner"} .drop.has .dt b{font-size:0}
.drop.has .dt b::before{font-size:12.5px}
.hbanner{border-radius:var(--r3) var(--r3) 0 0;overflow:hidden;border:1px solid var(--line);border-bottom:0;margin-bottom:-1px;background:var(--paper-3)}
.hbanner img{display:block;width:100%;aspect-ratio:16/4;object-fit:cover}
.hbanner:not([hidden])+.hero{border-top-left-radius:0;border-top-right-radius:0}
/* settings and modal forms read as paired fields, never as a five-across strip */
[data-spanel] .grid2,.sheet .grid2{grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));
  max-width:760px}
@media (min-width:900px){[data-spanel] .grid2{grid-template-columns:repeat(2,minmax(0,1fr))}}
.grid3{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}

/* combobox */
.cbx{position:relative}
.cbxlist{position:absolute;z-index:50;left:0;right:0;top:calc(100% + 4px);background:#fff;
  border:1px solid var(--line-2);border-radius:8px;box-shadow:var(--e4);
  max-height:290px;overflow:auto;display:none;padding:4px;min-width:260px}
.cbxlist.open{display:block;animation:rise .18s var(--ease)}
.opt{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:8px;cursor:pointer;min-width:0}
.opt:hover,.opt.on{background:var(--brand-tint)}
#sdCust .opt:hover{background:transparent}
.opt .av{width:30px;height:30px;border-radius:6px;flex:none;display:grid;place-items:center;
  background:var(--paper-3);color:var(--ink-2);font-weight:700;font-size:12px}
.opt .nm{font-size:13px;font-weight:600;line-height:1.25}
.opt .mt{font-size:11.5px;color:var(--ink-3);font-family:var(--fm)}
.opt .rt{margin-left:auto;text-align:right;font-size:11.5px;color:var(--ink-3);white-space:nowrap}
.opt mark{background:#FFF1A8;color:inherit;border-radius:3px;padding:0 1px}

/* dropdown lists must never be clipped by the card they sit in */
.card:has(.cbxlist.open),.card:has(.cbxlist.open) .tw,.card:has(.cbxlist.open) .cb{overflow:visible}
.lines-card,.lines-card .tw{overflow:visible}
.addrow{display:flex;align-items:center;gap:12px;border-top:1px solid var(--line);padding:10px 16px}
.lpw{display:flex;align-items:center;gap:8px}
.lthumb{width:34px;height:34px;border-radius:6px;flex:none;background:var(--paper-2);border:1px solid var(--line);
  display:grid;place-items:center;overflow:hidden;animation:pop .35s var(--ease)}
.lthumb img{width:100%;height:100%;object-fit:contain;display:block}
.lpw .lps{flex:1;min-width:0}

/* payment method: a dropdown that shows the method's icon */
.msel{position:relative}
.mselb{display:flex;align-items:center;gap:8px;text-align:left;cursor:pointer;padding:0 8px 0 10px}
.mselb .mic{width:22px;height:22px;border-radius:5px;display:grid;place-items:center;background:var(--paper-2);flex:none}
.mselb .mic svg,.mopt svg:first-child{width:16px;height:16px;stroke:var(--ink-3)}
.mselb .mlbl{flex:1;min-width:0;font-weight:500;color:var(--ink)}
.mselb .chev svg{width:14px;height:14px;stroke:var(--ink-4)}
.mselb[aria-expanded="true"]{border-color:var(--brand);box-shadow:0 0 0 3px rgba(8,152,48,.18)}
.mselb .mic svg.brand,.mopt svg.brand:first-child{stroke:none}
.mselb .mic:has(svg.brand){background:transparent}
.mic svg.tick{animation:pop .4s var(--ease)}
.mlist{min-width:0}
.mopt{gap:10px;padding:9px 10px}
.mopt svg:last-child{width:14px;height:14px;stroke:var(--brand);margin-left:auto;opacity:0}
.mopt[aria-selected="true"]{background:var(--brand-tint)}
.mopt[aria-selected="true"] svg:last-child{opacity:1}

/* money inputs: currency prefix, value left-aligned, the Stripe amount field */
.money{position:relative;display:inline-block;vertical-align:middle;max-width:100%}
.fld>.money{display:block}
.money .cur{position:absolute;left:11px;top:50%;transform:translateY(-50%);font-size:13.5px;font-weight:600;color:var(--ink-4);pointer-events:none;line-height:1;transition:color .15s}
.money:focus-within .cur{color:var(--ink-2)}
.money .inp{padding-left:27px;text-align:left}
.cpn{display:flex;gap:8px} .cpn .inp{flex:1;min-width:0;text-transform:uppercase} .cpn .btn{flex:none}
.hint.ok{color:var(--brand)} .hint.bad{color:var(--bad)}
.qb:disabled{opacity:.35;cursor:not-allowed}
/* section tabs carry an icon; period and filter toggles stay text-only */
.seg button{display:inline-flex;align-items:center;gap:6px}
.seg button svg{width:14px;height:14px;stroke:var(--ink-4);flex:none;transition:stroke .15s,transform .2s var(--ease)}
.seg button:hover svg{stroke:var(--ink-2)}
.seg button[aria-pressed="true"] svg{stroke:var(--brand);transform:scale(1.08)}
.fbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
/* goal-gradient bar on a due row: paid share of sold (Hull 1932; Kivetz 2006) */
.prog{height:6px;border-radius:99px;background:var(--paper-3);overflow:hidden;min-width:120px}
.prog i{display:block;height:100%;border-radius:99px;background:var(--brand);transition:width .6s var(--ease)}
b.bad{color:var(--bad)}
.note.edit{border-color:#F3D9A4;background:var(--warn-bg);color:#7A4B0A;margin-bottom:16px}
.note.edit b{color:#5C3A05}
.pcard.arch{opacity:.72} .pcard.arch .pimg{filter:grayscale(1)}
/* twelve-month bars on the product page */
.mchart{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:6px;height:150px;align-items:end;padding-top:26px}
.mb{position:relative;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%;gap:6px;border-radius:6px;outline:0;cursor:default}
.mb i{display:block;width:100%;max-width:34px;min-height:2px;border-radius:4px 4px 2px 2px;background:var(--brand-tint);border:1px solid rgba(8,152,48,.25);transition:background .15s,transform .2s var(--ease);transform-origin:bottom}
.mb.best i{background:var(--brand);border-color:var(--brand)}
.mb.cur b{color:var(--ink)}
.mb b{font-size:11px;font-weight:500;color:var(--ink-4);line-height:1}
.mb:hover i,.mb:focus-visible i{background:var(--brand);border-color:var(--brand);transform:scaleY(1.03)}
.mtip{position:absolute;bottom:calc(100% - 14px);left:50%;transform:translate(-50%,4px);background:var(--ink);color:#fff;font-size:11.5px;line-height:1.35;padding:6px 9px;border-radius:6px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .15s,transform .15s;z-index:3}
.mtip b{display:block;font-size:12.5px;font-weight:650;color:#fff}
.mb:hover .mtip,.mb:focus-visible .mtip{opacity:1;transform:translate(-50%,0)}
.epphoto{display:flex;align-items:center;gap:14px;margin-bottom:14px}
.epphoto .hpic{width:64px;height:64px;border-radius:8px}

/* sale lines */
table.lines td{vertical-align:top;padding:10px 12px}
table.lines td:first-child{padding-left:16px}
.lpc{min-width:240px;position:relative}
.lpc .lps{font-weight:500}
.lpm{margin-top:4px;font-size:12px;min-height:16px}
.lpm .bad{color:var(--bad);font-weight:500}
.lpl{min-width:340px}
.pimg.sm{width:34px;height:34px;border-radius:6px}
.qtyc{display:inline-flex;align-items:stretch;border:1px solid var(--line-2);border-radius:6px;overflow:hidden;box-shadow:var(--e1)}
.qtyc .lq{width:52px;height:34px;border:0;border-radius:0;box-shadow:none;text-align:center;padding:0 4px;
  -moz-appearance:textfield}
.qtyc .lq::-webkit-outer-spin-button,.qtyc .lq::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.qtyc .lq:focus{box-shadow:inset 0 0 0 2px rgba(8,152,48,.25)}
.qb{width:30px;border:0;background:var(--paper-2);color:var(--ink-2);font-size:16px;cursor:pointer;line-height:1}
.qb:hover{background:var(--paper-3);color:var(--ink)}
table.lines .lr{width:112px;text-align:left}
table.lines th:nth-child(2),table.lines td:nth-child(2){width:118px}
table.lines th:nth-child(3),table.lines td:nth-child(3){width:124px}
table.lines th:nth-child(4),table.lines td:nth-child(4){width:92px;white-space:nowrap}
table.lines th:nth-child(5),table.lines td:nth-child(5){width:40px}
/* the sale screen needs ~640px for its line table; below that the payment card drops under the items */
/* table-heavy two-column pages need ~640px for the main column; below that they stack. Dashboard keeps two. */
@media (max-width:1400px){ .g13:not(.gdash){grid-template-columns:minmax(0,1fr)} }
@media (max-width:1600px){ .g13.gcust{grid-template-columns:minmax(0,1fr)} }
/* product picker in sheets: opens in flow, never clipped by the sheet */
.ppick{position:relative}
.pselb{display:flex;align-items:center;gap:10px;text-align:left;cursor:pointer;padding:0 8px 0 6px;height:44px}
.pselb .lthumb{width:30px;height:30px;flex:none}
.pselb .mlbl{flex:1;min-width:0;font-weight:500;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pselb .chev svg{width:14px;height:14px;stroke:var(--ink-4)}
.pselb[aria-expanded="true"]{border-color:var(--brand);box-shadow:0 0 0 3px rgba(8,152,48,.18)}
.ppick .plist{position:static;display:none;max-height:236px;overflow:auto;margin-top:6px;box-shadow:none}
.ppick .plist.open{display:block}
.ppick .plist .opt{gap:10px;padding:8px 10px}
.ppick .plist .opt .mt{display:block;font-size:11.5px;color:var(--ink-3)}
.ppick .plist .opt>svg{width:14px;height:14px;stroke:var(--brand);margin-left:auto;opacity:0;flex:none}
.ppick .plist .opt[aria-selected="true"]{background:var(--brand-tint)} .ppick .plist .opt[aria-selected="true"]>svg{opacity:1}
table.lines .lps{min-width:0}
table.lines .lt{font-weight:600;color:var(--ink);padding-top:19px;white-space:nowrap}
tr.line.over .lq{color:var(--bad)}
table.sum{font-size:13.5px} table.sum td{padding:5px 0;border:0}
table.sum tr.tot td{font-weight:700;color:var(--ink);font-size:17px;border-top:1px solid var(--line);padding-top:12px}
.okdraw svg path{stroke-dasharray:32;stroke-dashoffset:32;animation:draw2 .45s var(--ease) forwards}
@keyframes draw2{to{stroke-dashoffset:0}}

/* profile hero */
.hero{background:var(--paper);border:1px solid var(--line);border-radius:var(--r3);padding:20px;
  display:flex;gap:15px;align-items:flex-start;flex-wrap:wrap;box-shadow:var(--e1);min-width:0}
.hav svg{width:26px;height:26px;stroke:#fff}
.hav{width:56px;height:56px;border-radius:10px;flex:none;display:grid;place-items:center;
  background:linear-gradient(145deg,var(--brand),#0ab93a);color:#fff;font-size:23px;font-weight:700;
  box-shadow:0 10px 24px -10px rgba(8,152,48,.9)}
.hmeta{display:flex;flex-wrap:wrap;align-items:center;gap:8px;color:var(--ink-3);font-size:12.5px;margin-top:5px}
.hmeta i{width:3px;height:3px;border-radius:50%;background:var(--ink-4);display:inline-block}
.htags{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}

/* timeline */
.tl{position:relative;padding-left:26px}
.tl::before{content:"";position:absolute;left:7px;top:5px;bottom:5px;width:2px;
  background:linear-gradient(var(--line),var(--line) 70%,transparent)}
.tlx{position:relative;padding:0 0 18px}
.tlx::before{content:"";position:absolute;left:-24px;top:3px;width:12px;height:12px;border-radius:50%;
  background:#fff;border:2.5px solid var(--ink-4)}
.tlx.sale::before{border-color:var(--brand)}
.tlx.pay::before{border-color:var(--info)}
.tlx.dueev::before{border-color:var(--warn)}
.tlx .dt{font-size:11.5px;color:var(--ink-3);font-family:var(--fm)}
.tlx .ti{font-size:13.5px;font-weight:600;margin-top:1px;color:var(--ink)}
.tlx .tx{font-size:12.5px;color:var(--ink-3);margin-top:1px}
.tlx .amt{font-weight:650;color:var(--ink);font-variant-numeric:tabular-nums}

/* product grid */
.pgrid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(310px,1fr))}
.pcard{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:13px;
  text-align:left;padding:13px;background:var(--paper);border:1px solid var(--line);
  border-radius:var(--r3);box-shadow:var(--e1);cursor:pointer;min-width:0;position:relative;
  transition:transform .2s var(--ease),box-shadow .2s var(--ease),border-color .2s}
.pcard:hover{transform:translateY(-1px);box-shadow:var(--e2);border-color:var(--ink-4)}
.pcard:hover .go2{opacity:1;transform:translateX(3px)}
.pimg{width:60px;height:60px;border-radius:8px;background:var(--paper-2);
  border:1px solid var(--line);display:grid;place-items:center;flex:none;overflow:hidden}
.pimg img{width:100%;height:100%;object-fit:contain;display:block}
.pbody{display:block;min-width:0}
.pname{display:block;font-size:14px;font-weight:650;letter-spacing:-.15px;line-height:1.25;
  overflow-wrap:anywhere}
.ppack{display:block;font-size:11.5px;color:var(--ink-3);margin-top:1px;line-height:1.45}
.pbar{display:block;height:4px;border-radius:99px;background:var(--paper-3);margin:8px 0 5px;overflow:hidden}
.pbar i{display:block;height:100%;border-radius:99px;background:var(--brand)}
.pmeta{display:flex;align-items:center;gap:7px;font-size:13px;
  font-variant-numeric:tabular-nums;min-width:0;flex-wrap:wrap}
.pmeta .mut{font-size:11.5px;white-space:nowrap}
.ptags{margin-left:auto;display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.ptags .pill{font-size:10.5px;padding:1px 7px;line-height:16px}
.pcard .go2{align-self:center}

/* product hero picture */
.hpic{width:80px;height:80px;border-radius:10px;flex:none;display:grid;place-items:center;
  background:var(--paper-2);border:1px solid var(--line);overflow:hidden}
.hpic img{width:100%;height:100%;object-fit:contain;display:block}

/* carried-over screens: footnote, report launcher, settings rows */
.note{background:var(--paper-2);border:1px solid var(--line);border-radius:var(--r2);
  padding:12px 16px;font-size:12.5px;color:var(--ink-2);line-height:1.6}
.note b{color:var(--ink)}

.repgrid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));
  margin-bottom:14px}
.rep{display:flex;align-items:flex-start;gap:11px;text-align:left;padding:14px;
  background:var(--paper);border:1px solid var(--line);border-radius:var(--r2);
  box-shadow:var(--e1);cursor:pointer;min-width:0;
  transition:transform .2s var(--ease),box-shadow .2s var(--ease),border-color .2s}
.rep:hover{transform:translateY(-1px);box-shadow:var(--e2);border-color:var(--ink-4)}
.rep svg{width:18px;height:18px;flex:none;stroke:var(--brand);margin-top:1px}
.rep span{display:block;min-width:0}
.rep b{display:block;font-size:13.5px;font-weight:650}
.rep em{display:block;font-style:normal;font-size:11.5px;color:var(--ink-3);margin-top:2px;line-height:1.45}

.setrow{display:flex;align-items:center;gap:12px;padding:9px 0;
  border-bottom:1px solid var(--line);font-size:13px;min-width:0}
.setrow:last-child{border-bottom:0}
.setrow span{color:var(--ink-3);flex:1;min-width:0}
.setrow b{font-weight:600;text-align:right;white-space:nowrap}

.nav a .ic{display:grid;place-items:center}

/* notifications */
.notif{position:absolute;right:0;top:calc(100% + 8px);width:min(380px,86vw);background:#fff;
  border:1px solid var(--line-2);border-radius:var(--r3);box-shadow:var(--e4);
  display:none;overflow:hidden;z-index:60}
.notif.open{display:block;animation:rise .18s var(--ease)}
.nh{display:flex;align-items:center;gap:8px;padding:12px 14px;border-bottom:1px solid var(--line);
  font-size:12.5px;font-weight:650}
.nf{padding:10px 14px;border-top:1px solid var(--line);font-size:11.5px;color:var(--ink-3);
  background:var(--paper-2)}
.notif .opt{border:1px solid var(--line);border-radius:6px;margin:8px 12px;padding:10px 12px;gap:10px;align-items:flex-start;background:#fff}
.notif .opt+.opt{margin-top:0}
.notif .opt:hover{border-color:var(--line-2);background:var(--paper-2)}
.notif .nw{flex:none;font-size:11px;color:var(--ink-4);white-space:nowrap;margin-top:2px;font-variant-numeric:tabular-nums}
#notifList{padding:2px 0 4px;max-height:60vh;overflow:auto}
.notif .opt.nolink{cursor:default}
.notif .opt.nolink:hover{background:transparent}
.ndot{width:8px;height:8px;border-radius:50%;flex:none;margin-top:5px;background:var(--ink-4)}
.ndot.due{background:var(--warn)} .ndot.bad{background:var(--bad)}
.ndot.warn{background:var(--warn)} .ndot.ok{background:var(--ok)}

/* tick control */
.tick{width:22px;height:22px;border-radius:7px;border:1.5px solid var(--line-2);background:#fff;
  display:grid;place-items:center;cursor:pointer;padding:0;
  transition:background .16s,border-color .16s,transform .12s var(--ease)}
.tick svg{width:13px;height:13px;stroke:#fff;opacity:0;transition:opacity .16s}
.tick:hover{border-color:var(--brand)}
.tick.on{background:var(--brand);border-color:var(--brand)}
.tick.on svg{opacity:1}
tr.is-done td{opacity:.52}
tr.is-done b{text-decoration:line-through}

/* toast */
.toast{position:fixed;left:50%;bottom:26px;transform:translate(-50%,14px);z-index:200;
  background:#30313D;color:#fff;border-radius:8px;padding:12px 17px;font-size:13.5px;
  box-shadow:var(--e4);display:none;align-items:center;gap:10px;max-width:min(560px,92vw)}
.toast.show{display:flex;animation:slideup .3s var(--ease)}
.toast svg{width:18px;height:18px;stroke:#2BD255;flex:none}
.toast.show svg path{stroke-dasharray:32;stroke-dashoffset:32;animation:draw2 .5s var(--ease) .05s forwards}
.toast b{color:#fff}

/* modal */
.scrim{position:fixed;inset:0;background:rgba(11,18,32,.45);backdrop-filter:blur(3px);
  z-index:150;display:none;align-items:flex-start;justify-content:center;padding:5vh 16px}
.scrim.open{display:flex;animation:rise .2s var(--ease)}
.sheet{background:#fff;border-radius:var(--r4);box-shadow:var(--e4);width:min(560px,100%);
  border:1px solid var(--line);
  max-height:90vh;overflow:auto;animation:rise .3s var(--ease)}   /* tall sheets scroll inside, the save button never leaves the screen */
#custModal .sheet{width:min(640px,100%)}

/* banners */
.demo{display:flex;align-items:center;gap:9px;background:#FFF9E6;border:1px solid #F5DFA0;
  color:#7A5A06;border-radius:11px;padding:9px 13px;font-size:12.5px;margin-bottom:16px}
.demo svg{width:16px;height:16px;flex:none;stroke:#B07C0A}
.hr{height:1px;background:var(--line);margin:22px 0}

.g2{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));align-items:start}
.g3{display:grid;gap:16px;grid-template-columns:repeat(3,minmax(0,1fr));align-items:start}
@media (max-width:1400px){.g3{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}}
.g13{display:grid;gap:16px;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);align-items:start}

/* ══════════════════════════════════════════════════════════════════════════
   5 · RESPONSIVE — the rail collapses to icons, then to a bottom bar
   ══════════════════════════════════════════════════════════════════════════ */
@media (max-width:1180px){
  :root{--rail:68px}
  .bn,.bs,.nav a span:not(.ic),.navgrp,.who .wn,.who .wr{display:none}
  .nav a{justify-content:center;padding:11px 0}
  .nav a::before{display:none}
  .brandrow{justify-content:center;padding:18px 0}
  .g13{grid-template-columns:minmax(0,1fr)}
  .nbadge{display:none}
}
@media (max-width:780px){
  /* ── the rail becomes a bottom bar with labels. Icon-only is faster to build
     and slower to use: the audience is not looking at this screen all day. */
  .app{grid-template-columns:minmax(0,1fr)}
  .rail{position:fixed;bottom:0;left:0;right:0;top:auto;height:auto;z-index:100;
    flex-direction:row;border-top:1px solid rgba(255,255,255,.1);overflow-x:auto;
    padding-bottom:env(safe-area-inset-bottom,0px);scrollbar-width:none;
    background-image:none;background:#0B1220}
  .rail::-webkit-scrollbar{display:none}
  .brandrow,.railfoot{display:none}
  .navgrp{display:none}
  .nav{flex-direction:row;padding:6px 0;gap:2px;flex:none}
  .rail>.nav:first-of-type{padding-left:8px}
  .rail>.nav:last-of-type{padding-right:8px}
  .nav a{flex-direction:column;justify-content:center;gap:4px;padding:8px 10px;min-width:64px;
    font-size:10.5px;font-weight:600;text-align:center;border-radius:11px}
  .nav a span:not(.ic):not(.nbadge){display:block;max-width:100%;font-size:10px;line-height:1.15;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .nav a{min-width:70px;flex:1 0 70px}
  .nav a svg{width:20px;height:20px;opacity:.95}
  .nav a::before{display:none}
  .nav a[aria-current="page"]{background:rgba(8,152,48,.2)}
  .nbadge{display:block;position:absolute;top:3px;right:6px;font-size:9.5px;padding:0 5px;
    line-height:15px;background:var(--brand);color:#fff}
  .nav a{position:relative}

  /* ── topbar: the breadcrumb goes, search gets the room it needs, the primary
     action keeps its icon but drops its label. */
  .top{padding:8px 12px;gap:8px}
  .crumb{display:none}
  .gsearch{margin-left:0;width:auto;flex:1;max-width:none;min-width:0}
  .gsearch input{height:44px;padding-right:12px}
  .kbd{display:none}
  .iconbtn{width:40px;height:40px}
  .top .btn-p{width:44px;padding:0;gap:0;height:40px}
  .top .btn-p svg{margin:0}
  .top .btn-p span,.top .btn-p{font-size:0}
  .top .btn-p svg{width:20px;height:20px}

  /* ── canvas must clear the bottom bar */
  .canvas{padding:16px 12px calc(96px + env(safe-area-inset-bottom,0px))}
  .ph .meta{width:100%;justify-content:center}
  .chartbox{height:200px}

  /* ── page head stacks, actions go full width and wrap sensibly */
  .ph{gap:10px;margin-bottom:14px}
  .ph h1{font-size:22px}
  .ph p{font-size:13px}
  .phact{margin-left:0;width:100%;gap:8px}
  .phact .btn{flex:1 1 auto}
  .phact .seg{order:-1;width:100%}

  /* ── two KPIs per row. One per row turns five cards into a scroll marathon. */
  .kpis{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}
  .kpis>.kpi:last-child:nth-child(odd){grid-column:1/-1}
  .kpi{padding:12px}
  .kl{font-size:11px;gap:6px;margin-bottom:16px}
  .kl svg{width:22px;height:22px;padding:4px}
  .kv{font-size:19px;letter-spacing:-.6px}
  .d{font-size:11.5px}

  /* ── 44px everywhere a finger lands */
  .btn{height:44px;font-size:13.5px}
  .btn-xs{height:42px;font-size:12.5px;padding:0 12px}
  #custDistrict{height:44px!important;width:100%!important}
  .ch .gsearch{width:100%!important}
  td a{display:inline-block;padding:12px 0;margin:-12px 0}
  .seg{width:100%;-webkit-mask-image:linear-gradient(90deg,#000 88%,transparent);
    mask-image:linear-gradient(90deg,#000 88%,transparent);padding-right:22px}
  .seg button{height:42px;padding:0 15px;font-size:13px}
  .mchart{height:120px;gap:3px;padding-top:24px} .mb b{font-size:9.5px}
  .fbar .seg:last-child{margin-left:0!important}
  .seg.sm button{height:42px}
  .qb{width:44px} .qtyc .lq{height:44px;width:60px}
  .lpl{min-width:0}
  .ibtn{width:40px;height:40px}
  .lnk{min-height:44px;padding:0 6px}
  .links{gap:8px}
  /* Apple-style segmented controls on a phone: full width, equal buttons, no clipping */
  .ch{flex-wrap:wrap} .ch .sp{flex-basis:100%;margin-left:0;justify-content:stretch}
  .ch .sp .seg,.fbar .seg{display:flex;width:100%}
  .ch .sp .seg button,.fbar .seg button{flex:1;padding:0 4px;font-size:12.5px;justify-content:center;min-width:0;white-space:nowrap}
  .fbar{flex-direction:column;align-items:stretch;gap:8px} .fbar>.sub{display:none}
  .seg button svg{width:13px;height:13px}
  .inp{height:44px;font-size:14px}
  select.inp{height:44px}
  td{padding:13px 12px}
  th{padding:10px 12px}
  .crow td:first-child,.crow td:last-child{padding-left:12px;padding-right:12px}
  .tick{width:26px;height:26px}
  .opt{padding:11px 10px}


  /* ── phone tables: keep the columns a person acts on, drop the rest.
     Every hidden figure is one tap away on the detail screen. */
  td,th{white-space:nowrap}
  td b,td .mut{white-space:nowrap}
  table{font-size:12.5px}
  td{padding:12px 9px}
  th{padding:9px 9px;font-size:9.5px}
  td:first-child,th:first-child{padding-left:13px}
  td:last-child,th:last-child{padding-right:13px}
  /* inventory */
  table:has(#invFinBody) :is(th,td):nth-child(4){display:none}
  table:has(#invRawBody) :is(th,td):is(:nth-child(2),:nth-child(4)){display:none}
  table:has(#invMovBody) :is(th,td):nth-child(5){display:none}
  /* reports: district and monthly */
  #v-reports .g2>.card:first-child :is(th,td):nth-child(3),
  #v-reports .g2>.card:last-child :is(th,td):nth-child(3){display:none}
  /* sale lines: each line is a small card. Product on top, then qty · rate · amount */
  table.lines thead{display:none}
  table.lines,table.lines tbody{display:block}
  table.lines tr.line{display:grid;grid-template-columns:auto minmax(0,1fr) auto auto;gap:10px 10px;
    padding:12px 12px 14px;border-bottom:1px solid var(--line);align-items:center;white-space:normal}
  table.lines td{display:block;padding:0!important;border:0;white-space:normal}
  table.lines td.lpc{grid-column:1/-1;min-width:0}
  table.lines .lr{width:100%}
  table.lines .lt{padding-top:0!important;font-size:15px}
  .lpl{left:0;right:0}
  /* profile payments */
  table:has(#pPayBody) :is(th,td):nth-child(3){display:none}
  table:has(#custBody) :is(th,td):is(:nth-child(1),:nth-child(3),:nth-child(5),:nth-child(6),:nth-child(9),:nth-child(10)){display:none}
  table:has(#distBody) :is(th,td):nth-child(5){display:none}
  table:has(#acBody) :is(th,td):is(:nth-child(2),:nth-child(5)){display:none}
  table:has(#acBody) td:nth-child(3){white-space:normal;min-width:120px}
  table:has(#pendBody) :is(th,td):nth-child(3){display:none}
  table:has(#pdBuyerBody) :is(th,td):is(:nth-child(2),:nth-child(3)){display:none}
  table:has(#pdOrderBody) :is(th,td):is(:nth-child(2),:nth-child(5),:nth-child(7)){display:none}
  table:has(#pOrderBody) :is(th,td):is(:nth-child(3),:nth-child(5)){display:none}
  table:has(#topCust) td:first-child{white-space:normal}
  table:has(#custBody) td:nth-child(2),table:has(#pdBuyerBody) td:first-child{white-space:normal;min-width:110px}
  table:has(#lap60) :is(th,td):nth-child(4),table:has(#lap90) :is(th,td):nth-child(4){display:none}

  /* ── cards and tables */
  .card,.pcard,.kpi,.hero{border-radius:10px}
  .ch{padding:12px 13px;flex-wrap:wrap;gap:7px}
  .ch h3{font-size:13px}
  .cb{padding:13px}
  .g13,.g2,.g3{grid-template-columns:minmax(0,1fr)}
  .hero{padding:14px;gap:12px}
  .hav{width:48px;height:48px;border-radius:13px;font-size:19px}
  .hpic{width:64px;height:64px;border-radius:15px}
  .pgrid{grid-template-columns:minmax(0,1fr)}
  .repgrid{grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr))}
  .tl{padding-left:22px}

  /* ── sheets slide up from the bottom, the pattern every phone user knows */
  .scrim{align-items:flex-end;padding:0}
  .sheet{width:100%;border-radius:14px 14px 0 0;max-height:92vh;overflow:auto;
    padding-bottom:env(safe-area-inset-bottom,0px)}
  .sheet .grid2{grid-template-columns:minmax(0,1fr)}
  .tierpick{grid-template-columns:minmax(0,1fr)} .tierpick button{min-height:56px}
  .dp{left:12px!important;right:12px;width:auto} .dp .dpg button{height:42px}
  .toast{left:12px;right:12px;bottom:calc(84px + env(safe-area-inset-bottom,0px));
    transform:none;max-width:none;font-size:13px}
  .toast.show{animation:rise .3s var(--ease)}
  .notif{position:fixed;left:12px;right:12px;top:60px;width:auto}
}

@media (max-width:400px){
  /* the cheapest Androids: every pixel of a table row is spoken for */
  table{font-size:12px}
  td{padding:11px 6px}
  th{padding:9px 6px}
  td:first-child,th:first-child{padding-left:11px}
  td:last-child,th:last-child{padding-right:11px}
  .rank{display:none}
  .pill{padding:2px 6px;font-size:10.5px}
  td .mut{font-size:11.5px}
  .kv{font-size:17.5px}
  .nav a{min-width:58px;padding:8px 7px}
  .ph h1{font-size:20px}
}
'''
