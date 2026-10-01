#!/usr/bin/env python3
# Shada Bird Feed · 404 page generator
# One screen. Say what happened, give the search box, give four ways out.
# Nothing else — a 404 is a junction, not a page to read.
import re, os, json

HEAD = open('/tmp/pg/head.txt', encoding='utf-8').read()
FOOT = open('/tmp/pg/foot.txt', encoding='utf-8').read()

WA = '8801813323535'
PH = '01813-323535'

I = lambda p, w=1.9: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
I_WA     = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd">'
            '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.9a8.1 8.1 0 0 1 6.6 12.8l-.3.4.7 2.5-2.6-.7-.4.2A8.1 8.1 0 1 1 12 3.9Z"/>'
            '<path d="M9.1 7.2h.6c.2 0 .5-.1.7.5l.9 2.2c.1.1.1.3 0 .5l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.4 2.4 1.5.3.1.4.1.6-.1.1-.2.7-.9.9-1.2.2-.2.4-.2.7-.1.2.1 1.7.9 2 1 .3.1.5.2.6.4 0 .1 0 .7-.2 1.4-.2.7-1.5 1.3-2 1.4-.6.1-1.1.3-3.6-.7-3-1.3-5-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.7-2.2 1-2.5c.3-.3.6-.4.8-.4Z"/></svg>')
I_SEARCH = I('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', 2.1)
I_BAG    = I('<path d="M6 7h12l1 13H5z"/><path d="M9 7a3 3 0 0 1 6 0"/>')
I_BOOK   = I('<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H19v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H19v3H6.5A2.5 2.5 0 0 1 4 20.5z"/>')
I_TAG    = I('<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>')
I_PIN    = I('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>')
I_ARROW  = I('<path d="M5 12h14M12 5l7 7-7 7"/>', 2.4)

# Four ways out. Ordered by how often a lost visitor actually wants them.
# Every URL here was checked live and returns 200. Do not add one without checking.
EXITS = [
    ('/shop/',    I_BAG,  'The shop',    'Six formulas, every pack size'),
    ('/blog/',    I_BOOK, 'Guides',      'Hand feeding, weaning, supplements'),
    ('/dealers/', I_PIN,  'Find a shop', 'Dealers by district'),
    ('/contact/', I_TAG,  'Talk to us',  'WhatsApp, phone or the form'),
]

CSS = '''
/* ═══════════════════════════════════════════════════════════════════
   404  ·  page not found
   Loads after 01-base.css. One screen, no scrolling on desktop.
   A 404 is a junction. Say what happened, then get the visitor moving.
   ═══════════════════════════════════════════════════════════════════ */
.e404{background:var(--ink);color:#fff;position:relative;overflow:hidden;
  min-height:calc(100vh - var(--hh,64px));min-height:calc(100svh - var(--hh,64px));
  display:grid;place-items:center;padding:clamp(48px,7vw,96px) 0}
.e404::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;
  opacity:.07;pointer-events:none}
.e404 .wrap{position:relative;text-align:center;max-width:820px}

.e404 .code{display:inline-flex;align-items:center;gap:9px;font-size:12.5px;font-weight:600;
  letter-spacing:.09em;text-transform:uppercase;color:var(--leaf);
  border:1px solid rgba(95,212,138,.34);border-radius:999px;padding:7px 15px;margin-bottom:20px}
.e404 .code b{font-weight:700;color:#fff}
.e404 h1{font-size:clamp(32px,5vw,58px);letter-spacing:-.035em;line-height:1.05;margin-bottom:14px}
.e404 .lede{font-size:17px;line-height:1.6;color:var(--on2);max-width:50ch;margin:0 auto}

/* Search. The single most useful control on a 404. */
.e4s{display:flex;gap:9px;max-width:460px;margin:30px auto 0}
.e4s .f{position:relative;flex:1}
.e4s .f svg{position:absolute;left:16px;top:50%;transform:translateY(-50%);
  width:18px;height:18px;color:var(--tx3);pointer-events:none}
.e4s input{width:100%;height:56px;border:1.5px solid transparent;border-radius:var(--r2);background:#fff;
  padding:0 16px 0 44px;font:500 15.5px/1 var(--ff);color:var(--tx);outline:none;
  transition:border-color .18s,box-shadow .18s}
.e4s input::placeholder{color:var(--tx3);font-weight:400}
.e4s input:focus{border-color:var(--leaf);box-shadow:0 0 0 4px rgba(95,212,138,.22)}
.e4s button{flex:0 0 auto;height:56px;padding:0 24px}
@media(max-width:520px){
  .e4s{flex-direction:column;gap:10px}
  .e4s button{width:100%}
}

/* Four ways out */
/* Stays 2 wide down to 320px. A stacked column pushes the last exit
   below the fold on a phone, which is the one thing a 404 must not do. */
.e4x{display:grid;grid-template-columns:repeat(4,1fr);gap:11px;margin-top:38px;text-align:left}
@media(max-width:860px){.e4x{grid-template-columns:1fr 1fr;gap:9px}}
.e4c{display:block;background:var(--ink2);border:1px solid var(--line-d);border-radius:var(--r2);
  padding:20px;text-decoration:none;color:#fff;transition:border-color .18s,background .18s}
@media(max-width:860px){.e4c{padding:16px 15px}
  .e4c svg{margin-bottom:10px}.e4c b{font-size:15px}.e4c span{font-size:12.5px}}
.e4c:hover{background:#17402c;border-color:rgba(95,212,138,.45)}
.e4c svg{width:21px;height:21px;color:var(--leaf);margin-bottom:13px}
.e4c b{display:block;font-size:16px;font-weight:600;letter-spacing:-.01em;margin-bottom:4px}
.e4c span{display:block;font-size:13.5px;line-height:1.45;color:var(--on2)}

.e4w{margin-top:32px;font-size:15px;color:var(--on2)}
.e4w a{display:inline-flex;align-items:center;gap:7px;color:#fff;font-weight:600;text-decoration:none;
  border-bottom:1px solid rgba(255,255,255,.34);padding-bottom:1px}
.e4w a:hover{color:var(--leaf);border-color:var(--leaf)}
.e4w a svg{width:17px;height:17px}
'''


def page404():
    exits = ''.join(
        f'<a class="e4c" href="{href}">{icon}<b>{title}</b><span>{sub}</span></a>'
        for href, icon, title, sub in EXITS)

    body = f'''<main id="main">

<!-- ═══════════ 404 ═══════════ -->
<section class="e404">
  <div class="wrap">
    <span class="code"><b>404</b> Page not found</span>
    <h1>That page is not here.</h1>
    <p class="lede">The link may be old, or the address mistyped. Nothing is wrong with your order
    or your account. Search below, or pick up where you meant to be.</p>

    <form class="e4s" role="search" method="get" action="/">
      <div class="f">
        {I_SEARCH}
        <input type="search" name="s" placeholder="Search products and guides"
               aria-label="Search this website" autocomplete="off">
      </div>
      <button class="btn b-brand" type="submit">Search {I_ARROW}</button>
    </form>

    <div class="e4x">{exits}</div>

    <p class="e4w">Looking for something specific?
      <a href="https://wa.me/{WA}?text=Hello" target="_blank" rel="noopener">{I_WA} WhatsApp {PH}</a>
    </p>
  </div>
</section>

</main>
'''

    head = (HEAD
        .replace('<title>Shop · Shada Bird Feed</title>', '<title>Page not found · Shada Bird Feed</title>')
        .replace('<link rel="canonical" href="https://shadabirdfeed.com/shop/">', ''))
    head = re.sub(r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="That page is not here. Search the site, or go to the shop, pack prices, guides or the dealer list."',
        head, count=1)
    # A 404 must never be indexed.
    head = head.replace('</head>', '<meta name="robots" content="noindex, follow">\n</head>')
    return head.replace('</head>', f'<style>{CSS}</style>\n</head>') + body + FOOT


if __name__ == '__main__':
    os.makedirs('/tmp/pg/out', exist_ok=True)
    open('/tmp/pg/out/404.html', 'w', encoding='utf-8').write(page404())
    print('404.html', round(os.path.getsize('/tmp/pg/out/404.html') / 1024), 'KB |',
          len(EXITS), 'exits | noindex set')
