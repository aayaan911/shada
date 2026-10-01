import re,json,base64,io,os
from PIL import Image
T=open('shada-v21-template.html',encoding='utf-8').read()
head_css=T[T.index('<style>'):T.index('</style>')+8]
import re as _re
shell_top=T[T.index('<div class="tick"'):T.index('<main id="main">')].replace('<div class="dh"><span class="logo">','<div class="dh"><span class="logo" aria-label="Shada Bird Feed">')
shell_top=_re.sub(r'href="#(?!\\b(?:main)\\b)', 'href="/#', shell_top)
footer=_re.sub(r'<svg(?![^>]*aria-hidden)',r'<svg aria-hidden="true"',_re.sub(r'href="#', 'href="/#', T[T.index('<footer>'):T.index('<script>')]))
shell_top=_re.sub(r'<svg(?![^>]*aria-hidden)', '<svg aria-hidden="true"', shell_top)
footer=_re.sub(r'<svg(?![^>]*aria-hidden)', '<svg aria-hidden="true"', footer)
script=T[T.index('<script>'):T.rindex('</script>')+9].replace("document.getElementById('ltabs').addEventListener(","const _lt=document.getElementById('ltabs');if(_lt)_lt.addEventListener(")
AR='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
LK='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
WA='<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5.3-.5c.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5 2.5 1 3 .8 3.6.7.5-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4ZM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>'
CK='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
I_SEAL='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="14" rx="3"/><path d="M8 7V5a4 4 0 0 1 8 0v2M12 12v4"/></svg>'
I_TRUCK='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>'
I_LEAF='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15zM5 19l8-8"/></svg>'
I_LIST='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6h13M8 12h13M8 18h9M3.5 6h.01M3.5 12h.01M3.5 18h.01"/></svg>'
I_SCALE='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M5 7h14M7 7l-3 7h6ZM17 7l-3 7h6Z"/></svg>'
PLUS='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>'
DL='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0 4-4m-4 4-4-4M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/></svg>'
I_CART='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/></svg>'
I_PRICE='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>'
HALO='<svg class="halo" viewBox="0 0 400 400" aria-hidden="true"><circle class="h1" cx="200" cy="200" r="120"/><circle class="h2" cx="200" cy="200" r="152"/><circle class="h3" cx="200" cy="200" r="186"/></svg>'
CATS={'hand-rearing':('Hand rearing','#089830','linear-gradient(180deg,#F5F5F3,#E6F4EA)'),'breeding':('Breeding','#B8871B','linear-gradient(180deg,#F5F5F3,#FBF3D6)'),'supplements':('Supplements','#8E1F35','linear-gradient(180deg,#F5F5F3,#FBE6EA)')}
def cat_of(k):
    """Any new category works: falls back to a readable name and the brand green."""
    return CATS.get(k,(k.replace('-',' ').capitalize(),'#089830','linear-gradient(180deg,#F5F5F3,#E6F4EA)'))
SKU={'nutricare':'NHF','eggfood':'AEF','herbs':'AHB','spirulina':'ASP','beetroot':'ABP','moringa':'AML'}
def sku_code(p): return p.get('sku') or SKU.get(p['k']) or p['k'][:3].upper()
P=[
 dict(k='nutricare',slug='nutricare-hand-feeding-formula',name='Nutricare Hand Feeding Formula',short='Nutricare',cat='hand-rearing',ac='#22B14C',role='All-in-one hand feeding formula, day one to weaning',packs=[('100g',130),('200g',240),('500g',485),('1kg',920)],birds=['lovebird','budgerigar','cockatiel','conure','ringneck','rosella'],tag='Hand rearing'),
 dict(k='eggfood',slug='avian-eggfood',name='Avian Eggfood',short='Eggfood',cat='breeding',ac='#123A72',role='Protein for the pair on the nest, ready to use',packs=[('100g',110),('200g',210),('500g',450),('1kg',870)],birds=['lovebird','budgerigar','cockatiel','ringneck','rosella'],tag='Breeding'),
 dict(k='spirulina',slug='avian-spirulina',name='Avian Spirulina',short='Spirulina',cat='supplements',ac='#1E5B2E',role='Immunity and deep feather colour, six weeks before a show',packs=[('50g',350),('100g',655),('200g',1275)],birds=['lovebird','conure','rosella'],tag='Colour and immunity'),
 dict(k='moringa',slug='avian-moringa-leaf-powder',name='Avian Moringa Leaf Powder',short='Moringa',cat='supplements',ac='#5A8F3C',role='Daily greens: iron, calcium and vitamins for every bird',packs=[('50g',125),('100g',205),('200g',370)],birds=['lovebird','budgerigar','cockatiel','conure','ringneck','rosella'],tag='Daily greens'),
 dict(k='beetroot',slug='avian-beetroot-powder',name='Avian Beetroot Powder',short='Beetroot',cat='supplements',ac='#8E1F35',role='Red factor and blood health through the moult',packs=[('50g',125),('100g',205),('200g',370)],birds=['conure','rosella'],tag='Red factor'),
 dict(k='herbs',slug='avian-herbs',name='Avian Herbs',short='Herbs',cat='supplements',ac='#2F4A3C',role='Fifty-plus herbs, seeds and bark for digestion and recovery',packs=[('50g',220),('100g',395),('200g',730)],birds=['lovebird','budgerigar','cockatiel','conure','ringneck','rosella'],tag='Digestion and recovery'),
]
fmt=lambda v:f"{v:,}"
def sku(p,s): return f"SBF-{sku_code(p)}-{1000 if s=='1kg' else int(s[:-1]):03d}"
def grams(s): return 1000 if s=='1kg' else int(s[:-1])
def perkg(p,g): return round(p*1000/g)
def pcard(p):
    cn,cac,bg=cat_of(p['cat'])
    sizes="".join(f'<span>{s}</span>' for s,_ in p['packs'])
    return f'''<a class="sp" href="/products/{p['slug']}/" style="--ac:{p['ac']}">
      <div class="spa"><span class="cat">{cn}</span><img src="@JL_{p['k']}@" alt="{p['name']}"></div>
      <div class="spb"><h3>{p['name']}</h3><p>{p['role']}</p><div class="sizes">{sizes}</div><div class="skufam"><span>SKU</span><code>SBF-{sku_code(p)}-</code><small>{" · ".join(str(1000 if s=="1kg" else int(s[:-1])).zfill(3) for s,_ in p['packs'])}</small></div>
        <div class="spm"><span class="price">from <b>৳{fmt(p['packs'][0][1])}</b><small>{p['packs'][0][0]}</small></span><span class="go">{AR}</span></div></div></a>'''
def chips(active='all',birds=False):
    out=f'<a class="cchip{" on" if active=="all" else ""}" href="/shop/">All products</a>'
    for k,(n,ac,bg) in CATS.items(): out+=f'<a class="cchip{" on" if active==k else ""}" href="/product-category/{k}/">{n}</a>'
    return f'<nav class="cchips" aria-label="Categories">{out}</nav>'
TRUST=f'''<div class="trust"><span>{CK}Sealed in Bhaluka, batch date on the lid</span><span>{CK}All 64 districts, 2 working days</span><span>{CK}Factory retail price, same in every district</span><span>{CK}Order on WhatsApp 01813-323535</span></div>'''
CTA=f'''<section class="brand wing final" style="overflow:hidden">
  <img class="avi" src="@B_lovebird@" alt="" style="--w:clamp(70px,9vw,130px);left:clamp(8px,4vw,80px);bottom:10%;--d:.4s">
  <img class="avi mirror" src="@B_conure@" alt="" style="--w:clamp(70px,9vw,130px);right:clamp(8px,4vw,80px);top:12%;--d:1.2s">
  <div class="wrap ctr"><span class="eyebrow">Not sure which jar?</span><h2 class="h-l">Send a photo of the bird.</h2><p class="sub" style="max-width:44ch;margin:0 auto 30px">A breeder replies on WhatsApp with the jar and the routine. No form, no wait.</p>
  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn b-white" href="https://wa.me/8801813323535" target="_blank" rel="noopener">{WA}&nbsp;Ask on WhatsApp</a><a class="btn b-line" href="/#plan">See the feeding plan</a></div></div>
</section>'''
CSS='''
/* ── shop system ── */
.shero{padding:clamp(52px,6.5vw,88px) 0 clamp(26px,3.5vw,44px)}
.shero h1{font-size:clamp(38px,5.6vw,68px);letter-spacing:-.04em;line-height:1.02;margin:12px 0 14px}
.shero .sub{max-width:52ch}
.shero-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:32px;align-items:end}
@media(max-width:800px){.shero-grid{grid-template-columns:1fr}}
.cchips{display:flex;gap:8px;flex-wrap:wrap;margin:26px 0 0}
.cchip{display:inline-flex;align-items:center;min-height:38px;padding:0 14px;border-radius:var(--r);border:1px solid var(--line);background:#fff;font-size:13.5px;font-weight:500;color:var(--tx);transition:border-color .15s,background .15s,color .15s}
.cchip:hover{border-color:var(--brand)} .cchip.on{background:var(--ink);border-color:var(--ink);color:#fff}
.bstats{display:flex;gap:22px;flex-wrap:wrap;justify-content:flex-end}
.bstats b{display:block;font-size:30px;font-weight:600;letter-spacing:-.04em;line-height:1;color:var(--brand-d)} .bstats span{font-size:13px;color:var(--tx2)}
@media(max-width:800px){.bstats{justify-content:flex-start}}
.bsec{padding:clamp(36px,4.5vw,64px) 0}
.bhead{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:22px;flex-wrap:wrap}
.trust{display:flex;gap:10px 26px;flex-wrap:wrap;font-size:13.5px;color:var(--tx2);padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.trust span{display:inline-flex;align-items:center;gap:8px} .trust svg{width:15px;height:15px;color:var(--brand)}
.sgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
@media(max-width:1000px){.sgrid{grid-template-columns:repeat(2,1fr)}} @media(max-width:560px){.sgrid{grid-template-columns:1fr}}
.sp{background:#fff;border:1px solid var(--line);border-radius:var(--r2);overflow:hidden;display:flex;flex-direction:column;transition:transform .35s var(--ease),box-shadow .35s var(--ease),border-color .25s}
.sp:hover{transform:translateY(-8px);box-shadow:0 26px 54px rgba(0,0,0,.09);border-color:var(--ac)}
.spa{position:relative;height:250px;display:grid;place-items:center;background:linear-gradient(180deg,#F5F5F3,#ECECE9);overflow:hidden}
.spa .halo{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.spa .halo circle{fill:none;stroke:var(--ac);transform-origin:200px 200px;stroke-opacity:.25}
.spa .halo .h1{stroke-width:1.5;stroke-dasharray:3 9;animation:spin 40s linear infinite} .spa .halo .h2{stroke-width:1;stroke-dasharray:1 7;animation:spin 60s linear infinite reverse} .spa .halo .h3{stroke-width:1;stroke-opacity:.14;stroke-dasharray:24 14;animation:spin 90s linear infinite}
.spa img{height:190px;width:auto;position:relative;filter:drop-shadow(0 18px 22px rgba(0,0,0,.16));transition:transform .5s var(--ease)} .sp:hover .spa img{transform:scale(1.05)}
.spa .cat{position:absolute;top:14px;left:14px;font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;background:rgba(255,255,255,.9);padding:5px 10px;border-radius:var(--r);color:var(--tx2);z-index:1}
.spb{padding:20px 22px 20px;flex:1;display:flex;flex-direction:column}
.sp h3{font-size:19px;line-height:1.25;letter-spacing:-.02em;margin-bottom:6px}
.sp p{font-size:14px;color:var(--tx2);line-height:1.5;margin-bottom:14px}
.sizes{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}
.skufam{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--tx2);margin-bottom:14px} .skufam span{font-weight:700;letter-spacing:.06em;font-size:10.5px} .skufam code{font-family:var(--ff);font-weight:600;color:var(--tx2);letter-spacing:.02em} .skufam small{font-size:12px}
.pk .o code{font-family:var(--ff);font-size:10.5px;font-weight:600;letter-spacing:.03em;color:var(--tx3);margin-top:3px}
.pk input:checked+.o code{color:var(--brand-d)}
.skurow{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:18px}
.skubar{display:inline-flex;align-items:center;gap:8px;padding:7px 8px 7px 11px;border-radius:var(--r);background:var(--ink);color:#fff}
.stock{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:500;color:var(--tx2)} .stock i{width:8px;height:8px;border-radius:50%;background:var(--brand);box-shadow:0 0 0 3px var(--brand-soft)}
.skubar .skul{font-size:10.5px;font-weight:700;letter-spacing:.1em;color:var(--leaf)} .skubar b{font-size:15px;font-weight:700;letter-spacing:.04em}
.skubar button{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;padding:5px 6px;border-radius:6px;background:rgba(255,255,255,.12);color:#fff;transition:background .2s} .skubar button svg{width:13px;height:13px} .skubar button:hover{background:rgba(255,255,255,.2)} .skubar button.ok{background:var(--brand)}
.stagechip{display:inline-flex;align-items:center;gap:9px;padding:8px 12px 8px 8px;border-radius:var(--r);border:1px solid var(--line);font-size:13px;margin:0 0 22px;transition:border-color .15s,background .15s}
.stagechip:hover{border-color:var(--brand);background:var(--brand-soft)} .stagechip i{font-style:normal;font-size:11px;font-weight:700;color:var(--brand);letter-spacing:.06em;background:var(--brand-soft);padding:4px 7px;border-radius:6px} .stagechip b{font-weight:600} .stagechip span{color:var(--tx2)} .stagechip svg{width:13px;height:13px;color:var(--brand)}
.pladder.wing{--wing-c:#fff;--wing-a:.08}
.lsku{display:block;font-family:var(--ff);font-size:10.5px;font-weight:600;letter-spacing:.04em;color:var(--on2);margin-top:6px} .lc.best .lsku{color:rgba(255,255,255,.85)} .sizes span{font-size:12px;font-weight:600;padding:4px 9px;border-radius:6px;background:var(--paper2);color:var(--tx2)}
.spm{margin-top:auto;display:flex;align-items:center;justify-content:space-between;padding-top:14px;border-top:1px solid var(--line)}
.spm .price{font-size:13.5px;color:var(--tx2)} .spm .price b{font-size:20px;font-weight:600;color:var(--tx);letter-spacing:-.02em;margin:0 4px 0 2px} .spm .price small{font-size:12px;color:var(--tx3)}
.spm .go{width:46px;height:28px;border-radius:var(--r);display:grid;place-items:center;border:1px solid var(--tx);color:var(--tx);transition:background .25s,color .25s,border-color .25s} .spm .go svg{width:17px;height:17px;transition:transform .35s var(--ease)}
.sp:hover .spm .go{background:var(--brand);border-color:var(--brand);color:#fff} .sp:hover .spm .go svg{transform:translateX(3px)}
.bystage{display:grid;grid-template-columns:repeat(3,1fr);gap:14px} @media(max-width:800px){.bystage{grid-template-columns:1fr}}
.bybird{display:grid;grid-template-columns:repeat(6,1fr);gap:10px} @media(max-width:900px){.bybird{grid-template-columns:repeat(3,1fr)}} @media(max-width:480px){.bybird{grid-template-columns:repeat(2,1fr)}}
.bb{display:flex;flex-direction:column;align-items:center;padding:16px 10px 14px;border-radius:var(--r2);background:#fff;border:1px solid var(--line);transition:transform .3s var(--ease),border-color .2s} .bb:hover{transform:translateY(-4px);border-color:var(--brand)} .bb img{width:72px;height:72px;object-fit:contain;margin-bottom:8px} .bb b{font-size:14px;font-weight:600}
.cgrid{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:clamp(24px,4vw,56px);align-items:start} @media(max-width:1000px){.cgrid{grid-template-columns:1fr}}
.cgrid .sgrid{grid-template-columns:repeat(2,1fr)} @media(max-width:600px){.cgrid .sgrid{grid-template-columns:1fr}}
.side{position:sticky;top:84px;display:grid;gap:14px} @media(max-width:1000px){.side{position:static}}
.sbox{border:1px solid var(--line);border-radius:var(--r2);padding:20px;background:#fff} .sbox .mh{display:block;margin-bottom:12px}
.sbox .cl a{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--line);font-size:14.5px} .sbox .cl a:last-child{border:0} .sbox .cl a:hover{color:var(--brand-d)} .sbox .cl span{color:var(--tx3);font-size:13px}
.sbox.dark{background:var(--ink);color:#fff;border-color:transparent}
.chero-art{width:clamp(180px,22vw,300px);height:clamp(180px,22vw,300px);border-radius:var(--r2);background:var(--pa);display:grid;place-items:center;position:relative;overflow:hidden;justify-self:end} .chero-art img{height:70%;animation:float 6s ease-in-out infinite;filter:drop-shadow(0 18px 22px rgba(0,0,0,.18))}
@media(max-width:800px){.chero-art{justify-self:start}}
.crumbs{display:flex;gap:9px;align-items:center;font-size:13px;color:var(--tx2);flex-wrap:wrap} .crumbs a:hover{color:var(--brand-d);text-decoration:underline;text-underline-offset:3px} .crumbs i{width:auto;height:auto;border-radius:0;background:none;font-style:normal;color:var(--tx3)} .crumbs i::before{content:"/"} .crumbs span:last-child{color:var(--tx);font-weight:500}
/* single product v3 (homepage language) */
.phero{padding:clamp(20px,3vw,36px) 0 0;overflow:visible;--ov:clamp(110px,13vw,200px)}
.pgrid{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(20px,3.5vw,48px);align-items:start;margin-top:22px;position:relative;z-index:2}
.pbox{background:#fff;border:1px solid var(--line);border-radius:var(--r2);box-shadow:0 30px 70px rgba(10,38,23,.14);padding:clamp(18px,2.4vw,32px)}
@media(max-width:900px){.pgrid{grid-template-columns:minmax(0,1fr)}}
.pright{padding:clamp(4px,1vw,12px) 0 0} .pright .h-xl{font-size:clamp(36px,4.6vw,58px);margin:10px 0 12px;letter-spacing:-.04em;line-height:1.02} .pright .h-xl .hl{color:var(--brand)}
.pright .sub{margin-bottom:18px;max-width:46ch;font-size:clamp(15px,1.4vw,18px)}
.pmain{position:relative;border-radius:var(--r2);background:var(--paper2);border:0;box-shadow:none;padding:clamp(16px,2vw,24px);height:100%;justify-content:center;display:flex;flex-direction:column;align-items:center;gap:14px}
.pmain .gjar{height:clamp(260px,26vw,380px);max-width:88%;object-fit:contain;margin:clamp(24px,3vw,40px) 0 6px;filter:drop-shadow(0 26px 30px rgba(0,0,0,.16))}
.pmain .gtag{position:absolute;top:14px;left:14px;display:flex;gap:6px} .pmain .gtag span{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;background:#fff;padding:5px 9px;border-radius:var(--r);color:var(--tx2)} .pmain .gtag span.b{background:var(--brand);color:#fff}
.pmain .gthumbs{grid-template-columns:repeat(5,minmax(0,1fr));width:100%;margin:0;gap:6px}
.pmain .gthumbs button{padding:6px;background:#fff}
@media(max-width:400px){.pmain .gthumbs{gap:4px}.pmain .gthumbs button{padding:4px}.pmain .gthumbs .ph{font-size:8.5px;line-height:1.15}} .pmain .gthumbs .ph{font-size:10px}
.buycard{background:#fff;border:0;border-top:1px solid var(--line);border-radius:0;padding:18px 0 0;box-shadow:none;position:relative;z-index:2}
.buycard .pblk{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:0 0 14px;border-top:0;border-bottom:1px solid var(--line);margin-bottom:14px}
.buycard .pnow{font-size:36px} .buycard .pnow small{margin-top:4px;font-size:13px}
.ticks{list-style:none;display:grid;gap:8px;margin:0 0 18px}
.ticks li{display:flex;align-items:flex-start;gap:9px;font-size:15.5px;line-height:1.4;color:var(--tx)}
.ticks svg{width:17px;height:17px;color:var(--brand);flex-shrink:0;margin-top:2px}
.eta{display:flex;align-items:center;gap:8px;font-size:13.5px;color:var(--tx2);margin:0 0 12px;padding:9px 12px;border-radius:var(--r);background:var(--paper2)}
.eta b{color:var(--tx);font-weight:600} .eta svg{width:15px;height:15px;color:var(--brand);flex-shrink:0}
.chips2.top{justify-content:flex-start;gap:10px;margin:0 0 18px}
.brow2{display:grid;grid-template-columns:auto 1fr 1fr;gap:10px;margin-top:4px}
@media(max-width:560px){.brow2{grid-template-columns:auto 1fr}.brow2 .b-wa{grid-column:1/-1}}
.brow2 .btn{min-height:54px;height:54px;font-size:15px;gap:8px;padding:0 12px;white-space:nowrap;line-height:1;flex-wrap:nowrap} .brow2 .btn svg{width:17px;height:17px;flex-shrink:0}
.b-wa,.b-line2{border:1.5px solid var(--brand);color:var(--brand-d);background:#fff} .b-wa:hover,.b-line2:hover{background:var(--brand-soft)}
.b-cart{margin:0} .b-wa{border:1.5px solid var(--brand);color:var(--brand-d);background:#fff} .b-wa:hover{background:var(--brand-soft)}
.phband{background:linear-gradient(180deg,var(--brand) 0%,#077A2A 100%);margin-top:calc(-1 * var(--ov));padding:calc(var(--ov) + clamp(28px,3.5vw,48px)) 0 clamp(40px,5vw,72px);color:#fff;--wing-c:#fff;--wing-a:.2;position:relative}
.phband .wrap{position:relative;z-index:1}
.phband .avi{width:var(--w)}
.factsrow{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:12px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:var(--r2);padding:16px 18px;backdrop-filter:blur(8px)}
.factsrow>div{display:grid;gap:6px;align-content:start;padding-right:12px;border-right:1px solid rgba(255,255,255,.16)} .factsrow>div:last-child{border-right:0}
.factsrow span{font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.7)} .factsrow b{font-size:13.5px;font-weight:500;color:#fff;line-height:1.35}
.factsrow .bf{display:flex;gap:4px;flex-wrap:wrap} .factsrow .bf a{display:inline-flex;align-items:center;gap:5px;min-height:32px;padding:3px 10px 3px 3px;border-radius:6px;background:rgba(255,255,255,.14);font-size:12px;font-weight:500;color:#fff} .factsrow .bf a:hover{background:#fff;color:var(--tx)} .factsrow .bf img{width:20px;height:20px;object-fit:contain}
.factsrow .stg{display:inline-flex;align-items:center;gap:6px} .factsrow .stg i{font-style:normal;font-size:11px;font-weight:700;color:var(--ink);background:var(--leaf);padding:2px 6px;border-radius:5px}
@media(max-width:900px){.factsrow{grid-template-columns:1fr 1fr}.factsrow>div{border-right:0;border-bottom:1px solid rgba(255,255,255,.16);padding-bottom:10px}.factsrow>div:nth-last-child(-n+2){border-bottom:0;padding-bottom:0}}
@media(max-width:520px){.factsrow{grid-template-columns:1fr}.factsrow>div{border-bottom:1px solid rgba(255,255,255,.16)!important;padding-bottom:10px!important}.factsrow>div:last-child{border-bottom:0!important}}
.pspecs{margin-top:clamp(24px,3vw,40px)}
.pspecs .spec b{font-size:clamp(34px,4.2vw,54px);white-space:nowrap}
.pspecs .spec span{font-size:15px;display:block;margin-bottom:6px}
.pspecs .spec i{font-size:13px;line-height:1.4;max-width:30ch;margin:0 auto} .pspecs .spec{padding:0 16px;border-left:1px solid rgba(255,255,255,.18)} .pspecs .spec:first-child{border-left:0} .pspecs .spec b{color:#fff;font-size:clamp(40px,5vw,64px)} .pspecs .spec b small{color:rgba(255,255,255,.7)} .pspecs .spec span{color:rgba(255,255,255,.9)} .pspecs .spec i{color:rgba(255,255,255,.6)}
@media(max-width:640px){.pspecs .spec{border-left:0;padding:0}}
@media(max-width:900px){.phero{--ov:80px}}
.fitbirds .bird{position:relative;text-align:left;padding:18px 14px 16px}
.fitbirds .bird img{max-width:120px}
.fitbirds .bf2{display:block;position:relative} .fitbirds .bf2 b{display:block;font-size:16px} .fitbirds .bf2 small{display:block;font-size:12px;color:var(--on2);margin-top:2px;line-height:1.3}
.fitbirds .ok{position:absolute;top:12px;right:12px;width:24px;height:24px;border-radius:6px;background:var(--brand);color:#fff;display:grid;place-items:center;z-index:2} .fitbirds .ok svg{width:13px;height:13px}
.fitbirds .bird.no{opacity:.5} .fitbirds .bird.no .ok{background:rgba(255,255,255,.14);color:var(--on2)} .fitbirds .bird.no img{filter:grayscale(.6)}
#does .why{margin-top:0}
.tlwrap{margin-top:18px;padding:22px 24px 18px;border-radius:var(--r2);background:var(--ink);color:#fff;--ac:var(--leaf)} .tlwrap .mh{display:block;color:var(--leaf);margin-bottom:4px} .tlwrap .tl{padding-top:22px} .tlwrap .tl span{color:var(--on2)} .tlwrap .tl span b{color:#fff} .tlwrap .tl .track{background:rgba(255,255,255,.14)} .tlwrap .tl .dot{box-shadow:0 0 0 4px var(--ink)}
.plan{--wing-a:.08}
.phead{display:grid;grid-template-columns:1.2fr 1fr;gap:clamp(20px,4vw,64px);align-items:end;margin-bottom:clamp(8px,1.5vw,20px)}
@media(max-width:800px){.phead{grid-template-columns:1fr}}
.phead .sub{max-width:42ch}
.pmap{position:relative;height:clamp(150px,18vw,230px)} .pmap svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.pguide{fill:none;stroke:var(--leaf);stroke-opacity:.2;stroke-width:1.5;stroke-dasharray:4 8;vector-effect:non-scaling-stroke}
.pline{fill:none;stroke:var(--leaf);stroke-width:2.5;stroke-linecap:round;vector-effect:non-scaling-stroke;stroke-dasharray:1000;stroke-dashoffset:1000;transition:stroke-dashoffset 2.4s var(--ease) .2s}
.pmap.in .pline{stroke-dashoffset:0}
.pnode .pulse{fill:none;stroke:var(--leaf);stroke-width:2;vector-effect:non-scaling-stroke;opacity:0}
.pnode.on .pulse{opacity:1}
.pnode .core{fill:var(--ink);stroke:var(--leaf);stroke-width:2.5;vector-effect:non-scaling-stroke}
.pnode.on .core{fill:var(--brand);stroke:#fff}
.pnode text{font-family:var(--ff);font-size:14px;font-weight:700;fill:#fff;text-anchor:middle}
.pbird{filter:drop-shadow(0 10px 14px rgba(0,0,0,.35))}
.pstages{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:8px}
@media(max-width:800px){.pstages{grid-template-columns:1fr}.pmap{display:none}}
.ps{position:relative;background:rgba(255,255,255,.05);border:1px solid var(--line-d);border-radius:var(--r2);padding:20px}
.ps.on{background:rgba(95,212,138,.1);border-color:rgba(95,212,138,.5)}
.youare{position:absolute;top:-9px;left:20px;font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:var(--leaf);color:var(--ink);padding:3px 8px;border-radius:6px}
.pt{display:inline-block;font-size:12px;font-weight:600;letter-spacing:.04em;color:var(--leaf);margin-bottom:8px}
.ps h3{font-size:22px;letter-spacing:-.025em;margin-bottom:12px}
.pjars{display:flex;flex-wrap:wrap;gap:6px}
.pj{display:inline-flex;align-items:center;gap:7px;padding:5px 11px 5px 5px;border-radius:var(--r);background:rgba(255,255,255,.07);border:1px solid var(--line-d);font-size:13px;font-weight:600;color:#fff;transition:background .25s,border-color .25s}
.pj:hover{background:var(--brand);border-color:var(--brand)} .pj.me{background:#fff;color:var(--tx);border-color:#fff}
.pj img{width:28px;height:28px;object-fit:contain;background:#fff;border-radius:6px;padding:2px}
.fingrid{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(28px,5vw,72px);align-items:center;position:relative;z-index:1}
@media(max-width:900px){.fingrid{grid-template-columns:1fr}}
.fintext h2{margin-bottom:22px}
.finticks{list-style:none;display:grid;gap:12px}
.finticks li{display:flex;align-items:flex-start;gap:11px;font-size:15.5px;line-height:1.45;color:rgba(255,255,255,.85)}
.finticks b{color:#fff;font-weight:600} .finticks svg{width:18px;height:18px;color:#fff;flex-shrink:0;margin-top:2px}
.fincard{background:#fff;border-radius:var(--r2);padding:22px;box-shadow:0 30px 70px rgba(0,0,0,.25);color:var(--tx)}
.fc-top{display:flex;align-items:center;gap:12px;padding-bottom:14px;border-bottom:1px solid var(--line);margin-bottom:4px}
.fc-top img{width:48px;height:48px;object-fit:contain} .fc-top b{display:block;font-size:15.5px;letter-spacing:-.01em;line-height:1.2} .fc-top small{font-size:12.5px;color:var(--tx2)}
.fc-row{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-size:14px;color:var(--tx2)}
.fc-row b{font-size:16px;font-weight:600;color:var(--tx)} .fc-row b.ok{color:var(--brand-d)}
.fincard .btn{width:100%;min-height:50px;margin-top:12px;gap:9px} .fincard .btn svg{width:17px;height:17px}
.b-line2{border:1.5px solid var(--brand);color:var(--brand-d);background:#fff;margin-top:8px!important} .b-line2:hover{background:var(--brand-soft)}
.fc-note{display:block;font-size:12.5px;color:var(--tx2);margin-top:12px;text-align:center}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:900px){.cols3{gap:12px}.c3b{padding:18px 16px 20px}.c3b h3{font-size:17px}.c3b p{font-size:13.5px}}
@media(max-width:640px){.cols3{grid-template-columns:1fr;gap:14px}.c3b{padding:22px}.c3b h3{font-size:19px}.c3b p{font-size:14.5px}}
.c3{background:#fff;border:1px solid var(--line);border-radius:var(--r2);overflow:hidden;display:flex;flex-direction:column;transition:transform .35s var(--ease),box-shadow .35s var(--ease),border-color .25s}
.c3:hover{transform:translateY(-6px);box-shadow:0 24px 50px rgba(10,38,23,.10);border-color:var(--brand)}
.c3i{position:relative;background:var(--zb);height:clamp(180px,17vw,215px);display:grid;place-items:center;overflow:hidden}
.c3i img{width:min(52%,150px);filter:drop-shadow(0 14px 18px rgba(0,0,0,.16));animation:hover 5.2s ease-in-out infinite;transition:transform .4s var(--ease)}
.c3:hover .c3i img{transform:scale(1.06) rotate(-3deg)}
.c3n{position:absolute;top:14px;left:14px;width:26px;height:26px;border-radius:8px;background:rgba(255,255,255,.9);display:grid;place-items:center;font-size:12px;font-weight:700;color:var(--tx2)}
.c3b{padding:22px 22px 24px;flex:1}
.c3b h3{font-size:19px;letter-spacing:-.02em;line-height:1.25;margin-bottom:8px}
.c3b p{font-size:14.5px;color:var(--tx2);line-height:1.55}
#fit .h-l,#details2 .h-l,#does .h-l,#howto .h-l,#faq .h-l,#plan .h-l,.pfin .h-l{font-size:clamp(30px,3.9vw,50px)}
.dwrap{max-width:900px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:var(--r2);box-shadow:0 20px 50px rgba(10,38,23,.08);overflow:hidden}
.link{min-height:30px}
.dtabs{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:4px;padding:6px;background:var(--paper2);border-bottom:1px solid var(--line)}
.dtab{display:inline-flex;align-items:center;justify-content:center;gap:8px;width:100%;min-width:0;padding:7px 8px;border-radius:var(--r);font-size:13px;font-weight:500;color:var(--tx2);min-height:50px;transition:background .2s,color .2s}
.dtab span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dtab i{width:34px;height:34px;border-radius:var(--r);background:#fff;display:grid;place-items:center;flex-shrink:0;transition:background .2s,color .2s} .dtab i svg{width:18px;height:18px}
.dtab:hover{color:var(--tx);background:rgba(255,255,255,.6)} .dtab:hover i{background:var(--brand-soft);color:var(--brand-d)}
.dtab.on{background:var(--ink);color:#fff;font-weight:600} .dtab.on i{background:var(--leaf);color:var(--ink)}
@media(max-width:900px){.dtabs{grid-template-columns:repeat(3,minmax(0,1fr))}.dtab{font-size:13.5px;justify-content:flex-start;padding:7px 10px 7px 7px}}
@media(max-width:640px){.dtabs{grid-template-columns:repeat(2,minmax(0,1fr))}.dtab{min-height:48px;font-size:13px}.dtab i{width:32px;height:32px}.dtab i svg{width:17px;height:17px}}
@media(max-width:600px){.pladder .lrow{grid-template-columns:1fr 1fr!important;gap:10px}
.pladder .lc{padding:20px 8px 12px} .pladder .lc img{height:56px} .ldrop{top:-9px;left:50%;transform:translate(-50%,0)} .lbest{top:6px}}
.dpanel{display:none;background:#fff;border:0;border-radius:0;box-shadow:none;max-width:none;margin:0;padding:clamp(22px,3vw,34px)}
.dpanel.on{display:block;animation:fade .35s var(--ease)}
.dpanel h3{font-size:clamp(20px,2vw,26px);letter-spacing:-.025em;margin-bottom:10px}
.dpanel p{font-size:16px;color:var(--tx2);line-height:1.6;max-width:70ch} .dpanel p+p{margin-top:12px} .dpanel p strong{color:var(--tx)}
.dpanel .dsub{font-size:14.5px;color:var(--tx2);margin-bottom:18px}
.dpanel .speclist{margin-top:4px}
.ing{display:grid;grid-template-columns:1fr 1.15fr;gap:14px} @media(max-width:800px){.ing{grid-template-columns:1fr}}
.ingc{background:var(--paper2);border-radius:var(--r2);padding:20px}
.ingc .mh{display:flex;align-items:center;gap:8px;margin-bottom:14px;color:var(--tx2)} .ingc .mh svg{width:16px;height:16px;color:var(--brand)}
.ingc .mh small{margin-left:auto;font-size:10.5px;font-weight:600;letter-spacing:.06em;color:var(--tx3)}
.chipset{display:flex;flex-wrap:wrap;gap:6px}
.ingchip{display:inline-flex;align-items:center;font-size:13px;font-weight:500;padding:6px 11px;border-radius:var(--r);background:#fff;border:1px solid var(--line);color:var(--tx)}
.ingnote{font-size:13px;color:var(--tx2);margin-top:12px;font-style:italic}
.agrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px} @media(max-width:520px){.agrid{grid-template-columns:1fr 1fr}}
.at{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:14px 12px;text-align:center}
.at b{display:block;font-size:22px;font-weight:600;letter-spacing:-.03em;color:var(--brand-d);line-height:1}
.at span{display:block;font-size:12px;color:var(--tx2);margin-top:5px;line-height:1.25}
.dlcards{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px} @media(max-width:600px){.dlcards{grid-template-columns:1fr}}
.dlc{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:var(--r2);border:1px solid var(--line);background:#fff;transition:border-color .2s,background .2s}
.dlc:hover{border-color:var(--brand);background:var(--brand-soft)}
.dlc i{width:40px;height:40px;border-radius:var(--r);background:var(--brand-soft);display:grid;place-items:center;flex-shrink:0} .dlc i svg{width:19px;height:19px;color:var(--brand-d)}
.dlc b{display:block;font-size:14.5px;font-weight:600} .dlc small{font-size:12.5px;color:var(--tx2)} .dlc svg:last-child{width:14px;height:14px;margin-left:auto;color:var(--brand);flex-shrink:0}
.ph{color:var(--tx3);font-weight:400;font-style:italic} .dpanel .cmp{box-shadow:none;max-width:none}
.acc{max-width:900px;margin:0 auto;border-top:1px solid var(--line)}
.acc details{border-bottom:1px solid var(--line);background:#fff}
.acc summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:20px 22px;font-size:clamp(16px,1.6vw,19px);font-weight:600;letter-spacing:-.01em}
.acc summary::-webkit-details-marker{display:none}
.acc summary .pl{width:28px;height:28px;border-radius:var(--r);background:var(--paper2);display:grid;place-items:center;flex-shrink:0;transition:transform .25s var(--ease),background .2s,color .2s} .acc summary .pl svg{width:12px;height:12px}
.acc details[open] summary .pl{transform:rotate(45deg);background:var(--ink);color:#fff}
.acc .fa{padding:0 22px 22px;font-size:16px;color:var(--tx2);line-height:1.6}
.acc .fa p{max-width:70ch} .acc .fa strong{color:var(--tx)}
.acc .speclist{margin-top:4px}
.kitbar{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-top:16px;padding:16px 20px;border-radius:var(--r2);background:var(--ink);color:#fff}
.kitbar .ke{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--leaf)}
.kitbar b{font-size:24px;letter-spacing:-.03em} .kitbar .kl{font-size:13.5px;color:var(--on2)} .kitbar .btn{margin-left:auto}
@media(max-width:600px){.kitbar .btn{margin-left:0;width:100%}}
.fsteps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
@media(max-width:1000px){.fsteps{grid-template-columns:1fr 1fr}} @media(max-width:520px){.fsteps{grid-template-columns:1fr}}
.fstep{background:rgba(255,255,255,.05);border:1px solid var(--line-d);border-radius:var(--r2);padding:22px 20px 20px;transition:background .3s,border-color .3s,transform .35s var(--ease)}
.fstep:hover{background:rgba(255,255,255,.08);border-color:rgba(95,212,138,.45);transform:translateY(-4px)}
.fk{display:block;font-size:12.5px;font-weight:600;letter-spacing:.04em;color:var(--leaf);margin-bottom:10px}
.fv{display:block;font-size:clamp(24px,2.4vw,32px);font-weight:600;letter-spacing:-.03em;line-height:1;color:#fff;margin-bottom:14px;padding-bottom:14px;border-bottom:1px solid var(--line-d)}
.fstep h3{font-size:17px;letter-spacing:-.015em;line-height:1.25;margin-bottom:6px;color:#fff}
.fstep p{font-size:14px;color:var(--on2);line-height:1.5}
.hgrid{display:grid;grid-template-columns:1.35fr .65fr;gap:16px;margin-top:16px;align-items:start} @media(max-width:800px){.hgrid{grid-template-columns:1fr}}
.fcard{background:#fff;border-radius:var(--r2);overflow:hidden;color:var(--tx)} .fcard .ftable{border:0} .fcard .ftable th{color:var(--tx2)} .fcard .ftable td{color:var(--tx)}
.tip{padding:22px;border-radius:var(--r2);background:rgba(95,212,138,.12);border:1px solid rgba(95,212,138,.3)} .tip b{display:block;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--leaf);margin-bottom:6px} .tip p{font-size:15px;line-height:1.5;margin-bottom:12px;color:var(--on)} .tip .link{color:var(--leaf)}
#compare .cmp{box-shadow:0 20px 50px rgba(10,38,23,.08)}
.vside.dark{background:var(--ink2);border-color:var(--line-d);color:#fff} .vside.dark ol{color:var(--on2)} .vside.dark .dl{border-color:var(--line-d)} .vside.dark .dl a{color:#fff} .vside.dark .dl a svg{color:var(--leaf)}
#faq .faqs{margin-top:0}
/* single product v2 */
.pd{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(28px,4.5vw,64px);align-items:start;padding:clamp(16px,2.5vw,32px) 0 clamp(40px,5vw,64px)}
@media(max-width:900px){.pd{grid-template-columns:minmax(0,1fr)}}
.gal{position:sticky;top:84px} @media(max-width:900px){.gal{position:static}}
.gmain{position:relative;border-radius:var(--r2);background:linear-gradient(180deg,#F7F7F5,#EDF5EF);min-height:clamp(320px,38vw,560px);display:grid;place-items:center;overflow:hidden;isolation:isolate;--wing-c:var(--brand);--wing-a:.06}
.gmain .gjar{height:min(76%,430px);max-width:80%;object-fit:contain;position:relative;z-index:1;filter:drop-shadow(0 30px 36px rgba(0,0,0,.18))}
.gmain .avi{z-index:2;height:auto;filter:drop-shadow(0 14px 18px rgba(0,0,0,.2))}
.gmain .gtag{position:absolute;top:16px;left:16px;z-index:2;display:flex;gap:6px}
.gmain .gtag span{font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;background:rgba(255,255,255,.92);padding:6px 10px;border-radius:var(--r);color:var(--tx2)} .gmain .gtag span.b{background:var(--brand);color:#fff}
.gthumbs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:10px}
.gthumbs button{aspect-ratio:1;min-width:0;overflow:hidden;border-radius:var(--r);background:var(--paper2);border:1px solid var(--line);display:grid;place-items:center;padding:8px;transition:border-color .15s} .gthumbs button.on,.gthumbs button:hover{border-color:var(--brand)} .gthumbs img{height:80%;width:auto;object-fit:contain} .gthumbs .ph{font-size:11px;color:var(--tx3);text-align:center;line-height:1.2}
.buy .cat{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ac);background:color-mix(in srgb,var(--ac) 12%,#fff);padding:5px 10px;border-radius:var(--r);margin:10px 0 12px}
.buy h1{font-size:clamp(30px,3.4vw,44px);letter-spacing:-.035em;line-height:1.06;margin-bottom:8px}
.buy .lede{font-size:clamp(17px,1.5vw,20px);color:var(--tx2);line-height:1.45;margin-bottom:20px}
.pblk{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;padding:16px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-bottom:18px}
.pnow{font-size:40px;font-weight:600;letter-spacing:-.045em;line-height:1} .pnow small{display:block;font-size:14px;font-weight:500;color:var(--tx2);letter-spacing:0;margin-top:6px}
.lbl{display:flex;justify-content:space-between;align-items:center;font-size:13px;font-weight:600;color:var(--tx2);margin-bottom:8px} .lbl a{color:var(--brand-d);font-weight:600;display:inline-flex;align-items:center;gap:4px;min-height:30px} .lbl a svg{width:12px;height:12px}
.pk{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
@media(max-width:560px){.pk{display:grid;grid-template-columns:1fr 1fr}.pk label{flex:none}}
.pk label{position:relative;cursor:pointer;flex:1 1 auto} .pk input{position:absolute;opacity:0;inset:0}
.pk .o{display:flex;flex-direction:column;align-items:center;gap:1px;padding:10px 12px;border-radius:var(--r);border:1.5px solid var(--line);background:#fff;transition:border-color .15s,background .15s;text-align:center;min-width:76px}
.pk .o b{font-size:15px;font-weight:600} .pk .o span{font-size:13px;color:var(--tx2)}
.pk .o .bv{position:absolute;top:-9px;left:50%;transform:translateX(-50%);font-size:9.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;background:var(--brand);color:#fff;padding:2px 7px;border-radius:5px;white-space:nowrap}
.pk input:checked+.o{border-color:var(--brand);background:var(--brand-soft)} .pk input:checked+.o span{color:var(--brand-d)} .pk input:focus-visible+.o{outline:2px solid var(--brand);outline-offset:2px}
.chips2{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:18px}
.skubar{display:inline-flex;align-items:center;gap:8px;padding:7px 8px 7px 11px;border-radius:var(--r);background:var(--ink);color:#fff}
.skubar .skul{font-size:10.5px;font-weight:700;letter-spacing:.1em;color:var(--leaf)} .skubar b{font-size:14px;font-weight:700;letter-spacing:.04em}
.skubar button{display:inline-flex;align-items:center;justify-content:center;gap:5px;font-size:12px;font-weight:600;min-width:30px;min-height:30px;padding:4px 7px;border-radius:6px;background:rgba(255,255,255,.12);color:#fff;transition:background .2s} .skubar button svg{width:13px;height:13px} .skubar button:hover{background:rgba(255,255,255,.2)} .skubar button.ok{background:var(--brand)}
.stockchip{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:var(--r);font-size:13px;font-weight:600;background:var(--brand-soft);color:var(--brand-d)} .stockchip i{width:8px;height:8px;border-radius:50%;background:var(--brand)}
.stockchip.out{background:#FBE6EA;color:#8E1F35} .stockchip.out i{background:#8E1F35}
.brow{display:grid;grid-template-columns:auto 1fr;gap:10px;margin-bottom:10px}
.qty{display:inline-flex;align-items:center;border:1.5px solid var(--line);border-radius:var(--r);overflow:hidden;height:54px} .qty button{width:44px;height:100%;font-size:20px;color:var(--tx)} .qty button:hover{background:var(--paper2)} .qty output{min-width:44px;text-align:center;font-weight:600;font-size:16px;border-left:1.5px solid var(--line);border-right:1.5px solid var(--line);height:100%;display:grid;place-items:center}
.brow .btn{min-height:54px;font-size:16px;gap:9px} .brow .btn svg{width:18px;height:18px}
.b-cart{width:100%;min-height:48px;font-size:15px;margin-bottom:18px}
.bnote{font-size:13px;color:var(--tx2);display:grid;gap:6px} .bnote span{display:flex;align-items:center;gap:8px} .bnote svg{width:14px;height:14px;color:var(--brand);flex-shrink:0}
.trust3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:22px}
.trust3 div{display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;padding:12px 8px;border-radius:var(--r);background:var(--paper2);font-size:12.5px;line-height:1.3;color:var(--tx2)} .trust3 svg{width:20px;height:20px;color:var(--brand)} .trust3 b{color:var(--tx);font-weight:600;font-size:13px}
@media(max-width:480px){.trust3{grid-template-columns:1fr 1fr 1fr;gap:6px}.trust3 div{padding:10px 4px;font-size:11.5px}}
.facts{border:1px solid var(--line);border-radius:var(--r2);overflow:hidden;font-size:14px}
.facts div{display:grid;grid-template-columns:120px 1fr;gap:12px;padding:11px 14px;border-bottom:1px solid var(--line);align-items:center} .facts div:last-child{border:0} .facts span{font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--tx3)} .facts b{font-weight:500;color:var(--tx)}
.facts .bf{display:flex;gap:4px;flex-wrap:wrap} .facts .bf a{display:inline-flex;align-items:center;gap:5px;padding:3px 8px 3px 3px;border-radius:6px;border:1px solid var(--line);font-size:12.5px;font-weight:500} .facts .bf a:hover{border-color:var(--brand)} .facts .bf img{width:22px;height:22px;object-fit:contain}
.facts .stg{display:inline-flex;align-items:center;gap:6px} .facts .stg i{font-style:normal;font-size:11px;font-weight:700;color:var(--brand);background:var(--brand-soft);padding:2px 6px;border-radius:5px}
@media(max-width:480px){.facts div{grid-template-columns:1fr;gap:4px}}
/* sticky summary bar */
.sbar{position:fixed;left:0;right:0;top:64px;z-index:250;background:rgba(255,255,255,.94);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line);transform:translateY(-110%);transition:transform .3s var(--ease)}
.sbar.on{transform:none}
.sbar .wrap{display:flex;align-items:center;gap:14px;padding-top:10px;padding-bottom:10px}
.sbar img{width:44px;height:44px;object-fit:contain} .sbar .sn{flex:1;min-width:0} .sbar .sn b{display:block;font-size:15px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis} .sbar .sn small{font-size:12.5px;color:var(--tx2)}
.sbar .sp2{font-size:20px;font-weight:600;letter-spacing:-.03em;white-space:nowrap} .sbar .btn{min-height:44px;padding:0 18px;gap:8px} .sbar .btn svg{width:16px;height:16px}

/* sections */
.ptabs{display:flex;gap:4px;border-bottom:1px solid var(--line);margin-bottom:clamp(28px,3.5vw,44px);overflow-x:auto;scrollbar-width:none} .ptabs a{white-space:nowrap;padding:12px 14px;font-size:14px;font-weight:600;color:var(--tx2);border-bottom:2px solid transparent;margin-bottom:-1px} .ptabs a:hover,.ptabs a.on{color:var(--tx);border-color:var(--brand)}
.pblock{scroll-margin-top:130px}
.pblock h2{font-size:clamp(26px,2.8vw,38px);letter-spacing:-.03em;line-height:1.1;margin-bottom:10px} .pblock .sub{font-size:17px;margin-bottom:24px;max-width:62ch}
.pblock+.pblock{margin-top:clamp(48px,6vw,80px)}
.fit{display:grid;grid-template-columns:repeat(6,1fr);gap:10px} @media(max-width:900px){.fit{grid-template-columns:repeat(3,1fr)}} @media(max-width:480px){.fit{grid-template-columns:repeat(2,1fr)}}
.fb{display:flex;flex-direction:column;align-items:center;text-align:center;padding:16px 10px 14px;border-radius:var(--r2);background:#fff;border:1px solid var(--line);position:relative} .fb img{width:70px;height:70px;object-fit:contain;margin-bottom:8px} .fb b{font-size:14.5px;font-weight:600} .fb small{font-size:12px;color:var(--tx2);line-height:1.3;margin-top:3px}
.fb .ok{position:absolute;top:10px;right:10px;width:22px;height:22px;border-radius:6px;background:var(--brand);color:#fff;display:grid;place-items:center} .fb .ok svg{width:12px;height:12px}
.fb.no{opacity:.55} .fb.no .ok{background:var(--paper3);color:var(--tx3)}
.does{display:grid;grid-template-columns:repeat(3,1fr);gap:14px} @media(max-width:800px){.does{grid-template-columns:1fr}}
.does div{padding:22px;border-radius:var(--r2);background:#fff;border:1px solid var(--line)} .does .wyi{margin-bottom:14px} .does b{display:block;font-size:17px;margin-bottom:6px;letter-spacing:-.01em} .does p{font-size:14.5px;color:var(--tx2);line-height:1.5}
.tlwrap{margin-top:22px;padding:22px 24px 18px;border-radius:var(--r2);background:var(--ink);color:#fff;--ac:var(--leaf)} .tlwrap .mh{display:block;color:var(--leaf);margin-bottom:4px} .tlwrap .tl{padding-top:22px} .tlwrap .tl span{color:var(--on2)} .tlwrap .tl span b{color:#fff} .tlwrap .tl .track{background:rgba(255,255,255,.14)} .tlwrap .tl .dot{box-shadow:0 0 0 4px var(--ink)}
.howto{display:grid;grid-template-columns:1fr 1fr;gap:20px} @media(max-width:900px){.howto{grid-template-columns:1fr}}
.rail4{position:relative;display:grid;gap:14px;padding-left:4px} .rail4::before{content:'';position:absolute;left:21px;top:20px;bottom:20px;width:2px;background:var(--line)}
.rail4>div{display:grid;grid-template-columns:36px 1fr;gap:14px;align-items:start;position:relative} .rail4 i{width:36px;height:36px;border-radius:var(--r);background:var(--brand);color:#fff;display:grid;place-items:center;font-style:normal;font-weight:700;font-size:14px;box-shadow:0 0 0 4px var(--paper2)} .rail4 b{display:block;font-size:16px;margin:6px 0 3px} .rail4 p{font-size:14.5px;color:var(--tx2);line-height:1.5}
.ftable{width:100%;border-collapse:separate;border-spacing:0;font-size:14.5px;border:1px solid var(--line);border-radius:var(--r2);overflow:hidden;background:#fff}
.ftable th,.ftable td{padding:12px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top} .ftable th{background:var(--paper2);font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--tx2)} .ftable tr:last-child td{border-bottom:0} .ftable td b{font-weight:600}
.size{display:grid;grid-template-columns:.9fr 1.1fr;gap:16px;align-items:stretch} @media(max-width:900px){.size{grid-template-columns:1fr}}
.calc{padding:22px;border-radius:var(--r2);background:#fff;border:1px solid var(--line);display:flex;flex-direction:column;gap:14px}
.calc label{display:block;font-size:12.5px;font-weight:600;color:var(--tx2);margin-bottom:6px}
.calcout{padding:14px 16px;border-radius:var(--r);background:var(--brand-soft)} .lbl2{display:block;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--brand-d)} .calcout b{display:block;font-size:24px;letter-spacing:-.02em;margin:2px 0} .calcout small{font-size:13.5px;color:var(--tx2)}
.calc .note{font-size:12px;color:var(--tx3);margin-top:auto}
.pladder{background:var(--ink);color:#fff;border-radius:var(--r2);padding:clamp(18px,2.4vw,28px)} .pladder .mh{display:block;color:var(--leaf);margin-bottom:12px}
.pladder .lrow{gap:8px} .pladder .lc{padding:18px 8px 12px} .pladder .lc img{height:64px}
.pladder.wing{--wing-c:#fff;--wing-a:.08}
.video{display:grid;grid-template-columns:1.2fr .8fr;gap:18px} @media(max-width:800px){.video{grid-template-columns:1fr}}
.vthumb{position:relative;display:grid;place-items:center;min-height:300px;border-radius:var(--r2);background:var(--ink2);border:1px solid var(--line-d);overflow:hidden} .vthumb img{height:180px;opacity:.55;filter:blur(1px)}
.play{position:absolute;width:72px;height:72px;border-radius:50%;background:#fff;color:var(--ink);display:grid;place-items:center;box-shadow:0 20px 40px rgba(0,0,0,.35);transition:transform .3s var(--ease)} .play svg{width:30px;height:30px;margin-left:4px} .vthumb:hover .play{transform:scale(1.08)}
.vcap{position:absolute;bottom:14px;left:16px;right:16px;font-size:12.5px;color:var(--on2)}
.vside{padding:20px 22px;border-radius:var(--r2);background:#fff;border:1px solid var(--line)} .vside b{display:block;font-size:16px;margin-bottom:8px} .vside ol{padding-left:1.2em;font-size:14.5px;color:var(--tx2);line-height:1.5} .vside li+li{margin-top:4px}
.dlrow{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:16px;font-size:14px} .dlrow .mh{margin:0} .dlrow a{display:inline-flex;align-items:center;gap:8px;font-weight:500} .dlrow a svg{width:15px;height:15px;color:var(--brand)} .dlrow small{font-size:12px}
.dl{margin-top:18px;padding-top:14px;border-top:1px solid var(--line)} .dl .mh{display:block;margin-bottom:8px} .dl a{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:500;padding:7px 0} .dl a svg{width:16px;height:16px;color:var(--brand)} .dl a small{margin-left:auto;font-size:12px}
.speclist{display:grid;grid-template-columns:1fr 1fr;gap:18px} @media(max-width:800px){.speclist{grid-template-columns:1fr}} .speclist .ftable td:last-child{text-align:right;font-weight:600}
.ph{color:var(--tx3);font-weight:400!important;font-style:italic}
.cmp2 .cmp{max-width:none;box-shadow:none}
.bundle{display:grid;grid-template-columns:auto auto auto auto auto 1fr;gap:12px;align-items:center;padding:20px 22px;border-radius:var(--r2);background:#fff;border:1px solid var(--line)}
@media(max-width:900px){.bundle{grid-template-columns:1fr;text-align:center}.plus{display:none}}
.bi{display:flex;flex-direction:column;align-items:center;text-align:center;padding:8px 14px;border-radius:var(--r);transition:background .15s} .bi:hover{background:var(--paper2)} .bi img{width:74px;height:74px;object-fit:contain} .bi b{font-size:14px;font-weight:600;margin-top:4px} .bi small{font-size:12.5px;color:var(--tx2)}
.plus{font-size:24px;color:var(--tx3);font-weight:300}
.btot{justify-self:end;text-align:right;display:grid;gap:4px;justify-items:end} .btot span{font-size:12.5px;color:var(--tx2)} .btot b{font-size:26px;letter-spacing:-.03em;line-height:1}
@media(max-width:900px){.btot{justify-self:center;justify-items:center;text-align:center;padding-top:12px;border-top:1px solid var(--line)}}
.dealers{display:grid;grid-template-columns:1fr 1fr;gap:16px} @media(max-width:800px){.dealers{grid-template-columns:1fr}}
.dd{padding:22px;border-radius:var(--r2);background:#fff;border:1px solid var(--line)} .dd b{display:block;font-size:17px;margin-bottom:6px} .dd p{font-size:14.5px;color:var(--tx2);line-height:1.5;margin-bottom:14px}
.dsearch{display:flex;align-items:center;gap:10px;flex-wrap:wrap} .dsearch input{flex:1;min-width:200px;min-height:46px;padding:0 14px;border:1.5px solid var(--line);border-radius:var(--r);font:inherit;font-size:15px} .dsearch input:focus{outline:0;border-color:var(--brand)} .dsearch .ph{font-size:12px}
.rev{display:grid;grid-template-columns:280px 1fr;gap:24px;align-items:start} @media(max-width:800px){.rev{grid-template-columns:1fr}}
.revs{padding:22px;border-radius:var(--r2);background:var(--paper2);text-align:center} .revs b{display:block;font-size:44px;font-weight:600;letter-spacing:-.04em;line-height:1} .revs small{display:block;color:var(--tx2);font-size:13.5px;margin-top:6px}
.revempty{padding:28px;border:1.5px dashed var(--paper3);border-radius:var(--r2);text-align:center;color:var(--tx2);font-size:15px} .revempty b{display:block;color:var(--tx);font-size:17px;margin-bottom:6px}
'''
def page(title,desc,path,body,ld=''):
    ldt=f'<script type="application/ld+json">{ld}</script>' if ld else ''
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
{ldt}
{head_css.replace('</style>',CSS+'</style>')}
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
BIRDS=['lovebird','budgerigar','cockatiel','conure','ringneck','rosella']
# ── SHOP ──
shop_body=f'''<section class="tint wing wing-l shero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><i></i><span>Shop</span></nav>
    <div class="shero-grid">
      <div><span class="eyebrow" style="margin-top:22px">Shop</span><h1>Six formulas.<br>Twenty pack sizes.</h1><p class="sub">Every jar formulated, milled and sealed in Bhaluka. Every price is the factory retail price, the same in all 64 districts.</p></div>
      <div class="bstats"><div><b>6</b><span>formulas</span></div><div><b>20</b><span>pack sizes</span></div><div><b>৳110</b><span>first jar</span></div></div>
    </div>
    {chips('all')}
  </div>
</section>
<section class="bsec" style="padding-top:20px">
  <div class="wrap">
    <div class="bhead"><div><h2 class="h-m" style="font-size:clamp(24px,2.6vw,34px)">All products</h2></div><span style="font-size:13.5px;color:var(--tx2)">Showing 6 of 6</span></div>
    <div class="sgrid">
{chr(10).join(pcard(p) for p in P)}
    </div>
  </div>
</section>
<section class="tint bsec">
  <div class="wrap">
    <div class="bhead"><div><span class="eyebrow">Shop by stage</span><h2 class="h-m" style="font-size:clamp(24px,2.6vw,34px)">Hatch, grow, thrive.</h2></div><a class="link" href="/#plan">See the plan {LK}</a></div>
    <div class="bystage">
      <a class="sbox" href="/product-category/hand-rearing/" style="display:block"><span class="mh" style="color:var(--brand)">01 · Hatch</span><b style="display:block;font-size:18px;margin-bottom:4px">Day 1 to weaning</b><small style="color:var(--tx2);font-size:13.5px">Nutricare</small></a>
      <a class="sbox" href="/product-category/breeding/" style="display:block"><span class="mh" style="color:#B8871B">02 · Grow</span><b style="display:block;font-size:18px;margin-bottom:4px">Pairing to moult</b><small style="color:var(--tx2);font-size:13.5px">Eggfood · Moringa</small></a>
      <a class="sbox" href="/product-category/supplements/" style="display:block"><span class="mh" style="color:#8E1F35">03 · Thrive</span><b style="display:block;font-size:18px;margin-bottom:4px">Show season and recovery</b><small style="color:var(--tx2);font-size:13.5px">Spirulina · Beetroot · Herbs</small></a>
    </div>
    <div class="bhead" style="margin-top:44px"><div><span class="eyebrow">Shop by bird</span><h2 class="h-m" style="font-size:clamp(24px,2.6vw,34px)">Start with your bird.</h2></div></div>
    <div class="bybird">{"".join(f'<a class="bb" href="/birds/{b}/"><img src="@B_{b}@" alt=""><b>{b.title()}</b></a>' for b in BIRDS)}</div>
  </div>
</section>
<section class="bsec">
  <div class="wrap">
    <div class="deal dark feather" style="grid-template-columns:1fr;padding:clamp(28px,4vw,48px)">
      <div style="display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center;flex-wrap:wrap">
        <div><span class="eyebrow">Wholesale</span><h2 class="h-m" style="font-size:clamp(24px,2.6vw,34px);margin:6px 0 8px">Twenty SKUs, one supplier.</h2><p style="color:var(--on2);max-width:52ch;font-size:15.5px">Dealer pricing from 10kg, shipped in the same two working days. Ask for the price list on WhatsApp.</p></div>
        <a class="btn b-brand" href="/#wholesale">Apply on WhatsApp {LK}</a>
      </div>
    </div>
  </div>
</section>
{CTA}'''
# ── CATEGORY (one function, every category) ──
CATCOPY={'supplements':('One pinch a day.','Four jars that change what you can see: colour, red, recovery, daily greens. Over soft food, Eggfood or in the water. Fifty-gram jars, so the first one is a trial.',
   'spirulina','How to use','Over soft food, or in the water.','One pinch per bird per day. Mix into Eggfood or soft food so the bird cannot sort it out. In the drinking water, change the water daily.',
   [('What you can see','The pinch','The routine'),[('Dull feather, show in six weeks','Spirulina','A pinch daily, six weeks before the show'),('Pale red on a conure or rosella','Beetroot','Daily through the moult'),('Loose droppings, slow recovery','Herbs','Daily until back on form, then twice a week'),('Every bird, every day','Moringa','A pinch in every bowl, all year')]],
   [('Spirulina: how much, how often','/blog/spirulina-for-birds/'),('Red factor through the moult','/blog/red-factor-beetroot/'),('Moringa: the daily pinch','/blog/moringa-daily-pinch/')]),
 'hand-rearing':('Day one to weaning.','Everything between pulling the chick and the day it eats on its own. One formula the whole way, mixed with warm water and fed by syringe or spoon.',
   'nutricare','How to feed','Warm the chick, then the food.','Feed at 39 to 41&deg;C, mix fresh every feed, and never feed on top of a crop that has not emptied. Weigh every morning before the first feed.',
   [('Age','Feeds','Mix'),[('Day 1 to 4','Every 2 to 3 hours, one late feed','Thin porridge'),('Day 5 to 14','Every 3 to 4 hours','Thickening'),('Week 3','4 feeds','Soft peak'),('Week 4 to 5','3, then 2 feeds','Soft peak'),('Weaning','1 evening feed, then none','Soft food + Eggfood')]],
   [('How to hand feed a lovebird chick','/blog/hand-feeding-lovebird-chicks/'),('Crop not emptying: the first hour','/blog/crop-not-emptying/'),('Budgerigar chicks: when to pull','/blog/budgerigar-chicks-when-to-pull/')]),
 'breeding':('Pairing to moult.','Protein for the pair on the nest and the daily green that goes in every bowl. Daily through the season, twice a week the rest of the year.',
   'eggfood','How to use','A spoon in the cup, every morning.','Fresh each morning, remove what is left in the evening. Parents with chicks will empty the cup by noon. Loose droppings mean too much; cut back.',
   [('Stage','How often','How much'),[('Pairing','Daily','1 spoon per pair'),('Laying','Daily','1 spoon per pair'),('Chicks in nest','Daily, refill if empty','2 spoons per pair'),('Moult','Daily','1 spoon per pair'),('Off season','Twice a week','1 spoon per pair')]],
   [('Eggfood through the season','/blog/eggfood-through-the-season/'),('Setting up a lovebird pair','/blog/first-clutch-lovebird-pair/'),('Moringa: the daily pinch','/blog/moringa-daily-pinch/')])}
def category_page(ck):
    cn,cac,cbg=cat_of(ck); cp=[p for p in P if p['cat']==ck]
    h2,sub,hero,htitle,hh2,hsub,(cols,rows),guides=CATCOPY[ck]
    cgrid="\n".join(pcard(p) for p in sorted(cp,key=lambda p:p['packs'][0][1]))
    cl="".join(f'<a href="/product-category/{k}/"><span style="color:var(--tx)">{cat_of(k)[0]}</span><span>{sum(1 for p in P if p["cat"]==k)}</span></a>' for k in CATS)
    rw="".join('<tr>'+"".join(f'<td>{"<b>"+c+"</b>" if j==0 else c}</td>' for j,c in enumerate(r))+'</tr>' for r in rows)
    gl="".join(f'<a href="{u}"><span style="color:var(--tx)">{t}</span><span>{LK}</span></a>' for t,u in guides)
    body=f'''<section class="tint wing wing-l shero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><i></i><a href="/shop/">Shop</a><i></i><span>{cn}</span></nav>
    <div class="shero-grid">
      <div><span class="eyebrow" style="margin-top:22px">Category</span><h1>{cn}.<br>{h2}</h1><p class="sub">{sub}</p></div>
      <div class="chero-art" style="--pa:{cbg}"><img src="@JL_{hero}@" alt=""></div>
    </div>
    {chips(ck)}
  </div>
</section>
<section class="bsec" style="padding-top:20px">
  <div class="wrap cgrid">
    <div>
      <div class="bhead"><div><h2 class="h-m" style="font-size:clamp(22px,2.4vw,30px)">{len(cp)} product{"s" if len(cp)!=1 else ""} in {cn.lower()}</h2></div><span style="font-size:13.5px;color:var(--tx2)">Price, low to high</span></div>
      <div class="sgrid">
{cgrid}
      </div>
      <div class="pblock" style="margin-top:44px"><h2>{hh2}</h2><p class="sub">{hsub}</p>
      <table class="ftable"><thead><tr>{"".join(f"<th>{c}</th>" for c in cols)}</tr></thead><tbody>{rw}</tbody></table></div>
    </div>
    <aside class="side">
      <div class="sbox dark"><span class="eyebrow">{htitle}</span><b style="display:block;font-size:18px;letter-spacing:-.02em;margin-bottom:8px">{hh2}</b><p style="font-size:14px;color:var(--on2);line-height:1.5">{hsub}</p></div>
      <div class="sbox"><span class="mh">All categories</span><div class="cl">{cl}</div></div>
      <div class="sbox"><span class="mh">Guides on {cn.lower()}</span><div class="cl">{gl}</div></div>
    </aside>
  </div>
</section>
{CTA}'''
    return page(f"{cn} \u00b7 Shada Bird Feed",sub[:150],f"/product-category/{ck}/",body)

# ── SINGLE PRODUCT (global template, one function for all) ──

GRAD=['linear-gradient(145deg,#E6F4EA,#C9E8D2)','linear-gradient(145deg,#F5F5F3,#E4E4DF)','linear-gradient(145deg,#FBF3D6,#F2E2A8)','linear-gradient(145deg,#EAF3DF,#CFE5B6)','linear-gradient(145deg,#FBE6EA,#F3C3CF)','linear-gradient(145deg,#E8EEF9,#C9D7F0)']
def auto_strip(p,C):
    """The three green-band numbers, computed from the verified price master."""
    g=lambda s:1000 if s=='1kg' else int(s[:-1])
    best=p['packs'][-1]; first=p['packs'][0]
    bg=g(best[0]); per_g=best[1]/bg
    unit=C.get('gpu',100); one=C.get('unitone','bird')
    cost=round(per_g*unit)
    n=int(bg//unit)
    save=round((first[1]/g(first[0])-per_g)/(first[1]/g(first[0]))*100)
    kg_best=round(per_g*1000); kg_first=round(first[1]/g(first[0])*1000)
    return [(f"৳{cost:,}",f"per {one}",f"from the {best[0]} jar at about {unit}g per {one}"),
            (f"{n} {one}s" if n>1 else f"1 {one}",f"on one {best[0]} jar",f"about {unit}g per {one}"),
            (f"{save}% less",f"per kilo in the {best[0]} jar",f"৳{kg_best:,} a kilo, against ৳{kg_first:,} in the {first[0]} pack")]
def fill(p,C):
    """Every optional field falls back, so a new product needs only the essentials."""
    C=dict(C); k=p['k']; nm=p['short']; cn=cat_of(p['cat'])[0]
    d={'h1':(nm+'.',p.get('role','').split(',')[0]+'.'),'lede':p.get('role',''),'tag':cn,
       'h2':f"{nm} for {', '.join(b for b in p['birds'][:3])} and more.",'answer':p.get('role',''),
       'overview':'','cards':[],'steps':[],'stepk':[],'stepv':[],'rows':[],'cols':('Stage','How often','How much'),
       'howtitle':'How to use','howh2':'How to use it.','howsub':'','tip':'','guide':('All guides','/blog/'),
       'faq':[],'fit':{}, 'fith2':f"Made for {len(p['birds'])} species.",'fitsub':'',
       'use':'','stage':('01','Use','Every day'),'gpu':100,'unit':'Birds','unitone':'bird','needsub':'',
       'thumbs':['Powder<br>texture','In the<br>bowl','Bird<br>feeding'],'shots':[],'video':f'Watch: how to use {nm}',
       'dl':'feeding chart','cmp':'','cmph2':'Versus the import','cmptab':'Compare',
       'kitname':f'Goes with {nm}','kit':[],'related':[],'zigbirds':[],'spec':('','',''),'strip':[]}
    for kk,v in d.items(): C.setdefault(kk,v)
    if not C['strip']: C['strip']=auto_strip(p,C)
    if not C['zigbirds']:
        bl=p['birds'] or BIRDS
        C['zigbirds']=[(bl[i%len(bl)],GRAD[i%len(GRAD)]) for i in range(max(1,len(C['cards'])))]
    if not C['related']: C['related']=[x['k'] for x in P if x['k']!=k][:3]
    if not C['stepk']: C['stepk']=[f'Step {i+1}' for i in range(len(C['steps']))]
    if not C['stepv']: C['stepv']=['']*len(C['steps'])
    if not C['kit']:
        others=[x for x in P if x['k']!=k][:2]
        C['kit']=[(p['slug'],f"{nm} {p['packs'][0][0]}",sku(p,p['packs'][0][0]),p['packs'][0][1],k,'')]+[(o['slug'],f"{o['short']} {o['packs'][0][0]}",sku(o,o['packs'][0][0]),o['packs'][0][1],o['k'],'') for o in others]
    return C

def product_page(p,C):
    C=fill(p,C)
    cn,cac,cbg=cat_of(p['cat'])
    opts=""
    for i,(s,pr) in enumerate(p['packs']):
        g=grams(s); best=i==len(p['packs'])-1
        opts+=f'<label><input type="radio" name="pack" value="{s}" data-price="{pr}" data-kg="{perkg(pr,g)}" data-sku="{sku(p,s)}" {"checked" if i==0 else ""}><span class="o">{"<span class=bv>Best value</span>" if best else ""}<b>{s}</b><span>৳{fmt(pr)}</span></span></label>'
    GL={'lovebird':'#F08A2A','budgerigar':'#8CD34A','cockatiel':'#F2D060','conure':'#F5A623','ringneck':'#5FD48A','rosella':'#E0405A'}
    fitcards="".join((f'<a class="bird" href="/birds/{b}/" style="--glow:{GL[b]};--d:{i*0.45:.2f}s"><span class="ok">{CK}</span><img src="@B_{b}@" alt=""><span class="bf2"><b>{b.title()}</b><small>{C["fit"].get(b,"Yes")}</small></span></a>' if b in p['birds'] else f'<a class="bird no" href="/birds/{b}/" style="--glow:#777;--d:{i*0.45:.2f}s"><span class="ok">&ndash;</span><img src="@B_{b}@" alt=""><span class="bf2"><b>{b.title()}</b><small>{C["fit"].get(b,"Not needed")}</small></span></a>') for i,b in enumerate(BIRDS))
    tlstops=C.get('tl',[(r[0],r[1]) for r in C['rows']][:4])
    tlspans="".join(f'<span><b>{a}</b>{b}</span>' for a,b in tlstops)
    ladder_cards=""
    for i,(s,pr) in enumerate(p['packs']):
        g=grams(s); kg=perkg(pr,g); best=' best' if i==len(p['packs'])-1 else ''
        prev=perkg(p['packs'][i-1][1],grams(p['packs'][i-1][0])) if i else None
        drop='' if i==0 else f'<span class="ldrop"><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12l7 7-7 7"/></svg>{round((prev-kg)/prev*100)}%</span>'
        sc=[.62,.75,.88,1] if len(p['packs'])==4 else [.68,.84,1]
        ladder_cards+=f'<div class="lc{best}" style="--i:{i};--s:{sc[i]}">{drop}{"<span class=lbest>Best value</span>" if best else ""}<img src="@JS_{p["k"]}@" alt=""><b class="lpk">{s}</b><span class="lpr">৳{fmt(pr)}</span><span class="lkg">৳{fmt(kg)} <small>per kg</small></span><code class="lsku">{sku(p,s)}</code></div>'
    save=round((perkg(p['packs'][0][1],grams(p['packs'][0][0]))-perkg(p['packs'][-1][1],grams(p['packs'][-1][0])))/perkg(p['packs'][0][1],grams(p['packs'][0][0]))*100)
    related="\n".join(pcard(x) for x in P if x['k']!=p['k'] and x['k'] in C['related'])
    steps="".join(f'<div class="fstep"><span class="fk">0{i+1} · {C["stepk"][i]}</span><b class="fv">{C["stepv"][i]}</b><h3>{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate(C['steps']))
    rows="".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a,b,c in C['rows'])
    faqs="".join(f'<details{" open" if i==0 else ""}><summary>{q}<span class="pl"><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></span></summary><div class="fa">{a}</div></details>' for i,(q,a) in enumerate(C['faq']))
    STG=[('01','Hatch','Day 1 to weaning',['nutricare']),('02','Grow','Pairing to moult',['eggfood','moringa']),('03','Thrive','Show season and recovery',['spirulina','beetroot','herbs'])]
    here=C['stage'][0]
    nodes="".join(f'''<g class="pnode{' on' if s[0]==here else ''}" transform="translate({x} {y})"><circle class="pulse" r="13"><animate attributeName="r" values="13;40" dur="2.6s" begin="{i*0.8}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".75;0" dur="2.6s" begin="{i*0.8}s" repeatCount="indefinite"/></circle><circle class="core" r="13"/><text y="5">{i+1}</text></g>''' for i,(s,x,y) in enumerate(zip(STG,[200,600,1000],[120,110,130])))
    def _pj(keys):
        out=""
        for kk in keys:
            o=next((x for x in P if x['k']==kk),None)
            if o: out+=f'<a class="pj{" me" if o["k"]==p["k"] else ""}" href="/products/{o["slug"]}/"><img src="@JS_{o["k"]}@" alt="">{o["short"]}</a>'
        return out
    stages="".join(f'''<div class="ps rv in{' on' if s[0]==here else ''}">{'<span class="youare">You are here</span>' if s[0]==here else ''}<span class="pt">{s[2]}</span><h3>{s[1]}</h3><div class="pjars">{_pj(s[3])}</div></div>''' for s in STG)
    strip="".join(f'<div class="spec"><b>{a}</b><span>{b}</span><i>{c}</i></div>' for a,b,c in C['strip'])
    ticks="".join(f'<li>{CK}{a}</li>' for _,a,_ in C['cards'])
    ZB=C['zigbirds']
    zigrows="".join(f'''<div class="c3"><div class="c3i" style="--zb:{ZB[i][1]}"><span class="c3n">{i+1}</span><img src="@B_{ZB[i][0]}@" alt=""></div><div class="c3b"><h3>{a}</h3><p>{b}</p></div></div>''' for i,(ic,a,b) in enumerate(C['cards']))
    kit=C['kit']; kitsum=sum(k[3] for k in kit)
    kitmsg='Hi Shada, I want the '+C['kitname'].lower()+': '+', '.join(f"{k[1]} ({k[2]})" for k in kit)
    kititems=''.join(f'<a class="bi" href="/products/{k[0]}/"><img src="@JS_{k[4]}@" alt=""><b>{k[1]}</b><small>৳{fmt(k[3])}{" · "+k[5] if k[5] else ""}</small></a>'+('<span class="plus">+</span>' if i<len(kit)-1 else '') for i,k in enumerate(kit))
    wa0=f"https://wa.me/8801813323535?text="+__import__('urllib.parse').parse.quote(f"Hi Shada, I want to order {p['short']} {p['packs'][0][0]} x1 ({sku(p,p['packs'][0][0])})")
    h1a,h1b=C['h1']
    body=f'''<section class="phero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><i></i><a href="/shop/">Shop</a><i></i><a href="/product-category/{p['cat']}/">{cn}</a><i></i><span>{p['short']}</span></nav>
    <div class="pgrid pbox">
      <div class="pgal2">
        <div class="pmain"><div class="gtag"><span class="b">Factory sealed</span><span>Batch 07·26</span></div><img id="gimg" class="gjar" src="@JL_{p['k']}@" alt="{p['name']}">
          <div class="gthumbs">
            <button class="on" type="button"><img src="@JS_{p['k']}@" alt="Front"></button>
            <button type="button"><span class="ph">Label<br>close-up</span></button>
            <button type="button"><span class="ph">{C['thumbs'][0]}</span></button>
            <button type="button"><span class="ph">{C['thumbs'][1]}</span></button>
            <button type="button"><span class="ph">{C['thumbs'][2]}</span></button>
          </div></div>
      </div>
      <div class="pright">
        <span class="eyebrow">{p['tag']}</span>
        <h1 class="h-xl">{h1a}<br>{h1b}</h1>
        <p class="sub">{C['lede']}</p>
        <ul class="ticks">{ticks}</ul>
        <div class="chips2 top"><span class="skubar"><span class="skul">SKU</span><b id="sku">{sku(p,p['packs'][0][0])}</b><button type="button" id="skucopy" title="Copy SKU"><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg></button></span><span class="stockchip"><i></i>In stock · 2 working days, all 64 districts</span></div>
        <div class="buycard" id="buy" style="--ac:{p['ac']}">
          <div class="pblk"><div class="pnow"><span id="pnow">৳{fmt(p['packs'][0][1])}</span><small id="pkg">৳{fmt(perkg(p['packs'][0][1],grams(p['packs'][0][0])))} per kg · factory retail price</small></div></div>
          <div class="lbl"><span>Pack size</span><a href="#details2" data-tab="pp">Price per kilo {LK}</a></div>
          <form class="pkf" id="pkf"><div class="pk">{opts}</div>
          <p class="eta" id="eta"></p>
          <div class="brow2"><div class="qty"><button type="button" id="qm" aria-label="Less">&minus;</button><output id="qv">1</output><button type="button" id="qp" aria-label="More">+</button></div><button class="btn b-brand b-cart" type="submit">{I_CART}Add to cart</button><a class="btn b-wa" id="wabtn" href="{wa0}" target="_blank" rel="noopener">{WA}Order on WhatsApp</a></div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div class="phband wing wing-l">
    <img class="avi" src="@B_{p['birds'][0]}@" alt="" style="--w:clamp(60px,7vw,100px);left:clamp(6px,1.6vw,26px);bottom:clamp(10px,1.6vw,22px);--d:.6s">
    <img class="avi mirror" src="@B_{p['birds'][-1]}@" alt="" style="--w:clamp(70px,8vw,116px);right:clamp(24px,7vw,120px);top:clamp(-60px,-5vw,-40px);--d:1.4s">
    <div class="wrap">
      <div class="factsrow">
        <div><span>Made for</span><div class="bf">{"".join(f'<a href="/birds/{b}/"><img src="@B_{b}@" alt="">{b.title()}</a>' for b in p['birds'])}</div></div>
        <div><span>Stage</span><b class="stg"><i>{C['stage'][0]}</i>{C['stage'][1]} · {C['stage'][2]}</b></div>
        <div><span>How to use</span><b>{C['use']}</b></div>
        <div><span>Sealed</span><b>Bhaluka, Mymensingh · batch date on the lid</b></div>
      </div>
      <div class="specs pspecs">{strip}</div>
    </div>
  </div>
</section>

<section class="dark wing" id="fit">
  <div class="wrap">
    <div class="head ctr"><span class="eyebrow">Is it for my bird?</span><h2 class="h-l">{C['fith2']}</h2><p class="sub">{C['fitsub']}</p></div>
    <div class="birds fitbirds rv">{fitcards}</div>
  </div>
</section>

<section id="details2">
  <div class="wrap">
    <div class="head ctr"><span class="eyebrow">The detail</span><h2 class="h-l">Everything on the label.</h2></div>
    <div class="dwrap rv">
    <div class="dtabs" id="dtabs" role="tablist">
      <button class="dtab on" role="tab" data-d="ov" aria-selected="true"><i>{I_LEAF}</i><span>Overview</span></button>
      <button class="dtab" role="tab" data-d="in" aria-selected="false"><i>{I_LIST}</i><span>Ingredients</span></button>
      <button class="dtab" role="tab" data-d="st" aria-selected="false"><i>{I_SEAL}</i><span>Storage</span></button>
      <button class="dtab" role="tab" data-d="pp" aria-selected="false"><i>{I_PRICE}</i><span>Pack prices</span></button>
      {f'<button class="dtab" role="tab" data-d="vs" aria-selected="false"><i>{I_SCALE}</i><span>'+C["cmptab"]+'</span></button>' if C['cmp'] else ''}
      <button class="dtab" role="tab" data-d="dl" aria-selected="false"><i>{I_TRUCK}</i><span>Delivery</span></button>
    </div>
    <div class="dpanel on" id="d-ov" role="tabpanel"><h3>Product overview</h3><p>{C['answer']}</p><p>{C['overview']}</p></div>
    <div class="dpanel" id="d-in" role="tabpanel"><h3>Ingredients and analysis</h3><p class="dsub">Printed on every jar. Fill these from the {p['short']} label before the page goes live.</p>
      <div class="ing">
        <div class="ingc"><span class="mh">{I_LEAF}Composition</span>
          <div class="chipset">{"".join('<span class="ingchip ph">ingredient %d</span>'%(i+1) for i in range(8))}</div>
          <p class="ingnote">Replace each chip with one ingredient from the label, in label order.</p></div>
        <div class="ingc"><span class="mh">{I_LIST}Analytical constituents<small>per 100g</small></span>
          <div class="agrid">
            <div class="at"><b class="ph">00%</b><span>Crude protein</span></div>
            <div class="at"><b class="ph">00%</b><span>Crude fat</span></div>
            <div class="at"><b class="ph">00%</b><span>Crude fibre</span></div>
            <div class="at"><b class="ph">00%</b><span>Crude ash</span></div>
            <div class="at"><b class="ph">00%</b><span>Moisture</span></div>
            <div class="at"><b class="ph">00%</b><span>Calcium</span></div>
          </div></div>
      </div>
      <div class="dlcards">
        <a class="dlc" href="#"><i>{DL}</i><span><b>Label and {C['dl']}</b><small>PDF <em class="ph">add file</em></small></span>{LK}</a>
        <a class="dlc" href="#"><i>{DL}</i><span><b>Dealer price list</b><small>PDF <em class="ph">add file</em></small></span>{LK}</a>
      </div></div>
    <div class="dpanel" id="d-st" role="tabpanel"><h3>Storage and shelf life</h3><p>Keep the lid tight, the jar dry and out of the sun. Use a dry scoop only; a wet scoop is what spoils a jar in the monsoon. The batch date is printed on the lid. Shelf life: <span class="ph">from label</span>.</p></div>
    <div class="dpanel" id="d-pp" role="tabpanel"><h3>The bigger the pack, the cheaper the kilo.</h3><p class="dsub">Per-kilo price steps down as the jar steps up. Save {save}% per kilo with the {p['packs'][-1][0]} jar.</p>
      <div class="pladder dark wing"><div class="lrow" style="--n:{len(p['packs'])}">{ladder_cards}</div></div></div>
    <div class="dpanel" id="d-vs" role="tabpanel"><h3>{C['cmph2']}</h3><p class="dsub">Checked on Bangladeshi marketplaces, August 2026. n/a means not published by the seller.</p>{C['cmp']}</div>
    <div class="dpanel" id="d-dl" role="tabpanel"><h3>Delivery, payment and returns</h3><p>Sundarban Courier to all 64 districts, two working days from the factory in Bhaluka. The same factory retail price in every district. Payment options and the returns policy are set by the client: <span class="ph">confirm before launch</span>. Questions on WhatsApp 01813-323535.</p></div>
    </div>
  </div>
</section>

{'<!--' if not C['cards'] else ''}<section class="tint wing wing-l" id="does">
  <div class="wrap">
    <div class="head ctr"><span class="eyebrow">What it does</span><h2 class="h-l">{C['h2']}</h2></div>
    <div class="cols3 rv">{zigrows}</div>
  </div>
</section>{'-->' if not C['cards'] else ''}

{'<!--' if not C['steps'] else ''}<section class="dark wing" id="howto">
  <div class="wrap">
    <div class="head ctr"><span class="eyebrow">{C['howtitle']}</span><h2 class="h-l">{C['howh2']}</h2><p class="sub">{C['howsub']}</p></div>
    <div class="fsteps rv">{steps}</div>
    <div class="hgrid"><div class="fcard"><table class="ftable"><thead><tr><th>{C['cols'][0]}</th><th>{C['cols'][1]}</th><th>{C['cols'][2]}</th></tr></thead><tbody>{rows}</tbody></table></div>
      <div class="tip"><b>Tip</b><p>{C['tip']}</p><a class="link" style="font-size:15px" href="{C['guide'][1]}">{C['guide'][0]} {LK}</a></div></div>
  </div>
</section>{'-->' if not C['steps'] else ''}

<section id="more">
  <div class="wrap">
    <div class="bhead"><div><span class="eyebrow">Pairs well with</span><h2 class="h-m" style="font-size:clamp(24px,2.6vw,34px)">{C['kitname']}.</h2></div><a class="link" href="/shop/">All products {LK}</a></div>
    <div class="sgrid">{related}</div>
    <div class="kitbar"><span class="ke">Buy the three together</span><b>৳{fmt(kitsum)}</b><span class="kl">{" + ".join(k[1] for k in kit)}</span><a class="btn b-brand b-sm" href="https://wa.me/8801813323535?text={__import__('urllib.parse').parse.quote(kitmsg)}" target="_blank" rel="noopener">Order the kit on WhatsApp</a></div>
  </div>
</section>

<section class="tint" id="faq">
  <div class="wrap">
    <div class="head ctr"><span class="eyebrow">Before you ask</span><h2 class="h-l">Questions we get on WhatsApp.</h2></div>
    <div class="faqs rv">{faqs}</div>
  </div>
</section>
<section class="dark wing plan" id="plan" style="overflow:hidden">
  <div class="wrap">
    <div class="phead rv">
      <div><span class="eyebrow">Six jars, one plan</span><h2 class="h-l">Where {p['short']}<br>sits in the year.</h2></div>
      <p class="sub">Every jar has a place in the bird&rsquo;s life. {p['short']} is stage {C['stage'][0]}. Follow the line for what comes before and after.</p>
    </div>
    <div class="pmap rv in">
      <svg viewBox="0 0 1200 240" preserveAspectRatio="none" aria-hidden="true">
        <path class="pguide" d="M0 160 C100 80 150 80 200 120 C350 190 450 190 600 110 C750 30 850 60 1000 130 C1100 180 1150 150 1200 120" pathLength="1000"/>
        <path class="pline" id="planpath" d="M0 160 C100 80 150 80 200 120 C350 190 450 190 600 110 C750 30 850 60 1000 130 C1100 180 1150 150 1200 120" pathLength="1000"/>
        {nodes}
        <image class="pbird" href="@B_{p['birds'][0]}@" width="132" height="104" x="-66" y="-92"><animateMotion dur="18s" repeatCount="indefinite" rotate="auto" calcMode="linear"><mpath href="#planpath"/></animateMotion></image>
      </svg>
    </div>
    <div class="pstages">{stages}</div>
  </div>
</section>
<section class="brand wing pfin" style="overflow:hidden">
  <img class="avi" src="@B_{p['birds'][0]}@" alt="" style="--w:clamp(62px,7vw,104px);left:clamp(6px,3vw,46px);bottom:7%;--d:.4s">
  <img class="avi mirror" src="@B_{p['birds'][-1]}@" alt="" style="--w:clamp(62px,7vw,104px);right:clamp(6px,3vw,46px);top:9%;--d:1.2s">
  <div class="wrap fingrid">
    <div class="fintext">
      <span class="eyebrow">Ready to order</span>
      <h2 class="h-l">Ready when<br>your birds are.</h2>
      <ul class="finticks">
        <li>{CK}<span><b>Factory sealed in Bhaluka.</b> Batch date on every lid, never repacked.</span></li>
        <li>{CK}<span><b>Two working days, all 64 districts.</b> Sundarban Courier from the factory.</span></li>
        <li>{CK}<span><b>One factory retail price.</b> The same in Dhaka and in Panchagarh.</span></li>
        <li>{CK}<span><b>A breeder on WhatsApp.</b> Send a photo of the bird and ask before you buy.</span></li>
      </ul>
    </div>
    <div class="fincard">
      <div class="fc-top"><img src="@JS_{p['k']}@" alt=""><div><b>{p['name']}</b><small id="fsize">{p['packs'][0][0]} &middot; {sku(p,p['packs'][0][0])}</small></div></div>
      <div class="fc-row"><span>Price</span><b id="fprice">৳{fmt(p['packs'][0][1])}</b></div>
      <div class="fc-row"><span>Per kilo</span><b id="fkg">৳{fmt(perkg(p['packs'][0][1],grams(p['packs'][0][0])))}</b></div>
      <div class="fc-row"><span>At your door</span><b id="feta">&mdash;</b></div>
      <div class="fc-row"><span>Stock</span><b class="ok">In stock</b></div>
      <a class="btn b-brand" href="#buy">{I_CART}Add to cart</a>
      <a class="btn b-line2" id="fwa" href="{wa0}" target="_blank" rel="noopener">{WA}Order on WhatsApp</a>
      <small class="fc-note">Prices in BDT, factory retail. Change the pack size at the top of the page.</small>
    </div>
  </div>
</section>

<script>
(function(){{const f=document.getElementById('pkf');if(!f)return;let q=1;const qv=document.getElementById('qv');const NAME={json.dumps(p['short'])};
const upd=()=>{{const r=f.querySelector('input[name=pack]:checked');const pr=+r.dataset.price*q;document.getElementById('pnow').textContent='৳'+pr.toLocaleString('en-IN');document.getElementById('pkg').textContent='৳'+(+r.dataset.kg).toLocaleString('en-IN')+' per kg';document.getElementById('sku').textContent=r.dataset.sku;
 const fs=document.getElementById('fsize');if(fs){{fs.innerHTML=r.value+' &middot; '+r.dataset.sku;document.getElementById('fprice').textContent='৳'+pr.toLocaleString('en-IN');document.getElementById('fkg').textContent='৳'+(+r.dataset.kg).toLocaleString('en-IN');document.getElementById('fwa').href='https://wa.me/8801813323535?text='+encodeURIComponent('Hi Shada, I want to order '+NAME+' '+r.value+' x'+q+' ('+r.dataset.sku+')');}}
 const msg=encodeURIComponent('Hi Shada, I want to order '+NAME+' '+r.value+' x'+q+' ('+r.dataset.sku+')');document.getElementById('wabtn').href='https://wa.me/8801813323535?text='+msg;}};
f.addEventListener('change',upd);document.getElementById('qm').onclick=()=>{{q=Math.max(1,q-1);qv.value=q;upd()}};document.getElementById('qp').onclick=()=>{{q=Math.min(20,q+1);qv.value=q;upd()}};f.addEventListener('submit',e=>{{e.preventDefault();alert('Add to cart connects to WooCommerce on the live site.')}});
document.querySelectorAll('[data-tab]').forEach(a=>a.addEventListener('click',()=>{{const b=document.querySelector('.dtab[data-d="'+a.dataset.tab+'"]');if(b)b.click()}}));
(function(){{const e=document.getElementById('eta');if(!e)return;const d=new Date();let n=0;while(n<2){{d.setDate(d.getDate()+1);if(d.getDay()!==5)n++}}
const s=d.toLocaleDateString('en-GB',{{weekday:'long',day:'numeric',month:'short'}});
const fe=document.getElementById('feta');if(fe)fe.textContent=s;
 e.innerHTML='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>Order today, at your door by <b>'+s+'</b>';}})();
const dt=document.getElementById('dtabs');if(dt)dt.addEventListener('click',e=>{{const b=e.target.closest('.dtab');if(!b)return;const k=b.dataset.d;
 dt.querySelectorAll('.dtab').forEach(x=>{{const on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-selected',String(on))}});
 document.querySelectorAll('.dpanel').forEach(pn=>pn.classList.toggle('on',pn.id==='d-'+k));}});
const sc=document.getElementById('skucopy');if(sc)sc.onclick=()=>{{navigator.clipboard&&navigator.clipboard.writeText(document.getElementById('sku').textContent);sc.classList.add('ok');setTimeout(()=>sc.classList.remove('ok'),1200)}};
document.querySelectorAll('.gthumbs button').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.gthumbs button').forEach(x=>x.classList.remove('on'));b.classList.add('on')}}));
const tabs=[...document.querySelectorAll('.ptabs a')];const blocks=tabs.map(a=>document.querySelector(a.getAttribute('href')));
const io=new IntersectionObserver(en=>{{en.forEach(x=>{{if(x.isIntersecting){{tabs.forEach(t=>t.classList.toggle('on',t.getAttribute('href')==='#'+x.target.id))}}}})}},{{rootMargin:'-40% 0px -55% 0px'}});blocks.forEach(b=>b&&io.observe(b));}})();
</script>'''
    ld=json.dumps({"@context":"https://schema.org","@graph":[{"@type":"Product","name":p['name'],"sku":f"SBF-{sku_code(p)}","brand":{"@type":"Brand","name":"Shada Bird Feed"},"description":C['lede'],"category":cn,"offers":[{"@type":"Offer","name":s,"sku":sku(p,s),"price":pr,"priceCurrency":"BDT","availability":"https://schema.org/InStock","url":f"https://shadabirdfeed.com/products/{p['slug']}/"} for s,pr in p['packs']]},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in C['faq']]},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://shadabirdfeed.com/"},{"@type":"ListItem","position":2,"name":"Shop","item":"https://shadabirdfeed.com/shop/"},{"@type":"ListItem","position":3,"name":cn,"item":f"https://shadabirdfeed.com/product-category/{p['cat']}/"},{"@type":"ListItem","position":4,"name":p['name']}]}]},ensure_ascii=False)
    return page(f"{p['name']} · Shada Bird Feed",C['lede'][:150],f"/products/{p['slug']}/",body,ld)
exec(open('shopcontent.py',encoding='utf-8').read())
pages={'shop.html':page('Shop · Shada Bird Feed','Six formulas, twenty pack sizes. Hand feeding formula, eggfood and supplements, sealed in Bhaluka, delivered to all 64 districts.','/shop/',shop_body),

       }
for ck in CATS: pages[f'category-{ck}.html']=category_page(ck)
for pp in P: pages[f"product-{pp['k']}.html"]=product_page(pp,CONTENT[pp['k']])
uris=json.load(open('shada-assets/uris.json')); small=json.load(open('shada-assets/small.json'))
m={'nutricare':'Shada Nutricare Hand Feeding','eggfood':'Shada Avian Eggfood','herbs':'Shada Avian Herbs','spirulina':'Shada Avian Spirulina','moringa':'Shada Moringa Leaf Powder','beetroot':'Shada Beetroot Powder'}
birdsb={}
for n in BIRDS:
    im=Image.open(f'birds/{n}.png').convert('RGBA'); im.thumbnail((360,360)); o=io.BytesIO(); im.save(o,'WEBP',quality=82,method=6); birdsb[n]='data:image/webp;base64,'+base64.b64encode(o.getvalue()).decode()
white=open('shada-assets/logo-white.svg',encoding='utf-8').read(); white=re.sub(r'<\?xml[^>]*\?>','',white).strip(); white=re.sub(r'\s(width|height)="[^"]*"','',white,count=2)
fonts=open('/tmp/wf/fonts-inline.css').read(); keep=[b for b in fonts.split('\n') if "'Plus Jakarta Sans'" in b or "'Hind Siliguri'" in b]
os.makedirs('shop',exist_ok=True)
for fn,html in pages.items():
    t=html
    for k,alt in m.items(): t=t.replace('@JL_%s@'%k,uris[alt]).replace('@JS_%s@'%k,small[k])
    for n,u in birdsb.items(): t=t.replace('@B_%s@'%n,u)
    t=t.replace('@LOGO_DARK@',white.replace('rgb(100%, 100%, 100%)','#1D1D1F'))
    left=re.findall(r'@[A-Z_a-z]+@',t); assert not left,(fn,left)
    open(f'shop/{fn}','w',encoding='utf-8').write(t)
    a=t.replace('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600;700&display=swap" rel="stylesheet">','<style>:root{color-scheme:light}\n'+"\n".join(keep)+'</style>').replace('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>','')
    open(f'shop/{fn[:-5]}-artifact.html','w',encoding='utf-8').write(a)
    print(fn,round(len(t)/1024),'KB')
