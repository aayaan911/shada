#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shada BMS · working prototype.

One file, 8 menus, and the interactions that matter actually work:
  · dashboard filter tabs swap the KPIs and redraw the chart
  · sales entry recalculates line totals, subtotal, total and due as you type
  · add and remove sale lines
  · save shows a toast and returns to the dashboard
  · search filters the visible table
  · report type cards switch the report
  · inventory and accounts chips filter their rows

Still no PHP and no database. This is Phase 0: a design and behaviour approval,
not production code. The real screens are rendered by the plugin.
"""
import os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bms_one import (tk, IC, NAV, CSS, CSS2, rail, chart_svg,
                     dashboard, sales_entry, customer_profile, customer_timeline,
                     inventory, accounts, reports, settings, PRODUCTS)
from bms_design import DESIGN

OUT = '/tmp/bms'

# ═════════════════════════════════════════════════════════════════════════
#  PERIOD DATA — what each dashboard filter tab shows.
#  Five periods, five sets of numbers and five chart series. In production
#  these come from shada_daily_summary, one indexed row per day, never a
#  live aggregate over the sales table.
# ═════════════════════════════════════════════════════════════════════════
PERIODS = {
 'today': {
   'label':'Today', 'sub':'Saturday, 26 September 2026',
   'kpi':[18420,11900,486300,5,2],
   'delta':[('up','+12% vs yesterday'),('up','+4%'),('fl','across 34 customers'),
            ('up','3 from the website'),('fl','below reorder level')],
   'chart':[3,5,4,8,6,11,9,14,12,18,15,21,19,24,22,28,25,31,29,34],
   'chartLabel':'Sales today, by hour'},
 'week': {
   'label':'This week', 'sub':'21 to 26 September 2026',
   'kpi':[112400,86200,486300,11,3],
   'delta':[('up','+9% vs last week'),('up','+7%'),('fl','across 34 customers'),
            ('up','6 from the website'),('fl','below reorder level')],
   'chart':[62,74,58,88,96,71,112],
   'chartLabel':'Sales this week, by day'},
 'month': {
   'label':'This month', 'sub':'September 2026',
   'kpi':[486300,392800,486300,5,2],
   'delta':[('up','+16% vs August'),('up','+11%'),('fl','across 34 customers'),
            ('up','3 from the website'),('fl','below reorder level')],
   'chart':[42,55,38,61,72,58,80,66,91,74,88,96,83,101,94,112,105,98,121,114,
            131,118,142,126,155,139,148,162,151,168],
   'chartLabel':'Sales, last 30 days'},
 'year': {
   'label':'This year', 'sub':'January to September 2026',
   'kpi':[3184700,2698400,486300,5,2],
   'delta':[('up','+38% vs 2025'),('up','+34%'),('fl','across 34 customers'),
            ('up','3 from the website'),('fl','below reorder level')],
   'chart':[186,212,198,244,268,241,302,336,318,389,419,486],
   'chartLabel':'Sales this year, by month'},
 'custom': {
   'label':'Custom range', 'sub':'01 July to 26 September 2026',
   'kpi':[1293600,1078900,486300,5,2],
   'delta':[('up','+21% vs the quarter before'),('up','+18%'),('fl','across 34 customers'),
            ('up','3 from the website'),('fl','below reorder level')],
   'chart':[388,419,486],
   'chartLabel':'Sales, July to September'},
}

def _fmt(i, v):
    return str(v) if i in (3, 4) else tk(v)

PERIOD_JSON = json.dumps({
  k: {'label':p['label'], 'sub':p['sub'], 'chartLabel':p['chartLabel'], 'chart':p['chart'],
      'kpi':[_fmt(i, v) for i, v in enumerate(p['kpi'])],
      'delta':[[c, t] for c, t in p['delta']]}
  for k, p in PERIODS.items()}, ensure_ascii=False)

PRODUCT_JSON = json.dumps([{'n':f'{n} · {s}', 'r':r, 'w':w} for n, s, r, w in PRODUCTS],
                          ensure_ascii=False)


# ═════════════════════════════════════════════════════════════════════════
#  Rewrite the two screens that need live behaviour, so the JS has hooks.
# ═════════════════════════════════════════════════════════════════════════
import re

def wire_dashboard(html):
    """Give the KPI values, deltas, chips, chart and subtitle stable hooks."""
    # chips become period buttons
    old_chips = ''.join(
        f'<button aria-pressed="{"true" if i==2 else "false"}">{t}</button>'
        for i, t in enumerate(['Today','This week','This month','This year','Custom range']))
    new_chips = ''.join(
        f'<button data-period="{k}" aria-pressed="{"true" if k=="month" else "false"}">{v["label"]}</button>'
        for k, v in PERIODS.items())
    html = html.replace(old_chips, new_chips)

    # KPI values and deltas get indexes
    n = [0]
    def tag_v(m):
        i = n[0]; n[0] += 1
        return f'<span class="v" data-kpi="{i}">'
    html = re.sub(r'<span class="v">', tag_v, html, count=5)
    d = [0]
    def tag_d(m):
        i = d[0]; d[0] += 1
        return f'<span class="d {m.group(1)}" data-delta="{i}">'
    html = re.sub(r'<span class="d (up|dn|fl)">', tag_d, html, count=5)

    # subtitle + chart get ids
    html = html.replace('<div class="sub">Saturday, 26 September 2026 · everything below updates from one sales entry</div>',
        '<div class="sub"><span id="periodSub">Saturday, 26 September 2026</span> · everything below updates from one sales entry</div>')
    html = html.replace('<h2>Sales, last 30 days</h2>', '<h2 id="chartTitle">Sales, last 30 days</h2>')
    html = html.replace('<div class="chart">', '<div class="chart" id="chartBox">')
    # the search box filters tables
    html = html.replace('<input placeholder="Search customer, phone, invoice, memo">',
                        '<input id="globalSearch" placeholder="Search customer, phone, invoice, memo">')
    return html


def wire_sales(html):
    """Make the sales entry a live calculator."""
    opts = ''.join(f'<option value="{w}">{n} · {s} — {tk(r)}</option>' for n, s, r, w in PRODUCTS)
    rows = ''
    for pi, q in [(0, 6), (3, 12), (4, 4)]:
        n, s, r, w = PRODUCTS[pi]
        sel = ''.join(
            f'<option value="{ww}"{" selected" if j==pi else ""}>{nn} · {ss} — {tk(rr)}</option>'
            for j, (nn, ss, rr, ww) in enumerate(PRODUCTS))
        rows += (f'<tr class="line">'
                 f'<td><select class="in sel">{sel}</select></td>'
                 f'<td style="width:92px"><input class="in r qty" value="{q}" inputmode="numeric"></td>'
                 f'<td style="width:116px"><input class="in price" value="{w}" inputmode="numeric"></td>'
                 f'<td class="r" style="width:118px"><b class="ltot">{tk(q*w)}</b></td>'
                 f'<td style="width:52px"><button class="iconbtn del" aria-label="Remove line">{IC["trash"]}</button></td>'
                 f'</tr>')

    # swap the static table body for the live one
    html = re.sub(r'<tbody>(?:(?!</tbody>).)*?</tbody>\s*</table>\s*<div class="addline">',
                  f'<tbody id="lineBody">{rows}</tbody></table><div class="addline">',
                  html, count=1, flags=re.S)
    html = html.replace('<button class="btn">' + IC['plus'] + 'Add line</button>',
                        '<button class="btn" id="addLine">' + IC['plus'] + 'Add line</button>')
    # totals get ids
    html = re.sub(r'<div class="row">Subtotal <b>[^<]*</b></div>',
                  '<div class="row">Subtotal <b id="tSub">৳0</b></div>', html)
    html = re.sub(r'<div class="row">Discount <b>[^<]*</b></div>',
                  '<div class="row">Discount <b>-<input class="in r" id="tDisc" value="400" '
                  'inputmode="numeric" style="height:30px;width:92px;display:inline-block;'
                  'text-align:right;padding:0 8px;font-size:14px"></b></div>', html)
    html = re.sub(r'<div class="row">Delivery <b>[^<]*</b></div>',
                  '<div class="row">Delivery <b><input class="in r" id="tDeliv" value="250" '
                  'inputmode="numeric" style="height:30px;width:92px;display:inline-block;'
                  'text-align:right;padding:0 8px;font-size:14px"></b></div>', html)
    html = re.sub(r'<div class="row big">Total <b>[^<]*</b></div>',
                  '<div class="row big">Total <b id="tTotal">৳0</b></div>', html)
    html = html.replace('<input class="in r" value="8000" inputmode="numeric">',
                        '<input class="in r" id="tPaid" value="8000" inputmode="numeric">')
    html = re.sub(r'<b style="font-size:20px">[^<]*</b>',
                  '<b style="font-size:20px" id="tDue">৳0</b>', html)
    html = html.replace('<span style="font-weight:600">Due after this sale</span>',
                        '<span style="font-weight:600" id="tDueLabel">Due after this sale</span>')
    html = html.replace('<button class="btn pri lg" style="width:100%;margin-top:14px">',
                        '<button class="btn pri lg" id="saveSale" style="width:100%;margin-top:14px">')
    # the "what this updates" panel gets a live line count
    html = html.replace('stock for 3 products,', 'stock for <b id="nLines">3</b> products,')
    html = html.replace('<span class="sp">3 lines</span>', '<span class="sp"><b id="nLines2">3</b> lines</span>')
    return html


# ═════════════════════════════════════════════════════════════════════════
#  THE ENGINE
# ═════════════════════════════════════════════════════════════════════════
JS = '''
/* ═══════════════════════════════════════════════════════════════════════
   Shada BMS prototype engine.
   Plain JavaScript, no framework, no build step. Roughly 200 lines, which
   is the point: a prototype that needs a toolchain is a prototype nobody
   opens in six months.
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var PERIODS = __PERIODS__;
  var PRODUCTS = __PRODUCTS__;

  /* ── money, Bangla lakh grouping ───────────────────────────────────── */
  function tk(n) {
    n = Math.round(n || 0);
    var s = String(Math.abs(n)), out;
    if (s.length > 3) {
      var head = s.slice(0, -3), tail = s.slice(-3), parts = [];
      while (head.length > 2) { parts.unshift(head.slice(-2)); head = head.slice(0, -2); }
      if (head) parts.unshift(head);
      out = parts.join(',') + ',' + tail;
    } else out = s;
    return '৳' + (n < 0 ? '-' : '') + out;
  }
  function num(el) { return parseFloat(String(el.value).replace(/[^0-9.-]/g, '')) || 0; }

  /* ── 1 · router ────────────────────────────────────────────────────── */
  var views = document.querySelectorAll('.view');
  var links = document.querySelectorAll('.rail a[data-go]');

  function go(name) {
    var found = false;
    views.forEach(function (v) {
      var on = v.id === 'v-' + name;
      v.classList.toggle('on', on);
      if (on) { found = true; document.title = v.dataset.title + ' · Shada BMS'; }
    });
    if (!found) { location.hash = 'dashboard'; return; }
    links.forEach(function (a) { a.classList.toggle('on', a.dataset.go === name); });
    window.scrollTo(0, 0);
  }
  function fromHash() { go((location.hash || '#dashboard').slice(1)); }
  window.addEventListener('hashchange', fromHash);

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    var n = a.getAttribute('href').slice(1);
    if (document.getElementById('v-' + n)) {
      e.preventDefault();
      if (location.hash !== '#' + n) location.hash = n; else go(n);
    }
  });

  /* ── 2 · toast ─────────────────────────────────────────────────────── */
  var toast = document.getElementById('toast'), toastT;
  function say(msg) {
    if (!toast) return;
    toast.querySelector('span').innerHTML = msg;
    toast.classList.add('show');
    clearTimeout(toastT);
    toastT = setTimeout(function () { toast.classList.remove('show'); }, 3200);
  }

  /* ── 3 · chart, drawn not imported ─────────────────────────────────── */
  function drawChart(vals) {
    var box = document.getElementById('chartBox');
    if (!box) return;
    var w = 760, h = 150, lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
    var rng = (hi - lo) || 1, step = w / Math.max(vals.length - 1, 1), pts = [];
    for (var i = 0; i < vals.length; i++)
      pts.push([i * step, h - ((vals[i] - lo) / rng) * (h - 18) - 9]);
    var line = 'M' + pts.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' L');
    var area = line + ' L' + w + ',' + h + ' L0,' + h + ' Z';
    var grid = '';
    for (var k = 0; k < 4; k++) grid += '<line class="gl" x1="0" y1="' + (h * k / 3) + '" x2="' + w + '" y2="' + (h * k / 3) + '"/>';
    var last = pts[pts.length - 1];
    box.innerHTML =
      '<svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" role="img" aria-label="Sales trend">' +
      '<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">' +
      '<stop offset="0" stop-color="#089830" stop-opacity=".18"/>' +
      '<stop offset="1" stop-color="#089830" stop-opacity="0"/></linearGradient></defs>' +
      grid + '<path class="ar" d="' + area + '"/><path class="ln" d="' + line + '"/>' +
      '<circle class="dot" cx="' + last[0].toFixed(1) + '" cy="' + last[1].toFixed(1) + '" r="4"/></svg>';
    var ln = box.querySelector('.ln');
    if (ln && ln.getTotalLength) ln.style.setProperty('--len', ln.getTotalLength());
  }

  /* ── 4 · dashboard filter tabs ─────────────────────────────────────── */
  function setPeriod(key) {
    var p = PERIODS[key];
    if (!p) return;
    document.querySelectorAll('[data-period]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.period === key));
    });
    document.querySelectorAll('[data-kpi]').forEach(function (el, i) {
      if (p.kpi[i] === undefined) return;
      el.textContent = p.kpi[i];
      el.classList.remove('bump'); void el.offsetWidth; el.classList.add('bump');
    });
    document.querySelectorAll('[data-delta]').forEach(function (el, i) {
      if (!p.delta[i]) return;
      el.className = 'd ' + p.delta[i][0];
      el.setAttribute('data-delta', i);
      el.textContent = p.delta[i][1];
    });
    var sub = document.getElementById('periodSub');   if (sub) sub.textContent = p.sub;
    var ct = document.getElementById('chartTitle');   if (ct) ct.textContent = p.chartLabel;
    drawChart(p.chart);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-period]');
    if (b) setPeriod(b.dataset.period);
  });

  /* ── 5 · chip groups that are not the period filter ────────────────── */
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.chips button:not([data-period])');
    if (!b) return;
    b.parentNode.querySelectorAll('button').forEach(function (x) {
      x.setAttribute('aria-pressed', String(x === b));
    });
    var view = b.closest('.view');
    var label = b.textContent.trim().toLowerCase();
    var tables = view ? view.querySelectorAll('.tb tbody') : [];
    tables.forEach(function (tb) {
      var shown = 0;
      tb.querySelectorAll('tr').forEach(function (tr) {
        var hit = label === 'all' || label === 'everything' ||
                  tr.textContent.toLowerCase().indexOf(label.split(' ')[0]) > -1;
        tr.style.display = hit ? '' : 'none';
        if (hit) shown++;
      });
      if (!shown) {
        tb.querySelectorAll('tr').forEach(function (tr) { tr.style.display = ''; });
      }
    });
  });

  /* ── 6 · global search filters every visible table ─────────────────── */
  var search = document.getElementById('globalSearch');
  if (search) search.addEventListener('input', function () {
    var q = this.value.trim().toLowerCase();
    document.querySelectorAll('.view.on .tb tbody tr').forEach(function (tr) {
      tr.style.display = (!q || tr.textContent.toLowerCase().indexOf(q) > -1) ? '' : 'none';
    });
  });

  /* ── 7 · sales entry, live calculator ──────────────────────────────── */
  var body = document.getElementById('lineBody');

  function lineRow(pi) {
    pi = pi || 0;
    var tr = document.createElement('tr');
    tr.className = 'line';
    var opts = PRODUCTS.map(function (p, j) {
      return '<option value="' + p.w + '"' + (j === pi ? ' selected' : '') + '>' +
             p.n + ' — ' + tk(p.r) + '</option>';
    }).join('');
    tr.innerHTML =
      '<td><select class="in sel">' + opts + '</select></td>' +
      '<td style="width:92px"><input class="in r qty" value="1" inputmode="numeric"></td>' +
      '<td style="width:116px"><input class="in price" value="' + PRODUCTS[pi].w + '" inputmode="numeric"></td>' +
      '<td class="r" style="width:118px"><b class="ltot">৳0</b></td>' +
      '<td style="width:52px"><button class="iconbtn del" aria-label="Remove line">' +
      document.querySelector('.iconbtn.del').innerHTML + '</button></td>';
    return tr;
  }

  function recalc() {
    if (!body) return;
    var sub = 0;
    body.querySelectorAll('tr.line').forEach(function (tr) {
      var q = num(tr.querySelector('.qty')), p = num(tr.querySelector('.price'));
      var t = q * p;
      tr.querySelector('.ltot').textContent = tk(t);
      sub += t;
    });
    var disc = num(document.getElementById('tDisc'));
    var dlv  = num(document.getElementById('tDeliv'));
    var paid = num(document.getElementById('tPaid'));
    var total = sub - disc + dlv;
    var due = total - paid;
    var set = function (id, v) { var e = document.getElementById(id); if (e) e.textContent = tk(v); };
    set('tSub', sub); set('tTotal', total); set('tDue', due);
    var n = body.querySelectorAll('tr.line').length;
    ['nLines', 'nLines2'].forEach(function (id) {
      var e = document.getElementById(id); if (e) e.textContent = n;
    });
    /* A negative due is an advance, not a negative number. Say so, because a
       minus sign next to money is how a bookkeeper loses confidence in a tool. */
    var dueEl = document.getElementById('tDue');
    var dueLbl = document.getElementById('tDueLabel');
    if (dueEl) {
      if (due > 0)      { dueEl.textContent = tk(due);   dueEl.style.color = 'var(--warn-d)'; }
      else if (due < 0) { dueEl.textContent = tk(-due);  dueEl.style.color = 'var(--ok)'; }
      else              { dueEl.textContent = tk(0);     dueEl.style.color = 'var(--ok)'; }
      if (dueLbl) dueLbl.textContent = due > 0 ? 'Due after this sale'
                    : (due < 0 ? 'Advance held for next order' : 'Fully paid, no due');
    }
  }

  if (body) {
    body.addEventListener('input', function (e) {
      if (e.target.classList.contains('sel')) {
        var tr = e.target.closest('tr');
        tr.querySelector('.price').value = e.target.value;
      }
      recalc();
    });
    body.addEventListener('change', recalc);
    body.addEventListener('click', function (e) {
      var d = e.target.closest('.del');
      if (!d) return;
      if (body.querySelectorAll('tr.line').length <= 1) { say('A sale needs at least one line.'); return; }
      d.closest('tr').remove();
      recalc();
    });
    var add = document.getElementById('addLine');
    if (add) add.addEventListener('click', function () {
      body.appendChild(lineRow(0));
      recalc();
      body.lastElementChild.querySelector('.qty').focus();
    });
    ['tDisc', 'tDeliv', 'tPaid'].forEach(function (id) {
      var e = document.getElementById(id);
      if (e) e.addEventListener('input', recalc);
    });
    recalc();
  }

  var save = document.getElementById('saveSale');
  if (save) save.addEventListener('click', function () {
    var n = body ? body.querySelectorAll('tr.line').length : 0;
    var total = document.getElementById('tTotal');
    say('<b>Sale saved.</b> Invoice INV-2609-0149, ' + n + ' lines, ' +
        (total ? total.textContent : '') + '. Stock, due and every report updated.');
    setTimeout(function () { location.hash = 'dashboard'; }, 900);
  });

  /* ── 8 · report type cards switch the report ───────────────────────── */
  document.addEventListener('click', function (e) {
    var r = e.target.closest && e.target.closest('.rep');
    if (!r) return;
    document.querySelectorAll('.rep').forEach(function (x) { x.classList.toggle('on', x === r); });
    say('<b>' + r.querySelector('b').textContent + '</b> selected. Export and print use this range.');
  });

  /* ── 9 · buttons that are not wired yet say so, rather than doing nothing ── */
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.btn');
    if (!b || b.id === 'saveSale' || b.id === 'addLine' || b.getAttribute('href')) return;
    say('<b>' + b.textContent.trim() + '</b> is designed but not wired. Phase 0 is the design approval.');
  });

  /* boot */
  fromHash();
  setPeriod('month');
})();
'''


def build():
    views = {
      'dashboard':         wire_dashboard(dashboard()),
      'sales-entry':       wire_sales(sales_entry()),
      'customer-profile':  customer_profile(),
      'customer-timeline': customer_timeline(),
      'inventory':         inventory(),
      'accounts':          accounts(),
      'reports':           reports(),
      'settings':          settings(),
    }
    titles = {k: t for k, t, _ in NAV}
    sections = ''.join(
        f'<section class="view{" on" if k=="dashboard" else ""}" id="v-{k}" '
        f'data-title="{titles[k]}">{v}</section>' for k, v in views.items())

    js = (JS.replace('__PERIODS__', PERIOD_JSON)
            .replace('__PRODUCTS__', PRODUCT_JSON))

    toast = (f'<div class="toast" id="toast" role="status" aria-live="polite">'
             f'{IC["check"]}<span></span></div>')

    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light">
<title>Dashboard · Shada BMS</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}{CSS2}{DESIGN}</style></head><body>
<div class="demo">DEMO DATA · Phase 0 working prototype · filters, sales entry and search all work · no real customer or sales data</div>
<div class="app">{rail()}<main class="main">{sections}</main></div>
{toast}
<script>{js}</script>
</body></html>'''


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    html = build()
    open(f'{OUT}/shada-bms-prototype.html', 'w', encoding='utf-8').write(html)
    print(f'shada-bms-prototype.html  {round(len(html)/1024)} KB  ·  {len(NAV)} menus  ·  '
          f'{len(PERIODS)} live filter periods')
