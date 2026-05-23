"""Build present.html — 商談者用 左右分割ビュー。
左=台本（クリックでスライド連動）、右=確認用スライド。別窓の顧客提示画面と同期。
slide rendering JS is reused verbatim from build_html.py so both views stay identical."""
import json, re

with open('slides_data.json', encoding='utf-8') as f:
    DATA = json.load(f)
DATA_JSON = json.dumps(DATA, ensure_ascii=False)

# --- pull the render() function + slide CSS out of build_html.py so we never diverge ---
with open('build_html.py', encoding='utf-8') as f:
    src = f.read()

# slide CSS lives between the first ":root{" block start and the "/* ---------- chrome" marker
css_match = re.search(r'(:root\{.*?)(/\* ---------- chrome)', src, re.S)
SLIDE_CSS = css_match.group(1)

# render() function body: from "function esc" through the close of "function render"
rnd_match = re.search(r'(function esc\(s\).*?function render\(s\)\{.*?\n    default: return.*?\n  \}\n\}\n)', src, re.S)
RENDER_JS = rnd_match.group(1)

HTML = r'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CBA 商談ビュー（商談者用）</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<style>
__SLIDE_CSS__
  /* ===== presenter shell ===== */
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;font-family:"Noto Serif JP",serif;background:#15100e;color:#3A2D2A;overflow:hidden}
  #app{display:flex;height:100vh}

  /* left: script */
  #script{width:38%;min-width:330px;max-width:560px;height:100vh;overflow-y:auto;background:#1a1411;
          border-right:1px solid rgba(232,221,213,.12);padding:0 0 120px}
  #script::-webkit-scrollbar{width:9px}
  #script::-webkit-scrollbar-thumb{background:rgba(232,221,213,.18);border-radius:5px}
  .sc-top{position:sticky;top:0;z-index:5;background:#0f0b09;padding:16px 22px;border-bottom:1px solid rgba(232,221,213,.12)}
  .sc-top .ttl{font-family:"Cormorant Garamond",serif;letter-spacing:.18em;font-size:15px;color:#e8ddd5}
  .sc-top .sub{font-size:11px;color:#9a8b80;letter-spacing:.08em;margin-top:3px}
  .sc-item{padding:18px 22px;border-bottom:1px solid rgba(232,221,213,.08);cursor:pointer;transition:background .15s}
  .sc-item:hover{background:rgba(232,221,213,.04)}
  .sc-item.active{background:rgba(232,155,126,.12);border-left:3px solid var(--accent);padding-left:19px}
  .sc-head{display:flex;align-items:center;gap:10px;margin-bottom:9px}
  .sc-num{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:19px;color:var(--accent)}
  .sc-sec{font-size:10px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase}
  .sc-badge{font-size:9px;letter-spacing:.12em;background:var(--accent);color:#1a1411;padding:2px 7px;border-radius:9px}
  .sc-stitle{font-size:13px;color:#fff;opacity:.82;margin-bottom:10px;letter-spacing:.04em;line-height:1.4}
  .sc-lbl{font-size:9px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase;margin:11px 0 4px}
  .sc-talk{font-size:13.5px;line-height:1.85;letter-spacing:.02em;color:#f0e8e1}
  .sc-cue{font-size:12px;line-height:1.7;color:#c2b1a6;border-left:2px solid var(--accent);padding-left:11px;margin-top:4px}

  /* right: slide stage */
  #right{flex:1;display:flex;flex-direction:column;background:#241c1a;height:100vh}
  #rbar{height:50px;flex:0 0 50px;display:flex;align-items:center;justify-content:space-between;
        padding:0 18px;background:#1a1411;border-bottom:1px solid rgba(232,221,213,.1)}
  #rbar .pos{font-family:"Cormorant Garamond",serif;letter-spacing:.16em;font-size:14px;color:#c2b1a6}
  #rbar .btns{display:flex;gap:8px}
  #rbar button{background:rgba(232,221,213,.1);color:#e8ddd5;border:1px solid rgba(232,221,213,.22);
               border-radius:16px;padding:6px 15px;font-size:12px;letter-spacing:.06em;cursor:pointer;
               font-family:"Noto Serif JP",serif}
  #rbar button:hover{background:rgba(232,221,213,.2)}
  #rbar button.share{background:rgba(232,155,126,.18);border-color:rgba(232,155,126,.55);color:#f8d7ca}
  #rbar button.fs{background:var(--accent);color:#1a1411;border-color:var(--accent);font-weight:500}
  #rstage{flex:1;display:flex;align-items:center;justify-content:center;padding:22px;min-height:0}
  #rframe{position:relative;width:100%;aspect-ratio:16/9;max-height:100%;max-width:calc((100vh - 94px)*1.7778);
          background:var(--bg);overflow:hidden;container-type:size;box-shadow:0 10px 40px rgba(0,0,0,.4)}
  .slide{position:absolute;inset:0;opacity:0;transition:opacity .4s ease;pointer-events:none}
  .slide.active{opacity:1;pointer-events:auto}

  /* fullscreen mode: right frame fills screen, hide everything else */
  body.fs #script,body.fs #rbar{display:none}
  body.fs #right{height:100vh}
  body.fs #rstage{padding:0}
  body.fs #rframe{aspect-ratio:auto;width:100vw;height:100vh;max-width:none;max-height:none;box-shadow:none}
  #fsexit{display:none;position:fixed;top:14px;right:16px;z-index:100;background:rgba(36,28,26,.55);
          color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:18px;padding:7px 16px;
          font-size:12px;letter-spacing:.08em;cursor:pointer;font-family:"Noto Serif JP",serif}
  body.fs #fsexit{display:block}
  body.fs #fsexit:hover{background:rgba(36,28,26,.8)}

  /* customer display: /customer is a clean, shareable screen. It listens to /present. */
  body.customer #script,body.customer #rbar,body.customer #fsexit{display:none}
  body.customer #app,body.customer #right{width:100vw;height:100vh}
  body.customer #rstage{padding:0;width:100vw;height:100vh}
  body.customer #rframe{aspect-ratio:auto;width:100vw;height:100vh;max-width:none;max-height:none;box-shadow:none}
  body.customer{background:#241c1a}

  @media(max-width:900px){
    #app{flex-direction:column}
    #script{width:100%;max-width:none;height:42vh;border-right:none;border-bottom:1px solid rgba(232,221,213,.12)}
    #right{height:58vh}
  }
</style>
</head>
<body>
<div id="app">
  <div id="script">
    <div class="sc-top">
      <div class="ttl">PRESENTER SCRIPT</div>
      <div class="sub">台本をクリック → 右のスライドが連動します</div>
    </div>
    <div id="sclist"></div>
  </div>
  <div id="right">
    <div id="rbar">
      <span class="pos" id="pos"></span>
      <div class="btns">
        <button onclick="go(-1)">‹ 前</button>
        <button onclick="go(1)">次 ›</button>
        <button class="share" onclick="openCustomer()">↗ 顧客提示画面を別窓で開く</button>
        <button class="fs" onclick="enterFs()">⛶ この画面を全画面</button>
      </div>
    </div>
    <div id="rstage"><div id="rframe"></div></div>
  </div>
</div>
<button id="fsexit" onclick="exitFs()">✕ 全画面を終了（商談者ビューに戻る）</button>

<script>
const DATA = __DATA__;
const S = DATA.slides, IMG = DATA.images;
let cur = 0;

const VIEW_MODE = (()=>{
  const path = location.pathname.replace(/\/$/,'');
  const q = new URLSearchParams(location.search);
  return (path.endsWith('/customer') || q.get('view') === 'customer') ? 'customer' : 'presenter';
})();
const IS_CUSTOMER = VIEW_MODE === 'customer';
if(IS_CUSTOMER) document.body.classList.add('customer');

const SYNC_CHANNEL = 'cba-present-sync-v1';
const SYNC_KEY = 'cba-present-current-slide';
let bc = null;
try{
  bc = new BroadcastChannel(SYNC_CHANNEL);
  bc.onmessage = e => {
    const msg = e.data || {};
    if(IS_CUSTOMER && msg.type === 'slide') show(Number(msg.index)||0,{broadcast:false,scroll:false});
  };
}catch(e){}

function publishSlide(i){
  const msg = {type:'slide', index:i, ts:Date.now()};
  try{ if(bc) bc.postMessage(msg); }catch(e){}
  try{ localStorage.setItem(SYNC_KEY, JSON.stringify(msg)); }catch(e){}
}
function readInitialSlide(){
  const q = new URLSearchParams(location.search);
  if(q.has('slide')) return Math.max(0, Math.min(S.length-1, Number(q.get('slide'))||0));
  try{
    const msg = JSON.parse(localStorage.getItem(SYNC_KEY)||'{}');
    if(Number.isFinite(msg.index)) return Math.max(0, Math.min(S.length-1, msg.index));
  }catch(e){}
  return 0;
}
window.addEventListener('storage',e=>{
  if(!IS_CUSTOMER || e.key !== SYNC_KEY || !e.newValue) return;
  try{
    const msg = JSON.parse(e.newValue);
    if(msg.type === 'slide') show(Number(msg.index)||0,{broadcast:false,scroll:false});
  }catch(err){}
});
function openCustomer(){
  const url = new URL('/customer', location.origin);
  url.searchParams.set('slide', String(cur));
  const w = window.open(url.toString(), 'cba_customer_display', 'popup=yes,width=1280,height=720');
  if(w) w.focus();
  setTimeout(()=>publishSlide(cur), 300);
  setTimeout(()=>publishSlide(cur), 1000);
}

__RENDER_JS__

/* ---- build right stage ---- */
const rframe = document.getElementById('rframe');
S.forEach((s,i)=>{
  const el=document.createElement('div'); el.className='slide'; el.dataset.i=i;
  el.innerHTML=render(s); rframe.appendChild(el);
});
const slideEls=[...rframe.querySelectorAll('.slide')];

/* ---- build left script ---- */
const sclist=document.getElementById('sclist');
sclist.innerHTML=S.map((s,i)=>{
  const n=s.notes||{};
  const badge=s.badge?`<span class="sc-badge">${s.badge}</span>`:'';
  const stitle=(s.deck.title||s.deck.headline||s.deck.eyebrow||s.id).replace(/<[^>]+>/g,'');
  return `<div class="sc-item" data-i="${i}" onclick="show(${i})">
    <div class="sc-head"><span class="sc-num">${String(i+1).padStart(2,'0')}</span>
      <span class="sc-sec">${s.section||''}</span>${badge}</div>
    <div class="sc-stitle">${stitle}</div>
    ${n.talk?`<div class="sc-lbl">話す内容</div><div class="sc-talk">${n.talk}</div>`:''}
    ${n.cue?`<div class="sc-lbl">進行のポイント</div><div class="sc-cue">${n.cue}</div>`:''}
  </div>`;
}).join('');
const scItems=[...sclist.querySelectorAll('.sc-item')];

/* ---- sync ---- */
function show(i,opt={}){
  cur=Math.max(0,Math.min(S.length-1,i));
  slideEls.forEach((el,k)=>el.classList.toggle('active',k===cur));
  scItems.forEach((el,k)=>el.classList.toggle('active',k===cur));
  const pos=document.getElementById('pos');
  if(pos) pos.textContent=String(cur+1).padStart(2,'0')+' / '+String(S.length).padStart(2,'0');
  // keep active script item in view
  if(!IS_CUSTOMER && opt.scroll !== false){
    const a=scItems[cur];
    if(a){const r=a.getBoundingClientRect(),sc=document.getElementById('script');
      if(r.top<90||r.bottom>innerHeight)a.scrollIntoView({block:'center',behavior:'smooth'});}
  }
  if(!IS_CUSTOMER && opt.broadcast !== false) publishSlide(cur);
}
function go(d){show(cur+d)}

/* ---- fullscreen (customer-facing) ---- */
function enterFs(){
  document.body.classList.add('fs');
  if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen().catch(()=>{});
}
function exitFs(){
  document.body.classList.remove('fs');
  if(document.fullscreenElement)document.exitFullscreen().catch(()=>{});
}
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement)document.body.classList.remove('fs')});

/* ---- keys: arrows always work; in fullscreen click advances ---- */
addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){go(1);e.preventDefault()}
  if(e.key==='ArrowLeft'||e.key==='PageUp'){go(-1)}
  if(e.key==='Escape'&&document.body.classList.contains('fs'))exitFs();
  if(e.key==='Home')show(0); if(e.key==='End')show(S.length-1);
});
rframe.addEventListener('click',()=>{if(!IS_CUSTOMER && document.body.classList.contains('fs'))go(1)});
let tx=0;
rframe.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});
rframe.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)go(dx<0?1:-1)},{passive:true});

show(readInitialSlide(),{broadcast:false,scroll:false});
if(!IS_CUSTOMER) setTimeout(()=>publishSlide(cur), 500);
</script>
</body>
</html>'''

out = (HTML
       .replace('__SLIDE_CSS__', SLIDE_CSS)
       .replace('__RENDER_JS__', RENDER_JS)
       .replace('__DATA__', DATA_JSON))
with open('present.html','w',encoding='utf-8') as f:
    f.write(out)
print(f"Wrote present.html ({len(out)} bytes), reused {len(SLIDE_CSS)} css + {len(RENDER_JS)} render js")
