# -*- coding: utf-8 -*-
"""Shada BMS · the customer dataset.

Twelve customers with complete records, so the demo can click any row and see a
real profile rather than the same placeholder. Names are the ones in the
client's own spreadsheet where they exist. Everything else is invented and the
screens are flagged DEMO.

Field order matches the shada_customers table we will actually build:
  code, name, phone, district, area, type, since, orders, sold, paid, last
Due is never stored. It is sold minus paid, computed in one place.
"""

# code, name, phone, district, area, tier, since, orders, sold, paid, last order
CUSTOMERS = [
 ('SBF-001','Saddam','01711 234567','Dhaka','Mirpur 11','Wholesale','12 Jan 2026',5,65469,40140,'26 Sep 2026'),
 ('SBF-002','Ali','01712 887401','Dhaka','Jatrabari','Wholesale','04 Feb 2026',3,35786,24304,'31 May 2026'),
 ('SBF-003','Jahid','01819 556230','Bogura','Bogura Sadar','Wholesale','19 Feb 2026',3,20072,4420,'14 Sep 2026'),
 ('SBF-004','Rafiq','01521 330914','Chattogram','Pahartali','Wholesale','02 Mar 2026',3,51959,43241,'11 Sep 2026'),
 ('SBF-005','Nazmul','01777 401226','Sylhet','Zindabazar','Re-wholesale','21 Mar 2026',3,30372,29236,'23 Sep 2026'),
 ('SBF-006','Hasan','01911 620377','Khulna','Sonadanga','Re-wholesale','08 Apr 2026',2,28682,15907,'20 Jul 2026'),
 ('SBF-008','Tanvir','01515 774102','Rajshahi','Boalia','Re-wholesale','29 Apr 2026',2,16466,16466,'14 Jul 2026'),
 ('SBF-007','Mamun','01611 209845','Rangpur','Rangpur Sadar','Re-wholesale','17 Apr 2026',2,16280,6390,'21 Sep 2026'),
 ('SBF-010','Imran','01998 112640','Mymensingh','Bhaluka','Retail','26 May 2026',2,25170,2740,'27 Jul 2026'),
 ('SBF-009','Sohel','01813 445090','Barishal','Barishal Sadar','Retail','11 May 2026',2,17805,1910,'22 Jun 2026'),
 ('SBF-012','Faruk','01881 336704','Cumilla','Cumilla Sadar','Retail','02 Jul 2026',2,24935,24935,'09 Aug 2026'),
 ('SBF-011','Shakil','01733 908215','Dhaka','Uttara','Retail','14 Jun 2026',2,38140,30020,'18 Sep 2026'),
]

# orders per customer: invoice, date, items, total, paid
ORDERS = {
 'SBF-001': [
   ('INV-2609-0148','26 Sep 2026',28,13730,4120,[(0,13,690),(1,5,362),(6,10,295)]),
   ('INV-2609-0121','11 Sep 2026',20,13120,0,[(7,10,295),(4,10,1017)]),
   ('INV-2609-0094','02 Sep 2026',16,5189,2590,[(1,7,362),(6,9,295)]),
   ('INV-2608-0331','21 Aug 2026',17,9878,9878,[(5,11,580),(2,6,583)]),
   ('INV-2608-0287','09 Aug 2026',33,23552,23552,[(4,10,1017),(5,9,580),(2,14,583)]),
 ],
 'SBF-002': [
   ('INV-2605-0212','31 May 2026',22,12805,7680,[(5,7,580),(2,15,583)]),
   ('INV-2605-0180','18 May 2026',27,12384,12384,[(0,10,690),(1,7,362),(6,10,295)]),
   ('INV-2604-0142','27 Apr 2026',16,10597,4240,[(4,3,1017),(5,11,580),(2,2,583)]),
 ],
 'SBF-003': [
   ('INV-2609-0126','14 Sep 2026',25,11707,0,[(6,14,295),(7,5,295),(4,6,1017)]),
   ('INV-2608-0301','16 Aug 2026',4,1996,600,[(3,2,308),(0,2,690)]),
   ('INV-2607-0244','24 Jul 2026',20,6369,3820,[(1,7,362),(6,13,295)]),
 ],
 'SBF-004': [
   ('INV-2609-0147','11 Sep 2026',28,16285,16285,[(5,13,580),(2,15,583)]),
   ('INV-2608-0318','19 Aug 2026',30,18236,18236,[(6,7,295),(7,10,295),(4,13,1017)]),
   ('INV-2607-0261','28 Jul 2026',27,17438,8720,[(4,4,1017),(5,13,580),(2,10,583)]),
 ],
 'SBF-005': [
   ('INV-2609-0146','23 Sep 2026',23,12493,12493,[(2,3,583),(3,8,308),(0,12,690)]),
   ('INV-2608-0294','12 Aug 2026',7,2266,1130,[(1,3,362),(6,4,295)]),
   ('INV-2607-0233','19 Jul 2026',31,15613,15613,[(0,14,690),(1,14,362),(6,3,295)]),
 ],
 'SBF-006': [
   ('INV-2607-0219','20 Jul 2026',27,15907,15907,[(6,13,295),(7,3,295),(4,11,1017)]),
   ('INV-2606-0188','14 Jun 2026',26,12775,0,[(2,9,583),(3,11,308),(0,6,690)]),
 ],
 'SBF-007': [
   ('INV-2609-0145','21 Sep 2026',12,7150,0,[(7,7,295),(4,5,1017)]),
   ('INV-2608-0276','05 Aug 2026',16,9130,6390,[(3,5,308),(0,11,690)]),
 ],
 'SBF-008': [
   ('INV-2607-0214','14 Jul 2026',16,11218,11218,[(7,7,295),(4,9,1017)]),
   ('INV-2606-0171','09 Jun 2026',8,5248,5248,[(7,4,295),(4,4,1017)]),
 ],
 'SBF-009': [
   ('INV-2606-0195','22 Jun 2026',8,4770,1910,[(7,6,370),(4,2,1275)]),
   ('INV-2605-0166','30 May 2026',23,13035,0,[(6,9,370),(7,9,370),(4,5,1275)]),
 ],
 'SBF-010': [
   ('INV-2607-0226','27 Jul 2026',14,9120,2740,[(3,8,450),(0,6,920)]),
   ('INV-2606-0183','11 Jun 2026',20,16050,0,[(3,5,450),(0,15,920)]),
 ],
 'SBF-011': [
   ('INV-2609-0138','18 Sep 2026',32,24610,24610,[(2,12,870),(3,9,450),(0,11,920)]),
   ('INV-2608-0305','17 Aug 2026',17,13530,5410,[(7,9,370),(4,8,1275)]),
 ],
 'SBF-012': [
   ('INV-2608-0283','09 Aug 2026',34,16505,16505,[(0,4,920),(1,15,485),(6,15,370)]),
   ('INV-2607-0238','21 Jul 2026',13,8430,8430,[(7,9,370),(4,4,1275)]),
 ],
}

# payments per customer: date, method, amount, against invoice
PAYMENTS = {
 'SBF-001': [('26 Sep 2026','bKash',4120,'INV-2609-0148'),('02 Sep 2026','Bank',2590,'INV-2609-0094'),('21 Aug 2026','Cash',9878,'INV-2608-0331'),('09 Aug 2026','bKash',23552,'INV-2608-0287')],
 'SBF-002': [('31 May 2026','Cash',7680,'INV-2605-0212'),('18 May 2026','bKash',12384,'INV-2605-0180'),('27 Apr 2026','Cash',4240,'INV-2604-0142')],
 'SBF-003': [('16 Aug 2026','Cash',600,'INV-2608-0301'),('24 Jul 2026','Bank',3820,'INV-2607-0244')],
 'SBF-004': [('11 Sep 2026','bKash',16285,'INV-2609-0147'),('19 Aug 2026','Cash',18236,'INV-2608-0318'),('28 Jul 2026','bKash',8720,'INV-2607-0261')],
 'SBF-005': [('23 Sep 2026','Bank',12493,'INV-2609-0146'),('12 Aug 2026','bKash',1130,'INV-2608-0294'),('19 Jul 2026','Bank',15613,'INV-2607-0233')],
 'SBF-006': [('20 Jul 2026','Cash',15907,'INV-2607-0219')],
 'SBF-007': [('05 Aug 2026','Cash',6390,'INV-2608-0276')],
 'SBF-008': [('14 Jul 2026','Bank',11218,'INV-2607-0214'),('09 Jun 2026','Bank',5248,'INV-2606-0171')],
 'SBF-009': [('22 Jun 2026','Cash',1910,'INV-2606-0195')],
 'SBF-010': [('27 Jul 2026','Cash',2740,'INV-2607-0226')],
 'SBF-011': [('18 Sep 2026','bKash',24610,'INV-2609-0138'),('17 Aug 2026','bKash',5410,'INV-2608-0305')],
 'SBF-012': [('09 Aug 2026','Cash',16505,'INV-2608-0283'),('21 Jul 2026','Cash',8430,'INV-2607-0238')],
}

def as_dict():
    """Shape the rows the way the browser wants them.

    Two fields are derived here rather than stored in the table above:
      source  — Web orders came through WooCommerce, Manual ones were typed in.
                This is what proves the WebSync promise on the dashboard.
      pending — the five most recent orders network-wide are not yet delivered.
                Anything older is closed, which is how the real workflow behaves.
    """
    import datetime
    MON = {m: i for i, m in enumerate(
        'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(), 1)}

    def pd(x):
        d, m, y = x.split()
        return datetime.date(int(y), MON[m], int(d))

    flat = sorted(((pd(b), c, a) for c, rows in ORDERS.items() for a, b, *_ in rows),
                  reverse=True)
    pending = {inv for _, _, inv in flat[:5]}

    out = []
    for i, (c, n, ph, d, ar, t, since, o, sold, paid, last) in enumerate(CUSTOMERS, 1):
        orders = []
        for k, (a, b, cc, dd, ee, items) in enumerate(ORDERS.get(c, [])):
            orders.append({'inv': a, 'd': b, 'n': cc, 't': dd, 'p': ee,
                           'src': 'Web' if (i + k) % 3 == 0 else 'Manual',
                           'pending': a in pending,
                           'it': [{'k': x[0], 'q': x[1], 'r': x[2], 't': x[1] * x[2]}
                                  for x in items]})
        out.append({
          'code':c, 'name':n, 'phone':ph, 'district':d, 'area':ar, 'tier':t,
          'since':since, 'orders':o, 'sold':sold, 'paid':paid, 'due':sold-paid,
          'last':last, 'rank':i, 'o':orders,
          'p':[{'d':a,'m':b,'a':cc,'inv':dd} for a,b,cc,dd in PAYMENTS.get(c,[])],
        })
    return out
