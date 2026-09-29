document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('.quiz').forEach(function(quizEl){
    const dataEl = quizEl.querySelector('script[type="application/json"]');
    if (!dataEl) return;
    const Q = JSON.parse(dataEl.textContent);
    const root = quizEl.querySelector('.quiz-root');
    let scoreBox, restartBtn, answered;
    function build(){
      root.innerHTML = '';
      answered = 0; let score = 0;
      Q.items.forEach((q, qi) => {
        const box = document.createElement('div'); box.className = 'qitem';
        const head = document.createElement('div');
        head.innerHTML = '<b>Câu ' + (qi+1) + '.</b> ' + q.q;
        box.appendChild(head);
        const explain = document.createElement('div');
        explain.className = 'explain'; explain.textContent = q.explain;
        q.opts.forEach((opt, oi) => {
          const b = document.createElement('button'); b.type='button'; b.className = 'opt'; b.textContent = opt;
          b.addEventListener('click', () => {
            if (b.dataset.done) return;
            [...box.querySelectorAll('.opt')].forEach(x => x.dataset.done = '1');
            const correct = oi === q.correct;
            b.classList.add(correct ? 'correct' : 'wrong');
            if (!correct) { const ok = box.querySelectorAll('.opt')[q.correct]; if (ok) ok.classList.add('correct'); }
            explain.classList.add('show');
            answered++;
            if (correct) score++;
            scoreBox.textContent = 'Điểm: ' + score + '/' + Q.items.length + (answered < Q.items.length ? ' (đang làm...)' : ' — hoàn thành!');
          });
          box.appendChild(b);
        });
        box.appendChild(explain);
        root.appendChild(box);
      });
      if (window.renderMathInElement) {
        try { renderMathInElement(root, {delimiters: window.KATEX_DELIMS || [
          {left:'$$', right:'$$', display:true},{left:'$', right:'$', display:false}
        ], macros: window.KATEX_MACROS || {}, throwOnError: false}); } catch(e){}
      }
    }
    scoreBox = document.createElement('div'); scoreBox.className = 'quiz-score';
    scoreBox.textContent = 'Điểm: 0/' + Q.items.length;
    quizEl.insertBefore(scoreBox, root);
    restartBtn = document.createElement('button'); restartBtn.type='button';
    restartBtn.className = 'quiz-restart'; restartBtn.textContent = '↻ Làm lại từ đầu';
    restartBtn.addEventListener('click', () => {
      if (answered > 0 && !window.confirm('Làm lại toàn bộ quiz từ đầu?')) return;
      build(); scoreBox.textContent = 'Điểm: 0/' + Q.items.length;
    });
    quizEl.appendChild(restartBtn);
    build();
  });
});
