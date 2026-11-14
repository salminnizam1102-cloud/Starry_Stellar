"""
GHOSTS OF SPACE - real 3D (Three.js) home page
Abandoned, but not forgotten

Run:  python homepage.py      -> opens http://localhost:8000
Pages: /  (Home)   /about  (The Story Behind Space)   /universe
Needs only Python standard library. Internet is needed for the
Three.js + Google Fonts CDN files (cdnjs.cloudflare.com).
"""
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000

HOME = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ghosts of Space</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#e8f1ff;--mut:#9fb4d6;--blue:#6eaaff;--cy:#7ff0ff;--bg:#000208}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:'Inter','Segoe UI',Arial,sans-serif;line-height:1.7}
#gl{position:fixed;inset:0;width:100%;height:100%;z-index:0}
.vig{position:fixed;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at 50% 45%,transparent 35%,rgba(0,0,0,.65) 100%)}
nav{position:fixed;top:0;left:0;right:0;z-index:10;display:flex;justify-content:space-between;align-items:center;padding:16px 4vw;
 background:linear-gradient(#000208cc,transparent)}
nav b{font-family:Orbitron;letter-spacing:.2em;font-size:14px}
nav div a{color:var(--mut);text-decoration:none;margin-left:22px;font-size:13px;letter-spacing:.08em}
nav div a:hover{color:#fff}
section{position:relative;z-index:2;min-height:100vh;padding:14vh 6vw;display:flex;flex-direction:column;justify-content:center}
.hero{align-items:center;text-align:center;padding-bottom:22vh}
.badge{font-family:Orbitron;font-size:clamp(9px,2vw,12px);letter-spacing:.5em;color:var(--blue);margin-bottom:18px}
h1{line-height:.95;font-family:Orbitron}
.g{display:block;font-weight:900;font-size:clamp(54px,16vw,220px);letter-spacing:.05em;color:#f4f8ff;
 text-shadow:0 0 28px rgba(110,170,255,.7),0 0 100px rgba(70,120,255,.45);animation:flick 7s 3s infinite}
.o{display:block;font-weight:900;font-size:clamp(24px,8vw,110px);letter-spacing:.38em;padding-left:.38em;color:transparent;
 -webkit-text-stroke:1.5px rgba(190,220,255,.95)}
.tag{margin-top:22px;font-family:Orbitron;font-size:clamp(11px,2.6vw,18px);letter-spacing:.3em;color:#b9cdea}
.tag b{color:#fff}
.portal{position:relative;display:inline-block;margin-top:44px;padding:2px;border-radius:70px;overflow:hidden;text-decoration:none;cursor:pointer}
.ring{position:absolute;left:-150%;top:-150%;width:400%;height:400%;background:conic-gradient(from 0deg,transparent 0 62%,#3fa0ff 80%,#fff 100%);animation:spin 2.6s linear infinite}
.inner{position:relative;display:block;border-radius:70px;padding:17px 40px 15px;background:rgba(2,8,24,.92)}
.portal:hover .inner{background:rgba(10,30,70,.9)}
.t{display:block;font-family:Orbitron;font-weight:900;font-size:15px;letter-spacing:.3em;color:#fff}
.s{display:block;margin-top:6px;font-family:Orbitron;font-size:8px;letter-spacing:.35em;color:var(--blue)}
.scroll{position:absolute;bottom:22px;left:0;right:0;text-align:center;font-size:10px;letter-spacing:.35em;color:#5d7599}
h2{font-family:Orbitron;font-size:clamp(26px,4.5vw,46px);letter-spacing:.08em;margin-bottom:18px}
p{color:var(--mut);max-width:62ch}
.glass{background:rgba(6,16,40,.55);border:1px solid rgba(120,170,255,.22);border-radius:18px;padding:34px;backdrop-filter:blur(10px)}
.left{max-width:640px}.right{margin-left:auto;max-width:640px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin-top:28px}
.card{background:rgba(6,16,40,.6);border:1px solid rgba(120,170,255,.22);border-radius:14px;padding:22px;backdrop-filter:blur(8px);transition:.3s}
.card:hover{transform:translateY(-6px);border-color:var(--cy)}
.card h3{font-family:Orbitron;font-size:15px;letter-spacing:.1em;margin-bottom:4px}
.card small{color:var(--cy);font-size:12px;display:block;margin-bottom:10px}
.card p{font-size:14px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px;text-align:center;margin-top:30px}
.stats b{display:block;font-family:Orbitron;font-size:clamp(30px,5vw,52px);color:#fff;text-shadow:0 0 20px rgba(110,170,255,.7)}
.stats span{font-size:13px;color:var(--mut)}
.tl{border-left:2px solid rgba(120,170,255,.4);margin-top:24px;padding-left:24px}
.tl div{margin-bottom:20px}.tl b{font-family:Orbitron;color:var(--cy);font-size:14px}
footer{position:relative;z-index:2;padding:50px 6vw 30px;background:#000208ee;border-top:1px solid rgba(120,170,255,.2)}
.fg{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:30px}
footer h4{font-family:Orbitron;font-size:13px;letter-spacing:.15em;margin-bottom:10px}
footer a{display:block;color:var(--mut);text-decoration:none;font-size:14px;margin:5px 0}
footer a:hover{color:#fff}.copy{margin-top:34px;font-size:12px;color:#5d7599;text-align:center}
#flash{position:fixed;inset:0;background:#cde4ff;opacity:0;z-index:50;pointer-events:none}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes flick{0%,90%,100%{opacity:1}91%{opacity:.5}92%{opacity:1}94%{opacity:.35}95%{opacity:1}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
nav a.on{color:#fff;border-bottom:2px solid var(--cy);padding-bottom:3px}.team .card{text-align:center}.av{width:64px;height:64px;border-radius:50%;margin:0 auto 12px;background:radial-gradient(circle at 35% 30%,#7fb2ff,#14306b);border:1px solid var(--cy)}.more{display:inline-block;margin-top:18px;color:var(--cy);text-decoration:none;border:1px solid var(--cy);padding:9px 22px;border-radius:30px;font-size:13px}.more:hover{background:rgba(127,240,255,.15)}@media(max-width:700px){nav{flex-direction:column;gap:8px;padding:10px 3vw}nav div{display:flex;flex-wrap:wrap;justify-content:center}nav div a{margin:0 9px;font-size:12px}.right{margin-left:0}section{padding:18vh 5vw 10vh}}
</style>
</head>
<body>
<canvas id="gl"></canvas><div class="vig"></div><div id="flash"></div>
<nav><b>GHOSTS OF SPACE</b><div><a href="/" class="NAVHOME">Home</a><a href="/about" class="NAVABOUT">About</a><a href="/#ghosts">The Ghosts</a><a href="/#numbers">Numbers</a><a href="/#mission">Mission</a><a href="/universe">Explore</a></div></nav>

<section class="hero" id="top">
  <div class="badge">THE GRAVEYARD OF MACHINES</div>
  <h1><span class="g">GHOSTS</span><span class="o">OF SPACE</span></h1>
  <p class="tag">ABANDONED, BUT <b>NOT FORGOTTEN</b></p>
  <a class="portal" id="go" href="/universe"><span class="ring"></span><span class="inner">
    <span class="t">EXPLORE THE UNIVERSE</span><span class="s">ENTER THE GRAVEYARD OF MACHINES</span></span></a>
  <div class="scroll">SCROLL TO FLY &middot; MOVE MOUSE TO LOOK AROUND</div>
</section>

<section id="about"><div class="glass left">
  <h2>About Us</h2>
  <p>We are a team of students, coders and space enthusiasts with one idea: <i>abandoned, but not forgotten</i>. Humanity has sent thousands of machines beyond the sky. When their batteries fade and their radios go quiet, they do not vanish: they keep drifting, orbiting and sitting silently on other worlds.</p>
  <p style="margin-top:12px">Ghosts of Space tells their stories with open NASA and ESA knowledge, turning dead satellites, silent rovers and forgotten landers into something you can see, rotate and remember.</p>
  <a class="more" href="/about">Read our full story</a>
</div></section>

<section id="ghosts"><h2>The Ghosts</h2>
  <p>Machines humanity left behind on other worlds.</p>
  <div class="grid">
    <div class="card"><h3>The Moon</h3><small>Discarded equipment</small><p>Apollo lunar module descent stages, lunar rovers, science instruments and landers still rest where they were left, undisturbed for decades.</p></div>
    <div class="card"><h3>Mars</h3><small>Discarded equipment</small><p>Silent rovers and landers such as Spirit, Opportunity and the Viking probes sit on the red dust, slowly covered by Martian sand.</p></div>
  </div>
</section>

<section id="numbers"><div class="glass right">
  <h2>By the Numbers</h2>
  <p>Space around Earth is getting crowded. Approximate figures from space agencies:</p>
  <div class="stats">
    <div><b data-n="40000">0</b><span>objects tracked in orbit</span></div>
    <div><b data-n="1200000">0</b><span>fragments larger than 1 cm</span></div>
    <div><b data-n="28000">0</b><span>km/h typical debris speed</span></div>
  </div>
</div></section>

<section id="mission"><h2>Our Mission</h2>
  <p>To make space heritage and space debris visible to everyone, so that forgotten machines are honoured and future missions are built to leave nothing harmful behind.</p>
  <div class="tl">
    <div><b>1957</b><p>Sputnik opens the space age.</p></div>
    <div><b>1958</b><p>Vanguard 1 begins its endless orbit.</p></div>
    <div><b>2004</b><p>Opportunity lands on Mars.</p></div>
    <div><b>Today</b><p>Thousands of dead satellites circle above us.</p></div>
    <div><b>Tomorrow</b><p>Clean orbits, active debris removal and responsible design.</p></div>
  </div>
</section>

<footer>
  <div class="fg">
    <div><h4>GHOSTS OF SPACE</h4><p style="font-size:14px">Abandoned, but not forgotten.</p></div>
    <div><h4>EXPLORE</h4><a href="/">Home</a><a href="/about">The Story</a><a href="/#ghosts">The Ghosts</a><a href="/#numbers">Numbers</a><a href="/universe">The Universe</a></div>
    <div><h4>DATA SOURCES</h4><a href="https://www.nasa.gov" target="_blank" rel="noopener">NASA</a><a href="https://www.esa.int" target="_blank" rel="noopener">ESA</a></div>
    <div><h4>CONTACT</h4><a href="mailto:team@ghostsofspace.example">team@ghostsofspace.example</a></div>
  </div>
  <div class="copy">&copy; 2026 Ghosts of Space</div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>window.THREE||document.write('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"><\/script>')</script>
<script>
(function(){
function say(m){var e=document.createElement('div');e.style.cssText='position:fixed;inset:0;z-index:60;display:flex;align-items:center;justify-content:center;background:#000208;color:#ff9a9a;font:14px Arial;text-align:center;line-height:1.6;padding:20px';e.innerHTML=m;document.body.appendChild(e)}
if(typeof THREE==='undefined'){say('Could not load the 3D engine (Three.js).<br>Check your internet connection, then press Ctrl+F5.');return}
window.addEventListener('error',function(e){say('Script error: '+e.message+'<br>Please send this message.')});
var cv=document.getElementById('gl');
var R=new THREE.WebGLRenderer({canvas:cv,antialias:true});
R.setPixelRatio(Math.min(devicePixelRatio,2));
R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.15;
var S=new THREE.Scene(),C=new THREE.PerspectiveCamera(50,1,.1,3000);C.position.set(0,0,12);
var SUN=new THREE.Vector3(-.8,.35,.5).normalize();

/* ---------- procedural noise ---------- */
function hs(x,y,z){var s=Math.sin(x*127.1+y*311.7+z*74.7)*43758.5453;return s-Math.floor(s)}
function lp(a,b,t){return a+(b-a)*t}
function vn(x,y,z){var xi=Math.floor(x),yi=Math.floor(y),zi=Math.floor(z),xf=x-xi,yf=y-yi,zf=z-zi;
  xf=xf*xf*(3-2*xf);yf=yf*yf*(3-2*yf);zf=zf*zf*(3-2*zf);
  return lp(lp(lp(hs(xi,yi,zi),hs(xi+1,yi,zi),xf),lp(hs(xi,yi+1,zi),hs(xi+1,yi+1,zi),xf),yf),
            lp(lp(hs(xi,yi,zi+1),hs(xi+1,yi,zi+1),xf),lp(hs(xi,yi+1,zi+1),hs(xi+1,yi+1,zi+1),xf),yf),zf)}
function fbm(x,y,z,o){var v=0,a=.5;for(var i=0;i<o;i++){v+=a*vn(x,y,z);x*=2.03;y*=2.03;z*=2.03;a*=.5}return v}
function mk(w,h){var c=document.createElement('canvas');c.width=w;c.height=h;var g=c.getContext('2d');return{c:c,g:g,d:g.createImageData(w,h)}}
function fin(o){o.g.putImageData(o.d,0,0);var t=new THREE.CanvasTexture(o.c);t.anisotropy=8;return t}
function put(o,k,r,g,b){o.d.data[k]=r;o.d.data[k+1]=g;o.d.data[k+2]=b;o.d.data[k+3]=255}

/* ---------- Earth: day, night lights, ocean-specular, clouds ---------- */
function tx(o){var t=new THREE.CanvasTexture(o.c);t.anisotropy=8;return t}
function fillC(o,c){o.g.fillStyle=c;o.g.fillRect(0,0,o.c.width,o.c.height)}
var jobs=[],total=0,doneRows=0;
function job(h,fn,done){jobs.push({y:0,h:h,fn:fn,done:done});total+=h}
function runJobs(){var t0=performance.now();while(jobs.length&&performance.now()-t0<9){var j=jobs[0];j.fn(j.y);j.y++;doneRows++;if(j.y>=j.h){j.done();jobs.shift()}}}
var EW=640,EH=320,ED=mk(EW,EH),EN=mk(EW,EH),EP=mk(EW,EH),CD=mk(512,256);
fillC(ED,'#0b2a5c');fillC(EN,'#000');fillC(EP,'#fff');fillC(CD,'#000');
var ET={d:tx(ED),n:tx(EN),s:tx(EP)},CT=tx(CD);
job(EH,function(j){var la=(.5-j/EH)*Math.PI,cl=Math.cos(la),y=Math.sin(la),ay=Math.abs(y);
  for(var i=0;i<EW;i++){var lo=i/EW*6.2832,x=cl*Math.cos(lo),z=cl*Math.sin(lo),k=(j*EW+i)*4;
    var e=fbm(x*2.2+9,y*2.2,z*2.2,6),m=fbm(x*3+40,y*3,z*3,4),r,g,b,nl=0,sp=0;
    if(e<.5){var dp=Math.min(1,(.5-e)*5);r=22-dp*18;g=100-dp*80;b=145-dp*90;sp=255;if(ay>.9){r=g=b=230;sp=40}}
    else{var hh=(e-.5)*3.2,t=1-ay*1.15-hh*.35;
      if(t<.12||ay>.88){r=g=b=238}
      else if(hh>.55){r=g=b=105+hh*50}
      else if(m<.47&&t>.35){r=185-hh*40;g=150-hh*30;b=95}
      else{r=28+m*50;g=88+m*40-hh*30;b=38+m*10}
      if(t>.15&&vn(x*14,y*14,z*14)>.7&&fbm(x*40,y*40,z*40,2)>.45)nl=1}
    put(ED,k,r,g,b);put(EN,k,nl*255,nl*190,nl*110);put(EP,k,sp,sp,sp)}},
  function(){[ED,EN,EP].forEach(function(o){o.g.putImageData(o.d,0,0)});ET.d.needsUpdate=ET.n.needsUpdate=ET.s.needsUpdate=true});
job(256,function(j){var la=(.5-j/256)*Math.PI,cl=Math.cos(la),y=Math.sin(la);
  for(var i=0;i<512;i++){var lo=i/512*6.2832,q=fbm(cl*Math.cos(lo)*2.8+3,y*2.8,cl*Math.sin(lo)*2.8,5),v=Math.max(0,Math.min(1,(q-.47)*4))*255;put(CD,(j*512+i)*4,v,v,v)}},
  function(){CD.g.putImageData(CD.d,0,0);CT.needsUpdate=true});
var U={d:{value:ET.d},nt:{value:ET.n},sp:{value:ET.s},c:{value:CT},sun:{value:SUN},rot:{value:0}};
var earthMat=new THREE.ShaderMaterial({uniforms:U,
  vertexShader:'varying vec2 vUv;varying vec3 vN,vP;void main(){vUv=uv;vN=normalize(mat3(modelMatrix)*normal);vP=(modelMatrix*vec4(position,1.)).xyz;gl_Position=projectionMatrix*viewMatrix*vec4(vP,1.);}',
  fragmentShader:'uniform sampler2D d,nt,sp,c;uniform vec3 sun;uniform float rot;varying vec2 vUv;varying vec3 vN,vP;'+
  'void main(){vec2 u=vec2(vUv.x+rot,vUv.y);vec3 N=normalize(vN),V=normalize(cameraPosition-vP),H=normalize(sun+V);'+
  'float l=dot(N,sun),day=smoothstep(-.1,.3,l);float cl=texture2D(c,vec2(vUv.x+rot*1.3,vUv.y)).r;'+
  'vec3 dc=texture2D(d,u).rgb;float s=pow(max(dot(N,H),0.),80.)*texture2D(sp,u).r*(1.-cl);'+
  'vec3 lit=dc*(max(l,0.)*1.25+.015)+vec3(1.,.95,.85)*s*.9;lit=mix(lit,vec3(max(l,0.)*1.15+.02),cl*.92);'+
  'vec3 nite=texture2D(nt,u).rgb*(1.-cl*.85)*1.6+dc*.012;vec3 col=mix(nite,lit,day);'+
  'float tw=smoothstep(-.05,.2,l)*(1.-smoothstep(.2,.45,l));col+=vec3(.55,.22,.06)*tw*.35;'+
  'float f=pow(1.-max(dot(N,V),0.),3.);col+=vec3(.25,.5,1.)*f*(.25+.9*day);gl_FragColor=vec4(col,1.);}'});
var atmMat=new THREE.ShaderMaterial({transparent:true,side:THREE.BackSide,blending:THREE.AdditiveBlending,depthWrite:false,uniforms:{sun:{value:SUN}},
  vertexShader:'varying vec3 n,w;void main(){n=normalize(normalMatrix*normal);w=normalize(mat3(modelMatrix)*normal);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
  fragmentShader:'uniform vec3 sun;varying vec3 n,w;void main(){float i=pow(max(.68-dot(n,vec3(0,0,1.)),0.),3.);float lit=.25+.9*smoothstep(-.3,.6,dot(w,sun));gl_FragColor=vec4(.28,.58,1.,1.)*i*2.2*lit;}'});

/* system group: Earth + Moon + ghosts + debris all move/scale together */
var sys=new THREE.Group();S.add(sys);
sys.add(new THREE.Mesh(new THREE.SphereGeometry(3,128,128),earthMat));
sys.add(new THREE.Mesh(new THREE.SphereGeometry(3.3,64,64),atmMat));

/* lights */
var sunL=new THREE.DirectionalLight(0xfff1dc,2.4);sunL.position.copy(SUN).multiplyScalar(50);S.add(sunL);
S.add(new THREE.HemisphereLight(0x3d66c0,0x000000,.28));

/* ---------- Moon with craters ---------- */
var MD=mk(512,256);fillC(MD,'#8a8a8a');var MT=tx(MD);
job(256,function(j){var la=(.5-j/256)*Math.PI,cl=Math.cos(la),y=Math.sin(la);
  for(var i=0;i<512;i++){var lo=i/512*6.2832,q=fbm(cl*Math.cos(lo)*3,y*3,cl*Math.sin(lo)*3,5),v=110+q*110;put(MD,(j*512+i)*4,v,v,v*1.02)}},
  function(){MD.g.putImageData(MD.d,0,0);
    for(var n=0;n<220;n++){var cx=Math.random()*512,cy=Math.random()*256,r=3+Math.pow(Math.random(),3)*34;
      var gr=MD.g.createRadialGradient(cx,cy,r*.1,cx,cy,r);gr.addColorStop(0,'rgba(0,0,0,.38)');gr.addColorStop(.8,'rgba(0,0,0,.14)');gr.addColorStop(.92,'rgba(255,255,255,.28)');gr.addColorStop(1,'rgba(255,255,255,0)');
      MD.g.fillStyle=gr;MD.g.beginPath();MD.g.arc(cx,cy,r,0,6.2832);MD.g.fill()}
    MT.needsUpdate=true});
var moon=new THREE.Mesh(new THREE.SphereGeometry(.82,64,64),new THREE.MeshStandardMaterial({map:MT,bumpMap:MT,bumpScale:2.5,roughness:1,metalness:0}));
sys.add(moon);
var mars=new THREE.Mesh(new THREE.SphereGeometry(1.2,48,48),new THREE.MeshStandardMaterial({color:0xb5603a,roughness:1}));
mars.position.set(-16,6,-40);S.add(mars);

/* ---------- stars + Milky Way band (twinkling shader points) ---------- */
var NS=9000,sp3=new Float32Array(NS*3),sc3=new Float32Array(NS*3),ssz=new Float32Array(NS),sph=new Float32Array(NS),i;
var bn=new THREE.Vector3(.3,1,.2).normalize(),bu=new THREE.Vector3().crossVectors(bn,new THREE.Vector3(0,0,1)).normalize(),bv=new THREE.Vector3().crossVectors(bn,bu);
for(i=0;i<NS;i++){var d=new THREE.Vector3();
  if(i<NS*.5){var a=Math.random()*6.2832,off=(Math.random()+Math.random()+Math.random()-1.5)*.38;
    d.set(0,0,0).addScaledVector(bu,Math.cos(a)).addScaledVector(bv,Math.sin(a)).addScaledVector(bn,off).normalize()}
  else{d.set(Math.random()-.5,Math.random()-.5,Math.random()-.5).normalize()}
  d.multiplyScalar(900);sp3[i*3]=d.x;sp3[i*3+1]=d.y;sp3[i*3+2]=d.z;
  var h=Math.random(),cc=h<.1?[1,.78,.55]:h<.3?[.65,.78,1]:[1,.97,.95];sc3.set(cc,i*3);
  ssz[i]=(Math.random()<.04?3.8:1.3+Math.random()*1.4)*(i<NS*.5?.8:1);sph[i]=Math.random()}
var sg=new THREE.BufferGeometry();sg.setAttribute('position',new THREE.BufferAttribute(sp3,3));sg.setAttribute('col',new THREE.BufferAttribute(sc3,3));
sg.setAttribute('sz',new THREE.BufferAttribute(ssz,1));sg.setAttribute('ph',new THREE.BufferAttribute(sph,1));
var SU={t:{value:0},pr:{value:Math.min(devicePixelRatio,2)}};
var stars=new THREE.Points(sg,new THREE.ShaderMaterial({uniforms:SU,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
  vertexShader:'attribute float sz,ph;attribute vec3 col;uniform float t,pr;varying vec3 c;varying float a;void main(){c=col;a=.65+.35*sin(t*(1.+ph*2.)+ph*60.);gl_PointSize=sz*pr*a;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
  fragmentShader:'varying vec3 c;varying float a;void main(){float d=length(gl_PointCoord-.5);if(d>.5)discard;float k=smoothstep(.5,0.,d);gl_FragColor=vec4(c*k*a,k*a);}'}));
S.add(stars);
function glow(c,s,x,y,z,o){var k=document.createElement('canvas');k.width=k.height=128;var g=k.getContext('2d'),r=g.createRadialGradient(64,64,0,64,64,64);
  r.addColorStop(0,'rgba('+c+',.6)');r.addColorStop(1,'rgba('+c+',0)');g.fillStyle=r;g.fillRect(0,0,128,128);
  var sp=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(k),blending:THREE.AdditiveBlending,depthWrite:false,transparent:true,opacity:o||.4}));
  sp.scale.set(s,s,1);sp.position.set(x,y,z);S.add(sp);return sp}
glow('90,50,190',500,-300,150,-600,.3);glow('30,100,200',560,350,-80,-650,.28);glow('190,70,140',380,80,-250,-600,.2);
glow('255,240,210',260,SUN.x*600,SUN.y*600,SUN.z*600,.9);

/* ---------- derelict machines: solid, metallic, tumbling ---------- */
var foil=new THREE.MeshStandardMaterial({color:0xc9a24a,metalness:.9,roughness:.35}),
    grey=new THREE.MeshStandardMaterial({color:0x8a8f98,metalness:.8,roughness:.45,side:THREE.DoubleSide}),
    white=new THREE.MeshStandardMaterial({color:0xd8dce2,metalness:.4,roughness:.6});
var pc=document.createElement('canvas');pc.width=128;pc.height=64;var pg=pc.getContext('2d');pg.fillStyle='#0d1f4a';pg.fillRect(0,0,128,64);pg.strokeStyle='#4a6aa8';
for(i=0;i<=128;i+=16){pg.beginPath();pg.moveTo(i,0);pg.lineTo(i,64);pg.stroke()}for(i=0;i<=64;i+=16){pg.beginPath();pg.moveTo(0,i);pg.lineTo(128,i);pg.stroke()}
var panel=new THREE.MeshStandardMaterial({map:new THREE.CanvasTexture(pc),metalness:.7,roughness:.25});
var leds=[];
function bx(w,h,d,m,x,y,z){var o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(x||0,y||0,z||0);return o}
function led(o,x,y,z){var l=new THREE.Mesh(new THREE.SphereGeometry(.04,8,8),new THREE.MeshBasicMaterial({color:0xff2a2a}));l.position.set(x,y,z);o.add(l);leds.push(l)}
function satA(){var o=new THREE.Group();o.add(bx(.6,.6,.6,foil));o.add(bx(1.8,.03,.8,panel,1.25,0,0));
  var b=bx(1.1,.03,.8,panel,-1,0,0);b.rotation.z=.35;b.rotation.y=.2;o.add(b);
  var a=new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,.9),grey);a.position.y=.7;o.add(a);
  var dsh=new THREE.Mesh(new THREE.SphereGeometry(.3,20,8,0,6.2832,0,1.1),grey);dsh.position.set(0,.4,.35);dsh.rotation.x=1.2;o.add(dsh);led(o,.3,.3,.31);return o}
function satB(){var o=new THREE.Group();o.add(bx(.7,.7,2.2,foil));o.add(bx(2.8,.03,.7,panel,1.8,0,-.6));
  o.add(bx(.12,.12,.9,grey,0,.5,1.1));var d=new THREE.Mesh(new THREE.CylinderGeometry(.4,.1,.12,20),white);d.position.set(0,.45,-1.2);o.add(d);led(o,0,.37,1.12);return o}
function stage(){var o=new THREE.Group();var c=new THREE.Mesh(new THREE.CylinderGeometry(.38,.38,2.6,24),white);o.add(c);
  var n=new THREE.Mesh(new THREE.CylinderGeometry(.3,.5,.6,24,1,true),grey);n.position.y=-1.5;o.add(n);
  var st=new THREE.Mesh(new THREE.CylinderGeometry(.385,.385,.3,24),new THREE.MeshStandardMaterial({color:0x222222,roughness:.7}));st.position.y=.5;o.add(st);return o}
function probe(){var o=new THREE.Group();o.add(bx(.5,.5,.8,foil));
  var d=new THREE.Mesh(new THREE.SphereGeometry(.8,28,8,0,6.2832,0,.85),grey);d.rotation.x=-Math.PI/2;d.position.z=.5;o.add(d);
  var bm=new THREE.Mesh(new THREE.CylinderGeometry(.015,.015,1.6),grey);bm.rotation.z=Math.PI/2;bm.position.set(.8,0,-.2);o.add(bm);led(o,0,.27,-.3);return o}
var ghosts=[];
[satA,satB,stage,probe,satA,stage].forEach(function(f,k){var g=f();g.scale.setScalar(.38+Math.random()*.2);sys.add(g);
  ghosts.push({m:g,a:k/6*6.2832,r:4.6+Math.random()*3,i:(Math.random()-.5)*1.4,v:.035+Math.random()*.05,
    rt:new THREE.Vector3((Math.random()-.5)*.35,(Math.random()-.5)*.35,(Math.random()-.5)*.35)})});

/* debris belt */
var DN=480,deb=new THREE.InstancedMesh(new THREE.DodecahedronGeometry(1,0),new THREE.MeshStandardMaterial({color:0x9a9ca2,roughness:.7,metalness:.6,flatShading:true}),DN),dd=[],dm=new THREE.Object3D();
for(i=0;i<DN;i++)dd.push({a:Math.random()*6.2832,r:4.4+Math.random()*4.2,i:(Math.random()-.5)*1.5,v:(.02+Math.random()*.05)*(Math.random()<.2?-1:1),s:.02+Math.random()*.045,rx:Math.random()*6,ry:Math.random()*6});
sys.add(deb);
function orbitPos(o,r,a,inc){o.position.set(Math.cos(a)*r,Math.sin(a)*r*Math.sin(inc),Math.sin(a)*r*Math.cos(inc))}

/* shooting stars */
var sh=[];for(i=0;i<3;i++){var l=new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(),new THREE.Vector3(-16,-5,0)]),new THREE.LineBasicMaterial({color:0xcfe6ff,transparent:true,opacity:0}));
  l.userData={life:0,wait:2+Math.random()*8};S.add(l);sh.push(l)}

/* ---------- interaction ---------- */
var mx=0,my=0,warp=false,wt=0,fl=document.getElementById('flash');
addEventListener('mousemove',function(e){mx=e.clientX/innerWidth-.5;my=e.clientY/innerHeight-.5});
addEventListener('touchmove',function(e){if(e.touches[0]){mx=e.touches[0].clientX/innerWidth-.5;my=e.touches[0].clientY/innerHeight-.5}},{passive:true});
function prog(){var m=document.documentElement.scrollHeight-innerHeight;return m>0?Math.min(1,scrollY/m):0}
var goB=document.getElementById('go');if(goB)goB.addEventListener('click',function(e){e.preventDefault();if(!warp){warp=true;wt=0}});
function size(){R.setSize(innerWidth,innerHeight,false);C.aspect=innerWidth/innerHeight;C.updateProjectionMatrix()}
addEventListener('resize',size);size();
var seen=false;
function count(){document.querySelectorAll('[data-n]').forEach(function(el){var t=+el.dataset.n,s=performance.now();
  (function up(n){var p=Math.min(1,(n-s)/1800);el.textContent=Math.floor(t*(1-Math.pow(1-p,3))).toLocaleString()+(p>=1?'+':'');if(p<1)requestAnimationFrame(up)})(s)})}
var nm=document.getElementById('numbers');if(nm)new IntersectionObserver(function(en){if(en[0].isIntersecting&&!seen){seen=true;count()}}).observe(nm);

/* ---------- loop ---------- */
var clock=new THREE.Clock(),ps=0;
function loop(){
  runJobs();
  var dt=Math.min(clock.getDelta(),.05),t=clock.elapsedTime,p=prog();ps+=(p-ps)*.05;SU.t.value=t;
  var q=Math.min(1,ps*3),ex=lp(0,5.2,q),ey=lp(-5.2,-.4,q),sc=lp(1.7,1,q);
  sys.position.set(ex,ey,0);sys.scale.setScalar(sc);U.rot.value+=dt*.004;
  orbitPos(moon,9.5,t*.04+1,.18);moon.rotation.y=t*.01;mars.rotation.y+=dt*.05;
  ghosts.forEach(function(o){o.a+=o.v*dt;orbitPos(o.m,o.r,o.a,o.i);o.m.rotation.x+=o.rt.x*dt;o.m.rotation.y+=o.rt.y*dt;o.m.rotation.z+=o.rt.z*dt});
  leds.forEach(function(l,k){l.material.color.setScalar(Math.sin(t*3+k*2)>.8?1:.12);l.material.color.r=1})
  for(var n=0;n<DN;n++){var d=dd[n];d.a+=d.v*dt;orbitPos(dm,d.r,d.a,d.i);dm.rotation.set(d.rx+t*.3,d.ry+t*.2,0);dm.scale.setScalar(d.s);dm.updateMatrix();deb.setMatrixAt(n,dm.matrix)}
  deb.instanceMatrix.needsUpdate=true;
  sh.forEach(function(l){var u=l.userData;if(u.wait>0){u.wait-=dt;l.material.opacity=0;if(u.wait<=0){u.life=.9;l.position.set(60+Math.random()*120,60+Math.random()*80,-250)}}
    else{u.life-=dt;l.position.x-=dt*190;l.position.y-=dt*55;l.material.opacity=Math.max(0,u.life/.9);if(u.life<=0)u.wait=4+Math.random()*10}});
  stars.rotation.y+=dt*.003;
  C.position.x+=(mx*2.4+Math.sin(t*.1)*.4-C.position.x)*.03;C.position.y+=(-my*1.5+Math.cos(t*.08)*.25-C.position.y)*.03;
  var cz=12-ps*3;
  if(warp){wt+=dt;var k=wt/1.6;cz=12-k*k*60;C.fov=50+k*k*70;C.updateProjectionMatrix();fl.style.opacity=k>.8?Math.min(1,(k-.8)/.2):0;if(k>=1)location.href='/universe'}
  C.position.z+=(cz-C.position.z)*.08;C.lookAt(ex*.35,ey*.4+1.2,0);
  R.render(S,C);requestAnimationFrame(loop)}
addEventListener('pageshow',function(){warp=false;C.fov=50;C.updateProjectionMatrix();fl.style.opacity=0});
loop();
})();
</script>
</body>
</html>
"""

PAGE_STYLE = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;color:#e8f1ff;min-height:100vh;
 background:radial-gradient(ellipse at 50% 120%,#1b4a9c 0%,#0a1e45 30%,transparent 60%),#000308}
.page{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px}
h2{font-size:clamp(26px,6vw,48px);letter-spacing:.1em;margin-bottom:12px}
.tagline{font-size:clamp(13px,3vw,18px);color:#9fb4d6;max-width:520px;margin-bottom:28px}
a{color:#fff;text-decoration:none;border:1px solid #6eaaff;padding:12px 28px;border-radius:40px}
a:hover{background:#1b4a9c}
"""


ABOUT_BODY = r"""
<section><div class="glass left">
  <h2>The Story Behind Space</h2>
  <p>We are <b>Starry Stellar</b>, a team with one idea: <i>abandoned, but not forgotten</i>. Since 1957 humanity has launched thousands of machines. When they stop working they are rarely brought home: they keep orbiting, drifting or resting on other worlds.</p>
  <p style="margin-top:12px">Ghosts of Space turns that hidden story into an experience you can explore in 3D, using open knowledge from NASA and ESA.</p>
</div></section>

<section><h2>What We Do</h2>
  <div class="grid">
    <div class="card"><h3>Remember</h3><small>Space heritage</small><p>We tell the stories of retired satellites, rovers and landers so their achievements are not lost.</p></div>
    <div class="card"><h3>Visualise</h3><small>Real-time 3D</small><p>Earth, Moon and orbiting debris are built live in your browser, nothing to install.</p></div>
    <div class="card"><h3>Raise awareness</h3><small>Orbital debris</small><p>Tens of thousands of tracked objects circle Earth. We show why clean orbits matter.</p></div>
    <div class="card"><h3>Inspire</h3><small>Next generation</small><p>We want students to see space as a place we must look after, not just visit.</p></div>
  </div>
</section>

<section class="team"><h2>Our Team</h2>
  <p>Six members, one mission.</p>
  <div class="grid">
    <div class="card"><div class="av"></div><h3>Salmin N</h3><small>Team Lead</small><p>Plans the project, coordinates the team and reviews the final site.</p></div>
    <div class="card"><div class="av"></div><h3>Niharika S</h3><small>3D Developer &amp; Content</small><p>make equipments rotate and move and 3D demonstrations Moon.</p></div>
    <div class="card"><div class="av"></div><h3>Malavika A</h3><small>Frontend Developer and animator</small><p>Builds the pages, layout and navigation and space effects.</p></div>
    <div class="card"><div class="av"></div><h3>Lekshmi Prasad</h3><small>Animator</small><p>Creates the animations, space effects and motion.</p></div>
    <div class="card"><div class="av"></div><h3>Jisha</h3><small>Design &amp; UI</small><p>Designs the colors, fonts and visual look of the site.</p></div>
    <div class="card"><div class="av"></div><h3>Sandra Sebu</h3><small>Testing &amp; Documentation</small><p>Tests every page, fixes issues and prepares the project report.</p></div>
  </div>
</section>

<section style="min-height:50vh"><div class="glass right">
  <h2>Keep Exploring</h2>
  <a class="more" href="/">Back to Home</a> <a class="more" href="/universe">Explore the Universe</a>
</div></section>
"""
_a = HOME.index('<section class="hero"')
_b = HOME.index('<footer>')
ABOUT = HOME[:_a] + ABOUT_BODY + HOME[_b:]
ABOUT = ABOUT.replace('<title>Ghosts of Space</title>', '<title>The Story Behind Space - Ghosts of Space</title>', 1)
HOME = HOME.replace('NAVHOME','on').replace('NAVABOUT','')
ABOUT = ABOUT.replace('NAVABOUT','on').replace('NAVHOME','')


def simple_page(title, text):
    return ("<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>%s - Ghosts of Space</title><style>%s</style></head><body><div class='page'><h2>%s</h2>"
            "<p class='tagline'>%s</p><a href='/'>Back to home</a></div></body></html>" % (title, PAGE_STYLE, title, text))


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, code=200):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self._send(HOME)
        elif path == "/about":
            self._send(ABOUT)
        elif path == "/universe":
            self._send(simple_page("The Universe", "The graveyard of machines is coming soon. Add your next page here."))
        else:
            self._send(simple_page("Lost in space", "This page drifted away."), 404)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)
    threading.Timer(0.8, lambda: webbrowser.open("http://localhost:%d" % PORT)).start()
    print("Ghosts of Space running at http://localhost:%d  (Ctrl+C to stop)" % PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()