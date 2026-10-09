// Ngân hàng trắc nghiệm luyện tập sâu — lọc nguồn/chủ đề, phân trang, chấm ngay, lưu tiến độ.
// Hợp đồng: BankUI.init({mount, dataUrl, storageKey}).
(function (global) {
  "use strict";

  function escT(s) { const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }

  async function init(opts) {
    const mount = typeof opts.mount === "string" ? document.querySelector(opts.mount) : opts.mount;
    if (!mount) return;
    mount.innerHTML = '<p class="sb-loading">⏳ Đang tải ngân hàng câu hỏi…</p>';

    let items;
    try {
      const r = await fetch(opts.dataUrl);
      if (!r.ok) throw new Error("HTTP " + r.status);
      items = await r.json();
    } catch (e) {
      mount.innerHTML = `<div class="callout warn"><div class="lbl">Lỗi tải ngân hàng</div>${escT(e.message)}</div>`;
      return;
    }

    const storageKey = opts.storageKey || "bank:default";
    let progress = {};
    try { progress = JSON.parse(localStorage.getItem(storageKey) || "{}"); } catch (e) {}
    const save = () => { try { localStorage.setItem(storageKey, JSON.stringify(progress)); } catch (e) {} };

    const topics = ["Tất cả"].concat([...new Set(items.map(i => i.topic))]);
    const PAGE = 15;
    let topic = "Tất cả", src = "Tất cả", onlyWrong = false, page = 0, shuffled = false;
    let order = items.map((_, i) => i);

    function current() {
      let list = order.map(i => items[i]);
      if (topic !== "Tất cả") list = list.filter(q => q.topic === topic);
      if (src !== "Tất cả") list = list.filter(q => q.src === src);
      if (onlyWrong) list = list.filter(q => progress[q.id] && progress[q.id].ok === false);
      return list;
    }

    function render() {
      const list = current();
      const totalPages = Math.max(1, Math.ceil(list.length / PAGE));
      page = Math.min(page, totalPages - 1);
      const pageItems = list.slice(page * PAGE, page * PAGE + PAGE);
      const doneCount = items.filter(q => progress[q.id] && progress[q.id].ok).length;

      mount.innerHTML = `
        <div class="sb-toolbar">
          <select id="bk-topic">${topics.map(t => `<option ${t === topic ? "selected" : ""}>${escT(t)}</option>`).join("")}</select>
          <select id="bk-src">
            <option ${src === "Tất cả" ? "selected" : ""}>Tất cả</option>
            <option value="gốc-slide" ${src === "gốc-slide" ? "selected" : ""}>➕ Chỉ câu gốc (slide/giáo trình)</option>
            <option value="bổ-sung" ${src === "bổ-sung" ? "selected" : ""}>➕ Chỉ câu bổ sung</option>
          </select>
          <label><input type="checkbox" id="bk-wrong" ${onlyWrong ? "checked" : ""}> Chỉ câu đã sai</label>
          <button id="bk-shuffle">🔀 ${shuffled ? "Về thứ tự gốc" : "Xáo trộn"}</button>
          <span class="sb-progress">Đã làm đúng ${doneCount}/${items.length}</span>
          <button id="bk-reset-all" class="sb-reset-all">↺ Xoá tiến độ</button>
        </div>
        <div id="bk-list"></div>
        <div class="bk-pager">
          <button id="bk-prev" ${page === 0 ? "disabled" : ""}>◀ Trang trước</button>
          <span>Trang ${page + 1}/${totalPages} (${list.length} câu khớp bộ lọc)</span>
          <button id="bk-next" ${page >= totalPages - 1 ? "disabled" : ""}>Trang sau ▶</button>
        </div>`;

      mount.querySelector("#bk-topic").onchange = (e) => { topic = e.target.value; page = 0; render(); };
      mount.querySelector("#bk-src").onchange = (e) => { src = e.target.value; page = 0; render(); };
      mount.querySelector("#bk-wrong").onchange = (e) => { onlyWrong = e.target.checked; page = 0; render(); };
      mount.querySelector("#bk-shuffle").onclick = () => {
        shuffled = !shuffled;
        order = shuffled ? items.map((_, i) => i).sort(() => Math.random() - 0.5) : items.map((_, i) => i);
        page = 0; render();
      };
      mount.querySelector("#bk-reset-all").onclick = () => {
        if (confirm("Xoá toàn bộ tiến độ ngân hàng câu hỏi này?")) { progress = {}; save(); render(); }
      };
      mount.querySelector("#bk-prev").onclick = () => { page--; render(); };
      mount.querySelector("#bk-next").onclick = () => { page++; render(); };

      const listEl = mount.querySelector("#bk-list");
      listEl.innerHTML = pageItems.map((q, li) => renderQ(q, li)).join("");
      pageItems.forEach((q, li) => wireQ(listEl, q, li));
    }

    function renderQ(q, li) {
      const st = progress[q.id];
      const answered = st && typeof st.picked === "number";
      const srcBadge = q.src === "gốc-slide" ? '<span class="bk-badge goc">Gốc slide/giáo trình</span>' : '<span class="bk-badge bosung">➕ Bổ sung</span>';
      return `<div class="bk-item" data-li="${li}">
        <div class="bk-qhead">${srcBadge} <span class="bk-topic">${escT(q.topic)}</span></div>
        <div class="bk-qtext">${escT(q.q)}</div>
        <div class="bk-opts">
          ${q.opts.map((o, oi) => `<button class="bk-opt ${answered ? (oi === q.correct ? "correct" : (oi === st.picked ? "picked-wrong" : "")) : ""}" data-oi="${oi}" ${answered ? "disabled" : ""}>${escT(o)}</button>`).join("")}
        </div>
        <div class="bk-explain" ${answered ? "" : "hidden"}>${answered ? (st.ok ? "✅ Chính xác. " : "❌ Chưa đúng. ") + escT(q.explain) : ""}</div>
        <button class="bk-retry" ${answered ? "" : "hidden"}>↺ Làm lại câu này</button>
      </div>`;
    }

    function wireQ(listEl, q, li) {
      const item = listEl.querySelector(`.bk-item[data-li="${li}"]`);
      item.querySelectorAll(".bk-opt").forEach(btn => {
        btn.onclick = () => {
          const oi = +btn.dataset.oi;
          progress[q.id] = { ok: oi === q.correct, picked: oi };
          save();
          render();
        };
      });
      const retry = item.querySelector(".bk-retry");
      if (retry) retry.onclick = () => { delete progress[q.id]; save(); render(); };
    }

    render();
  }

  global.BankUI = { init };
})(window);
