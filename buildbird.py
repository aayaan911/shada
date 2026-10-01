#!/usr/bin/env python3
# Shada Bird Feed · species page generator  ·  /birds/<species>/
#
# These URLs are a PRODUCT TAXONOMY archive, not a page. The existing Elementor
# archive template already renders: breadcrumb, term name as H1, term description,
# then the product loop. This generator produces the sections that go ABOVE and
# BELOW that loop, so the loop keeps working and nothing dynamic is hand-built.
#
# Research note: none of Vetafarm, Nekton or Versele-Laga publishes a per-species
# landing page. They stop at animal type. So there is no competitor pattern to copy
# here, and no competitor to outrank either. Designed from search intent instead.
import re, os, sys, json

HEAD = open('/tmp/pg/head.txt', encoding='utf-8').read()
FOOT = open('/tmp/pg/foot.txt', encoding='utf-8').read()

WA   = '8801813323535'
PH   = '01813-323535'

I = lambda p, w=1.9: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
I_WA    = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd">'
           '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.9a8.1 8.1 0 0 1 6.6 12.8l-.3.4.7 2.5-2.6-.7-.4.2A8.1 8.1 0 1 1 12 3.9Z"/>'
           '<path d="M9.1 7.2h.6c.2 0 .5-.1.7.5l.9 2.2c.1.1.1.3 0 .5l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.4 2.4 1.5.3.1.4.1.6-.1.1-.2.7-.9.9-1.2.2-.2.4-.2.7-.1.2.1 1.7.9 2 1 .3.1.5.2.6.4 0 .1 0 .7-.2 1.4-.2.7-1.5 1.3-2 1.4-.6.1-1.1.3-3.6-.7-3-1.3-5-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.7-2.2 1-2.5c.3-.3.6-.4.8-.4Z"/></svg>')
I_ARROW = I('<path d="M5 12h14M12 5l7 7-7 7"/>', 2.4)
I_THERM = I('<path d="M14 14.8V4a2 2 0 1 0-4 0v10.8a4 4 0 1 0 4 0z"/>')
I_CLOCK = I('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
I_SCALE = I('<path d="M12 3v18M7 7h10"/><path d="M4 12a3 3 0 0 0 6 0L7 6z"/><path d="M14 12a3 3 0 0 0 6 0l-3-6z"/>')
I_ALERT = I('<path d="M12 8v5"/><circle cx="12" cy="16.5" r=".6" fill="currentColor"/><path d="M10.3 3.9 2.6 17.4A2 2 0 0 0 4.3 20.4h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>')

IMG = 'https://eleven.thewebduo.com/wp-content/uploads/2026/08/'

# ═════════════════════════════════════════════════════════════════════════
#  THE CATALOGUE
#  Six products, in the order a breeder needs them. Prices are the verified
#  retail floor from the client's price list. Image URLs were read off the
#  live site, not guessed. Accent colours are the --p1..--p6 product tokens.
#  The 'why' line is written per species below, which is what stops six
#  species pages being six duplicates of the shop.
# ═════════════════════════════════════════════════════════════════════════
CATALOGUE = [
  ('nutricare-hand-feeding', 'Nutricare Hand Feeding Formula', 'Hand rearing',
   'shada-nutricare-hand-feeding-formula.png', ['100g','200g','500g','1kg'], 130, '100g', 'var(--p1)'),
  ('avian-eggfood', 'Avian Eggfood', 'Breeding',
   'shada-avian-eggfood.png', ['100g','200g','500g','1kg'], 110, '100g', 'var(--p4)'),
  ('avian-herbs', 'Avian Herbs', 'Supplements',
   'shada-avian-herbs-200g.png', ['50g','100g','200g'], 220, '50g', 'var(--p3)'),
  ('avian-spirulina', 'Avian Spirulina', 'Supplements',
   'shada-avian-spirulina-200g.png', ['50g','100g','200g'], 350, '50g', 'var(--p5)'),
  ('moringa-leaf-powder', 'Avian Moringa Leaf Powder', 'Supplements',
   'shada-avian-moringa-leaf-powder-200g.png', ['50g','100g','200g'], 125, '50g', 'var(--p2)'),
  ('beetroot-powder', 'Avian Beetroot Powder', 'Supplements',
   'shada-avian-beetroot-powder-200g.png', ['50g','100g','200g'], 125, '50g', 'var(--p6)'),
]

# ═════════════════════════════════════════════════════════════════════════
#  THE THREE MISTAKES — identical on all six species pages.
#  Static in the template on purpose: making these fields would be 18 fields
#  of duplicated typing per species for zero gain. Any species-specific number
#  belongs in bg_facts or bg_stages, never here.
# ═════════════════════════════════════════════════════════════════════════
MISTAKES = [
  (I_THERM, 'Formula fed too cool',
   'Cold formula slows the crop, and a crop that stops emptying is how a chick is lost. '
   'Measure the temperature at every single feed. Use the figure for your species, not a guess.'),
  (I_CLOCK, 'Feeding on the clock, not on the crop',
   'The schedule is a guide. The crop emptying is the instruction. A full crop at feeding time '
   'is a reason to stop and check, not a reason to top it up.'),
  (I_SCALE, 'Switching formula mid-clutch',
   'Chicks handle one formula consistently far better than two good ones alternated. Pick a '
   'brand and finish the clutch on it. That is why every Shada jar carries its batch date.'),
]

# ═════════════════════════════════════════════════════════════════════════
#  SPECIES DATA lives in species_data.py so the content is editable without
#  touching the builder. Shared strings are constants there, only the deltas
#  are per species, which mirrors the three CMS repeater fields exactly.
# ═════════════════════════════════════════════════════════════════════════
from species_data import SPECIES, SOURCES

CSS = '''
/* ═══════════════════════════════════════════════════════════════════════════
   SPECIES PAGE  ·  /birds/<species>/
   Sections that wrap the existing product loop on the birds taxonomy archive.
   Loads after 01-base.css. Homepage classes only, plus a .bg* block.

   The bg- prefix is deliberate. The first draft used .sp*, which collided with
   .spm in 02-shop-pages.css (the product-card meta row, display:flex) and broke
   every card on the page. assert_no_collisions() below now blocks that at build
   time instead of leaving it to be spotted in a screenshot.
   ═══════════════════════════════════════════════════════════════════════════ */

/* ── Hero ────────────────────────────────────────────────────────────── */
.bghero{background:var(--ink);color:#fff;position:relative;overflow:hidden;
  padding:clamp(38px,5vw,70px) 0 clamp(34px,4.4vw,58px)}
.bghero::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;
  opacity:.07;pointer-events:none}
.bghero .wrap{position:relative}
.bghero h1{font-size:clamp(34px,5vw,62px);letter-spacing:-.037em;line-height:1.04;margin:10px 0 14px}
.bghero .lede{font-size:17.5px;line-height:1.6;color:var(--on2);max-width:58ch}
.bghero .acts{display:flex;gap:11px;flex-wrap:wrap;margin-top:28px}
.bgfacts{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-top:34px}
@media(max-width:760px){.bgfacts{grid-template-columns:1fr}}
.bgfact{background:var(--ink2);border:1px solid var(--line-d);border-radius:var(--r2);padding:18px 20px}
.bgfact b{display:block;font-size:clamp(22px,2.6vw,30px);letter-spacing:-.035em;line-height:1}
.bgfact span{display:block;font-size:13px;color:var(--on2);margin-top:7px;line-height:1.45}

/* ── The feeding calendar. The reason this page exists. ──────────────── */
.bgstages{display:grid;gap:0;border-top:1px solid var(--line)}
.bgstage{display:grid;grid-template-columns:150px 1fr 1.15fr;gap:clamp(16px,2.4vw,36px);
  padding:clamp(22px,2.6vw,32px) 0;border-bottom:1px solid var(--line);align-items:start}
@media(max-width:860px){.bgstage{grid-template-columns:1fr;gap:10px}}
.bgstage .age{font-size:12.5px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;
  color:var(--brand);padding-top:4px}
.bgstage h3{font-size:clamp(19px,2vw,23px);letter-spacing:-.022em;line-height:1.25;margin-bottom:8px}
.bgstage .feed{font-size:15.5px;line-height:1.5;color:var(--tx);font-weight:600}
.bgstage p{font-size:15.5px;line-height:1.62;color:var(--tx2)}

/* ── Where the product loop goes ─────────────────────────────────────── */
.bgloop{border:2px dashed var(--brand);border-radius:var(--r3);background:var(--brand-soft);
  padding:clamp(24px,3vw,40px);text-align:center}
.bgloop b{display:block;font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
  color:var(--brand-d);margin-bottom:8px}
.bgloop p{font-size:15.5px;line-height:1.6;color:var(--tx2);max-width:60ch;margin:0 auto}

/* ── Mistakes, on dark ───────────────────────────────────────────────── */
.bgmiss{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:860px){.bgmiss{grid-template-columns:1fr}}
.bgm{background:var(--ink2);border:1px solid var(--line-d);border-radius:var(--r3);padding:26px 28px}
.bgm .ic{width:42px;height:42px;border-radius:11px;display:grid;place-items:center;margin-bottom:16px;
  background:rgba(95,212,138,.13);border:1px solid rgba(95,212,138,.28)}
.bgm .ic svg{width:20px;height:20px;color:var(--leaf)}
.bgm h3{font-size:18.5px;letter-spacing:-.02em;margin-bottom:8px;line-height:1.3;color:#fff}
.bgm p{font-size:15px;line-height:1.6;color:var(--on2)}

/* ── FAQ ─────────────────────────────────────────────────────────────── */
.bgfaq{max-width:860px;border-top:1px solid var(--line)}
.bgq{border-bottom:1px solid var(--line)}
.bgq summary{display:flex;align-items:flex-start;gap:14px;justify-content:space-between;
  padding:20px 0;cursor:pointer;list-style:none;font-size:clamp(17px,1.8vw,19.5px);
  font-weight:600;letter-spacing:-.018em;line-height:1.35;color:var(--tx)}
.bgq summary::-webkit-details-marker{display:none}
.bgq summary:hover{color:var(--brand)}
.bgq .pm{flex:0 0 auto;width:26px;height:26px;border-radius:50%;border:1px solid var(--line);
  display:grid;place-items:center;margin-top:1px;transition:transform .2s var(--ease),
  background .2s,border-color .2s}
/* Both bars must share ONE grid cell. Without grid-area they flow into two rows
   and the plus renders as a vertical bar. */
.bgq .pm::before,.bgq .pm::after{content:"";grid-area:1/1;background:var(--tx2);
  border-radius:1px;transition:opacity .2s,background .2s}
.bgq .pm::before{width:11px;height:1.6px}
.bgq .pm::after{width:1.6px;height:11px}
.bgq[open] .pm{background:var(--brand);border-color:var(--brand);transform:rotate(180deg)}
.bgq[open] .pm::before,.bgq[open] .pm::after{background:#fff}
.bgq[open] .pm::after{opacity:0}
.bgq .a{padding:0 44px 22px 0;font-size:16px;line-height:1.68;color:var(--tx2);max-width:74ch}

/* ── The honesty line ────────────────────────────────────────────────── */
.bgnote{margin-top:26px;padding:18px 22px;background:var(--paper2);border:1px solid var(--line);
  border-left:3px solid var(--tx3);border-radius:var(--r2);font-size:14.5px;line-height:1.6;
  color:var(--tx2);max-width:74ch}
.bgnote b{color:var(--tx)}
'''


def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def assert_no_collisions():
    """Every class this file defines must be unused by the site's existing CSS.

    A collision does not error, it silently restyles the page — which is the
    worst kind of bug because it looks like a design mistake. Fail the build.
    """
    mine = sorted(set(re.findall(r'\.(bg[a-z0-9]+)\b', CSS)))
    clashes = [c for c in mine if re.search(r'[.\s]' + c + r'\b[^{}]{0,150}\{', HEAD)]
    if clashes:
        raise SystemExit(
            'CLASS COLLISION with the site stylesheet: ' + ', '.join(clashes) +
            '\nRename them before building. Nothing was written.'
        )
    return mine


def build(key, template=False):
    """template=True emits the ONE global archive template.

    Dynamic slots are marked with {{ }} so it is obvious in Elementor what is a
    dynamic tag and what is fixed. Sections 4 and 5 are deliberately static: the
    three mistakes and the breeding-season copy are true for every species, so
    making them fields would be 20 fields of duplicated typing for no gain.
    """
    s = SPECIES[key]
    T = template
    def dyn(marker, fallback):
        return marker if T else fallback

    facts = (
      '<!-- REPEATER: bg_facts (3 rows) -->\n'
      '<div class="bgfact"><b>{{ bg_facts.value }}</b><span>{{ bg_facts.label }}</span></div>'
      if T else
      ''.join(f'<div class="bgfact"><b>{v}</b><span>{l}</span></div>' for v, l in s['facts']))

    stages = (
      '<!-- REPEATER: bg_stages (4 rows) -->\n'
      '<div class="bgstage"><div class="age">{{ bg_stages.age }}</div>'
      '<div><h3>{{ bg_stages.title }}</h3><p class="feed">{{ bg_stages.feed }}</p></div>'
      '<p>{{ bg_stages.note }}</p></div>'
      if T else
      ''.join(
        f'<div class="bgstage"><div class="age">{age}</div>'
        f'<div><h3>{title}</h3><p class="feed">{feed}</p></div>'
        f'<p>{note}</p></div>'
        for title, age, feed, note in s['stages']))

    mistakes = ''.join(
        f'<div class="bgm"><span class="ic">{icon}</span><h3>{t}</h3><p>{p}</p></div>'
        for icon, t, p in MISTAKES)

    faq = (
      '<!-- REPEATER: bg_faq (4 to 6 rows) -->\n'
      '<details class="bgq"><summary>{{ bg_faq.q }}<span class="pm"></span></summary>'
      '<div class="a">{{ bg_faq.a }}</div></details>'
      if T else
      ''.join(
        f'<details class="bgq"><summary>{q}<span class="pm"></span></summary>'
        f'<div class="a">{a}</div></details>'
        for q, a in s['faq']))

    # ── The product grid ─────────────────────────────────────────────────
    # Reuses the site's own .sgrid / .sp / .spa / .spb / .spm card, already
    # defined in 02-shop-pages.css. No new card CSS, and it matches the shop
    # exactly. Images point at the live uploads, never inlined as base64.
    GO = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M4 12h16M14 6l6 6-6 6"/></svg>')
    cards = ''
    _skip_cards = T
    if T:
        cards = ('<!-- ══ DYNAMIC PRODUCT LOOP ══\n'
                 '     Elementor / JetWooBuilder "Products" or "Listing Grid" widget.\n'
                 '     Source: current taxonomy archive query. 3 columns desktop, 2 tablet, 1 mobile.\n'
                 '     Whatever products carry this bird term appear here. Nothing to edit per species. -->\n'
                 '<div class="sgrid" data-loop="archive-products"></div>')
    for slug, title, cat, img, sizes, price, floor, accent in ([] if T else CATALOGUE):
        why = s['why'][slug]
        chips = ''.join(f'<span>{z}</span>' for z in sizes)
        cards += (
            f'<a class="sp" href="/product/{slug}/" style="--ac:{accent}">'
            f'<div class="spa"><span class="cat">{cat}</span>'
            f'<img src="{IMG}{img}" alt="{title}" loading="lazy" width="600" height="600"></div>'
            f'<div class="spb"><h3>{title}</h3><p>{why}</p>'
            f'<div class="sizes">{chips}</div>'
            f'<div class="spm"><span class="price">from <b>৳{price}</b><small>{floor}</small></span>'
            f'<span class="go">{GO}</span></div></div></a>'
        )
    if not T:
        cards = '<div class="sgrid">' + cards + '</div>'

    bt, bsub, bbody = s['breeding']
    h1      = dyn('{{ term.name }} feeding.', s['h1'])
    lede    = dyn('{{ term.description }}', s['lede'])
    species = dyn('{{ term.name }}', s['name'])
    lower   = dyn('{{ term.name }}', s['name'].lower())

    body = f'''<main id="main">

<!-- ═══════════ 1 · HERO  (replaces the plain archive header) ═══════════ -->
<section class="bghero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb" style="color:var(--on2)"><a href="/" style="color:var(--on2)">Home</a><i></i><a href="/shop/" style="color:var(--on2)">Birds</a><i></i><span style="color:#fff">{species}</span></nav>
    <span class="eyebrow" style="color:var(--leaf)">Bird guide</span>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="acts">
      <a class="btn b-brand" href="#feed">The feeding plan {I_ARROW}</a>
      <a class="btn b-white" href="https://wa.me/{WA}?text={species}%20feeding%20question" target="_blank" rel="noopener">{I_WA} Ask a breeder</a>
    </div>
    <div class="bgfacts">{facts}</div>
  </div>
</section>

<!-- ═══════════ 2 · THE PRODUCTS  ═══════════
     Products come before the guide content. This is a product category page:
     a visitor arriving on "lovebird food" wants to see the range, not read first.
     When building in Elementor, either paste these cards or drop the archive
     product loop widget here. The cards below use the site's own shop classes. -->
<section id="range">
  <div class="wrap">
    <div class="bhead" style="display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:clamp(22px,2.6vw,32px)">
      <div>
        <span class="eyebrow">The range</span>
        <h2 class="h-l" style="font-size:clamp(28px,3.4vw,44px)">Feed for {lower}s.</h2>
      </div>
      <span style="font-size:13.5px;color:var(--tx2)">{len(CATALOGUE)} products &middot; every pack size</span>
    </div>
    {cards}
    <p style="margin-top:26px;font-size:14.5px;color:var(--tx2);line-height:1.6">
      One retail price, the same in all 64 districts.
      <a class="link" style="font-size:inherit" href="/wholesale/">Dealer pricing</a> is for shops buying to resell.
    </p>
  </div>
</section>

<!-- ═══════════ 3 · THE FEEDING CALENDAR ═══════════ -->
<section class="tint" id="feed">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Stage by stage</span>
      <h2 class="h-l">What to feed, and when.</h2>
    </div>
    <div class="bgstages">{stages}</div>
    <div class="bgnote"><b>This is general guidance, not veterinary advice.</b> It follows published
    aviculture practice and our own experience in Bhaluka. A chick that is not gaining weight, or a
    bird that is unwell, needs an avian vet, not a change of feed.</div>
  </div>
</section>

<!-- ═══════════ 4 · WHAT GOES WRONG ═══════════ -->
<section class="dark wing">
  <div class="wrap" style="position:relative;z-index:1">
    <div class="head">
      <span class="eyebrow" style="color:var(--leaf)">Before you lose a clutch</span>
      <h2 class="h-l" style="color:#fff">Three things that go wrong.</h2>
    </div>
    <div class="bgmiss">{mistakes}</div>
  </div>
</section>

<!-- ═══════════ 5 · BREEDING SEASON ═══════════ -->
<section class="brand wing">
  <div class="wrap" style="position:relative;z-index:1">
    <div class="head" style="margin-bottom:clamp(18px,2vw,26px)">
      <span class="eyebrow" style="color:#DFF7E6">{bt}</span>
      <h2 class="h-l" style="color:#fff">{bsub}</h2>
    </div>
    <p style="font-size:clamp(17px,1.9vw,21px);line-height:1.55;color:rgba(255,255,255,.92);max-width:62ch">{bbody}</p>
    <div style="display:flex;gap:11px;flex-wrap:wrap;margin-top:28px">
      <a class="btn b-white" href="/product/avian-eggfood/">See Avian Eggfood {I_ARROW}</a>
      <a class="btn b-line" href="/blog/">Read the guides</a>
    </div>
  </div>
</section>

<!-- ═══════════ 6 · FAQ ═══════════ -->
<section class="tint">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Questions</span>
      <h2 class="h-l">{species} feeding, answered.</h2>
    </div>
    <div class="bgfaq">{faq}</div>
  </div>
</section>

<!-- ═══════════ 7 · FINAL CTA ═══════════ -->
<section class="final ctr">
  <div class="wrap">
    <h2 class="h-l">Start with one jar.</h2>
    <p class="sub">Sealed in Bhaluka, batch date on the lid. Two working days to most districts.</p>
    <div style="display:flex;gap:11px;flex-wrap:wrap;justify-content:center;margin-top:30px">
      <a class="btn b-brand b-lg" href="/shop/">Shop the range {I_ARROW}</a>
      <a class="btn b-line b-lg" href="https://wa.me/{WA}" target="_blank" rel="noopener">{I_WA} Order on WhatsApp</a>
    </div>
  </div>
</section>

</main>
'''

    # Two schemas: the FAQ for rich results, and an ItemList so Google reads this
    # as a product category page rather than an article.
    base = 'https://shadabirdfeed.com'
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}}
            for q, a in s['faq']
        ],
    }
    list_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"Feed for {s['name'].lower()}s",
        "numberOfItems": len(CATALOGUE),
        "itemListElement": [
            {"@type": "ListItem", "position": i,
             "item": {"@type": "Product", "name": title,
                      "url": f"{base}/product/{slug}/",
                      "image": IMG + img,
                      "brand": {"@type": "Brand", "name": "Shada Bird Feed"},
                      "offers": {"@type": "AggregateOffer", "priceCurrency": "BDT",
                                 "lowPrice": price, "availability": "https://schema.org/InStock"}}}
            for i, (slug, title, cat, img, sizes, price, floor, accent) in enumerate(CATALOGUE, 1)
        ],
    }
    ldjson = ('<script type="application/ld+json">' + json.dumps(faq_ld, ensure_ascii=False) + '</script>\n'
              '<script type="application/ld+json">' + json.dumps(list_ld, ensure_ascii=False) + '</script>')

    head = (HEAD
        .replace('<title>Shop · Shada Bird Feed</title>',
                 f"<title>{s['name']} feeding guide · Shada Bird Feed</title>")
        .replace('<link rel="canonical" href="https://shadabirdfeed.com/shop/">',
                 f'<link rel="canonical" href="https://shadabirdfeed.com/birds/{key}/">'))
    head = re.sub(r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="What to feed a {s["name"].lower()} at every stage, from day one to breeding season. Formula temperature, weaning age, and the three mistakes that cost a clutch."',
        head, count=1)

    return head.replace('</head>', f'<style>{CSS}</style>\n{ldjson}\n</head>') + body + FOOT


if __name__ == '__main__':
    key = sys.argv[1] if len(sys.argv) > 1 else 'lovebird'
    classes = assert_no_collisions()
    os.makedirs('/tmp/pg/out', exist_ok=True)
    s = SPECIES[key]

    # THE GLOBAL TEMPLATE — build this once in Elementor, all 6 species use it.
    tpl = build(key, template=True)
    open('/tmp/pg/out/birds-TEMPLATE.html', 'w', encoding='utf-8').write(tpl)
    print(f'birds-TEMPLATE.html       {round(len(tpl)/1024):4} KB  dynamic tags + loop')

    # Reference build, lovebird content filled in, so the template can be seen working.
    html = build(key)
    open(f'/tmp/pg/out/birds-{key}.html', 'w', encoding='utf-8').write(html)
    print(f'birds-{key}.html          {round(len(html)/1024):4} KB  live image URLs')

    # Preview build: the same page with compressed images inlined, so it renders
    # correctly offline. Never paste this one into WordPress.
    inline_path = '/tmp/pimg/inline.json'
    if os.path.exists(inline_path):
        table = json.load(open(inline_path))
        prev = html
        for _, _, _, img, _, _, _, _ in CATALOGUE:
            if img in table:
                prev = prev.replace(IMG + img, table[img])
        prev = prev.replace('</head>',
            '<style>/* preview only */.sgrid img{background:var(--paper2)}</style></head>', 1)
        open(f'/tmp/pg/out/birds-{key}-PREVIEW.html', 'w', encoding='utf-8').write(prev)
        print(f'birds-{key}-PREVIEW.html  {round(len(prev)/1024):4} KB  images inlined')

    print(f'{len(s["stages"])} stages · {len(MISTAKES)} mistakes · {len(s["faq"])} FAQ · '
          f'{len(CATALOGUE)} products · {len(classes)} classes, 0 collisions')
