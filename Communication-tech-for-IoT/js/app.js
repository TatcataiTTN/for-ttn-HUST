/* Truyen thong Ve tinh cho IoT -- 200-question study app.
   Vanilla JS, static, no backend. Client-side grading. Progress: localStorage. */
(function () {
  "use strict";

  var LS_MCQ = "sat_iot_progress_v1";
  var Q = null;   // {meta, questions}
  var M = (typeof mathify === "function") ? mathify : function (s) { return esc(s); };
  var BY_PERSP = {};
  var P_MCQ = load(LS_MCQ);   // id -> {chosen, correct}

  function load(k) { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } }
  function saveMcq() { try { localStorage.setItem(LS_MCQ, JSON.stringify(P_MCQ)); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function boot() {
    fetch("data/questions.json", { cache: "no-cache" }).then(chk).then(function (r) {
      Q = r;
      Q.questions.forEach(function (q) { (BY_PERSP[q.perspective] = BY_PERSP[q.perspective] || []).push(q); });
      window.addEventListener("hashchange", route);
      route();
    }).catch(function (e) {
      document.getElementById("content").innerHTML =
        '<div class="loading">Không tải được dữ liệu (' + esc(e.message) +
        ').<br><button class="btn btn-primary" onclick="location.reload()">Thử lại</button></div>';
    });
  }
  function chk(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); }

  /* ---------------- sidebar ---------------- */
  function renderNav() {
    var nav = document.getElementById("nav");
    var list = "";
    Q.meta.perspectives.forEach(function (p) {
      var arr = BY_PERSP[p.num]; var st = mcqStats(arr);
      var pct = st.total ? Math.round(100 * st.done / st.total) : 0;
      list += navItem("#/p/" + p.num + "/0", "P" + p.num, p.title, st, pct, "mcq-" + p.num);
    });
    nav.innerHTML = list;
    renderOverall();
  }
  function navItem(href, tag, title, st, pct, key) {
    return '<a class="nav-item" data-key="' + key + '" href="' + href + '">' +
      '<span class="ni-top"><span class="ni-num">' + tag + '</span>' +
      '<span class="ni-count">' + st.done + "/" + st.total + "</span></span>" +
      '<span class="ni-title">' + esc(title) + "</span>" +
      '<span class="ni-mini"><i style="width:' + pct + '%"></i></span></a>';
  }
  function renderOverall() {
    var sm = mcqStats(Q.questions);
    var pm = Math.round(100 * sm.done / sm.total);
    document.getElementById("overall-progress").innerHTML =
      "<div><strong>Tiến độ tổng thể</strong></div>" +
      '<div class="op-row"><span>Đã làm</span><span>' + sm.done + "/" + sm.total + " · " + (sm.done ? Math.round(100 * sm.correct / sm.done) : 0) + "% đúng</span></div>" +
      '<div class="op-bar"><div class="op-fill" style="width:' + pm + '%"></div></div>';
  }
  function mcqStats(list) { var d = 0, c = 0; list.forEach(function (q) { var p = P_MCQ[q.id]; if (p) { d++; if (p.correct) c++; } }); return { done: d, correct: c, total: list.length }; }
  function setActive(key) { document.querySelectorAll(".nav-item").forEach(function (b) { b.classList.toggle("active", b.dataset.key === key); }); }

  function wrongMcq() { return Q.questions.filter(function (q) { var p = P_MCQ[q.id]; return p && !p.correct; }); }

  /* ---------------- router ---------------- */
  function route() {
    var h = location.hash || "#/";
    window.scrollTo(0, 0);
    renderNav();
    if (h === "#/frameworks") { setActive(null); return renderFrameworks(); }
    if (h === "#/review") { setActive(null); return renderReviewHome(); }
    var rv = h.match(/^#\/review\/(\d+)$/);
    if (rv) { setActive(null); return renderReviewItem(+rv[1]); }
    var mp = h.match(/^#\/p\/(\d+)(?:\/(\d+))?$/);
    if (mp && BY_PERSP[+mp[1]]) { setActive("mcq-" + mp[1]); return renderMcq(+mp[1], mp[2] ? +mp[2] : 0); }
    setActive(null); renderHome();
  }

  /* ---------------- home ---------------- */
  function renderHome() {
    var sm = mcqStats(Q.questions);
    var html =
      '<div class="home-hero"><h1>Truyền thông Vệ tinh cho IoT — Không gian ôn tập</h1>' +
      "<p><strong>200 câu hỏi hệ thống, 7 chủ đề: từ vật lý kênh quang (FSO) đến máy thu, thời tiết thực, hình học vùng phủ, lập lịch mạng lưới và relay liên-vệ-tinh.</strong></p>" +
      '<p class="hh-muted">Môn Các công nghệ truyền thông cho IoT · HUST 20251196M · Trương Tuấn Nghĩa.</p>' +
      "<p>Mỗi câu hỏi đi kèm dòng <em>khung lý thuyết</em> giải thích Ý NGHĨA của công thức/thuật toán, không chỉ đáp án đúng — mục tiêu là hiểu bản chất, không học vẹt.</p>" +
      '<div class="home-ctas">' +
      '<a class="home-cta" href="#/p/0/0">Bắt đầu · 200 câu →</a>' +
      '<a class="home-cta ghost" href="#/review">Ôn lại câu sai 🔁</a>' +
      '<a class="home-cta ghost" href="#/frameworks">Tra cứu ý nghĩa công thức 🧠</a>' +
      "</div></div>";
    html += '<div class="two-col"><div class="col-card"><h2>200 câu hỏi</h2><p class="cc-sub">7 chủ đề, từ khái niệm nền tảng đến vật lý kênh, máy thu, thời tiết, hình học, lập lịch, và các mở rộng nâng cao.</p>' +
      '<div class="pb-track"><div class="pb-fill" style="width:' + Math.round(100 * sm.done / sm.total) + '%"></div></div>' +
      '<div class="cc-stat">' + sm.done + " / " + sm.total + " đã làm" + (sm.done ? " · " + Math.round(100 * sm.correct / sm.done) + "% đúng" : "") + "</div></div></div>";
    document.getElementById("content").innerHTML = html;
  }

  /* ---------------- MCQ ---------------- */
  function renderMcq(pn, qi) {
    var list = BY_PERSP[pn];
    qi = Math.max(0, Math.min(qi, list.length - 1));
    var q = list[qi], meta = Q.meta.perspectives.find(function (p) { return p.num === pn; });
    var st = mcqStats(list), pct = Math.round(100 * st.done / st.total);
    var prog = P_MCQ[q.id];
    var html = pageHead("P" + pn + " · " + esc(meta.title), "Câu " + (qi + 1) + " / " + list.length + (q.group ? " · " + esc(q.group) : ""), st, pct);
    html += '<div class="qcard"><div class="qhead"><span class="qid">Q' + q.id + "</span>" + (q.group ? '<span class="qgroup">' + esc(q.group) + "</span>" : "") + "</div>";
    html += '<div class="qtext">' + M(q.question) + '</div><div class="opts" id="opts">';
    q.options.forEach(function (o) {
      var cls = "opt", mark = "";
      if (prog) { cls += " disabled"; if (o.key === q.answer) { cls += " correct"; mark = "✓"; } else if (o.key === prog.chosen) { cls += " wrong"; mark = "✗"; } }
      html += '<div class="' + cls + '" data-key="' + o.key + '"><span class="opt-key">' + o.key + "</span><span class=\"opt-text\">" + M(o.text) + "</span>" + (mark ? '<span class="opt-mark">' + mark + "</span>" : "") + "</div>";
    });
    html += "</div>";
    html += '<div class="qactions"><button class="btn btn-primary" id="submit-btn"' + (prog ? " disabled" : "") + '>Kiểm tra đáp án</button><span class="verdict" id="verdict"></span></div>';
    html += frameworkBox(q.framework, !!prog);
    html += "</div>" + pager("#/p/" + pn + "/", pn, qi, list.length, Q.meta.perspectives, "num");
    var content = document.getElementById("content"); content.innerHTML = html;

    var verdict = document.getElementById("verdict"), fw = document.getElementById("framework"), submitBtn = document.getElementById("submit-btn");
    if (prog) { verdict.textContent = prog.correct ? "Chính xác" : "Chưa đúng — đáp án đúng: " + q.answer; verdict.className = "verdict " + (prog.correct ? "ok" : "bad"); return; }
    var selected = null, optsEl = document.getElementById("opts");
    optsEl.querySelectorAll(".opt").forEach(function (el) {
      el.onclick = function () { selected = el.dataset.key; optsEl.querySelectorAll(".opt").forEach(function (x) { x.classList.remove("selected"); }); el.classList.add("selected"); submitBtn.disabled = false; };
    });
    submitBtn.disabled = true;
    submitBtn.onclick = function () {
      if (!selected) return;
      var correct = selected === q.answer;
      P_MCQ[q.id] = { chosen: selected, correct: correct }; saveMcq();
      optsEl.querySelectorAll(".opt").forEach(function (el) {
        el.classList.add("disabled"); el.onclick = null; el.classList.remove("selected");
        var k = el.dataset.key;
        if (k === q.answer) { el.classList.add("correct"); el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✓</span>'); }
        else if (k === selected) { el.classList.add("wrong"); el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✗</span>'); }
      });
      submitBtn.disabled = true;
      verdict.textContent = correct ? "Chính xác" : "Chưa đúng — đáp án đúng: " + q.answer;
      verdict.className = "verdict " + (correct ? "ok" : "bad");
      fw.classList.add("show"); renderNav(); setActive("mcq-" + pn);
    };
  }

  /* ---------------- Frameworks reference ---------------- */
  function renderFrameworks() {
    var html = '<a class="back-home" href="#/">← Về trang chủ</a><div class="page-head"><h1>Tra cứu ý nghĩa công thức 🧠</h1>' +
      '<div class="ph-sub">Toàn bộ 200 dòng khung lý thuyết, gộp theo 7 chủ đề, để ôn nhanh ý nghĩa công thức mà không cần trả lời lại câu hỏi. Dùng ô tìm kiếm để tra nhanh một khái niệm.</div></div>';
    html += '<input type="text" id="fw-search" class="fw-search" placeholder="Tìm khung lý thuyết (ví dụ: crosstalk, Rytov, Hungarian, QBER)…">';
    html += '<div id="fw-list">';
    Q.meta.perspectives.forEach(function (p) {
      var arr = BY_PERSP[p.num];
      html += '<div class="fw-group"><h3>P' + p.num + " — " + esc(p.title) + "</h3>";
      arr.forEach(function (q) { html += fwItem("Q" + q.id, q.question, q.framework); });
      html += "</div>";
    });
    html += "</div>";
    document.getElementById("content").innerHTML = html;
    var search = document.getElementById("fw-search");
    search.oninput = function () {
      var t = search.value.toLowerCase().trim();
      document.querySelectorAll(".fw-item").forEach(function (it) {
        it.style.display = (!t || it.textContent.toLowerCase().indexOf(t) >= 0) ? "" : "none";
      });
      document.querySelectorAll(".fw-group").forEach(function (g) {
        var any = [].some.call(g.querySelectorAll(".fw-item"), function (it) { return it.style.display !== "none"; });
        g.style.display = any ? "" : "none";
      });
    };
  }
  function fwItem(tag, prompt, fw) {
    return '<div class="fw-item"><div class="fw-q"><span class="fw-tag">' + tag + "</span> " + M(prompt) + "</div>" +
      '<div class="fw-a">' + M(fw) + "</div></div>";
  }

  /* ---------------- Review wrong answers ---------------- */
  function renderReviewHome() {
    var wm = wrongMcq();
    var html = '<a class="back-home" href="#/">← Về trang chủ</a><div class="page-head"><h1>Ôn lại câu sai 🔁</h1>' +
      '<div class="ph-sub">Chỉ làm lại các câu đã trả lời sai. Sửa đúng thì câu đó tự động rời khỏi danh sách.</div></div>';
    if (!wm.length) {
      html += '<div class="qcard" style="text-align:center"><div class="qtext" style="margin:8px 0">🎉 Không có câu nào cần ôn lại.</div>' +
        '<p class="cc-sub">Làm một số câu hỏi trước, rồi quay lại đây để luyện riêng những câu bị sai.</p>' +
        '<a class="btn btn-primary" href="#/p/0/0">Đi làm bài</a></div>';
      document.getElementById("content").innerHTML = html; return;
    }
    html += '<div class="home-ctas"><a class="home-cta" href="#/review/0">Ôn lại ' + wm.length + ' câu sai →</a></div>';
    html += '<div class="fw-group"><h3>Danh sách câu sai (' + wm.length + ")</h3>";
    wm.forEach(function (it, i) {
      html += '<a class="fw-item" style="display:block;text-decoration:none" href="#/review/' + i + '">' +
        '<div class="fw-q"><span class="fw-tag">Q' + it.id + "</span> " + esc(it.question) + "</div></a>";
    });
    html += "</div>";
    document.getElementById("content").innerHTML = html;
  }

  function renderReviewItem(i) {
    var list = wrongMcq();
    if (!list.length) {
      document.getElementById("content").innerHTML =
        '<a class="back-home" href="#/review">← Ôn lại</a><div class="qcard" style="text-align:center">' +
        '<div class="qtext" style="margin:8px 0">🎉 Hết câu sai rồi!</div>' +
        '<a class="btn btn-primary" href="#/review">Quay lại</a></div>';
      return;
    }
    i = Math.max(0, Math.min(i, list.length - 1));
    var q = list[i];
    var head = '<a class="back-home" href="#/review">← Ôn lại</a>' +
      '<div class="page-head"><h1>Ôn lại · câu sai</h1>' +
      '<div class="ph-sub">' + list.length + " câu cần sửa · đang làm lại Q" + q.id + "</div></div>";
    var html = head + '<div class="qcard"><div class="qhead"><span class="qid">Q' + q.id + "</span>" +
      (q.group ? '<span class="qgroup">' + esc(q.group) + "</span>" : "") + "</div>" +
      '<div class="qtext">' + M(q.question) + '</div><div class="opts" id="opts">';
    q.options.forEach(function (o) {
      html += '<div class="opt" data-key="' + o.key + '"><span class="opt-key">' + o.key + '</span><span class="opt-text">' + M(o.text) + "</span></div>";
    });
    html += '</div><div class="qactions"><button class="btn btn-primary" id="submit-btn" disabled>Kiểm tra đáp án</button>' +
      '<span class="verdict" id="verdict"></span></div>' + frameworkBox(q.framework, false) +
      '<div class="pager" id="rev-pager"></div></div>';
    document.getElementById("content").innerHTML = html;
    var selected = null, optsEl = document.getElementById("opts"), submitBtn = document.getElementById("submit-btn"),
        verdict = document.getElementById("verdict"), fw = document.getElementById("framework");
    optsEl.querySelectorAll(".opt").forEach(function (el) {
      el.onclick = function () { selected = el.dataset.key; optsEl.querySelectorAll(".opt").forEach(function (x) { x.classList.remove("selected"); }); el.classList.add("selected"); submitBtn.disabled = false; };
    });
    submitBtn.onclick = function () {
      if (!selected) return;
      var correct = selected === q.answer;
      P_MCQ[q.id] = { chosen: selected, correct: correct }; saveMcq();
      optsEl.querySelectorAll(".opt").forEach(function (el) {
        el.classList.add("disabled"); el.onclick = null; el.classList.remove("selected");
        var k = el.dataset.key;
        if (k === q.answer) { el.classList.add("correct"); el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✓</span>'); }
        else if (k === selected) { el.classList.add("wrong"); el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✗</span>'); }
      });
      submitBtn.disabled = true;
      verdict.textContent = correct ? "Đã sửa đúng!" : "Vẫn sai — đáp án đúng: " + q.answer;
      verdict.className = "verdict " + (correct ? "ok" : "bad");
      fw.classList.add("show");
      document.getElementById("rev-pager").innerHTML =
        '<a class="btn btn-ghost" href="#/review">Về danh sách</a><button class="btn btn-primary" id="rev-next">Câu sai tiếp theo →</button>';
      document.getElementById("rev-next").onclick = function () {
        var l2 = wrongMcq();
        if (!l2.length) { location.hash = "#/review"; } else { renderReviewItem(0); }
      };
      renderNav();
    };
  }

  /* ---------------- shared bits ---------------- */
  function pageHead(title, sub, st, pct) {
    return '<div class="page-head"><h1>' + title + '</h1><div class="ph-sub">' + sub + "</div></div>" +
      '<div class="persp-bar"><div class="pb-prog"><div class="pb-track"><div class="pb-fill" style="width:' + pct + '%"></div></div></div>' +
      '<div class="pb-num">' + st.done + "/" + st.total + " đã làm" + (st.done ? " · " + Math.round(100 * st.correct / st.done) + "% đúng" : "") + "</div></div>";
  }
  function frameworkBox(fw, show) {
    return '<div class="framework' + (show ? " show" : "") + '" id="framework"><div class="fw-label">Khung lý thuyết</div>' + M(fw) + "</div>";
  }
  function pager(base, num, i, len, arr, key) {
    var html = '<div class="pager">';
    html += i > 0 ? '<a class="btn btn-ghost" href="' + base + (i - 1) + '">← Câu trước</a>' : "<span></span>";
    if (i < len - 1) html += '<a class="btn btn-primary" href="' + base + (i + 1) + '">Câu tiếp →</a>';
    else {
      var idx = arr.findIndex(function (o) { return o[key] === num; });
      if (idx < arr.length - 1) html += '<a class="btn btn-primary" href="' + base.replace(/\/\d+\/$/, "/") + arr[idx + 1][key] + '/0">Chủ đề tiếp theo →</a>';
      else html += '<a class="btn btn-primary" href="#/">Hoàn thành — về trang chủ →</a>';
    }
    return html + "</div>";
  }

  document.getElementById("reset-btn").onclick = function () {
    if (confirm("Xóa TOÀN BỘ tiến độ đã lưu trên trình duyệt này?")) { P_MCQ = {}; saveMcq(); route(); }
  };
  boot();
})();
