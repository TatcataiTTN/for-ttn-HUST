// SQL Sandbox + ngân hàng bài tập chạy sql.js (SQLite WASM) 100% phía trình duyệt.
// Hợp đồng: mỗi trang module gọi SQLBank.init({dataUrl, schemaUrl, vendorUrl, mount, storageKey}).
(function (global) {
  "use strict";

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function rowsEqual(expectedCols, expectedRows, gotCols, gotRows) {
    // So khớp theo GIÁ TRỊ (không phân biệt thứ tự cột theo tên, nhưng thứ tự DÒNG phải khớp
    // trừ khi referenceSql không có ORDER BY — ta chấp nhận khác thứ tự dòng, chỉ so đa tập).
    if (gotCols.length !== expectedCols.length) return false;
    const norm = (rows) => rows.map(r => r.map(v => (v === null || v === undefined) ? "∅" : String(v)).join("\u0001")).sort();
    const a = norm(expectedRows), b = norm(gotRows);
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
    return true;
  }

  function renderTable(cols, rows) {
    if (!cols.length) return '<p class="sb-empty">(không có cột trả về — câu lệnh không phải SELECT?)</p>';
    if (!rows.length) return '<p class="sb-empty">(0 dòng kết quả)</p>';
    let h = '<table class="sb-result"><thead><tr>' + cols.map(c => `<th>${esc(c)}</th>`).join("") + "</tr></thead><tbody>";
    for (const r of rows.slice(0, 200)) {
      h += "<tr>" + r.map(v => `<td>${v === null ? "<i>NULL</i>" : esc(v)}</td>`).join("") + "</tr>";
    }
    h += "</tbody></table>";
    if (rows.length > 200) h += `<p class="sb-empty">… và ${rows.length - 200} dòng nữa (chỉ hiện 200 dòng đầu)</p>`;
    return h;
  }

  async function loadEngine(vendorUrl) {
    if (global.__sqljs_promise) return global.__sqljs_promise;
    global.__sqljs_promise = new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = vendorUrl + "sql-wasm.js";
      s.onload = () => {
        global.initSqlJs({ locateFile: (f) => vendorUrl + f }).then(resolve).catch(reject);
      };
      s.onerror = () => reject(new Error("Không tải được sql-wasm.js"));
      document.head.appendChild(s);
    });
    return global.__sqljs_promise;
  }

  async function init(opts) {
    const mount = typeof opts.mount === "string" ? document.querySelector(opts.mount) : opts.mount;
    if (!mount) return;
    mount.innerHTML = '<p class="sb-loading">⏳ Đang tải SQLite engine (sql.js, ~650KB, chỉ tải 1 lần)…</p>';

    let SQL, schemaSql, questions;
    try {
      const engineP = loadEngine(opts.vendorUrl);
      const [schemaResp, dataResp] = await Promise.all([fetch(opts.schemaUrl), fetch(opts.dataUrl)]);
      if (!schemaResp.ok || !dataResp.ok) throw new Error("Không tải được schema/dữ liệu bài tập");
      schemaSql = await schemaResp.text();
      questions = await dataResp.json();
      SQL = await engineP;
    } catch (e) {
      mount.innerHTML = `<div class="callout warn"><div class="lbl">Lỗi tải SQL Sandbox</div>${esc(e.message)}
        <br><button class="mdeck-prev" id="sb-retry">↺ Thử lại</button></div>`;
      const btn = mount.querySelector("#sb-retry");
      if (btn) btn.onclick = () => init(opts);
      return;
    }

    const db = new SQL.Database();
    db.run(schemaSql);

    const storageKey = opts.storageKey || "sqlbank:default";
    let progress = {};
    try { progress = JSON.parse(localStorage.getItem(storageKey) || "{}"); } catch (e) {}
    const saveProgress = () => { try { localStorage.setItem(storageKey, JSON.stringify(progress)); } catch (e) {} };

    const topics = ["Tất cả"].concat([...new Set(questions.map(q => q.topic))]);
    let filterTopic = "Tất cả", filterDiff = 0, idx = 0;

    function filtered() {
      return questions.filter(q => (filterTopic === "Tất cả" || q.topic === filterTopic) && (!filterDiff || q.difficulty === filterDiff));
    }

    function renderShell() {
      const list = filtered();
      const done = list.filter(q => progress[q.id] && progress[q.id].ok).length;
      mount.innerHTML = `
        <div class="sb-toolbar">
          <select id="sb-topic">${topics.map(t => `<option ${t === filterTopic ? "selected" : ""}>${esc(t)}</option>`).join("")}</select>
          <select id="sb-diff">
            <option value="0">Mọi mức độ</option>
            <option value="1" ${filterDiff === 1 ? "selected" : ""}>1 - Dễ</option>
            <option value="2" ${filterDiff === 2 ? "selected" : ""}>2 - Trung</option>
            <option value="3" ${filterDiff === 3 ? "selected" : ""}>3 - Khó</option>
          </select>
          <span class="sb-progress">Đã làm đúng ${done}/${list.length}</span>
          <button id="sb-reset-all" class="sb-reset-all">↺ Xoá tiến độ</button>
        </div>
        <div class="sb-main">
          <div class="sb-sidebar" id="sb-sidebar"></div>
          <div class="sb-panel" id="sb-panel"></div>
        </div>`;
      mount.querySelector("#sb-topic").onchange = (e) => { filterTopic = e.target.value; idx = 0; renderShell(); };
      mount.querySelector("#sb-diff").onchange = (e) => { filterDiff = +e.target.value; idx = 0; renderShell(); };
      mount.querySelector("#sb-reset-all").onclick = () => {
        if (confirm("Xoá toàn bộ tiến độ SQL sandbox của module này?")) { progress = {}; saveProgress(); renderShell(); }
      };
      renderSidebar();
      renderPanel();
    }

    function renderSidebar() {
      const sb = mount.querySelector("#sb-sidebar");
      const list = filtered();
      sb.innerHTML = list.map((q, i) => {
        const st = progress[q.id];
        const mark = st ? (st.ok ? "✅" : "❌") : "⬜";
        return `<button class="sb-item ${i === idx ? "active" : ""}" data-i="${i}">${mark} ${esc(q.id)}</button>`;
      }).join("");
      sb.querySelectorAll(".sb-item").forEach(b => b.onclick = () => { idx = +b.dataset.i; renderSidebar(); renderPanel(); });
    }

    function renderPanel() {
      const list = filtered();
      const panel = mount.querySelector("#sb-panel");
      if (!list.length) { panel.innerHTML = "<p>Không có câu nào khớp bộ lọc.</p>"; return; }
      const q = list[idx];
      const st = progress[q.id];
      const savedSql = (st && st.lastSql) || "";
      panel.innerHTML = `
        <div class="sb-q"><b>${esc(q.id)}</b> · độ khó ${q.difficulty} · chủ đề: ${esc(q.topic)}<br>${esc(q.q)}</div>
        <textarea id="sb-editor" class="sb-editor" spellcheck="false" placeholder="Viết câu SQL ở đây rồi bấm Chạy...">${esc(savedSql)}</textarea>
        <div class="sb-actions">
          <button id="sb-run" class="mdeck-prev">▶ Chạy thử</button>
          <button id="sb-grade" class="mdeck-next">✅ Chấm điểm</button>
          <button id="sb-retry-one">↺ Làm lại câu này</button>
          <button id="sb-show-sol">👁 Xem lời giải mẫu</button>
        </div>
        <div id="sb-out"></div>`;

      const editor = panel.querySelector("#sb-editor");
      const out = panel.querySelector("#sb-out");

      function execUser() {
        const sql = editor.value.trim();
        if (!sql) { out.innerHTML = '<p class="sb-empty">Hãy nhập câu SQL.</p>'; return null; }
        try {
          const res = db.exec(sql);
          if (!res.length) return { cols: [], rows: [] };
          return { cols: res[0].columns, rows: res[0].values };
        } catch (e) {
          out.innerHTML = `<p class="no">❌ Lỗi SQL: ${esc(e.message)}</p>`;
          return null;
        }
      }

      panel.querySelector("#sb-run").onclick = () => {
        const r = execUser();
        if (r) out.innerHTML = renderTable(r.cols, r.rows);
      };

      panel.querySelector("#sb-grade").onclick = () => {
        const r = execUser();
        if (!r) return;
        const ok = rowsEqual(q.expectedCols, q.expectedRows, r.cols, r.rows);
        progress[q.id] = { ok, lastSql: editor.value };
        saveProgress();
        out.innerHTML = (ok
          ? '<p class="ok">✅ Chính xác — kết quả khớp với lời giải mẫu chạy thật trên dữ liệu.</p>'
          : '<p class="no">❌ Chưa khớp đáp án. Kết quả của bạn:</p>') + renderTable(r.cols, r.rows);
        renderSidebar();
      };

      panel.querySelector("#sb-retry-one").onclick = () => {
        delete progress[q.id]; saveProgress(); editor.value = ""; out.innerHTML = ""; renderSidebar();
      };

      panel.querySelector("#sb-show-sol").onclick = () => {
        out.innerHTML = `<div class="callout info"><div class="lbl">Lời giải mẫu</div><pre class="sb-sol">${esc(q.referenceSql)}</pre></div>` +
          renderTable(q.expectedCols, q.expectedRows);
      };
    }

    renderShell();
  }

  global.SQLBank = { init };
})(window);
