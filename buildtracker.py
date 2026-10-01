#!/usr/bin/env python3
"""Shada project tracker PDF — cluster by cluster, done vs not done.

Brand colours come from the same tokens as the website so the document reads as
Shada rather than as a generic report.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)
from reportlab.lib.enums import TA_LEFT
import datetime, os

INK   = colors.HexColor('#0A2617')
INK2  = colors.HexColor('#123222')
BRAND = colors.HexColor('#089830')
LEAF  = colors.HexColor('#5FD48A')
GOLD  = colors.HexColor('#B8871B')
RED   = colors.HexColor('#C0392B')
TX    = colors.HexColor('#1D1D1F')
TX2   = colors.HexColor('#6E6E73')
TX3   = colors.HexColor('#A1A1A6')
LINE  = colors.HexColor('#E3E3E0')
PAPER2= colors.HexColor('#F5F5F3')
SOFT  = colors.HexColor('#E6F4EA')

DATE = '24 September 2026'

def S(n, **k):
    base = dict(fontName='Helvetica', fontSize=9.5, leading=13.5,
                textColor=TX, alignment=TA_LEFT)
    base.update(k)
    return ParagraphStyle(n, **base)
st_h1   = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=26, leading=29,
                         textColor=colors.white, spaceAfter=0)
st_sub  = ParagraphStyle('sub', fontName='Helvetica', fontSize=10.5, leading=15,
                         textColor=colors.HexColor('#A1A1A6'))
st_h2   = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=14, leading=17,
                         textColor=INK, spaceBefore=0, spaceAfter=3)
st_eyeb = ParagraphStyle('eb', fontName='Helvetica-Bold', fontSize=7.5, leading=10,
                         textColor=BRAND, spaceAfter=2)
st_note = S('note', fontSize=9, leading=12.5, textColor=TX2)
st_cell = S('cell', fontSize=9, leading=12)
st_cellb= ParagraphStyle('cellb', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=TX)
st_small= S('small', fontSize=8, leading=11, textColor=TX2)

DONE, PART, TODO, BLOCK = 'DONE', 'PARTIAL', 'TO DO', 'BLOCKED'
BADGE = {DONE:(SOFT, BRAND), PART:(colors.HexColor('#FFF6D9'), GOLD),
         TODO:(PAPER2, TX2), BLOCK:(colors.HexColor('#FDECEA'), RED)}

# ── clusters ──────────────────────────────────────────────────────────────
CLUSTERS = [
 ('A', 'Foundation and design system',
  'The tokens, the shell, and the rules everything else is built on.',
  [('Design tokens, type scale, buttons, section skins', DONE, '01-base.css, live site-wide 21 Sep'),
   ('Tokens added to the Customizer site-wide', DONE, 'They existed nowhere before, pages used literal hex'),
   ('Wing and feather motifs', DONE, 'CSS masks in 01-base.css'),
   ('Header, mega menu, footer', DONE, 'Live site-wide'),
   ('Favicon set, 18 files', DONE, '01-HOME/assets/favicon'),
   ('Brand style guide', DONE, '01-HOME/BRAND-STYLE-GUIDE.html'),
   ('Class collision guard in every generator', DONE, 'Fails the build on a clash'),
   ('shada-website-ui-sop skill', DONE, 'Design system, survives into new chats'),
   ('shada-birds skill', DONE, 'Project context, requirements, blockers')]),

 ('B', 'Public website pages',
  'Everything a logged-out visitor can reach.',
  [('Home', DONE, 'Live'),
   ('Shop', DONE, 'Live'),
   ('Product categories, 3', DONE, 'hand-rearing, breeding, supplements'),
   ('Product pages, 6', DONE, 'All six formulas'),
   ('Blog index, 3 articles, article category', DONE, 'Live'),
   ('Contact', DONE, 'Live'),
   ('Thank you', DONE, 'Live at /thank-you/, redirect fixed'),
   ('Wholesale', DONE, 'Live, 20 to 42 percent margin figures'),
   ('Dealers', DONE, 'Live'),
   ('About', DONE, 'Live'),
   ('HTML sitemap', DONE, 'Live, 34 URLs'),
   ('404 template', DONE, 'Live'),
   ('FAQ page', TODO, 'Optional, not scoped')]),

 ('C', 'Species pages, the birds taxonomy',
  'One global archive template, six terms, dynamic product loop.',
  [('Taxonomy audited and understood', DONE, 'birds taxonomy on product, was empty'),
   ('All 6 products assigned to all 6 species', DONE, 'Via REST, 21 Sep'),
   ('Term descriptions written for all 6', DONE, 'Live'),
   ('Global archive template built', DONE, '00-TEMPLATE/birds-TEMPLATE.html'),
   ('6 species pages designed with assets', DONE, '06-BIRDS/01 to 06'),
   ('Content sheet for the 3 CMS fields', DONE, 'CONTENT-FOR-FIELDS.md'),
   ('Keyword map, no cannibalisation', DONE, 'KEYWORD-MAP file'),
   ('Rosella weaning age', BLOCK, 'No published figure. Ask the client or noindex.'),
   ('Build the template in Elementor Theme Builder', TODO, 'Ayaan'),
   ('Create the 3 JetEngine repeater fields', TODO, 'bg_facts, bg_stages, bg_faq'),
   ('Fill the fields for 6 terms', TODO, 'Content is written, paste only')]),

 ('D', 'WooCommerce and the account area',
  'Cart through to re-order, styled not rebuilt.',
  [('shada-woo.css written, 221 rules', DONE, '05-WOOCOMMERCE'),
   ('Deployed to the Customizer', DONE, '21 Sep, 18,250 to 53,664 chars'),
   ('Cart', DONE, 'Sticky totals, stacked cards under 700px'),
   ('Checkout', DONE, 'Sticky order review'),
   ('Order received', DONE, 'Styled'),
   ('My account, left rail dashboard', DONE, 'Dark rail, scroller on mobile'),
   ('Orders table and re-order', DONE, 'Re-order is the green action'),
   ('Dealer portal CSS layer', PART, 'Written and live, dormant until the body class is added'),
   ('Dealer body-class filter', TODO, 'One filter in functions.php or WPCode'),
   ('Role-based retail vs dealer pricing', TODO, 'Custom build, not a plugin')]),

 ('E', 'Policies and legal',
  'Written against Bangladeshi law as it stands in 2026.',
  [('Privacy policy, PDPA 2026 aligned', PART, 'Live with 9 CONFIRM markers'),
   ('Terms and conditions', PART, 'Live with 4 CONFIRM markers'),
   ('Refund and returns', PART, 'Live at /refund-returns/, 7 markers'),
   ('Shipping policy', PART, 'Live with 5 markers'),
   ('25 client decisions', BLOCK, '00-DECISIONS-FOR-THE-CLIENT.md, 5 block publication'),
   ('Lawyer review of final text', TODO, 'Before production launch')]),

 ('F', 'Live site fixes',
  'Things found by auditing the running site.',
  [('14 invented dealers unpublished', DONE, 'Set to draft 21 Sep, reversible'),
   ('Thank you page URL fixed', DONE, 'Now /thank-you/ directly'),
   ('Six thin /birds/ pages fixed', DONE, '10 words to 270 plus a product grid'),
   ('Policy shell links corrected', DONE, 'refund-returns, privacy-policy, terms'),
   ('Three Wholesale links point at /dealers/', TODO, 'Elementor header and footer template'),
   ('Homepage link audit, 20 links', DONE, 'Zero broken')]),

 ('G', 'Business Management System',
  'The real project. WordPress plus a custom plugin on dedicated MySQL tables.',
  [('Technical blueprint', DONE, 'Client file, 26 KB'),
   ('Feasibility matrix, all 3 stages', DONE, '12 standard, 47 custom, 0 impossible'),
   ('94-task build plan, 516 hours', DONE, 'Client file'),
   ('shada-bms plugin bootstrap', PART, 'Written, parked mid-build'),
   ('Core: DB, migrations, module registry', TODO, 'Phase 1'),
   ('20 dedicated MySQL tables', TODO, 'Phase 1'),
   ('WebSync bridge, web order to shada_orders', TODO, 'The Stage 3 requirement'),
   ('Stage 1: dashboard, customers, sales, inventory, accounts', TODO, 'Phases 2 to 6'),
   ('Stage 2: BI, follow-ups, KPI, search, export', TODO, 'Phase 7'),
   ('Stage 3: customer site and online ordering', PART, 'The website half is largely done'),
   ('Clickable prototype for client sign-off', TODO, 'Phase D, before any feature code')]),

 ('H', 'Data blockers with the client',
  'Unanswered questions that corrupt reports later if left open.',
  [('Wholesale weight rule is self-contradictory', BLOCK, 'Need 3 bands: 0-5, 5-10, 10kg+'),
   ('District list has 63, not 64', BLOCK, 'Bandarban is missing'),
   ('District spelling conflicts', BLOCK, 'Bogra/Bogura, Jessore/Jashore, Comilla/Cumilla'),
   ('No customer mobile numbers in the sheet', BLOCK, 'Column exists, all empty'),
   ('Rosella weaning age', BLOCK, 'Not in the literature'),
   ('25 policy decisions', BLOCK, 'See cluster E')]),

 ('I', 'Launch readiness',
  'What stands between staging and shadabirdfeed.com.',
  [('Move off staging to the real domain', TODO, 'Nothing ranks on eleven.thewebduo.com'),
   ('Submit the XML sitemap', TODO, 'After the domain move'),
   ('Analytics and consent banner named in the privacy policy', BLOCK, 'One of the 25 decisions'),
   ('Payment methods confirmed', BLOCK, 'Blocks Terms and Refund pages'),
   ('Delivery charge confirmed', BLOCK, 'Blocks the Shipping policy'),
   ('Load test and UAT', TODO, 'Phase 9')]),
]


def header(c, doc):
    c.saveState()
    w, h = A4
    c.setFillColor(INK); c.rect(0, h-26*mm, w, 26*mm, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont('Helvetica-Bold', 11)
    c.drawString(18*mm, h-14*mm, 'SHADA BIRD FEED')
    c.setFillColor(LEAF); c.setFont('Helvetica', 8.5)
    c.drawString(18*mm, h-19.5*mm, 'Project tracker, cluster by cluster')
    c.setFillColor(colors.HexColor('#A1A1A6')); c.setFont('Helvetica', 8)
    c.drawRightString(w-18*mm, h-14*mm, DATE)
    c.drawRightString(w-18*mm, h-19.5*mm, 'eleven.thewebduo.com')
    c.setFillColor(TX3); c.setFont('Helvetica', 7.5)
    c.drawString(18*mm, 12*mm, 'Shada Bird Feed  ·  prepared by Ayaan Ahmed Shohan')
    c.drawRightString(w-18*mm, 12*mm, f'Page {doc.page}')
    c.setStrokeColor(LINE); c.setLineWidth(.5)
    c.line(18*mm, 16*mm, w-18*mm, 16*mm)
    c.restoreState()


def badge(status):
    bg, fg = BADGE[status]
    t = Table([[Paragraph(f'<font size=7.5 color="#{fg.hexval()[2:]}"><b>{status}</b></font>',
                          S('b', fontSize=7.5, leading=9))]],
              colWidths=[20*mm], rowHeights=[6.2*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),
                           ('BOX',(0,0),(-1,-1),.6,fg),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('LEFTPADDING',(0,0),(-1,-1),5),
                           ('TOPPADDING',(0,0),(-1,-1),0),
                           ('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    return t


def cluster_block(letter, title, blurb, rows):
    tally = {}
    for _, s, _ in rows:
        tally[s] = tally.get(s, 0) + 1
    counts = '   '.join(f'{v} {k.lower()}' for k, v in
                        sorted(tally.items(), key=lambda x: ['DONE','PARTIAL','TO DO','BLOCKED'].index(x[0])))

    head = Table([[Paragraph(f'<b>{letter}</b>', ParagraphStyle('L', fontName='Helvetica-Bold',
                     fontSize=15, leading=17, textColor=colors.white)),
                   Paragraph(f'{title}<br/><font size=8.5 color="#6E6E73">{blurb}</font>', st_h2),
                   Paragraph(f'<font size=8 color="#6E6E73">{counts}</font>', st_small)]],
                 colWidths=[11*mm, 118*mm, 45*mm])
    head.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0),BRAND),
        ('ALIGN',(0,0),(0,0),'CENTER'), ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(1,0),(1,0),8), ('RIGHTPADDING',(2,0),(2,0),2),
        ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LINEBELOW',(0,0),(-1,-1),1.1,INK),
    ]))

    data = []
    for task, status, note in rows:
        data.append([Paragraph(task, st_cellb), badge(status), Paragraph(note, st_small)])
    body = Table(data, colWidths=[78*mm, 22*mm, 74*mm])
    style = [('VALIGN',(0,0),(-1,-1),'MIDDLE'),
             ('LEFTPADDING',(0,0),(0,-1),2), ('LEFTPADDING',(1,0),(1,-1),0),
             ('RIGHTPADDING',(0,0),(-1,-1),6),
             ('TOPPADDING',(0,0),(-1,-1),4.5), ('BOTTOMPADDING',(0,0),(-1,-1),4.5),
             ('LINEBELOW',(0,0),(-1,-2),.4,LINE)]
    for i,(_,s,_) in enumerate(rows):
        if s == BLOCK:  style.append(('BACKGROUND',(0,i),(-1,i),colors.HexColor('#FEF7F6')))
        elif s == DONE: style.append(('TEXTCOLOR',(0,i),(0,i),TX2))
    body.setStyle(TableStyle(style))
    return [head, Spacer(1, 2), body, Spacer(1, 9)]


def build(path):
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=18*mm, rightMargin=18*mm,
                            topMargin=32*mm, bottomMargin=20*mm,
                            title='Shada Bird Feed — project tracker',
                            author='Ayaan Ahmed Shohan')
    story = []

    # ── summary ──
    tot = {DONE:0, PART:0, TODO:0, BLOCK:0}
    for _,_,_,rows in CLUSTERS:
        for _,s,_ in rows: tot[s]+=1
    n = sum(tot.values())
    pct = round(tot[DONE]/n*100)

    story.append(Paragraph('WHERE THE PROJECT STANDS', st_eyeb))
    story.append(Paragraph(f'{tot[DONE]} of {n} tasks complete', ParagraphStyle(
        'big', fontName='Helvetica-Bold', fontSize=21, leading=24, textColor=INK, spaceAfter=4)))
    story.append(Paragraph(
        f'Across 9 clusters. {pct} percent done. The website design work is finished; what remains '
        f'is client answers, the CMS build, and the Business Management System.', st_note))
    story.append(Spacer(1, 8))

    cells = []
    for s in [DONE, PART, TODO, BLOCK]:
        bg, fg = BADGE[s]
        cells.append(Table([[Paragraph(f'<font size=17 color="#{fg.hexval()[2:]}"><b>{tot[s]}</b></font>',
                                       S('x', fontSize=17, leading=20))],
                            [Paragraph(f'<font size=7.5 color="#6E6E73">{s}</font>', st_small)]],
                           colWidths=[41*mm], rowHeights=[9*mm, 5*mm],
                           style=TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),
                                             ('BOX',(0,0),(-1,-1),.6,fg),
                                             ('LEFTPADDING',(0,0),(-1,-1),8),
                                             ('TOPPADDING',(0,0),(-1,-1),1),
                                             ('BOTTOMPADDING',(0,0),(-1,-1),0),
                                             ('VALIGN',(0,0),(-1,-1),'MIDDLE')])))
    row = Table([cells], colWidths=[43*mm]*4)
    row.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),2),
                             ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    story += [row, Spacer(1, 12)]

    story.append(Paragraph(
        '<b>The four things that block everything else.</b>  1. The 25 policy decisions. '
        '2. The wholesale weight rule. 3. The district list, 63 not 64, and the spelling conflicts. '
        '4. Moving off the staging domain. Nothing ranks on eleven.thewebduo.com.', st_note))
    story.append(Spacer(1, 14))

    for letter, title, blurb, rows in CLUSTERS:
        blk = cluster_block(letter, title, blurb, rows)
        # keep the cluster header with its first rows, then let the table flow
        story.append(KeepTogether(blk[:2] + [Spacer(1, 1)]))
        story.extend(blk[2:])

    story.append(PageBreak())
    story.append(Paragraph('WHAT TO DO NEXT', st_eyeb))
    story.append(Paragraph('In priority order', ParagraphStyle(
        'nx', fontName='Helvetica-Bold', fontSize=17, leading=20, textColor=INK, spaceAfter=8)))
    nxt = [
      ('1', 'Send the client the 25 policy decisions and the 4 data blockers',
       'One WhatsApp message. It unblocks 4 live pages and the whole BMS data model. '
       'Five of the 25 block publication outright: legal name and trade licence, payment methods, '
       'delivery charge, return window, and which analytics tools are installed.'),
      ('2', 'Fix the 3 Wholesale links in the Elementor header and footer template',
       'They point at /dealers/ on every page. Sixty seconds in Theme Builder. Not automated on '
       'purpose: editing _elementor_data by API risks the live template.'),
      ('3', 'Build the birds archive template and the 3 repeater fields',
       'One template, six terms. All the content is written in CONTENT-FOR-FIELDS.md. '
       'Set rosella to noindex until its weaning age arrives.'),
      ('4', 'Add the dealer body-class filter',
       'One filter. It activates the dealer portal CSS that is already live.'),
      ('5', 'Move to shadabirdfeed.com and submit the sitemap',
       'No amount of on-page work compensates for a staging domain.'),
      ('6', 'Build the shada-bms plugin core and the WebSync bridge',
       'The hook on woocommerce_checkout_order_processed is what makes the client\'s '
       '"one database, no second entry" requirement literally true.'),
    ]
    data=[]
    for num, t, d in nxt:
        data.append([Paragraph(f'<font color="#089830"><b>{num}</b></font>',
                     ParagraphStyle('n', fontName='Helvetica-Bold', fontSize=13, leading=15)),
                     Paragraph(f'<b>{t}</b><br/><font size=8.5 color="#6E6E73">{d}</font>', st_cell)])
    t = Table(data, colWidths=[9*mm, 165*mm])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                           ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                           ('LEFTPADDING',(0,0),(-1,-1),2),
                           ('LINEBELOW',(0,0),(-1,-2),.4,LINE)]))
    story.append(t)
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        '<font size=8 color="#A1A1A6">Every status in this document was checked against the live '
        'site or the project folder on 24 September 2026. Nothing is assumed.</font>', st_small))

    doc.build(story, onFirstPage=header, onLaterPages=header)
    return path


if __name__ == '__main__':
    out = '/sessions/pensive-affectionate-einstein/mnt/outputs/Shada-Project-Tracker.pdf'
    build(out)
    print(out, round(os.path.getsize(out)/1024), 'KB')
