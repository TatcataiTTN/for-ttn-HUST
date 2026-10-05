document.addEventListener('DOMContentLoaded', function(){
  const modal = document.getElementById('info-modal');
  if (!modal) return;
  const openers = document.querySelectorAll('[data-open-info]');
  const closeBtn = modal.querySelector('.close');
  openers.forEach(b => b.addEventListener('click', () => { modal.hidden = false; }));
  closeBtn?.addEventListener('click', () => { modal.hidden = true; });
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.hidden = true; });
});
