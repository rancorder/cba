"""Generate a single self-contained index.html from slides_data.json.
Data-driven: adding a slide = adding one object to slides_data.json's 'slides' array."""
import json

with open('slides_data.json', encoding='utf-8') as f:
    DATA = json.load(f)

DATA_JSON = json.dumps(DATA, ensure_ascii=False)

HTML = r'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>CBA アーティスト・インストラクター育成講座</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#FBF6F1; --band:#F8D7CA; --accent:#E89B7E; --ink:#3A2D2A;
    --sub:#5C4A45; --gold:#B89968; --hair:rgba(184,153,104,.55);
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#241c1a;font-family:"Noto Serif JP",serif;color:var(--ink);-webkit-font-smoothing:antialiased}
  .en,.eyebrow,.num{font-family:"Cormorant Garamond",serif}

  /* ---------- stage ---------- */
  #stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#241c1a}
  .slide-frame{position:relative;width:100vw;height:56.25vw;max-height:100vh;max-width:177.78vh;background:var(--bg);overflow:hidden}
  .slide{position:absolute;inset:0;opacity:0;transition:opacity .55s ease;pointer-events:none;
         /* base canvas 1280x720, everything scales via container query units */}
  .slide.active{opacity:1;pointer-events:auto}

  /* scale text to frame: use cqw if available, fallback vw via JS-set --u */
  .slide-frame{container-type:size}
  .u{font-size:1cqw}

  /* ---------- shared atoms ---------- */
  .eyebrow{letter-spacing:.4em;color:var(--gold);text-transform:uppercase;text-align:center}
  .hair{height:1px;background:var(--gold);margin:0 auto}
  .band{position:absolute;top:0;left:0;right:0;background:var(--band);display:flex;align-items:center}
  em{font-style:normal;background:linear-gradient(transparent 62%,var(--band) 62%);padding:0 .12em}
  .accent{color:var(--accent)}

  /* ---------- layout per type (all sizes in cqw/cqh) ---------- */
  .pad{position:absolute;inset:0;padding:7cqh 9cqw}

  /* cover */
  .cv-logo{position:absolute;top:4cqh;left:3cqw;width:9cqw;height:9cqw;border-radius:50%;object-fit:cover;z-index:3}
  .cv-hero{position:absolute;top:4.5cqh;left:50%;transform:translateX(-50%);width:82cqw;height:52cqh;object-fit:cover}
  .cv-badge{position:absolute;top:7cqh;left:50%;transform:translateX(-50%);z-index:3;background:rgba(251,246,241,.55);
            padding:.5cqh 2cqw;font-size:2cqw;letter-spacing:.15em}
  .cv-tb{position:absolute;bottom:9cqh;left:0;right:0;text-align:center}
  .cv-lead{font-size:1.9cqw;letter-spacing:.22em;color:var(--sub);margin-bottom:1.6cqh}
  .cv-title{font-size:3cqw;letter-spacing:.16em;color:var(--ink)}
  .cv-sub{margin-top:2.2cqh;font-size:1.15cqw;letter-spacing:.18em;color:var(--sub)}
  .cv-sub .en{font-style:italic;margin-left:1.4cqw;letter-spacing:.06em}
  .cv-sep{color:var(--gold);margin:0 .2cqw}

  /* statement */
  .st{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center}
  .st .eyebrow{font-size:1.25cqw;margin-bottom:4.5cqh}
  .st .hair{width:5cqw;margin-bottom:4.5cqh}
  .st h1{font-weight:400;font-size:3.2cqw;letter-spacing:.16em;line-height:2}
  .st .foot-mark{position:absolute;bottom:4cqh;right:5cqw;font-size:.85cqw;letter-spacing:.25em;color:var(--gold);font-style:italic}

  /* agenda / reflect / cards / closing share heading */
  .head-band{height:13cqh;padding-left:6cqw;background:var(--band)}
  .head-band h2{font-weight:400;font-size:2.5cqw;letter-spacing:.2em;align-self:center}
  .center-eyebrow{font-size:1.15cqw;margin-bottom:2.2cqh}
  .center-title{text-align:center;font-weight:400;font-size:2.8cqw;letter-spacing:.16em;line-height:1.55}

  .lst{position:absolute;top:34cqh;left:14cqw;right:14cqw}
  .lst .row{display:flex;align-items:flex-start;margin-bottom:3.4cqh}
  .lst .n{flex:0 0 5cqw;font-style:italic;font-size:2.2cqw;color:var(--accent)}
  .lst .t{flex:1;font-size:1.65cqw;letter-spacing:.1em;line-height:1.9}
  .foot{position:absolute;bottom:7cqh;left:0;right:0;text-align:center;font-size:1.35cqw;letter-spacing:.16em;color:var(--sub)}

  /* curator / diagnostic */
  .blk{position:absolute;top:36cqh;left:14cqw;right:14cqw}
  .blk .row{display:flex;align-items:flex-start;margin-bottom:3cqh}
  .blk .n{flex:0 0 5cqw;font-style:italic;font-size:2cqw;color:var(--accent);padding-top:.4cqh}
  .blk .t{flex:1;font-size:1.5cqw;letter-spacing:.1em;line-height:1.85}
  .sign{position:absolute;bottom:4.5cqh;right:6cqw;font-size:1.05cqw;letter-spacing:.18em;color:var(--sub)}
  .lead-c{text-align:center;font-size:1.4cqw;letter-spacing:.2em;color:var(--sub);margin-top:2cqh}
  .close-c{position:absolute;bottom:7cqh;left:0;right:0;text-align:center;font-size:1.45cqw;letter-spacing:.16em;color:var(--sub);line-height:1.9}

  /* testimonial */
  .tm-meta{position:absolute;top:20cqh;left:9cqw;font-size:1.35cqw;letter-spacing:.16em;color:var(--sub)}
  .tm-hl{position:absolute;top:27cqh;left:9cqw;right:9cqw;text-align:center;color:var(--accent);font-size:2.5cqw;letter-spacing:.14em;padding:2cqh 0}
  .tm-hl .hair{width:5cqw;background:var(--accent)}
  .tm-q{position:absolute;top:44cqh;left:16cqw;right:16cqw;font-size:1.4cqw;letter-spacing:.08em;line-height:2.1;text-align:justify}
  .tm-q p{margin-bottom:1.6cqh}
  .tm-q p:first-child:before{content:"「";color:var(--gold)}
  .tm-q p:last-child:after{content:"」";color:var(--gold)}

  /* service */
  .sv{position:absolute;top:28cqh;left:11cqw;right:11cqw}
  .sv .row{display:flex;align-items:flex-start;margin-bottom:2.8cqh;padding-bottom:2.8cqh;border-bottom:1px solid var(--hair)}
  .sv .row:last-child{border-bottom:none}
  .sv .n{flex:0 0 4cqw;font-style:italic;font-size:1.8cqw;color:var(--accent)}
  .sv .c{flex:1}
  .sv .ti{font-size:1.7cqw;letter-spacing:.12em;margin-bottom:.6cqh}
  .sv .de{font-size:1.2cqw;letter-spacing:.06em;color:var(--sub);line-height:1.6}

  /* cards */
  .cards{position:absolute;top:32cqh;left:9cqw;right:9cqw;display:flex;gap:3cqw;justify-content:center}
  .card{flex:1;border:1px solid var(--hair);padding:5cqh 2.5cqw;text-align:center;font-size:1.5cqw;
        letter-spacing:.1em;line-height:1.7;display:flex;align-items:center;justify-content:center;min-height:24cqh}

  /* price */
  .pr{position:absolute;top:30cqh;left:14cqw;right:14cqw;display:flex;gap:4cqw}
  .pr .plan{flex:1;border:1px solid var(--hair);padding:5cqh 2cqw;text-align:center}
  .pr .pn{font-size:1.5cqw;letter-spacing:.16em;color:var(--sub);margin-bottom:2cqh}
  .pr .pp{font-size:3.4cqw;letter-spacing:.05em;color:var(--accent);margin-bottom:1.5cqh}
  .pr .pd{font-size:1.1cqw;letter-spacing:.08em;color:var(--sub)}
  .pr-note{position:absolute;bottom:11cqh;left:0;right:0;text-align:center;font-size:1.2cqw;letter-spacing:.12em;color:var(--sub)}

  /* special */
  .sp{position:absolute;top:30cqh;left:11cqw;right:11cqw;display:flex;gap:3cqw}
  .sp .opt{flex:1;background:rgba(248,215,202,.35);padding:4.5cqh 2.5cqw;text-align:center}
  .sp .ol{font-style:italic;font-size:1.6cqw;color:var(--accent);letter-spacing:.1em;margin-bottom:2cqh}
  .sp .ot{font-size:1.5cqw;letter-spacing:.08em;line-height:1.6;margin-bottom:1.5cqh}
  .sp .od{font-size:1.1cqw;color:var(--sub);letter-spacing:.06em;line-height:1.5}

  /* contract */
  .ct{position:absolute;top:26cqh;left:10cqw;right:10cqw}
  .ct .row{display:flex;align-items:flex-start;margin-bottom:2.4cqh}
  .ct .k{flex:0 0 22cqw;font-size:1.45cqw;letter-spacing:.1em}
  .ct .v{flex:1;font-size:1.2cqw;letter-spacing:.05em;color:var(--sub);line-height:1.65}
  .ct .row.warn .k,.ct .row.warn .v{color:var(--accent)}

  /* revenue */
  .rev{position:absolute;top:24cqh;left:10cqw;right:10cqw}
  .rev .rrow{display:flex;align-items:center;padding:1.7cqh 0;border-bottom:1px solid var(--hair)}
  .rev .rrow:last-child{border-bottom:none}
  .rev .rk{flex:0 0 32cqw;font-size:1.4cqw;letter-spacing:.08em}
  .rev .rm{flex:1;font-size:1.15cqw;color:var(--sub);letter-spacing:.04em}
  .rev .rv{flex:0 0 20cqw;text-align:right;font-size:1.6cqw;color:var(--accent);letter-spacing:.04em}

  /* closing */
  .cl{position:absolute;top:34cqh;left:18cqw;right:18cqw}
  .cl .row{display:flex;align-items:flex-start;margin-bottom:2.8cqh}
  .cl .n{flex:0 0 4cqw;font-style:italic;font-size:1.8cqw;color:var(--accent)}
  .cl .t{flex:1;font-size:1.55cqw;letter-spacing:.1em;line-height:1.7}

  /* ---------- chrome ---------- */
  #ui{position:fixed;left:0;right:0;bottom:0;height:46px;display:flex;align-items:center;justify-content:center;
      gap:18px;background:rgba(36,28,26,.0);z-index:50;opacity:0;transition:opacity .3s}
  body:hover #ui,#ui:hover{opacity:1}
  #ui button{background:rgba(251,246,241,.12);color:#FBF6F1;border:1px solid rgba(251,246,241,.25);
             border-radius:20px;padding:5px 14px;font-size:12px;letter-spacing:.08em;cursor:pointer;font-family:"Cormorant Garamond",serif}
  #ui button:hover{background:rgba(251,246,241,.22)}
  #prog{position:fixed;top:0;left:0;height:3px;background:var(--accent);z-index:60;transition:width .4s}
  #counter{position:fixed;top:10px;right:16px;color:rgba(251,246,241,.5);font-family:"Cormorant Garamond",serif;
           font-size:14px;letter-spacing:.15em;z-index:60}
  #dots{position:fixed;top:10px;left:16px;z-index:60;font-family:"Cormorant Garamond",serif;font-size:11px;
        letter-spacing:.2em;color:rgba(251,246,241,.5);text-transform:uppercase}

  /* ---------- presenter notes ---------- */
  #notes{position:fixed;inset:0;background:#1a1411;color:#e8ddd5;z-index:200;display:none;overflow-y:auto;
         font-family:"Noto Serif JP",serif}
  #notes.show{display:block}
  .nt-wrap{max-width:1100px;margin:0 auto;padding:40px 32px 80px}
  .nt-head{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid rgba(232,221,213,.2);
           padding-bottom:16px;margin-bottom:30px}
  .nt-head h1{font-size:20px;font-weight:500;letter-spacing:.1em}
  .nt-head .x{cursor:pointer;color:var(--accent);font-size:14px;letter-spacing:.1em}
  .nt-card{border:1px solid rgba(232,221,213,.16);border-radius:8px;padding:22px 26px;margin-bottom:18px;background:rgba(255,255,255,.02)}
  .nt-card .meta{display:flex;align-items:center;gap:12px;margin-bottom:14px}
  .nt-card .idx{font-family:"Cormorant Garamond",serif;font-size:22px;color:var(--accent);font-style:italic}
  .nt-card .sec{font-size:11px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase}
  .nt-card .badge{font-size:10px;letter-spacing:.15em;background:var(--accent);color:#1a1411;padding:2px 8px;border-radius:10px}
  .nt-card .stitle{font-size:15px;color:#fff;margin-bottom:14px;letter-spacing:.06em;opacity:.85}
  .nt-card .lbl{font-size:10px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase;margin:14px 0 6px}
  .nt-card .talk{font-size:15px;line-height:1.9;letter-spacing:.03em;color:#f0e8e1}
  .nt-card .cue{font-size:13px;line-height:1.75;letter-spacing:.03em;color:#c9b8ad;border-left:2px solid var(--accent);padding-left:14px;margin-top:6px}
  .nt-bar{position:fixed;top:0;left:0;right:0;height:48px;background:#0f0b09;display:flex;align-items:center;
          justify-content:space-between;padding:0 20px;z-index:210}
  .nt-bar .t{font-family:"Cormorant Garamond",serif;letter-spacing:.2em;font-size:14px;color:#e8ddd5}
  .nt-bar .toggle{font-size:12px;color:var(--accent);cursor:pointer;letter-spacing:.1em;border:1px solid rgba(232,221,213,.25);
                  padding:5px 12px;border-radius:14px}
  #notes .nt-wrap{padding-top:70px}

  @media (max-width:768px){
    .slide-frame{height:auto;aspect-ratio:16/9}
  }
</style>
</head>
<body>
<div id="prog"></div>
<div id="dots"></div>
<div id="counter"></div>
<div id="stage"><div class="slide-frame" id="frame"></div></div>
<div id="ui">
  <button onclick="go(-1)">‹ 前へ</button>
  <button onclick="toggleNotes()">商談メモ</button>
  <button onclick="toggleFs()">全画面</button>
  <button onclick="go(1)">次へ ›</button>
</div>

<div id="notes">
  <div class="nt-bar">
    <span class="t">PRESENTER NOTES — 商談者専用（聴衆には表示されません）</span>
    <span class="toggle" onclick="toggleNotes()">✕ 閉じてプレゼンに戻る</span>
  </div>
  <div class="nt-wrap" id="nt-wrap"></div>
</div>

<script>
const DATA = __DATA__;
const S = DATA.slides, IMG = DATA.images;
let cur = 0;

/* ---------- renderers ---------- */
function esc(s){return s==null?'':s}
function roman(i){return ['i','ii','iii','iv','v','vi','vii','viii'][i]||(i+1)}

function render(s){
  const d = s.deck;
  switch(s.type){
    case 'cover': return `
      <img class="cv-logo" src="${IMG[d.logo]}">
      <img class="cv-hero" src="${IMG[d.hero]}">
      <div class="cv-badge">【20周年記念 特別プログラム】</div>
      <div class="cv-tb">
        <div class="cv-lead">${d.lead}</div>
        <div class="cv-title">${d.title}</div>
        <div class="cv-sub">${d.sub.replace(/◇/g,'<span class="cv-sep">◇</span>')}<span class="en">— ${d.en}</span></div>
      </div>`;
    case 'statement': return `
      <div class="st">
        ${d.eyebrow?`<div class="eyebrow">${d.eyebrow}</div><div class="hair"></div>`:''}
        <h1>${d.title}</h1>
        <div class="foot-mark">Crystal Singing Bowl Beauty Academy</div>
      </div>`;
    case 'agenda': return `
      <div style="position:absolute;top:11cqh;left:0;right:0;text-align:center">
        <div class="center-title">${d.title}</div>
      </div>
      <div class="lst">
        ${d.items.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
      </div>
      <div class="foot">${d.foot}</div>`;
    case 'curator': return `
      <div style="position:absolute;top:9cqh;left:0;right:0;text-align:center">
        <div class="eyebrow center-eyebrow">${d.eyebrow}</div><div class="hair" style="width:5cqw"></div>
      </div>
      <div style="position:absolute;top:16cqh;left:0;right:0"><div class="center-title">${d.title}</div></div>
      <div class="blk">
        ${d.reasons.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
      </div>
      <div class="sign">${d.sign}</div>`;
    case 'reflect': return `
      <div style="position:absolute;top:9cqh;left:0;right:0;text-align:center">
        <div class="eyebrow center-eyebrow">${d.eyebrow}</div><div class="hair" style="width:5cqw"></div>
      </div>
      <div style="position:absolute;top:16cqh;left:0;right:0"><div class="center-title">${d.title}</div></div>
      <div class="blk">
        ${d.lines.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
      </div>
      <div class="foot">${d.foot}</div>`;
    case 'testimonial': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="tm-meta">${d.meta}</div>
      <div class="tm-hl"><div class="hair"></div><div style="padding:1.4cqh 0">${d.headline}</div><div class="hair"></div></div>
      <div class="tm-q">${d.quote.map(p=>`<p>${p}</p>`).join('')}</div>`;
    case 'service': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="sv">
        ${d.items.map((it,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="c"><div class="ti">${it[0]}</div><div class="de">${it[1]}</div></div></div>`).join('')}
      </div>
      <div class="foot" style="bottom:4cqh">${d.foot}</div>`;
    case 'cards': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="cards">${d.cards.map(c=>`<div class="card">${c}</div>`).join('')}</div>
      <div class="foot">${d.foot}</div>`;
    case 'diagnostic': return `
      <div style="position:absolute;top:8cqh;left:0;right:0;text-align:center">
        <div class="eyebrow center-eyebrow">${d.eyebrow}</div><div class="hair" style="width:5cqw"></div>
      </div>
      <div style="position:absolute;top:15cqh;left:0;right:0">
        <div class="center-title">${d.title}</div><div class="lead-c">${d.lead}</div>
      </div>
      <div class="blk" style="top:34cqh">
        ${d.questions.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
      </div>
      <div class="close-c">${d.close}</div>`;
    case 'revenue': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="rev">
        ${d.rows.map(r=>`<div class="rrow"><div class="rk">${r[0]}</div><div class="rm">${r[1]}</div><div class="rv">${r[2]}</div></div>`).join('')}
      </div>
      <div class="foot" style="bottom:4cqh">${d.foot}</div>`;
    case 'price': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="pr">
        ${d.plans.map(p=>`<div class="plan"><div class="pn">${p[0]}</div><div class="pp">${p[1]}</div><div class="pd">${p[2]}</div></div>`).join('')}
      </div>
      <div class="pr-note">${d.note}</div>
      <div class="foot" style="bottom:6cqh">${d.foot}</div>`;
    case 'special': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div style="position:absolute;top:22cqh;left:0;right:0;text-align:center;font-size:1.3cqw;letter-spacing:.16em;color:var(--sub)">${d.lead}</div>
      <div class="sp">
        ${d.options.map(o=>`<div class="opt"><div class="ol">${o[0]}</div><div class="ot">${o[1]}</div><div class="od">${o[2]}</div></div>`).join('')}
      </div>`;
    case 'contract': return `
      <div class="band head-band"><h2>${d.title}</h2></div>
      <div class="ct">
        ${d.points.map(p=>{const w=p[0].includes('返金')?' warn':'';return `<div class="row${w}"><div class="k">${p[0]}</div><div class="v">${p[1]}</div></div>`}).join('')}
      </div>`;
    case 'closing': return `
      <div style="position:absolute;top:11cqh;left:0;right:0;text-align:center">
        <div class="eyebrow center-eyebrow">${d.eyebrow}</div><div class="hair" style="width:5cqw"></div>
      </div>
      <div style="position:absolute;top:18cqh;left:0;right:0"><div class="center-title">${d.title}</div></div>
      <div class="cl">
        ${d.steps.map((t,i)=>`<div class="row"><div class="n">${roman(i)}.</div><div class="t">${t}</div></div>`).join('')}
      </div>
      <div class="foot">${d.foot}</div>`;
    default: return `<div class="st"><h1>${s.id}</h1></div>`;
  }
}

/* ---------- build slides ---------- */
const frame = document.getElementById('frame');
S.forEach((s,i)=>{
  const el = document.createElement('div');
  el.className = 'slide';
  el.dataset.i = i;
  el.innerHTML = render(s);
  frame.appendChild(el);
});
const slideEls = [...frame.querySelectorAll('.slide')];

/* dots / sections */
function show(i){
  cur = Math.max(0, Math.min(S.length-1, i));
  slideEls.forEach((el,k)=>el.classList.toggle('active',k===cur));
  document.getElementById('prog').style.width = ((cur+1)/S.length*100)+'%';
  document.getElementById('counter').textContent = String(cur+1).padStart(2,'0')+' / '+String(S.length).padStart(2,'0');
  document.getElementById('dots').textContent = S[cur].section || '';
  location.hash = cur+1;
}
function go(d){show(cur+d)}

/* keyboard / swipe */
addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){go(1);e.preventDefault()}
  if(e.key==='ArrowLeft'||e.key==='PageUp'){go(-1)}
  if(e.key==='Home')show(0);
  if(e.key==='End')show(S.length-1);
  if(e.key.toLowerCase()==='n')toggleNotes();
  if(e.key.toLowerCase()==='f')toggleFs();
});
let tx=0;
addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});
addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)go(dx<0?1:-1)},{passive:true});
frame.addEventListener('click',e=>{const r=frame.getBoundingClientRect();(e.clientX-r.left)/r.width>.5?go(1):go(-1)});

function toggleFs(){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}

/* ---------- presenter notes ---------- */
function buildNotes(){
  const w = document.getElementById('nt-wrap');
  w.innerHTML = S.map((s,i)=>{
    const n=s.notes||{};
    const badge = s.badge?`<span class="badge">${s.badge}</span>`:'';
    const title = (s.deck.title||s.deck.headline||(s.deck.title)||s.id);
    return `<div class="nt-card" id="nt-${i}">
      <div class="meta"><span class="idx">${String(i+1).padStart(2,'0')}</span><span class="sec">${s.section||''}</span>${badge}</div>
      <div class="stitle">${(s.deck.title||s.deck.headline||(s.deck.title)||s.id).replace(/<[^>]+>/g,'')}</div>
      ${n.talk?`<div class="lbl">話す内容</div><div class="talk">${n.talk}</div>`:''}
      ${n.cue?`<div class="lbl">進行のポイント</div><div class="cue">${n.cue}</div>`:''}
    </div>`;
  }).join('');
}
function toggleNotes(){
  const n=document.getElementById('notes');
  n.classList.toggle('show');
  if(n.classList.contains('show')){
    const c=document.getElementById('nt-'+cur);
    if(c)c.scrollIntoView({block:'center'});
  }
}

buildNotes();
const start = parseInt(location.hash.replace('#',''))||1;
show(start-1);
</script>
</body>
</html>'''

out = HTML.replace('__DATA__', DATA_JSON)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(out)
print(f"Wrote index.html ({len(out)} bytes)")
