(function(){
  'use strict';
  const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
  const html=document.documentElement,stage=$('#stage'),telas=$$('.tela'),prog=$('#prog i'),cont=$('#cont'),fala=$('#fala'),sum=$('#sumario'),caixa=$('#caixa');
  const modoPdf=new URLSearchParams(location.search).has('pdf');
  if(modoPdf)html.classList.add('pdf');
  /* PDF: o vídeo da montagem para no display já montado */
  if(modoPdf)document.querySelectorAll('video').forEach(v=>{v.removeAttribute('autoplay');v.pause();const f=()=>{try{v.currentTime=4.2}catch(e){}};v.readyState>0?f():v.addEventListener('loadedmetadata',f,{once:true});});
  /* espaços da equipe de design: assets/slots/<nome>.<webp|png|jpg|svg|mp4> entra sozinho no lugar reservado */
  $$('[data-slot]').forEach(f=>{const nome=f.dataset.slot,exts=(f.dataset.tipos||'webp png jpg svg').split(' ');let i=0;
    (function tenta(){if(i>=exts.length)return;const e=exts[i++],u='assets/slots/'+nome+'.'+e;
      if(e==='mp4'){const v=document.createElement('video');v.muted=true;v.loop=true;v.playsInline=true;v.autoplay=!modoPdf;v.preload='auto';
        v.addEventListener('loadeddata',()=>{f.classList.add('cheio');f.prepend(v);if(modoPdf){try{v.currentTime=Math.min(4,(v.duration||8)/2)}catch(x){}}else v.play().catch(()=>{});},{once:true});
        v.addEventListener('error',tenta,{once:true});v.src=u;}
      else{const im=new Image();im.onload=()=>{im.alt=f.dataset.alt||'';f.classList.add('cheio');f.prepend(im);};im.onerror=tenta;im.src=u;}})();});
  const total=telas.length,dd=n=>String(n).padStart(2,'0');let atual=-1,verFala=false;

  /* celular: abaixo de 900 px as telas viram blocos empilhados */
  const ehCel=()=>!modoPdf&&Math.min(innerWidth,screen.width||innerWidth)<900;
  function escala(){
    html.classList.toggle('cel',ehCel());
    if(html.classList.contains('cel')){stage.style.transform='';return;}
    stage.style.transform='scale('+Math.min(innerWidth/1600,innerHeight/900)+')';
  }
  addEventListener('resize',escala);addEventListener('orientationchange',escala);escala();

  /* números que contam */
  function contar(el){
    const alvo=parseFloat(el.dataset.conta),casas=+el.dataset.casas||0,fmt=v=>v.toFixed(casas).replace('.',',');
    if(modoPdf||html.classList.contains('cel')){el.textContent=fmt(alvo);return;}
    const t0=performance.now();(function p(t){const f=Math.min(1,(t-t0)/1200);el.textContent=fmt(alvo*(1-Math.pow(1-f,3)));if(f<1)requestAnimationFrame(p);})(t0);
  }

  /* abas com temporizador: abrem sozinhas, uma por vez; o primeiro clique de verdade para tudo */
  const grupos=$$('[data-abas]').map(g=>{
    const bts=$$('.aba',g),pns=$$('.painel',g);
    const st={g,bts,pns,i:0,timer:null,parado:false};
    function mostra(i){st.i=i;g.dataset.on=i;bts.forEach((b,k)=>{b.classList.toggle('on',k===i);b.style.setProperty('--t','0s');b.classList.remove('corre');});pns.forEach((p,k)=>p.classList.toggle('on',k===i));
      pns[i]&&pns[i].querySelectorAll('[data-conta]').forEach(contar);}
    st.mostra=mostra;
    st.agenda=function(){clearTimeout(st.timer);if(st.parado||modoPdf)return;
      const txt=(pns[st.i]&&pns[st.i].textContent||'').trim().split(/\s+/).length;const ms=Math.max(5000,Math.min(14000,txt*260));
      const b=bts[st.i];if(b){b.style.setProperty('--t',ms+'ms');void b.offsetWidth;b.classList.add('corre');}
      st.timer=setTimeout(()=>{mostra((st.i+1)%bts.length);st.agenda();},ms);};
    st.para=function(){st.parado=true;clearTimeout(st.timer);bts.forEach(b=>b.classList.remove('corre'));g.classList.add('parado');};
    bts.forEach((b,k)=>b.addEventListener('click',e=>{e.stopPropagation();st.para();mostra(k);}));
    mostra(0);return st;
  });
  function iniciaTimers(t){grupos.forEach(st=>{if(t.contains(st.g)&&!st.parado){st.mostra(0);st.agenda();}else clearTimeout(st.timer);});}
  /* o primeiro clique de verdade dentro da tela para os temporizadores dela */
  telas.forEach(t=>t.addEventListener('pointerdown',()=>grupos.forEach(st=>{if(t.contains(st.g))st.para();})));

  /* PDF: uma página por botão (fonte/gerar-pdf.mjs) */
  window.__pdfEstados=function(){const t=telas[atual];const st=grupos.find(s=>t.contains(s.g));return st?st.bts.length:0;};
  window.__pdfEstado=function(k){const t=telas[atual];grupos.filter(s=>t.contains(s.g)).forEach(st=>{st.para();st.mostra(Math.min(k,st.bts.length-1));});};

  const wipe=$('#wipe');let trocando=false;
  function ir(n){
    n=Math.max(0,Math.min(total-1,n));if(n===atual||trocando)return;
    if(atual<0||modoPdf||html.classList.contains('cel')||matchMedia('(prefers-reduced-motion:reduce)').matches){troca(n);return;}
    trocando=true;const cap=telas[n].classList.contains('cap');
    wipe.classList.remove('vai','capitulo');void wipe.offsetWidth;wipe.classList.toggle('capitulo',cap);wipe.classList.add('vai');stage.classList.add('cine');
    const cobre=cap?520:380,sai=cap?1150:860;
    setTimeout(()=>{troca(n,sai-cobre-120);},cobre);
    setTimeout(()=>{wipe.classList.remove('vai');stage.classList.remove('cine');trocando=false;},sai);
  }
  /* espera: a tela aparece por baixo da cortina e só começa a animar quando a cortina sai, para os infográficos serem vistos */
  function troca(n,espera){
    const ant=atual>=0?telas[atual]:null;
    if(ant){ant.classList.remove('ativa','visivel');ant.classList.add('saindo');setTimeout(()=>ant.classList.remove('saindo'),700);}
    atual=n;const t=telas[n];
    if(espera>0){t.classList.add('visivel');setTimeout(()=>{if(atual===n)entra(t);},espera);}else entra(t);
    prog.style.width=((n+1)/total*100)+'%';cont.textContent=dd(n+1)+' / '+dd(total);
    $('#ant').disabled=n===0;$('#prox').disabled=n===total-1;
    html.dataset.fundo=t.classList.contains('escuro')||t.classList.contains('capa')||t.classList.contains('q-tema-escuro')||t.classList.contains('vermelho')?'escuro':(t.classList.contains('amarelo')?'amarelo':'claro');
    $$('#sumLista button').forEach(b=>b.classList.toggle('atual',+b.dataset.i===n));
    history.replaceState(null,'','#'+(n+1));mostrarFala();marcaFio(t);
  }
  function marcaFio(t){const p=+(t.dataset.parte||0);$$('#fio li').forEach(li=>{const k=+li.dataset.p;li.classList.toggle('on',k===p);li.classList.toggle('feito',k<p);});$('#fio').classList.toggle('some',!p);}
  function entra(t){
    t.classList.remove('visivel');t.classList.add('ativa');
    t.querySelectorAll('[data-conta]').forEach(el=>{if(!el.closest('.painel'))contar(el);});
    iniciaTimers(t);
  }
  function mostrarFala(){const r=telas[atual].querySelector('aside.roteiro');fala.textContent=r?r.textContent.trim():'';fala.classList.toggle('on',verFala&&!!fala.textContent);}

  $('#ant').addEventListener('click',e=>{e.stopPropagation();ir(atual-1);});
  $('#prox').addEventListener('click',e=>{e.stopPropagation();ir(atual+1);});
  $$('[data-ir]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();ir(+b.dataset.ir);}));
  addEventListener('hashchange',()=>{const n=parseInt(location.hash.slice(1),10);if(!isNaN(n))ir(n-1);});

  /* sumário (tecla M) */
  const lista=$('#sumLista');let cap='';
  telas.forEach((t,i)=>{
    if(t.dataset.capitulo&&t.dataset.capitulo!==cap){cap=t.dataset.capitulo;const h=document.createElement('li');h.className='cap';h.textContent=cap;lista.appendChild(h);}
    const li=document.createElement('li'),b=document.createElement('button');b.innerHTML='<b>'+dd(i+1)+'</b>'+t.dataset.titulo;b.dataset.i=i;
    b.addEventListener('click',e=>{e.stopPropagation();sum.classList.remove('aberto');setTimeout(()=>ir(i),60);});li.appendChild(b);lista.appendChild(li);});
  $$('[data-sumario]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();sum.classList.add('aberto');}));
  $('.fechar',sum).addEventListener('click',e=>{e.stopPropagation();sum.classList.remove('aberto');});
  sum.addEventListener('click',e=>e.stopPropagation());

  /* toda imagem amplia */
  $$('[data-amplia]').forEach(i=>i.addEventListener('click',e=>{e.stopPropagation();$('#cxImg').src=i.dataset.amplia||i.src;$('#cxImg').alt=i.alt||'';caixa.classList.add('aberta');}));
  caixa.addEventListener('click',e=>{e.stopPropagation();caixa.classList.remove('aberta');});

  addEventListener('keydown',e=>{
    if(caixa.classList.contains('aberta')){if(e.key==='Escape')caixa.classList.remove('aberta');return;}
    if(sum.classList.contains('aberto')){if(e.key==='Escape'||e.key==='m'||e.key==='M')sum.classList.remove('aberto');return;}
    if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();ir(atual+1);}
    else if(['ArrowLeft','PageUp','Backspace'].includes(e.key)){e.preventDefault();ir(atual-1);}
    else if(e.key==='Home')ir(0);else if(e.key==='End')ir(total-1);
    else if('nNrR'.includes(e.key)&&e.key.length===1){verFala=!verFala;mostrarFala();}
    else if(e.key==='m'||e.key==='M')sum.classList.add('aberto');
  });
  /* toque: deslizar */
  let x0=null;addEventListener('touchstart',e=>{x0=e.touches[0].clientX;},{passive:true});
  addEventListener('touchend',e=>{if(x0===null||html.classList.contains('cel'))return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>60)ir(dx<0?atual+1:atual-1);x0=null;});

  /* cursor em dois tons, visível sobre amarelo, vermelho, fotos e fundo escuro */
  if(matchMedia('(pointer:fine)').matches&&!modoPdf){
    document.body.classList.add('tem-mouse');const c=$('#cursor'),a=$('#anel');let x=0,y=0,ax=0,ay=0;
    addEventListener('mousemove',e=>{x=e.clientX;y=e.clientY;c.style.transform='translate('+x+'px,'+y+'px)';a.classList.toggle('gr',!!e.target.closest('a,button,[data-amplia],.aba,.mes'));},{passive:true});
    (function p(){ax+=(x-ax)*.22;ay+=(y-ay)*.22;a.style.transform='translate('+ax+'px,'+ay+'px)';requestAnimationFrame(p);})();
  }
  /* luz que segue o mouse */
  if(!modoPdf)addEventListener('mousemove',e=>{const r=stage.getBoundingClientRect();stage.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');stage.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%');},{passive:true});

  /* celular: tela entra quando aparece na rolagem */
  if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting&&html.classList.contains('cel')){en.target.classList.add('vista');en.target.querySelectorAll('[data-conta]').forEach(contar);}}),{threshold:.15});telas.forEach(t=>io.observe(t));}

  const n0=parseInt(location.hash.slice(1),10);ir(isNaN(n0)?0:n0-1);
})();
