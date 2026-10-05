# -*- coding: utf-8 -*-
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from modules_content import MODULES
from quiz_extra import EXTRA_QUIZ

for _m in MODULES:
    _m["quiz"] = _m["quiz"] + EXTRA_QUIZ.get(_m["n"], [])

ROOT = pathlib.Path(__file__).parent.parent
EX = json.loads((pathlib.Path(__file__).parent / "exercises.json").read_text(encoding="utf-8"))

HEAD_THEME_SCRIPT = """<script>(function(){try{
  var t = localStorage.getItem('site-theme');
  if (t && t !== 'light') document.documentElement.setAttribute('data-theme', t);
}catch(e){}})();</script>"""

KATEX = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script>
window.KATEX_MACROS = {
  "\\\\E": "\\\\mathbb{E}", "\\\\Prob": "\\\\mathbb{P}", "\\\\R": "\\\\mathbb{R}", "\\\\F": "\\\\mathbb{F}",
  "\\\\Var": "\\\\operatorname{Var}", "\\\\eps": "\\\\varepsilon",
  "\\\\norm": "\\\\left\\\\lVert #1 \\\\right\\\\rVert", "\\\\ip": "\\\\left\\\\langle #1, #2 \\\\right\\\\rangle"
};
window.KATEX_DELIMS = [{left:'$$', right:'$$', display:true},{left:'$', right:'$', display:false}];
</script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:window.KATEX_DELIMS, macros:window.KATEX_MACROS, throwOnError:false});"></script>"""

def topbar(rel_lang):
    """rel_lang: đường dẫn tương đối để về vi/ (thư mục ngôn ngữ), dùng cho index.html và modules/."""
    return f"""<div class="topbar">
  <a class="brand" href="{rel_lang}index.html">Lưu trữ &amp; xử lý <span>dữ liệu lớn</span></a>
  <nav>
    <a href="{rel_lang}index.html">Trang chủ</a>
    <a href="{rel_lang}modules/00-slide-goc/index.html">Bài tập trên slide gốc</a>
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
    """rel_root: đường dẫn tương đối về gốc site (nơi có _shared/, data/, assets/)."""
    return f"""<footer>
  <div class="wrap">Hệ thống tự học &quot;Lưu trữ &amp; xử lý dữ liệu lớn&quot; · dựng từ giáo trình Sketching
  Algorithms (Jelani Nelson) và bộ 580 bài tập tự soạn. Không backend, chạy hoàn toàn phía trình duyệt.</div>
</footer>
<button class="fab" data-open-info title="Thông tin">ℹ️</button>
<div id="info-modal" hidden><div class="box">
  <button class="close">✕</button>
  <h3>Về trang này</h3>
  <p>Hệ thống tự học mở, xây từ giáo trình <i>Sketching Algorithms</i> (Jelani Nelson) và lộ trình 14 buổi
  tự học môn Lưu trữ &amp; xử lý dữ liệu lớn. Toàn bộ nội dung, bài tập, quiz chạy tĩnh, không cần server.</p>
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
<script src="{rel_root}_shared/algo.js"></script>
<script src="{rel_root}_shared/deck.js"></script>
<script src="{rel_root}_shared/quiz.js"></script>
<script src="{rel_root}_shared/sim.js"></script>
{extra_script}
</body></html>"""

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def render_exlist(title, items, note=""):
    if not items:
        return ""
    lis = "\n".join(f"<li>{esc(it).replace(chr(10), '<br>')}</li>" for it in items)
    return f"""<details class="ex"><summary>{title} ({len(items)} bài){' — ' + note if note else ''}</summary>
<ol class="exlist">{lis}</ol></details>"""

def slide_html(s, extra_img=""):
    img = f'<p><img src="{extra_img}" alt="Sơ đồ minh hoạ" style="border:1px solid var(--border);border-radius:10px"></p>' if extra_img else ""
    return f'<div class="mdeck-slide"><h2>{s["h"]}</h2>{s["body"]}{img}</div>'

def part_divider(idx, total_parts, part):
    lis = "\n".join(f"<li>{b}</li>" for b in part["bullets"])
    return f"""<div class="mdeck-slide part-divider"><div class="kicker">PHẦN {idx}/{total_parts}</div>
<div class="part-num">{idx:02d}</div><h2>{part["title"]}</h2>
<ul class="part-list">{lis}</ul></div>"""

# slug module -> (index slide trong part cuối cùng để chèn ảnh, tên file svg)
DIAGRAM_FOR = {
    "09-ma-tran-sketch": "sketch-matrix.svg",
    "11-ham-bam": "countmin-hash.svg",
    "12-cay-nhi-phan": "dyadic-tree.svg",
    "13-do-thi-boruvka": "boruvka-rounds.svg",
}

# slug module -> tên widget trong sim.js (data-sim="...")
SIM_FOR = {
    "01-ky-vong": "morris",
    "02-markov": "markov",
    "03-chebyshev": "chebyshev",
    "04-chernoff": "chernoff",
    "05-hoeffding-union": "unionbound",
    "06-quy-nap": "induction",
    "07-tail-taylor": "fm",
    "08-vector-chuan": "vectornorm",
    "09-ma-tran-sketch": "sketchmatrix",
    "10-rademacher-khintchine": "ams",
    "11-ham-bam": "countmin",
    "12-cay-nhi-phan": "rank",
    "13-do-thi-boruvka": "boruvka",
    "14-truong-huu-han": "schwartzzippel",
}

def build_module_page(mod, prev_mod, next_mod):
    rel_lang = "../../"      # vi/modules/<slug>/index.html -> vi/
    rel_root = "../../../"   # vi/modules/<slug>/index.html -> site root
    diagram = DIAGRAM_FOR.get(mod["slug"])
    slides = [f'<div class="mdeck-slide"><div class="kicker">BUỔI {mod["n"]:02d} · {mod["tag"]}</div>'
              f'<h2>{mod["title"]}</h2><p>{mod["intro"]}</p></div>']
    total_parts = len(mod["parts"])
    for pi, part in enumerate(mod["parts"], 1):
        slides.append(part_divider(pi, total_parts, part))
        last_part = (pi == total_parts)
        n_slides = len(part["slides"])
        for si, s in enumerate(part["slides"]):
            is_last_slide_of_deck = last_part and (si == n_slides - 1)
            img = f"{rel_root}assets/diagrams/{diagram}" if (diagram and is_last_slide_of_deck) else ""
            slides.append(slide_html(s, img))
    deck = f"""<div class="mdeck"><div class="mdeck-viewport">{''.join(slides)}</div>
<div class="mdeck-bar">
  <button class="mdeck-prev">◀ Trước</button><button class="mdeck-next">Sau ▶</button>
  <span class="mdeck-count"></span><div class="mdeck-dots"></div>
  <button class="mdeck-fs">⛶ Toàn màn hình</button>
</div></div>"""

    n = mod["n"]
    sim_name = SIM_FOR.get(mod["slug"])
    sim_html = (f'<h2>🧪 Thực hành tương tác</h2>\n'
                f'<div class="sim" data-sim="{sim_name}"></div>') if sim_name else ""

    ex_html = "\n".join([
        render_exlist("📗 Bài tập nền tảng — Phần 1 (toán/xác suất, tổng quát hoá + kiểm chứng code)", EX["phan1"].get(str(n), [])),
        render_exlist("🐍 Bài tập nền tảng — Phần 2 (thuật toán/mã giả Python)", EX["phan2"].get(str(n), [])),
        render_exlist("✍️ Bài tập tự luận mức vừa (chứng minh)", EX["tuluan"].get(str(n), [])),
    ])

    quiz_items = json.dumps({"items": mod["quiz"]}, ensure_ascii=False)
    quiz_html = f"""<h2>✅ Quiz tự kiểm tra</h2>
<div class="quiz"><div class="quiz-root"></div>
<script type="application/json">{quiz_items}</script></div>"""

    nb_link = (f'<p><a href="{rel_root}data/notebooks/modules/{n:02d}_{mod["slug"]}.ipynb" download>'
               f'⬇️ Tải notebook Python buổi {n} (.ipynb)</a> — chứa 10 bài thực hành code từ Phần 2, '
               f'mở bằng Jupyter/Colab. &nbsp;·&nbsp; '
               f'<a href="{rel_root}data/source/notes.pdf" target="_blank">📄 Lecture Notes gốc (PDF)</a> &nbsp;·&nbsp; '
               f'<a href="{rel_root}data/source/streaming-algorithms-vi.pdf" target="_blank">📄 Slide bài giảng gốc (PDF)</a></p>')

    nav = '<div class="callout info" style="display:flex;justify-content:space-between;gap:10px">'
    nav += (f'<a href="../{prev_mod["slug"]}/index.html">◀ Buổi {prev_mod["n"]}: {prev_mod["title"]}</a>'
            if prev_mod else '<span></span>')
    nav += (f'<a href="../{next_mod["slug"]}/index.html">Buổi {next_mod["n"]}: {next_mod["title"]} ▶</a>'
            if next_mod else '<span></span>')
    nav += '</div>'

    body = f"""<div class="hero"><div class="kicker">Buổi {n:02d} / 14</div>
<h1>{mod["title"]}</h1></div>
{deck}
{sim_html}
<h2>📚 Bài tập gắn với buổi này</h2>
{ex_html}
{nb_link}
{quiz_html}
{nav}
"""
    html = page_shell(f"Buổi {n}: {mod['title']} · Lưu trữ & xử lý dữ liệu lớn", rel_lang, rel_root, body)
    out = ROOT / "vi" / "modules" / mod["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out

def build_slide_ref_page():
    rel_lang = "../../"
    rel_root = "../../../"
    items = EX["slide"]
    lis = "\n".join(f"<li>{esc(it)}</li>" for it in items)
    body = f"""<div class="hero"><div class="kicker">Tài liệu bổ sung</div>
<h1>20 bài tập áp dụng trực tiếp lên slide gốc</h1>
<p>Slide gốc <i>streaming-algorithms-vi.pdf</i> trình bày lần lượt: Morris → F0 (FM/KMV/lấy mẫu hình học) →
Quantiles (q-digest/MRL/KLL) → Linear sketching (CountMin/CountSketch) → Graph sketching (AGM/SupportFind) →
Norm estimation (AMS/p-stable). 20 bài dưới đây yêu cầu chứng minh lại từng bổ đề cốt lõi của slide, có ghi
rõ số trang tham chiếu.</p></div>
<details class="ex" open><summary>20 bài (đủ 6 chủ đề của slide)</summary><ol class="exlist">{lis}</ol></details>
<div class="callout good"><div class="lbl">Cách dùng</div>Làm sau khi đã hoàn thành 14 buổi module — đây là
bài tập tổng hợp áp dụng trực tiếp lên đúng thứ tự trình bày của slide gốc, không phải bài tập nền tảng.</div>
"""
    html = page_shell("Bài tập trên slide gốc · Lưu trữ & xử lý dữ liệu lớn", rel_lang, rel_root, body)
    out = ROOT / "vi" / "modules" / "00-slide-goc" / "index.html"
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
    slide_card = """<a class="mod-card" href="modules/00-slide-goc/index.html" style="border-color:var(--accent2)">
<span class="kicker">Bổ sung</span><h3>20 bài áp dụng trực tiếp lên slide gốc</h3>
<span class="tag">Morris · FM · KMV · CountMin · AGM · AMS</span>
<div class="go">Mở →</div></a>"""
    notes_card = """<a class="mod-card" href="../data/source/notes.pdf" target="_blank" style="border-color:var(--good)">
<span class="kicker">Tài liệu nguồn gốc</span><h3>Lecture Notes — Sketching Algorithms (Jelani Nelson, PDF)</h3>
<span class="tag">127 trang · nguồn chính của toàn bộ site</span>
<div class="go">Mở / tải PDF →</div></a>"""
    slide_pdf_card = """<a class="mod-card" href="../data/source/streaming-algorithms-vi.pdf" target="_blank" style="border-color:var(--good)">
<span class="kicker">Tài liệu nguồn gốc</span><h3>Slide bài giảng gốc — Thuật toán trên luồng dữ liệu (PDF, tiếng Việt)</h3>
<span class="tag">67 trang · dùng để soạn 20 bài "áp dụng slide gốc"</span>
<div class="go">Mở / tải PDF →</div></a>"""
    group1_card = """<a class="mod-card" href="group-1-slides.html" style="border-color:var(--accent2)">
<span class="kicker">Bài tập lớn · Nhóm 1</span><h3>Hệ sinh thái Hadoop (Chương 2)</h3>
<span class="tag">48 slide · Trương Tuấn Nghĩa, Nguyễn Vũ Việt Hoàng, Nguyễn Thế Hoàng</span>
<div class="go">Mở slide thuyết trình →</div></a>"""
    body = f"""<div class="hero">
<div class="kicker">Hệ thống tự học mở · Tiếng Việt</div>
<h1>Lưu trữ &amp; xử lý dữ liệu lớn</h1>
<p>Streaming &amp; Sketching Algorithms — 14 buổi tự học bám sát giáo trình <i>Sketching Algorithms</i>
(Jelani Nelson), tích hợp trọn bộ 580 bài tập đã soạn (420 nền tảng có kiểm chứng bằng code Python + 140
bài tự luận + 20 bài áp dụng slide gốc). Mỗi buổi có slide-deck tương tác, <b>demo mô phỏng thuật toán chạy
thật trên trình duyệt</b>, 15–25 câu quiz tự chấm, và notebook Python.</p>
</div>
<div class="callout good"><div class="lbl">Cách dùng lộ trình 2 tuần / 14 buổi</div>
Mỗi ngày học đúng 1 buổi: đọc slide-deck (điều hướng bằng phím ← →) → bấm thử mục <b>🧪 Thực hành tương
tác</b> (chạy thật thuật toán của buổi đó ngay trên trang, không cần cài gì) → mở accordion bài tập, làm 20
bài nền tảng rồi 10 bài Python rồi 10 bài tự luận → làm quiz tự kiểm tra → tải notebook để chạy thử code.
Sau khi xong cả 14 buổi, làm 20 bài tổng hợp áp dụng trực tiếp lên slide gốc.</div>
<div class="callout info"><div class="lbl">🧪 14 demo tương tác (mỗi buổi 1 demo, chạy thật phía trình duyệt)</div>
Morris counter trực tiếp · kiểm chứng Markov trên dữ liệu ngẫu nhiên · Chebyshev + KMV đếm phần tử phân biệt
· so sánh nhị thức chính xác với chặn Chernoff · union bound tính số hàng CountMin · kiểm chứng quy nạp
$\mathbb E[2^{{X_n}}]=n+1$ bằng thực nghiệm · FM lý tưởng hoá (và vì sao trung bình cộng gây hiểu lầm) ·
máy tính $F_0,F_1,F_2$ từ 1 luồng · sketch tuyến tính streaming vs tính lại từ đầu · AMS ước lượng $F_2$ ·
CountMin sketch thật xây từ luồng dữ liệu · rank/quantile trên mảng · Borůvka chạy từng vòng · kiểm chứng
Schwartz–Zippel bằng Monte Carlo.</div>
<h2>14 buổi học</h2>
<div class="grid">{''.join(cards)}</div>
<h2>Tài liệu bổ sung</h2>
<div class="grid">{notes_card}{slide_pdf_card}{slide_card}</div>
<h2>Bài tập lớn môn học (ngoài 14 buổi tự học)</h2>
<div class="grid">{group1_card}</div>
"""
    # index.html nằm trực tiếp trong vi/ -> rel_root phải là "../"
    html = page_shell("Lưu trữ & xử lý dữ liệu lớn — Streaming & Sketching Algorithms", rel_lang, rel_root, body)
    (ROOT / "vi" / "index.html").write_text(html, encoding="utf-8")

def build_root_redirect():
    html = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=vi/index.html">
<title>Lưu trữ & xử lý dữ liệu lớn</title></head>
<body><p>Đang chuyển hướng… <a href="vi/index.html">Bấm vào đây nếu không tự chuyển</a>.</p></body></html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")

if __name__ == "__main__":
    build_slide_ref_page()
    for i, m in enumerate(MODULES):
        prev_mod = MODULES[i-1] if i > 0 else None
        next_mod = MODULES[i+1] if i < len(MODULES)-1 else None
        build_module_page(m, prev_mod, next_mod)
    build_index()
    build_root_redirect()
    print("Đã sinh", len(MODULES), "module + 1 trang slide-ref + index")
