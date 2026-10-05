(function(){
  function applyFont(f){
    document.documentElement.style.setProperty('--userfont', f || '');
    if (f) document.body.style.fontFamily = f + ',-apple-system,"Segoe UI",Roboto,sans-serif';
  }
  document.addEventListener('DOMContentLoaded', function(){
    var sw = document.querySelector('.switcher');
    if (!sw) return;
    sw.querySelectorAll('[data-theme-set]').forEach(function(btn){
      btn.addEventListener('click', function(){
        var t = btn.getAttribute('data-theme-set');
        try{ localStorage.setItem('site-theme', t); }catch(e){}
        if (t === 'light') document.documentElement.removeAttribute('data-theme');
        else document.documentElement.setAttribute('data-theme', t);
        sw.removeAttribute('open');
      });
    });
    sw.querySelectorAll('[data-font-set]').forEach(function(btn){
      btn.addEventListener('click', function(){
        var f = btn.getAttribute('data-font-set');
        try{ localStorage.setItem('site-font', f); }catch(e){}
        applyFont(f);
        sw.removeAttribute('open');
      });
    });
    document.addEventListener('click', function(e){
      if (sw.hasAttribute('open') && !sw.contains(e.target)) sw.removeAttribute('open');
    });
    try{ var f = localStorage.getItem('site-font'); if (f) applyFont(f); }catch(e){}
  });
})();
