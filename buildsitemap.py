#!/usr/bin/env python3
# Shada Bird Feed · HTML sitemap generator  ·  /html-sitemap/
# Every URL below was read out of the live wp-sitemap.xml and then checked
# individually for a 200. Nothing here is typed from memory.
# Re-verify with:  python3 buildsitemap.py --check
import re, os, sys, json, subprocess

HEAD = open('/tmp/pg/head.txt', encoding='utf-8').read()
FOOT = open('/tmp/pg/foot.txt', encoding='utf-8').read()
BASE = 'https://eleven.thewebduo.com'

I = lambda p, w=1.9: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
I_ARROW = I('<path d="M5 12h14M12 5l7 7-7 7"/>', 2.4)

# ── Groups. Order = how a visitor actually looks for things. ──────────
GROUPS = [
 ('Main pages', [
    ('/',                                                'Home'),
    ('/shop/',                                           'Shop'),
    ('/about/',                                          'About'),
    ('/wholesale/',                                      'Wholesale'),
    ('/dealers/',                                        'Dealers'),
    ('/contact/',                                        'Contact'),
    ('/blog/',                                           'Guides'),
 ]),
 ('Products', [
    ('/product/nutricare-hand-feeding/',                 'Nutricare Hand Feeding Formula'),
    ('/product/avian-eggfood/',                          'Avian Eggfood'),
    ('/product/avian-herbs/',                            'Avian Herbs'),
    ('/product/avian-spirulina/',                        'Avian Spirulina'),
    ('/product/moringa-leaf-powder/',                    'Avian Moringa Leaf Powder'),
    ('/product/beetroot-powder/',                        'Avian Beetroot Powder'),
 ]),
 ('Shop by need', [
    ('/product-category/hand-rearing/',                  'Hand rearing'),
    ('/product-category/breeding/',                      'Breeding'),
    ('/product-category/supplements/',                   'Supplements'),
 ]),
 ('Guides', [
    ('/how-to-hand-feed-a-lovebird-chick-day-one-to-weaning/','How to hand feed a lovebird chick, day one to weaning'),
    ('/spirulina-for-birds-how-much-how-often-and-when-to-stop/','Spirulina for birds: how much, how often, when to stop'),
    ('/bird-food-prices-in-bangladesh-2026/',            'Bird food prices in Bangladesh, 2026'),
 ]),
 ('Guide topics', [
    ('/category/hand-rearing/',                          'Hand rearing'),
    ('/category/supplements/',                           'Supplements'),
    ('/category/prices/',                                'Prices'),
 ]),
 ('Birds we formulate for', [
    ('/birds/lovebird/',                                 'Lovebird'),
    ('/birds/budgerigar/',                               'Budgerigar'),
    ('/birds/cockatiel/',                                'Cockatiel'),
    ('/birds/conure/',                                   'Conure'),
    ('/birds/ringneck/',                                 'Ringneck'),
    ('/birds/rosella/',                                  'Rosella'),
 ]),
 ('Your orders', [
    ('/cart/',                                           'Cart'),
    ('/checkout/',                                       'Checkout'),
    ('/my-account/',                                     'My account'),
 ]),
 ('The small print', [
    ('/privacy-policy/',                                 'Privacy policy'),
    ('/terms-and-conditions/',                           'Terms and conditions'),
    ('/refund_returns/',                                 'Refund and returns'),
 ]),
]

# Deliberately NOT listed:
#   /thank-you/          a form destination, no reason to browse to it
#   /home/               a duplicate of /, would split link equity
#   /coming-soon/        a leftover launch page
#   /dealers/<name>/     the 15 dealer entries — see README, 14 are samples
#   /districts/<name>/   thin taxonomy archives, better reached from /dealers/

CSS = '''
/* ═══════════════════════════════════════════════════════════════════
   HTML SITEMAP  ·  /html-sitemap/
   Loads after 01-base.css. One page, every real URL, grouped the way a
   visitor looks for things rather than the way WordPress stores them.
   ═══════════════════════════════════════════════════════════════════ */
.smhero{background:var(--ink);color:#fff;position:relative;overflow:hidden;
  padding:clamp(38px,5vw,66px) 0 clamp(34px,4.2vw,54px)}
.smhero::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;
  opacity:.07;pointer-events:none}
.smhero .wrap{position:relative}
.smhero h1{font-size:clamp(30px,4.4vw,52px);letter-spacing:-.035em;line-height:1.06;margin:10px 0 12px}
.smhero p{font-size:16.5px;line-height:1.6;color:var(--on2);max-width:56ch}

.smgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(18px,2.4vw,34px)}
@media(max-width:1000px){.smgrid{grid-template-columns:1fr 1fr}}
@media(max-width:680px){.smgrid{grid-template-columns:1fr}}

/* One line per page. No pack sizes, no descriptions, no counts — the same
   convention every competitor sitemap uses, and the only one that stays clean
   as the site grows. */
.smg{break-inside:avoid}
.smg h2{font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
  color:var(--brand);margin-bottom:12px}
.smg ul{list-style:none;border-top:1px solid var(--line)}
.smg li{border-bottom:1px solid var(--line)}
.smg a{display:flex;align-items:center;gap:12px;min-height:46px;padding:11px 2px;
  font-size:15.5px;line-height:1.4;color:var(--tx);text-decoration:none;
  transition:color .15s,padding .15s}
.smg a:hover{color:var(--brand);padding-left:6px}
.smg a > span{flex:1;min-width:0}
.smg .ch{flex:0 0 auto;width:15px;height:15px;color:var(--brand);opacity:0;
  transition:opacity .15s,transform .15s;transform:translateX(-4px)}
.smg a:hover .ch{opacity:1;transform:translateX(0)}

.smfoot{margin-top:clamp(36px,4.4vw,60px);padding-top:26px;border-top:1px solid var(--line);
  display:flex;gap:14px;flex-wrap:wrap;align-items:center;justify-content:space-between}
.smfoot p{font-size:14px;color:var(--tx2);line-height:1.6;max-width:62ch}
.smfoot a.link{white-space:nowrap}
'''


def build():
    CHEV = ('<svg class="ch" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6 6 6-6 6"/></svg>')
    total = sum(len(rows) for _, rows in GROUPS)

    groups = ''
    for name, rows in GROUPS:
        items = ''.join(f'<li><a href="{href}"><span>{label}</span>{CHEV}</a></li>'
                        for href, label in rows)
        groups += f'<div class="smg"><h2>{name}</h2><ul>{items}</ul></div>'

    body = f'''<main id="main">

<!-- ═══════════ HERO ═══════════ -->
<section class="smhero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb" style="color:var(--on2)"><a href="/" style="color:var(--on2)">Home</a><i></i><span style="color:#fff">Sitemap</span></nav>
    <span class="eyebrow" style="color:var(--leaf)">All pages</span>
    <h1>Every page on this site.</h1>
    <p>Grouped the way you would look for them. If you cannot find something here,
    message us on WhatsApp and we will send you the link.</p>
  </div>
</section>

<!-- ═══════════ THE MAP ═══════════ -->
<section>
  <div class="wrap">
    <div class="smgrid">{groups}</div>
    <div class="smfoot">
      <p>This page is for people. Search engines read the XML version at
      <a class="link" style="font-size:inherit" href="/wp-sitemap.xml">/wp-sitemap.xml</a>,
      which updates itself whenever a page is published.</p>
      <a class="btn b-brand" href="/contact/">Cannot find it? Ask us {I_ARROW}</a>
    </div>
  </div>
</section>

</main>
'''

    head = (HEAD
        .replace('<title>Shop · Shada Bird Feed</title>', '<title>Sitemap · Shada Bird Feed</title>')
        .replace('<link rel="canonical" href="https://shadabirdfeed.com/shop/">',
                 '<link rel="canonical" href="https://shadabirdfeed.com/html-sitemap/">'))
    head = re.sub(r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Every page on shadabirdfeed.com in one place: products, guides, dealers, ordering and policies."',
        head, count=1)
    return head.replace('</head>', f'<style>{CSS}</style>\n</head>') + body + FOOT


def check():
    """Hit every URL in GROUPS and report anything that is not 200."""
    bad = []
    n = 0
    for name, rows in GROUPS:
        for href, label in rows:
            n += 1
            code = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', BASE + href],
                                  capture_output=True, text=True).stdout
            if code != '200':
                bad.append((code, href, f'{name} → {label}'))
    print(f'checked {n} URLs')
    if bad:
        print('NOT 200:')
        for c, h, w in bad:
            print(f'  {c}  {h}   ({w})')
    else:
        print('all 200 ✓')
    return not bad


if __name__ == '__main__':
    if '--check' in sys.argv:
        sys.exit(0 if check() else 1)
    os.makedirs('/tmp/pg/out', exist_ok=True)
    open('/tmp/pg/out/html-sitemap.html', 'w', encoding='utf-8').write(build())
    print('html-sitemap.html', round(os.path.getsize('/tmp/pg/out/html-sitemap.html') / 1024), 'KB |',
          sum(len(r) for _, r in GROUPS), 'URLs in', len(GROUPS), 'groups')
