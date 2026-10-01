import re,json,base64,io,os
from PIL import Image
T=open('shada-v21-template.html',encoding='utf-8').read()
head_css=T[T.index('<style>'):T.index('</style>')+8]
shell_top=T[T.index('<div class="tick"'):T.index('<main id="main">')]
footer=T[T.index('<footer>'):T.index('<script>')]
# Homepage-only anchors (#plan, #ladder, #about, ...) must point back at the homepage
# on every non-homepage page, or they are dead links. #main is the skip-link, leave it.
shell_top=re.sub(r'href="#(?!main\b)', 'href="/#', shell_top)
footer=re.sub(r'href="#(?!main\b)', 'href="/#', footer)
shell_top=re.sub(r'<svg(?![^>]*aria-hidden)', '<svg aria-hidden="true"', shell_top)
footer=re.sub(r'<svg(?![^>]*aria-hidden)', '<svg aria-hidden="true"', footer)
script=T[T.index('<script>'):T.rindex('</script>')+9].replace("document.getElementById('ltabs').addEventListener(","const _lt=document.getElementById('ltabs');if(_lt)_lt.addEventListener(")
AR='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
LK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
WA='<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5.3-.5c.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5 2.5 1 3 .8 3.6.7.5-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4ZM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>'
CATS={'hand-rearing':('Hand rearing','linear-gradient(145deg,#E6F4EA,#C9E8D2)','#089830'),'breeding':('Breeding','linear-gradient(145deg,#FBF3D6,#F2E2A8)','#B8871B'),'prices':('Prices','linear-gradient(145deg,#E8EEF9,#C9D7F0)','#123A72'),'supplements':('Supplements','linear-gradient(145deg,#FBE6EA,#F3C3CF)','#8E1F35'),'birds':('Birds','linear-gradient(145deg,#EAF3DF,#CFE5B6)','#5A8F3C'),'wholesale':('Wholesale','linear-gradient(145deg,#ECECE9,#D8D8D3)','#2F4A3C')}
ARTS=[
 ('hand-feeding-lovebird-chicks','hand-rearing','lovebird','How to hand feed a lovebird chick, day one to weaning','Water temperature, mix consistency, feeds per day by age, and the two mistakes that lose chicks in week one.',6,'2 Sep 2026'),
 ('bird-food-price-in-bangladesh','prices','budgerigar','Bird food prices in Bangladesh, 2026','Every hand feeding, eggfood and supplement brand sold here, per 100g, checked on the marketplaces. Imports included.',8,'28 Aug 2026'),
 ('spirulina-for-birds','supplements','rosella','Spirulina for birds: how much, how often, and when to stop','Why show breeders start six weeks out, what a pinch actually weighs, and the birds that should not have it at all.',5,'21 Aug 2026'),
 ('eggfood-through-the-season','breeding','cockatiel','Eggfood through the season: daily, or twice a week?','When the pair needs protein every day, when they need a break, and how to tell from the droppings.',4,'14 Aug 2026'),
 ('crop-not-emptying','hand-rearing','conure','Crop not emptying: what to do in the first hour','The three causes, in the order to check them, and the one thing never to do to a slow crop.',4,'7 Aug 2026'),
 ('red-factor-beetroot','supplements','conure','Red factor in conures and rosellas: beetroot through the moult','Why colour has to be fed before the feather grows, not after, and how long the moult window really is.',5,'31 Jul 2026'),
 ('budgerigar-chicks-when-to-pull','hand-rearing','budgerigar','Budgerigar chicks: when to pull, when to leave them','Pulling at two weeks versus three, what changes for the tame bird, and what changes for the parents.',6,'24 Jul 2026'),
 ('reading-a-jar-label','prices','ringneck','Reading a jar label: batch date, seal, and what repack means','How to tell a factory jar from a market repack in ten seconds, and why it matters more in the monsoon.',3,'17 Jul 2026'),
 ('first-clutch-lovebird-pair','breeding','lovebird','Setting up a lovebird pair for the first clutch','Cage, box, light and feed for the first season, and the mistake most first-year breeders make in month one.',7,'10 Jul 2026'),
 ('moringa-daily-pinch','supplements','budgerigar','Moringa for every bird: what a daily pinch does','Iron, calcium and vitamins for a bird that never sees a leaf, and how to get a fussy bird to take it.',4,'3 Jul 2026'),
 ('ringneck-weaning-week','birds','ringneck','Ringneck weaning: the slow week that decides the tame bird','Why ringnecks wean later than lovebirds, and how to keep the bird hand-tame through it.',5,'26 Jun 2026'),
 ('opening-a-bird-shop','wholesale','cockatiel','Opening a bird shop: the twenty SKUs that sell','What a first order looks like, which jars move weekly, and the counter card that does the selling.',6,'19 Jun 2026'),
]
def card(a,big=False):
    slug,cat,bird,title,ex,mins,date=a; cn,bg,ac=CATS[cat]
    return f'''<a class="post" href="/blog/{slug}/" style="--pa:{bg}">
        <div class="pa"><span class="cat">{cn}</span><img src="@B_{bird}@" alt=""></div>
        <div class="pb"><h3>{title}</h3><p>{ex}</p><div class="pm"><span>{mins} min read · {date}</span><span class="go">{AR}</span></div></div></a>'''
def chips(active='all'):
    out=f'<a class="cchip{" on" if active=="all" else ""}" href="/blog/">All guides</a>'
    for k,(n,bg,ac) in CATS.items(): out+=f'<a class="cchip{" on" if active==k else ""}" href="/blog/category/{k}/">{n}</a>'
    return f'<nav class="cchips" aria-label="Categories">{out}</nav>'
CTA=f'''<section class="brand wing final" style="overflow:hidden">
  <img class="avi" src="@B_budgerigar@" alt="" style="--w:clamp(70px,9vw,130px);left:clamp(8px,4vw,80px);bottom:10%;--d:.4s">
  <img class="avi mirror" src="@B_rosella@" alt="" style="--w:clamp(70px,9vw,130px);right:clamp(8px,4vw,80px);top:12%;--d:1.2s">
  <div class="wrap ctr"><span class="eyebrow">A question the guides did not answer?</span><h2 class="h-l">Send a photo of the bird.</h2><p class="sub" style="max-width:44ch;margin:0 auto 30px">A breeder replies on WhatsApp with the jar and the routine. No form, no wait.</p>
  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn b-white" href="https://wa.me/8801813323535" target="_blank" rel="noopener">{WA}&nbsp;Ask on WhatsApp</a><a class="btn b-line" href="/#plan">See the feeding plan</a></div></div>
</section>'''
BLOGCSS='''
/* ── blog system ── */
.bhero{padding:clamp(56px,7vw,96px) 0 clamp(28px,3.5vw,44px)}
.bhero h1{font-size:clamp(38px,5.6vw,68px);letter-spacing:-.04em;line-height:1.02;margin:12px 0 14px}
.bhero .sub{max-width:52ch}
.bhero-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:32px;align-items:end}
@media(max-width:800px){.bhero-grid{grid-template-columns:1fr}}
.bstats{display:flex;gap:22px;flex-wrap:wrap;justify-content:flex-end}
.bstats div{text-align:left} .bstats b{display:block;font-size:30px;font-weight:600;letter-spacing:-.04em;line-height:1;color:var(--brand-d)} .bstats span{font-size:13px;color:var(--tx2)}
@media(max-width:800px){.bstats{justify-content:flex-start}}
.cchips{display:flex;gap:8px;flex-wrap:wrap;margin:26px 0 0}
.cchip{display:inline-flex;align-items:center;min-height:38px;padding:0 14px;border-radius:var(--r);border:1px solid var(--line);background:#fff;font-size:13.5px;font-weight:500;color:var(--tx);transition:border-color .15s,background .15s,color .15s}
.cchip:hover{border-color:var(--brand)} .cchip.on{background:var(--ink);border-color:var(--ink);color:#fff}
.fpost{display:grid;grid-template-columns:1.1fr .9fr;gap:0;background:#fff;border:1px solid var(--line);border-radius:var(--r2);overflow:hidden;margin-bottom:18px;transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
.fpost:hover{transform:translateY(-6px);box-shadow:0 26px 54px rgba(0,0,0,.09)}
.fpost .fa{position:relative;display:grid;place-items:center;min-height:360px;background:var(--pa);overflow:hidden}
.fpost .fa img{width:min(60%,330px);transition:transform .6s var(--ease)} .fpost:hover .fa img{transform:scale(1.05) rotate(-4deg)}
.fpost .fa .cat{position:absolute;top:18px;left:18px;font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;background:rgba(255,255,255,.9);padding:5px 10px;border-radius:var(--r);color:var(--tx2)}
.fpost .fb{padding:clamp(24px,3vw,40px);display:flex;flex-direction:column}
.fpost .fb .eyebrow{margin-bottom:10px}
.fpost h2{font-size:clamp(24px,2.4vw,34px);letter-spacing:-.03em;line-height:1.12;margin-bottom:12px}
.fpost p{font-size:16px;color:var(--tx2);line-height:1.55;margin-bottom:22px;max-width:48ch}
.fpost .pm{margin-top:auto;display:flex;align-items:center;justify-content:space-between;font-size:13px;color:var(--tx3);padding-top:16px;border-top:1px solid var(--line)}
.fpost .pm .go{width:46px;height:28px;border-radius:var(--r);display:grid;place-items:center;border:1px solid var(--tx);color:var(--tx);transition:background .25s,color .25s}
.fpost .pm .go svg{width:17px;height:17px} .fpost:hover .pm .go{background:var(--brand);border-color:var(--brand);color:#fff}
@media(max-width:800px){.fpost{grid-template-columns:1fr}.fpost .fa{min-height:240px}}
.bsec{padding:clamp(36px,4.5vw,64px) 0}
.bsec .bhead{margin-bottom:22px}
.pager{display:flex;justify-content:center;gap:6px;margin-top:36px}
.pager a{min-width:42px;height:42px;padding:0 12px;display:inline-grid;place-items:center;border-radius:var(--r);border:1px solid var(--line);font-size:14px;font-weight:500}
.pager a.on{background:var(--ink);color:#fff;border-color:var(--ink)} .pager a:hover:not(.on){border-color:var(--brand)}
.topics{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:900px){.topics{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.topics{grid-template-columns:1fr}}
.topics .sbox:hover{border-color:var(--brand)}
.bsub{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:800px){.bsub{grid-template-columns:1fr}}
.bsub .dp{min-height:0}
/* article */
.crumbs{display:flex;gap:8px;align-items:center;font-size:13px;color:var(--tx2);flex-wrap:wrap} .crumbs a:hover{color:var(--brand-d)} .crumbs i{width:3px;height:3px;border-radius:50%;background:var(--tx3)}
.ahead{padding:clamp(40px,5vw,72px) 0 clamp(24px,3vw,40px)}
.ahead .cat{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ac,var(--brand));background:color-mix(in srgb,var(--ac,var(--brand)) 12%,#fff);padding:5px 10px;border-radius:var(--r);margin:22px 0 14px}
.ahead h1{font-size:clamp(32px,4.6vw,56px);letter-spacing:-.035em;line-height:1.06;max-width:22ch;margin-bottom:16px}
.ahead .lede{font-size:clamp(18px,1.8vw,21px);color:var(--tx2);line-height:1.45;max-width:56ch}
.ameta{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:22px;font-size:13.5px;color:var(--tx2)}
.ameta .av{width:36px;height:36px;border-radius:var(--r);background:var(--ink);color:#fff;display:grid;place-items:center;font-size:13px;font-weight:700}
.ameta b{color:var(--tx);font-weight:600} .ameta i{width:3px;height:3px;border-radius:50%;background:var(--tx3)}
.ahero{margin:0 auto;border-radius:var(--r2);background:var(--pa);min-height:clamp(220px,32vw,420px);display:grid;place-items:center;position:relative;overflow:hidden}
.ahero img{width:min(46%,360px);animation:hover 5.2s ease-in-out infinite}
.ahero .cap{position:absolute;bottom:14px;left:18px;font-size:12.5px;color:var(--tx2);background:rgba(255,255,255,.85);padding:5px 10px;border-radius:var(--r)}
.agrid{display:grid;grid-template-columns:240px minmax(0,720px);gap:clamp(32px,5vw,72px);justify-content:center;padding:clamp(32px,4vw,56px) 0 clamp(48px,6vw,80px)}
@media(max-width:900px){.agrid{grid-template-columns:1fr}}
.toc{position:sticky;top:84px;align-self:start;font-size:14px}
.toc .mh{display:block;margin-bottom:10px}
.toc a{display:block;padding:7px 0 7px 12px;border-left:2px solid var(--line);color:var(--tx2);line-height:1.35} .toc a:hover,.toc a.on{color:var(--tx);border-color:var(--brand)}
.toc .tshare{margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}
.share{display:flex;gap:6px;flex-wrap:wrap}
.share a,.share button{display:inline-flex;align-items:center;gap:6px;min-height:36px;padding:0 12px;border-radius:var(--r);border:1px solid var(--line);font-size:13px;font-weight:500;background:#fff}
.share a:hover,.share button:hover{border-color:var(--brand)} .share svg{width:15px;height:15px}
@media(max-width:900px){.toc{position:static;padding:16px 18px;background:var(--paper2);border-radius:var(--r2)}.toc a{display:inline-block;border:0;padding:4px 10px 4px 0}}
.abody{font-size:17px;line-height:1.7;color:var(--tx)}
.abody>*+*{margin-top:1.1em}
.abody h2{font-size:clamp(24px,2.3vw,30px);letter-spacing:-.03em;line-height:1.15;margin-top:2em;scroll-margin-top:90px}
.abody h3{font-size:20px;letter-spacing:-.02em;margin-top:1.6em}
.abody p{color:var(--tx)} .abody p.lead{font-size:19px}
.abody ul,.abody ol{padding-left:1.3em} .abody li+li{margin-top:.4em} .abody li::marker{color:var(--brand)}
.abody strong{font-weight:600}
.abody a{color:var(--brand-d);text-decoration:underline;text-underline-offset:3px;text-decoration-color:rgba(8,152,48,.35)}
.abody table{width:100%;border-collapse:separate;border-spacing:0;font-size:15px;border:1px solid var(--line);border-radius:var(--r2);overflow:hidden}
.abody th,.abody td{padding:12px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top} .abody th{background:var(--paper2);font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--tx2)} .abody tr:last-child td{border-bottom:0} .abody td b{font-weight:600}
.callout{border-radius:var(--r2);padding:20px 22px;background:var(--brand-soft);border-left:4px solid var(--brand);font-size:16px}
.callout.warn{background:#FBE6EA;border-color:#8E1F35} .callout b{display:block;font-weight:600;margin-bottom:4px}
.pcard{display:grid;grid-template-columns:120px 1fr auto;gap:18px;align-items:center;padding:18px 22px;border-radius:var(--r2);background:var(--ink);color:#fff;text-decoration:none!important;position:relative;isolation:isolate;overflow:hidden}
.pcard img{width:120px;height:120px;object-fit:contain;filter:drop-shadow(0 14px 16px rgba(0,0,0,.35))}
.pcard b{display:block;font-size:19px;letter-spacing:-.02em;margin-bottom:4px} .pcard small{font-size:14px;color:var(--on2);line-height:1.4} .pcard .eyebrow{margin-bottom:6px}
.pcard .btn{white-space:nowrap}
.abody .pcard,.abody .pcard b,.abody .pcard small{color:#fff;text-decoration:none} .abody .pcard small{color:var(--on2)}
@media(max-width:600px){.pcard{grid-template-columns:1fr;text-align:center;justify-items:center}}
.abody figure{margin:0} .abody figcaption{font-size:13px;color:var(--tx3);margin-top:8px}
.afaq{margin-top:2.4em} .afaq .faqs{margin:0;max-width:none} .afaq h2{margin-bottom:.6em}
.author{display:flex;gap:16px;align-items:flex-start;padding:22px;border:1px solid var(--line);border-radius:var(--r2);margin-top:2.4em;font-size:15px}
.author .av{width:52px;height:52px;border-radius:var(--r);background:var(--ink);color:#fff;display:grid;place-items:center;font-size:17px;font-weight:700;flex-shrink:0}
.author b{display:block;font-weight:600;margin-bottom:2px} .author p{color:var(--tx2);margin:0}
.anext{display:flex;justify-content:space-between;gap:16px;margin-top:2.4em;padding-top:22px;border-top:1px solid var(--line);font-size:14px}
.anext a{max-width:46%;color:var(--tx)} .anext a small{display:block;color:var(--tx3);font-size:12px;margin-bottom:3px} .anext a b{font-weight:600;line-height:1.3} .anext a:last-child{text-align:right}
/* category */
.chero{padding:clamp(48px,6vw,84px) 0 clamp(28px,3.5vw,44px)}
.chero-grid{display:grid;grid-template-columns:1fr auto;gap:32px;align-items:center}
@media(max-width:800px){.chero-grid{grid-template-columns:1fr}}
.chero h1{font-size:clamp(36px,5.2vw,64px);letter-spacing:-.04em;line-height:1.03;margin:12px 0 14px}
.chero .sub{max-width:50ch}
.chero-art{width:clamp(180px,22vw,300px);height:clamp(180px,22vw,300px);border-radius:var(--r2);background:var(--pa);display:grid;place-items:center;position:relative;overflow:hidden}
.chero-art img{width:68%;animation:hover 5.2s ease-in-out infinite}
.cgrid{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:clamp(24px,4vw,56px);align-items:start}
@media(max-width:1000px){.cgrid{grid-template-columns:1fr}}
.cgrid .posts{grid-template-columns:repeat(2,1fr)} @media(max-width:600px){.cgrid .posts{grid-template-columns:1fr}}
.side{position:sticky;top:84px;display:grid;gap:14px}
@media(max-width:1000px){.side{position:static}}
.sbox{border:1px solid var(--line);border-radius:var(--r2);padding:20px;background:#fff}
.sbox .mh{display:block;margin-bottom:12px}
.sbox .cl a{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--line);font-size:14.5px} .sbox .cl a:last-child{border:0} .sbox .cl a:hover{color:var(--brand-d)} .sbox .cl span{color:var(--tx3);font-size:13px}
.sbox.dark{background:var(--ink);color:#fff;border-color:transparent}
.sbox.dark img{width:110px;margin:0 auto 10px;display:block;filter:drop-shadow(0 14px 16px rgba(0,0,0,.35))}
.sbox.dark b{display:block;font-size:18px;letter-spacing:-.02em;text-align:center} .sbox.dark small{display:block;text-align:center;color:var(--on2);font-size:13.5px;margin:4px 0 14px}
'''
def page(title,desc,path,body,extra_ld=''):
    ld=f'<script type="application/ld+json">{extra_ld}</script>' if extra_ld else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://shadabirdfeed.com{path}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600;700&display=swap" rel="stylesheet">
{ld}
{head_css.replace('</style>',BLOGCSS+'</style>')}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{shell_top}
<main id="main">
{body}
</main>

{footer}
{script}
</body>
</html>'''

# ── 1. BLOG INDEX ──
feat=ARTS[0]; slug,cat,bird,title,ex,mins,date=feat; cn,bg,ac=CATS[cat]
grid="\n".join(card(a) for a in ARTS[1:10])
index_body=f'''<section class="tint wing wing-l bhero">
  <div class="wrap">
    <div class="bhero-grid rv in">
      <div><span class="eyebrow">Guides from the aviary</span><h1>Feeding, explained.<br>With the number in the answer.</h1><p class="sub">Short guides written by breeders in Bhaluka: how much, how often, at what temperature, and what to do when it goes wrong.</p></div>
      <div class="bstats"><div><b>{len(ARTS)}</b><span>guides</span></div><div><b>6</b><span>topics</span></div><div><b>6</b><span>species</span></div></div>
    </div>
    {chips('all')}
  </div>
</section>
<section class="bsec">
  <div class="wrap">
    <a class="fpost rv in" href="/blog/{slug}/" style="--pa:{bg}">
      <div class="fa"><span class="cat">{cn}</span><img src="@B_{bird}@" alt=""></div>
      <div class="fb"><span class="eyebrow">Start here</span><h2>{title}</h2><p>{ex}</p><div class="pm"><span>{mins} min read · {date} · Shada aviary team</span><span class="go">{AR}</span></div></div>
    </a>
    <div class="bhead" style="margin-top:36px"><div><h2 class="h-m" style="font-size:clamp(24px,2.6vw,34px)">Latest guides</h2></div><span style="font-size:13.5px;color:var(--tx2)">Newest first</span></div>
    <div class="posts rv in">
{grid}
    </div>
    <div class="pager"><a class="on" href="/blog/">1</a><a href="/blog/page/2/">2</a><a href="/blog/page/2/">Next {LK}</a></div>
  </div>
</section>
<section class="tint bsec">
  <div class="wrap">
    <div class="bhead"><div><span class="eyebrow">Browse by topic</span><h2 class="h-m" style="font-size:clamp(24px,2.6vw,34px)">Six topics. Six species.</h2></div></div>
    <div class="topics">
      {"".join(f'<a class="sbox" href="/blog/category/{k}/" style="display:block"><span class="mh" style="color:{ac}">{n}</span><b style="display:block;font-size:17px;margin-bottom:6px">{["Chicks, crops, weaning","Pairs, clutches, the season","What things cost, and why","The four pinches","One species at a time","Shops and dealers"][i]}</b><small style="color:var(--tx2);font-size:13.5px">{sum(1 for a in ARTS if a[1]==k)} guides</small></a>' for i,(k,(n,bg,ac)) in enumerate(CATS.items()))}
    </div>
  </div>
</section>
{CTA}'''
# ── 2. SINGLE ARTICLE ──
a=ARTS[0]; slug,cat,bird,title,ex,mins,date=a; cn,bg,ac=CATS[cat]
related="\n".join(card(x) for x in ARTS if x[1]=='hand-rearing' and x[0]!=slug)+"\n"+card(ARTS[3])
article_body=f'''<section class="ahead" style="--ac:{ac}">
  <div class="wrap" style="max-width:1000px">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><i></i><a href="/blog/">Guides</a><i></i><a href="/blog/category/{cat}/">{cn}</a></nav>
    <span class="cat">{cn}</span>
    <h1>{title}</h1>
    <p class="lede">{ex}</p>
    <div class="ameta"><span class="av">SA</span><span><b>Shada aviary team</b>, Bhaluka</span><i></i><span>{date}</span><i></i><span>{mins} min read</span><i></i><span>Reviewed against the Nutricare label, batch 07·26</span></div>
  </div>
</section>
<section style="padding:0">
  <div class="wrap" style="max-width:1000px"><div class="ahero" style="--pa:{bg}"><img src="@B_{bird}@" alt="Lovebird illustration"><span class="cap">Fischer&rsquo;s lovebird, the species most hand reared in Bangladesh</span></div></div>
</section>
<section style="padding:0">
  <div class="wrap agrid">
    <aside class="toc">
      <span class="mh">In this guide</span>
      <a href="#before">Before the first feed</a><a href="#mix">Mixing the formula</a><a href="#schedule">Feeds per day, by age</a><a href="#crop">Reading the crop</a><a href="#mistakes">The two mistakes</a><a href="#weaning">Weaning</a><a href="#faq">Questions</a>
      <div class="tshare"><span class="mh">Share</span><div class="share"><a href="https://wa.me/?text=https://shadabirdfeed.com/blog/{slug}/" target="_blank" rel="noopener">{WA} WhatsApp</a><a href="https://www.facebook.com/sharer/sharer.php?u=https://shadabirdfeed.com/blog/{slug}/" target="_blank" rel="noopener">Facebook</a><button type="button" onclick="navigator.clipboard&&navigator.clipboard.writeText(location.href);this.textContent='Copied'">Copy link</button></div></div>
    </aside>
    <article class="abody">
      <p class="lead">A lovebird chick pulled at two weeks needs about three weeks of hand feeding. Most of what goes wrong happens in the first four days, and almost all of it comes down to two numbers: the temperature of the formula and the state of the crop before the next feed.</p>
      <h2 id="before">Before the first feed</h2>
      <p>Set up before you pull the chick, not after. You need a brooder or a box that holds a steady warm temperature, a small digital scale that reads in grams, a syringe or a bent spoon, a thermometer for the formula, and a jar of hand feeding formula with the batch date still readable on the lid.</p>
      <ul><li><strong>Warmth first.</strong> A cold chick will not digest. Warm the chick before you warm the food.</li><li><strong>Weigh every morning</strong> before the first feed, and write it down. Weight is the only honest signal you have.</li><li><strong>One clean syringe per chick</strong>, rinsed in hot water between feeds. Formula left in the syringe sours in an hour in Bangladeshi heat.</li></ul>
      <h2 id="mix">Mixing the formula</h2>
      <p>Mix a fresh batch for every feed. Never keep formula from one feed to the next, and never reheat it. Use water that has been boiled and cooled to hand-warm, then adjust to the target temperature with the thermometer, not with your finger.</p>
      <div class="callout"><b>The temperature rule</b>Feed at <strong>39 to 41&deg;C</strong>. Cooler than that and the crop slows; hotter and you burn the crop lining. Stir well and check the middle of the mix, not the edge.</div>
      <p>Consistency changes with age. For the first three days the mix should run off the spoon like a thin porridge. From day four, thicken it a little each day until, by the second week, it holds a soft peak. Follow the water-to-powder ratio printed on the jar and move within that range; a chick on a thin mix for too long fills up on water and stops gaining.</p>
      <a class="pcard" href="/products/nutricare-hand-feeding-formula/"><img src="@JL_nutricare@" alt=""><span><span class="eyebrow">The jar this guide uses</span><b>Nutricare Hand Feeding Formula</b><small>All-in-one, day one to weaning, for lovebird, conure, budgerigar, cockatiel, ringneck and rosella chicks. Sealed in Bhaluka.</small></span><span class="btn b-brand b-sm">View Nutricare {LK}</span></a>
      <h2 id="schedule">Feeds per day, by age</h2>
      <p>These are the routines breeders in our own room use. Treat them as a starting point and let the crop and the scale correct you.</p>
      <table><thead><tr><th>Age</th><th>Feeds</th><th>Mix</th><th>What to watch</th></tr></thead><tbody>
      <tr><td><b>Day 1 to 4</b></td><td>Every 2 to 3 hours, including one feed late at night</td><td>Thin porridge</td><td>Crop empties fully before each feed</td></tr>
      <tr><td><b>Day 5 to 14</b></td><td>Every 3 to 4 hours, no night feed once weight climbs daily</td><td>Thickening</td><td>Steady daily gain; pin feathers appear</td></tr>
      <tr><td><b>Week 3</b></td><td>4 feeds</td><td>Soft peak</td><td>Chick begins to refuse the last feed of the day</td></tr>
      <tr><td><b>Week 4 to 5</b></td><td>3 feeds, then 2</td><td>Soft peak</td><td>Pecking at soft food and Eggfood in the box</td></tr>
      <tr><td><b>Weaning</b></td><td>1 evening feed, then none</td><td>&nbsp;</td><td>Weight dips slightly then holds. Normal.</td></tr>
      </tbody></table>
      <h2 id="crop">Reading the crop</h2>
      <p>The crop is the soft pouch at the base of the neck. After a feed it should be full and rounded, not tight like a drum. Before the next feed it should be nearly flat. If it is still half full when the next feed is due, <strong>skip the feed</strong>, keep the chick warm, and check again in an hour. Feeding on top of a slow crop is how sour crop starts.</p>
      <p>Read <a href="/blog/crop-not-emptying/">Crop not emptying: what to do in the first hour</a> for the three causes in the order to check them.</p>
      <h2 id="mistakes">The two mistakes that lose chicks in week one</h2>
      <div class="callout warn"><b>1. Formula too cold, or fed onto a full crop</b>Both slow the crop. Slow crop turns to sour crop within a day in this climate. Temperature and an empty crop are the whole game in week one.</div>
      <div class="callout warn"><b>2. Feeding too fast</b>Formula that goes down the wrong way reaches the lungs. Feed in short pushes, from the left side of the beak towards the right, and stop the moment the chick stops the pumping motion. Slow is fast.</div>
      <h2 id="weaning">Weaning</h2>
      <p>From week four leave a shallow dish of soft food and a pinch of <a href="/products/avian-eggfood/">Eggfood</a> in the box during the day. The chick will play with it long before it eats it; that is the point. Drop the midday feed first, then the morning feed, and keep the evening feed until the chick refuses it two nights in a row. Expect a small weight dip at weaning and a recovery within the week. A dip that keeps going is a chick that is not eating, and the evening feed goes back on.</p>
      <p>A weaned lovebird on Nutricare through this whole routine uses roughly one 100g jar per chick. Two chicks, two jars; a clutch of four, the 500g jar is the cheaper buy. See <a href="/#ladder">pack prices per kilo</a>.</p>
      <div class="afaq" id="faq"><h2>Questions we get on WhatsApp</h2><div class="faqs">
        <details open><summary>Can I use a spoon instead of a syringe?<span class="pl"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></span></summary><div class="fa">Yes. A small spoon with the sides bent inward is safer for a beginner because the chick sets the pace. It is slower and messier, and that is fine.</div></details>
        <details><summary>The chick will not open its beak. What now?<span class="pl"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></span></summary><div class="fa">Check warmth first, then the crop. A cold chick or a full crop will not beg. Touch the side of the beak with the warm spoon; the feeding response usually follows.</div></details>
        <details><summary>How long does an open jar last?<span class="pl"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></span></summary><div class="fa">Keep the lid tight, the jar dry and out of the sun, and use the dry scoop only. In the monsoon buy the size you will finish in the season rather than the biggest size.</div></details>
      </div></div>
      <div class="author"><span class="av">SA</span><div><b>Shada aviary team, Bhaluka</b><p>Written by the breeders who rear the test clutches on every batch of Nutricare before it is sealed. Questions go to WhatsApp 01813-323535.</p></div></div>
      <div class="anext"><a href="/blog/opening-a-bird-shop/"><small>Previous</small><b>Opening a bird shop: the twenty SKUs that sell</b></a><a href="/blog/bird-food-price-in-bangladesh/"><small>Next</small><b>Bird food prices in Bangladesh, 2026</b></a></div>
    </article>
  </div>
</section>
<section class="tint bsec">
  <div class="wrap">
    <div class="bhead"><div><span class="eyebrow">Keep reading</span><h2 class="h-m" style="font-size:clamp(24px,2.6vw,34px)">More on hand rearing</h2></div><a class="link" href="/blog/category/hand-rearing/">All hand rearing guides {LK}</a></div>
    <div class="posts">
{related}
    </div>
  </div>
</section>
{CTA}'''
art_ld=json.dumps({"@context":"https://schema.org","@graph":[
 {"@type":"Article","headline":title,"description":ex,"datePublished":"2026-09-02","dateModified":"2026-09-02","author":{"@type":"Organization","name":"Shada Bird Feed"},"publisher":{"@type":"Organization","name":"Shada Bird Feed","url":"https://shadabirdfeed.com/"},"mainEntityOfPage":f"https://shadabirdfeed.com/blog/{slug}/"},
 {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://shadabirdfeed.com/"},{"@type":"ListItem","position":2,"name":"Guides","item":"https://shadabirdfeed.com/blog/"},{"@type":"ListItem","position":3,"name":cn,"item":f"https://shadabirdfeed.com/blog/category/{cat}/"},{"@type":"ListItem","position":4,"name":title}]},
 {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Can I use a spoon instead of a syringe?","acceptedAnswer":{"@type":"Answer","text":"Yes. A small spoon with the sides bent inward is safer for a beginner because the chick sets the pace."}},{"@type":"Question","name":"The chick will not open its beak. What now?","acceptedAnswer":{"@type":"Answer","text":"Check warmth first, then the crop. A cold chick or a full crop will not beg."}},{"@type":"Question","name":"How long does an open jar last?","acceptedAnswer":{"@type":"Answer","text":"Keep the lid tight, dry and out of the sun, use the dry scoop only, and in the monsoon buy the size you will finish in the season."}}]}]},ensure_ascii=False)
# ── 3. CATEGORY ──
ck='hand-rearing'; cn,bg,ac=CATS[ck]; cats_arts=[x for x in ARTS if x[1]==ck]
cgrid="\n".join(card(x) for x in cats_arts+[ARTS[8],ARTS[10]])
cl="".join(f'<a href="/blog/category/{k}/"><span style="color:var(--tx)">{n}</span><span>{sum(1 for a in ARTS if a[1]==k)}</span></a>' for k,(n,_,_) in CATS.items())
cat_body=f'''<section class="tint wing wing-l chero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><i></i><a href="/blog/">Guides</a><i></i><span>{cn}</span></nav>
    <div class="chero-grid">
      <div><span class="eyebrow" style="margin-top:22px">Topic</span><h1>{cn}.<br>Chicks, crops, weaning.</h1><p class="sub">Everything between pulling the chick and the day it eats on its own: temperatures, feeds per day, the crop, and the mistakes that cost a clutch. {len(cats_arts)+2} guides.</p></div>
      <div class="chero-art" style="--pa:{bg}"><img src="@B_lovebird@" alt=""></div>
    </div>
    {chips(ck)}
  </div>
</section>
<section class="bsec">
  <div class="wrap cgrid">
    <div>
      <div class="bhead"><div><h2 class="h-m" style="font-size:clamp(22px,2.4vw,30px)">{len(cats_arts)+2} guides on {cn.lower()}</h2></div><span style="font-size:13.5px;color:var(--tx2)">Newest first</span></div>
      <div class="posts">
{cgrid}
      </div>
      <div class="pager"><a class="on" href="/blog/category/{ck}/">1</a></div>
    </div>
    <aside class="side">
      <div class="sbox dark"><img src="@JL_nutricare@" alt=""><b>The jar for this topic</b><small>Nutricare, day one to weaning. From ৳130.</small><a class="btn b-white" style="width:100%" href="/products/nutricare-hand-feeding-formula/">View Nutricare</a></div>
      <div class="sbox"><span class="mh">All topics</span><div class="cl">{cl}</div></div>
      <div class="sbox"><span class="mh">Start with your bird</span><div class="cl">{"".join(f'<a href="/birds/{b}/"><span style="color:var(--tx)">{b.title()}</span><span>{LK}</span></a>' for b in ['lovebird','budgerigar','cockatiel','conure','ringneck','rosella'])}</div></div>
    </aside>
  </div>
</section>
{CTA}'''
pages={'blog-index.html':page('Guides · Shada Bird Feed','Short feeding guides written by breeders in Bhaluka: hand rearing, breeding, prices, supplements, species, wholesale.','/blog/',index_body),
       'blog-article.html':page(f'{title} · Shada Bird Feed',ex,f'/blog/{slug}/',article_body,art_ld),
       'blog-category.html':page(f'{cn} guides · Shada Bird Feed','Hand rearing guides: temperatures, feeds per day, the crop, weaning.',f'/blog/category/{ck}/',cat_body)}
# inline assets (same as build21)
uris=json.load(open('shada-assets/uris.json')); small=json.load(open('shada-assets/small.json'))
m={'nutricare':'Shada Nutricare Hand Feeding','eggfood':'Shada Avian Eggfood','herbs':'Shada Avian Herbs','spirulina':'Shada Avian Spirulina','moringa':'Shada Moringa Leaf Powder','beetroot':'Shada Beetroot Powder'}
birdsb={}
for n in ['lovebird','budgerigar','cockatiel','conure','ringneck','rosella']:
    im=Image.open(f'birds/{n}.png').convert('RGBA'); im.thumbnail((360,360)); o=io.BytesIO(); im.save(o,'WEBP',quality=82,method=6); birdsb[n]='data:image/webp;base64,'+base64.b64encode(o.getvalue()).decode()
white=open('shada-assets/logo-white.svg',encoding='utf-8').read(); white=re.sub(r'<\?xml[^>]*\?>','',white).strip(); white=re.sub(r'\s(width|height)="[^"]*"','',white,count=2)
fonts=open('/tmp/wf/fonts-inline.css').read(); keep=[b for b in fonts.split('\n') if "'Plus Jakarta Sans'" in b or "'Hind Siliguri'" in b]
os.makedirs('blog',exist_ok=True)
for fn,html in pages.items():
    t=html
    for k,alt in m.items(): t=t.replace('@JL_%s@'%k,uris[alt]).replace('@JS_%s@'%k,small[k])
    for n,u in birdsb.items(): t=t.replace('@B_%s@'%n,u)
    t=t.replace('@LOGO_DARK@',white.replace('rgb(100%, 100%, 100%)','#1D1D1F'))
    left=re.findall(r'@[A-Z_a-z]+@',t); assert not left,(fn,left)
    open(f'blog/{fn}','w',encoding='utf-8').write(t)
    a=t.replace('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600;700&display=swap" rel="stylesheet">','<style>:root{color-scheme:light}\n'+"\n".join(keep)+'</style>').replace('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>','')
    open(f'blog/{fn[:-5]}-artifact.html','w',encoding='utf-8').write(a)
    print(fn,round(len(t)/1024),'KB')
