# -*- coding: utf-8 -*-
"""Customer list, follow-ups, notifications and the Stage 2 KPI row.

Everything the client listed that had no screen yet. All of it visual only:
this is a design prototype for approval, not working code.
"""
from bms_one import IC, tk
from bms_customers import as_dict

CUST = as_dict()


def customers_list():
    rows = ''
    for c in CUST:
        duecell = ('<span class="pill paid">clear</span>' if c['due'] == 0
                   else f'<span class="pill due">{tk(c["due"])}</span>')
        tier = {'Wholesale':'ok','Re-wholesale':'web','Retail':'man'}[c['tier']]
        rows += (
          f'<tr class="crow" data-code="{c["code"]}" tabindex="0" role="button" '
          f'aria-label="Open {c["name"]}">'
          f'<td><span class="mono">{c["code"]}</span></td>'
          f'<td><b>{c["name"]}</b><div class="mut">{c["area"]}, {c["district"]}</div></td>'
          f'<td class="mono mut">{c["phone"]}</td>'
          f'<td><span class="pill {tier}">{c["tier"]}</span></td>'
          f'<td class="r mut">{c["orders"]}</td>'
          f'<td class="r"><b>{tk(c["sold"])}</b></td>'
          f'<td class="r">{duecell}</td>'
          f'<td class="r mut">{c["last"]}</td>'
          f'<td class="r"><span class="go2">{IC["chev"]}</span></td></tr>')

    tot_sold = sum(c['sold'] for c in CUST)
    tot_due  = sum(c['due'] for c in CUST)
    owing    = len([c for c in CUST if c['due'] > 0])

    return f'''
<div class="top">
  <div><h1>Customers</h1><div class="sub">{len(CUST)} customers. Click any row to open the full profile.</div></div>
  <div class="sp">
    <span class="srch">{IC['search']}<input id="custSearch" placeholder="Search by ID, name, phone or district"></span>
    <a class="btn">{IC['plus']}Add customer</a>
  </div>
</div>
<div class="chips">
  <button aria-pressed="true">All</button><button>Wholesale</button><button>Re-wholesale</button>
  <button>Retail</button><button>With due</button><button>Dhaka</button>
</div>
<div class="kpis">
  <div class="kpi"><span class="k">Customers</span><span class="v">{len(CUST)}</span><span class="d up">+3 this quarter</span></div>
  <div class="kpi"><span class="k">Lifetime sales</span><span class="v">{tk(tot_sold)}</span><span class="d up">+21%</span></div>
  <div class="kpi due"><span class="k">Total due</span><span class="v">{tk(tot_due)}</span><span class="d fl">{owing} customers owing</span></div>
  <div class="kpi"><span class="k">Average order</span><span class="v">{tk(tot_sold/sum(c["orders"] for c in CUST))}</span><span class="d up">+6%</span></div>
</div>
<div class="card">
  <div class="h"><h2>All customers</h2><span class="sp">ranked by lifetime value</span></div>
  <div class="b flush"><table class="tb" id="custTable">
    <thead><tr><th>ID</th><th>Customer</th><th>Phone</th><th>Tier</th><th class="r">Orders</th>
      <th class="r">Lifetime</th><th class="r">Due</th><th class="r">Last order</th><th></th></tr></thead>
    <tbody>{rows}</tbody></table>
    <div class="none" id="custNone" style="display:none"><b>No customer matches that.</b>Try a different ID, name or phone.</div>
  </div>
</div>
<p class="note">Due is never stored. Every figure on this page is derived from that customer's own
orders and payments, which is why the list total and each profile can never disagree.</p>
'''


def followups():
    F = [('Hasan','Khulna','01911 620377','68 days','Called 12 Sep, asked to call back after Eid','Due today','warn'),
         ('Tanvir','Rajshahi','01515 774102','74 days','No contact yet','Overdue 4 days','bad'),
         ('Ali','Dhaka','01712 887401','118 days','Switched to a local supplier, worth a visit','Due in 2 days','ok'),
         ('Imran','Mymensingh','01998 112640','61 days','Asked for a price list','Due in 5 days','ok'),
         ('Sohel','Barishal','01813 445090','96 days','Shop closed for renovation, reopening October','Due 12 Oct','ok')]
    rows = ''.join(
      f'<tr><td><b>{n}</b><div class="mut">{d}</div></td><td class="mono mut">{p}</td>'
      f'<td class="r mut">{last}</td><td class="mut">{note}</td>'
      f'<td class="r"><span class="pill {"crit" if s=="bad" else ("due" if s=="warn" else "ok")}">{when}</span></td>'
      f'<td class="r"><a class="btn" style="min-height:30px;padding:0 10px;font-size:12.5px">{IC["wa"]}Call</a></td></tr>'
      for n,d,p,last,note,when,s in F)
    return f'''
<div class="top">
  <div><h1>Follow-ups</h1><div class="sub">Who to call today, why, and what was said last time.</div></div>
  <div class="sp"><a class="btn pri">{IC['plus']}Add follow-up</a></div>
</div>
<div class="chips"><button aria-pressed="true">Due today</button><button>Overdue</button>
  <button>This week</button><button>No contact yet</button><button>Done</button></div>
<div class="kpis">
  <div class="kpi alert"><span class="k">Overdue</span><span class="v">1</span><span class="d fl">Tanvir, 4 days</span></div>
  <div class="kpi due"><span class="k">Due today</span><span class="v">1</span><span class="d fl">Hasan</span></div>
  <div class="kpi"><span class="k">This week</span><span class="v">3</span><span class="d fl">scheduled</span></div>
  <div class="kpi"><span class="k">Recovered this month</span><span class="v">{tk(68400)}</span><span class="d up">from 6 follow-ups</span></div>
</div>
<div class="card">
  <div class="h"><h2>Follow-up list</h2><span class="sp">last purchase, last contact, next action</span></div>
  <div class="b flush"><table class="tb"><thead><tr><th>Customer</th><th>Phone</th>
    <th class="r">Last purchase</th><th>Last contact note</th><th class="r">Next follow-up</th><th class="r">Action</th></tr></thead>
    <tbody>{rows}</tbody></table></div>
</div>
<p class="note">A follow-up is generated automatically when a customer crosses 30, 60 or 90 days
without an order. Nobody has to remember to create one.</p>
'''
