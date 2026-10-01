# -*- coding: utf-8 -*-
"""Shada BMS · design layer — palette, type, motion, elevation.

Extends the website tokens rather than inventing a second system. Everything
here is additive: the brand green, the bottle green and the paper greys are
unchanged, so the BMS and the website read as one product.
"""

DESIGN = '''
/* ═══════════════════════════════════════════════════════════════════════════
   1 · PALETTE
   The website gives us brand, ink and paper. An admin tool needs three more
   things the marketing site never needed: a semantic state scale, an elevation
   scale, and a data-visualisation ramp.
   ═══════════════════════════════════════════════════════════════════════════ */
:root{
  /* type */
  --ff:'Plus Jakarta Sans','Hind Siliguri',system-ui,sans-serif;
  --fm:ui-monospace,'SF Mono',Menlo,Consolas,monospace;   /* invoice numbers, codes */

  /* brand, unchanged from the website */
  --ink:#0A2617; --ink2:#123222; --ink3:#1A4430;
  --brand:#089830; --brand-d:#067426; --brand-l:#0EA63A; --brand-soft:#E6F4EA;
  --leaf:#5FD48A; --leaf-d:#8CE8AC;

  /* neutrals */
  --paper:#FFFFFF; --paper2:#F5F5F3; --paper3:#ECECE9; --paper4:#E2E2DE;
  --tx:#1D1D1F; --tx2:#6E6E73; --tx3:#A1A1A6; --tx4:#C4C4C8;
  --on:#F5F5F7; --on2:#A1A1A6; --on3:#6F8579;
  --line:rgba(0,0,0,.08); --line2:rgba(0,0,0,.14); --line-d:rgba(255,255,255,.12);

  /* semantic states. One hue per meaning, never reused for decoration. */
  --ok:#089830;    --ok-soft:#E6F4EA;    --ok-d:#067426;
  --warn:#E0B810;  --warn-soft:#FFF6D9;  --warn-d:#8A6A00;
  --bad:#C0392B;   --bad-soft:#FDECEA;   --bad-d:#96271B;
  --info:#123A72;  --info-soft:#E8EEF8;  --info-d:#0C2A55;

  /* data visualisation ramp, colour-blind safe order */
  --d1:#089830; --d2:#123A72; --d3:#E0B810; --d4:#8E1F35; --d5:#5A8F3C; --d6:#2F4A3C;

  /* elevation. Greens rather than greys, so shadows feel part of the brand. */
  --e1:0 1px 2px rgba(10,38,23,.06);
  --e2:0 2px 8px rgba(10,38,23,.07);
  --e3:0 8px 24px rgba(10,38,23,.10);
  --e4:0 18px 44px rgba(10,38,23,.14);
  --focus:0 0 0 3px rgba(8,152,48,.18);

  /* radius */
  --r1:8px; --r:10px; --r2:14px; --r3:18px; --rp:999px;

  /* motion. Two curves and three durations, nothing else. */
  --ease:cubic-bezier(.22,1,.36,1);
  --ease-out:cubic-bezier(.16,1,.3,1);
  --t1:.14s; --t2:.24s; --t3:.42s;
}

/* ═══════════════════════════════════════════════════════════════════════════
   2 · TYPE
   One family, six roles. Numbers are tabular everywhere so columns line up,
   and identifiers are monospace so an invoice number can be read aloud.
   ═══════════════════════════════════════════════════════════════════════════ */
body{font-size:14.5px;line-height:1.5;letter-spacing:-.008em}
h1{font-size:clamp(21px,2.2vw,27px);font-weight:600;letter-spacing:-.03em;line-height:1.14}
h2{font-size:14px;font-weight:600;letter-spacing:-.014em}
h3{font-size:15.5px;font-weight:600;letter-spacing:-.016em}
.mono,.inv{font-family:var(--fm);font-size:.94em;letter-spacing:-.02em}
.num,.tb .r,.kpi .v{font-variant-numeric:tabular-nums}
.eyebrow{font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3)}

/* ═══════════════════════════════════════════════════════════════════════════
   3 · MOTION
   Purposeful only: state changes, route changes, and feedback after an action.
   Nothing loops, nothing decorates. All of it stops under reduced-motion.
   ═══════════════════════════════════════════════════════════════════════════ */
@keyframes viewIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes rowIn{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
@keyframes toastIn{from{opacity:0;transform:translateY(14px) scale(.97)}to{opacity:1;transform:none}}
@keyframes pop{0%{transform:scale(1)}45%{transform:scale(1.06)}100%{transform:scale(1)}}
@keyframes shimmer{0%{background-position:-420px 0}100%{background-position:420px 0}}
@keyframes drawIn{from{stroke-dashoffset:var(--len)}to{stroke-dashoffset:0}}

.view.on{animation:viewIn var(--t3) var(--ease-out) both}
.view.on .kpi{animation:rowIn var(--t3) var(--ease-out) both}
.view.on .kpi:nth-child(2){animation-delay:.04s}
.view.on .kpi:nth-child(3){animation-delay:.08s}
.view.on .kpi:nth-child(4){animation-delay:.12s}
.view.on .kpi:nth-child(5){animation-delay:.16s}
.kpi .v.bump{animation:pop var(--t3) var(--ease)}
.chart .ln{stroke-dasharray:var(--len);animation:drawIn .9s var(--ease-out) both}

.skel{background:linear-gradient(90deg,var(--paper2) 25%,var(--paper3) 37%,var(--paper2) 63%);
  background-size:840px 100%;animation:shimmer 1.3s linear infinite;border-radius:6px;color:transparent}

@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;
    transition-duration:.01ms!important}
}

/* ═══════════════════════════════════════════════════════════════════════════
   4 · REFINEMENTS on the base components
   ═══════════════════════════════════════════════════════════════════════════ */
.rail{background:linear-gradient(180deg,var(--ink) 0%,#08200F 100%);box-shadow:var(--e2)}
.rail a{position:relative}
.rail a.on::before{content:"";position:absolute;left:-12px;top:9px;bottom:9px;width:3px;
  border-radius:0 3px 3px 0;background:var(--leaf)}
.brandrow b{font-size:15px;letter-spacing:.06em}

.card{box-shadow:var(--e1);transition:box-shadow var(--t2) var(--ease)}
.card:hover{box-shadow:var(--e2)}
.kpi{box-shadow:var(--e1);transition:transform var(--t2) var(--ease),box-shadow var(--t2) var(--ease)}
.kpi:hover{transform:translateY(-2px);box-shadow:var(--e3)}

.btn{transition:transform var(--t1) var(--ease),background var(--t2),border-color var(--t2),box-shadow var(--t2)}
.btn:active{transform:scale(.97)}
.btn.pri{box-shadow:0 2px 8px rgba(8,152,48,.26),inset 0 1px 0 rgba(255,255,255,.22)}
.btn.pri:hover{box-shadow:0 5px 16px rgba(8,152,48,.32)}
.btn:focus-visible,.in:focus-visible,.chips button:focus-visible,.rail a:focus-visible{
  outline:none;box-shadow:var(--focus)}

.chips button{transition:all var(--t1) var(--ease)}
.chips button:active{transform:scale(.96)}
.tb tbody tr{transition:background var(--t1)}
.pill{transition:all var(--t1)}

/* ── toast ───────────────────────────────────────────────────────────── */
.toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);z-index:90;
  display:none;align-items:center;gap:11px;background:var(--ink);color:#fff;
  padding:13px 20px;border-radius:var(--rp);box-shadow:var(--e4);font-size:14px;font-weight:500;
  max-width:92vw}
.toast.show{display:flex;animation:toastIn var(--t2) var(--ease-out) both}
.toast svg{width:17px;height:17px;color:var(--leaf);flex:0 0 auto}
.toast b{font-weight:600}

/* ── empty state for filtered tables ─────────────────────────────────── */
.none{padding:34px 18px;text-align:center;color:var(--tx3);font-size:14px}
.none b{display:block;color:var(--tx2);font-weight:600;margin-bottom:3px}
'''
