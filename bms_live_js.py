# -*- coding: utf-8 -*-
"""The live engine. Everything derives from one in-memory store, so saving a
sale really does update the dashboard, the customer list, the profile, the
timeline and the totals. That is Single Data Entry, demonstrated rather than
described."""

ENGINE = r'''
(function () {
'use strict';

/* ═══════════════════════════════════════════════════════════════════════
   THE STORE
   One object. Orders and payments are append-only; every other number on
   every screen is computed from them. Nothing is stored twice, which is
   exactly how the real tables will work.
   ═══════════════════════════════════════════════════════════════════════ */
var GENERIC_IMG=__GENERIC__, PLUS=__PLUS__, SKUFAM=__SKUFAM__, DISTRICTS=__DISTRICTS__, TRUCK=__TRUCK__, PENCIL=__PENCIL__;
var S = { cust: __CUST__, prod: __PROD__, seq: 149, fu: __FU__, fuSeq: 0,
          /* expenses are their own ledger. Collections are never stored here:
             they are read off the customer payment rows, so the books and the
             customer profiles cannot drift apart. */
          exp: __EXP__, openCash: 94200, openBank: 612800, payable: __PAY__,
          cfg: __CFG__, log: __LOG__, raw: __RAW__, mov: __MOV__ };
/* Opening stock per pack. From here on, stock is only ever moved by a sale,
   a stock-in or a production batch, each of which writes a movement row. */
(function(){ var FIN=__FIN__; S.prod.forEach(function(p){
  var f=FIN.filter(function(x){return x.n===p.fam&&x.p===p.pack;})[0];
  p.stock = f?f.q:0; p.reorder = f?f.r:20; }); })();
function finList(){ return S.prod.map(function(p,k){ return {n:p.fam,p:p.pack,q:p.stock,r:p.reorder,k:k,arch:p.archived}; }).filter(function(x){return !x.arch;}); }
function moveStock(k, qty, type, ref){
  var p=S.prod[k]; if(!p) return;
  p.stock += qty;
  S.mov.forEach(function(m){m.isNew=false;});
  S.mov.unshift({d:'26 Sep', t:type, n:p.fam+' '+p.pack, q:qty, ref:ref, isNew:true, k:k});
}

function tk(n){ n=Math.round(n||0); var s=String(Math.abs(n)),o;
  if(s.length>3){var h=s.slice(0,-3),t=s.slice(-3),p=[];
    while(h.length>2){p.unshift(h.slice(-2));h=h.slice(0,-2);} if(h)p.unshift(h);
    o=p.join(',')+','+t;} else o=s;
  return '৳'+(n<0?'-':'')+o; }
function esc(s){ return String(s).replace(/[&<>"]/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
function num(el){ return parseFloat(String(el.value).replace(/[^0-9.-]/g,''))||0; }
function byCode(c){ return S.cust.filter(function(x){return x.code===c;})[0]; }

/* derived, never stored */
function sold(c){ return c.o.reduce(function(a,x){return a+x.t;},0); }
function paid(c){ return c.p.reduce(function(a,x){return a+x.a;},0); }
function due(c){ return sold(c)-paid(c); }
function totals(){ var s=0,p=0,n=0;
  S.cust.forEach(function(c){ s+=sold(c); p+=paid(c); n+=c.o.length; });
  return {sold:s,paid:p,due:s-p,orders:n}; }

var MON={Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11};
function pd(s){ var m=String(s).split(' '); return new Date(+m[2],MON[m[1]],+m[0]); }
var TODAY=pd('26 Sep 2026');
var RANGES={ today:[pd('26 Sep 2026'),pd('26 Sep 2026')],
             week:[pd('20 Sep 2026'),pd('26 Sep 2026')],
             month:[pd('01 Sep 2026'),pd('30 Sep 2026')],
             year:[pd('01 Jan 2026'),pd('31 Dec 2026')],
             custom:[pd('01 Jul 2026'),pd('26 Sep 2026')],
             last:[pd('01 Aug 2026'),pd('31 Aug 2026')],
             all:[pd('01 Jan 2000'),pd('31 Dec 2099')] };
var PPLABEL={month:'September 2026',last:'August 2026',year:'January to September 2026',all:'every recorded sale'};
var RLABEL={today:['Today','Saturday, 26 September 2026','Today against the last six days'],
            week:['This week','Sunday 20 to Saturday 26 September','Sales by day, this week'],
            month:['This month','1 to 26 September 2026','Sales by day, September'],
            year:['This year','January to September 2026','Sales by month, 2026'],
            custom:['Custom range','1 July to 26 September 2026','Sales by week, July to September']};
var DAYS=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'], MONS='Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ');
function addDays(d,k){ var x=new Date(d); x.setDate(x.getDate()+k); return x; }
function fmtD(d){ return d.getDate()+' '+MONS[d.getMonth()]; }
function short(n){ n=Math.round(n); if(n>=100000) return '৳'+(n/100000).toFixed(n%100000?1:0)+'L';
  if(n>=1000) return '৳'+(n/1000).toFixed(n%1000?1:0)+'K'; return '৳'+n; }
var period='month';
var acPeriod='month';

function inRange(dateStr,k){ var d=pd(dateStr),r=RANGES[k]; return d>=r[0]&&d<=r[1]; }
function periodSales(k){ var s=0,n=0;
  S.cust.forEach(function(c){ c.o.forEach(function(o){ if(inRange(o.d,k)){s+=o.t;n++;} }); });
  return {v:s,n:n}; }
function periodColl(k){ var s=0;
  S.cust.forEach(function(c){ c.p.forEach(function(p){ if(inRange(p.d,k)) s+=p.a; }); });
  return s; }
/* Buckets a date range by day, week or month, then sums orders into it.
   The previous period is the same window shifted back, so every point has a
   comparison. That is the Stripe pattern and the only way a chart answers
   "is this month better or worse". */
function buckets(start,end,gran){
  var out=[], d=new Date(start);
  while(d<=end){
    var e;
    if(gran==='day') e=new Date(d);
    else if(gran==='week'){ e=addDays(d,6); if(e>end) e=new Date(end); }
    else { e=new Date(d.getFullYear(),d.getMonth()+1,0); if(e>end) e=new Date(end); }
    out.push({s:new Date(d),e:e,v:0,n:0});
    d = gran==='day' ? addDays(d,1) : gran==='week' ? addDays(d,7) : new Date(d.getFullYear(),d.getMonth()+1,1);
  }
  return out;
}
function fillB(bk){
  S.cust.forEach(function(c){ c.o.forEach(function(o){ var d=pd(o.d);
    for(var i=0;i<bk.length;i++){ if(d>=bk[i].s && d<=bk[i].e){ bk[i].v+=o.t; bk[i].n++; break; } } }); });
  return bk;
}
function chartData(k){
  var r=RANGES[k], cur, prev, labels, tips, every=1, last=false;
  if(k==='today'){
    var s0=addDays(TODAY,-6);
    cur=fillB(buckets(s0,TODAY,'day')); prev=fillB(buckets(addDays(s0,-7),addDays(TODAY,-7),'day'));
    labels=cur.map(function(b,i){ return i===cur.length-1?'Today':DAYS[b.s.getDay()]; });
    tips=cur.map(function(b){ return DAYS[b.s.getDay()]+' '+fmtD(b.s); }); last=true;
  } else if(k==='week'){
    cur=fillB(buckets(r[0],r[1],'day')); prev=fillB(buckets(addDays(r[0],-7),addDays(r[1],-7),'day'));
    labels=cur.map(function(b){ return DAYS[b.s.getDay()]+' '+b.s.getDate(); });
    tips=cur.map(function(b){ return DAYS[b.s.getDay()]+' '+fmtD(b.s); });
  } else if(k==='month'){
    var end=TODAY; cur=fillB(buckets(r[0],end,'day'));
    var ps=new Date(r[0].getFullYear(),r[0].getMonth()-1,1), pe=new Date(ps.getFullYear(),ps.getMonth(),end.getDate());
    prev=fillB(buckets(ps,pe,'day'));
    labels=cur.map(function(b){ return String(b.s.getDate()); }); every=5;
    tips=cur.map(function(b){ return DAYS[b.s.getDay()]+' '+fmtD(b.s); });
  } else if(k==='year'){
    cur=fillB(buckets(r[0],TODAY,'month')); prev=null;
    labels=cur.map(function(b){ return MONS[b.s.getMonth()]; });
    tips=cur.map(function(b){ return MONS[b.s.getMonth()]+' '+b.s.getFullYear(); });
  } else {
    cur=fillB(buckets(r[0],r[1],'week'));
    var len=Math.round((r[1]-r[0])/86400000)+1;
    prev=fillB(buckets(addDays(r[0],-len),addDays(r[1],-len),'week'));
    labels=cur.map(function(b){ return fmtD(b.s); }); every=2;
    tips=cur.map(function(b){ return fmtD(b.s)+' to '+fmtD(b.e); });
  }
  var tot=cur.reduce(function(a,b){return a+b.v;},0), ptot=prev?prev.reduce(function(a,b){return a+b.v;},0):null;
  return {cur:cur,prev:prev,labels:labels,tips:tips,every:every,last:last,total:tot,ptotal:ptot,
          orders:cur.reduce(function(a,b){return a+b.n;},0)};
}

/* ═══════════════════════════════════════════════════════════════════════
   NUMBERS THAT ROLL, NOT JUMP
   On entering a screen a figure counts up from 0; on a change it counts from
   the old value to the new. Ease-out, 720 ms, tabular digits so the width
   never jitters. Off under reduced motion and under test automation.
   ═══════════════════════════════════════════════════════════════════════ */
var RM = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
var FMT = { tk:tk, int:function(n){ return String(Math.round(n)); }, pct:function(n){ return Math.round(n)+'%'; },
            stock:function(n){ return Math.round(n)+' in stock'; } };
function roll(id, value, fmt, ms){
  var el = typeof id==='string' ? document.getElementById(id) : id; if(!el) return;
  var f = FMT[fmt||'tk']||FMT.tk; value=+value||0;
  var from = el.dataset.v===undefined ? 0 : +el.dataset.v;
  el.dataset.v = value;
  var instant = RM || (navigator.webdriver && !window.__rollForce) || !el.offsetParent || from===value;
  if(el._raf){ cancelAnimationFrame(el._raf); el._raf=null; }
  if(instant){ el.textContent=f(value); return; }
  var ic=el.parentElement && el.parentElement.querySelector('.kl svg');
  if(ic){ ic.classList.remove('tick'); void ic.offsetWidth; ic.classList.add('tick'); }
  var dur=ms||720, t0=null;
  var step=function(t){ if(t0===null) t0=t;
    var p=Math.min((t-t0)/dur,1), e=1-Math.pow(1-p,3);
    el.textContent=f(from+(value-from)*e);
    if(p<1) el._raf=requestAnimationFrame(step); else { el.textContent=f(value); el._raf=null; } };
  el._raf=requestAnimationFrame(step);
}

/* ═══════════════════════════════════════════════════════════════════════
   TOAST
   ═══════════════════════════════════════════════════════════════════════ */
var toastEl=document.getElementById('toast'),tT;
function say(m){ if(!toastEl) return; toastEl.querySelector('span').innerHTML=m;
  toastEl.classList.add('show'); clearTimeout(tT);
  tT=setTimeout(function(){toastEl.classList.remove('show');},3600); }

/* ═══════════════════════════════════════════════════════════════════════
   CHART
   ═══════════════════════════════════════════════════════════════════════ */
var CH=null;
function chart(box,D){
  if(!box) return; CH={box:box,D:D};
  var W=box.clientWidth||760, H=240, PL=46, PR=14, PT=14, PB=26;
  var vals=D.cur.map(function(b){return b.v;}), pvals=D.prev?D.prev.map(function(b){return b.v;}):[];
  var hi=Math.max.apply(null, vals.concat(pvals,[1]));
  var raw=hi/4, pw=Math.pow(10,Math.floor(Math.log10(raw))), mm=raw/pw;
  var stepN=(mm<=1?1:mm<=2?2:mm<=2.5?2.5:mm<=5?5:10)*pw, lines=Math.ceil(hi/stepN), nice=stepN*lines;
  var n=vals.length, iw=W-PL-PR, ih=H-PT-PB;
  var X=function(i){ return PL + (n>1 ? i*iw/(n-1) : iw/2); };
  var Y=function(v){ return PT + ih - (v/nice)*ih; };
  var path=function(arr){ return arr.map(function(v,i){ return (i?'L':'M')+X(i).toFixed(1)+','+Y(v).toFixed(1); }).join(' '); };
  var line=path(vals), area=line+' L'+X(n-1).toFixed(1)+','+(PT+ih)+' L'+X(0).toFixed(1)+','+(PT+ih)+' Z';
  var g='';
  for(var k=0;k<=lines;k++){ var v=stepN*k, y=Y(v);
    g+='<line class="gl" x1="'+PL+'" y1="'+y.toFixed(1)+'" x2="'+(W-PR)+'" y2="'+y.toFixed(1)+'"/>'+
       '<text class="ax" x="'+(PL-8)+'" y="'+(y+4).toFixed(1)+'" text-anchor="end">'+short(v)+'</text>'; }
  var xl='';
  D.labels.forEach(function(l,i){ if(i%D.every===0 || i===n-1) xl+='<text class="ax" x="'+X(i).toFixed(1)+'" y="'+(H-8)+'" text-anchor="middle">'+esc(l)+'</text>'; });
  var band = D.last ? '<rect class="band" x="'+(X(n-1)-Math.max(12,iw/n/2)).toFixed(1)+'" y="'+PT+'" width="'+Math.max(24,iw/n).toFixed(1)+'" height="'+ih+'" rx="6"/>' : '';
  var dots = n<=14 ? vals.map(function(v,i){ return '<circle class="pt" cx="'+X(i).toFixed(1)+'" cy="'+Y(v).toFixed(1)+'" r="3"/>'; }).join('') : '';
  var lastPt='<circle class="dot" cx="'+X(n-1).toFixed(1)+'" cy="'+Y(vals[n-1]).toFixed(1)+'" r="4.5"/>';
  var prevLine = pvals.length ? '<path class="ln2" d="'+path(pvals)+'"/>' : '';
  box.innerHTML='<svg width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Sales chart">'+
    '<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#089830" stop-opacity=".16"/>'+
    '<stop offset="1" stop-color="#089830" stop-opacity="0"/></linearGradient></defs>'+
    band+g+xl+prevLine+'<path class="ar" d="'+area+'"/><path class="ln" d="'+line+'"/>'+dots+lastPt+
    '<line class="xh" id="chXh" x1="0" y1="'+PT+'" x2="0" y2="'+(PT+ih)+'" hidden/>'+
    '<circle class="fpt" id="chFp" r="5" hidden/><circle class="fpt2" id="chFp2" r="4" hidden/>'+
    '<rect id="chHit" x="'+PL+'" y="0" width="'+iw+'" height="'+H+'" fill="transparent"/></svg>'+
    '<div class="ctip" id="chTip" hidden></div>';
  var ln=box.querySelector('.ln'); if(ln&&ln.getTotalLength) ln.style.setProperty('--len',ln.getTotalLength());
  CH.X=X; CH.Y=Y; CH.vals=vals; CH.pvals=pvals; CH.n=n; CH.W=W; CH.PL=PL; CH.iw=iw;
}
function chartHover(px){
  if(!CH) return; var D=CH.D, i=Math.round((px-CH.PL)/(CH.iw/Math.max(CH.n-1,1)));
  i=Math.max(0,Math.min(CH.n-1,i));
  var x=CH.X(i), y=CH.Y(CH.vals[i]);
  var xh=document.getElementById('chXh'), fp=document.getElementById('chFp'), fp2=document.getElementById('chFp2'), tip=document.getElementById('chTip');
  if(!xh) return;
  xh.setAttribute('x1',x); xh.setAttribute('x2',x); xh.hidden=false;
  fp.setAttribute('cx',x); fp.setAttribute('cy',y); fp.hidden=false;
  if(CH.pvals.length){ fp2.setAttribute('cx',x); fp2.setAttribute('cy',CH.Y(CH.pvals[i])); fp2.hidden=false; } else fp2.hidden=true;
  var pv=CH.pvals.length?CH.pvals[i]:null, d=(pv!==null&&pv>0)?Math.round((CH.vals[i]-pv)/pv*100):null;
  tip.innerHTML='<div class="tt">'+esc(D.tips[i])+'</div><div class="tv">'+tk(CH.vals[i])+'</div>'+
    '<div class="tm">'+D.cur[i].n+(D.cur[i].n===1?' order':' orders')+
    (pv!==null?' · <span class="tp">'+tk(pv)+' previous'+(d!==null?' <b class="'+(d>=0?'up':'dn')+'">'+(d>=0?'▲':'▼')+' '+Math.abs(d)+'%</b>':'')+'</span>':'')+'</div>';
  tip.hidden=false;
  var bw=CH.box.clientWidth, tw=tip.offsetWidth, left=x+14; if(left+tw>bw-4) left=x-tw-14;
  tip.style.left=Math.max(4,left)+'px'; tip.style.top=Math.max(4,y-14-tip.offsetHeight/2)+'px';
}
function chartLeave(){ ['chXh','chFp','chFp2','chTip'].forEach(function(id){ var e=document.getElementById(id); if(e) e.hidden=true; }); }
document.addEventListener('pointermove',function(e){ if(e.target&&e.target.id==='chHit'){ var r=CH.box.getBoundingClientRect(); chartHover(e.clientX-r.left); } },{passive:true});
document.addEventListener('pointerleave',function(e){ if(e.target&&e.target.id==='chHit') chartLeave(); },true);
document.addEventListener('pointerout',function(e){ if(e.target&&e.target.id==='chHit') chartLeave(); },true);
var rzT; window.addEventListener('resize',function(){ clearTimeout(rzT); rzT=setTimeout(function(){ if(CH&&CH.box.offsetParent) chart(CH.box,CH.D); },120); });

/* ═══════════════════════════════════════════════════════════════════════
   RENDER · DASHBOARD
   ═══════════════════════════════════════════════════════════════════════ */
function lapsed(days){
  return S.cust.filter(function(c){
    if(!c.o.length) return false;            /* brand new is not lapsed */
    var last=c.o.map(function(o){return pd(o.d);}).sort(function(a,b){return b-a;})[0];
    return (TODAY-last)/86400000 >= days;
  }).sort(function(a,b){ return sold(b)-sold(a); });
}
function daysSince(c){
  if(!c.o.length) return null;
  var last=c.o.map(function(o){return pd(o.d);}).sort(function(a,b){return b-a;})[0];
  return Math.round((TODAY-last)/86400000);
}

/* DUES — the collections screen. due = sold − paid, same rows as everywhere else */
var duTab='all';
function oldestUnpaid(c){
  var owed=due(c); if(owed<=0) return null;
  var os=c.o.slice().sort(function(a,b){return pd(a.d)-pd(b.d);}), acc=0;
  var totalPaid=paid(c);
  for(var i=0;i<os.length;i++){ acc+=os[i].t; if(acc>totalPaid) return os[i]; }
  return os[os.length-1]||null;
}
function renderDues(){
  var tb=document.getElementById('duBody'); if(!tb) return;
  document.querySelectorAll('[data-df]').forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.df===duTab)); });
  var rows=S.cust.map(function(c){ var o=oldestUnpaid(c); var age=o?Math.round((TODAY-pd(o.d))/86400000):0;
      return {c:c,due:due(c),sold:sold(c),paid:paid(c),o:o,age:age}; }).filter(function(x){return x.due>0;});
  var total=rows.reduce(function(a,x){return a+x.due;},0);
  var old30=rows.filter(function(x){return x.age>30;}), old60=rows.filter(function(x){return x.age>60;});
  var shown=rows.filter(function(x){ return duTab==='all' || (duTab==='30'&&x.age>30) || (duTab==='60'&&x.age>60) || (duTab==='whole'&&/wholesale/i.test(x.c.tier||'')); })
                .sort(function(a,b){return b.due-a.due;});
  var set=function(id,v){var e=document.getElementById(id); if(e) e.textContent=v;};
  roll('duTotal',total); set('duTotalSub',rows.length+(rows.length===1?' customer owes':' customers owe'));
  roll('duOld',old30.reduce(function(a,x){return a+x.due;},0)); set('duOldSub',old30.length+' customers · '+tk(old60.reduce(function(a,x){return a+x.due;},0))+' over 60 days');
  var collM=0; S.cust.forEach(function(c){ c.p.forEach(function(p){ if(inRange(p.d,'month')) collM+=p.a; }); });
  roll('duColl',collM); set('duCollSub','September, all methods');
  var allSold=S.cust.reduce(function(a,c){return a+sold(c);},0), allPaid=S.cust.reduce(function(a,c){return a+paid(c);},0);
  var rate=allSold?Math.round(allPaid/allSold*100):0; roll('duRate',rate,'pct');
  set('duScope',shown.length+' of '+rows.length+' · largest first');
  tb.innerHTML = shown.length ? shown.map(function(x){ var pct=x.sold?Math.round(x.paid/x.sold*100):0; var tone=x.age>60?'bad':x.age>30?'due':'ok';
    return '<tr class="crow'+(x.c.isNew?' fresh':'')+'" data-open="'+x.c.code+'" tabindex="0">'+
      '<td><b>'+esc(x.c.name)+'</b><div class="mut">'+esc(x.c.code)+' · '+esc(x.c.district||'')+' · '+esc(x.c.phone||'')+'</div></td>'+
      '<td>'+(x.o?'<span class="mono">'+esc(x.o.inv)+'</span><div class="mut">'+esc(x.o.d)+' · <span class="pill '+tone+'">'+x.age+' days</span></div>':'<span class="mut">no invoice</span>')+'</td>'+
      '<td class="r mut">'+tk(x.sold)+'</td><td class="r">'+tk(x.paid)+'</td>'+
      '<td><div class="prog" title="paid '+tk(x.paid)+' of '+tk(x.sold)+'"><i style="width:'+pct+'%"></i></div><div class="mut" style="font-size:11.5px;margin-top:4px">paid '+pct+'%</div></td>'+
      '<td class="r"><b class="bad">'+tk(x.due)+'</b></td>'+
      '<td class="r"><button class="btn btn-xs btn-p" data-collect="'+esc(x.c.code)+'">'+CHKSVG+'Collect</button></td></tr>'; }).join('')
    : '<tr><td colspan="7"><div class="none"><b>Nobody in this filter owes anything.</b>Every taka is collected.</div></td></tr>';
}
function renderDash(){
  var ps=periodSales(period),pc=periodColl(period),T=totals();
  var pend=S.cust.reduce(function(a,c){ return a.concat(c.o.filter(function(o){return o.pending;})
      .map(function(o){ return {c:c,o:o}; })); },[]);
  var K=[[ps.v,'tk','up',ps.n+' orders in this period'],
         [pc,'tk','up',(T.sold?Math.round(pc/Math.max(ps.v,1)*100):0)+'% of period sales'],
         [T.due,'tk','fl',S.cust.filter(function(c){return due(c)>0;}).length+' customers owing'],
         [pend.length,'int','up',pend.filter(function(x){return x.o.src==='Web';}).length+' from the website'],
         [S.prod.filter(function(p){return !p.archived&&stat(p.stock,p.reorder)!=='ok';}).length,'int','fl',
          S.prod.filter(function(p){return !p.archived&&stat(p.stock,p.reorder)==='critical';}).length+' critical']];
  document.querySelectorAll('[data-kpi]').forEach(function(el,i){ if(K[i]) roll(el,K[i][0],K[i][1]); });
  document.querySelectorAll('[data-delta]').forEach(function(el,i){
    if(!K[i])return; el.className='d '+K[i][2]; el.setAttribute('data-delta',i); el.textContent=K[i][3]; });
  document.querySelectorAll('[data-period]').forEach(function(b){
    b.setAttribute('aria-pressed',String(b.dataset.period===period)); });
  var sub=document.getElementById('periodSub'); if(sub) sub.textContent=RLABEL[period][1];
  var ct=document.getElementById('chartTitle'); if(ct) ct.textContent=RLABEL[period][2];
  var D=chartData(period); chart(document.getElementById('chartBox'),D);
  var cs=document.getElementById('chartSum'); if(cs){ var d=(D.ptotal!==null&&D.ptotal>0)?Math.round((D.total-D.ptotal)/D.ptotal*100):null;
    cs.innerHTML='<b class="num">'+tk(D.total)+'</b><span class="mut"> · '+D.orders+(D.orders===1?' order':' orders')+'</span>'+
      (d!==null?' <span class="pill '+(d>=0?'ok':'bad')+'">'+(d>=0?'▲':'▼')+' '+Math.abs(d)+'% vs previous</span>'
               :(D.prev?' <span class="pill man">no previous data</span>':' <span class="pill man">no 2025 data to compare</span>')); }
  var lg=document.getElementById('chartLegend'); if(lg) lg.hidden=!(D.prev&&D.prev.length);

  /* pending orders */
  var pb=document.getElementById('pendBody');
  if(pb) pb.innerHTML = pend.length ? pend.map(function(x){
    return '<tr'+(x.o.isNew?' class="fresh"':'')+'><td><a href="#sale" class="mono" data-inv="'+esc(x.o.inv)+'">'+esc(x.o.inv)+'</a>'+
      (x.o.isNew?' <span class="pill ok">new</span>':'')+'</td>'+
      '<td><a href="#customer-profile" data-open="'+x.c.code+'"><b>'+esc(x.c.name)+'</b></a>'+
      '<div class="mut">'+esc(x.c.district)+'</div></td>'+
      '<td class="r mut">'+x.o.n+' items</td><td class="r"><b>'+tk(x.o.t)+'</b></td>'+
      '<td class="r"><span class="pill '+(x.o.src==='Web'?'web':'man')+'">'+esc(x.o.src||'Manual')+'</span></td></tr>';
  }).join('') : '<tr><td colspan="5"><div class="none"><b>No pending orders.</b>Everything is delivered.</div></td></tr>';

  /* top 10 customers */
  var tc=document.getElementById('topCust');
  if(tc) tc.innerHTML=S.cust.slice().sort(function(a,b){return sold(b)-sold(a);}).slice(0,10)
    .map(function(c,i){ var d=due(c);
      return '<tr><td><span class="rank '+(i<3?'t'+(i+1):'')+'">'+(i+1)+'</span>'+
        '<a href="#customer-profile" data-open="'+c.code+'"><b>'+esc(c.name)+'</b></a>'+
        '<div class="mut">'+esc(c.area)+', '+esc(c.district)+'</div></td>'+
        '<td class="r">'+tk(sold(c))+'</td><td class="r">'+
        (d?'<b>'+tk(d)+'</b>':'<span class="pill paid">clear</span>')+'</td></tr>'; }).join('');

  /* lapsed */
  /* bands do not overlap: each quiet customer sits in exactly one card */
  function lap(id,days,upto){ var el=document.getElementById(id); if(!el) return;
    var L=lapsed(days).filter(function(c){ return !upto || daysSince(c)<upto; });
    el.innerHTML = L.length ? L.map(function(c){
      return '<tr><td><a href="#customer-profile" data-open="'+c.code+'"><b>'+esc(c.name)+'</b></a>'+
        '<div class="mut">'+esc(c.district)+'</div></td>'+
        '<td class="r mut">'+daysSince(c)+' days</td><td class="r"><b>'+tk(sold(c))+'</b></td>'+
        '<td class="r"><a class="btn btn-xs" data-soon="Opens WhatsApp on '+esc(c.name)+
          '\u2019s number and logs the contact against their record.">'+WA+'Call</a></td></tr>'; }).join('')
      : '<tr><td colspan="4"><div class="none"><b>Nobody.</b>No customer in this range.</div></td></tr>';
    var at=L.reduce(function(t,c){return t+sold(c);},0);
    var cnt=document.getElementById(id+'Count'); if(cnt) cnt.textContent=L.length+(L.length===1?' customer':' customers')+(L.length?' \u00b7 '+tk(at)+' lifetime':''); }
  lap('lap30',30,60); lap('lap60',60,90); lap('lap90',90);
}

/* ═══════════════════════════════════════════════════════════════════════
   RENDER · CUSTOMER LIST
   ═══════════════════════════════════════════════════════════════════════ */
var TIERCLS={'Wholesale':'ok','Re-wholesale':'web','Retail':'man'};

/* The two filters are independent and both narrow the same list, so picking
   Dhaka and then typing a phone number searches inside Dhaka only. Every KPI
   above the table recomputes for whatever is on screen, which is the whole
   point: "show me Dhaka" has to answer with Dhaka's money, not the country's. */
function districts(){
  var seen={},out=[];
  S.cust.forEach(function(c){ if(!(c.district in seen)){seen[c.district]=0;out.push(c.district);} 
    seen[c.district]++; });
  out.sort();
  return out.map(function(d){return {d:d,n:seen[d]};});
}

function filtered(){
  var dv=(document.getElementById('custDistrict')||{}).value||'';
  var q=((document.getElementById('custSearch')||{}).value||'').trim().toLowerCase();
  return S.cust.filter(function(c){
    if(dv && c.district!==dv) return false;
    if(!q) return true;
    return (c.code+' '+c.name+' '+c.phone+' '+c.phone.replace(/\s/g,'')+' '+
            c.area+' '+c.district+' '+c.tier).toLowerCase().indexOf(q)>-1;
  });
}

function renderCustomers(){
  var sel=document.getElementById('custDistrict');
  if(sel && !sel.dataset.filled){
    sel.dataset.filled='1';
    sel.innerHTML='<option value="">All districts ('+S.cust.length+')</option>'+
      districts().map(function(x){
        return '<option value="'+esc(x.d)+'">'+esc(x.d)+' ('+x.n+')</option>'; }).join('');
  }

  var list=filtered().sort(function(a,b){return sold(b)-sold(a);});
  var tb=document.getElementById('custBody'); if(!tb) return;
  tb.innerHTML=list.map(function(c){ var d=due(c);
    return '<tr class="crow'+(c.isNew?' fresh':'')+'" data-code="'+c.code+'" tabindex="0">'+
      '<td><span class="mono">'+esc(c.code)+'</span></td>'+
      '<td><b>'+esc(c.name)+'</b><div class="mut">'+esc(c.area)+'</div></td>'+
      '<td class="mono mut">'+esc(c.phone)+'</td>'+
      '<td><span class="pill man">'+esc(c.district)+'</span></td>'+
      '<td><span class="pill '+TIERCLS[c.tier]+'">'+esc(c.tier)+'</span></td>'+
      '<td class="r mut">'+c.o.length+'</td>'+
      '<td class="r"><b>'+tk(sold(c))+'</b></td>'+
      '<td class="r">'+(d?'<span class="pill due">'+tk(d)+'</span>':'<span class="pill paid">clear</span>')+'</td>'+
      '<td class="r mut">'+esc(c.last)+'</td>'+
      '<td class="r"><span class="go2">›</span></td></tr>'; }).join('');

  var none=document.getElementById('custNone'); if(none) none.hidden=list.length>0;

  /* KPIs follow the filter */
  var s=0,p=0,n=0;
  list.forEach(function(c){ s+=sold(c); p+=paid(c); n+=c.o.length; });
  var owing=list.filter(function(c){return due(c)>0;}).length;
  var dv=(document.getElementById('custDistrict')||{}).value||'';
  var set=function(id,v){var e=document.getElementById(id); if(e) e.textContent=v;};
  roll('cCount',list.length,'int'); roll('cSold',s); roll('cDue',s-p);
  roll('cAvg',n?s/n:0);
  set('cOwing',owing+(owing===1?' customer owing':' customers owing'));
  set('cScope',dv?dv+' only':'All 12 customers');
  set('cCountSub',dv?('in '+dv):'active on the ledger');
  var clr=document.getElementById('custClear');
  if(clr) clr.hidden=!(dv||((document.getElementById('custSearch')||{}).value||''));

  /* district roll-up, so he can see where the money and the dues actually sit */
  var by={};
  S.cust.forEach(function(c){
    var b=by[c.district]||(by[c.district]={n:0,s:0,d:0});
    b.n++; b.s+=sold(c); b.d+=due(c); });
  var rows=Object.keys(by).sort(function(a,b){return by[b].s-by[a].s;});
  var db=document.getElementById('distBody');
  if(db) db.innerHTML=rows.map(function(k){ var b=by[k];
    return '<tr class="crow'+(dv===k?' on':'')+'" data-district="'+esc(k)+'" tabindex="0">'+
      '<td><b>'+esc(k)+'</b></td><td class="r mut">'+b.n+'</td>'+
      '<td class="r">'+tk(b.s)+'</td>'+
      '<td class="r">'+(b.d?'<span class="pill due">'+tk(b.d)+'</span>':'<span class="pill paid">clear</span>')+'</td>'+
      '<td class="r"><span class="go2">›</span></td></tr>'; }).join('');
}

/* ═══════════════════════════════════════════════════════════════════════
   FOLLOW-UPS
   Real state, not a picture of a list. Ticking one moves it to Done and the
   counts move with it, which is how the client will actually work the day.
   ═══════════════════════════════════════════════════════════════════════ */
var FUTONE={'Due reminder':'due','Win back':'bad','Reorder due':'ok','New customer':'web','Other':'man'};

function renderFollowups(){
  var open=S.fu.filter(function(f){return !f.done;});
  var done=S.fu.filter(function(f){return f.done;});
  open.sort(function(a,b){ return pd(a.when)-pd(b.when); });

  function row(f){
    var c=byCode(f.code);
    return '<tr class="'+(f.done?'is-done':'')+(f.isNew?' fresh':'')+'">'+
      '<td style="width:38px"><button class="tick'+(f.done?' on':'')+'" data-fu="'+f.id+'" '+
        'role="checkbox" aria-checked="'+(f.done?'true':'false')+'" '+
        'aria-label="Mark '+esc(f.name)+' done">'+CHK+'</button></td>'+
      '<td>'+(c?'<a href="#customer-profile" data-open="'+c.code+'"><b>'+esc(f.name)+'</b></a>'
               :'<b>'+esc(f.name)+'</b>')+
        '<div class="mut">'+esc(f.district)+'</div></td>'+
      '<td><span class="pill '+(FUTONE[f.kind]||'man')+'">'+esc(f.kind)+'</span></td>'+
      '<td class="mono mut">'+esc(f.when)+'</td>'+
      '<td class="mut">'+esc(f.note)+'</td>'+
      '<td class="r"><button class="btn btn-xs" data-call="'+f.id+'">'+WA+'Call</button></td></tr>';
  }

  var ob=document.getElementById('fuBody');
  if(ob) ob.innerHTML = open.length ? open.map(row).join('')
    : '<tr><td colspan="6"><div class="none"><b>Nothing outstanding.</b>'+
      'Every reminder in the next 7 days is handled.</div></td></tr>';
  var db=document.getElementById('fuDone');
  if(db) db.innerHTML = done.length ? done.map(row).join('')
    : '<tr><td colspan="6"><div class="none"><b>Nothing done yet today.</b>'+
      'Tick a reminder above once you have called.</div></td></tr>';

  var set=function(id,v){var e=document.getElementById(id); if(e) e.textContent=v;};
  set('fuOpen',open.length); set('fuDoneN',done.length);
  set('fuOpenSub',open.length===1?'reminder outstanding':'reminders outstanding');
  set('fuValue',tk(open.reduce(function(a,f){var c=byCode(f.code);return a+(c?due(c):0);},0)));
  var nb=document.querySelector('.nav a[href="#followups"] .nbadge');
  if(nb){ nb.textContent=open.length; nb.hidden=!open.length; }
}

function toggleFu(id){
  var f=S.fu.filter(function(x){return x.id===id;})[0]; if(!f) return;
  S.fu.forEach(function(x){x.isNew=false;});
  f.done=!f.done; f.isNew=true;
  renderFollowups();
  say(f.done ? '<b>'+esc(f.name)+'</b> marked done. Moved to today’s completed list.'
             : '<b>'+esc(f.name)+'</b> put back on the open list.');
}

function logCall(id){
  var f=S.fu.filter(function(x){return x.id===id;})[0]; if(!f) return;
  var c=byCode(f.code);
  say('Calling <b>'+esc(f.name)+'</b> on '+(c?esc(c.phone):'file')+
      '. The call is logged against the customer and the reminder rolls forward 7 days.');
  var d=pd(f.when); d.setDate(d.getDate()+7);
  var M='Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ');
  f.when=('0'+d.getDate()).slice(-2)+' '+M[d.getMonth()]+' '+d.getFullYear();
  f.note='Called on 26 Sep 2026. '+f.note;
  S.fu.forEach(function(x){x.isNew=false;}); f.isNew=true;
  renderFollowups();
}

/* the Add reminder sheet */
function fuOpenModal(){
  var sel=document.getElementById('fuCust');
  if(sel) sel.innerHTML=S.cust.slice().sort(function(a,b){return sold(b)-sold(a);})
    .map(function(c){ return '<option value="'+c.code+'">'+esc(c.name)+' · '+esc(c.code)+
      ' · '+esc(c.district)+'</option>'; }).join('');
  var n=document.getElementById('fuNote'); if(n) n.value='';
  document.getElementById('fuModal').classList.add('open');
  setTimeout(function(){ if(sel) sel.focus(); },60);
}
function fuClose(){ document.getElementById('fuModal').classList.remove('open'); }

function fuSave(){
  var code=(document.getElementById('fuCust')||{}).value;
  var kind=(document.getElementById('fuKind')||{}).value||'Other';
  var when=(document.getElementById('fuWhen')||{}).value||'27 Sep 2026';
  var note=((document.getElementById('fuNote')||{}).value||'').trim()||'No note added';
  var c=byCode(code); if(!c){ say('Pick a customer.'); return; }
  S.fu.forEach(function(x){x.isNew=false;});
  S.fuSeq++;
  S.fu.unshift({id:'fu-new-'+S.fuSeq,code:c.code,name:c.name,district:c.district,
                kind:kind,when:when,note:note,done:false,isNew:true});
  fuClose(); renderFollowups();
  say('<b>Reminder saved.</b> '+esc(c.name)+' · '+esc(kind)+' on '+esc(when)+
      ' &nbsp;<a href="#followups" style="color:#2BD255;font-weight:650">See follow-ups →</a>');
  location.hash='followups';
}

/* ═══════════════════════════════════════════════════════════════════════
   ADD CUSTOMER
   The code is generated, never typed, because a customer key a human invents
   is a duplicate waiting to happen. The phone number is checked against the
   whole book before saving for the same reason.
   ═══════════════════════════════════════════════════════════════════════ */
function nextCode(){
  var n=0;
  S.cust.forEach(function(c){ var m=/(\d+)$/.exec(c.code); if(m) n=Math.max(n,+m[1]); });
  return 'SBF-'+('00'+(n+1)).slice(-3);
}

function distSearch(q){
  var list=document.getElementById('ncDistList'); if(!list) return; q=(q||'').trim().toLowerCase();
  var hits=DISTRICTS.filter(function(d){ return !q || d.toLowerCase().indexOf(q)>-1; }).slice(0,8);
  list.innerHTML = hits.length ? hits.map(function(d,i){ return '<div class="opt'+(i===0?' on':'')+'" data-dpick="'+esc(d)+'" role="option"><div class="nm">'+esc(d)+'</div></div>'; }).join('')
    : '<div class="none" style="padding:14px"><b>No district matches.</b>All 64 are in the list.</div>';
  list.classList.add('open');
}
var editCode=null;   /* null = new customer, otherwise the code being edited */
function custOpen(){
  editCode=null;
  var f=document.getElementById('custForm'); if(f) f.reset();
  var code=document.getElementById('ncCode'); if(code) code.textContent=nextCode();
  var tt=document.getElementById('ncTitle'); if(tt) tt.textContent='New customer';
  var sb=document.getElementById('ncSave'); if(sb) sb.lastChild.textContent='Save customer';
  var sub=document.querySelector('#custModal .ch .sub'); if(sub) sub.innerHTML='Code <b class="mono" id="ncCode">'+nextCode()+'</b>, generated';
  var err=document.getElementById('ncErr'); if(err){ err.hidden=true; err.textContent=''; }
  ncTierPick('Retail'); ncBannerImg=null;
  var bp=document.getElementById('ncBannerPrev'); if(bp){ bp.hidden=true; bp.removeAttribute('src'); }
  var bd=document.getElementById('ncDrop'); if(bd) bd.classList.remove('has');
  document.getElementById('custModal').classList.add('open');
  setTimeout(function(){ var n=document.getElementById('ncName'); if(n) n.focus(); },60);
}
function custClose(){ document.getElementById('custModal').classList.remove('open'); }
function custEdit(code){
  var c=byCode(code); if(!c) return;
  custOpen(); editCode=c.code;
  var set=function(id,v){ var e=document.getElementById(id); if(e) e.value=v||''; };
  set('ncName',c.name); set('ncPhone',c.phone); set('ncShop',c.shop||''); set('ncArea',c.area===c.district?'':c.area);
  set('ncDistrict',c.district); set('ncSince',c.since); ncTierPick(c.tier||'Retail');
  if(c.banner){ ncBannerImg=c.banner; var bp=document.getElementById('ncBannerPrev'); if(bp){ bp.src=c.banner; bp.hidden=false; } var bd=document.getElementById('ncDrop'); if(bd) bd.classList.add('has'); }
  var tt=document.getElementById('ncTitle'); if(tt) tt.textContent='Edit customer';
  var sub=document.querySelector('#custModal .ch .sub'); if(sub) sub.innerHTML='<b class="mono">'+esc(c.code)+'</b> · orders and payments stay as they are';
  var sb=document.getElementById('ncSave'); if(sb) sb.lastChild.textContent='Save changes';
}
var ncBannerImg=null;

/* ═══ DATE PICKER · one component for every date field (input[data-dp], value "26 Sep 2026") ═══ */
var MONN=['January','February','March','April','May','June','July','August','September','October','November','December'];
var MONS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function fd(d){ return d.getDate()+' '+MONS[d.getMonth()]+' '+d.getFullYear(); }
var DP={el:null,input:null,y:0,m:0};
function dpOpen(input){
  dpClose();
  var cur=/^\d{1,2} [A-Z][a-z]{2} \d{4}$/.test(input.value)?pd(input.value):TODAY;
  DP.input=input; DP.y=cur.getFullYear(); DP.m=cur.getMonth();
  var el=document.createElement('div'); el.className='dp'; el.setAttribute('role','dialog'); el.setAttribute('aria-label','Pick a date');
  document.body.appendChild(el); DP.el=el; dpPaint(); dpPlace();
}
function dpPlace(){
  if(!DP.el||!DP.input) return;
  var r=DP.input.getBoundingClientRect(), h=DP.el.offsetHeight, w=DP.el.offsetWidth;
  var top=r.bottom+6; if(top+h>window.innerHeight-8) top=Math.max(8,r.top-h-6);
  var left=Math.min(r.left, window.innerWidth-w-8);
  DP.el.style.top=top+'px'; DP.el.style.left=Math.max(8,left)+'px';
}
function dpPaint(){
  var y=DP.y,m=DP.m, sel=/^\d{1,2} [A-Z][a-z]{2} \d{4}$/.test(DP.input.value)?pd(DP.input.value):null;
  var max=(DP.input.dataset.dp==='past')?TODAY:null;         /* data-dp="past": no future dates (a customer cannot start tomorrow) */
  var first=new Date(y,m,1), start=first.getDay(), days=new Date(y,m+1,0).getDate(), prevDays=new Date(y,m,0).getDate();
  var cells=[]; var i;
  for(i=start-1;i>=0;i--) cells.push({d:new Date(y,m-1,prevDays-i),o:1});
  for(i=1;i<=days;i++) cells.push({d:new Date(y,m,i),o:0});
  while(cells.length%7) cells.push({d:new Date(y,m+1,cells.length-days-start+1),o:1});
  var same=function(a,b){return a&&b&&a.getFullYear()===b.getFullYear()&&a.getMonth()===b.getMonth()&&a.getDate()===b.getDate();};
  var ch='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg>';
  var chr='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>';
  DP.el.innerHTML='<div class="dph"><button type="button" data-dpnav="-1" aria-label="Previous month">'+ch+'</button><b>'+MONN[m]+' '+y+'</b><button type="button" data-dpnav="1" aria-label="Next month">'+chr+'</button></div>'+
    '<div class="dpw7"><span>Su</span><span>Mo</span><span>Tu</span><span>We</span><span>Th</span><span>Fr</span><span>Sa</span></div>'+
    '<div class="dpg">'+cells.map(function(c){ var fut=max&&c.d>max; return '<button type="button" data-dpday="'+fd(c.d)+'" class="'+(c.o?'o ':'')+(same(c.d,TODAY)?'t ':'')+(same(c.d,sel)?'s ':'')+(fut?'f':'')+'"'+(fut?' disabled':'')+'>'+c.d.getDate()+'</button>'; }).join('')+'</div>'+
    '<div class="dpf"><div class="hint">'+(sel?fd(sel):'No date yet')+'</div><button type="button" data-dpclear>Clear</button><button type="button" class="p" data-dptoday>Today</button></div>';
}
function dpSet(v){ if(!DP.input) return; DP.input.value=v; DP.input.dispatchEvent(new Event('change',{bubbles:true})); dpClose(); }
function dpClose(){ if(DP.el){ DP.el.remove(); DP.el=null; } DP.input=null; }
document.addEventListener('click',function(e){
  var t=e.target;
  var inp=t.closest&&t.closest('input[data-dp]'); if(inp){ e.preventDefault(); if(DP.input===inp) dpClose(); else dpOpen(inp); return; }
  if(!DP.el) return;
  if(t.closest('.dp')){
    var nav=t.closest('[data-dpnav]'); if(nav){ DP.m+=+nav.dataset.dpnav; if(DP.m<0){DP.m=11;DP.y--;} if(DP.m>11){DP.m=0;DP.y++;} dpPaint(); dpPlace(); return; }
    var day=t.closest('[data-dpday]'); if(day&&!day.disabled){ dpSet(day.dataset.dpday); return; }
    if(t.closest('[data-dptoday]')){ dpSet(fd(TODAY)); return; }
    if(t.closest('[data-dpclear]')){ dpSet(''); return; }
    return;
  }
  dpClose();
},true);
document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&DP.el) dpClose(); });
window.addEventListener('resize',dpPlace); window.addEventListener('scroll',dpPlace,true);
function ncTierNow(){ var b=document.querySelector('[data-nctier][aria-pressed="true"]'); return b?b.dataset.nctier:'Retail'; }
function ncTierPick(t){ document.querySelectorAll('[data-nctier]').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.nctier===t?'true':'false'); }); }
function ncBannerPick(f){
  if(!f) return;
  if(f.size>2*1024*1024){ var err=document.getElementById('ncErr'); if(err){err.textContent='That picture is over 2 MB. Pick a smaller one.'; err.hidden=false;} return; }
  var rd=new FileReader(); rd.onload=function(){ ncBannerImg=rd.result; var p=document.getElementById('ncBannerPrev'); if(p){ p.src=ncBannerImg; p.hidden=false; } var d=document.getElementById('ncDrop'); if(d) d.classList.add('has'); }; rd.readAsDataURL(f);
}

function custSave(){
  var v=function(id){ return ((document.getElementById(id)||{}).value||'').trim(); };
  var name=v('ncName'), phone=v('ncPhone'), district=v('ncDistrict'),
      area=v('ncArea'), tier=ncTierNow(), since=v('ncSince')||'26 Sep 2026', shop=v('ncShop');
  var err=document.getElementById('ncErr');
  var fail=function(m){ if(err){err.textContent=m; err.hidden=false;} };

  if(name.length<2) return fail('Enter the customer name.');
  if(phone.replace(/\D/g,'').length<11) return fail('A Bangladeshi mobile number is 11 digits.');
  var dm=DISTRICTS.filter(function(d){return d.toLowerCase()===district.toLowerCase();})[0];
  if(!dm) return fail('Pick a district from the list. Every report groups by it, so it has to be spelt one way.');
  district=dm;
  var dupe=S.cust.filter(function(c){
    return c.code!==editCode && c.phone.replace(/\D/g,'')===phone.replace(/\D/g,''); })[0];
  if(dupe) return fail('That number already belongs to '+dupe.name+' ('+dupe.code+').');

  if(editCode){                                      /* ── update in place; the ledger is untouched */
    var ec=byCode(editCode); if(!ec) return;
    var before={name:ec.name,phone:ec.phone,shop:ec.shop||'',area:ec.area,district:ec.district,tier:ec.tier,since:ec.since,banner:!!ec.banner};
    ec.name=name; ec.phone=phone; ec.shop=shop; ec.area=area||district; ec.district=district; ec.tier=tier; ec.since=since; ec.banner=ncBannerImg;
    var after={name:ec.name,phone:ec.phone,shop:ec.shop||'',area:ec.area,district:ec.district,tier:ec.tier,since:ec.since,banner:!!ec.banner};
    var changed=Object.keys(after).filter(function(k){return String(before[k])!==String(after[k]);});
    if(changed.length){
      S.log.unshift({when:'26 Sep '+new Date().toTimeString().slice(0,5), who:'Anowar Bhai', what:'Edited customer '+ec.name+' ('+ec.code+'): '+changed.join(', '),
        before:changed.map(function(k){return k+': '+before[k];}).join(' · '), after:changed.map(function(k){return k+': '+after[k];}).join(' · '), isNew:true});
    }
    custClose(); editCode=null;
    var sel2=document.getElementById('custDistrict'); if(sel2){ sel2.dataset.filled=''; }
    renderCustomers(); renderDash(); renderNotifs(); current=ec.code; renderProfile(); renderTimeline();
    if(typeof renderSettings==='function') renderSettings();
    say(changed.length?'<b>'+esc(ec.name)+' updated</b> · '+esc(changed.join(', '))+' · logged':'No changes to save.');
    return;
  }

  S.cust.forEach(function(c){ c.isNew=false;
    c.o.forEach(function(o){o.isNew=false;}); c.p.forEach(function(p){p.isNew=false;}); });

  var c={code:nextCode(), name:name, phone:phone, district:district,
         area:area||district, tier:tier, since:since, last:'', o:[], p:[], isNew:true, shop:shop, banner:ncBannerImg};
  S.cust.push(c);

  custClose();
  var sel=document.getElementById('custDistrict');
  if(sel){ sel.dataset.filled=''; }        /* the district list has a new entry */
  renderCustomers(); renderDash(); renderNotifs();
  current=c.code; renderProfile(); renderTimeline();

  say('<b>'+esc(c.name)+' added</b> as '+esc(c.code)+' · '+esc(c.tier)+' · '+esc(c.district)+
      ' &nbsp;<a href="#sales-entry" data-sell="'+c.code+'" style="color:#2BD255;font-weight:650">'+
      'Record their first sale →</a>');
  location.hash='customers';
}

/* ═══════════════════════════════════════════════════════════════════════
   ACCOUNTS
   Cash and bank are opening balance plus collections minus expenses, computed
   on every render. Receivable is the same due figure the dashboard shows.
   Nothing here is a second copy of a number kept somewhere else.
   ═══════════════════════════════════════════════════════════════════════ */
function collections(){
  var out=[];
  S.cust.forEach(function(c){ c.p.forEach(function(p){
    out.push({d:p.d,kind:'Collection',who:c.name+' · '+p.m,t:'in',a:p.a,
              acc:(p.m==='Bank transfer'?'Bank':'Cash'),code:c.code,isNew:p.isNew}); }); });
  return out;
}
function ledger(){
  return collections().concat(S.exp).sort(function(a,b){
    return (b.isNew?1:0)-(a.isNew?1:0) || pd(b.d)-pd(a.d); });
}
function balances(){
  var cash=S.openCash, bank=S.openBank, expMonth=0;
  ledger().forEach(function(x){
    var v = x.t==='in' ? x.a : -x.a;
    if(x.acc==='Bank') bank+=v; else cash+=v;
    if(x.t==='out' && inRange(x.d,'month')) expMonth+=x.a; });
  return {cash:cash,bank:bank,exp:expMonth};
}

function renderAccounts(){
  var ALL=ledger(), B=balances();
  var L=ALL.filter(function(x){ return inRange(x.d,acPeriod); });
  var recv=S.cust.reduce(function(a,c){return a+Math.max(due(c),0);},0);
  var owing=S.cust.filter(function(c){return due(c)>0;}).length;
  var pay=S.payable.reduce(function(a,p){return a+p.v;},0);
  var todayIn=0, todayOut=0, perIn=0, perOut=0;
  ALL.forEach(function(x){ if(inRange(x.d,'today')){ if(x.t==='in') todayIn+=x.a; else todayOut+=x.a; } });
  L.forEach(function(x){ if(x.t==='in') perIn+=x.a; else perOut+=x.a; });

  document.querySelectorAll('[data-acper]').forEach(function(b){
    b.setAttribute('aria-pressed', String(b.dataset.acper===acPeriod)); });
  var sub=document.getElementById('acSub'); if(sub) sub.textContent=RLABEL[acPeriod][1];

  var set=function(id,v){var e=document.getElementById(id); if(e) e.textContent=v;};
  roll('acCash',B.cash); roll('acBank',B.bank);
  roll('acColl',perIn);  roll('acExp',perOut);
  roll('acRecv',recv);   roll('acPay',pay);
  set('acCollD', L.filter(function(x){return x.t==='in';}).length+' collections in this period');
  set('acExpD',  L.filter(function(x){return x.t==='out';}).length+' payments out in this period');
  set('acCashD', todayIn?('+'+tk(todayIn)+' collected today'):'no collection today');
  set('acBankD', todayOut?('-'+tk(todayOut)+' paid out today'):'nothing paid out today');
  set('acRecvD', owing+(owing===1?' customer owing':' customers owing'));
  set('acPayD', S.payable.length+' suppliers');

  var tb=document.getElementById('acBody');
  var cnt=document.getElementById('acCount');
  if(cnt) cnt.textContent=L.length+(L.length===1?' transaction':' transactions');
  if(tb) tb.innerHTML = L.length ? L.slice(0,20).map(function(x){
    return '<tr'+(x.isNew?' class="fresh"':'')+'><td class="mut">'+esc(x.d)+'</td>'+
      '<td>'+esc(x.kind)+(x.isNew?' <span class="pill ok">new</span>':'')+'</td>'+
      '<td>'+(x.code?'<a href="#customer-profile" data-open="'+x.code+'">'+esc(x.who)+'</a>'
                    :esc(x.who))+'</td>'+
      '<td class="r"><b style="color:'+(x.t==='in'?'var(--brand)':'var(--bad)')+'">'+
        (x.t==='in'?'+':'-')+tk(x.a)+'</b></td>'+
      '<td class="r"><span class="pill man">'+esc(x.acc)+'</span></td></tr>'; }).join('')
    : '<tr><td colspan="5"><div class="none"><b>Nothing in this period.</b>'+
      'Widen the range, or record a collection or an expense.</div></td></tr>';

  var pb=document.getElementById('acPayBody');
  if(pb) pb.innerHTML=S.payable.map(function(p){
    return '<tr><td>'+esc(p.n)+'</td><td class="r"><b>'+tk(p.v)+'</b></td>'+
      '<td class="r"><span class="pill '+(p.w.indexOf('today')>-1?'due':'man')+'">'+esc(p.w)+
      '</span></td></tr>'; }).join('');
}

/* ── the two sheets ─────────────────────────────────────────────────────── */
function colOpen(code, inv){
  var sel=document.getElementById('coCust');
  if(sel) sel.innerHTML=S.cust.filter(function(c){return due(c)>0;})
    .sort(function(a,b){return due(b)-due(a);})
    .map(function(c){ return '<option value="'+c.code+'">'+esc(c.name)+' · '+esc(c.code)+
      ' · '+tk(due(c))+' due</option>'; }).join('')
    || '<option value="">Nobody owes anything</option>';
  if(sel && code) sel.value=code;
  colSync();
  if(inv){ var ci=document.getElementById('coInv'); if(ci){ ci.value=inv; } var x=findSale(inv); var ca=document.getElementById('coAmt');
    if(x&&ca){ ca.value=x.o.t-x.o.p; ca.dataset.touched='1'; } }
  var e=document.getElementById('coErr'); if(e){e.hidden=true;e.textContent='';}
  document.getElementById('colModal').classList.add('open');
  setTimeout(function(){ if(sel) sel.focus(); },60);
}
function colSync(){
  var c=byCode((document.getElementById('coCust')||{}).value);
  var inv=document.getElementById('coInv');
  var d=document.getElementById('coDue');
  if(d) d.textContent=c?tk(due(c)):tk(0);
  if(inv) inv.innerHTML=c?c.o.filter(function(o){return o.t-o.p>0;})
    .map(function(o){ return '<option value="'+o.inv+'">'+esc(o.inv)+' · '+
      tk(o.t-o.p)+' outstanding</option>'; }).join('')+
    '<option value="On account">On account, oldest invoice first</option>'
    : '<option value="On account">On account</option>';
  var amt=document.getElementById('coAmt');
  if(amt && c && !amt.dataset.touched) amt.value=due(c);
}
function colClose(){ document.getElementById('colModal').classList.remove('open'); }

function colSave(){
  var c=byCode((document.getElementById('coCust')||{}).value);
  var a=num(document.getElementById('coAmt')||{value:0});
  var m=(document.getElementById('coMethod')||{}).value||'Cash';
  var inv=(document.getElementById('coInv')||{}).value||'On account';
  var err=document.getElementById('coErr');
  var fail=function(t){ if(err){err.textContent=t;err.hidden=false;} };
  if(!c) return fail('Pick a customer.');
  if(a<=0) return fail('Enter an amount greater than zero.');
  if(a>due(c)) return fail(c.name+' only owes '+tk(due(c))+'. Overpayment is Phase 4.');

  S.cust.forEach(function(x){ x.isNew=false;
    x.o.forEach(function(o){o.isNew=false;}); x.p.forEach(function(p){p.isNew=false;}); });
  S.exp.forEach(function(x){x.isNew=false;});

  c.p.push({d:'26 Sep 2026',m:m,a:a,inv:inv,isNew:true});
  /* settle the oldest unpaid invoice first, the way the ledger actually works */
  var left=a;
  var named=c.o.filter(function(o){return o.inv===inv;})[0];
  if(named){ var take0=Math.min(named.t-named.p,left); if(take0>0){ named.p+=take0; left-=take0; } }
  c.o.slice().sort(function(x,y){return pd(x.d)-pd(y.d);}).forEach(function(o){
    if(left<=0) return; var owe=o.t-o.p; if(owe<=0) return;
    var take=Math.min(owe,left); o.p+=take; left-=take; });

  colClose();
  renderAccounts(); renderDash(); renderCustomers(); renderSales(); renderSale(); renderDues();
  current=c.code; renderProfile(); renderTimeline(); renderNotifs();
  var amt=document.getElementById('coAmt'); if(amt) amt.dataset.touched='';
  say('<b>'+tk(a)+' collected</b> from '+esc(c.name)+' by '+esc(m)+'. Their due is now '+
      tk(due(c))+' &nbsp;<a href="#customer-profile" data-open="'+c.code+
      '" style="color:#2BD255;font-weight:650">View customer →</a>');
  /* stay where the payment was recorded: order page, profile, dues, accounts. Anywhere else goes to Dues. */
  if(['#sale','#customer-profile','#dues','#accounts','#customer-timeline'].indexOf(location.hash)<0) location.hash='dues';
}

function expOpen(){
  var f=document.getElementById('expForm'); if(f) f.reset();
  var e=document.getElementById('exErr'); if(e){e.hidden=true;e.textContent='';}
  document.getElementById('expModal').classList.add('open');
  setTimeout(function(){ var d=document.getElementById('exDetail'); if(d) d.focus(); },60);
}
function expClose(){ document.getElementById('expModal').classList.remove('open'); }

function expSave(){
  var cat=(document.getElementById('exCat')||{}).value||'Other';
  var det=(((document.getElementById('exDetail')||{}).value)||'').trim();
  var a=num(document.getElementById('exAmt')||{value:0});
  var acc=(document.getElementById('exAcc')||{}).value||'Cash';
  var err=document.getElementById('exErr');
  var fail=function(t){ if(err){err.textContent=t;err.hidden=false;} };
  if(det.length<3) return fail('Describe the expense so it is readable a year later.');
  if(a<=0) return fail('Enter an amount greater than zero.');
  var B=balances();
  if(acc==='Cash' && a>B.cash) return fail('Cash in hand is '+tk(B.cash)+'. Not enough to cover this.');
  if(acc==='Bank' && a>B.bank) return fail('Bank balance is '+tk(B.bank)+'. Not enough to cover this.');

  S.exp.forEach(function(x){x.isNew=false;});
  S.cust.forEach(function(x){ x.p.forEach(function(p){p.isNew=false;}); });
  S.exp.unshift({d:'26 Sep 2026',kind:'Expense',who:cat+' · '+det,t:'out',a:a,acc:acc,isNew:true});

  expClose(); renderAccounts(); renderDash();
  say('<b>'+tk(a)+' expense recorded</b> · '+esc(cat)+' · paid from '+esc(acc)+
      '. '+esc(acc)+' balance is now '+tk(acc==='Cash'?balances().cash:balances().bank));
  location.hash='accounts';
}

/* ═══════════════════════════════════════════════════════════════════════
   SETTINGS
   Editable, and Save writes the before and after of every changed field into
   the activity log. That is the client's Stage 2.8 requirement, demonstrated
   rather than described: change the invoice prefix, save, read it back.
   ═══════════════════════════════════════════════════════════════════════ */
var setTab='company';

function renderSettings(){
  document.querySelectorAll('[data-stab]').forEach(function(b){
    b.setAttribute('aria-pressed', String(b.dataset.stab===setTab)); });
  document.querySelectorAll('[data-spanel]').forEach(function(pnl){
    pnl.hidden = pnl.dataset.spanel!==setTab;
    if(!pnl.hidden){ pnl.style.animation='none'; void pnl.offsetWidth; pnl.style.animation=''; } });

  /* fields read from the store every time, so Cancel is just "do not save" */
  document.querySelectorAll('[data-cfg]').forEach(function(el){
    var k=el.dataset.cfg.split('.');
    var v=(S.cfg[k[0]]||{})[k[1]];
    if(v!==undefined && document.activeElement!==el) el.value=v; });

  var lb=document.getElementById('logBody');
  if(lb) lb.innerHTML=S.log.slice(0,14).map(function(r){
    return '<tr'+(r.isNew?' class="fresh"':'')+'><td class="mut mono">'+esc(r.when)+'</td>'+
      '<td>'+esc(r.who)+'</td><td>'+esc(r.what)+(r.isNew?' <span class="pill ok">new</span>':'')+'</td>'+
      '<td class="r mut">'+esc(r.before)+'</td><td class="r"><b>'+esc(r.after)+'</b></td></tr>'; }).join('');
  var lc=document.getElementById('logCount');
  if(lc) lc.textContent=S.log.length+' entries';
  var dirty=document.getElementById('setDirty');
  if(dirty) dirty.textContent=changedFields().length
    ? changedFields().length+' unsaved change'+(changedFields().length===1?'':'s')
    : 'No unsaved changes';
}

function changedFields(){
  var out=[];
  document.querySelectorAll('[data-cfg]').forEach(function(el){
    var k=el.dataset.cfg.split('.');
    var was=(S.cfg[k[0]]||{})[k[1]];
    if(was!==undefined && String(el.value)!==String(was))
      out.push({el:el,sec:k[0],key:k[1],label:el.dataset.label||k[1],was:was,now:el.value}); });
  return out;
}

function settingsSave(){
  var ch=changedFields();
  if(!ch.length){ say('Nothing to save. No field on this screen has changed.'); return; }
  S.log.forEach(function(r){r.isNew=false;});
  var t=new Date(), hh=('0'+t.getHours()).slice(-2), mm=('0'+t.getMinutes()).slice(-2);
  ch.forEach(function(c){
    S.cfg[c.sec][c.key]=c.now;
    S.log.unshift({when:'26 Sep '+hh+':'+mm, who:'Anowar Bhai',
                   what:'Changed '+c.label, before:String(c.was)||'—', after:String(c.now),
                   isNew:true}); });
  renderSettings();
  say('<b>'+ch.length+' setting'+(ch.length===1?'':'s')+' saved.</b> '+
      esc(ch.map(function(c){return c.label;}).join(', '))+
      ' · written to the activity log with the value before and after.');
  setTab='log'; renderSettings();
}

function settingsBackup(){
  say('<b>Backup prepared.</b> 20 tables, '+
      (S.cust.length+' customers, '+S.cust.reduce(function(a,c){return a+c.o.length;},0)+
       ' orders, '+S.exp.length+' expenses')+
      ' · downloads as SQL. Phase 9 also runs this nightly to off-site storage.');
}

/* ═══════════════════════════════════════════════════════════════════════
   INVENTORY
   The tabs filter, they do not decorate. Status is derived from stock against
   the reorder level, never stored, so it cannot go stale.
   ═══════════════════════════════════════════════════════════════════════ */
var invTab='all';
function stat(q,r){ return q<=r*0.5 ? 'critical' : (q<=r ? 'low' : 'ok'); }
var STONE={critical:'bad',low:'due',ok:'ok'};

function renderRawAndMoves(){
  var rb=document.getElementById('invRawBody');
  if(rb) rb.innerHTML = S.raw.map(function(x){ var st=stat(x.q,x.r);
    return '<tr><td>'+esc(x.n)+'</td><td class="r mut">'+esc(x.u)+'</td>'+
      '<td class="r"><b>'+x.q+'</b></td><td class="r mut">'+x.r+'</td>'+
      '<td class="r"><span class="pill '+STONE[st]+'">'+st+'</span></td></tr>'; }).join('');
  var rc=document.getElementById('invRawCount'); if(rc) rc.textContent=S.raw.filter(function(x){return stat(x.q,x.r)!=='ok';}).length+' of '+S.raw.length+' need attention';
  var mb=document.getElementById('invMovBody');
  if(mb) mb.innerHTML=S.mov.slice(0,12).map(function(x){
    return '<tr'+(x.isNew?' class="fresh"':'')+'><td class="mut">'+esc(x.d)+'</td>'+
      '<td><span class="pill '+(x.t==='In'?'web':'man')+'">'+esc(x.t)+'</span></td>'+
      '<td>'+esc(x.n)+'</td><td class="r"><b>'+(x.q>0?'+':'')+x.q+'</b></td>'+
      '<td class="mut">'+esc(x.ref)+'</td></tr>'; }).join('');
}
function renderInventory(){
  renderRawAndMoves();
  if(!document.getElementById('v-inventory')) return;
  document.querySelectorAll('[data-inv]').forEach(function(b){
    b.setAttribute('aria-pressed', String(b.dataset.inv===invTab)); });

  var below = invTab==='below';
  var fin=finList().filter(function(x){ return !below || stat(x.q,x.r)!=='ok'; });
  var raw=S.raw.filter(function(x){ return !below || stat(x.q,x.r)!=='ok'; });

  var show=function(id,on){ var e=document.getElementById(id); if(e) e.hidden=!on; };
  show('invFin', invTab==='all'||invTab==='fin'||below);
  show('invRaw', invTab==='all'||invTab==='raw'||below);
  show('invMov', invTab==='all'||invTab==='mov');

  var fb=document.getElementById('invFinBody');
  if(fb) fb.innerHTML = fin.length ? fin.map(function(x){ var st=stat(x.q,x.r);
    var pr=S.prod[x.k];
    return '<tr class="crow'+(pr&&pr.isNew?' fresh':'')+'" data-prod="'+x.k+'" tabindex="0">'+
      '<td><b>'+esc(x.n)+'</b></td><td class="mut">'+esc(x.p)+'</td>'+
      '<td class="r"><b class="'+(pr&&pr.bump?'bump':'')+'">'+x.q+'</b></td><td class="r mut">'+x.r+'</td>'+
      '<td class="r"><span class="pill '+STONE[st]+'">'+st+'</span></td>'+
      '<td class="r"><button class="btn btn-xs" data-stockin="'+x.k+'">'+PLUS+'Stock in</button></td></tr>'; }).join('')
    : '<tr><td colspan="6"><div class="none"><b>Everything is above reorder level.</b>'+
      'No finished product needs attention.</div></td></tr>';
  S.prod.forEach(function(pp){pp.bump=false;});

  var rb=document.getElementById('invRawBody');
  if(rb) rb.innerHTML = raw.length ? raw.map(function(x){ var st=stat(x.q,x.r);
    return '<tr><td>'+esc(x.n)+'</td><td class="r mut">'+esc(x.u)+'</td>'+
      '<td class="r"><b>'+x.q+'</b></td><td class="r mut">'+x.r+'</td>'+
      '<td class="r"><span class="pill '+STONE[st]+'">'+st+'</span></td></tr>'; }).join('')
    : '<tr><td colspan="5"><div class="none"><b>Everything is above reorder level.</b>'+
      'No raw material needs attention.</div></td></tr>';

  var mb=document.getElementById('invMovBody');
  if(mb) mb.innerHTML=S.mov.map(function(x){
    return '<tr'+(x.isNew?' class="fresh"':'')+'><td class="mut">'+esc(x.d)+'</td>'+
      '<td><span class="pill '+(x.t==='In'?'web':'man')+'">'+esc(x.t)+'</span></td>'+
      '<td>'+esc(x.n)+'</td><td class="r"><b>'+(x.q>0?'+':'')+x.q+'</b></td>'+
      '<td class="mut">'+esc(x.ref)+'</td></tr>'; }).join('');

  var alerts=finList().concat(S.raw).filter(function(x){return stat(x.q,x.r)!=='ok';});
  var crit=alerts.filter(function(x){return stat(x.q,x.r)==='critical';}).length;
  var set=function(id,v){var e=document.getElementById(id); if(e) e.textContent=v;};
  roll('invBelow',alerts.length,'int'); set('invCrit',crit+' critical');
  set('invFinCount',fin.length+' of '+S.prod.length+' packs');
  var units=S.prod.reduce(function(a,p){return a+p.stock;},0);
  roll('invUnits',units,'int'); set('invUnitsSub',S.prod.length+' packs on the shelf');
  set('invRawCount',raw.length+' of '+S.raw.length+' materials');
  var nb=document.querySelector('.nav a[href="#inventory"] .nbadge');
  if(nb) nb.textContent=alerts.length;
}

/* ═══════════════════════════════════════════════════════════════════════
   PRODUCTS
   Units, revenue and the buyer list are read off the sale lines, so a product
   page and a customer page can never disagree. Sell something on the sale
   screen and it appears here in the same breath.
   ═══════════════════════════════════════════════════════════════════════ */
function prodStats(k, period){
  var units=0, rev=0, orders=0, buyers={}, rows=[];
  S.cust.forEach(function(c){ c.o.forEach(function(o){
    if(period && !inRange(o.d, period)) return;
    (o.it||[]).forEach(function(it){
      if(it.k!==k) return;
      units+=it.q; rev+=it.t; orders++;
      var b=buyers[c.code]||(buyers[c.code]={c:c,q:0,v:0,n:0});
      b.q+=it.q; b.v+=it.t; b.n++;
      rows.push({c:c,o:o,it:it});
    }); }); });
  var bl=Object.keys(buyers).map(function(k2){return buyers[k2];})
          .sort(function(a,b){return b.v-a.v;});
  rows.sort(function(a,b){ return (b.o.isNew?1:0)-(a.o.isNew?1:0) || pd(b.o.d)-pd(a.o.d); });
  return {units:units, rev:rev, orders:orders, buyers:bl, rows:rows};
}

var ppTab='year', pfTab='all';
function renderProducts(){
  var grid=document.getElementById('prodGrid'); if(!grid) return;
  renderRawAndMoves();
  document.querySelectorAll('[data-pp]').forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.pp===ppTab)); });
  document.querySelectorAll('[data-pf]').forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.pf===pfTab)); });
  var live=S.prod.map(function(p,k){ var st=prodStats(k, ppTab); st.k=k; st.p=p; return st; }).filter(function(x){return !x.p.archived;});
  var stats=live.slice().sort(function(a,b){return b.rev-a.rev || b.units-a.units;});
  var maxRev=Math.max.apply(null, stats.map(function(x){return x.rev;}))||1;
  var byRev=stats;
  var rank={}; byRev.forEach(function(x,i){ rank[x.k]=i+1; });
  var shown = pfTab==='archived' ? S.prod.map(function(p,k){ var st=prodStats(k, ppTab); st.k=k; st.p=p; return st; }).filter(function(x){return x.p.archived;})
            : pfTab==='below' ? stats.filter(function(x){ return stat(x.p.stock,x.p.reorder)!=='ok'; })
            : stats;
  var sc=document.getElementById('pgScope'); if(sc) sc.textContent=PPLABEL[ppTab]||'';
  if(!shown.length){ grid.innerHTML='<div class="none" style="grid-column:1/-1"><b>'+(pfTab==='archived'?'No archived packs.':pfTab==='below'?'Nothing below its reorder level.':'No packs yet.')+'</b>'+(pfTab==='archived'?'Archive a pack from its Edit sheet; it stays here with its history.':pfTab==='below'?'Every pack has enough stock for now.':'')+'</div>'; }
  else grid.innerHTML=shown.map(function(x){
    var st = stat(x.p.stock,x.p.reorder);
    return '<button class="pcard'+(x.p.isNew?' fresh':'')+(x.p.archived?' arch':'')+'" data-prod="'+x.k+'">'+
      '<span class="pimg"><img src="'+x.p.img+'" alt="'+esc(x.p.fam)+'" loading="lazy"></span>'+
      '<span class="pbody">'+
        '<span class="pname">'+esc(x.p.fam)+'</span>'+
        '<span class="ppack"><span class="mono">'+esc(x.p.sku||'')+'</span> · '+esc(x.p.pack)+' · retail '+tk(x.p.r)+' · wholesale '+tk(x.p.w)+'</span>'+
        '<span class="pbar"><i style="width:'+Math.max(4,Math.round(x.rev/maxRev*100))+'%"></i></span>'+
        '<span class="pmeta"><b>'+tk(x.rev)+'</b><span class="mut">'+x.units+' units · '+
          x.buyers.length+' buyers</span>'+
          '<span class="ptags">'+
            (x.p.archived?'<span class="pill bad">Archived</span>':(rank[x.k]<=3&&x.rev>0?'<span class="pill ok">#'+rank[x.k]+'</span>':''))+
            '<span class="pill '+STONE[st]+'" title="Reorder at '+x.p.reorder+'">'+x.p.stock+' in stock'+(st!=='ok'?' · reorder at '+x.p.reorder:'')+'</span>'+
          '</span></span>'+
      '</span>'+
      '<span class="go2">›</span></button>'; }).join('');

  var set=function(id,v){var e=document.getElementById(id); if(e) e.textContent=v;};
  roll('pgSku',live.length,'int');
  var fams={}; live.forEach(function(x){fams[x.p.fam]=1;}); set('pgSkuSub','across '+Object.keys(fams).length+' formulas');
  roll('pgUnits',stats.reduce(function(a,x){return a+x.units;},0),'int'); set('pgUnitsSub',PPLABEL[ppTab]||'');
  roll('pgRev',stats.reduce(function(a,x){return a+x.rev;},0));
  var top=byRev[0]&&byRev[0].rev>0?byRev[0]:null;
  set('pgTop',top?top.p.fam+' '+top.p.pack:'No sales in this period');
  set('pgTopSub',top?tk(top.rev)+' · '+top.units+' units from '+top.buyers.length+' buyers':'');
  var al=live.filter(function(x){return stat(x.p.stock,x.p.reorder)!=='ok';});
  roll('pgAlerts',al.length,'int');
  var crit=al.filter(function(x){return stat(x.p.stock,x.p.reorder)==='critical';}).length;
  set('pgAlertsSub', al.length ? (crit+' critical · '+(al.length-crit)+' low. Filter Below reorder') : 'every pack above its reorder level');
  var aw=document.getElementById('pgAlertWrap'); if(aw) aw.className='kpi'+(al.length?' due':'');
}
/* twelve months of one pack, hand-drawn bars, hover for the numbers */
function renderProdMonths(k){
  var box=document.getElementById('pdMonths'); if(!box) return;
  var MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var months=[]; for(var i=11;i>=0;i--){ var d=new Date(TODAY.getFullYear(), TODAY.getMonth()-i, 1); months.push({y:d.getFullYear(),m:d.getMonth(),u:0,v:0,n:0}); }
  S.cust.forEach(function(c){ c.o.forEach(function(o){ (o.it||[]).forEach(function(it){ if(it.k!==k) return;
    var d=pd(o.d); var mo=months.filter(function(x){return x.y===d.getFullYear()&&x.m===d.getMonth();})[0]; if(mo){ mo.u+=it.q; mo.v+=it.t; mo.n++; } }); }); });
  var max=Math.max.apply(null, months.map(function(x){return x.v;}))||1;
  var best=months.slice().sort(function(a,b){return b.v-a.v;})[0];
  box.innerHTML=months.map(function(x){
    var cur=x.y===TODAY.getFullYear()&&x.m===TODAY.getMonth();
    return '<div class="mb'+(cur?' cur':'')+(x.v===best.v&&x.v>0?' best':'')+'" tabindex="0" aria-label="'+MN[x.m]+' '+x.y+': '+x.u+' units, '+tk(x.v)+'">'+
      '<span class="mtip"><b>'+tk(x.v)+'</b>'+x.u+' units · '+x.n+(x.n===1?' order':' orders')+'</span>'+
      '<i style="height:'+(x.v?Math.max(3,Math.round(x.v/max*100)):0)+'%"></i><b>'+MN[x.m]+'</b></div>'; }).join('');
  var sub=document.getElementById('pdMonSub'); if(sub) sub.textContent = best&&best.v>0 ? 'best month '+MN[best.m]+' '+best.y+' at '+tk(best.v)+' · hover a bar for the numbers' : 'no sales in the last twelve months';
}

var curProd=0;
function openProduct(k){
  curProd=+k; renderProduct(); location.hash='product';
}
function renderProduct(){
  if(curProd!=null && document.getElementById('pdMonths')) renderProdMonths(curProd);
  var p=S.prod[curProd]; if(!p) return;
  var x=prodStats(curProd);
  var stock={q:p.stock,r:p.reorder};
  var set=function(id,v){var e=document.getElementById(id); if(e) e.innerHTML=v;};

  var im=document.getElementById('pdImg'); if(im) im.src=p.img;
  set('pdName',esc(p.fam));
  set('pdMeta',(p.archived?'<span class="pill bad">Archived</span><i></i>':'')+'<span class="mono">'+esc(p.sku||'')+'</span><i></i><span class="pill man">'+esc(p.pack)+'</span><i></i>'+
      '<span>Retail <b>'+tk(p.r)+'</b></span><i></i><span>Wholesale <b>'+tk(p.w)+'</b></span>'+
      '<i></i><span>Margin '+Math.round((p.r-p.w)/p.r*100)+'% off retail</span>');
  roll('pdRev',x.rev); roll('pdUnits',x.units,'int');
  roll('pdOrders',x.orders,'int'); roll('pdBuyers',x.buyers.length,'int');
  set('pdAvg', x.orders?tk(Math.round(x.rev/x.orders)):tk(0));
  roll('pdStock', stock.q, 'stock');
  var sc=document.getElementById('pdStockCard');
  if(sc) sc.className='kpi'+(stat(stock.q,stock.r)!=='ok'?' due':'');
  set('pdStockSub', 'reorder at '+stock.r+' · '+(stat(stock.q,stock.r)==='ok'?'healthy':stat(stock.q,stock.r)));
  var pm=document.getElementById('pdMovBody');
  if(pm){ var mv=S.mov.filter(function(m){return m.k===curProd || m.n===(p.fam+' '+p.pack);});
    pm.innerHTML = mv.length ? mv.slice(0,8).map(function(x){
      return '<tr'+(x.isNew?' class="fresh"':'')+'><td class="mut">'+esc(x.d)+'</td>'+
        '<td><span class="pill '+(x.t==='In'?'web':'man')+'">'+esc(x.t)+'</span></td>'+
        '<td class="r"><b>'+(x.q>0?'+':'')+x.q+'</b></td><td class="mut">'+esc(x.ref)+'</td></tr>'; }).join('')
      : '<tr><td colspan="4"><div class="none"><b>No movements yet.</b>Sales, stock-in and batches land here.</div></td></tr>'; }
  var si=document.getElementById('pdStockIn'); if(si) si.setAttribute('data-stockin', curProd);

  var bb=document.getElementById('pdBuyerBody');
  if(bb) bb.innerHTML = x.buyers.length ? x.buyers.map(function(b,i){
    return '<tr class="crow" data-code="'+b.c.code+'" tabindex="0">'+
      '<td><span class="rank '+(i<3?'t'+(i+1):'')+'">'+(i+1)+'</span>'+
      '<b>'+esc(b.c.name)+'</b><div class="mut">'+esc(b.c.area)+', '+esc(b.c.district)+'</div></td>'+
      '<td><span class="pill man">'+esc(b.c.district)+'</span></td>'+
      '<td class="r mut">'+b.n+'</td><td class="r">'+b.q+'</td>'+
      '<td class="r"><b>'+tk(b.v)+'</b></td><td class="r"><span class="go2">›</span></td></tr>';
  }).join('')
  : '<tr><td colspan="6"><div class="none"><b>Nobody has bought this yet.</b>'+
    'Record a sale with this pack and the buyer appears here.</div></td></tr>';

  var ob=document.getElementById('pdOrderBody');
  if(ob) ob.innerHTML = x.rows.length ? x.rows.map(function(r){
    return '<tr'+(r.o.isNew?' class="fresh"':'')+'><td class="mut">'+esc(r.o.d)+'</td>'+
      '<td><a href="#sale" class="mono" data-inv="'+esc(r.o.inv)+'">'+esc(r.o.inv)+'</a>'+
        (r.o.isNew?' <span class="pill ok">new</span>':'')+'</td>'+
      '<td><a href="#customer-profile" data-open="'+r.c.code+'">'+esc(r.c.name)+'</a></td>'+
      '<td class="r">'+r.it.q+'</td><td class="mut">'+tk(r.it.r)+'</td>'+
      '<td class="r"><b>'+tk(r.it.t)+'</b></td>'+
      '<td class="r"><span class="pill '+(r.o.src==='Web'?'web':'man')+'">'+esc(r.o.src)+'</span></td></tr>';
  }).join('')
  : '<tr><td colspan="7"><div class="none"><b>No sale lines yet.</b>'+
    'This pack has not been sold in the period on file.</div></td></tr>';

  var dl=document.getElementById('pdDistBody');
  var by={};
  x.rows.forEach(function(r){ var b=by[r.c.district]||(by[r.c.district]={q:0,v:0});
    b.q+=r.it.q; b.v+=r.it.t; });
  var keys=Object.keys(by).sort(function(a,b){return by[b].v-by[a].v;});
  if(dl) dl.innerHTML = keys.length ? keys.map(function(k){
    return '<tr><td><b>'+esc(k)+'</b></td><td class="r">'+by[k].q+'</td>'+
      '<td class="r"><b>'+tk(by[k].v)+'</b></td></tr>'; }).join('')
    : '<tr><td colspan="3"><div class="none"><b>No districts yet.</b></div></td></tr>';
}

/* ═══════════════════════════════════════════════════════════════════════
   STOCK IN · PRODUCTION BATCH · NEW PRODUCT
   Three writes, each of which the rest of the app reads. A batch consumes raw
   material on a fixed recipe so the raw table moves too.
   ═══════════════════════════════════════════════════════════════════════ */
function setMethod(inputId, m){
  var wrap=document.getElementById('msel-'+inputId); if(!wrap) return;
  wrap.querySelectorAll('[data-method]').forEach(function(o){ o.setAttribute('aria-selected',String(o.getAttribute('data-method')===m)); });
  var sel=wrap.querySelector('[data-method="'+m+'"]');
  wrap.querySelector('.mlbl').textContent=m;
  wrap.querySelector('.mic').innerHTML=sel?sel.querySelector('svg').outerHTML:'';
  wrap.querySelector('.mic').className='mic '+(sel&&sel.classList.contains('bk')?'bk':sel&&sel.classList.contains('ng')?'ng':'');
  var ic=wrap.querySelector('.mic svg'); if(ic){ ic.classList.add('tick'); }
  wrap.querySelector('.mlist').classList.remove('open'); wrap.querySelector('.mselb').setAttribute('aria-expanded','false');
  document.getElementById(inputId).value=m;
}
/* product picker with photos, used by the Stock in and Production batch sheets. Hidden input keeps the id. */
function ppickFill(id, sel){
  var w=document.querySelector('[data-ppick="'+id+'"]'); if(!w) return; sel=+sel||0;
  w.querySelector('.plist').innerHTML=S.prod.map(function(p,k){ if(p.archived) return ''; var st=stat(p.stock,p.reorder);
    return '<div class="opt" role="option" data-ppk="'+k+'" aria-selected="'+(k===sel)+'"><span class="pimg sm"><img src="'+p.img+'" alt=""></span>'+
      '<span style="min-width:0;flex:1"><span class="nm">'+esc(p.fam+' · '+p.pack)+'</span><span class="mt"><span class="mono">'+esc(p.sku||'')+'</span> · <span class="'+(st==='ok'?'':'bad')+'">'+p.stock+' in stock</span></span></span>'+CHKSVG+'</div>'; }).join('');
  ppickSet(id, sel, true);
}
function ppickSet(id, k, silent){
  var w=document.querySelector('[data-ppick="'+id+'"]'); if(!w) return; var p=S.prod[k]; if(!p) return;
  w.querySelector('.mlbl').textContent=p.fam+' · '+p.pack+' ('+p.stock+' in stock)';
  w.querySelector('.lthumb img').src=p.img;
  w.querySelectorAll('[data-ppk]').forEach(function(o){ o.setAttribute('aria-selected', String(+o.dataset.ppk===k)); });
  w.querySelector('.plist').classList.remove('open'); w.querySelector('.pselb').setAttribute('aria-expanded','false');
  var h=document.getElementById(id); h.value=k;
  if(!silent) h.dispatchEvent(new Event('change',{bubbles:true}));
}
function prodOptions(sel){ return S.prod.map(function(p,k){
  return '<option value="'+k+'"'+(k===sel?' selected':'')+'>'+esc(p.fam+' · '+p.pack)+' ('+p.stock+' in stock)</option>'; }).join(''); }

function stockInOpen(k){
  ppickFill('siProd', k===undefined||k===null?0:+k);
  var q=document.getElementById('siQty'); if(q) q.value='';
  var r=document.getElementById('siRef'); if(r) r.value='';
  var e=document.getElementById('siErr'); if(e){e.hidden=true;e.textContent='';}
  document.getElementById('siModal').classList.add('open');
  setTimeout(function(){ if(q) q.focus(); },60);
}
function stockInSave(){
  var k=+((document.getElementById('siProd')||{}).value||0), q=num(document.getElementById('siQty')||{value:0});
  var ref=(((document.getElementById('siRef')||{}).value)||'').trim()||'Stock in, counter';
  var err=document.getElementById('siErr'); var fail=function(m){ if(err){err.textContent=m;err.hidden=false;} };
  if(q<=0) return fail('Enter how many units came in.');
  if(q>100000) return fail('That is more than the factory makes in a year. Check the number.');
  S.prod.forEach(function(p){p.isNew=false;});
  var before=S.prod[k].stock;
  moveStock(k, q, 'In', ref); S.prod[k].bump=true;
  document.getElementById('siModal').classList.remove('open');
  renderInventory(); renderProducts(); renderProduct(); renderDash(); renderNotifs();
  say('<b>+'+q+' '+esc(S.prod[k].fam+' '+S.prod[k].pack)+'</b> · stock '+before+' → '+S.prod[k].stock+
      ' &nbsp;<a href="#product" data-prod="'+k+'" style="color:#2BD255;font-weight:650">See the product →</a>');
  location.hash='products';
}

/* production: one batch of a pack consumes raw material on a simple recipe */
var RECIPE={ 'Nutricare Hand Feeding':[['Maize flour',0.55],['Soya protein',0.3],['Calcium carbonate',0.05]],
             'Avian Eggfood':[['Maize flour',0.5],['Soya protein',0.35],['Calcium carbonate',0.05]],
             'Avian Spirulina':[['Spirulina powder',1]], 'Avian Herbs':[['Moringa leaf powder',0.5]],
             'Avian Moringa':[['Moringa leaf powder',1]], 'Avian Beetroot':[['Beetroot powder',1]] };
function packKg(p){ var m=/([\d.]+)\s*(kg|g)/i.exec(p.pack||''); if(!m) return 0.2;
  return m[2].toLowerCase()==='kg'?+m[1]:(+m[1])/1000; }
function batchOpen(){
  ppickFill('pbProd', 0);
  var q=document.getElementById('pbQty'); if(q) q.value='';
  var b=document.getElementById('pbCode'); if(b) b.value='B-09'+(13+S.mov.filter(function(m){return /batch/i.test(m.ref);}).length);
  var e=document.getElementById('pbErr'); if(e){e.hidden=true;e.textContent='';}
  batchPreview();
  document.getElementById('pbModal').classList.add('open');
  setTimeout(function(){ if(q) q.focus(); },60);
}
function batchPreview(){
  var k=+((document.getElementById('pbProd')||{}).value||0), q=num(document.getElementById('pbQty')||{value:0});
  var p=S.prod[k]; if(!p) return; var kg=packKg(p)*q; var rec=RECIPE[p.fam]||[];
  var el=document.getElementById('pbPreview'); if(!el) return;
  if(!q){ el.innerHTML='<div class="hint">Enter a quantity to see what the batch consumes.</div>'; return; }
  el.innerHTML='<div class="hint" style="margin-bottom:6px">'+q+' × '+esc(p.pack)+' = <b>'+kg.toFixed(1)+' kg</b> of finished product. Consumes:</div>'+
    '<table style="font-size:12.5px">'+rec.map(function(r){ var need=kg*r[1];
      var raw=S.raw.filter(function(x){return x.n===r[0];})[0]; var ok=raw&&raw.q>=need;
      return '<tr><td style="padding:4px 0;border:0">'+esc(r[0])+'</td><td class="r" style="padding:4px 0;border:0">'+need.toFixed(1)+' kg</td>'+
        '<td class="r" style="padding:4px 0;border:0"><span class="pill '+(ok?'ok':'bad')+'">'+(raw?raw.q+' kg on hand':'not tracked')+'</span></td></tr>'; }).join('')+'</table>';
}
function batchSave(){
  var k=+((document.getElementById('pbProd')||{}).value||0), q=num(document.getElementById('pbQty')||{value:0});
  var code=(((document.getElementById('pbCode')||{}).value)||'').trim()||'B-0900';
  var err=document.getElementById('pbErr'); var fail=function(m){ if(err){err.textContent=m;err.hidden=false;} };
  if(q<=0) return fail('Enter how many units the batch produced.');
  var p=S.prod[k], kg=packKg(p)*q, rec=RECIPE[p.fam]||[];
  for(var i=0;i<rec.length;i++){ var raw=S.raw.filter(function(x){return x.n===rec[i][0];})[0];
    if(raw && raw.q < kg*rec[i][1]) return fail('Not enough '+rec[i][0]+': need '+(kg*rec[i][1]).toFixed(1)+' kg, have '+raw.q+' kg. Buy raw material first.'); }
  S.prod.forEach(function(x){x.isNew=false;});
  rec.forEach(function(r){ var raw=S.raw.filter(function(x){return x.n===r[0];})[0]; if(raw) raw.q=Math.round((raw.q-kg*r[1])*10)/10; });
  var before=p.stock;
  moveStock(k, q, 'In', 'Production batch '+code); p.bump=true;
  S.log.forEach(function(r){r.isNew=false;});
  S.log.unshift({when:'26 Sep '+new Date().toTimeString().slice(0,5), who:'Factory', what:'Production batch '+code+', '+p.fam+' '+p.pack, before:String(before), after:String(p.stock), isNew:true});
  document.getElementById('pbModal').classList.remove('open');
  renderInventory(); renderProducts(); renderProduct(); renderDash(); renderNotifs(); renderSettings();
  say('<b>Batch '+esc(code)+' recorded.</b> +'+q+' '+esc(p.fam+' '+p.pack)+' · stock '+before+' → '+p.stock+
      ' · raw material deducted on the recipe');
  location.hash='products';
}

/* a new pack of an existing formula, or a brand-new formula */
function newProdOpen(){
  var f=document.getElementById('npForm'); if(f) f.reset();
  var sel=document.getElementById('npFam'); var fams=[]; S.prod.forEach(function(p){ if(fams.indexOf(p.fam)<0) fams.push(p.fam); });
  if(sel) sel.innerHTML=fams.map(function(x){return '<option>'+esc(x)+'</option>';}).join('')+'<option value="__new">New formula…</option>';
  var nn=document.getElementById('npNewName'); if(nn) nn.parentElement.hidden=true;
  var e=document.getElementById('npErr'); if(e){e.hidden=true;e.textContent='';}
  document.getElementById('npModal').classList.add('open');
  setTimeout(function(){ var q=document.getElementById('npPack'); if(q) q.focus(); },60);
}
function newProdSave(){
  var v=function(id){ return ((document.getElementById(id)||{}).value||'').trim(); };
  var fam=v('npFam')==='__new'?v('npNewName'):v('npFam');
  var pack=v('npPack'), r=num({value:v('npRetail')}), w=num({value:v('npWhole')}),
      stock=num({value:v('npStock')||'0'}), reorder=num({value:v('npReorder')||'20'});
  var err=document.getElementById('npErr'); var fail=function(m){ if(err){err.textContent=m;err.hidden=false;} };
  if(fam.length<3) return fail('Give the formula a name.');
  if(!/^\d+\s*(g|kg)$/i.test(pack)) return fail('Pack size like 200g or 1kg.');
  if(r<=0) return fail('Enter the retail price.');
  if(w<=0||w>=r) return fail('Wholesale must be below retail ('+tk(r)+').');
  if(S.prod.some(function(p){return p.fam.toLowerCase()===fam.toLowerCase()&&p.pack.toLowerCase()===pack.toLowerCase();}))
    return fail(fam+' '+pack+' already exists. Use Stock in to add units.');
  var like=S.prod.filter(function(p){return p.fam===fam;})[0];
  S.prod.forEach(function(p){p.isNew=false;});
  var g=/kg/i.test(pack)?Math.round(parseFloat(pack)*1000):parseInt(pack,10);
  var code=SKUFAM[fam] || (fam.split(/\s+/).filter(function(w){return w.toLowerCase()!=='avian';}).map(function(w){return w[0];}).join('').slice(0,3).toUpperCase()+'XXX').slice(0,3);
  var sku='SBF-'+code+'-'+(g<100?('00'+g).slice(-3):g);
  S.prod.push({n:fam+' · '+pack, fam:fam, pack:pack, r:r, w:w, img:like?like.img:GENERIC_IMG,
               stock:0, reorder:reorder, isNew:true, sku:sku});
  var k=S.prod.length-1;
  if(stock>0) moveStock(k, stock, 'In', 'Opening stock');
  S.log.forEach(function(x){x.isNew=false;});
  S.log.unshift({when:'26 Sep '+new Date().toTimeString().slice(0,5), who:'Anowar Bhai', what:'Added product '+fam+' '+pack, before:'—', after:tk(r)+' / '+tk(w)+' · '+stock+' units', isNew:true});
  document.getElementById('npModal').classList.remove('open');
  renderProducts(); renderInventory(); renderDash(); renderNotifs(); renderSettings();
  document.querySelectorAll('#lineBody .lp').forEach(function(sel){ var cur=sel.value; sel.innerHTML=S.prod.map(function(p,i){return '<option value="'+i+'">'+esc(p.n)+'</option>';}).join(''); sel.value=cur; });
  say('<b>'+esc(fam+' '+pack)+' added</b> · retail '+tk(r)+' · wholesale '+tk(w)+' · '+stock+' in stock'+
      ' &nbsp;<a href="#sales-entry" style="color:#2BD255;font-weight:650">Already on the sale screen →</a>');
  location.hash='products';
  setTimeout(function(){ var c=document.querySelector('.pcard.fresh'); if(c) c.scrollIntoView({block:'center',behavior:'smooth'}); },250);
}

/* ═══════════════════════════════════════════════════════════════════════
   EDIT A PRODUCT'S PRICES
   The product record is the one place a price lives. The sale screen, the
   product cards and the reports read it; nothing else stores it.
   ═══════════════════════════════════════════════════════════════════════ */
var epImg=null;
function prodEditOpen(){
  var p=S.prod[curProd]; if(!p) return;
  var set=function(id,v){ var e=document.getElementById(id); if(e) e.value=v; };
  set('epFam',p.fam); set('epPack',p.pack); set('epSku',p.sku||''); set('epRetail',p.r); set('epWhole',p.w); set('epReorder',p.reorder);
  epImg=null; var pic=document.querySelector('#epPic img'); if(pic) pic.src=p.img;
  var t=document.getElementById('epTitle'); if(t) t.textContent='Edit '+p.fam+' '+p.pack;
  var ab=document.getElementById('epArchive'); if(ab){ var sv=ab.querySelector('svg'); ab.innerHTML=(sv?sv.outerHTML:'')+(p.archived?'Restore':'Archive'); }
  var e=document.getElementById('epErr'); if(e){e.hidden=true;e.textContent='';}
  document.getElementById('epModal').classList.add('open');
  setTimeout(function(){ var r=document.getElementById('epFam'); if(r){r.focus();r.select();} },60);
}
function prodEditSave(){
  var p=S.prod[curProd]; if(!p) return;
  var v=function(id){ return ((document.getElementById(id)||{}).value||'').trim(); };
  var fam=v('epFam'), pack=v('epPack'), sku=v('epSku').toUpperCase();
  var r=num({value:v('epRetail')}), w=num({value:v('epWhole')}), ro=num({value:v('epReorder')});
  var err=document.getElementById('epErr'); var fail=function(m,id){ if(err){err.textContent=m;err.hidden=false;} var f=id&&document.getElementById(id); if(f){f.focus();} };
  if(fam.length<3) return fail('Give the product a name.','epFam');
  if(!/^\d+\s*(g|kg)$/i.test(pack)) return fail('Pack size like 200g or 1kg.','epPack');
  if(!/^SBF-[A-Z]{3}-\d{3,4}$/.test(sku)) return fail('SKU like SBF-NHF-1000 or SBF-AHB-050: SBF, the product code, the grams.','epSku');
  if(S.prod.some(function(q,i){ return i!==curProd && (q.sku||'').toUpperCase()===sku; })) return fail('SKU '+sku+' is already used by another pack.','epSku');
  if(S.prod.some(function(q,i){ return i!==curProd && q.fam.toLowerCase()===fam.toLowerCase() && q.pack.toLowerCase()===pack.toLowerCase(); })) return fail(fam+' '+pack+' already exists.','epPack');
  if(r<=0) return fail('Enter the retail price.','epRetail');
  if(w<=0||w>=r) return fail('Wholesale must be below retail ('+tk(r)+').','epWhole');
  if(ro<0) return fail('Reorder level cannot be negative.','epReorder');
  var label=p.fam+' '+p.pack, ch=[];
  if(fam!==p.fam) ch.push(['Product name',p.fam,fam]);
  if(pack!==p.pack) ch.push(['Pack size '+p.fam,p.pack,pack]);
  if(sku!==(p.sku||'')) ch.push(['SKU '+label,p.sku||'none',sku]);
  if(r!==p.r) ch.push(['Retail price '+label,tk(p.r),tk(r)]);
  if(w!==p.w) ch.push(['Wholesale price '+label,tk(p.w),tk(w)]);
  if(ro!==p.reorder) ch.push(['Reorder level '+label,String(p.reorder),String(ro)]);
  if(epImg) ch.push(['Photo '+label,'previous photo','new photo']);
  if(!ch.length){ document.getElementById('epModal').classList.remove('open'); say('Nothing changed.'); return; }
  p.fam=fam; p.pack=pack; p.sku=sku; p.r=r; p.w=w; p.reorder=ro; p.n=fam+' · '+pack; if(epImg) p.img=epImg;
  S.log.forEach(function(x){x.isNew=false;});
  ch.forEach(function(c){ S.log.unshift({when:'26 Sep '+new Date().toTimeString().slice(0,5), who:'Anowar Bhai', what:'Changed '+c[0], before:c[1], after:c[2], isNew:true}); });
  document.getElementById('epModal').classList.remove('open');
  renderProduct(); renderProducts(); renderInventory(); renderDash(); renderNotifs(); renderSettings(); renderSales(); renderSale();
  document.querySelectorAll('#lineBody .line').forEach(function(tr){ if(+tr.querySelector('.lp').value===curProd){ var rr=tr.querySelector('.lr'); if(rr.dataset.touched!=='1') rr.value=''; linePick(tr,curProd); } });
  recalc();
  say('<b>'+esc(fam+' '+pack)+' updated.</b> '+ch.length+(ch.length===1?' change':' changes')+' logged with before and after. Sale screen, lists and invoices read the new record.');
}
function prodArchiveToggle(){
  var p=S.prod[curProd]; if(!p) return; p.archived=!p.archived;
  S.log.forEach(function(x){x.isNew=false;});
  S.log.unshift({when:'26 Sep '+new Date().toTimeString().slice(0,5), who:'Anowar Bhai', what:(p.archived?'Archived ':'Restored ')+p.fam+' '+p.pack, before:p.archived?'Active':'Archived', after:p.archived?'Archived':'Active', isNew:true});
  document.getElementById('epModal').classList.remove('open');
  renderProduct(); renderProducts(); renderInventory(); renderDash(); renderNotifs(); renderSettings();
  say('<b>'+esc(p.fam+' '+p.pack)+'</b> '+(p.archived?'archived. Hidden from new sales and lists; its history stays. Filter Archived to bring it back.':'restored and back on sale.'));
}
function epFilePick(f){
  if(!f || !/^image\//.test(f.type)) return;
  var rd=new FileReader(); rd.onload=function(){ epImg=rd.result; var pic=document.querySelector('#epPic img'); if(pic) pic.src=epImg; }; rd.readAsDataURL(f);
}

/* ═══════════════════════════════════════════════════════════════════════
   SALES LIST — every invoice, from the same rows the dashboard reads
   ═══════════════════════════════════════════════════════════════════════ */
var slFilter='all';
function allSales(){
  var out=[]; S.cust.forEach(function(c){ c.o.forEach(function(o){ out.push({c:c,o:o}); }); });
  out.sort(function(a,b){ return (b.o.isNew?1:0)-(a.o.isNew?1:0) || pd(b.o.d)-pd(a.o.d) || (b.o.inv>a.o.inv?1:-1); });
  return out;
}
function methodOf(c,o){ var p=c.p.filter(function(x){return x.inv===o.inv;})[0]; return p?p.m:(o.p>0?'Cash':'—'); }
function renderSales(){
  var tb=document.getElementById('slBody'); if(!tb) return;
  var q=((document.getElementById('slSearch')||{}).value||'').trim();
  document.querySelectorAll('[data-sf]').forEach(function(b){ b.setAttribute('aria-pressed',String(b.dataset.sf===slFilter)); });
  var all=allSales(), rows=all.filter(function(x){
    var o=x.o, due_=o.t-o.p;
    if(slFilter==='pending'&&!o.pending) return false;
    if(slFilter==='due'&&due_<=0) return false;
    if(slFilter==='paid'&&due_>0) return false;
    if(slFilter==='web'&&o.src!=='Web') return false;
    return !q || words(o.inv+' '+x.c.name+' '+x.c.phone+' '+x.c.code+' '+x.c.district, q);
  });
  tb.innerHTML=rows.map(function(x){ var o=x.o,c=x.c,d=o.t-o.p;
    return '<tr class="crow'+(o.isNew?' fresh':'')+'" data-inv="'+esc(o.inv)+'" tabindex="0">'+
      '<td class="mut">'+esc(o.d)+'</td>'+
      '<td><span class="mono">'+esc(o.inv)+'</span>'+(o.isNew?' <span class="pill ok">new</span>':'')+'</td>'+
      '<td><b>'+esc(c.name)+'</b><div class="mut">'+esc(c.district)+'</div></td>'+
      '<td class="r mut">'+o.n+'</td><td class="r"><b>'+tk(o.t)+'</b></td><td class="r">'+tk(o.p)+'</td>'+
      '<td class="r">'+(d>0?'<span class="pill due">'+tk(d)+'</span>':'<span class="pill paid">paid</span>')+'</td>'+
      '<td class="mut">'+esc(methodOf(c,o))+'</td>'+
      '<td><span class="pill '+(o.src==='Web'?'web':'man')+'">'+esc(o.src||'Manual')+'</span></td>'+
      '<td><span class="pill '+(o.pending?'due':'ok')+'">'+(o.pending?'Pending':'Delivered')+'</span></td>'+
      '<td class="r"><button class="ibtn" data-edit="'+esc(o.inv)+'" aria-label="Edit '+esc(o.inv)+'" title="Edit order">'+PENCIL+'</button></td></tr>'; }).join('');
  var none=document.getElementById('slNone'); if(none) none.hidden=rows.length>0;
  var m=all.filter(function(x){return inRange(x.o.d,'month');}), mt=m.reduce(function(a,x){return a+x.o.t;},0);
  var unpaid=all.filter(function(x){return x.o.t-x.o.p>0;});
  roll('slMonth',mt); roll('slCount',all.length,'int'); roll('slAvg', all.length?all.reduce(function(a,x){return a+x.o.t;},0)/all.length:0);
  roll('slUnpaid',unpaid.length,'int');
  var set=function(id,v){var e=document.getElementById(id); if(e) e.textContent=v;};
  set('slMonthSub', m.length+(m.length===1?' order':' orders')+' in September');
  set('slUnpaidSub', tk(unpaid.reduce(function(a,x){return a+(x.o.t-x.o.p);},0))+' outstanding');
  set('slScope', rows.length===all.length?(all.length+' orders'):(rows.length+' of '+all.length));
  var nb=document.querySelector('.nav a[href="#sales"] .nbadge'); if(nb){ nb.textContent=all.filter(function(x){return x.o.pending;}).length; nb.hidden=false; }
}

/* ═══════════════════════════════════════════════════════════════════════
   ONE INVOICE
   Read from the same order row the list, the dashboard and the profile use.
   Its actions write back to that row, so every other screen moves with it.
   ═══════════════════════════════════════════════════════════════════════ */
var curInv=null;
function findSale(inv){ for(var i=0;i<S.cust.length;i++){ var c=S.cust[i]; for(var j=0;j<c.o.length;j++) if(c.o[j].inv===inv) return {c:c,o:c.o[j]}; } return null; }
function openSale(inv){ curInv=inv; renderSale(); location.hash='sale'; }
function renderSale(){
  var x=findSale(curInv) || (allSales()[0]||null); if(!x) return; curInv=x.o.inv;
  var c=x.c, o=x.o, d=o.t-o.p, set=function(id,v){var e=document.getElementById(id); if(e) e.innerHTML=v;};
  set('sdInv',esc(o.inv));
  set('sdStatus','<span class="pill '+(o.pending?'due':'ok')+'">'+(o.pending?'Pending delivery':'Delivered')+'</span>');
  set('sdSrc',(o.edited?'<span class="pill man" title="Lines were corrected after saving. Payments untouched.">edited</span><i></i>':'')+'<span class="pill '+(o.src==='Web'?'web':'man')+'">'+(o.src==='Web'?'Website order':'Entered at counter')+'</span>'+
    (o.src==='Web'?'<i></i><span class="mono mut" title="WooCommerce order number. The same order, one record.">WC #'+(1000+(+o.inv.slice(-4)))+'</span>':''));
  set('sdMeta','<span>'+esc(o.d)+'</span><i></i><span>'+o.n+(o.n===1?' unit':' units')+'</span><i></i><span>'+
      (d>0?'<b style="color:var(--warn)">'+tk(d)+' due</b>':'<span style="color:var(--ok)">paid in full</span>')+'</span>');
  set('sdCust','<div class="opt" style="cursor:default;padding:0"><div class="av" style="background:var(--brand);color:#fff">'+esc(c.name[0])+'</div>'+
      '<div style="min-width:0"><div class="nm">'+esc(c.name)+' <span class="pill '+(c.tier==='Wholesale'?'ok':c.tier==='Re-wholesale'?'web':'man')+'">'+esc(c.tier)+'</span></div>'+
      '<div class="mt">'+esc(c.code)+' · '+esc(c.phone)+' · '+esc(c.area)+', '+esc(c.district)+'</div></div>'+
      '<div class="rt">'+c.o.length+' orders<br>'+(due(c)>0?'<b style="color:var(--warn)">'+tk(due(c))+' total due</b>':'<span style="color:var(--ok)">no dues</span>')+'</div></div>');
  var pr=document.getElementById('sdProfile'); if(pr) pr.setAttribute('data-open',c.code);
  var lines=o.it||[], sub=lines.reduce(function(a,l){return a+l.t;},0);
  var lb=document.getElementById('sdLines');
  if(lb) lb.innerHTML = lines.length ? lines.map(function(l){ var p=S.prod[l.k]||{fam:'Product',pack:'',img:GENERIC_IMG,sku:''};
    return '<tr class="crow" data-prod="'+l.k+'" tabindex="0"><td><div class="lpw"><span class="lthumb"><img src="'+p.img+'" alt=""></span>'+
      '<div><b>'+esc(p.fam)+'</b> <span class="mut">'+esc(p.pack)+'</span><div class="mut mono">'+esc(p.sku||'')+'</div></div></div></td>'+
      '<td class="r">'+l.q+'</td><td class="mut">'+tk(l.r)+'</td><td class="r"><b>'+tk(l.t)+'</b></td></tr>'; }).join('')
    : '<tr><td colspan="4"><div class="none"><b>No line detail on this invoice.</b>Imported from the old sheet, total only.</div></td></tr>';
  set('sdQty', lines.length ? (o.n+' units across '+lines.length+(lines.length===1?' item':' items')) : (o.n+' units'));
  var disc=o.disc||0, del=o.del||0;
  set('sdSub',tk(lines.length?sub:o.t)); set('sdDisc','-'+tk(disc)); set('sdDel',tk(del)); set('sdTotal',tk(o.t)); set('sdPaid',tk(o.p));
  var rd=document.getElementById('sdRowDisc'); if(rd) rd.hidden=!disc; var rl=document.getElementById('sdRowDel'); if(rl) rl.hidden=!del;
  var sdl=document.getElementById('sdDiscLbl'); if(sdl) sdl.textContent='Discount'+(o.coupon?' · '+o.coupon:'');
  roll('sdDue', d>0?d:0);
  var dw=document.getElementById('sdDueWrap'); if(dw) dw.className='kpi'+(d>0?' due':'');
  set('sdDueSub', d>0?'record a payment to clear it':'nothing owing on this invoice');
  var nw=document.getElementById('sdNoteWrap'); if(nw){ nw.hidden=!o.note; set('sdNote',esc(o.note||'')); }
  var pays=c.p.filter(function(p){return p.inv===o.inv;});
  var pb=document.getElementById('sdPayBody');
  if(pb) pb.innerHTML = pays.length ? pays.map(function(p){ return '<tr'+(p.isNew?' class="fresh"':'')+'><td class="mut">'+esc(p.d)+'</td><td>'+esc(p.m)+'</td><td class="r"><b>'+tk(p.a)+'</b></td></tr>'; }).join('')
    : '<tr><td colspan="3"><div class="none"><b>No payment yet.</b>The full amount is outstanding.</div></td></tr>';
  set('sdPayCount', pays.length+(pays.length===1?' payment':' payments'));
  var db=document.getElementById('sdDeliver'); if(db){ db.innerHTML=(o.pending?TRUCK+'Mark delivered':TRUCK+'Mark pending'); }
  var cb=document.getElementById('sdCollect'); if(cb) cb.disabled=!(d>0);
}
function deliverToggle(){
  var x=findSale(curInv); if(!x) return; x.o.pending=!x.o.pending;
  S.log.forEach(function(r){r.isNew=false;});
  S.log.unshift({when:'26 Sep '+new Date().toTimeString().slice(0,5), who:'Sales staff', what:(x.o.pending?'Reopened ':'Delivered ')+x.o.inv+', '+x.c.name, before:x.o.pending?'Delivered':'Pending', after:x.o.pending?'Pending':'Delivered', isNew:true});
  renderSale(); renderSales(); renderDash(); renderNotifs(); renderSettings();
  say('<b>'+esc(x.o.inv)+'</b> marked '+(x.o.pending?'pending again':'delivered')+'. Pending orders on the dashboard moved with it.');
}
function saveEdit(t, btn){
  var inv=editingInv, x=findSale(inv); if(!x){ resetSale(); btn.disabled=false; return; }
  var o=x.o, method=(document.getElementById('salePayMethod')||{}).value||'Cash';
  var lines=[]; t.rows.forEach(function(tr){ var k=+tr.querySelector('.lp').value, q=num(tr.querySelector('.lq')), r=num(tr.querySelector('.lr')); if(q>0) lines.push({k:k,q:q,r:r,t:q*r}); });
  var disc0=num(document.getElementById('saleDisc')||{value:0}), del0=num(document.getElementById('saleDeliv')||{value:0});
  var note0=(((document.getElementById('saleNote')||{}).value)||'').trim();
  var before={n:o.n,t:o.t,it:(o.it||[]).slice(),disc:o.disc||0,del:o.del||0,method:o.method,note:o.note||''};
  /* stock moves by the difference, one movement per product that changed */
  var delta={}; before.it.forEach(function(l){ delta[l.k]=(delta[l.k]||0)+l.q; }); lines.forEach(function(l){ delta[l.k]=(delta[l.k]||0)-l.q; });
  Object.keys(delta).forEach(function(k){ var d=delta[k]; if(d) moveStock(+k, d, d>0?'In':'Out', inv+' edited'); });
  o.it=lines; o.n=t.qty; o.t=t.total; o.disc=disc0; o.del=del0; o.note=note0; o.method=method; o.coupon=(couponOn&&couponOk?couponOn.code:''); o.edited=true;
  S.cust.forEach(function(c){ c.o.forEach(function(q){q.isNew=false;}); }); o.isNew=true;
  S.log.forEach(function(l){l.isNew=false;});
  S.log.unshift({when:'26 Sep '+new Date().toTimeString().slice(0,5), who:'Anowar Bhai', what:'Edited '+inv+' ('+x.c.name+')',
    before:before.n+' units · '+tk(before.t)+(before.disc?' · disc '+tk(before.disc):'')+' · '+before.method, after:o.n+' units · '+tk(o.t)+(o.disc?' · disc '+tk(o.disc):'')+' · '+o.method, isNew:true});
  renderDash(); renderCustomers(); renderAccounts(); renderSales(); renderDues(); renderProducts(); renderProduct(); renderInventory(); renderNotifs(); renderSettings();
  current=x.c.code; renderProfile(); renderTimeline();
  btn.innerHTML='<span class="okdraw">'+CHK+'</span>Saved';
  setTimeout(function(){ btn.disabled=false; btn.innerHTML=CHK+'Save sale'; },900);
  resetSale();
  say('<b>'+esc(inv)+' updated.</b> '+tk(before.t)+' → '+tk(o.t)+' · payments untouched ('+tk(o.p)+' paid, '+tk(Math.max(o.t-o.p,0))+' due). Logged with before and after.');
  openSale(inv);
}
/* EDIT ORDER — correct lines, discount, delivery, note, method. Payments are never edited here;
   they are their own rows (Record payment), so a 50K order paid 30K + 20K keeps both receipts. */
var editingInv=null;
function editOrder(inv){
  var x=findSale(inv); if(!x) return;
  location.hash='sales-entry';
  setTimeout(function(){
    resetSale(); editingInv=inv; cbxPick(x.c.code);
    var o=x.o, lb=document.getElementById('lineBody'); lb.innerHTML='';
    (o.it||[]).forEach(function(l,i){ lb.insertAdjacentHTML('beforeend', lineHTML(i)); var tr=lb.lastElementChild; linePick(tr,l.k);
      tr.querySelector('.lq').value=l.q; var r=tr.querySelector('.lr'); r.value=l.r; r.dataset.touched='1'; });
    if(!(o.it||[]).length) lb.innerHTML=lineHTML(0);
    var v=function(id,val){ var e=document.getElementById(id); if(e) e.value=val; };
    var show=function(wrap,link){ var w=document.getElementById(wrap), l=document.getElementById(link); if(w) w.hidden=false; if(l) l.hidden=true; };
    if(o.disc){ v('saleDisc',o.disc); show('discWrap','showDisc'); }
    if(o.del){ v('saleDeliv',o.del); show('delWrap','showDel'); }
    if(o.coupon){ var c=COUPONS.filter(function(q){return q.code===o.coupon;})[0]; if(c){ couponOn=c; v('saleCoupon',o.coupon); show('couponWrap','showCoupon'); } }
    v('saleNote',o.note||''); v('salePaid',0);
    setMethod('salePayMethod', o.method||'Cash');
    var pw=document.getElementById('paidWrap'); if(pw) pw.hidden=true;
    var pays=x.c.p.filter(function(p){return p.inv===inv;});
    var b=document.getElementById('editBanner'); if(b){ b.hidden=false;
      b.innerHTML='<b>Editing '+esc(inv)+'</b> for '+esc(x.c.name)+'. Change items, rates, discount, delivery, note or method. '+
        'Payments are not edited here: '+(pays.length?pays.length+(pays.length===1?' payment':' payments')+' totalling '+tk(o.p)+' stay as recorded':'nothing paid yet')+
        '; record any new payment from the order page. Stock is corrected by the difference. Every change is logged with before and after.'; }
    var h=document.querySelector('#v-sales-entry .ph h1'); if(h) h.textContent='Edit order';
    var sb=document.getElementById('saveBtn'); if(sb) sb.innerHTML=CHK+'Save changes';
    var rb=document.getElementById('resetBtn'); if(rb) rb.innerHTML=XI+'Cancel, back to the order';
    var inv0=document.getElementById('saleInv'); if(inv0) inv0.textContent=inv;
    recalc();
    var inv1=document.getElementById('saleInv'); if(inv1) inv1.textContent=inv;
    window.scrollTo({top:0,behavior:'smooth'});
  },120);
}
function repeatOrder(){
  var x=findSale(curInv); if(!x) return;
  location.hash='sales-entry';
  setTimeout(function(){
    resetSale(); cbxPick(x.c.code);
    var lb=document.getElementById('lineBody'); lb.innerHTML='';
    (x.o.it||[]).forEach(function(l,i){ lb.insertAdjacentHTML('beforeend', lineHTML(i)); var tr=lb.lastElementChild; linePick(tr,l.k); tr.querySelector('.lq').value=l.q; });
    if(!(x.o.it||[]).length) lb.innerHTML=lineHTML(0);
    recalc();
    say('<b>Repeat of '+esc(x.o.inv)+'</b> for '+esc(x.c.name)+'. Same items at today’s prices. Adjust and save.');
  },120);
}

/* ═══════════════════════════════════════════════════════════════════════
   NOTIFICATIONS — derived from the ledger, never a hard-coded list
   ═══════════════════════════════════════════════════════════════════════ */
function renderNotifs(){
  var out=[];
  var lastOrder=function(c){ return c.o.slice().sort(function(a,b){return pd(b.d)-pd(a.d);})[0]; };
  S.cust.slice().sort(function(a,b){return due(b)-due(a);}).slice(0,3).forEach(function(c){
    if(due(c)>0){ var ou=oldestUnpaid(c); var age=ou?Math.round((TODAY-pd(ou.d))/86400000):0;
      out.push({k:'due',t:esc(c.name)+' owes '+tk(due(c)),
      s:(ou?esc(ou.inv)+' unpaid '+age+(age===1?' day':' days'):'')+' · '+esc(c.district), w:ou?'Since '+esc(ou.d):'', code:c.code}); } });
  lapsed(90).slice(0,2).forEach(function(c){ var lo=lastOrder(c);
    out.push({k:'bad',t:esc(c.name)+' has not ordered in '+daysSince(c)+' days',
      s:'Lifetime '+tk(sold(c))+' · worth a call', w:lo?'Last order '+esc(lo.d):'', code:c.code}); });
  S.prod.forEach(function(p,k){ if(p.archived) return; var st=stat(p.stock,p.reorder); if(st==='ok') return;
    var mv=S.mov.filter(function(m){return m.k===k;})[0];
    out.push({k:st==='critical'?'bad':'warn', t:esc(p.fam)+' '+esc(p.pack)+' is at '+p.stock,
      s:'Reorder level is '+p.reorder+' · '+st, w:mv?'Last movement '+esc(mv.d)+' 2026':'No movement yet', prod:k}); });

  var el=document.getElementById('notifList');
  if(el) el.innerHTML=out.map(function(n){
    return '<div class="opt'+((n.code||n.prod!==undefined)?'':' nolink')+'"'+(n.code?' data-open="'+n.code+'"':'')+
      (n.prod!==undefined?' data-prod="'+n.prod+'"':'')+'>'+
      '<span class="ndot '+n.k+'"></span><div style="min-width:0;flex:1">'+
      '<div class="nm">'+n.t+'</div><div class="mt">'+n.s+'</div></div>'+
      '<span class="nw">'+(n.w||'')+'</span></div>'; }).join('');
  var c=document.getElementById('notifCount'); if(c) c.textContent=out.length;
}

/* ═══════════════════════════════════════════════════════════════════════
   RENDER · PROFILE + TIMELINE
   ═══════════════════════════════════════════════════════════════════════ */
var current='SBF-001';
function openCustomer(code,view){
  current=code||current;
  renderProfile(); renderTimeline();
  location.hash = view || 'customer-profile';
}

function renderProfile(){
  var c=byCode(current); if(!c) return;
  var s=sold(c),p=paid(c),d=s-p;
  var rank=S.cust.slice().sort(function(a,b){return sold(b)-sold(a);})
           .findIndex(function(x){return x.code===c.code;})+1;
  var set=function(id,v){var e=document.getElementById(id); if(e) e.innerHTML=v;};
  set('pAv',esc(c.name[0]));
  set('pName',esc(c.name));
  set('pMeta',(c.shop?'<span><b>'+esc(c.shop)+'</b></span><i></i>':'')+'<span class="mono">'+esc(c.code)+'</span><i></i><span class="mono">'+esc(c.phone)+
      '</span><i></i><span>'+esc(c.area)+', '+esc(c.district)+'</span><i></i><span>Customer since '+esc(c.since)+'</span>');
  var bn=document.getElementById('pBanner'); if(bn){ if(c.banner){ bn.querySelector('img').src=c.banner; bn.hidden=false; } else { bn.hidden=true; } }
  set('pTags','<span class="tag">'+esc(c.tier)+'</span>'+(rank<=3?'<span class="tag vip">Top '+rank+' customer</span>':'')+
      '<span class="tag">'+esc(c.district)+'</span>');
  roll('pLtv',s); roll('pPaid',p);
  roll('pDue',d>0?d:0); roll('pOrders',c.o.length,'int');
  set('pRank','#'+rank);
  set('pPaidPct',(s?Math.round(p/s*100):100)+'% collected');
  set('pAvg','avg '+tk(c.o.length?s/c.o.length:0));
  set('pRankSub','of '+S.cust.length+' customers');
  set('pDueSub', d ? ('oldest '+daysSince(c)+' days') : (c.o.length?'nothing owing':'no orders yet'));
  var de=document.getElementById('pDueCard');
  if(de) de.className='kpi'+(d?' due':'');
  set('pLast', esc(c.last||'no orders yet'));

  var ob=document.getElementById('pOrderBody');
  if(ob) ob.innerHTML = !c.o.length
    ? '<tr><td colspan="6"><div class="none"><b>No orders yet.</b>'+
      'Record the first sale from the New sale screen and it appears here straight away.</div></td></tr>'
    : c.o.slice().sort(function(a,b){return (b.isNew?1:0)-(a.isNew?1:0)||pd(b.d)-pd(a.d);}).map(function(o){
    var u=o.t-o.p;
    return '<tr'+(o.isNew?' class="fresh"':'')+'><td class="mut">'+esc(o.d)+'</td>'+
      '<td><a href="#sale" class="mono" data-inv="'+esc(o.inv)+'">'+esc(o.inv)+'</a>'+(o.isNew?' <span class="pill ok">new</span>':'')+'</td>'+
      '<td class="r mut">'+o.n+'</td><td class="r">'+tk(o.t)+'</td><td class="r">'+tk(o.p)+'</td>'+
      '<td class="r">'+(u>0?'<span class="pill due">'+tk(u)+'</span>':'<span class="pill paid">clear</span>')+'</td></tr>';
  }).join('');

  var ps=document.getElementById('pPaySub'); if(ps) ps.textContent=c.p.length?(c.p.length+(c.p.length===1?' receipt':' receipts')+' · '+tk(p)+' in total · newest first'):'nothing received yet';
  var pb=document.getElementById('pPayBody');
  if(pb) pb.innerHTML=c.p.length?c.p.slice().sort(function(a,b){return (b.isNew?1:0)-(a.isNew?1:0) || pd(b.d)-pd(a.d);}).map(function(x){
    return '<tr'+(x.isNew?' class="fresh"':'')+'><td class="mut">'+esc(x.d)+'</td><td>'+esc(x.m)+'</td>'+
      '<td class="mono mut">'+esc(x.inv)+'</td><td class="r"><b>'+tk(x.a)+'</b></td></tr>'; }).join('')
    : '<tr><td colspan="4"><div class="none"><b>No payment yet.</b>The full amount is outstanding.</div></td></tr>';

  roll('dSold',s,'tk',400); roll('dPaid',p,'tk',400); roll('dDue',d>0?d:0,'tk',400);
}

function renderTimeline(){
  var c=byCode(current); if(!c) return;
  var ev=[];
  c.o.forEach(function(o){
    ev.push({k:'sale',d:o.d,t:'New order · '+o.inv,x:o.n+' items',a:o.t,isNew:o.isNew});
    if(o.t-o.p>0) ev.push({k:'dueev',d:o.d,t:'Due created',x:o.inv+' partially paid on the day',a:o.t-o.p});
  });
  c.p.forEach(function(p){
    ev.push({k:'pay',d:p.d,t:'Payment received · '+p.m,x:'Against '+p.inv,a:p.a,isNew:p.isNew}); });
  var first=c.o.slice().sort(function(a,b){return pd(a.d)-pd(b.d);})[0];
  if(first) ev.push({k:'sale',d:c.since,t:'First order',x:'Customer since this date',a:first.t});
  ev.sort(function(a,b){ return (b.isNew?1:0)-(a.isNew?1:0) || pd(b.d)-pd(a.d); });
  var el=document.getElementById('tlBody');
  if(el && !ev.length){ el.innerHTML='<div class="none"><b>Nothing on file yet.</b>'+
    'Every order, due and payment will appear here the moment it is recorded.</div>'; }
  else if(el) el.innerHTML=ev.map(function(e){
    return '<div class="tlx '+e.k+(e.isNew?' fresh':'')+'"><div class="dt">'+esc(e.d)+
      (e.isNew?' <span class="pill ok">just now</span>':'')+'</div>'+
      '<div class="ti">'+esc(e.t)+'</div><div class="tx">'+esc(e.x)+' · <span class="amt">'+tk(e.a)+'</span></div></div>'; }).join('');
  var h=document.getElementById('tlHead');
  if(h) h.innerHTML=esc(c.name)+' · '+esc(c.area)+', '+esc(c.district);
  var m=document.getElementById('tlMeta');
  if(m) m.textContent=c.o.length+' orders · '+tk(sold(c))+' lifetime · '+tk(due(c))+' due';
  var n=document.getElementById('tlName'); if(n) n.textContent=c.name;
}
'''

ENGINE2 = r'''
/* ═══════════════════════════════════════════════════════════════════════
   SALES ENTRY
   The customer picker searches code, name and phone at once, because the
   client said his staff remember different things about different people.
   ═══════════════════════════════════════════════════════════════════════ */
var picked=null;

function cbxRender(q){
  var box=document.getElementById('cbxList'); if(!box) return;
  q=(q||'').trim().toLowerCase();
  var hits=S.cust.filter(function(c){
    if(!q) return true;
    return words(c.code+' '+c.name+' '+c.phone+' '+c.phone.replace(/\s/g,'')+' '+c.district+' '+c.area, q) ||
           c.phone.replace(/\s/g,'').indexOf(q.replace(/\s/g,''))>-1;
  }).slice(0,8);
  function hl(s){ if(!q) return esc(s);
    var i=s.toLowerCase().indexOf(q); if(i<0) return esc(s);
    return esc(s.slice(0,i))+'<mark>'+esc(s.slice(i,i+q.length))+'</mark>'+esc(s.slice(i+q.length)); }
  box.innerHTML = hits.length ? hits.map(function(c,i){
    var d=due(c);
    return '<div class="opt'+(i===0?' on':'')+'" data-pick="'+c.code+'" role="option" tabindex="-1">'+
      '<div class="av">'+esc(c.name[0])+'</div>'+
      '<div style="min-width:0"><div class="nm">'+hl(c.name)+'</div>'+
      '<div class="mt">'+hl(c.code)+' · '+hl(c.phone)+'</div></div>'+
      '<div class="rt">'+esc(c.tier)+'<br>'+(d?'<span style="color:#B45309">'+tk(d)+' due</span>':'clear')+'</div></div>';
  }).join('')
  : '<div class="opt" data-new="1"><div class="av">+</div><div><div class="nm">Add “'+esc(q)+'” as a new customer</div>'+
    '<div class="mt">No match on name, code or phone</div></div></div>';
  box.classList.add('open');
}

function cbxPick(code){
  var c=byCode(code); if(!c) return;
  picked=c;
  var i=document.getElementById('cbxInput'); if(i) i.value=c.name+' · '+c.code;
  document.getElementById('cbxList').classList.remove('open');
  var set=function(id,v){var e=document.getElementById(id); if(e) e.innerHTML=v;};
  var d=due(c);
  set('cbxCard','<div class="opt" style="cursor:default;background:var(--brand-tint)">'+
    '<div class="av" style="background:var(--brand);color:#fff">'+esc(c.name[0])+'</div>'+
    '<div style="min-width:0"><div class="nm">'+esc(c.name)+' <span class="pill '+
      (c.tier==='Wholesale'?'ok':c.tier==='Re-wholesale'?'web':'man')+'">'+esc(c.tier)+'</span></div>'+
    '<div class="mt">'+esc(c.code)+' · '+esc(c.phone)+' · '+esc(c.area)+', '+esc(c.district)+'</div></div>'+
    '<div class="rt">'+c.o.length+' past orders<br>'+
      (d?'<b style="color:#B45309">'+tk(d)+' already due</b>':'<span style="color:#089830">no dues</span>')+'</div></div>');
  setTier(c.tier);
  var f=document.querySelector('#lineBody .line .lps'); if(f && !document.querySelector('#lineBody .lp').value) f.focus();
}

/* line items */
function lineHTML(i){
  return '<tr class="line" data-i="'+i+'">'+
    '<td class="lpc cbx"><input type="hidden" class="lp" value="">'+
      '<div class="lpw"><span class="lthumb" hidden><img alt=""></span>'+
      '<input class="inp lps" autocomplete="off" placeholder="Search by name or SKU" aria-label="Product"></div>'+
      '<div class="cbxlist lpl" role="listbox"></div><div class="lpm mut"></div></td>'+
    '<td><div class="qtyc"><button type="button" class="qb qm" aria-label="Less">−</button>'+
      '<input class="inp lq num" type="number" min="1" value="1" inputmode="numeric" aria-label="Quantity">'+
      '<button type="button" class="qb qp" aria-label="More">+</button></div></td>'+
    '<td><div class="money"><span class="cur">৳</span><input class="inp lr num" value="" placeholder="0" inputmode="numeric" aria-label="Rate"></div></td>'+
    '<td class="r lt num">৳0</td>'+
    '<td class="r"><button class="ibtn ldel" type="button" aria-label="Remove line">'+XI+'</button></td></tr>';
}
/* the product search on a line: name, pack, SKU, stock, and the price for the picked tier */
function words(hay,q){ hay=hay.toLowerCase(); var ts=(q||'').toLowerCase().split(/[\s·,-]+/).filter(Boolean);
  return ts.every(function(t){ return hay.indexOf(t)>-1; }); }
function lineSearch(tr, q){
  var list=tr.querySelector('.lpl'); q=(q||'').trim();
  var hits=S.prod.map(function(p,k){return {p:p,k:k};}).filter(function(x){ return !x.p.archived; }).filter(function(x){
    return !q || words(x.p.fam+' '+x.p.pack+' '+(x.p.sku||'').replace('-',' ')+' '+(x.p.sku||''), q); }).slice(0,8);
  list.innerHTML = hits.length ? hits.map(function(x,i){ var st=stat(x.p.stock,x.p.reorder);
    return '<div class="opt'+(i===0?' on':'')+'" data-lpick="'+x.k+'" role="option">'+
      '<span class="pimg sm"><img src="'+x.p.img+'" alt=""></span>'+
      '<div style="min-width:0"><div class="nm">'+esc(x.p.fam)+' <span class="mut">'+esc(x.p.pack)+'</span></div>'+
      '<div class="mt">'+esc(x.p.sku||'')+' · <span class="'+(st==='ok'?'':'bad')+'">'+x.p.stock+' in stock</span></div></div>'+
      '<div class="rt"><b>'+tk(priceFor(x.k))+'</b><br><span class="mut">per unit</span></div></div>'; }).join('')
    : '<div class="none" style="padding:14px"><b>No product matches.</b>Try the name or the SKU, like SBF-NHF-1000.</div>';
  list.classList.add('open');
}
function linePick(tr, k){
  var p=S.prod[k]; if(!p) return;
  tr.querySelector('.lp').value=k;
  tr.querySelector('.lps').value=p.fam+' · '+p.pack;
  var th=tr.querySelector('.lthumb'); if(th){ th.querySelector('img').src=p.img; th.hidden=false; }
  tr.querySelector('.lpl').classList.remove('open');
  var r=tr.querySelector('.lr'); r.dataset.touched='0';
  recalc();
  var q=tr.querySelector('.lq'); if(q){ q.focus(); q.select(); }
}
function tierNow(){ var b=document.querySelector('[data-tier][aria-pressed="true"]'); return b?b.dataset.tier:'Retail'; }
function setTier(t){ document.querySelectorAll('[data-tier]').forEach(function(b){ b.setAttribute('aria-pressed',String(b.dataset.tier===t)); });
  document.querySelectorAll('#lineBody .lr').forEach(function(r){r.dataset.touched='0';}); recalc(); }
function priceFor(k){ return tierNow()==='Retail' ? S.prod[k].r : S.prod[k].w; }
function recalc(){
  var all=[].slice.call(document.querySelectorAll('#lineBody .line')),sub=0,qty=0;
  var rows=all.filter(function(tr){ return tr.querySelector('.lp').value!==''; });
  all.forEach(function(tr){
    var lp=tr.querySelector('.lp').value, hint=tr.querySelector('.lpm');
    if(lp===''){ tr.querySelector('.lt').textContent='৳0'; if(hint) hint.textContent=''; return; }
    var k=+lp, q=num(tr.querySelector('.lq')), p=S.prod[k];
    var rEl=tr.querySelector('.lr');
    if(rEl.dataset.touched!=='1') rEl.value=priceFor(k);
    var t=q*num(rEl); sub+=t; qty+=q;
    var qmB=tr.querySelector('.qm'); if(qmB) qmB.disabled=q<=1;
    tr.querySelector('.lt').textContent=tk(t);
    if(hint){ var over=q>p.stock;
      hint.innerHTML=(p.sku||'')+' · <span class="'+(over?'bad':'')+'">'+(over?'only ':'')+p.stock+' in stock</span>';
      tr.classList.toggle('over', over); }
  });
  couponSync(sub);
  var disc=num(document.getElementById('saleDisc')||{value:0});
  var del=num(document.getElementById('saleDeliv')||{value:0});
  var total=Math.max(sub-disc+del,0);
  var dlb=document.getElementById('rowDiscLbl'); if(dlb) dlb.textContent='Discount'+(couponOn&&couponOk?' · '+couponOn.code:'');
  var paidNow=num(document.getElementById('salePaid')||{value:0});
  var bal=total-paidNow;
  var set=function(id,v){var e=document.getElementById(id); if(e) e.textContent=v;};
  set('sumQty',rows.length?(qty+(qty===1?' unit':' units')+' across '+rows.length+(rows.length===1?' item':' items')):'No items yet');
  set('sumSub',tk(sub)); set('sumDisc','-'+tk(disc)); set('sumDel',tk(del));
  var rd=document.getElementById('rowDisc'); if(rd) rd.hidden=!disc;
  var rl=document.getElementById('rowDel');  if(rl) rl.hidden=!del;
  var inv=document.getElementById('saleInv'); if(inv) inv.textContent='INV-2609-0'+(S.seq+1);
  roll('sumTotal',total,'tk',260); roll('sumBal',bal,'tk',260);
  var b=document.getElementById('sumBalWrap');
  if(b) b.className='kpi'+(bal>0?' due':'');
  var note=document.getElementById('sumNote');
  if(note) note.textContent = bal>0 ? 'This becomes a due on the customer record'
        : bal<0 ? 'Overpaid. It will sit as advance credit' : 'Paid in full. Nothing owing';
  return {sub:sub,qty:qty,total:total,paid:paidNow,bal:bal,rows:rows};
}

/* ═══════════════════════════════════════════════════════════════════════
   SAVE — the moment that proves Single Data Entry
   One write. Dashboard, customer record, timeline and reports all move.
   ═══════════════════════════════════════════════════════════════════════ */
function saveSale(){
  var t=recalc();
  if(!picked){ say('Pick a customer first. Search by name, ID or phone.');
    var i=document.getElementById('cbxInput'); if(i){i.focus();} return; }
  if(!t.rows.length){ say('Add at least one product. Type a name or a SKU in the item box.');
    var f=document.querySelector('#lineBody .lps'); if(f) f.focus(); return; }
  if(t.total<=0){ say('Every item needs a quantity and a rate.'); return; }
  var short=null, need={}, had={};
  if(editingInv){ var ex=findSale(editingInv); if(ex) (ex.o.it||[]).forEach(function(l){ had[l.k]=(had[l.k]||0)+l.q; }); }
  t.rows.forEach(function(tr){ var k=+tr.querySelector('.lp').value, q=num(tr.querySelector('.lq'));
    need[k]=(need[k]||0)+q; });
  Object.keys(need).forEach(function(k){ if(!short && need[k]-(had[k]||0)>S.prod[k].stock) short={p:S.prod[k],q:need[k]}; });
  if(editingInv){ var ex2=findSale(editingInv); if(ex2 && t.total<ex2.o.p){ say('<b>Total '+tk(t.total)+' is below what is already paid ('+tk(ex2.o.p)+').</b> Keep the total at or above the payments, or record a refund (Phase 4).'); return; } }
  if(short){ say('<b>Only '+short.p.stock+' of '+esc(short.p.fam+' '+short.p.pack)+' in stock.</b> '+
    'You asked for '+short.q+'. Record a stock-in or a production batch first.'); return; }

  var btn=document.getElementById('saveBtn');
  btn.disabled=true; btn.innerHTML='<span class="spin"></span>Saving';

  setTimeout(function(){
    if(editingInv){ saveEdit(t, btn); return; }
    S.seq++;
    var inv='INV-2609-0'+S.seq;
    var date='26 Sep 2026';
    var method=(document.getElementById('salePayMethod')||{}).value||'Cash';

    /* mark previous "new" flags stale so only this one flashes */
    S.cust.forEach(function(c){ c.isNew=false;
      c.o.forEach(function(o){o.isNew=false;}); c.p.forEach(function(p){p.isNew=false;}); });

    var lines=[];
    t.rows.forEach(function(tr){
      var k=+tr.querySelector('.lp').value, q=num(tr.querySelector('.lq')),
          r=num(tr.querySelector('.lr'));
      if(q>0) lines.push({k:k,q:q,r:r,t:q*r}); });
    var disc0=num(document.getElementById('saleDisc')||{value:0}), del0=num(document.getElementById('saleDeliv')||{value:0});
    var note0=(((document.getElementById('saleNote')||{}).value)||'').trim();
    picked.o.push({inv:inv,d:date,n:t.qty,t:t.total,p:t.paid,src:'Manual',
                   pending:true,isNew:true,it:lines,disc:disc0,del:del0,note:note0,method:method,coupon:(couponOn&&couponOk?couponOn.code:'')});
    lines.forEach(function(l){ moveStock(l.k, -l.q, 'Out', inv); S.prod[l.k].bump=true; });
    if(t.paid>0) picked.p.push({d:date,m:method,a:t.paid,inv:inv,isNew:true});
    picked.last=date;

    var saved=picked, amt=t.total, bal=t.bal;

    /* everything re-reads from the store. Nothing is updated by hand. */
    renderDash(); renderCustomers(); renderAccounts(); renderSales();
    renderProducts(); renderProduct(); renderInventory(); renderNotifs();
    current=saved.code; renderProfile(); renderTimeline();

    btn.innerHTML='<span class="okdraw">'+CHK+'</span>Saved';
    setTimeout(function(){ btn.disabled=false; btn.innerHTML=CHK+'Save sale'; },900);
    resetSale();

    say('<b>'+esc(inv)+' saved.</b> '+tk(amt)+' to '+esc(saved.name)+
        (bal>0?' · '+tk(bal)+' due':' · paid in full')+
        ' &nbsp;<a href="#sale" data-inv="'+inv+'" style="color:#2BD255;font-weight:650">Open invoice →</a>');

    slFilter='all'; var ss=document.getElementById('slSearch'); if(ss) ss.value='';
    location.hash='sales';
    setTimeout(function(){
      var row=document.querySelector('#slBody tr.fresh');
      if(row) row.scrollIntoView({block:'center',behavior:'smooth'});
    },260);
  },620);
}

var CHKSVG=(function(){ var b=document.getElementById('saveBtn'); var sv=b&&b.querySelector('svg'); return sv?sv.outerHTML:''; })();
var COUPONS=__COUPONS__, couponOn=null, couponOk=false,
    COUPON_HINT='Codes are created in WooCommerce. The same code works on the website and here.';
function couponApply(){
  var i=document.getElementById('saleCoupon'), m=document.getElementById('couponMsg'); if(!i) return;
  var code=(i.value||'').trim().toUpperCase(); i.value=code;
  if(!code){ couponOn=null; if(m){m.textContent=COUPON_HINT; m.className='hint';} recalc(); return; }
  var c=COUPONS.filter(function(x){return x.code===code;})[0];
  if(!c){ if(couponOn&&couponOn.type!=='delivery'){ var d0=document.getElementById('saleDisc'); if(d0) d0.value=0; } couponOn=null; if(m){m.textContent='No coupon '+code+'. Codes live in WooCommerce → Marketing → Coupons.'; m.className='hint bad';} recalc(); return; }
  couponOn=c; recalc();
}
function couponSync(sub){
  var m=document.getElementById('couponMsg'); if(!couponOn){ couponOk=false; return; }
  var dEl=document.getElementById('saleDisc'), dlEl=document.getElementById('saleDeliv');
  couponOk = couponOn.type!=='fixed' || sub>=couponOn.min;
  if(couponOn.type==='percent'){ if(dEl) dEl.value=Math.round(sub*couponOn.v/100); }
  else if(couponOn.type==='fixed'){ if(dEl) dEl.value=couponOk?couponOn.v:0; }
  else if(couponOn.type==='delivery'){ if(dlEl) dlEl.value=0; }
  if(couponOn.type!=='delivery'){ var dw=document.getElementById('discWrap'), sd=document.getElementById('showDisc'); if(dw) dw.hidden=false; if(sd) sd.hidden=true; }
  if(m){ m.className='hint '+(couponOk?'ok':'bad');
    m.textContent = couponOk ? couponOn.code+' applied: '+couponOn.label+(couponOn.type==='delivery'?'':' ('+tk(num(dEl))+')')
                             : couponOn.code+' needs a subtotal of '+tk(couponOn.min)+', now '+tk(sub); }
}
function resetSale(){
  picked=null; couponOn=null; couponOk=false; editingInv=null;
  var pw=document.getElementById('paidWrap'); if(pw) pw.hidden=false;
  var eb=document.getElementById('editBanner'); if(eb){ eb.hidden=true; eb.innerHTML=''; }
  var h0=document.querySelector('#v-sales-entry .ph h1'); if(h0) h0.textContent='New sale';
  var sb0=document.getElementById('saveBtn'); if(sb0&&!sb0.disabled) sb0.innerHTML=CHK+'Save sale';
  var rb0=document.getElementById('resetBtn'); if(rb0) rb0.innerHTML=XI+'Discard draft';
  var cw=document.getElementById('couponWrap'); if(cw) cw.hidden=true;
  var ci=document.getElementById('saleCoupon'); if(ci) ci.value='';
  var cm=document.getElementById('couponMsg'); if(cm){ cm.textContent=COUPON_HINT; cm.className='hint'; }
  var i=document.getElementById('cbxInput'); if(i) i.value='';
  var c=document.getElementById('cbxCard');
  if(c) c.innerHTML='<div class="none" style="padding:18px"><b>No customer selected</b>'+
    'Search above by name, customer ID or phone number.</div>';
  var lb=document.getElementById('lineBody'); if(lb) lb.innerHTML=lineHTML(0);
  ['saleDisc','saleDeliv','salePaid'].forEach(function(id){
    var e=document.getElementById(id); if(e) e.value=0; });
  var nt=document.getElementById('saleNote'); if(nt) nt.value='';
  setMethod('salePayMethod','Cash');
  ['discWrap','delWrap'].forEach(function(id){ var e=document.getElementById(id); if(e) e.hidden=true; });
  ['showDisc','showDel','showCoupon'].forEach(function(id){ var e=document.getElementById(id); if(e) e.hidden=false; });
  var tg=document.querySelector('[data-tier][aria-pressed="true"]'); if(!tg){ var w=document.querySelector('[data-tier="Wholesale"]'); if(w) w.setAttribute('aria-pressed','true'); }
  recalc();
}

/* ═══════════════════════════════════════════════════════════════════════
   GLOBAL SEARCH — one box, customers and invoices
   ═══════════════════════════════════════════════════════════════════════ */
function gsearch(q){
  var box=document.getElementById('gsList'); if(!box) return;
  q=(q||'').trim().toLowerCase();
  if(!q){ box.classList.remove('open'); return; }
  var out=[];
  S.cust.forEach(function(c){
    if((c.code+' '+c.name+' '+c.phone+' '+c.district).toLowerCase().indexOf(q)>-1)
      out.push({t:c.name,s:c.code+' · '+c.phone+' · '+tk(sold(c))+' lifetime',code:c.code,k:'Customer'});
    c.o.forEach(function(o){ if(o.inv.toLowerCase().indexOf(q)>-1)
      out.push({t:o.inv,s:c.name+' · '+o.d+' · '+tk(o.t),code:c.code,k:'Invoice'}); });
  });
  S.prod.forEach(function(p,k){ if((p.fam+' '+p.pack+' '+(p.sku||'')).toLowerCase().indexOf(q)>-1)
    out.push({t:p.fam+' '+p.pack,s:p.stock+' in stock · retail '+tk(p.r)+' · '+prodStats(k).units+' sold',prod:k,k:'Product'}); });
  out=out.slice(0,8);
  box.innerHTML = out.length ? out.map(function(r,i){
    return '<div class="opt'+(i===0?' on':'')+'"'+(r.code?' data-open="'+r.code+'"':' data-prod="'+r.prod+'"')+'>'+
      '<div class="av">'+esc(r.t[0])+'</div><div style="min-width:0">'+
      '<div class="nm">'+esc(r.t)+'</div><div class="mt">'+esc(r.s)+'</div></div>'+
      '<div class="rt">'+r.k+'</div></div>'; }).join('')
    : '<div class="none" style="padding:18px"><b>Nothing found</b>Try a customer, phone, invoice number or product.</div>';
  box.classList.add('open');
}

/* ═══════════════════════════════════════════════════════════════════════
   ROUTER + EVENTS
   ═══════════════════════════════════════════════════════════════════════ */
var CRUMB={dashboard:['Overview','Dashboard'],'sales-entry':['Sales','New sale'],sales:['Sales','Orders'],sale:['Sales','Order'],
  customers:['Customers','All customers'],'customer-profile':['Customers','Customer profile'],
  'customer-timeline':['Customers','Activity timeline'],followups:['Customers','Follow-ups'],
  products:['Catalogue','Products'], product:['Catalogue','Product detail'],
  inventory:['Operations','Inventory'],dues:['Finance','Dues'],accounts:['Finance','Accounts'],
  reports:['Finance','Reports'],settings:['System','Settings']};

function route(){
  var id=(location.hash||'#dashboard').slice(1)||'dashboard';
  if(id==='inventory') id='products';
  if(id==='payment'){ location.hash='dues'; setTimeout(function(){ colOpen(); },80); return; }
  if(!document.getElementById('v-'+id)) id='dashboard';
  document.querySelectorAll('.view').forEach(function(v){ v.hidden=(v.id!=='v-'+id); });
  var el=document.getElementById('v-'+id);
  if(el){ el.style.animation='none'; void el.offsetWidth; el.style.animation='';
    el.querySelectorAll('[data-v]').forEach(function(x){ x.dataset.v='0'; }); }
  document.querySelectorAll('.nav a').forEach(function(a){
    var h=a.getAttribute('href').slice(1);
    var on = h===id || (id==='customer-profile'&&h==='customers')
             || (id==='customer-timeline'&&h==='customers') || (id==='product'&&h==='products') || (id==='sale'&&h==='sales') || (id==='sales-entry'&&h==='sales');
    if(on) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); });
  var c=CRUMB[id]||['','']; var cr=document.getElementById('crumb');
  if(cr) cr.innerHTML=esc(c[0])+' <span style="color:var(--ink-4)">/</span> <b>'+esc(c[1])+'</b>';
  document.title='Shada BMS · '+c[1];
  window.scrollTo({top:0});
  if(id==='dashboard') renderDash();
  if(id==='customers') renderCustomers();
  if(id==='sales') renderSales(); if(id==='dues') renderDues();
  if(id==='sale') renderSale();
  if(id==='customer-profile') renderProfile();
  if(id==='customer-timeline') renderTimeline();
  if(id==='sales-entry'){ recalc(); }
  if(id==='accounts') renderAccounts();
  if(id==='settings') renderSettings();
  if(id==='inventory') renderInventory();
  if(id==='products') renderProducts();
  if(id==='product') renderProduct();
}
window.addEventListener('hashchange',route);

document.addEventListener('click',function(e){
  var t=e.target;

  var psb=t.closest('.pselb'); if(psb){ var pw=psb.closest('[data-ppick]'); var pl=pw.querySelector('.plist'); var o=!pl.classList.contains('open'); pl.classList.toggle('open',o); psb.setAttribute('aria-expanded',String(o)); return; }
  var ppk=t.closest('[data-ppk]'); if(ppk){ ppickSet(ppk.closest('[data-ppick]').dataset.ppick, +ppk.dataset.ppk); return; }
  var ed=t.closest('[data-edit]'); if(ed){ e.preventDefault(); editOrder(ed.getAttribute('data-edit')); return; }
  if(t.closest('#sdEdit')){ if(curInv) editOrder(curInv); return; }
  var open=t.closest('[data-open]');
  if(open && !t.closest('[data-collect]')){ e.preventDefault(); openCustomer(open.getAttribute('data-open'),
      open.getAttribute('data-view')||'customer-profile');
    document.getElementById('gsList').classList.remove('open'); return; }

  var tick=t.closest('[data-fu]');
  if(tick){ toggleFu(tick.getAttribute('data-fu')); return; }
  var call=t.closest('[data-call]');
  if(call){ logCall(call.getAttribute('data-call')); return; }
  if(t.closest('#fuAdd')){ fuOpenModal(); return; }
  if(t.closest('#fuSave')){ fuSave(); return; }
  if(t.closest('#fuCancel')||t.closest('#fuModal .scrimclose')){ fuClose(); return; }
  if(t.id==='fuModal'){ fuClose(); return; }

  if(t.closest('#custAdd')){ custOpen(); return; }
  if(t.closest('#pfEdit')){ custEdit(current); return; }
  if(t.closest('[data-nctier]')){ ncTierPick(t.closest('[data-nctier]').dataset.nctier); return; }
  var sti=t.closest('[data-stockin]');
  if(sti){ e.preventDefault(); e.stopPropagation(); stockInOpen(sti.getAttribute('data-stockin')); return; }
  if(t.closest('#invStockIn')){ stockInOpen(); return; }
  if(t.closest('#invBatch')){ batchOpen(); return; }
  if(t.closest('#prodAdd')){ newProdOpen(); return; }
  if(t.closest('#pdEdit')){ prodEditOpen(); return; }
  if(t.closest('#epArchive')){ prodArchiveToggle(); return; }
  var pp=t.closest('[data-pp]'); if(pp){ ppTab=pp.dataset.pp; renderProducts(); return; }
  var pf=t.closest('[data-pf]'); if(pf){ pfTab=pf.dataset.pf; renderProducts(); return; }
  if(t.closest('#showCoupon')){ document.getElementById('couponWrap').hidden=false; document.getElementById('showCoupon').hidden=true; document.getElementById('saleCoupon').focus(); return; }
  if(t.closest('#couponApply')){ couponApply(); return; }
  if(t.closest('#epSave')){ prodEditSave(); return; }
  if(t.closest('#epCancel')||t.id==='epModal'){ document.getElementById('epModal').classList.remove('open'); return; }
  if(t.closest('#siSave')){ stockInSave(); return; }
  if(t.closest('#pbSave')){ batchSave(); return; }
  if(t.closest('#npSave')){ newProdSave(); return; }
  if(t.closest('#siCancel')||t.id==='siModal'){ document.getElementById('siModal').classList.remove('open'); return; }
  if(t.closest('#pbCancel')||t.id==='pbModal'){ document.getElementById('pbModal').classList.remove('open'); return; }
  if(t.closest('#npCancel')||t.id==='npModal'){ document.getElementById('npModal').classList.remove('open'); return; }
  if(t.closest('#acCollect')||t.closest('#duCollect')){ colOpen(); return; }
  if(t.closest('#pfPay')||t.closest('#pfPay2')){ colOpen(current); return; }
  var df=t.closest('[data-df]'); if(df){ duTab=df.dataset.df; renderDues(); return; }
  if(t.closest('#acExpense')){ expOpen(); return; }
  if(t.closest('#coSave')){ colSave(); return; }
  if(t.closest('#coCancel')){ colClose(); return; }
  if(t.closest('#exSave')){ expSave(); return; }
  if(t.closest('#exCancel')){ expClose(); return; }
  if(t.id==='colModal'){ colClose(); return; }
  if(t.id==='expModal'){ expClose(); return; }
  var coll=t.closest('[data-collect]');
  if(coll){ e.preventDefault(); colOpen(coll.getAttribute('data-collect')); return; }
  if(t.closest('#ncSave')){ custSave(); return; }
  if(t.closest('#ncCancel')){ custClose(); return; }
  if(t.id==='custModal'){ custClose(); return; }

  /* the toast shortcut: jump to New sale with that customer already selected */
  var sell=t.closest('[data-sell]');
  if(sell){ e.preventDefault(); location.hash='sales-entry';
    setTimeout(function(){ cbxPick(sell.getAttribute('data-sell')); },80); return; }

  var bell=t.closest('#bell');
  if(bell){ e.preventDefault();
    document.getElementById('notifPanel').classList.toggle('open'); return; }
  if(!t.closest('#notifWrap')){
    var np=document.getElementById('notifPanel'); if(np) np.classList.remove('open'); }

  /* a tab bar still moves even when the filter itself is a later phase */
  var tab=t.closest('[data-tab]');
  if(tab){
    tab.parentNode.querySelectorAll('[data-tab]').forEach(function(x){
      x.setAttribute('aria-pressed', String(x===tab)); }); }

  /* Nothing on screen is allowed to be dead. Anything not wired above says
     plainly what it does or which build phase turns it on. */
  var soon=t.closest('[data-soon]');
  if(soon){ e.preventDefault(); say(soon.getAttribute('data-soon')); return; }

  var drow=t.closest('[data-district]');
  if(drow){
    var sel=document.getElementById('custDistrict');
    var v=drow.getAttribute('data-district');
    if(sel){ sel.value = (sel.value===v ? '' : v); renderCustomers(); }
    location.hash='customers'; return; }

  if(t.closest('#custClear')){
    var sd=document.getElementById('custDistrict'); if(sd) sd.value='';
    var sq=document.getElementById('custSearch');   if(sq) sq.value='';
    renderCustomers(); return; }

  var row=t.closest('.crow');
  if(row&&row.getAttribute('data-inv')){ openSale(row.getAttribute('data-inv')); return; }
  if(row&&row.getAttribute('data-code')){ openCustomer(row.getAttribute('data-code')); return; }

  var per=t.closest('[data-period]');
  if(per){ period=per.dataset.period; renderDash(); return; }

  var iv=t.closest('[data-inv]');
  if(iv && !t.closest('[data-open]') && !t.closest('[data-edit]')){ e.preventDefault(); openSale(iv.getAttribute('data-inv')); return; }
  if(t.closest('#sdDeliver')){ deliverToggle(); return; }
  if(t.closest('#sdRepeat')){ repeatOrder(); return; }
  if(t.closest('#sdCollect')){ var xs=findSale(curInv); if(xs) colOpen(xs.c.code, xs.o.inv); return; }
  var sf=t.closest('[data-sf]');
  if(sf){ slFilter=sf.dataset.sf; renderSales(); return; }
  var acper=t.closest('[data-acper]');
  if(acper){ acPeriod=acper.dataset.acper; renderAccounts(); return; }

  var pc=t.closest('[data-prod]');
  if(pc && !t.closest('[data-stockin]')){ e.preventDefault(); openProduct(pc.getAttribute('data-prod'));
    var np=document.getElementById('notifPanel'); if(np) np.classList.remove('open');
    var gl=document.getElementById('gsList'); if(gl) gl.classList.remove('open'); return; }

  var itab=t.closest('[data-inv]');
  if(itab){ invTab=itab.dataset.inv; renderInventory(); return; }

  var stab=t.closest('[data-stab]');
  if(stab){ setTab=stab.dataset.stab; renderSettings(); return; }
  if(t.closest('#setSave')){ settingsSave(); return; }
  if(t.closest('#setBackup')){ settingsBackup(); return; }

  var pick=t.closest('[data-pick]');
  if(pick){ cbxPick(pick.getAttribute('data-pick')); return; }
  var dpk=t.closest('[data-dpick]');
  if(dpk){ var di=document.getElementById('ncDistrict'); di.value=dpk.getAttribute('data-dpick'); document.getElementById('ncDistList').classList.remove('open'); var ar=document.getElementById('ncArea'); if(ar) ar.focus(); return; }

  if(t.closest('[data-new]')){ say('New customer form opens here. Wired in Phase 2.'); return; }
  if(t.closest('#addLine')){
    var lb=document.getElementById('lineBody');
    lb.insertAdjacentHTML('beforeend', lineHTML(document.querySelectorAll('#lineBody .line').length)); recalc();
    var last=lb.querySelector('.line:last-child .lps'); if(last) last.focus(); return; }
  var lpk=t.closest('[data-lpick]');
  if(lpk){ linePick(lpk.closest('.line'), +lpk.getAttribute('data-lpick')); return; }
  var qb=t.closest('.qb');
  if(qb){ var qi=qb.parentElement.querySelector('.lq'); var v=Math.max(1,num(qi)+(qb.classList.contains('qp')?1:-1)); qi.value=v; recalc(); return; }
  var msb=t.closest('[data-msel]');
  if(msb){ var lst=msb.parentElement.querySelector('.mlist'); var open=lst.classList.toggle('open');
    msb.setAttribute('aria-expanded',String(open)); return; }
  var mp=t.closest('[data-method]');
  if(mp){ setMethod(mp.getAttribute('data-for'), mp.getAttribute('data-method')); return; }
  var tb=t.closest('[data-tier]');
  if(tb){ setTier(tb.dataset.tier); return; }
  if(t.closest('#showDisc')){ document.getElementById('discWrap').hidden=false; document.getElementById('showDisc').hidden=true; document.getElementById('saleDisc').focus(); return; }
  if(t.closest('#showDel')){ document.getElementById('delWrap').hidden=false; document.getElementById('showDel').hidden=true; document.getElementById('saleDeliv').focus(); return; }
  if(t.closest('.ldel')){
    var rows=document.querySelectorAll('#lineBody .line');
    if(rows.length>1) t.closest('tr').remove(); else { var tr0=rows[0]; tr0.querySelector('.lp').value=''; tr0.querySelector('.lps').value=''; tr0.querySelector('.lr').value=''; tr0.querySelector('.lq').value=1; var th0=tr0.querySelector('.lthumb'); if(th0) th0.hidden=true; }
    recalc(); return; }
  if(t.closest('#saveBtn')){ saveSale(); return; }
  if(t.closest('#resetBtn')){ var was=editingInv; resetSale(); if(was){ openSale(was); say('Edit cancelled. '+esc(was)+' unchanged.'); } else say('Draft discarded. Next invoice number is ready.'); return; }
  if(t.closest('#tlBtn')){ location.hash='customer-timeline'; return; }

  if(!t.closest('.cbx')){
    document.querySelectorAll('.cbxlist').forEach(function(l){l.classList.remove('open');}); }
},false);

document.addEventListener('input',function(e){
  if(e.target.id==='saleDisc'&&couponOn){ couponOn=null; couponOk=false; var cm=document.getElementById('couponMsg'); if(cm){cm.textContent='Coupon removed. Manual discount instead.'; cm.className='hint';} var ci=document.getElementById('saleCoupon'); if(ci) ci.value=''; }
  var id=e.target.id;
  if(id==='cbxInput'){ cbxRender(e.target.value); picked=null; return; }
  if(id==='ncDistrict'){ distSearch(e.target.value); return; }
  if(id==='gs'){ gsearch(e.target.value); return; }
  if(id==='custSearch'){ renderCustomers(); return; }
  if(id==='slSearch'){ renderSales(); return; }
  if(id==='coAmt'){ e.target.dataset.touched='1'; return; }
  if(id==='pbQty'){ batchPreview(); return; }
  if(e.target.dataset && e.target.dataset.cfg){
    var d=document.getElementById('setDirty');
    var n=changedFields().length;
    if(d) d.textContent=n?(n+' unsaved change'+(n===1?'':'s')):'No unsaved changes';
    return; }
  if(e.target.classList.contains('lps')){ var trx=e.target.closest('.line'); lineSearch(trx, e.target.value);
    trx.querySelector('.lp').value=''; var thx=trx.querySelector('.lthumb'); if(thx) thx.hidden=true; recalc(); return; }
  if(e.target.classList.contains('lr')) e.target.dataset.touched='1';
  if(e.target.closest('#saleForm')) recalc();
},false);

document.addEventListener('keydown',function(e){
  if(e.target&&e.target.id==='saleCoupon'&&e.key==='Enter'){ e.preventDefault(); couponApply(); } });
document.addEventListener('change',function(e){
  if(e.target.id==='epFile'){ epFilePick(e.target.files&&e.target.files[0]); return; }
  if(e.target.id==='ncBanner'){ ncBannerPick(e.target.files&&e.target.files[0]); return; }
  if(e.target.id==='pbProd'){ batchPreview(); return; }
  if(e.target.id==='npFam'){ var nn=document.getElementById('npNewName'); if(nn){ nn.parentElement.hidden=e.target.value!=='__new'; if(e.target.value==='__new') nn.focus(); } return; }
  if(e.target.id==='coCust'){
    var a=document.getElementById('coAmt'); if(a) a.dataset.touched='';
    colSync(); return; }
  if(e.target.id==='custDistrict'){ renderCustomers(); return; }
  if(e.target.closest('#saleForm')) recalc();
},false);

document.addEventListener('focusin',function(e){
  if(e.target.classList&&e.target.classList.contains('lps')) lineSearch(e.target.closest('.line'), e.target.value);
  if(e.target.id==='ncDistrict') distSearch(e.target.value);
},false);

document.addEventListener('keydown',function(e){
  if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){
    e.preventDefault(); var g=document.getElementById('gs'); if(g){g.focus();g.select();} return; }
  if(e.key==='Escape'){
    document.querySelectorAll('.cbxlist').forEach(function(l){l.classList.remove('open');});
    ['custModal','colModal','expModal','siModal','pbModal','npModal','epModal'].forEach(function(id){
      var m=document.getElementById(id); if(m) m.classList.remove('open'); });
    var np=document.getElementById('notifPanel'); if(np) np.classList.remove('open');
    return; }
  if((e.key===' '||e.key==='Enter')&&e.target.classList&&e.target.classList.contains('tick')){
    e.preventDefault(); e.target.click(); return; }
  if(e.key==='Enter'&&e.target.id==='ncDistrict'){ e.preventDefault(); var dd=document.querySelector('#ncDistList .opt.on')||document.querySelector('#ncDistList .opt'); if(dd&&dd.dataset.dpick){ e.target.value=dd.dataset.dpick; document.getElementById('ncDistList').classList.remove('open'); var ar2=document.getElementById('ncArea'); if(ar2) ar2.focus(); } return; }
  if(e.key==='Enter'&&e.target.closest&&e.target.closest('#epForm')){ e.preventDefault(); prodEditSave(); return; }
  if(e.key==='Enter'&&e.target.closest&&e.target.closest('#custForm')){
    e.preventDefault(); custSave(); return; }
  if(e.target.classList&&e.target.classList.contains('lps')){
    var trl=e.target.closest('.line'), lst=trl.querySelector('.lpl');
    if(e.key==='Enter'){ e.preventDefault(); var o=lst.querySelector('.opt.on')||lst.querySelector('.opt'); if(o&&o.dataset.lpick!==undefined) linePick(trl,+o.dataset.lpick); return; }
    if(e.key==='ArrowDown'||e.key==='ArrowUp'){ e.preventDefault(); var os=[].slice.call(lst.querySelectorAll('.opt')); if(!os.length) return;
      var ii=os.findIndex(function(o){return o.classList.contains('on');}); os.forEach(function(o){o.classList.remove('on');});
      ii=e.key==='ArrowDown'?Math.min(ii+1,os.length-1):Math.max(ii-1,0); os[ii].classList.add('on'); os[ii].scrollIntoView({block:'nearest'}); return; }
    if(e.key==='Escape'){ lst.classList.remove('open'); return; } }
  if(e.target.classList&&e.target.classList.contains('mselb')){
    var ml=e.target.parentElement.querySelector('.mlist'), opts=[].slice.call(ml.querySelectorAll('[data-method]'));
    var cur=opts.findIndex(function(o){return o.getAttribute('aria-selected')==='true';});
    if(e.key==='ArrowDown'||e.key==='ArrowUp'){ e.preventDefault(); var ni=e.key==='ArrowDown'?Math.min(cur+1,opts.length-1):Math.max(cur-1,0);
      setMethod(e.target.getAttribute('data-msel'), opts[ni].getAttribute('data-method')); return; }
    if(e.key==='Escape'){ ml.classList.remove('open'); e.target.setAttribute('aria-expanded','false'); return; } }
  if(e.key==='Enter'&&e.target.classList&&e.target.classList.contains('lq')){
    e.preventDefault(); var ab=document.getElementById('addLine'); if(ab) ab.click(); return; }
  if(e.key==='Enter'&&e.target.id==='cbxInput'){
    e.preventDefault(); var on=document.querySelector('#cbxList .opt.on')||document.querySelector('#cbxList .opt');
    if(on&&on.dataset.pick) cbxPick(on.dataset.pick); return; }
  if(e.key==='Enter'&&e.target.classList.contains('crow')){ e.target.click(); }
  if((e.key==='ArrowDown'||e.key==='ArrowUp')&&e.target.id==='cbxInput'){
    e.preventDefault();
    var opts=[].slice.call(document.querySelectorAll('#cbxList .opt'));
    if(!opts.length) return;
    var i=opts.findIndex(function(o){return o.classList.contains('on');});
    opts.forEach(function(o){o.classList.remove('on');});
    i = e.key==='ArrowDown' ? Math.min(i+1,opts.length-1) : Math.max(i-1,0);
    opts[i].classList.add('on'); opts[i].scrollIntoView({block:'nearest'}); }
},false);

/* ═══════════════════════════════════════════════════════════════════════
   BOOT
   ═══════════════════════════════════════════════════════════════════════ */
resetSale();
renderDash(); renderCustomers(); renderProfile(); renderTimeline();
renderAccounts(); renderSettings(); renderInventory();
renderProducts(); renderProduct(); renderSales(); renderNotifs();
route();
})();
'''
