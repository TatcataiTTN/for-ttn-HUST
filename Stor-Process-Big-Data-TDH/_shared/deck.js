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
    const canvasWrap = deck.querySelector('.mdeck-canvas-wrap');
    const viewport = deck.querySelector('.mdeck-viewport');
    const DESIGN_W = 1280, DESIGN_H = 720;
    // Canvas thiết kế cố định 1280x720 được scale ĐỒNG NHẤT theo kích thước thật của
    // khung chứa (canvas-wrap) — phóng to khi chiếu full màn hình lớn, thu nhỏ khi nhúng
    // trong trang nhỏ. Không bao giờ co riêng từng slide theo nội dung nữa.
    function fit(){
      requestAnimationFrame(() => {
        const boxW = canvasWrap.clientWidth, boxH = canvasWrap.clientHeight;
        if (boxW <= 0 || boxH <= 0) return;
        const scale = Math.min(boxW / DESIGN_W, boxH / DESIGN_H);
        viewport.style.transform = `scale(${scale})`;
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
    // ResizeObserver bắt mọi thay đổi kích thước khung chứa (không chỉ window resize),
    // ví dụ khi sidebar/theme toggle làm layout trang đổi.
    if (window.ResizeObserver) new ResizeObserver(fit).observe(canvasWrap);
  });
});
