document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('.mdeck').forEach(function(deck){
    const slides = [...deck.querySelectorAll('.mdeck-slide')];
    const bar = deck.querySelector('.mdeck-bar');
    const prevBtn = bar.querySelector('.mdeck-prev'), nextBtn = bar.querySelector('.mdeck-next');
    const count = bar.querySelector('.mdeck-count'), dotsWrap = bar.querySelector('.mdeck-dots');
    const fsBtn = bar.querySelector('.mdeck-fs');
    let i = 0;
    slides.forEach((s, idx) => {
      const d = document.createElement('button'); d.type = 'button';
      d.addEventListener('click', () => go(idx));
      dotsWrap.appendChild(d);
    });
    const dots = [...dotsWrap.children];
    const viewport = deck.querySelector('.mdeck-viewport');
    function fit(){
      const s = slides[i];
      if (!s) return;
      s.style.transform = '';
      s.style.width = '';
      s.style.height = '';
      // chờ 1 frame để layout ổn định rồi đo chiều cao nội dung thật
      requestAnimationFrame(() => {
        const boxH = viewport.clientHeight;
        const contentH = s.scrollHeight;
        if (boxH > 0 && contentH > boxH) {
          const scale = Math.max(0.5, boxH / contentH);
          s.style.transformOrigin = 'top left';
          s.style.transform = `scale(${scale})`;
          s.style.width = (100 / scale) + '%';
          s.style.height = (100 / scale) + '%';
        }
      });
    }
    function render(){
      slides.forEach((s, idx) => s.classList.toggle('active', idx === i));
      dots.forEach((d, idx) => d.classList.toggle('on', idx === i));
      count.textContent = (i+1) + '/' + slides.length;
      prevBtn.disabled = i === 0; nextBtn.disabled = i === slides.length - 1;
      if (window.renderMathInElement) {
        try { renderMathInElement(slides[i], {delimiters: window.KATEX_DELIMS || [
          {left:'$$', right:'$$', display:true},
          {left:'$', right:'$', display:false}
        ], macros: window.KATEX_MACROS || {}, throwOnError: false}); } catch(e){}
      }
      fit();
    }
    function go(n){ i = Math.max(0, Math.min(slides.length - 1, n)); render(); }
    window.addEventListener('resize', fit);
    document.addEventListener('fullscreenchange', () => setTimeout(fit, 60));
    prevBtn.addEventListener('click', () => go(i - 1));
    nextBtn.addEventListener('click', () => go(i + 1));
    deck.tabIndex = 0;
    deck.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') go(i + 1);
      if (e.key === 'ArrowLeft') go(i - 1);
    });
    if (fsBtn) fsBtn.addEventListener('click', () => {
      if (!document.fullscreenElement) deck.requestFullscreen?.(); else document.exitFullscreen?.();
    });
    render();
  });
});
