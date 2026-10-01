#!/usr/bin/env python3
# Shada Bird Feed · FAQ page  /faq/   +   the Dealers empty state
#
# Two deliverables in one generator because they share the .fq* CSS block.
#   1. faq.html          the full FAQ page
#   2. dealers-empty.html  the "no dealer in your district yet" state, as a
#      standalone fragment to drop into the dealers page template
import re, os, sys, json

HEAD = open('/tmp/pg/head.txt', encoding='utf-8').read()
FOOT = open('/tmp/pg/foot.txt', encoding='utf-8').read()

WA, PH = '8801813323535', '01813-323535'

I = lambda p, w=1.9: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
I_WA = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd">'
        '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.9a8.1 8.1 0 0 1 6.6 12.8l-.3.4.7 2.5-2.6-.7-.4.2A8.1 8.1 0 1 1 12 3.9Z"/>'
        '<path d="M9.1 7.2h.6c.2 0 .5-.1.7.5l.9 2.2c.1.1.1.3 0 .5l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.4 2.4 1.5.3.1.4.1.6-.1.1-.2.7-.9.9-1.2.2-.2.4-.2.7-.1.2.1 1.7.9 2 1 .3.1.5.2.6.4 0 .1 0 .7-.2 1.4-.2.7-1.5 1.3-2 1.4-.6.1-1.1.3-3.6-.7-3-1.3-5-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.7-2.2 1-2.5c.3-.3.6-.4.8-.4Z"/></svg>')
I_ARROW = I('<path d="M5 12h14M12 5l7 7-7 7"/>', 2.4)
I_TRUCK = I('<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>')
I_PIN   = I('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>')

# ═════════════════════════════════════════════════════════════════════════
#  FAQ CONTENT
#  Grouped by what a visitor is actually trying to decide. Every answer is
#  verified against the site or the client's own data. Anything not yet
#  confirmed carries a [CONFIRM] marker rather than a guess.
# ═════════════════════════════════════════════════════════════════════════
GROUPS = [
 ('Ordering', 'How to buy, and what happens next.', [
   ('How do I place an order?',
    'Three ways. Order on this website, message us on WhatsApp at ' + PH + ', or buy from a '
    '<a href="/dealers/">dealer in your district</a>. WhatsApp is the fastest and it is how most '
    'customers order.'),
   ('Do I need an account to order?',
    'No. You can check out as a guest. An account is useful if you order regularly, because it '
    'keeps your address and lets you re-order a past order in one click.'),
   ('Can I change or cancel an order?',
    'Yes, if it has not left the factory. Message us on WhatsApp with your order number. Once the '
    'parcel is with the courier the <a href="/refund-returns/">refund and returns policy</a> applies instead.'),
   ('What payment methods do you accept?',
    '[CONFIRM: list every payment method, for example cash on delivery, bKash, Nagad, bank transfer]'),
 ]),

 ('Delivery', 'Where we ship, how long it takes, what it costs.', [
   ('Which districts do you deliver to?',
    'All 64 districts of Bangladesh, through Sundarban Courier.'),
   ('How long does delivery take?',
    'Two working days to most districts. Remote upazilas and hill districts can take longer. '
    'Working days are Saturday to Thursday, Friday is closed.'),
   ('What does delivery cost?',
    '[CONFIRM: the delivery charge. Flat rate, by district, or free above a minimum order?]'),
   ('How do I track my parcel?',
    'We send the tracking number once the parcel is collected. You can also message WhatsApp ' + PH +
    ' with your order number and we will check it for you.'),
   ('What if my parcel arrives damaged?',
    'Photograph the parcel and the jar before opening anything else, then message us the same day. '
    'A damaged, wrong or out-of-date product is replaced or refunded in full at our cost. See the '
    '<a href="/refund-returns/">refund and returns policy</a>.'),
 ]),

 ('The products', 'What is in the jar, and which one you need.', [
   ('Which product does my bird need?',
    'Start with the bird. We have a page for each species with a stage-by-stage feeding plan: '
    '<a href="/birds/lovebird/">lovebird</a>, <a href="/birds/budgerigar/">budgerigar</a>, '
    '<a href="/birds/cockatiel/">cockatiel</a>, <a href="/birds/conure/">conure</a>, '
    '<a href="/birds/ringneck/">ringneck</a> and <a href="/birds/rosella/">rosella</a>.'),
   ('Can Nutricare be used from day one?',
    'Yes. Nutricare is formulated for day one to weaning. Mix it thin at the start and thicken it '
    'as the chick grows.'),
   ('What temperature should hand feeding formula be?',
    'Between 39 and 41°C. Measure it, do not judge it by hand. Formula fed too cool is the most '
    'common cause of a crop that stops emptying.'),
   ('Is your feed repacked from another brand?',
    'No. Every jar is made and sealed at our own factory in Bhaluka, Mymensingh, with the batch '
    'date printed on the lid. We do not repack anyone else’s product.'),
   ('How should I store an opened jar?',
    'Sealed, dry and out of direct sun. Use a clean dry spoon every time. Moisture in the jar is '
    'what spoils a powder, not age.'),
   ('Is your feeding guidance veterinary advice?',
    'No. It is general guidance from breeders, based on published aviculture practice and our own '
    'experience. A bird that is unwell, or a chick that is not gaining weight, needs an avian vet.'),
 ]),

 ('Price and dealers', 'What it costs, and how to buy at wholesale.', [
   ('Is the price the same everywhere?',
    'Yes. We publish one retail price and hold it in all 64 districts, including on this website. '
    'A dealer may not advertise below it.'),
   ('How do I become a dealer?',
    'Apply on the <a href="/wholesale/">wholesale page</a>. We open one distributor per district. '
    'Dealers buy 20 to 42 percent below the printed retail price depending on the pack and the tier.'),
   ('Is there a franchise fee?',
    'No. No franchise fee, no monthly target, no lock-in. You buy at the dealer price and sell at '
    'the printed retail price.'),
   ('There is no dealer in my district. Can I still order?',
    'Yes. Order on this website or on WhatsApp and we deliver direct, anywhere in Bangladesh. '
    'A missing dealer never means a missing delivery.'),
 ]),
]

CSS = '''
/* ═══════════════════════════════════════════════════════════════════════════
   FAQ  ·  /faq/   and the DEALERS EMPTY STATE
   Loads after 01-base.css. Homepage classes plus a .fq* block.
   Prefix checked against the site stylesheet at build time, see
   assert_no_collisions() in the generator.
   ═══════════════════════════════════════════════════════════════════════════ */

/* ── Hero ────────────────────────────────────────────────────────────── */
.fqhero{background:var(--ink);color:#fff;position:relative;overflow:hidden;
  padding:clamp(36px,4.6vw,64px) 0 clamp(32px,4vw,52px)}
.fqhero::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;
  opacity:.07;pointer-events:none}
.fqhero .wrap{position:relative}
.fqhero h1{font-size:clamp(32px,4.6vw,56px);letter-spacing:-.036em;line-height:1.05;margin:10px 0 13px}
.fqhero p{font-size:17px;line-height:1.6;color:var(--on2);max-width:54ch}
.fqhero .acts{display:flex;gap:11px;flex-wrap:wrap;margin-top:26px}

/* ── Jump chips ──────────────────────────────────────────────────────── */
.fqjump{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:clamp(28px,3.4vw,44px);
  padding-bottom:clamp(20px,2.4vw,30px);border-bottom:1px solid var(--line)}
.fqjump a{display:inline-flex;align-items:center;min-height:38px;padding:8px 15px;border-radius:999px;
  border:1px solid var(--line);background:#fff;font-size:14px;font-weight:500;color:var(--tx2);
  text-decoration:none;transition:border-color .15s,color .15s,background .15s}
.fqjump a:hover{color:var(--brand);border-color:var(--brand);background:var(--paper2)}

/* ── Groups ──────────────────────────────────────────────────────────── */
.fqgroup{margin-bottom:clamp(34px,4vw,54px)}
.fqgroup:last-child{margin-bottom:0}
.fqgroup h2{font-size:clamp(22px,2.5vw,30px);letter-spacing:-.026em;line-height:1.2;
  margin-bottom:5px;scroll-margin-top:90px}
.fqgroup .gs{display:block;font-size:15px;color:var(--tx2);line-height:1.55;margin-bottom:16px}
.fqlist{border-top:1px solid var(--line);max-width:860px}

.fqq{border-bottom:1px solid var(--line)}
.fqq summary{display:flex;align-items:flex-start;gap:14px;justify-content:space-between;
  padding:19px 0;cursor:pointer;list-style:none;font-size:clamp(16.5px,1.75vw,19px);
  font-weight:600;letter-spacing:-.018em;line-height:1.35;color:var(--tx)}
.fqq summary::-webkit-details-marker{display:none}
.fqq summary:hover{color:var(--brand)}
.fqq .pm{flex:0 0 auto;width:26px;height:26px;border-radius:50%;border:1px solid var(--line);
  display:grid;place-items:center;margin-top:1px;
  transition:transform .2s var(--ease),background .2s,border-color .2s}
/* Both bars must share ONE grid cell or the plus renders as a vertical bar. */
.fqq .pm::before,.fqq .pm::after{content:"";grid-area:1/1;background:var(--tx2);
  border-radius:1px;transition:opacity .2s,background .2s}
.fqq .pm::before{width:11px;height:1.6px}
.fqq .pm::after{width:1.6px;height:11px}
.fqq[open] .pm{background:var(--brand);border-color:var(--brand);transform:rotate(180deg)}
.fqq[open] .pm::before,.fqq[open] .pm::after{background:#fff}
.fqq[open] .pm::after{opacity:0}
.fqq .a{padding:0 44px 21px 0;font-size:16px;line-height:1.68;color:var(--tx2);max-width:74ch}
.fqq .a a{color:var(--brand);font-weight:500;border-bottom:1px solid rgba(8,152,48,.3)}
.fqq .a a:hover{border-color:var(--brand)}

/* Unresolved client decision. Must be zero of these before launch. */
.fqq mark.tbc,mark.tbc{background:#FFE9A8;color:#6B4E00;border-radius:4px;padding:1px 6px;
  font-weight:600;font-size:14.5px;box-decoration-break:clone;-webkit-box-decoration-break:clone}

/* ── Still stuck ─────────────────────────────────────────────────────── */
.fqend{margin-top:clamp(36px,4.4vw,58px);background:var(--paper2);border:1px solid var(--line);
  border-radius:var(--r3);padding:clamp(24px,3vw,36px);display:flex;gap:20px;
  align-items:center;justify-content:space-between;flex-wrap:wrap}
.fqend h3{font-size:clamp(19px,2.1vw,24px);letter-spacing:-.022em;margin-bottom:6px}
.fqend p{font-size:15px;color:var(--tx2);line-height:1.55;max-width:46ch}
.fqend .acts{display:flex;gap:10px;flex-wrap:wrap}

/* ═══════════════════════════════════════════════════════════════════════════
   DEALERS EMPTY STATE
   Shows when a district filter returns nothing. An empty list is a dead end;
   this turns it into a delivery offer. A missing dealer must never read as a
   missing service.
   ═══════════════════════════════════════════════════════════════════════════ */
.fqnone{background:#fff;border:1px solid var(--line);border-radius:var(--r3);
  padding:clamp(28px,3.6vw,48px);text-align:center;max-width:620px;margin:0 auto}
.fqnone .ic{width:54px;height:54px;border-radius:15px;display:grid;place-items:center;
  margin:0 auto 18px;background:var(--brand-soft);border:1px solid rgba(8,152,48,.22)}
.fqnone .ic svg{width:26px;height:26px;color:var(--brand)}
.fqnone h3{font-size:clamp(20px,2.3vw,27px);letter-spacing:-.025em;line-height:1.22;margin-bottom:10px}
.fqnone p{font-size:16px;line-height:1.62;color:var(--tx2);max-width:44ch;margin:0 auto}
.fqnone .acts{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:24px}
.fqnone .fine{margin-top:20px;padding-top:18px;border-top:1px solid var(--line);
  font-size:13.5px;color:var(--tx3);line-height:1.55}
@media(max-width:520px){.fqnone .acts .btn{width:100%}}
'''


def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def assert_no_collisions():
    mine = sorted(set(re.findall(r'\.(fq[a-z0-9]+)\b', CSS)))
    clash = [c for c in mine if re.search(r'[.\s]' + c + r'\b[^{}]{0,150}\{', HEAD)]
    if clash:
        raise SystemExit('CLASS COLLISION: ' + ', '.join(clash) + '  — nothing written.')
    return mine


def faq_page():
    jump = ''.join(f'<a href="#{slug(g)}">{g}</a>' for g, _, _ in GROUPS)
    groups = ''
    for g, blurb, qs in GROUPS:
        items = ''.join(
            f'<details class="fqq"><summary>{q}<span class="pm"></span></summary>'
            f'<div class="a">{a}</div></details>' for q, a in qs)
        groups += (f'<div class="fqgroup"><h2 id="{slug(g)}">{g}</h2>'
                   f'<span class="gs">{blurb}</span><div class="fqlist">{items}</div></div>')

    total = sum(len(qs) for _, _, qs in GROUPS)

    body = f'''<main id="main">

<!-- ═══════════ HERO ═══════════ -->
<section class="fqhero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb" style="color:var(--on2)"><a href="/" style="color:var(--on2)">Home</a><i></i><span style="color:#fff">FAQ</span></nav>
    <span class="eyebrow" style="color:var(--leaf)">Questions</span>
    <h1>Answers, not a phone queue.</h1>
    <p>Ordering, delivery, the products themselves, and how dealer pricing works. If your question
    is not here, message us and a person answers.</p>
    <div class="acts">
      <a class="btn b-brand" href="https://wa.me/{WA}" target="_blank" rel="noopener">{I_WA} WhatsApp {PH}</a>
      <a class="btn b-white" href="/contact/">Contact page {I_ARROW}</a>
    </div>
  </div>
</section>

<!-- ═══════════ THE QUESTIONS ═══════════ -->
<section>
  <div class="wrap">
    <nav class="fqjump" aria-label="Jump to a section">{jump}</nav>
    {groups}
    <div class="fqend">
      <div>
        <h3>Still not answered?</h3>
        <p>Message us on WhatsApp. We answer faster there than anywhere else, and a breeder replies,
        not a script.</p>
      </div>
      <div class="acts">
        <a class="btn b-brand" href="https://wa.me/{WA}" target="_blank" rel="noopener">{I_WA} Ask on WhatsApp</a>
        <a class="btn b-line" href="/contact/">Contact form</a>
      </div>
    </div>
  </div>
</section>

<!-- ═══════════ FINAL CTA ═══════════ -->
<section class="brand wing">
  <div class="wrap ctr" style="position:relative;z-index:1">
    <h2 class="h-l" style="color:#fff">Start with one jar.</h2>
    <p class="sub" style="color:rgba(255,255,255,.85);margin-top:12px">Sealed in Bhaluka, batch date on the lid. Two working days to most districts.</p>
    <div style="display:flex;gap:11px;flex-wrap:wrap;justify-content:center;margin-top:30px">
      <a class="btn b-white b-lg" href="/shop/">Shop the range {I_ARROW}</a>
      <a class="btn b-line b-lg" href="/wholesale/">Dealer pricing</a>
    </div>
  </div>
</section>

</main>
'''

    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer",
                                             "text": re.sub(r'<[^>]+>', '', a)}}
                         for _, _, qs in GROUPS for q, a in qs]}

    head = (HEAD
        .replace('<title>Shop · Shada Bird Feed</title>', '<title>FAQ · Shada Bird Feed</title>')
        .replace('<link rel="canonical" href="https://shadabirdfeed.com/shop/">',
                 '<link rel="canonical" href="https://shadabirdfeed.com/faq/">'))
    head = re.sub(r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{total} answers on ordering, delivery to all 64 districts, '
        'the six formulas, and how to become a Shada dealer."', head, count=1)
    return (head.replace('</head>',
            f'<style>{CSS}</style>\n<script type="application/ld+json">'
            + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>')
            + body + FOOT), total


def dealers_empty():
    """Standalone fragment. Drop into the dealers template where the list renders."""
    frag = f'''<!-- ═══════════════════════════════════════════════════════════════
     DEALERS EMPTY STATE
     Render this INSTEAD of the dealer list when a district filter returns
     zero results, and when the list is empty overall.
     Replace {{DISTRICT}} with the selected district name, or drop that
     sentence entirely if no district is selected.
     ═══════════════════════════════════════════════════════════════ -->
<div class="fqnone">
  <span class="ic">{I_TRUCK}</span>
  <h3>No dealer in {{DISTRICT}} yet. You can still order.</h3>
  <p>We deliver direct to all 64 districts through Sundarban Courier, usually in two working days.
  A missing dealer never means a missing delivery.</p>
  <div class="acts">
    <a class="btn b-brand" href="/shop/">Order direct {I_ARROW}</a>
    <a class="btn b-line" href="https://wa.me/{WA}?text=Is%20there%20a%20dealer%20near%20me%3F" target="_blank" rel="noopener">{I_WA} Ask on WhatsApp</a>
  </div>
  <p class="fine">Run a shop in {{DISTRICT}}? We open one distributor per district and this one is
  still open. <a class="link" style="font-size:inherit" href="/wholesale/">See dealer pricing</a>.</p>
</div>
'''
    # a standalone preview so the state can be seen without the dealers page
    prev = (HEAD.replace('<title>Shop · Shada Bird Feed</title>',
                         '<title>Dealers empty state · preview</title>')
            .replace('</head>', f'<style>{CSS}</style></head>')
            + '<main id="main"><section class="tint"><div class="wrap">'
            + '<div class="head"><span class="eyebrow">Preview</span>'
            + '<h2 class="h-l">Dealers, empty state.</h2></div>'
            + frag.replace('{DISTRICT}', 'Bandarban')
            + '</div></section></main>' + FOOT)
    return frag, prev


if __name__ == '__main__':
    classes = assert_no_collisions()
    os.makedirs('/tmp/pg/out', exist_ok=True)
    html, total = faq_page()
    open('/tmp/pg/out/faq.html', 'w', encoding='utf-8').write(html)
    frag, prev = dealers_empty()
    open('/tmp/pg/out/dealers-empty-state.html', 'w', encoding='utf-8').write(frag)
    open('/tmp/pg/out/dealers-empty-PREVIEW.html', 'w', encoding='utf-8').write(prev)
    print(f'faq.html                    {round(len(html)/1024):4} KB  {total} questions in {len(GROUPS)} groups')
    print(f'dealers-empty-state.html    {round(len(frag)/1024):4} KB  fragment')
    print(f'dealers-empty-PREVIEW.html  {round(len(prev)/1024):4} KB')
    print(f'{len(classes)} classes, 0 collisions | CONFIRM markers: {html.count("[CONFIRM")}')
