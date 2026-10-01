#!/usr/bin/env python3
# Shada Bird Feed · About page generator
# Built on the homepage's own section classes: section / .dark / .tint / .wing /
# .wrap / .head / .eyebrow / .h-l / .h-m / .sub / .steps / .step / .btn / .link.
# Only the handful of classes unique to this page live in the page CSS block.
import re, os, json, base64

HEAD = open('/tmp/pg/head.txt', encoding='utf-8').read()
FOOT = open('/tmp/pg/foot.txt', encoding='utf-8').read()

WA   = '8801813323535'
PH   = '01813-323535'
MAIL = 'shadabirdfeed@gmail.com'
ADDR = 'Majorvita, Bhaluka, Mymensingh'

HOME = "/sessions/pensive-affectionate-einstein/mnt/Projects/Shada Birds/SHADA-SHOP-LIVE/01-HOME/assets"

def datauri(path, mime):
    return 'data:' + mime + ';base64,' + base64.b64encode(open(path, 'rb').read()).decode()

PHOTO = datauri(f"{HOME}/images-photos/breeder-lovebird-bhaluka-1200.webp", 'image/webp')
JARS  = {k: datauri(f"{HOME}/images-products/jar-{k}-thumb-160.webp", 'image/webp')
         for k in ['nutricare', 'eggfood', 'spirulina', 'moringa', 'beetroot', 'herbs']}

I = lambda p, w=1.9: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
I_WA    = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd">'
           '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.9a8.1 8.1 0 0 1 6.6 12.8l-.3.4.7 2.5-2.6-.7-.4.2A8.1 8.1 0 1 1 12 3.9Z"/>'
           '<path d="M9.1 7.2h.6c.2 0 .5-.1.7.5l.9 2.2c.1.1.1.3 0 .5l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.4 2.4 1.5.3.1.4.1.6-.1.1-.2.7-.9.9-1.2.2-.2.4-.2.7-.1.2.1 1.7.9 2 1 .3.1.5.2.6.4 0 .1 0 .7-.2 1.4-.2.7-1.5 1.3-2 1.4-.6.1-1.1.3-3.6-.7-3-1.3-5-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.7-2.2 1-2.5c.3-.3.6-.4.8-.4Z"/></svg>')
I_PHONE = I('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7A2 2 0 0 1 22 16.9z"/>')
I_MAIL  = I('<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m3 7 8.2 5.5a2 2 0 0 0 2.2 0L22 7"/>')
I_PIN   = I('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>')
I_CLOCK = I('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
I_LEAF  = I('<path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15zM5 19l8-8"/>')
I_LOCK  = I('<rect x="3" y="7" width="18" height="14" rx="3"/><path d="M8 7V5a4 4 0 0 1 8 0v2M12 12v4"/>')
I_GLOBE = I('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>')
I_ARROW = I('<path d="M5 12h14M12 5l7 7-7 7"/>', 2.4)
I_NO    = I('<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>', 2.1)
I_EYE   = I('<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>')
I_FACT  = I('<path d="M3 21V9l6 4V9l6 4V9l6 4v8zM3 21h18M7 17h2M13 17h2"/>')
I_JAR   = I('<path d="M7 9h10l-1 11a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2z"/><path d="M9 9V6a3 3 0 0 1 6 0v3M8 4h8"/>')
I_MAPBD = I('<path d="M3 7l6-3 6 3 6-3v13l-6 3-6-3-6 3zM9 4v13M15 7v13"/>')
I_SHOP  = I('<path d="M4 9h16l-1 11H5zM4 9l1.4-4.2A1 1 0 0 1 6.3 4h11.4a1 1 0 0 1 .9.8L20 9M9 13h6"/>')
I_TARGET= I('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>')

CSS = '''
/* ═══════════════════════════════════════════════════════════════════
   ABOUT  ·  /about/
   Loads after 01-base.css and 02-shop-pages.css.
   Built on the homepage's own classes: section / .dark / .tint / .wing /
   .wrap / .head / .eyebrow / .h-l / .h-m / .sub / .btn / .link.
   Five sections, nothing more. Checked against Vetafarm, Nekton and
   Aviform: all three run intro, story, a "why us" card row, and a short
   mission. None of them puts a product grid or a manufacturing
   walkthrough on this page, so neither do we.
   ═══════════════════════════════════════════════════════════════════ */

/* ── Hero ────────────────────────────────────────────────────────── */
.abhero{background:var(--ink);color:#fff;position:relative;overflow:hidden;
  padding:clamp(40px,5.4vw,78px) 0 clamp(38px,4.8vw,66px)}
.abhero::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;opacity:.07;pointer-events:none}
.abhero .wrap{position:relative;display:grid;grid-template-columns:1.06fr .94fr;
  gap:clamp(30px,4vw,64px);align-items:center}
@media(max-width:980px){.abhero .wrap{grid-template-columns:1fr;gap:34px}}
.abhero h1{font-size:clamp(34px,5vw,62px);letter-spacing:-.035em;line-height:1.04;margin:10px 0 14px;max-width:16ch}
.abhero .lede{font-size:17.5px;line-height:1.6;color:var(--on2);max-width:52ch}
.abhero .acts{display:flex;gap:11px;flex-wrap:wrap;margin-top:26px}

/* Photo card, same halo the homepage puts behind a product tile */
.abshot{position:relative;justify-self:end;width:100%;max-width:520px}
@media(max-width:980px){.abshot{justify-self:stretch;max-width:none}}
.abshot::before{content:"";position:absolute;inset:-12% -8%;border-radius:50%;
  background:radial-gradient(circle,rgba(95,212,138,.30),transparent 68%);z-index:0;pointer-events:none}
.abshot figure{position:relative;z-index:1;margin:0;border-radius:var(--r3);overflow:hidden;
  border:1px solid var(--line-d);box-shadow:0 30px 70px rgba(0,0,0,.36)}
.abshot img{display:block;width:100%;height:auto}
.abshot .chip{position:absolute;left:16px;bottom:16px;z-index:2;display:inline-flex;align-items:center;gap:8px;
  background:rgba(10,38,23,.82);backdrop-filter:blur(8px);border:1px solid rgba(95,212,138,.3);
  border-radius:999px;padding:9px 15px;font-size:12.5px;font-weight:600;color:#fff}
.abshot .chip svg{width:15px;height:15px;color:var(--leaf)}

/* ── Story. Short, with the four facts sitting under it as a strip.
      Vetafarm puts its numbers right after the intro. Same place. ─── */
.abstory{max-width:760px}
.abstory p{font-size:17px;line-height:1.7;color:var(--tx2);margin-bottom:16px}
.abstory p b{color:var(--tx);font-weight:600}
.abfacts{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:clamp(36px,4.4vw,56px);
  border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
@media(max-width:760px){.abfacts{grid-template-columns:repeat(2,1fr)}}
.abfact{padding:26px 22px;border-left:1px solid var(--line)}
.abfact:first-child{border-left:0;padding-left:0}
@media(max-width:760px){.abfact:nth-child(3){border-left:0;padding-left:0}
  .abfact:nth-child(3),.abfact:nth-child(4){border-top:1px solid var(--line)}}
.abfact b{display:block;font-size:clamp(30px,3.4vw,42px);letter-spacing:-.04em;line-height:1;
  font-variant-numeric:tabular-nums}
.abfact span{display:block;font-size:13.5px;color:var(--tx2);margin-top:8px;line-height:1.45}

/* ── Why Shada. The card row every competitor has. ──────────────── */
.abwhy{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:860px){.abwhy{grid-template-columns:1fr}}
.abw{background:var(--ink2);border:1px solid var(--line-d);border-radius:var(--r3);padding:30px 32px}
.abw .ic{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;margin-bottom:18px;
  background:rgba(95,212,138,.12);border:1px solid rgba(95,212,138,.22)}
.abw .ic svg{width:21px;height:21px;color:var(--leaf)}
.abw h3{font-size:20px;letter-spacing:-.02em;margin-bottom:9px;line-height:1.3}
.abw p{font-size:15.5px;line-height:1.6;color:var(--on2)}

/* ── Mission and vision, on the brand green band.
      Same treatment as the homepage finale: solid lid green, the wing
      watermark in white over it, white type. ───────────────────────── */
.abmv{display:grid;grid-template-columns:1fr 1fr;gap:0}
@media(max-width:820px){.abmv{grid-template-columns:1fr}}
.abm{padding:clamp(6px,1vw,14px) clamp(28px,3.4vw,52px)}
.abm:first-child{padding-left:0;border-right:1px solid rgba(255,255,255,.22)}
.abm:last-child{padding-right:0}
@media(max-width:820px){
  .abm:first-child{border-right:0;border-bottom:1px solid rgba(255,255,255,.22);padding:0 0 30px}
  .abm:last-child{padding:30px 0 0}
}
.abm .n{display:block;font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
  color:#DFF7E6;margin-bottom:16px}
.abm p{font-size:clamp(20px,2.2vw,27px);line-height:1.42;letter-spacing:-.02em;color:#fff;font-weight:500}

/* ── Contact strip ──────────────────────────────────────────────── */
.abcontact{display:grid;grid-template-columns:repeat(4,1fr);gap:13px}
@media(max-width:900px){.abcontact{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.abcontact{grid-template-columns:1fr}}
.abc{display:flex;gap:13px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line-d);
  border-radius:var(--r2);padding:20px;text-decoration:none;color:#fff;
  transition:border-color .2s,transform .3s var(--ease)}
a.abc:hover{border-color:var(--leaf);transform:translateY(-3px)}
.abc svg{width:20px;height:20px;flex:0 0 auto;margin-top:2px;color:var(--leaf)}
.abc b{display:block;font-size:15.5px;letter-spacing:-.01em;margin-bottom:3px}
.abc span{display:block;font-size:13px;color:var(--on2);line-height:1.45}
'''


def about_page():
    body = f'''<main id="main">

<!-- ═══════════ 1 · HERO ═══════════ -->
<section class="abhero">
  <div class="wrap">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb" style="color:var(--on2)"><a href="/" style="color:var(--on2)">Home</a><i></i><span style="color:#fff">About</span></nav>
      <span class="eyebrow" style="color:var(--leaf)">About Shada</span>
      <h1>Bangladesh&rsquo;s own bird nutrition company.</h1>
      <p class="lede">Six formulas, milled and sealed in our own factory in Bhaluka, sold at one
      price in all 64 districts.</p>
      <div class="acts">
        <a class="btn b-brand" href="/shop/">See the six formulas {I_ARROW}</a>
        <a class="btn b-white" href="/contact/">Talk to us</a>
      </div>
    </div>
    <div class="abshot">
      <figure>
        <img src="{PHOTO}" alt="A breeder hand feeding a lovebird chick in Bhaluka, Mymensingh" loading="eager">
      </figure>
      <span class="chip">{I_PIN} Majorvita, Bhaluka &middot; since 2021</span>
    </div>
  </div>
</section>

<!-- ═══════════ 2 · OUR STORY ═══════════ -->
<section class="tint">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow">Our story</span>
      <h2 class="h-l">Since 2021, made here.</h2>
    </div>
    <div class="abstory">
      <p>Shada started with a question nobody could answer well. Why should a breeder in Mymensingh
      pay imported prices for a formula built for a European winter, shipped through a port, a
      warehouse and two middlemen before it reaches a shop counter?</p>
      <p>The bird is the same bird. What changes is the climate, and what a breeder here can afford
      to buy <b>every month</b>, not once.</p>
      <p>So we built a factory in Majorvita, Bhaluka, and made the formula ourselves. Whole
      ingredients, milled fine, sealed the day they are made with the batch date on the lid. Six
      formulas later, the answer is still the same jar.</p>
    </div>
    <div class="abfacts">
      <div class="abfact"><b>2021</b><span>Making bird feed in Bhaluka since</span></div>
      <div class="abfact"><b>6</b><span>Formulas, one job each</span></div>
      <div class="abfact"><b>20</b><span>Pack sizes, 50g to 1kg</span></div>
      <div class="abfact"><b>64</b><span>Districts we deliver to</span></div>
    </div>
  </div>
</section>

<!-- ═══════════ 3 · WHY SHADA ═══════════ -->
<section class="dark wing">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow" style="color:var(--leaf)">Why Shada</span>
      <h2 class="h-l">Three things we will not do.</h2>
    </div>
    <div class="abwhy">
      <div class="abw"><span class="ic">{I_NO}</span>
        <h3>Sell an anonymous premix</h3>
        <p>If we cannot name an ingredient and say where it came from, it does not go in the jar.
        Every formula is built from whole ingredients we buy whole.</p></div>
      <div class="abw"><span class="ic">{I_LOCK}</span>
        <h3>Repack someone else&rsquo;s feed</h3>
        <p>Every jar is milled and sealed at our own factory, with the batch date on the lid.
        Nothing is bought in bulk and rebagged under our name.</p></div>
      <div class="abw"><span class="ic">{I_GLOBE}</span>
        <h3>Charge by district</h3>
        <p>One published price, retail and wholesale, in all 64 districts. A breeder in a small
        town pays what a breeder in Dhaka pays.</p></div>
    </div>
  </div>
</section>

<!-- ═══════════ 4 · MISSION AND VISION ═══════════ -->
<section class="brand wing" style="padding:clamp(56px,7vw,100px) 0">
  <div class="wrap" style="position:relative;z-index:1">
    <div class="abmv">
      <div class="abm"><span class="n">Our mission</span>
        <p>To put honest bird nutrition within monthly reach of every breeder in Bangladesh.</p></div>
      <div class="abm"><span class="n">Our vision</span>
        <p>Shada on the counter of a bird shop in every district, at the same price, with the same
        batch date on the lid.</p></div>
    </div>
  </div>
</section>

<!-- ═══════════ 5 · FIND US ═══════════ -->
<section class="dark wing">
  <div class="wrap">
    <div class="head">
      <span class="eyebrow" style="color:var(--leaf)">Find us</span>
      <h2 class="h-l">Come to the factory,<br>or just message us.</h2>
    </div>
    <div class="abcontact">
      <div class="abc">{I_PIN}<div><b>The factory</b><span>{ADDR}<br>Counter sales, no appointment needed.</span></div></div>
      <a class="abc" href="https://wa.me/{WA}" target="_blank" rel="noopener">{I_WA}<div><b>WhatsApp</b><span>{PH}<br>The fastest way to reach a breeder.</span></div></a>
      <a class="abc" href="tel:+{WA}">{I_PHONE}<div><b>Call</b><span>{PH}<br>Saturday to Thursday, 9am to 6pm.</span></div></a>
      <a class="abc" href="mailto:{MAIL}">{I_MAIL}<div><b>Email</b><span>{MAIL}</span></div></a>
    </div>
    <div style="margin-top:26px;display:flex;gap:11px;flex-wrap:wrap">
      <a class="btn b-brand" href="/contact/">Send a message {I_ARROW}</a>
      <a class="btn b-white" href="/dealers/">Find a dealer near you</a>
    </div>
  </div>
</section>

</main>
'''

    head = (HEAD
        .replace('<title>Shop · Shada Bird Feed</title>', '<title>About · Shada Bird Feed</title>')
        .replace('<link rel="canonical" href="https://shadabirdfeed.com/shop/">',
                 '<link rel="canonical" href="https://shadabirdfeed.com/about/">'))
    head = re.sub(r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Shada Bird Feed is made in Majorvita, Bhaluka, Mymensingh. Six formulas, whole ingredients, sealed at the factory, one price in all 64 districts."',
        head, count=1)

    ld = {"@context": "https://schema.org", "@type": "AboutPage",
          "name": "About Shada Bird Feed",
          "mainEntity": {
            "@type": "Organization", "name": "Shada Bird Feed",
            "foundingDate": "2021", "telephone": "+" + WA, "email": MAIL,
            "description": "Bird feed and supplements manufacturer in Bhaluka, Mymensingh, Bangladesh.",
            "address": {"@type": "PostalAddress", "streetAddress": "Majorvita",
                        "addressLocality": "Bhaluka", "addressRegion": "Mymensingh",
                        "addressCountry": "BD"},
            "areaServed": {"@type": "Country", "name": "Bangladesh"}}}
    ldjson = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    return head.replace('</head>', f'<style>{CSS}</style>\n{ldjson}\n</head>') + body + FOOT


if __name__ == '__main__':
    os.makedirs('/tmp/pg/out', exist_ok=True)
    open('/tmp/pg/out/about.html', 'w', encoding='utf-8').write(about_page())
    print('about.html', round(os.path.getsize('/tmp/pg/out/about.html') / 1024), 'KB')
