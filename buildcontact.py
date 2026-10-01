#!/usr/bin/env python3
# Shada Bird Feed · Contact + Thank you page generator
# Reuses the shop page shell (header, mega menus, footer) so nothing extra is needed site-wide.
import re, os, json

HEAD = open('/tmp/pg/head.txt', encoding='utf-8').read()
FOOT = open('/tmp/pg/foot.txt', encoding='utf-8').read()

WA   = '8801813323535'
PH   = '01813-323535'
MAIL = 'shadabirdfeed@gmail.com'
ADDR = 'Majorvita, Bhaluka, Mymensingh'

I = lambda p, w=1.9: ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                      f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')
I_WA    = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd">'
           '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.9a8.1 8.1 0 0 1 6.6 12.8l-.3.4.7 2.5-2.6-.7-.4.2A8.1 8.1 0 1 1 12 3.9Z"/>'
           '<path d="M9.1 7.2h.6c.2 0 .5-.1.7.5l.9 2.2c.1.1.1.3 0 .5l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.4 2.4 1.5.3.1.4.1.6-.1.1-.2.7-.9.9-1.2.2-.2.4-.2.7-.1.2.1 1.7.9 2 1 .3.1.5.2.6.4 0 .1 0 .7-.2 1.4-.2.7-1.5 1.3-2 1.4-.6.1-1.1.3-3.6-.7-3-1.3-5-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.7-2.2 1-2.5c.3-.3.6-.4.8-.4Z"/></svg>')
I_PHONE = I('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7A2 2 0 0 1 22 16.9z"/>')
I_MAIL  = I('<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m3 7 8.2 5.5a2 2 0 0 0 2.2 0L22 7"/>')
I_PIN   = I('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>')
I_CLOCK = I('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
I_TRUCK = I('<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>')
I_TAG   = I('<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>')
I_CHECK = I('<path d="M4 12.5 9.5 18 20 6.5"/>', 2.6)
I_ARROW = I('<path d="M5 12h14M12 5l7 7-7 7"/>', 2.4)
I_FB    = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/></svg>'
I_HELP  = I('<circle cx="12" cy="12" r="9"/><path d="M9.2 9.2a2.9 2.9 0 0 1 5.6 1c0 1.9-2.8 2.8-2.8 2.8M12 17h.01"/>')

CSS = '''
/* ═══════════════════════════════════════════════════════════════════
   CONTACT  ·  /contact/     and     THANK YOU  ·  /thank-you/
   Loads after 01-base.css and 02-shop-pages.css.
   Page-scoped: nothing here is used elsewhere, so it can also live in
   Elementor Page Settings CSS for these two pages only.
   Tokens come from 01-base.css.
   ═══════════════════════════════════════════════════════════════════ */

/* ── Hero. Deliberately short: the job of this page is the form. ──── */
.cthero{background:var(--ink);color:#fff;position:relative;overflow:hidden;
  padding:clamp(34px,4.4vw,60px) 0 clamp(30px,3.8vw,50px)}
.cthero::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;opacity:.07;pointer-events:none}
.cthero .wrap{position:relative}
.cthero h1{font-size:clamp(32px,4.4vw,54px);letter-spacing:-.035em;line-height:1.05;margin:10px 0 12px}
.cthero .sub{font-size:17px;line-height:1.6;color:var(--on2);max-width:54ch}

/* ── Three quick links. Most visitors want one of these, not the form. */
.ctquick{background:var(--ink);padding:0 0 clamp(30px,4vw,54px)}
.ctquick .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:13px}
@media(max-width:860px){.ctquick .wrap{grid-template-columns:1fr}}
.ctq{display:flex;gap:14px;align-items:center;background:var(--ink2);border:1px solid var(--line-d);
  border-radius:var(--r2);padding:20px 22px;text-decoration:none;color:#fff;
  transition:border-color .2s,transform .3s var(--ease)}
.ctq:hover{border-color:var(--leaf);transform:translateY(-3px)}
.ctq .ic{width:42px;height:42px;flex:0 0 auto;border-radius:11px;display:grid;place-items:center;
  background:rgba(95,212,138,.12);border:1px solid rgba(95,212,138,.22)}
.ctq .ic svg{width:20px;height:20px;color:var(--leaf)}
.ctq b{display:block;font-size:16px;letter-spacing:-.01em;margin-bottom:2px}
.ctq span{display:block;font-size:13px;color:var(--on2);line-height:1.4}
.ctq .go{margin-left:auto;width:17px;height:17px;color:var(--on2);flex:0 0 auto;transition:transform .3s var(--ease),color .2s}
.ctq:hover .go{color:var(--leaf);transform:translateX(3px)}

/* ── Body ─────────────────────────────────────────────────────────── */
.ctgrid{display:grid;grid-template-columns:1.3fr .8fr;gap:clamp(24px,3.4vw,52px);align-items:start}
@media(max-width:940px){.ctgrid{grid-template-columns:1fr}}

/* ── The form. The one thing on this page that should pull the eye:
      white card, soft lift, and a brand strip across the top. ─────── */
.ctform{background:#fff;border:1px solid var(--line);border-radius:var(--r3);
  box-shadow:0 22px 54px rgba(10,38,23,.09);overflow:hidden}
.ctform .bar{height:5px;background:linear-gradient(90deg,var(--brand),var(--leaf))}
.ctform .in{padding:clamp(24px,3.2vw,38px)}
.ctform h2{font-size:clamp(22px,2.5vw,30px);letter-spacing:-.025em;margin-bottom:7px}
.ctform .note{font-size:14.5px;color:var(--tx2);margin-bottom:26px;line-height:1.55}

.ctrow{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:560px){.ctrow{grid-template-columns:1fr}}
.ctf{margin-bottom:18px}
.ctf label{display:block;font-size:13px;font-weight:600;color:var(--tx);margin-bottom:7px;letter-spacing:.005em}
.ctf label i{font-style:normal;color:var(--tx3);font-weight:400}
.ctf label em{font-style:normal;color:var(--brand)}
.ctf input,.ctf select,.ctf textarea{width:100%;border:1.5px solid var(--line);border-radius:var(--r2);
  background:#fff;padding:0 15px;height:54px;font:500 15.5px/1 var(--ff);color:var(--tx);outline:none;
  transition:border-color .18s,box-shadow .18s;-webkit-appearance:none;appearance:none}
.ctf textarea{height:auto;min-height:140px;padding:15px;line-height:1.55;resize:vertical}
.ctf select{background-image:url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236E6E73' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 14px center;background-size:18px;padding-right:40px;cursor:pointer}
.ctf input:hover,.ctf select:hover,.ctf textarea:hover{border-color:var(--tx3)}
.ctf input:focus,.ctf select:focus,.ctf textarea:focus{border-color:var(--brand);box-shadow:0 0 0 4px rgba(8,152,48,.12)}
.ctf input::placeholder,.ctf textarea::placeholder{color:var(--tx3);font-weight:400}
.ctf.bad input,.ctf.bad select,.ctf.bad textarea{border-color:#C0392B;box-shadow:0 0 0 4px rgba(192,57,43,.1)}
.ctf .err{display:none;font-size:12.5px;color:#C0392B;margin-top:6px;font-weight:500}
.ctf.bad .err{display:block}

/* ── Searchable district picker ────────────────────────────────────
   Progressive enhancement. The markup ships a real <select> with all 64
   districts, so the field works with JavaScript off. On load the script
   hides it and builds this combobox, keeping the select in sync, so the
   form still submits a normal `district` value. */
.ctcombo{position:relative}
.ctcombo select.hid{position:absolute;opacity:0;pointer-events:none;height:0;min-height:0;width:0;padding:0;margin:0;border:0}
.cbinput{width:100%;border:1.5px solid var(--line);border-radius:var(--r2);background:#fff;
  padding:0 42px 0 15px;height:54px;font:500 15.5px/1 var(--ff);color:var(--tx);outline:none;
  transition:border-color .18s,box-shadow .18s}
.cbinput::placeholder{color:var(--tx3);font-weight:400}
.cbinput:hover{border-color:var(--tx3)}
.cbinput:focus{border-color:var(--brand);box-shadow:0 0 0 4px rgba(8,152,48,.12)}
.ctf.bad .cbinput{border-color:#C0392B;box-shadow:0 0 0 4px rgba(192,57,43,.1)}
.cbicon{position:absolute;right:15px;top:50%;transform:translateY(-50%);width:18px;height:18px;
  color:var(--tx3);pointer-events:none;transition:transform .18s}
.ctcombo.open .cbicon{transform:translateY(-50%) rotate(180deg)}

.cblist{position:absolute;z-index:30;left:0;right:0;top:calc(100% + 6px);margin:0;padding:6px;
  list-style:none;background:#fff;border:1px solid var(--line);border-radius:var(--r2);
  box-shadow:0 20px 44px rgba(10,38,23,.16);max-height:272px;overflow-y:auto;overscroll-behavior:contain}
.cblist[hidden]{display:none}
.cbopt{display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:44px;
  padding:10px 12px;border-radius:10px;font-size:15px;color:var(--tx);cursor:pointer;line-height:1.3}
.cbopt:hover,.cbopt.on{background:var(--paper2)}
.cbopt[aria-selected="true"]{color:var(--brand);font-weight:600}
.cbopt .tick{width:16px;height:16px;flex:0 0 auto;opacity:0;color:var(--brand)}
.cbopt[aria-selected="true"] .tick{opacity:1}
.cbopt mark{background:rgba(8,152,48,.16);color:inherit;border-radius:3px;padding:0 1px}
.cbnone{padding:14px 12px;font-size:14px;color:var(--tx2)}
.cbhint{font-size:12.5px;color:var(--tx3);margin-top:7px}

.ctsub{margin-top:8px;padding-top:22px;border-top:1px solid var(--line)}
.ctsub .btn{width:100%;min-height:58px;height:58px;font-size:16px}
.ctsub small{display:block;font-size:12.5px;color:var(--tx3);line-height:1.55;margin-top:14px;text-align:center}

/* ── Side column ─────────────────────────────────────────────────── */
.ctside{display:grid;gap:14px}
.ctcard{background:var(--paper2);border:1px solid var(--line);border-radius:var(--r3);padding:24px 26px}
.ctcard h3{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3);margin-bottom:16px}
.ctrows{display:grid;gap:4px}
.ctr{display:flex;gap:13px;align-items:flex-start;padding:11px 0;text-decoration:none;color:var(--tx);
  border-bottom:1px solid var(--line)}
.ctr:last-child{border-bottom:0}
.ctr svg{width:19px;height:19px;flex:0 0 auto;margin-top:2px;color:var(--brand)}
.ctr > span{text-align:left;min-width:0}
.ctr b{display:block;font-size:15.5px;font-weight:600;letter-spacing:-.01em;margin-bottom:2px}
.ctr span{display:block;font-size:13.5px;color:var(--tx2);line-height:1.45}
a.ctr:hover b{color:var(--brand)}
.ctsoc{display:flex;gap:9px;margin-top:4px}
.ctsoc a{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;border:1px solid var(--line);
  background:#fff;color:var(--tx);transition:all .18s}
.ctsoc a svg{width:19px;height:19px}
.ctsoc a:hover{border-color:var(--brand);color:var(--brand)}
.ctmap{border:1px solid var(--line);border-radius:var(--r3);overflow:hidden;background:var(--paper2)}
.ctmap iframe{display:block;width:100%;height:240px;border:0;filter:grayscale(.15)}
.ctmap .cap{padding:14px 18px;font-size:13.5px;color:var(--tx2);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.ctmap .cap a{font-weight:600;color:var(--tx)}
.ctmap .cap a:hover{color:var(--brand)}

/* ── Thank you page ──────────────────────────────────────────────
   One screen, one message. The hero fills the viewport between the
   header and the footer so the confirmation is all there is. ───────── */
.tyhero{background:var(--ink);color:#fff;position:relative;overflow:hidden;text-align:center;
  min-height:calc(100vh - var(--hh,64px));min-height:calc(100svh - var(--hh,64px));
  display:grid;place-items:center;padding:clamp(56px,8vw,110px) 0}
.tyhero::before{content:"";position:absolute;inset:0;background:var(--wing);background-size:cover;opacity:.07}
.tyhero .wrap{position:relative;max-width:720px}
.tytick{width:92px;height:92px;margin:0 auto 26px;border-radius:50%;background:var(--brand);display:grid;place-items:center}
.tytick svg{width:46px;height:46px;color:#fff}
.tyhero h1{font-size:clamp(34px,5vw,62px);letter-spacing:-.035em;line-height:1.04;margin-bottom:16px}
.tyhero p{font-size:17.5px;line-height:1.6;color:var(--on2);max-width:50ch;margin:0 auto}
.tyacts{display:flex;gap:11px;justify-content:center;flex-wrap:wrap;margin-top:32px}
@media(max-width:560px){.tyacts .btn{width:100%}}
'''

DISTRICTS = ['Bagerhat','Bandarban','Barguna','Barisal','Bhola','Bogra','Brahamanbaria','Chandpur','Chittagong',
 'Chuadanga','Comilla',"Cox's Bazar",'Dhaka','Dinajpur','Faridpur','Feni','Gaibandha','Gazipur','Gopalganj',
 'Habiganj','Jamalpur','Jessore','Jhalokati','Jhenaidah','Joypurhat','Khagrachhari','Khulna','Kishoreganj',
 'Kurigram','Kushtia','Lakshmipur','Lalmonirhat','Madaripur','Magura','Manikganj','Maulvibazar','Meherpur',
 'Moringa' if False else 'Munshiganj','Mymensingh','Naogaon','Narail','Narayanganj','Narsingdi','Natore',
 'Nawabganj','Netrakona','Nilphamari','Noakhali','Pabna','Panchagarh','Patuakhali','Pirojpur','Rajbari',
 'Rajshahi','Rangamati','Rangpur','Satkhira','Shariatpur','Sherpur','Sirajganj','Sunamganj','Sylhet',
 'Tangail','Thakurgaon']

SUBJECTS = [
    'Place an order',
    'Which formula for my bird',
    'Wholesale or dealer enquiry',
    'Delivery or an existing order',
    'A problem with a jar',
    'Something else',
]

def contact_page():
    opts = ''.join(f'<option value="{d}">{d}</option>' for d in sorted(set(DISTRICTS)))
    subs = ''.join(f'<option value="{t}">{t}</option>' for t in SUBJECTS)

    body = f'''<main id="main">

<!-- ═══════════ 1 · HERO ═══════════ -->
<section class="cthero">
  <div class="wrap">
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>Contact</span></nav>
    <h1>Contact us.</h1>
    <p class="sub">Whoever answers has hand fed a chick. Tell us the species, the age and what you
    feed now, and you will get a straight answer.</p>
  </div>
</section>

<!-- ═══════════ 2 · THREE QUICK LINKS ═══════════ -->
<section class="ctquick">
  <div class="wrap">
    <a class="ctq" href="/dealers/">
      <span class="ic">{I_PIN}</span>
      <span><b>Find a dealer</b><span>Buy over the counter in your district</span></span>
      {I_ARROW.replace('<svg ', '<svg class="go" ')}
    </a>
    <a class="ctq" href="/#faq">
      <span class="ic">{I_HELP}</span>
      <span><b>Read the FAQ</b><span>Prices, delivery and which formula to use</span></span>
      {I_ARROW.replace('<svg ', '<svg class="go" ')}
    </a>
    <a class="ctq" href="https://wa.me/{WA}?text=Dealer%20enquiry" target="_blank" rel="noopener">
      <span class="ic">{I_TAG}</span>
      <span><b>Wholesale enquiry</b><span>One distributor per district, open now</span></span>
      {I_ARROW.replace('<svg ', '<svg class="go" ')}
    </a>
  </div>
</section>

<!-- ═══════════ 3 · FORM + DETAILS ═══════════ -->
<section class="bsec tint">
  <div class="wrap ctgrid">

    <!-- Form. Plain HTML so any WordPress form plugin can take it over
         without redesigning. Keep the field names and the /thank-you/ action. -->
    <form class="ctform" id="shadaContact" method="post" action="/thank-you/" novalidate>
      <div class="bar"></div>
      <div class="in">
        <h2>Send a message</h2>
        <p class="note">Five fields. We reply on WhatsApp unless you tell us otherwise.</p>

        <div class="ctf" id="f_subject">
          <label for="c_subject">What is this about <em>*</em></label>
          <select id="c_subject" name="subject">
            <option value="">Choose one</option>{subs}
          </select>
          <span class="err">Please choose what this is about</span>
        </div>

        <div class="ctrow">
          <div class="ctf" id="f_name"><label for="c_name">Your name <em>*</em></label>
            <input id="c_name" name="name" type="text" autocomplete="name" placeholder="Write your name">
            <span class="err">Please add your name</span></div>
          <div class="ctf" id="f_phone"><label for="c_phone">Phone or WhatsApp <em>*</em></label>
            <input id="c_phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="01XXXXXXXXX">
            <span class="err">We need a number to reply to</span></div>
        </div>

        <div class="ctrow">
          <div class="ctf" id="f_district"><label for="c_district">District <em>*</em></label>
            <div class="ctcombo" id="districtCombo">
              <select id="c_district" name="district">
                <option value="">Select your district</option>{opts}
              </select>
            </div>
            <span class="err">Please choose your district</span></div>
          <div class="ctf"><label for="c_email">Email <i>optional</i></label>
            <input id="c_email" name="email" type="email" autocomplete="email" placeholder="you@example.com"></div>
        </div>

        <div class="ctf" id="f_msg"><label for="c_msg">Your message <em>*</em></label>
          <textarea id="c_msg" name="message" placeholder="Species, age of the bird, what you feed now, and what you need."></textarea>
          <span class="err">Tell us a little about the bird</span></div>

        <div class="ctsub">
          <button class="btn b-brand" type="submit">Send message {I_ARROW}</button>
          <small>Your number is used to answer this message only. We do not share it and we do not
          send marketing messages.</small>
        </div>
      </div>
    </form>

    <!-- Details -->
    <div class="ctside">

      <div class="ctcard">
        <h3>Get in touch</h3>
        <div class="ctrows">
          <a class="ctr" href="https://wa.me/{WA}" target="_blank" rel="noopener">
            {I_WA}<span><b>WhatsApp {PH}</b><span>The fastest way. Send a photo of the bird.</span></span></a>
          <a class="ctr" href="tel:+{WA}">
            {I_PHONE}<span><b>Call {PH}</b><span>Saturday to Thursday, 9am to 6pm</span></span></a>
          <a class="ctr" href="mailto:{MAIL}">
            {I_MAIL}<span><b>Email</b><span>{MAIL}</span></span></a>
          <div class="ctr">
            {I_PIN}<span><b>The factory</b><span>{ADDR}. Counter sales, no appointment needed.</span></span></div>
          <div class="ctr">
            {I_CLOCK}<span><b>Opening hours</b><span>Saturday to Thursday, 9am to 6pm. Closed Friday.</span></span></div>
        </div>
      </div>

      <div class="ctcard">
        <h3>Find us online</h3>
        <div class="ctsoc">
          <a href="https://www.facebook.com/" target="_blank" rel="noopener" aria-label="Shada Bird Feed on Facebook">{I_FB}</a>
          <a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Shada Bird Feed on WhatsApp">{I_WA}</a>
          <a href="mailto:{MAIL}" aria-label="Email Shada Bird Feed">{I_MAIL}</a>
        </div>
      </div>

      <div class="ctmap">
        <!-- Replace src with the real Google Maps embed for the factory building. -->
        <iframe title="Shada Bird Feed factory location, Bhaluka, Mymensingh" loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps?q=Bhaluka,+Mymensingh,+Bangladesh&output=embed"></iframe>
        <div class="cap"><span>{ADDR}</span>
          <a href="https://www.google.com/maps/search/?api=1&amp;query=Bhaluka%2C%20Mymensingh%2C%20Bangladesh"
             target="_blank" rel="noopener">Open in Maps</a></div>
      </div>

    </div>
  </div>
</section>

</main>

<script>
/* ═══════════════════════════════════════════════════════════════════
   CONTACT FORM
   1. Searchable district picker, built over the real <select> so the
      form still submits `district` and still works with JavaScript off.
   2. Inline validation. Nothing is sent from here: point the form at
      your form plugin, keep the field names and the /thank-you/ action.
   ═══════════════════════════════════════════════════════════════════ */
(function(){{

  /* ── 1 · searchable district picker ─────────────────────────────── */
  var wrap = document.getElementById('districtCombo');
  var sel  = document.getElementById('c_district');
  if(wrap && sel){{
    var items = [].slice.call(sel.options).filter(function(o){{ return o.value; }})
                  .map(function(o){{ return o.value; }});
    sel.classList.add('hid');
    sel.setAttribute('tabindex','-1');
    sel.setAttribute('aria-hidden','true');

    var box = document.createElement('div');
    box.innerHTML =
      '<input class="cbinput" id="cbInput" type="text" role="combobox" aria-expanded="false" ' +
      'aria-controls="cbList" aria-autocomplete="list" aria-label="District" autocomplete="off" ' +
      'placeholder="Type to search your district">' +
      '<svg class="cbicon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg>' +
      '<ul class="cblist" id="cbList" role="listbox" aria-label="Districts" hidden></ul>';
    while(box.firstChild) wrap.appendChild(box.firstChild);

    var input = document.getElementById('cbInput');
    var list  = document.getElementById('cbList');
    var TICK  = '<svg class="tick" aria-hidden="true" viewBox="0 0 24 24" fill="none" ' +
                'stroke="currentColor" stroke-width="2.6" stroke-linecap="round" ' +
                'stroke-linejoin="round"><path d="M4 12.5 9.5 18 20 6.5"/></svg>';
    var active = -1;

    function esc(t){{ return String(t).replace(/[&<>"]/g, function(c){{
      return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]; }}); }}

    /* Highlight the typed part so the match is obvious */
    function mark(name, q){{
      if(!q) return esc(name);
      var i = name.toLowerCase().indexOf(q.toLowerCase());
      if(i < 0) return esc(name);
      return esc(name.slice(0,i)) + '<mark>' + esc(name.slice(i, i+q.length)) + '</mark>' +
             esc(name.slice(i+q.length));
    }}

    function render(q){{
      q = (q || '').trim();
      var shown = items.filter(function(n){{ return n.toLowerCase().indexOf(q.toLowerCase()) > -1; }});
      if(!shown.length){{
        list.innerHTML = '<li class="cbnone">No district called &quot;' + esc(q) +
          '&quot;. We deliver everywhere, so pick the nearest one.</li>';
        active = -1; return;
      }}
      list.innerHTML = shown.map(function(n, i){{
        return '<li class="cbopt" id="cbo' + i + '" role="option" data-v="' + esc(n) + '" ' +
               'aria-selected="' + (sel.value === n) + '"><span>' + mark(n, q) + '</span>' + TICK + '</li>';
      }}).join('');
      active = -1;
    }}

    function open(){{
      if(!list.hidden) return;
      render(''); list.hidden = false;
      input.setAttribute('aria-expanded','true'); wrap.classList.add('open');
    }}
    function close(){{
      list.hidden = true; active = -1;
      input.setAttribute('aria-expanded','false'); wrap.classList.remove('open');
      input.removeAttribute('aria-activedescendant');
    }}
    function choose(name){{
      sel.value = name; input.value = name;
      sel.dispatchEvent(new Event('change', {{bubbles:true}}));
      close();
    }}
    function highlight(i){{
      var opts = list.querySelectorAll('.cbopt');
      if(!opts.length) return;
      if(i < 0) i = opts.length - 1;
      if(i >= opts.length) i = 0;
      active = i;
      [].forEach.call(opts, function(o, k){{ o.classList.toggle('on', k === i); }});
      opts[i].scrollIntoView({{block:'nearest'}});
      input.setAttribute('aria-activedescendant', opts[i].id);
    }}

    input.addEventListener('focus', open);
    input.addEventListener('click', open);
    input.addEventListener('input', function(){{
      if(list.hidden){{ list.hidden = false; input.setAttribute('aria-expanded','true'); wrap.classList.add('open'); }}
      render(input.value);
    }});
    input.addEventListener('keydown', function(e){{
      if(e.key === 'ArrowDown'){{ e.preventDefault(); if(list.hidden) open(); highlight(active + 1); }}
      else if(e.key === 'ArrowUp'){{ e.preventDefault(); if(list.hidden) open(); highlight(active - 1); }}
      else if(e.key === 'Enter'){{
        if(!list.hidden){{
          var opts = list.querySelectorAll('.cbopt');
          var pick = active > -1 ? opts[active] : (opts.length === 1 ? opts[0] : null);
          if(pick){{ e.preventDefault(); choose(pick.getAttribute('data-v')); }}
        }}
      }}
      else if(e.key === 'Escape'){{ close(); }}
    }});
    list.addEventListener('mousedown', function(e){{
      var o = e.target.closest ? e.target.closest('.cbopt') : null;
      if(!o) return;
      e.preventDefault(); choose(o.getAttribute('data-v'));
    }});
    /* Half typed text must not be left behind looking like a choice */
    input.addEventListener('blur', function(){{
      setTimeout(function(){{
        if(items.indexOf(input.value.trim()) === -1) input.value = sel.value || '';
        close();
      }}, 130);
    }});
    document.addEventListener('click', function(e){{ if(!wrap.contains(e.target)) close(); }});
  }}

  /* ── 2 · inline validation ──────────────────────────────────────── */
  var f = document.getElementById('shadaContact');
  if(!f) return;
  var req = [['f_subject','c_subject'],['f_name','c_name'],['f_phone','c_phone'],
             ['f_district','c_district'],['f_msg','c_msg']];
  f.addEventListener('submit', function(e){{
    var first = null;
    req.forEach(function(pair){{
      var w  = document.getElementById(pair[0]);
      var el = document.getElementById(pair[1]);
      var bad = !el.value.trim();
      w.classList.toggle('bad', bad);
      if(bad && !first){{
        first = (pair[1] === 'c_district' && document.getElementById('cbInput'))
                ? document.getElementById('cbInput') : el;
      }}
    }});
    if(first){{ e.preventDefault(); first.focus(); first.scrollIntoView({{block:'center',behavior:'smooth'}}); }}
  }});
  var clear = function(e){{ var w = e.target.closest('.ctf'); if(w) w.classList.remove('bad'); }};
  f.addEventListener('input', clear);
  f.addEventListener('change', clear);
}})();
</script>
'''
    head = (HEAD
        .replace('<title>Shop · Shada Bird Feed</title>', '<title>Contact · Shada Bird Feed</title>')
        .replace('<link rel="canonical" href="https://shadabirdfeed.com/shop/">',
                 '<link rel="canonical" href="https://shadabirdfeed.com/contact/">'))
    head = re.sub(r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Contact Shada Bird Feed. WhatsApp 01813-323535, call, email or send a message. Factory in Bhaluka, Mymensingh. Saturday to Thursday, 9am to 6pm."',
        head, count=1)
    ld = {"@context":"https://schema.org","@type":"ContactPage","name":"Contact Shada Bird Feed",
      "mainEntity":{"@type":"Organization","name":"Shada Bird Feed","telephone":"+"+WA,"email":MAIL,
        "address":{"@type":"PostalAddress","streetAddress":"Majorvita","addressLocality":"Bhaluka",
          "addressRegion":"Mymensingh","addressCountry":"BD"},
        "openingHoursSpecification":{"@type":"OpeningHoursSpecification",
          "dayOfWeek":["Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday"],
          "opens":"09:00","closes":"18:00"}}}
    ldjson = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    return head.replace('</head>', f'<style>{CSS}</style>\n{ldjson}\n</head>') + body + FOOT


def thankyou_page():
    body = f'''<main id="main">

<!-- ═══════════ 1 · CONFIRMATION ═══════════ -->
<section class="tyhero">
  <div class="wrap">
    <div class="tytick">{I_CHECK}</div>
    <h1>Message received.</h1>
    <p>It is with a breeder now, not a queue. If you left a WhatsApp number that is where the reply
    will come from, usually the same day.</p>
    <div class="tyacts">
      <a class="btn b-brand" href="https://wa.me/{WA}" target="_blank" rel="noopener">{I_WA} Message us now instead</a>
      <a class="btn b-white" href="/shop/">Browse the six formulas {I_ARROW}</a>
    </div>
  </div>
</section>

</main>

<script>
/* ═══════════════════════════════════════════════════════════════════
   THANK YOU · CONVERSION EVENT
   This page exists so a completed enquiry can be counted. Reaching
   /thank-you/ is the conversion. Both calls below are guarded, so
   nothing breaks if GA4 or the Meta Pixel is not installed yet.
   In GA4 mark "generate_lead" as a key event.
   ═══════════════════════════════════════════════════════════════════ */
(function(){{
  try{{ if(typeof gtag === 'function'){{ gtag('event','generate_lead',{{
    event_category:'contact', event_label:'contact form', value:1 }}); }} }}catch(e){{}}
  try{{ if(typeof fbq === 'function'){{ fbq('track','Lead'); }} }}catch(e){{}}
}})();
</script>
'''
    head = (HEAD
        .replace('<title>Shop · Shada Bird Feed</title>', '<title>Thank you · Shada Bird Feed</title>')
        .replace('<link rel="canonical" href="https://shadabirdfeed.com/shop/">',
                 '<link rel="canonical" href="https://shadabirdfeed.com/thank-you/">'))
    head = re.sub(r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Thank you. Your message has reached Shada Bird Feed and a breeder will reply, usually the same working day."',
        head, count=1)
    # Never index a thank you page: it would rank for the brand and skew conversion counts.
    head = head.replace('</head>', '<meta name="robots" content="noindex, follow">\n</head>')
    return head.replace('</head>', f'<style>{CSS}</style>\n</head>') + body + FOOT


if __name__ == '__main__':
    os.makedirs('/tmp/pg/out', exist_ok=True)
    open('/tmp/pg/out/contact.html', 'w', encoding='utf-8').write(contact_page())
    open('/tmp/pg/out/thank-you.html', 'w', encoding='utf-8').write(thankyou_page())
    for f in ('contact.html', 'thank-you.html'):
        print(f, round(os.path.getsize('/tmp/pg/out/' + f) / 1024), 'KB')
