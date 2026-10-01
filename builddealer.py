#!/usr/bin/env python3
# Shada Bird Feed · dealer locator page generator
# Reuses the shop page shell (header, mega menu, footer) and the 64-district map.
import json, re, os

HEAD = open('/tmp/dealer/head.txt', encoding='utf-8').read()
FOOT = open('/tmp/dealer/foot.txt', encoding='utf-8').read()
MAP  = open('/tmp/dealer/mapsvg.txt', encoding='utf-8').read()
DIV  = json.load(open('/tmp/dealer/div.json'))
DISTRICTS = sorted([d for v in DIV.values() for d in v])

I = lambda p, w=1.9: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
I_PIN   = I('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>')
I_PHONE = I('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7A2 2 0 0 1 22 16.9z"/>')
I_WA    = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5.3-.5c.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5 2.5 1 3 .8 3.6.7.5-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4ZM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Z"/></svg>'
I_NAV   = I('<path d="M3 11l19-9-9 19-2-8-8-2z"/>')
I_SEARCH= I('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>')
I_CLOCK = I('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
I_CHECK = I('<path d="M4 12.5 9.5 18 20 6.5"/>', 2.4)
I_TRUCK = I('<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>')
I_BADGE = I('<path d="M12 3l2.4 4.9 5.4.8-3.9 3.8.9 5.4-4.8-2.5-4.8 2.5.9-5.4L4.2 8.7l5.4-.8z"/>')
I_X     = I('<path d="M18 6 6 18M6 6l12 12"/>', 2.2)
I_ARROW = I('<path d="M5 12h14M12 5l7 7-7 7"/>', 2.4)

# ══════════════════════════════════════════════════════════════════════
#  DEALER RECORDS
#  The whole page is driven by this list. Adding a dealer is one object,
#  nothing else needs touching. The counters, the map highlighting, the
#  search and the division chips all read from it.
#
#  Fields
#    name      shop name as it appears on the signboard
#    person    who to ask for at the counter, optional
#    type      'distributor' (district wholesale) or 'retail' (shop counter)
#    district  MUST match a district name in the map, see DISTRICTS below
#    div       division
#    area      the local area, shown in bold on the card
#    addr      the full line that gets sent to Google Maps for directions
#    phone     as written locally, the tel: link strips it automatically
#    wa        WhatsApp number in international form, no + and no spaces
#    hours     opening hours, optional
#    since     year they became a dealer, optional
#    hq        True only for the factory outlet
# ══════════════════════════════════════════════════════════════════════

# The only verified record. Address and phone from the client's own invoice sheet.
REAL = [
    dict(name="Shada Bird Feed · Factory Outlet", person="Factory counter", type="distributor",
         district="Mymensingh", div="Mymensingh", area="Majorvita, Bhaluka",
         addr="Majorvita, Bhaluka, Mymensingh", phone="01813-323535", wa="8801813323535",
         hours="Sat to Thu, 9am to 6pm", since="2021", hq=True),
]

# ── SAMPLE DATA · DELETE BEFORE THE SITE GOES LIVE ────────────────────
# These exist so the page can be reviewed with a realistic number of
# dealers. Every name, phone and address below is invented. Set
# SHOW_SAMPLES = False, or delete this block, once the real list arrives.
SHOW_SAMPLES = True
SAMPLES = [
    dict(name="Dhaka Bird House", person="Saddam", type="distributor",
         district="Dhaka", div="Dhaka", area="Mirpur 11",
         addr="Mirpur 11, Dhaka", phone="01700-000001", wa="8801700000001",
         hours="Daily, 10am to 8pm", since="2022"),
    dict(name="Jatrabari Pet Corner", person="Ali", type="retail",
         district="Dhaka", div="Dhaka", area="Jatrabari",
         addr="Jatrabari, Dhaka", phone="01700-000002", wa="8801700000002",
         hours="Daily, 10am to 9pm", since="2023"),
    dict(name="Lutino Park Aviary", person="Rafiq", type="distributor",
         district="Manikganj", div="Dhaka", area="Manikganj Sadar",
         addr="Manikganj Sadar, Manikganj", phone="01700-000003", wa="8801700000003",
         hours="Sat to Thu, 10am to 7pm", since="2023"),
    dict(name="Bogra Bird Bazar", person="Jahid", type="distributor",
         district="Bogra", div="Rajshahi", area="Bogra Sadar",
         addr="Bogra Sadar, Bogra", phone="01700-000004", wa="8801700000004",
         hours="Sat to Thu, 9am to 8pm", since="2023"),
    dict(name="Rajshahi Pet Mart", person="Mamun", type="retail",
         district="Rajshahi", div="Rajshahi", area="Shaheb Bazar",
         addr="Shaheb Bazar, Rajshahi", phone="01700-000005", wa="8801700000005",
         hours="Daily, 10am to 8pm", since="2024"),
    dict(name="Port City Aviary", person="Nasir", type="distributor",
         district="Chittagong", div="Chattogram", area="Chawkbazar",
         addr="Chawkbazar, Chittagong", phone="01700-000006", wa="8801700000006",
         hours="Daily, 10am to 9pm", since="2022"),
    dict(name="Comilla Bird Care", person="Sohel", type="retail",
         district="Comilla", div="Chattogram", area="Kandirpar",
         addr="Kandirpar, Comilla", phone="01700-000007", wa="8801700000007",
         hours="Sat to Thu, 10am to 8pm", since="2024"),
    dict(name="Khulna Feather Store", person="Imran", type="distributor",
         district="Khulna", div="Khulna", area="Khulna Sadar",
         addr="Khulna Sadar, Khulna", phone="01700-000008", wa="8801700000008",
         hours="Sat to Thu, 9am to 8pm", since="2023"),
    dict(name="Jessore Bird Supply", person="Tanvir", type="retail",
         district="Jessore", div="Khulna", area="Jessore Sadar",
         addr="Jessore Sadar, Jessore", phone="01700-000009", wa="8801700000009",
         hours="Daily, 10am to 8pm", since="2024"),
    dict(name="Sylhet Aviary Centre", person="Kamrul", type="distributor",
         district="Sylhet", div="Sylhet", area="Zindabazar",
         addr="Zindabazar, Sylhet", phone="01700-000010", wa="8801700000010",
         hours="Daily, 10am to 9pm", since="2023"),
    dict(name="Rangpur Bird Feed", person="Shamim", type="distributor",
         district="Rangpur", div="Rangpur", area="Rangpur Sadar",
         addr="Rangpur Sadar, Rangpur", phone="01700-000011", wa="8801700000011",
         hours="Sat to Thu, 9am to 7pm", since="2024"),
    dict(name="Dinajpur Pet World", person="Rubel", type="retail",
         district="Dinajpur", div="Rangpur", area="Dinajpur Sadar",
         addr="Dinajpur Sadar, Dinajpur", phone="01700-000012", wa="8801700000012",
         hours="Sat to Thu, 10am to 8pm", since="2025"),
    dict(name="Barisal Bird Point", person="Faisal", type="distributor",
         district="Barisal", div="Barisal", area="Barisal Sadar",
         addr="Barisal Sadar, Barisal", phone="01700-000013", wa="8801700000013",
         hours="Daily, 10am to 8pm", since="2024"),
    dict(name="Jamalpur Aviary Supply", person="Hasan", type="retail",
         district="Jamalpur", div="Mymensingh", area="Jamalpur Sadar",
         addr="Jamalpur Sadar, Jamalpur", phone="01700-000014", wa="8801700000014",
         hours="Sat to Thu, 9am to 7pm", since="2025"),
]
# ── END SAMPLE DATA ───────────────────────────────────────────────────

DEALERS = REAL + (SAMPLES if SHOW_SAMPLES else [])

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))

DATA = json.dumps(DEALERS, ensure_ascii=False)
DIVJSON = json.dumps(DIV, ensure_ascii=False)

CSS = '''
/* ═══════════════════════════════════════════════════════════════════
   DEALER LOCATOR  ·  /dealers/
   Loads after 01-base.css and 02-shop-pages.css. Nothing here is used
   by any other page, so it can also live in Elementor Page Settings CSS
   for this page only.
   Tokens come from 01-base.css. No hard-coded brand colours below except
   inside the map, which is self-contained.
   ═══════════════════════════════════════════════════════════════════ */

/* ── Hero ───────────────────────────────────────────────────────── */
.dlhero{background:var(--ink);color:#fff;position:relative;overflow:hidden;padding:clamp(44px,6vw,84px) 0 clamp(36px,5vw,64px)}
.dlhero::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;opacity:.07;pointer-events:none}
.dlhero .wrap{position:relative}
.dlhero h1{font-size:clamp(34px,5vw,62px);letter-spacing:-.035em;line-height:1.04;margin:10px 0 14px}
.dlhero .sub{font-size:17px;line-height:1.6;color:var(--on2);max-width:54ch}

/* Live counters, filled by JS from the dealer list so they can never go stale */
.dlstats{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.dlstat{background:var(--ink2);border:1px solid var(--line-d);border-radius:var(--r2);padding:14px 18px;min-width:132px}
.dlstat b{display:block;font-size:clamp(24px,2.6vw,32px);letter-spacing:-.03em;line-height:1}
.dlstat span{display:block;font-size:12.5px;color:var(--on2);margin-top:5px}

/* ── Search and filter bar, sticks under the header while scrolling ── */
.dlbar{position:sticky;top:var(--hh,64px);z-index:40;background:rgba(255,255,255,.92);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--line);padding:14px 0}
.dlbar .wrap{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.dlsearch{position:relative;flex:1;min-width:240px}
.dlsearch svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:18px;height:18px;color:var(--tx3)}
.dlsearch input{width:100%;height:50px;border:1px solid var(--line);border-radius:var(--r2);
  padding:0 42px 0 42px;font:500 15px/1 var(--ff);color:var(--tx);background:#fff;outline:none}
.dlsearch input::placeholder{color:var(--tx3);font-weight:400}
.dlsearch input:focus{border-color:var(--brand);box-shadow:0 0 0 3px rgba(8,152,48,.13)}
.dlsearch .clr{position:absolute;right:8px;top:50%;transform:translateY(-50%);width:32px;height:32px;
  display:none;place-items:center;border:0;background:var(--paper2);border-radius:8px;color:var(--tx2);cursor:pointer}
.dlsearch .clr svg{position:static;transform:none;width:15px;height:15px;color:inherit}
.dlsearch.has .clr{display:grid}

.dlchips{display:flex;gap:7px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding-bottom:1px}
.dlchips::-webkit-scrollbar{display:none}
.dlchip{flex:0 0 auto;height:38px;padding:0 15px;border-radius:999px;border:1px solid var(--line);
  background:#fff;font:600 13.5px/1 var(--ff);color:var(--tx2);cursor:pointer;display:inline-flex;
  align-items:center;gap:7px;transition:background .2s,color .2s,border-color .2s}
.dlchip:hover{border-color:var(--tx3)}
.dlchip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#fff}
.dlchip i{font-style:normal;font-size:11.5px;opacity:.7}

/* ── Two-column body: map on the left, results on the right ─────── */
.dlgrid{display:grid;grid-template-columns:minmax(300px,420px) 1fr;gap:clamp(24px,3.4vw,48px);align-items:start}
@media(max-width:980px){.dlgrid{grid-template-columns:1fr}}

.dlmapcard{position:sticky;top:calc(var(--hh,64px) + 92px);background:var(--paper2);border:1px solid var(--line);
  border-radius:var(--r3);padding:18px 18px 14px}
@media(max-width:980px){.dlmapcard{position:static;order:2}}
.dlmapcard h2{font-size:17px;margin-bottom:3px}
.dlmapcard p{font-size:13px;color:var(--tx2);margin-bottom:12px}
.dlmap{width:100%;height:auto;display:block}
/* District states. Covered districts are clickable, the rest stay flat. */
.dlmap .dist path{fill:#E4E8E4;stroke:#fff;stroke-width:1.1;transition:fill .2s;cursor:default;outline:none}
.dlmap .dist path.has{fill:#9ED9B4;cursor:pointer}
.dlmap .dist path.has:hover{fill:var(--brand)}
.dlmap .dist path.on{fill:var(--ink)}
.dlmap .dist path.has:focus-visible{stroke:var(--ink);stroke-width:2.4}
.dlkey{display:flex;gap:16px;flex-wrap:wrap;margin-top:10px;font-size:12px;color:var(--tx2)}
.dlkey span{display:inline-flex;align-items:center;gap:6px}
.dlkey i{width:11px;height:11px;border-radius:3px;display:inline-block}

/* ── Results ────────────────────────────────────────────────────── */
.dlhead{display:flex;align-items:baseline;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:16px}
.dlhead h2{font-size:clamp(20px,2.3vw,27px);letter-spacing:-.025em}
.dlhead .cnt{font-size:13.5px;color:var(--tx2)}
.dlcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px;align-items:start}
.dlcard{background:#fff;border:1px solid var(--line);border-radius:var(--r3);padding:20px 22px;
  transition:border-color .2s,box-shadow .3s,transform .35s var(--ease)}
.dlcard:hover{border-color:var(--paper3);box-shadow:0 16px 38px rgba(0,0,0,.06);transform:translateY(-2px)}
.dlcard.hq{border-color:var(--brand);box-shadow:0 0 0 1px var(--brand) inset}
.dltop{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;margin-bottom:4px}
.dlcard h3{font-size:19px;letter-spacing:-.02em;line-height:1.25}
.dltag{flex:0 0 auto;display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600;
  letter-spacing:.04em;text-transform:uppercase;padding:5px 10px;border-radius:999px;
  background:var(--paper2);color:var(--tx2);border:1px solid var(--line)}
.dltag.d{background:rgba(8,152,48,.1);color:#0A6B27;border-color:rgba(8,152,48,.22)}
.dltag.h{background:var(--ink);color:#fff;border-color:var(--ink)}
.dltag svg{width:12px;height:12px}
.dlmeta{display:grid;gap:7px;margin:12px 0 16px}
.dlmeta div{display:flex;gap:9px;align-items:flex-start;font-size:14.5px;color:var(--tx2);line-height:1.45}
.dlmeta svg{width:17px;height:17px;flex:0 0 auto;color:var(--tx3);margin-top:1px}
.dlmeta b{color:var(--tx);font-weight:600}
.dlact{display:flex;gap:9px;flex-wrap:wrap;padding-top:14px;border-top:1px solid var(--line)}
.dlact a{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:44px;padding:0 16px;
  border-radius:var(--r);font:600 14px/1 var(--ff);text-decoration:none;white-space:nowrap;
  transition:background .2s,color .2s,border-color .2s}
.dlact svg{width:16px;height:16px}
.dlact .call{background:var(--brand);color:#fff;flex:1;min-width:132px}
.dlact .call:hover{background:var(--brand-d,#067426)}
.dlact .wa{background:#fff;color:var(--tx);border:1px solid var(--line)}
.dlact .wa:hover{border-color:#25D366;color:#128C4B}
.dlact .map{background:#fff;color:var(--tx);border:1px solid var(--line)}
.dlact .map:hover{border-color:var(--tx);}

/* Empty state, the most important screen on this page */
.dlnone{border:1px dashed var(--line);border-radius:var(--r3);padding:clamp(28px,4vw,44px);text-align:center;background:var(--paper2)}
.dlnone h3{font-size:21px;margin-bottom:8px;letter-spacing:-.02em}
.dlnone p{font-size:15px;color:var(--tx2);max-width:46ch;margin:0 auto 20px;line-height:1.6}
.dlnone .btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}

/* ── Become a dealer band ───────────────────────────────────────── */
.dljoin{background:var(--ink);color:#fff;position:relative;overflow:hidden}
.dljoin::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;opacity:.07}
.dljoin .wrap{position:relative;display:grid;grid-template-columns:1.1fr 1fr;gap:clamp(28px,4vw,64px);align-items:center}
@media(max-width:860px){.dljoin .wrap{grid-template-columns:1fr}}
.dljoin h2{font-size:clamp(28px,3.6vw,46px);letter-spacing:-.03em;line-height:1.06;margin-bottom:14px}
.dljoin p{font-size:16.5px;color:var(--on2);line-height:1.6;margin-bottom:8px;max-width:50ch}
.dljoin .btn{margin-top:18px}
.dljlist{display:grid;gap:11px;list-style:none}
.dljlist li{display:flex;gap:12px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line-d);
  border-radius:var(--r2);padding:16px 18px}
.dljlist svg{width:19px;height:19px;color:var(--leaf);flex:0 0 auto;margin-top:2px}
.dljlist b{display:block;font-size:15.5px;margin-bottom:3px}
.dljlist span{font-size:13.5px;color:var(--on2);line-height:1.45}

@media(max-width:560px){
  .dlact a{flex:1 1 100%}
  .dlcard{padding:18px}
}
'''

JS = '''
/* ═══════════════════════════════════════════════════════════════════
   DEALER LOCATOR  ·  behaviour
   One source of truth: the DEALERS array. Search, chips, the map,
   the counters and the result list all read from it, so adding a
   dealer is one object and nothing else needs touching.
   ═══════════════════════════════════════════════════════════════════ */
(function(){
  var DEALERS = __DATA__;
  var DIV     = __DIV__;

  var $  = function(s,c){return (c||document).querySelector(s)};
  var $$ = function(s,c){return [].slice.call((c||document).querySelectorAll(s))};

  var elList = $('#dlcards'), elCount = $('#dlcount'), elTitle = $('#dltitle');
  var elInput = $('#dlq'), elSearch = $('#dlsearch'), elMap = $('#dlmap');
  var state = { q:'', div:'', district:'' };

  /* ── Counters. Computed, never typed, so they cannot go stale. ── */
  var covered = {}; DEALERS.forEach(function(d){ covered[d.district] = true; });
  var nDist = Object.keys(covered).length;
  var nDiv  = Object.keys(DIV).filter(function(k){
                return DIV[k].some(function(d){ return covered[d]; }); }).length;
  $('#nDealers').textContent = DEALERS.length;
  $('#nDistricts').textContent = nDist;
  $('#nDivisions').textContent = nDiv;

  /* ── Map: mark covered districts, wire clicks ── */
  $$('#dlmap .dist path').forEach(function(p){
    var d = p.getAttribute('data-d');
    if(covered[d]) p.classList.add('has');
    p.addEventListener('click', function(){ if(covered[d]) pick(d); });
    p.addEventListener('keydown', function(e){
      if((e.key==='Enter'||e.key===' ') && covered[d]){ e.preventDefault(); pick(d); }
    });
  });

  function pick(d){
    state.district = (state.district===d) ? '' : d;
    state.div = ''; state.q=''; elInput.value=''; elSearch.classList.remove('has');
    syncChips(); render();
    var y = elTitle.getBoundingClientRect().top + window.scrollY - 150;
    window.scrollTo({top:y, behavior:'smooth'});
  }

  /* ── Division chips ── */
  $$('.dlchip').forEach(function(c){
    c.addEventListener('click', function(){
      var v = c.getAttribute('data-div');
      state.div = (state.div===v) ? '' : v;
      state.district = '';
      syncChips(); render();
    });
  });
  function syncChips(){
    $$('.dlchip').forEach(function(c){
      c.setAttribute('aria-pressed', String(c.getAttribute('data-div')===state.div && state.div!==''));
    });
  }

  /* ── Search ── */
  elInput.addEventListener('input', function(){
    state.q = elInput.value.trim().toLowerCase();
    elSearch.classList.toggle('has', !!state.q);
    if(state.q){ state.district=''; state.div=''; syncChips(); }
    render();
  });
  $('#dlclear').addEventListener('click', function(){
    elInput.value=''; state.q=''; elSearch.classList.remove('has'); elInput.focus(); render();
  });

  /* ── Filter and draw ── */
  function match(d){
    if(state.district && d.district !== state.district) return false;
    if(state.div && d.div !== state.div) return false;
    if(state.q){
      var hay = (d.name+' '+d.person+' '+d.district+' '+d.div+' '+d.area+' '+d.addr).toLowerCase();
      if(hay.indexOf(state.q) === -1) return false;
    }
    return true;
  }

  function card(d){
    var maps = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(d.addr);
    var tel  = 'tel:' + d.phone.replace(/[^0-9+]/g,'');
    var wa   = 'https://wa.me/' + d.wa;
    var tag  = d.hq ? '<span class="dltag h">__BADGE__ Factory</span>'
             : d.type==='distributor' ? '<span class="dltag d">Distributor</span>'
             : '<span class="dltag">Retail counter</span>';
    return '<article class="dlcard'+(d.hq?' hq':'')+'">'
      + '<div class="dltop"><h3>'+d.name+'</h3>'+tag+'</div>'
      + '<div class="dlmeta">'
      +   '<div>__PIN__<span><b>'+d.area+'</b>, '+d.district+' &middot; '+d.div+' division</span></div>'
      +   (d.person ? '<div>__BADGE__<span>'+d.person+(d.since?' &middot; Shada dealer since '+d.since:'')+'</span></div>' : '')
      +   (d.hours  ? '<div>__CLOCK__<span>'+d.hours+'</span></div>' : '')
      + '</div>'
      + '<div class="dlact">'
      +   '<a class="call" href="'+tel+'">__PHONE__ '+d.phone+'</a>'
      +   '<a class="wa" href="'+wa+'" target="_blank" rel="noopener">__WA__ WhatsApp</a>'
      +   '<a class="map" href="'+maps+'" target="_blank" rel="noopener">__NAV__ Directions</a>'
      + '</div></article>';
  }

  function render(){
    var out = DEALERS.filter(match);
    /* Factory first, then distributors, then retail, alphabetical inside each */
    out.sort(function(a,b){
      var r = (b.hq?2:0)+(b.type==='distributor'?1:0) - ((a.hq?2:0)+(a.type==='distributor'?1:0));
      return r || a.district.localeCompare(b.district);
    });

    var where = state.district ? state.district
              : state.div ? state.div + ' division'
              : state.q ? '"' + elInput.value.trim() + '"'
              : 'all 64 districts';
    elTitle.textContent = state.district || state.div || state.q
                        ? 'Dealers in ' + where : 'Every Shada dealer';
    elCount.textContent = out.length + (out.length===1?' dealer':' dealers')
                        + (state.district||state.div||state.q ? '' : ' listed');

    $$('#dlmap .dist path').forEach(function(p){
      p.classList.toggle('on', p.getAttribute('data-d')===state.district);
    });

    elList.innerHTML = out.length
      ? out.map(card).join('')
      : '<div class="dlnone"><h3>No dealer in '+where+' yet</h3>'
        + '<p>We deliver direct to every district, so you can still order at the same factory '
        + 'price and have it at your door in two working days. If you run a bird shop here, this '
        + 'district is open.</p><div class="btns">'
        + '<a class="btn b-brand" href="/shop/">Order direct __ARROW__</a>'
        + '<a class="btn b-line" href="#join">Become the dealer here</a></div></div>';
  }

  render();
})();
'''

def build():
    js = (JS.replace('__DATA__', DATA).replace('__DIV__', DIVJSON)
            .replace('__PIN__', I_PIN).replace('__PHONE__', I_PHONE).replace('__WA__', I_WA)
            .replace('__NAV__', I_NAV).replace('__CLOCK__', I_CLOCK).replace('__BADGE__', I_BADGE)
            .replace('__ARROW__', I_ARROW))
    js = js.replace('\n', '\n  ')

    chips = ''.join(
        f'<button class="dlchip" type="button" data-div="{esc(k)}" aria-pressed="false">{esc(k)}'
        f'<i>{len(v)}</i></button>' for k, v in DIV.items())

    body = f'''<main id="main">

<!-- ═══════════ 1 · HERO ═══════════ -->
<section class="dlhero">
  <div class="wrap">
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>Dealers</span></nav>
    <h1>Find a Shada dealer<br>near you.</h1>
    <p class="sub">Every dealer below buys at the factory and sells at the same price you would pay
    us direct. No district markup. If your district is not listed yet, we still deliver to it.</p>
    <div class="dlstats">
      <div class="dlstat"><b id="nDealers">0</b><span>Authorised dealers</span></div>
      <div class="dlstat"><b id="nDistricts">0</b><span>Districts with a counter</span></div>
      <div class="dlstat"><b id="nDivisions">0</b><span>Divisions covered</span></div>
      <div class="dlstat"><b>64</b><span>Districts we deliver to</span></div>
    </div>
  </div>
</section>

<!-- ═══════════ 2 · SEARCH AND FILTER ═══════════ -->
<div class="dlbar">
  <div class="wrap">
    <div class="dlsearch" id="dlsearch">
      {I_SEARCH}
      <input id="dlq" type="search" autocomplete="off" placeholder="Search district, shop or area">
      <button class="clr" id="dlclear" type="button" aria-label="Clear search">{I_X}</button>
    </div>
    <div class="dlchips" role="group" aria-label="Filter by division">{chips}</div>
  </div>
</div>

<!-- ═══════════ 3 · MAP AND RESULTS ═══════════ -->
<section class="bsec">
  <div class="wrap dlgrid">

    <div class="dlmapcard">
      <h2>Where we have a counter</h2>
      <p>Tap a green district to see its dealers. Grey districts have no counter yet, we deliver there direct.</p>
      <svg class="dlmap" id="dlmap" viewBox="0 0 560 791" xmlns="http://www.w3.org/2000/svg"
           role="img" aria-label="Map of Bangladesh. Districts with a Shada dealer are highlighted.">
        {MAP}
      </svg>
      <div class="dlkey">
        <span><i style="background:#9ED9B4"></i>Dealer counter</span>
        <span><i style="background:var(--ink)"></i>Selected</span>
        <span><i style="background:#E4E8E4"></i>Delivery only</span>
      </div>
    </div>

    <div>
      <div class="dlhead">
        <h2 id="dltitle">Every Shada dealer</h2>
        <span class="cnt" id="dlcount"></span>
      </div>
      <div class="dlcards" id="dlcards"></div>
    </div>

  </div>
</section>

<!-- ═══════════ 4 · BECOME A DEALER ═══════════ -->
<section class="dljoin" id="join">
  <div class="wrap">
    <div>
      <span class="eyebrow">Wholesale</span>
      <h2>Sell Shada in<br>your district.</h2>
      <p>We are opening one distributor per district. You buy at the wholesale tier, sell at the
      printed retail price, and keep the margin. No franchise fee, no target, no lock-in.</p>
      <a class="btn b-brand" href="/wholesale/">See wholesale rates {I_ARROW}</a>
    </div>
    <ul class="dljlist">
      <li>{I_TRUCK}<div><b>Delivered to your shop</b><span>Anywhere in Bangladesh, from Bhaluka, on our account above the minimum order.</span></div></li>
      <li>{I_BADGE}<div><b>Listed on this page</b><span>Your shop name, phone and directions, in front of every breeder searching your district.</span></div></li>
      <li>{I_CHECK}<div><b>One price everywhere</b><span>We hold the retail price in all 64 districts, so nobody undercuts you online.</span></div></li>
    </ul>
  </div>
</section>

</main>

<script>{js}</script>
'''
    ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Shada Bird Feed authorised dealers",
        "numberOfItems": len(DEALERS),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {
                "@type": "Store", "name": d["name"], "telephone": d["phone"],
                "address": {"@type": "PostalAddress", "streetAddress": d["area"],
                            "addressLocality": d["district"], "addressRegion": d["div"],
                            "addressCountry": "BD"},
                "brand": {"@type": "Brand", "name": "Shada Bird Feed"}}}
            for i, d in enumerate(DEALERS)]
    }
    ldjson = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    html = HEAD.replace('</head>', f'<style>{CSS}</style>\n{ldjson}\n</head>') + body + FOOT
    return html

if __name__ == '__main__':
    os.makedirs('/tmp/dealer/out', exist_ok=True)
    open('/tmp/dealer/out/dealers.html', 'w', encoding='utf-8').write(build())
    print('dealers.html', round(os.path.getsize('/tmp/dealer/out/dealers.html') / 1024), 'KB',
          '|', len(DEALERS), 'dealer record(s)')
