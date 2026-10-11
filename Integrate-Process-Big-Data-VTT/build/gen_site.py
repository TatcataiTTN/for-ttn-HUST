# -*- coding: utf-8 -*-
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from modules_content import MODULES

ROOT = pathlib.Path(__file__).parent.parent
EX = json.loads((pathlib.Path(__file__).parent / "exercises.json").read_text(encoding="utf-8"))

HEAD_THEME_SCRIPT = """<script>(function(){try{
  var t = localStorage.getItem('site-theme');
  if (t && t !== 'light') document.documentElement.setAttribute('data-theme', t);
}catch(e){}})();</script>"""

KATEX = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script>
window.KATEX_MACROS = {
  "\\\\E": "\\\\mathbb{E}", "\\\\Prob": "\\\\mathbb{P}", "\\\\R": "\\\\mathbb{R}",
  "\\\\Var": "\\\\operatorname{Var}"
};
window.KATEX_DELIMS = [{left:'$$', right:'$$', display:true},{left:'$', right:'$', display:false}];
</script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:window.KATEX_DELIMS, macros:window.KATEX_MACROS, throwOnError:false});"></script>"""

def topbar(rel_lang):
    return f"""<div class="topbar">
  <a class="brand" href="{rel_lang}index.html">Tích hợp &amp; xử lý <span>dữ liệu lớn</span></a>
  <nav>
    <a href="{rel_lang}index.html">Trang chủ</a>
    <a href="{rel_lang}modules/99-tai-lieu-tham-khao/index.html">Tài liệu tham khảo</a>
  </nav>
  <details class="switcher">
    <summary>🎨 Giao diện</summary>
    <div class="menu">
      <button data-theme-set="light">☀️ Sáng</button>
      <button data-theme-set="dark">🌙 Tối</button>
      <button data-font-set="Georgia, serif">Font chữ có chân</button>
      <button data-font-set="">Font mặc định</button>
    </div>
  </details>
</div>"""

def footer(rel_root):
    return f"""<footer>
  <div class="wrap">Hệ thống tự học &quot;IT5427 — Tích hợp và xử lý dữ liệu lớn&quot; (HUST, GV Vũ Tuyết Trinh) ·
  dựng từ 4 file slide bài giảng gốc + 23 bài báo khoa học đã xác minh. Không backend, chạy hoàn toàn phía trình duyệt.</div>
</footer>
<button class="fab" data-open-info title="Thông tin">ℹ️</button>
<div id="info-modal" hidden><div class="box">
  <button class="close">✕</button>
  <h3>Về trang này</h3>
  <p>Hệ thống tự học mở cho môn <b>IT5427 - Tích hợp và xử lý dữ liệu lớn</b> (HUST, giảng viên Vũ Tuyết Trinh).
  Bám sát 4 buổi slide đã học (Data Integration overview → Schema Alignment → Mediation Query → Record
  Linkage/Entity Resolution), cộng 1 module nền tảng CSDL tự bổ sung. Toàn bộ nội dung chạy tĩnh, không
  backend. Bài tập "làm giấy" ưu tiên câu gốc từ slide (ghi rõ nguồn), câu bổ sung gắn nhãn rõ ràng.</p>
</div></div>
<script src="{rel_root}_shared/theme.js"></script>
<script src="{rel_root}_shared/info.js"></script>"""

def page_shell(title, rel_lang, rel_root, body, extra_script=""):
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{HEAD_THEME_SCRIPT}
<title>{title}</title>
<link rel="stylesheet" href="{rel_root}_shared/common.css">
<link rel="stylesheet" href="{rel_root}_shared/deck.css">
{KATEX}
</head>
<body>
{topbar(rel_lang)}
<div class="wrap">
{body}
</div>
{footer(rel_root)}
<script src="{rel_root}_shared/deck.js"></script>
<script src="{rel_root}_shared/quiz.js"></script>
{extra_script}
</body></html>"""

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def slide_html(s):
    return f'<div class="mdeck-slide"><h2>{s["h"]}</h2>{s["body"]}</div>'

def part_divider(idx, total_parts, part):
    lis = "\n".join(f"<li>{b}</li>" for b in part["bullets"])
    return f"""<div class="mdeck-slide part-divider"><div class="kicker">PHẦN {idx}/{total_parts}</div>
<div class="part-num">{idx:02d}</div><h2>{part["title"]}</h2>
<ul class="part-list">{lis}</ul></div>"""

def render_tuluan(items):
    if not items:
        return ""
    blocks = []
    for i, it in enumerate(items, 1):
        blocks.append(f"""<details class="ex-item">
<summary>Bài {i}. {it['cau']} <span class="src">[{esc(it['nguon'])}]</span></summary>
<div class="loi-giai"><b>Lời giải:</b> {it['loi_giai']}</div></details>""")
    return f'<div class="exlist-tuluan">{"".join(blocks)}</div>'

def render_hoidap(items):
    if not items:
        return ""
    cards = []
    for it in items:
        cards.append(f"""<details class="flashcard">
<summary>❓ {esc(it['hoi'])}</summary><div class="dap">💡 {esc(it['dap'])}</div></details>""")
    return f'<div class="flashcard-grid">{"".join(cards)}</div>'

# slug module -> prefix file dữ liệu SQL sandbox (data/sql/schema_<prefix>.sql, questions_<prefix>.json)
SQL_SANDBOX_FOR = {
    "00-nen-tang-csdl": "m00",
    "01-data-integration-overview": "m01",
    "02-schema-alignment": "m02",
    "03-mediation-query-bigdata": "m03",
    "04-record-linkage-entity-resolution": "m04",
}
# slug module -> đường dẫn trang ngân hàng trắc nghiệm sâu (bank.html riêng, build bằng build_bank.py)
MCQ_BANK_FOR = {
    "00-nen-tang-csdl": "m00",
    "01-data-integration-overview": "m01",
    "02-schema-alignment": "m02",
    "03-mediation-query-bigdata": "m03",
    "04-record-linkage-entity-resolution": "m04",
}
# slug module -> mô tả ngắn nguồn gốc dữ liệu SQL sandbox của module đó
SQL_DESC_FOR = {
    "00-nen-tang-csdl": "Lược đồ 'Người thuê — Thuê — Căn hộ' (bảng trung gian N-N) đúng ví dụ đã dùng trong bài tập làm giấy Module 00.",
    "01-data-integration-overview": "Dùng lại dataset Movie S1-S7 của Module 02 để mô phỏng Wrapper/Query Reformulation/5V (module này chủ yếu lý thuyết kiến trúc nên số bài ít hơn).",
    "02-schema-alignment": "Lược đồ bảng S1-S7 lấy đúng nguyên văn slide gốc '2_SchemaAlignment.pdf'; dữ liệu 10 phim là dữ liệu minh hoạ tự soạn.",
    "03-mediation-query-bigdata": "Dùng lại dataset Movie S1-S7 của Module 02 để mô phỏng Join Graph/PAYGO/WebTables (module này chủ yếu lý thuyết nên số bài ít hơn).",
    "04-record-linkage-entity-resolution": "2 nguồn rao vặt bất động sản độc lập (nguon_a/nguon_b), 7/10 tin trùng thực thể với giá lệch 4-10% — đúng mô phỏng ví dụ D2 trong Quiz-Buoi4-RecordLinkage-ER.md.",
}

def build_module_page(mod, prev_mod, next_mod):
    rel_lang = "../../"
    rel_root = "../../../"
    slides = [f'<div class="mdeck-slide"><div class="kicker">BUỔI {mod["n"]:02d} · {mod["tag"]}</div>'
              f'<h2>{mod["title"]}</h2><p>{mod["intro"]}</p></div>']
    total_parts = len(mod["parts"])
    for pi, part in enumerate(mod["parts"], 1):
        slides.append(part_divider(pi, total_parts, part))
        for s in part["slides"]:
            slides.append(slide_html(s))
    deck = f"""<div class="mdeck"><div class="mdeck-viewport">{''.join(slides)}</div>
<div class="mdeck-bar">
  <button class="mdeck-prev">◀ Trước</button><button class="mdeck-next">Sau ▶</button>
  <span class="mdeck-count"></span><div class="mdeck-dots"></div>
  <button class="mdeck-fs">⛶ Toàn màn hình</button>
</div></div>"""

    n = mod["n"]
    tuluan_items = EX["tuluan"].get(str(n), [])
    hoidap_items = EX["hoidap"].get(str(n), [])

    ex_html = f"""<h2>✍️ Bài tập làm giấy (có lời giải)</h2>
{render_tuluan(tuluan_items)}
<h2>💬 Bài tập hỏi đáp nhanh</h2>
<p class="hint">Bấm vào từng câu hỏi để lật xem đáp án — ôn tập nhanh thuật ngữ &amp; khái niệm cốt lõi.</p>
{render_hoidap(hoidap_items)}"""

    quiz_items = json.dumps({"items": mod["quiz"]}, ensure_ascii=False)
    quiz_html = f"""<h2>✅ Trắc nghiệm nhanh (tự chấm)</h2>
<div class="quiz"><div class="quiz-root"></div>
<script type="application/json">{quiz_items}</script></div>"""

    sql_prefix = SQL_SANDBOX_FOR.get(mod["slug"])
    sql_html = ""
    if sql_prefix:
        sql_count = len(json.loads((ROOT / "data" / "sql" / f"questions_{sql_prefix}.json").read_text(encoding="utf-8")))
        sql_desc = SQL_DESC_FOR.get(mod["slug"], "Dữ liệu minh hoạ tự soạn (gắn nhãn rõ trong mã nguồn).")
        sql_html = f"""<h2>🖥️ SQL Sandbox — {sql_count} bài chạy thật (sql.js/SQLite, 100% trình duyệt)</h2>
<p class="hint">{sql_desc} Viết SQL vào ô bên dưới rồi bấm <b>Chạy thử</b>; bấm <b>Chấm điểm</b> để so với
lời giải mẫu đã chạy thật trên dữ liệu (không gõ tay đáp án).</p>
<div id="sb-mount-{sql_prefix}"></div>
<script src="{rel_root}_shared/sqlbank.js"></script>
<script>
SQLBank.init({{
  mount: "#sb-mount-{sql_prefix}",
  vendorUrl: "{rel_root}vendor/sql-wasm/",
  schemaUrl: "{rel_root}data/sql/schema_{sql_prefix}.sql",
  dataUrl: "{rel_root}data/sql/questions_{sql_prefix}.json",
  storageKey: "sqlbank:{mod['slug']}"
}});
</script>"""

    bank_prefix = MCQ_BANK_FOR.get(mod["slug"])
    bank_html = ""
    if bank_prefix:
        bank_count = len(json.loads((ROOT / "data" / "bank" / f"bank_{bank_prefix}.json").read_text(encoding="utf-8")))
        bank_html = f"""<h2>📚 Ngân hàng luyện tập sâu</h2>
<p class="hint">{bank_count} câu trắc nghiệm có nguồn gốc rõ ràng (gốc slide/giáo trình hoặc bổ sung — ghi rõ
từng câu), lọc theo chủ đề &amp; nguồn, chỉ xem câu đã sai, lưu tiến độ trên trình duyệt.</p>
<a class="mod-card" href="../{mod['slug']}/bank.html" style="display:block">
<span class="kicker">Luyện tập sâu</span><h3>Mở ngân hàng {bank_count} câu — {mod['title']}</h3>
<div class="go">Mở →</div></a>"""

    nav = '<div class="callout info" style="display:flex;justify-content:space-between;gap:10px">'
    nav += (f'<a href="../{prev_mod["slug"]}/index.html">◀ Buổi {prev_mod["n"]}: {prev_mod["title"]}</a>'
            if prev_mod else '<span></span>')
    nav += (f'<a href="../{next_mod["slug"]}/index.html">Buổi {next_mod["n"]}: {next_mod["title"]} ▶</a>'
            if next_mod else '<span></span>')
    nav += '</div>'

    body = f"""<div class="hero"><div class="kicker">Buổi {n:02d}</div>
<h1>{mod["title"]}</h1></div>
{deck}
{ex_html}
{sql_html}
{bank_html}
{quiz_html}
{nav}
"""
    html = page_shell(f"Buổi {n}: {mod['title']} · IT5427", rel_lang, rel_root, body)
    out = ROOT / "vi" / "modules" / mod["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out

REFERENCES = [
    ("Rahm, Bernstein — A survey of approaches to automatic schema matching", "VLDB Journal 2001"),
    ("Halevy, Franklin, Maier — Principles of dataspace systems", "PODS 2006"),
    ("Das Sarma, Dong, Halevy — Bootstrapping pay-as-you-go data integration systems", "SIGMOD 2008"),
    ("Cafarella, Halevy, Wang, Wu, Zhang — WebTables: exploring the power of tables on the web", "PVLDB 2008"),
    ("Talukdar, Jacob, Mehmood, Crammer, Ives, Pereira, Guha — Learning to create data-integrating queries", "PVLDB 2008"),
    ("Ullman — Information Integration Using Logical Views", "ICDT 1997 — bài gốc GAV/LAV"),
    ("Levy — Answering Queries Using Views: A Survey", "VLDB Journal 2001"),
    ("Lenzerini — Data Integration: A Theoretical Perspective", "PODS 2002 tutorial"),
    ("Dong, Srivastava — Big Data Integration", "PVLDB 2013 — bản mở hợp pháp của sách giáo trình chính thức môn học (Morgan & Claypool 2015, trả phí)"),
    ("Köpcke, Thor, Rahm — Evaluation of entity resolution approaches on real-world match problems", "PVLDB 2010"),
    ("Mudgal et al. — Deep Learning for Entity Matching (Magellan)", "SIGMOD 2018"),
    ("Hassanzadeh, Chiang, Miller, Lee — Framework for Evaluating Clustering Algorithms in Duplicate Detection", "PVLDB 2009"),
    ("Gruenheid, Dong, Srivastava — Incremental Record Linkage", "PVLDB 2014"),
    ("Burdick, Fagin, Kolaitis, Popa, Tan — Expressive Power of Entity-Linking Frameworks", "ICDT 2017"),
    ("Gionis, Indyk, Motwani — Similarity Search in High Dimensions via Hashing", "VLDB 1999 — bài gốc LSH"),
    ("Bansal, Blum, Chawla — Correlation Clustering", "Machine Learning 2004 — bài gốc Correlation Clustering"),
    ("Ebraheem, Thirumuruganathan, Joty, Ouzzani, Tang — Distributed Representations of Tuples for ER (DeepER)", "PVLDB 2018"),
    ("Kasai et al. — Low-resource Deep Entity Resolution with Transfer and Active Learning", "ACL 2019"),
    ("Fellegi, Sunter — A Theory for Record Linkage", "JASA 1969 — trả phí, xem tóm tắt trong slide buổi 4"),
]
TEXTBOOKS = [
    ("Xin Luna Dong, Divesh Srivastava — Big Data Integration", "Morgan & Claypool, 2015 — giáo trình chính thức #1. "
     "Chương 1 (Motivation) có bản free sample hợp pháp của tác giả; Ch.2 Schema Alignment, Ch.3 Record Linkage, "
     "Ch.4 Data Fusion khớp đúng pipeline 3 bước của môn — xem bản PVLDB 2013 mở tương đương ở mục bài báo dưới."),
    ("AnHai Doan, Alon Halevy, Zachary Ives — Principles of Data Integration", "Morgan Kaufmann, 2012 — giáo trình chính thức #2. "
     "Ch.3 §3.2 'Schema Mapping Languages' (GAV/LAV/GLAV/TGD) = cấu trúc chính xác của Module 02; "
     "Ch.4 'String Matching' + Ch.7 'Data Matching' = cấu trúc chính xác của Module 04. "
     "Không có mục Exercises cuối chương (chỉ Bibliographic Notes) — bài tập trên site đều tự soạn."),
    ("Rick Sherman — Business Intelligence Guidebook: From Data Integration to Analytics", "Morgan Kaufmann, 2015 — giáo trình chính thức #3"),
    ("Matei Zaharia, Bill Chambers — Spark: The Definitive Guide", "O'Reilly, 2018 — giáo trình chính thức #4 (phần Spark, buổi 6+)"),
]

def build_references_page():
    rel_lang = "../../"
    rel_root = "../../../"
    tb_lis = "\n".join(f"<li><b>{esc(t)}</b><br><span class='meta'>{esc(m)}</span></li>" for t, m in TEXTBOOKS)
    ref_lis = "\n".join(f"<li>{esc(t)} <span class='meta'>({esc(m)})</span></li>" for t, m in REFERENCES)
    body = f"""<div class="hero"><div class="kicker">Tài liệu tham khảo</div>
<h1>Giáo trình chính thức &amp; 19 bài báo khoa học đã xác minh</h1>
<p>Theo đề cương chính thức môn IT5427 (mục "Text and Reading"). Các sách dưới đây đều là tài liệu trả phí,
không có bản đầy đủ công khai hợp pháp — trang này chỉ liệt kê để tra cứu, KHÔNG đăng tải lại nội dung sách.</p></div>
<h2>📘 4 giáo trình chính thức</h2>
<ol class="reflist">{tb_lis}</ol>
<h2>📄 19 bài báo khoa học đã tải &amp; xác minh (pdftotext đối chiếu từng file)</h2>
<p class="hint">Danh sách đầy đủ + lý do chọn từng bài nằm trong <code>Literature-Review-Papers/README.md</code> của
repo nguồn (không public hoá PDF công khai trên site này, chỉ liệt kê trích dẫn — xem README để lấy link DOI/OA gốc).</p>
<ol class="reflist">{ref_lis}</ol>
"""
    html = page_shell("Tài liệu tham khảo · IT5427", rel_lang, rel_root, body)
    out = ROOT / "vi" / "modules" / "99-tai-lieu-tham-khao" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

def build_bank_page(mod):
    """Trang ngân hàng trắc nghiệm luyện tập sâu riêng cho 1 module (vi/modules/<slug>/bank.html)."""
    prefix = MCQ_BANK_FOR[mod["slug"]]
    rel_lang = "../../"
    rel_root = "../../../"
    body = f"""<div class="hero"><div class="kicker">Luyện tập sâu · Buổi {mod['n']:02d}</div>
<h1>Ngân hàng trắc nghiệm — {mod['title']}</h1>
<p>Mỗi câu ghi rõ nguồn (gốc slide/giáo trình hay bổ sung tự soạn), đáp án đã chấm &amp; giải thích ngay,
lưu tiến độ trên trình duyệt. Lọc theo chủ đề/nguồn, xem lại riêng các câu đã sai.</p></div>
<div id="bank-mount"></div>
<script src="{rel_root}_shared/bank.js"></script>
<script>
BankUI.init({{
  mount: "#bank-mount",
  dataUrl: "{rel_root}data/bank/bank_{prefix}.json",
  storageKey: "bank:{mod['slug']}"
}});
</script>
<div class="callout info" style="margin-top:18px">
<a href="index.html">◀ Về trang bài giảng Buổi {mod['n']}: {mod['title']}</a></div>
"""
    html = page_shell(f"Ngân hàng trắc nghiệm · Buổi {mod['n']} · IT5427", rel_lang, rel_root, body)
    out = ROOT / "vi" / "modules" / mod["slug"] / "bank.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

def build_index():
    rel_lang = ""
    rel_root = "../"
    cards = []
    for m in MODULES:
        cards.append(f"""<a class="mod-card" href="modules/{m['slug']}/index.html">
<span class="kicker">Buổi {m['n']:02d}</span>
<h3>{m['title']}</h3>
<span class="tag">{m['tag']}</span>
<div class="go">Mở bài giảng →</div></a>""")
    ref_card = """<a class="mod-card" href="modules/99-tai-lieu-tham-khao/index.html" style="border-color:var(--accent2)">
<span class="kicker">Tham khảo</span><h3>Giáo trình chính thức &amp; 19 bài báo khoa học</h3>
<span class="tag">Dong&amp;Srivastava · Doan-Halevy-Ives · Ullman · Lenzerini · Fellegi&amp;Sunter...</span>
<div class="go">Mở →</div></a>"""
    body = f"""<div class="hero">
<div class="kicker">Hệ thống tự học mở · Tiếng Việt</div>
<h1>IT5427 — Tích hợp và xử lý dữ liệu lớn</h1>
<p>HUST, giảng viên <b>Vũ Tuyết Trinh</b>. Bám sát 4 buổi slide đã học: Data Integration overview → Schema
Alignment &amp; Query Rewriting → Mediation Query (bán cấu trúc) &amp; Big Data challenges → Record Linkage
&amp; Entity Resolution. Mỗi buổi có slide-deck tương tác, bài tập làm giấy có lời giải, flashcard hỏi-đáp,
trắc nghiệm nhanh, <b>SQL Sandbox chạy thật</b> (sql.js/SQLite ngay trên trình duyệt, không cần cài gì), và
<b>ngân hàng luyện tập sâu</b> (40-96 câu/buổi, lọc theo chủ đề/nguồn).</p>
</div>
<div class="callout good"><div class="lbl">Cách dùng</div>
Học theo đúng thứ tự Buổi 00 (nền tảng, không bắt buộc) → 01 → 02 → 03 → 04. Mỗi buổi: đọc slide-deck (phím
← →) → làm bài tập làm giấy (có lời giải để tự đối chiếu) → ôn flashcard hỏi-đáp → luyện SQL Sandbox → làm
trắc nghiệm nhanh → vào ngân hàng luyện tập sâu để ôn kỹ hơn.</div>
<div class="callout warn"><div class="lbl">Phạm vi</div>
Site hiện bám đúng 4 buổi slide đã có (buổi 2-4 trong đề cương chính thức, cộng buổi 00 tự bổ sung). Đề cương
còn 5 buổi tiếp theo (Sources Profiling, Approximate Query Processing, Batch vs Streaming, Governance/
Provenance/Schema Drift, Project) — <b>chưa có slide nên chưa có module tương ứng</b>.</div>
<h2>5 buổi học</h2>
<div class="grid">{''.join(cards)}</div>
<h2>Tài liệu bổ sung</h2>
<div class="grid">{ref_card}</div>
"""
    html = page_shell("IT5427 — Tích hợp và xử lý dữ liệu lớn", rel_lang, rel_root, body)
    (ROOT / "vi" / "index.html").write_text(html, encoding="utf-8")

def build_root_redirect():
    html = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=vi/index.html">
<title>IT5427 - Tích hợp và xử lý dữ liệu lớn</title></head>
<body><p>Đang chuyển hướng… <a href="vi/index.html">Bấm vào đây nếu không tự chuyển</a>.</p></body></html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")

if __name__ == "__main__":
    build_references_page()
    for i, m in enumerate(MODULES):
        prev_mod = MODULES[i-1] if i > 0 else None
        next_mod = MODULES[i+1] if i < len(MODULES)-1 else None
        build_module_page(m, prev_mod, next_mod)
        if m["slug"] in MCQ_BANK_FOR:
            build_bank_page(m)
    build_index()
    build_root_redirect()
    print("Đã sinh", len(MODULES), "module + 1 trang tài liệu tham khảo + index")
