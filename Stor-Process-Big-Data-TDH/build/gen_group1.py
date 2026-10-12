# -*- coding: utf-8 -*-
"""Sinh slide thuyết trình bài tập lớn Nhóm 1, Chương 2, Hệ sinh thái Hadoop.
Nội dung bám sát IT4931_lecture_notes.pdf (Chương 2, tr.23-36, nhóm tác giả Trần Văn Đặng,
Nguyễn Hữu Đức, Nguyễn Bình Minh, Trần Việt Trung, Đại học Bách Khoa Hà Nội), không bịa thêm
sự kiện hay số liệu ngoài những gì sách nêu. Định dạng theo mẫu lap_lich_50_slides.pdf."""
import pathlib, sys, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen_site import HEAD_THEME_SCRIPT, KATEX, topbar, footer

ROOT = pathlib.Path(__file__).parent.parent

MEMBERS = ["Trương Tuấn Nghĩa (20251196M)", "Nguyễn Vũ Việt Hoàng (20252091M)", "Nguyễn Thế Hoàng (20251228M)"]

def slide(title, body, kicker=None):
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    return f'<div class="mdeck-slide">{k}<h2>{title}</h2>{body}</div>'

def divider(idx, total, title, bullets):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return f"""<div class="mdeck-slide part-divider"><div class="kicker">PHẦN {idx}/{total}</div>
<div class="part-num">{idx:02d}</div><h2>{title}</h2><ul class="part-list">{lis}</ul></div>"""

def tbl(head, rows, dense=False):
    h = "".join(f"<th>{x}</th>" for x in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    cls = ' class="dense"' if dense else ""
    return f'<table{cls}><tr>{h}</tr>{r}</table>'

def formula(label, math):
    return f'<div class="pd-formula"><div class="pd-formula-label">{label}</div><div class="pd-formula-math">${math}$</div></div>'

def callout(kind, label, text):
    return f'<div class="callout {kind}"><div class="lbl">{label}</div>{text}</div>'

def logo_img(f, h=40):
    return f'<img src="../assets/images/logos/{f}" alt="" style="height:{h}px;max-width:150px;width:auto;object-fit:contain;vertical-align:middle;background:#fff;border-radius:6px;padding:3px 6px;border:1px solid var(--border)">'

def tech_timeline_svg():
    """Timeline nhiều lane tự vẽ bằng SVG gốc. Đường nét đứt = ý tưởng/ảnh hưởng (bài báo → công nghệ);
    đường liền = phụ thuộc lúc chạy (chạy trên Hadoop, dùng ZooKeeper, nạp dữ liệu vào Hadoop)."""
    y0, y1 = 2002, 2013
    ml, step = 150, 64
    def X(year): return ml + (year - y0) * step
    W = X(y1) + 150
    H = 470
    lanes = [
        {"label": "Nghiên cứu<br/>nền tảng (Google)", "y": 72, "color": "#2b5ce6"},
        {"label": "Lõi Hadoop", "y": 168, "color": "#0f9d58"},
        {"label": "Streaming", "y": 264, "color": "#c2255c"},
        {"label": "Công cụ<br/>hệ sinh thái", "y": 360, "color": "#d98e00"},
    ]
    # (lane, năm, tên, mô tả, key, dx, hướng nhãn, căn nhãn, lệch nhãn)
    nodes = {
        "GFS": (0, 2003, "GFS", "SOSP 2003", True, 0, "u", "r", 0),
        "MR": (0, 2004, "MapReduce", "OSDI 2004", True, 0, "u", "c", 0),
        "BT": (0, 2006, "Bigtable", "OSDI 2006", True, -8, "u", "r", 0),
        "CH": (0, 2006, "Chubby", "OSDI 2006", False, 8, "u", "l", 0),
        "HD": (1, 2006, "Hadoop", "Tách từ Nutch<br/>(Cutting, Yahoo!)", True, 0, "d", "r", 0),
        "YARN": (1, 2012, "YARN", "Hadoop 2.0: tách<br/>quản lý tài nguyên", True, 0, "u", "c", 0),
        "KF": (2, 2011.1, "Kafka", "Mã nguồn mở (LinkedIn)", True, 0, "u", "l", 14),
        "KR": (2, 2013.2, "KRaft", "2022: Kafka bỏ<br/>ZooKeeper", False, 0, "d", "c", 0),
        "ZK": (3, 2007, "ZooKeeper", "Yahoo Research", False, 0, "d", "c", 0),
        "HB": (3, 2008.25, "HBase", "28/3/2008<br/>(Powerset)", True, 0, "d", "c", 0),
        "PIG": (3, 2008.75, "Pig", "9/2008 (Yahoo)", False, 0, "u", "l", 8),
        "HIVE": (3, 2010.8, "Hive", "10/2010 (Facebook)", True, 0, "u", "l", 8),
        "OZ": (3, 2012.3, "Oozie", "Top-level 2012", False, 0, "d", "c", 0),
    }
    def pos(k):
        n = nodes[k]; return X(n[1]) + n[5], lanes[n[0]]["y"]
    # (từ, đến, kiểu, màu, chú thích ngắn)
    GR = "#7a8499"
    links = [
        ("GFS", "HD", "dash", GR), ("MR", "HD", "dash", GR), ("BT", "HB", "dash", GR), ("CH", "ZK", "dash", GR),
        ("HD", "YARN", "solid", "#0f9d58"),
        ("HD", "HB", "solid", "#0f9d58"), ("HD", "PIG", "solid", "#0f9d58"),
        ("HD", "HIVE", "solid", "#0f9d58"), ("HD", "OZ", "solid", "#0f9d58"),
        ("ZK", "KF", "solid", "#c2255c"), ("ZK", "HB", "solid", "#d98e00"),
    ]
    svg = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Timeline phát triển hệ sinh thái Hadoop">']
    cols = sorted({c for _, _, _, c in links} | {"#c2255c"})
    svg.append("<defs>" + "".join(
        f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in cols) + "</defs>")
    yr = y0
    while yr < y1:
        x = X(yr)
        svg.append(f'<line x1="{x}" y1="36" x2="{x}" y2="410" stroke="var(--border)" stroke-width="1"/>')
        svg.append(f'<text x="{x}" y="440" font-size="13" fill="var(--muted)" text-anchor="middle">{yr}</text>')
        yr += 1
    xb = X(2013.2)
    svg.append(f'<text x="{xb}" y="440" font-size="13" fill="var(--muted)" text-anchor="middle">⋯ 2022</text>')
    for ln in lanes:
        svg.append(f'<line x1="{ml-20}" y1="{ln["y"]}" x2="{xb+30}" y2="{ln["y"]}" stroke="{ln["color"]}" stroke-width="2.5" opacity=".5"/>')
        svg.append(f'<foreignObject x="0" y="{ln["y"]-24}" width="{ml-30}" height="48">'
                   f'<div xmlns="http://www.w3.org/1999/xhtml" style="font:700 14px sans-serif;color:{ln["color"]};'
                   f'text-align:right;line-height:1.25;height:48px;display:flex;align-items:center;justify-content:flex-end">'
                   f'<span>{ln["label"]}</span></div></foreignObject>')
    import math
    def shorten(a, b, r=11):
        dx, dy = b[0]-a[0], b[1]-a[1]; d = math.hypot(dx, dy) or 1
        return (a[0]+dx/d*r, a[1]+dy/d*r), (b[0]-dx/d*(r+2), b[1]-dy/d*(r+2))
    for a, b, kind, col in links:
        pa, pb = shorten(pos(a), pos(b))
        dash = ' stroke-dasharray="5,4"' if kind == "dash" else ""
        svg.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="{col}" '
                   f'stroke-width="{1.4 if kind=="dash" else 1.8}"{dash} opacity=".85" marker-end="url(#ah{col[1:]})"/>')
    # Kafka nạp dữ liệu vào HDFS: mũi tên lên tới lane Hadoop
    kx, ky = pos("KF"); hy = lanes[1]["y"]
    svg.append(f'<line x1="{kx}" y1="{ky-11}" x2="{kx}" y2="{hy+10}" stroke="#c2255c" stroke-width="1.8" marker-end="url(#ah{"c2255c"})"/>')
    svg.append(f'<rect x="{kx-5}" y="{hy-5}" width="10" height="10" transform="rotate(45 {kx} {hy})" fill="var(--panel)" stroke="#0f9d58" stroke-width="2"/>')
    svg.append(f'<foreignObject x="{kx-150}" y="{hy+18}" width="144" height="40"><div xmlns="http://www.w3.org/1999/xhtml" '
               f'style="font:600 11.5px sans-serif;color:#c2255c;text-align:right;line-height:1.2">nạp dữ liệu<br/>vào HDFS</div></foreignObject>')
    for k, (lane_i, year, name, sub, key, dx, side, al, lx) in nodes.items():
        ln = lanes[lane_i]; x = X(year) + dx; y = ln["y"]
        svg.append(f'<circle cx="{x}" cy="{y}" r="{8 if key else 6}" fill="{ln["color"]}" stroke="var(--panel)" stroke-width="2"/>')
        bw = 150
        bx = {"c": x - bw/2, "l": x - 6 + lx, "r": x - bw + 6}[al]
        ta = {"c": "center", "l": "left", "r": "right"}[al]
        ai = {"c": "center", "l": "flex-start", "r": "flex-end"}[al]
        by, just = (y - 12 - 52, "flex-end") if side == "u" else (y + 12, "flex-start")
        svg.append(f'<foreignObject x="{bx}" y="{by}" width="{bw}" height="52">'
                   f'<div xmlns="http://www.w3.org/1999/xhtml" style="height:52px;display:flex;flex-direction:column;'
                   f'justify-content:{just};align-items:{ai};text-align:{ta};font-family:sans-serif">'
                   f'<div style="background:color-mix(in srgb,var(--panel) 90%,transparent);padding:0 3px;border-radius:3px">'
                   f'<div style="font-weight:{"800" if key else "700"};font-size:{"15" if key else "13.5"}px;color:var(--text);line-height:1.15">{name}</div>'
                   f'<div style="font-size:11.5px;color:var(--muted);line-height:1.2">{sub}</div></div></div></foreignObject>')
    svg.append('</svg>')
    return "".join(svg)

def imgs_slide(title, items, body_after="", gap=18, maxh=None):
    """Slide gồm nhiều ảnh cắt từ bài báo xếp ngang, mỗi ảnh có chú thích nguồn; items = [(file, caption, flex)]."""
    cells = "".join(
        f'<figure style="margin:0;flex:{fl}"><img src="../assets/images/papers/{f}" alt="" style="width:100%;height:auto;{('max-height:'+str(maxh)+'px;width:auto;max-width:100%;') if maxh else ''}'
        f'border:1px solid var(--border);border-radius:8px;background:#fff"><figcaption style="font-size:.76rem;'
        f'color:var(--muted);margin-top:4px">{cap}</figcaption></figure>' for f, cap, fl in items)
    return slide(title, f'<div style="display:flex;gap:{gap}px;align-items:flex-start;justify-content:center">{cells}</div>{body_after}')

def figslide(title, img, src, rows, side=True, img_w="56%"):
    """Slide hình gốc từ bài báo nền tảng (crop nguyên trạng, ghi nguồn) + bảng đối chiếu sang thuật ngữ Hadoop."""
    im = (f'<figure style="margin:0"><img src="../assets/images/papers/{img}" alt="{title}" '
          f'style="width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff">'
          f'<figcaption style="font-size:.78rem;color:var(--muted);margin-top:4px">{src}</figcaption></figure>')
    tb = tbl(["Trong bài báo gốc", "Trong hệ sinh thái Hadoop"], rows, dense=True)
    if side:
        return slide(title, f'<div style="display:flex;gap:22px;align-items:flex-start"><div style="flex:0 0 {img_w}">{im}</div><div style="flex:1">{tb}</div></div>')
    return slide(title, f'<div style="max-width:{img_w};margin:0 auto 12px">{im}</div>{tb}')

def tblock(header, items):
    """Khối kết quả dạng bảng-số có thanh tiêu đề màu, mô phỏng đúng kiểu block thuật toán/định lý
    trong slide Beamer của thầy Tạ Duy Hoàng (thanh màu + danh sách đánh số bên trong khung viền)."""
    lis = "".join(f"<li>{x}</li>" for x in items)
    return f'<div class="tblock"><div class="tblock-h">{header}</div><ol>{lis}</ol></div>'

SLIDES = []

# ---------- Title ----------
SLIDES.append(f"""<div class="mdeck-slide"><div class="kicker">IT4931: Lưu trữ &amp; xử lý dữ liệu lớn · Bài tập lớn</div>
<h2>Hệ sinh thái Hadoop</h2>
<p style="font-size:1.05rem;color:var(--muted)">Chương 2: Lưu trữ và Xử lý Dữ liệu Lớn (Trần Văn Đặng, Nguyễn Hữu Đức, Nguyễn Bình Minh, Trần Việt Trung, ĐH Bách Khoa Hà Nội)</p>
<p><b>Nhóm 1</b> · {" · ".join(MEMBERS)}</p>
<p style="color:var(--muted);font-size:.9rem">Giảng viên: Tạ Duy Hoàng &nbsp;·&nbsp; Bài giảng chuyên đề &nbsp;·&nbsp; __SLIDE_COUNT__ slide</p></div>""")

# ---------- Overview ----------
SLIDES.append(slide("Nội dung &amp; mục tiêu trình bày",
    tbl(["Nội dung", "Sau phần trình bày, lớp có thể"],
        [["Tổng quan Hadoop", "Giải thích vì sao Hadoop ra đời, kiến trúc scale-out"],
         ["HDFS", "Mô tả kiến trúc NameNode/DataNode, cơ chế nhân bản"],
         ["MapReduce &amp; YARN", "Phân biệt vai trò 2 thành phần, kiến trúc YARN"],
         ["Hive, Pig", "So sánh 2 cách trừu tượng hoá MapReduce"],
         ["HBase, Sqoop", "Nêu use-case NoSQL thời gian thực &amp; ETL với RDBMS"],
         ["Kafka, Oozie, ZooKeeper", "Giải thích vai trò streaming, điều phối workflow, coordination"]])
    + '<p style="margin-top:10px;color:var(--muted);font-size:.88rem">Nguồn duy nhất: Chương 2 giáo trình môn học, tr.23–36.</p>',
    "Mục tiêu học tập"))

# ===================== PHẦN 1 =====================
SLIDES.append(divider(1, 8, "Lý do ra đời của Hadoop", [
    "Bài toán: dữ liệu vượt quá khả năng 1 máy", "Apache Hadoop: nền tảng mã nguồn mở, kiến trúc scale-out",
    "Nguồn gốc: Google File System &amp; MapReduce", "4 thành phần cốt lõi"]))

SLIDES.append(slide("Tổng quan Apache Hadoop", f"""
<p>Nền tảng mã nguồn mở được thiết kế để <b>lưu trữ và xử lý khối lượng dữ liệu lớn trên cụm máy tính</b>: cung cấp khả năng lưu trữ <i>scalable</i> (mở rộng được) và <i>reliable</i> (tin cậy), hỗ trợ xử lý song song
trên phần cứng thông dụng (commodity hardware).</p>
{callout('good','Kiến trúc scale-out', 'Mở rộng bằng cách <b>thêm máy</b> thay vì nâng cấp 1 máy duy nhất: cho phép mở rộng cụm lên hàng chục nghìn node.')}
{callout('warn','Triết lý chịu lỗi', 'Hỏng hóc phần cứng được xem là <b>điều bình thường</b>, không phải ngoại lệ: hệ thống tự động phát hiện lỗi, nhân bản dữ liệu và chuyển tác vụ sang node khác.')}
"""))

SLIDES.append(slide("Nguồn gốc: 2 bài báo của Google", f"""
<p>Hadoop phát triển dựa trên nghiên cứu của Google về hệ thống phân tán:</p>
{tbl(['Bài báo gốc','Google','Trở thành trong Hadoop'],
     [['Google File System (GFS)','Hệ thống tập tin phân tán','HDFS'],
      ['MapReduce (2004)','Mô hình lập trình song song','Hadoop MapReduce']])}
<p><b>Mục tiêu chính:</b> giải quyết bài toán lưu trữ và xử lý dữ liệu lớn trong môi trường phân tán, trên phần cứng rẻ tiền thay vì thiết bị chuyên dụng đắt tiền.</p>
"""))

SLIDES.append(slide("Bốn thành phần cốt lõi của Hadoop", tbl(
    ["Thành phần", "Vai trò"],
    [["<b>HDFS</b> (Hadoop Distributed File System)", "Lưu trữ dữ liệu dung lượng lớn trên cụm máy tính"],
     ["<b>Hadoop MapReduce</b>", "Mô hình lập trình phân tán xử lý dữ liệu lớn kiểu batch"],
     ["<b>Hadoop YARN</b> (Yet Another Resource Negotiator)", "Quản lý tài nguyên &amp; lập lịch tác vụ, cho nhiều ứng dụng chạy đồng thời"],
     ["<b>Hadoop Common</b>", "Bộ thư viện &amp; tiện ích chung hỗ trợ các module khác"]]
) + callout('info', 'Phối hợp', 'HDFS đảm bảo lưu trữ tin cậy · MapReduce cung cấp mô hình lập trình đơn giản · YARN điều phối hiệu quả tài nguyên: kết hợp giúp xử lý dữ liệu khổng lồ với chi phí hợp lý.')))

SLIDES.append(slide("Scale-out so với Scale-up", tbl(
    ["Tiêu chí", "Scale-up (truyền thống)", "Scale-out (Hadoop)"],
    [["Cách mở rộng", "Nâng cấp 1 máy chủ (thêm CPU/RAM đắt tiền)", "Thêm nhiều máy chủ rẻ tiền vào cụm"],
     ["Giới hạn mở rộng", "Bị chặn bởi phần cứng cao cấp nhất hiện có", "Mở rộng tới hàng chục nghìn node"],
     ["Xử lý lỗi", "1 máy hỏng = toàn hệ thống dừng", "Lỗi node là bình thường, tự động nhân bản &amp; chuyển tác vụ"],
     ["Chi phí", "Tăng phi tuyến khi nâng cấp máy đơn", "Tăng gần tuyến tính khi thêm node thông dụng"]]
) + callout('good', 'Vì sao quan trọng', 'Đây là lựa chọn kiến trúc nền tảng khiến Hadoop khả thi về chi phí cho bài toán dữ liệu petabyte: mọi thành phần khác (HDFS, YARN...) đều thiết kế xoay quanh triết lý scale-out này.')))

# ===================== PHẦN 2: HDFS =====================
SLIDES.append(divider(2, 8, "HDFS: lưu trữ phân tán", [
    "Mô hình write-once, read-many", "Kiến trúc master/slave: NameNode &amp; DataNode",
    "Block &amp; Replication (nhân bản)", "Hạn chế của HDFS"]))

SLIDES.append(slide("Mục tiêu thiết kế của HDFS", f"""
<p>HDFS tối ưu cho các tệp <b>kích thước lớn</b> (hàng trăm MB đến TB), mô hình truy cập
<b>write-once, read-many</b> (ghi một lần, đọc nhiều lần).</p>
{callout('warn','Đánh đổi có chủ đích', 'Thiết kế để đạt <b>thông lượng cao</b> thay vì <b>độ trễ thấp</b>: phù hợp xử lý batch hơn truy vấn tương tác thời gian thực.')}
<p>Chạy trên <b>phần cứng thông dụng</b> (không cần thiết bị lưu trữ chuyên dụng đắt tiền): chấp nhận lỗi phần cứng xảy ra thường xuyên, bù lại bằng cơ chế chịu lỗi ở cấp phần mềm.</p>
"""))

SLIDES.append(slide("Kiến trúc master/slave: NameNode &amp; DataNode", f"""
<p style="text-align:center"><img src="../assets/diagrams/hdfs-architecture.svg" alt="Kiến trúc HDFS" style="border:1px solid var(--border);border-radius:10px;max-width:100%;max-height:380px;height:auto"></p>
<ul class="pd-legend"><li><b>NameNode</b><span>quản lý metadata: cấu trúc thư mục, tên tệp, ánh xạ tệp→block. Điều phối truy cập từ client.</span></li>
<li><b>DataNode</b><span>lưu trữ block dữ liệu thật, xử lý yêu cầu đọc/ghi từ client.</span></li></ul>
"""))

SLIDES.append(figslide("Hình gốc: kiến trúc GFS, nguồn cảm hứng của HDFS", "gfs_fig1.png",
    "Nguồn: Ghemawat, Gobioff, Leung. <i>The Google File System</i>, SOSP 2003, Figure 1.",
    [["GFS master (namespace, ánh xạ file → chunk, trong RAM)", "NameNode"],
     ["GFS chunkserver (lưu chunk trên Linux file system)", "DataNode"],
     ["Chunk 64 MB, nhân bản trên nhiều chunkserver", "Block 64/128 MB, nhân bản 3 lần"],
     ["Client hỏi master vị trí, rồi đọc/ghi <b>trực tiếp</b> chunkserver (mũi tên dày = dữ liệu không đi qua master)", "Client hỏi NameNode, truyền dữ liệu thẳng với DataNode"]]))

SLIDES.append(figslide("Hình gốc: luồng ghi của GFS, gốc của pipeline nhân bản trong HDFS", "gfs_fig2.png",
    "Nguồn: Ghemawat, Gobioff, Leung. <i>The Google File System</i>, SOSP 2003, Figure 2 (mũi tên mảnh = điều khiển, mũi tên dày = dữ liệu).",
    [["Bước 1-2: client hỏi master ai giữ lease (primary) và vị trí các replica", "Client hỏi NameNode danh sách DataNode cho block mới"],
     ["Bước 3: client đẩy <b>dữ liệu</b> theo chuỗi replica, mỗi máy chuyển tiếp ngay cho máy gần nhất chưa nhận", "Ghi theo <b>pipeline</b> DataNode 1 → 2 → 3, tận dụng băng thông ra của từng máy"],
     ["Bước 4-7: <b>điều khiển</b> đi qua primary, primary đánh số thứ tự rồi báo các secondary, tất cả trả lời lại", "Gói xác nhận (ack) chạy ngược pipeline về client"],
     ["Tách luồng dữ liệu khỏi luồng điều khiển để dùng mạng hiệu quả", "Cùng nguyên tắc: NameNode chỉ điều khiển, dữ liệu đi thẳng giữa client và DataNode"]], side=True, img_w="40%"))

SLIDES.append(slide("Khái niệm block trong HDFS", f"""
<p>Mỗi tệp trong HDFS được <b>chia thành nhiều block</b> (khối dữ liệu) thay vì lưu nguyên khối như hệ file thông thường.</p>
{formula('Kích thước block mặc định', '64\\text{ MB hoặc }128\\text{ MB}')}
{callout('info', 'Vì sao chia block', 'Block lớn giúp giảm chi phí quản lý metadata (ít block hơn so với chia nhỏ như hệ file truyền thống 4KB) và phù hợp mô hình đọc/ghi tuần tự khối lượng lớn mà HDFS hướng tới.')}
"""))

SLIDES.append(slide("Cơ chế nhân bản (replication)", f"""
<p>Mỗi block được <b>replicate</b> (nhân bản) thành nhiều bản sao, phân phối trên các DataNode <b>khác nhau</b> trong cụm.</p>
{formula('Hệ số nhân bản mặc định', '3\\text{ bản sao trên 3 DataNode khác nhau}')}
{callout('good','Vì sao nhân bản giúp chịu lỗi', 'Khi 1 DataNode hỏng, hệ thống vẫn còn bản sao trên node khác: NameNode tự động điều phối sao chép lại để duy trì đủ số bản sao mặc định.')}
"""))

SLIDES.append(slide("Ví dụ minh hoạ: dung lượng vật lý thực cần", f"""
<p style="color:var(--muted);font-size:.85rem">Ví dụ số liệu tự tính để minh hoạ khái niệm: không trích từ sách, chỉ dùng đúng các thông số sách đã nêu (block 128MB, nhân bản 3 lần).</p>
{tbl(['Bước tính','Giá trị'],
     [['Kích thước tệp cần lưu', '1 TB = 1 048 576 MB'],
      ['Kích thước block', '128 MB'],
      ['Số block cần (1 048 576 / 128)', '= 8 192 block'],
      ['Hệ số nhân bản', '× 3'],
      ['<b>Dung lượng vật lý thực tế cần trên cụm</b>', '<b>= 3 TB</b> (gấp 3 lần dữ liệu gốc)']])}
{callout('warn', 'Đánh đổi', 'Nhân bản 3 lần giúp chịu lỗi tốt nhưng tốn gấp 3 lần dung lượng lưu trữ thật: đây là chi phí đổi lấy độ tin cậy của HDFS.')}
"""))

SLIDES.append(slide("NameNode và rủi ro điểm lỗi duy nhất", f"""
<p>NameNode là thành phần <b>trung tâm duy nhất</b> giữ toàn bộ metadata: nếu NameNode gặp sự cố mà không có cơ chế dự phòng, cả hệ thống có nguy cơ mất khả năng xác định dữ liệu nằm ở đâu (dù dữ liệu thật vẫn còn nguyên trên DataNode).</p>
{callout('good', 'Cơ chế giảm thiểu rủi ro', '<i>Secondary NameNode</i> định kỳ sao lưu &amp; hợp nhất edit log của NameNode, hỗ trợ <b>phục hồi nhanh metadata</b> khi NameNode gặp sự cố: không phải bản sao chạy song song, mà là điểm khôi phục.')}
"""))

SLIDES.append(slide("Hạn chế của HDFS", tbl(["Hạn chế", "Lý do"], [
    ["Độ trễ truy xuất thấp (real-time)", "Tối ưu cho thông lượng tuần tự, không phải truy vấn ngẫu nhiên"],
    ["Số lượng lớn tệp nhỏ", "Metadata mọi tệp giữ trong bộ nhớ NameNode: giới hạn RAM"],
    ["Sửa đổi nội dung tuỳ ý", "Chỉ hỗ trợ <i>append</i> ở cuối tệp, không ghi đè giữa file"],
]) + callout('warn', 'Đánh đổi có chủ đích', 'HDFS hy sinh một số tính năng POSIX để đổi lấy khả năng mở rộng &amp; chịu lỗi vượt trội: nhờ đó lưu trữ được hàng petabyte trên cụm hàng nghìn node.')))

# ===================== PHẦN 3: MapReduce & YARN =====================
SLIDES.append(divider(3, 8, "MapReduce &amp; YARN", [
    "Mô hình lập trình Map + Reduce", "Vai trò MapReduce: Hadoop 1.x vs 2.x",
    "Vì sao cần tách YARN khỏi MapReduce", "Kiến trúc YARN: RM / AM / NM"]))

SLIDES.append(slide("Mô hình lập trình MapReduce", f"""
<p>Đề xuất bởi Google (2004): framework đơn giản cho xử lý dữ liệu lớn song song, dựa trên 2 hàm do người lập trình định nghĩa:</p>
{tbl(['Giai đoạn','Việc của lập trình viên','Việc của framework'],
     [['Map (ánh xạ)','Viết hàm Map','Phân chia dữ liệu, phân phối tác vụ lên cụm'],
      ['Reduce (giảm thiểu)','Viết hàm Reduce','Thu gộp kết quả trung gian, xử lý lỗi tự động']])}
{callout('good','Điểm mạnh','Lập trình viên chỉ cần viết 2 hàm: phần song song hoá, phân phối, chịu lỗi đều do framework tự động đảm nhiệm.')}
"""))

SLIDES.append(figslide("Hình gốc: luồng thực thi MapReduce của Google", "mr_fig1.png",
    "Nguồn: Dean, Ghemawat. <i>MapReduce: Simplified Data Processing on Large Clusters</i>, OSDI 2004, Figure 1.",
    [["User Program fork ra Master và các worker", "Client submit job; Master ↔ JobTracker (Hadoop 1.x) / ApplicationMaster (YARN)"],
     ["Input chia thành split, mỗi split cho 1 map worker", "InputSplit, 1 map task xử lý 1 split gần dữ liệu (data locality)"],
     ["Map ghi file trung gian lên <b>đĩa cục bộ</b>; reduce worker (5) remote read", "Giai đoạn shuffle: reduce kéo dữ liệu từ đĩa node chạy map"],
     ["Reduce worker ghi output file", "Kết quả ghi xuống HDFS"]], side=True, img_w="54%"))

SLIDES.append(imgs_slide("Hình gốc: MapReduce lan nhanh trong Google chỉ sau 18 tháng", [
    ("mr_fig4.png", "Figure 4: số chương trình MapReduce trong kho mã nguồn, từ 0 (đầu 2003) lên gần 900 (9/2004).", 38),
    ("mr_table1.png", "Table 1: các job MapReduce chạy tháng 8/2004 (nguồn: Dean, Ghemawat, OSDI 2004).", 45)],
    maxh=290, body_after=callout('good', 'Đọc số liệu', 'Mỗi job trung bình dùng <b>157</b> máy và gặp <b>1,2</b> lần máy chết, nên chịu lỗi tự động không phải tính năng phụ mà là điều kiện để chạy được. Tổng cộng 29.423 job đọc 3.288 TB đầu vào trong 1 tháng.')))

SLIDES.append(slide("Vai trò MapReduce: Hadoop 1.x → 2.x", tbl(
    ["Phiên bản", "Vai trò MapReduce"],
    [["Hadoop 1.x", "Engine xử lý dữ liệu <b>chính</b>, cung cấp khả năng xử lý batch cho mọi bài toán"],
     ["Hadoop 2.x (có YARN)", "Trở thành <b>một trong nhiều</b> framework chạy trên cụm, cạnh tranh tài nguyên với Spark, Flink..."]]
) + f"""<p>Tối ưu hoá tận dụng hạ tầng: <b>Data Locality</b> (đặt tác vụ gần dữ liệu), <b>Minimal Data Exchange</b>,
<b>Fault Tolerance</b> tự động: nhờ đó chạy hiệu quả trên hàng nghìn node, xử lý hàng petabyte theo lô.</p>
{callout('warn','Hạn chế', 'Độ trễ cao cho tác vụ lặp/tương tác → động lực ra đời Spark, Flink. Vẫn là nền tảng quan trọng cho <i>batch processing</i> truyền thống.')}"""))

SLIDES.append(slide("MapReduce tích hợp với cả hệ sinh thái", f"""
<p>MapReduce không hoạt động đơn độc: nó là <b>engine thực thi phía sau</b> của nhiều công cụ khác:</p>
{tbl(['Công cụ','Dịch sang MapReduce như thế nào'],
     [['HDFS', 'MapReduce đọc/ghi dữ liệu trực tiếp qua HDFS'],
      ['YARN', 'Quản lý tài nguyên cho các job MapReduce chạy trên cụm'],
      ['Hive', 'Dịch câu lệnh HiveQL thành job MapReduce'],
      ['Pig', 'Dịch kịch bản Pig Latin thành job MapReduce'],
      ['Sqoop', 'Dùng MapReduce (chỉ Map task) để import/export dữ liệu']])}
{callout('good', 'Ý nghĩa', 'Đây là lý do MapReduce được gọi là "engine chung": người dùng Hive/Pig/Sqoop không cần biết MapReduce chạy bên dưới, nhưng mọi tác vụ của họ cuối cùng đều quy về job MapReduce.')}
"""))

SLIDES.append(slide("Lý do tách YARN khỏi MapReduce", f"""
<p>Trong Hadoop 1.x, <b>MapReduce vừa xử lý dữ liệu vừa quản lý tài nguyên &amp; lập lịch</b> trên cụm: dẫn đến hạn chế về hiệu năng và tính linh hoạt.</p>
{callout('good','Giải pháp Hadoop 2.x','YARN (Yet Another Resource Negotiator) tách biệt <b>quản lý tài nguyên</b> khỏi <b>xử lý dữ liệu</b>, biến Hadoop thành nền tảng tổng quát hơn: nhiều mô hình (MapReduce, Spark, Flink, Tez...) cùng chạy trên 1 cụm.')}
"""))

SLIDES.append(slide("Kiến trúc YARN", f"""<p style="text-align:center"><img src="../assets/diagrams/yarn-architecture.svg" alt="Kiến trúc YARN" style="border:1px solid var(--border);border-radius:10px;max-width:100%;max-height:380px;height:auto"></p>
<ul class="pd-legend">
<li><b>ResourceManager</b><span>quản lý tài nguyên toàn cục (CPU, bộ nhớ) cho mọi ứng dụng trên cụm</span></li>
<li><b>ApplicationMaster</b><span>mỗi ứng dụng có 1 riêng, lập lịch/phối hợp thực thi tác vụ trên các NodeManager</span></li>
<li><b>NodeManager</b><span>tác nhân tại mỗi node: cấp container, giám sát thực thi tác vụ</span></li></ul>
"""))

SLIDES.append(slide("Quy trình 1 ứng dụng chạy trên YARN", f"""
<ol style="line-height:2.1">
<li>Ứng dụng được <b>submit</b> lên ResourceManager</li>
<li>ResourceManager cấp <b>container đầu tiên</b> để khởi chạy ApplicationMaster</li>
<li>ApplicationMaster yêu cầu ResourceManager cấp <b>thêm container</b> trên các NodeManager thích hợp</li>
<li>Các tác vụ của ứng dụng chạy trong những container đó, được NodeManager giám sát</li>
</ol>
{callout('info', 'Tự động hoá', 'Toàn bộ quá trình diễn ra tự động dưới sự điều phối của YARN: người dùng chỉ cần submit ứng dụng.')}
"""))

SLIDES.append(slide("Lợi ích YARN mang lại cho Hadoop", tbl(["Lợi ích", "Giải thích"], [
    ["Đa dạng hoá workload", "Nhiều loại ứng dụng chạy đồng thời (MapReduce, Spark, Flink, Tez...)"],
    ["Tăng tính linh hoạt", "Biến cụm Hadoop thành nền tảng đa năng, không chỉ dành cho MapReduce"],
    ["Mở rộng &amp; đa người dùng", "Cấu hình chính sách lập lịch: FIFO, Fair Scheduler, Capacity Scheduler"],
    ["Quản lý tài nguyên hiệu quả", "Phân bổ công bằng &amp; hiệu quả giữa các ứng dụng khác nhau"],
]) + callout('info', 'Ý nghĩa', 'YARN là bước ngoặt giúp hệ sinh thái Hadoop phát triển phong phú: Hive, Pig, Spark... có thể tích hợp và chạy chung 1 cụm thay vì hạ tầng riêng.')))

# ===================== PHẦN 4: Hive & Pig =====================
SLIDES.append(divider(4, 8, "Hive &amp; Pig: truy vấn và biến đổi dữ liệu", [
    "Apache Hive: data warehouse + HiveQL", "Apache Pig: Pig Latin, data flow",
    "Cả hai đều dịch sang job MapReduce", "So sánh 2 hướng tiếp cận"]))

SLIDES.append(slide("Apache Hive: data warehouse trên Hadoop", f"""
<p>Phát triển tại <b>Facebook</b>: cho phép truy vấn dữ liệu lớn bằng ngôn ngữ gần SQL (<b>HiveQL</b>): SELECT, JOIN, GROUP BY...
tự động dịch thành job MapReduce (hoặc Tez, Spark) để thực thi.</p>
{tbl(['Đặc trưng','Ý nghĩa'],
     [['Phù hợp phân tích dữ liệu lớn','Tối ưu cho truy vấn batch trên TB dữ liệu'],
      ['Thân thiện người dùng','Nhà phân tích dùng SQL quen thuộc, không cần viết Java MapReduce'],
      ['Schema on read','Dữ liệu lưu thô trên HDFS, schema chỉ định khi <i>đọc</i>: linh hoạt với dữ liệu đa dạng']])}
{callout('warn','Độ trễ','Tính bằng phút (do khởi tạo job MapReduce/Tez): phù hợp batch hơn truy vấn tương tác tức thì.')}
"""))

SLIDES.append(slide("Cơ chế hoạt động của Hive", f"""
<ol style="line-height:2.1">
<li>Người dùng viết câu lệnh <b>HiveQL</b> (SELECT, JOIN, GROUP BY...)</li>
<li>Hive <b>tự động dịch</b> câu lệnh thành job MapReduce (hoặc Tez, Spark) tương ứng</li>
<li>Job thực thi trên cụm Hadoop, đọc dữ liệu thô từ HDFS theo schema đã khai báo khi đọc</li>
<li>Kết quả trả về dưới dạng <b>bảng</b>, giống làm việc với CSDL truyền thống</li>
</ol>
{callout('good', 'Giá trị cốt lõi', 'Người dùng không cần biết MapReduce chạy bên dưới: chỉ cần viết SQL quen thuộc.')}
"""))

SLIDES.append(slide("Apache Pig: kịch bản xử lý dữ liệu", f"""
<p>Phát triển tại <b>Yahoo!</b>: thay vì SQL, Pig cung cấp ngôn ngữ kịch bản <b>Pig Latin</b> để biểu diễn luồng xử lý
(đọc, lọc, biến đổi, gộp nhóm, join, sắp xếp...) theo dạng <i>data flow</i>.</p>
{tbl(['Đặc điểm','Giải thích'],
     [['Độ dễ lập trình','Câu lệnh tuần tự, Pig tự song song hoá &amp; tối ưu'],
      ['Tối ưu hoá','Biết trước toàn bộ luồng → kết hợp bước, đẩy bộ lọc lên sớm'],
      ['Mở rộng (UDF)','Tự định nghĩa hàm bằng Java/Python chèn vào kịch bản']])}
<p>Pig Engine biên dịch kịch bản thành chuỗi job MapReduce: đặc biệt hiệu quả cho <b>transform &amp; join</b> dữ liệu phức tạp.</p>
"""))

SLIDES.append(slide("So sánh Hive vs Pig", tbl(["Tiêu chí", logo_img("apachehive.svg", 26) + " Hive", logo_img("pig.gif", 28) + " Pig"], [
    ["Ngôn ngữ", "HiveQL (giống SQL)", "Pig Latin (kịch bản)"],
    ["Đối tượng dùng", "Nhà phân tích quen SQL", "Kỹ sư dữ liệu, ETL phức tạp"],
    ["Mô hình dữ liệu", "Bảng (schema-on-read)", "Data flow tuần tự"],
    ["Engine thực thi", "Dịch sang MapReduce/Tez/Spark", "Dịch sang MapReduce"],
    ["Độ trễ", "Vài phút (batch)", "Vài phút (batch)"],
]) + callout('good', 'Điểm chung', 'Cả hai đều nhằm <b>đơn giản hoá sử dụng Hadoop</b>, không yêu cầu viết Java MapReduce thuần: cùng dịch công việc thành job MapReduce chạy trên cụm.')))

# ===================== PHẦN 5: HBase & Sqoop =====================
SLIDES.append(divider(5, 8, "HBase &amp; Sqoop", [
    "HBase: NoSQL wide-column trên Hadoop", "Mô hình Bigtable (Google)",
    "HBase vs RDBMS", "Sqoop: cầu nối Hadoop ↔ SQL"]))

SLIDES.append(slide("Apache HBase: \"cơ sở dữ liệu của Hadoop\"", f"""
<p>NoSQL phân tán xây trên Hadoop, thiết kế theo mô hình <b>Bigtable</b> (Google): lưu bảng <b>hàng tỷ dòng, hàng triệu cột</b>,
hỗ trợ truy cập ngẫu nhiên độ trễ thấp.</p>
{callout('info','Ví von','Nếu HDFS giống hệ file, thì HBase giống <b>database chạy trên HDFS</b>, đọc/ghi theo kiểu bảng.')}
{tbl(['Đặc trưng','Giải thích'],
     [['Mô hình wide-column','Cột nhóm thành <i>column family</i>; mỗi ô có row key, tên cột, giá trị, timestamp'],
      ['Mở rộng cực lớn','Scale-out hàng trăm node, bảng hàng chục petabyte, tự động chia region'],
      ['Đọc/ghi thời gian thực','Hàng trăm nghìn INSERT/giây nhờ LSM-tree + commit log']])}
"""))

SLIDES.append(slide("Điểm khác biệt giữa HBase và RDBMS", f"""
{callout('warn', 'Không phải RDBMS', 'HBase <b>không hỗ trợ SQL hay join phức tạp</b>: truy vấn qua API lập trình (Java/REST/Thrift) hoặc scan/get/put theo khoá. Không có transaction ACID đa bảng.')}
<p>Phù hợp cho: truy cập ngẫu nhiên theo khoá, khối lượng lớn (vd tra cứu/cập nhật theo userID): hơn là phân tích ad-hoc.</p>
<p><b>Ví dụ thực tế:</b> Facebook Messaging từng dùng HBase lưu tin nhắn cho hàng trăm triệu người dùng, khai thác khả năng mở rộng linh hoạt.</p>
"""))

SLIDES.append(figslide("Hình gốc: mô hình dữ liệu Bigtable, nền của HBase", "bigtable_fig1.png",
    "Nguồn: Chang et al. <i>Bigtable: A Distributed Storage System for Structured Data</i>, OSDI 2006, Figure 1 (ví dụ bảng lưu trang web, row key là URL đảo ngược).",
    [["Row key \"com.cnn.www\" (URL đảo ngược để các trang cùng domain nằm gần nhau, giữ thứ tự từ điển)", "Row key của HBase, sắp xếp theo thứ tự byte; thiết kế row key quyết định locality và hotspotting"],
     ["Column family <code>contents:</code> và <code>anchor:</code>", "Column family; cột viết dạng <code>family:qualifier</code>"],
     ["Mỗi ô có nhiều phiên bản gắn nhãn thời gian (t3, t5, t6)", "Cell có nhiều version theo timestamp"]], side=False, img_w="78%"))

SLIDES.append(figslide("Hình gốc: cách Bigtable tìm tablet, và vai trò của Chubby", "bigtable_fig4.png",
    "Nguồn: Chang et al. <i>Bigtable</i>, OSDI 2006, Figure 4 (phân cấp 3 tầng giống B+-tree).",
    [["Tầng 1: một file trong <b>Chubby</b> chứa vị trí root tablet", "ZooKeeper lưu vị trí của bảng meta"],
     ["Tầng 2-3: root tablet → các METADATA tablet → tablet của người dùng", "Bảng meta chứa vị trí từng region của mọi bảng"],
     ["Client lưu đệm vị trí, hiếm khi phải hỏi master", "Client HBase cũng lưu đệm vị trí region"]], side=True, img_w="52%"))

SLIDES.append(figslide("Hình gốc: tablet được lưu thế nào, gốc của MemStore và HFile", "bigtable_fig5.png",
    "Nguồn: Chang et al. <i>Bigtable</i>, OSDI 2006, Figure 5 (Tablet Representation).",
    [["Ghi: vào <b>tablet log</b> (commit log) rồi vào <b>memtable</b> trong bộ nhớ", "WAL rồi MemStore của HBase"],
     ["Memtable đầy thì ghi thành <b>SSTable</b> bất biến trên GFS (minor compaction)", "MemStore flush thành HFile trên HDFS"],
     ["Đọc: gộp memtable với các SSTable đã sắp xếp; định kỳ gộp lại (merging / major compaction)", "Đọc gộp MemStore và HFile; compaction định kỳ"]], side=True, img_w="48%"))

SLIDES.append(slide("Tiêu chí chọn giữa HDFS + Hive và HBase", tbl(
    ["Nhu cầu", "Chọn"],
    [["Phân tích tổng hợp trên tập dữ liệu lớn (batch)", "HDFS + MapReduce/Hive"],
     ["Đọc/ghi ngẫu nhiên theo khoá, độ trễ thấp, gần thời gian thực", "HBase"],
     ["Truy vấn kiểu SQL, JOIN, GROUP BY phức tạp", "Hive (không phải HBase)"],
     ["Tra cứu/cập nhật theo userID với tốc độ cao", "HBase (không phải Hive)"]]
) + callout('info', 'Nguyên tắc chọn', 'Không có công cụ nào "tốt hơn" tuyệt đối: HDFS+Hive phục vụ phân tích tổng hợp, HBase phục vụ truy cập chi tiết từng bản ghi. Hai nhu cầu khác nhau, hai công cụ khác nhau.')))

SLIDES.append(slide("Apache Sqoop: cầu nối Hadoop ↔ RDBMS", f"""
<p>Tên ghép từ <b>SQL + Hadoop</b>: công cụ nhập/xuất dữ liệu hàng loạt giữa Hadoop và RDBMS (MySQL, PostgreSQL, Oracle...).</p>
{tbl(['Chiều', 'Cơ chế'],
     [['Import (RDBMS → HDFS)', 'Kết nối JDBC, khởi chạy job MapReduce chỉ gồm Map task: mỗi task nhập 1 phần bảng (theo WHERE/primary key)'],
      ['Export (HDFS → RDBMS)', 'Chia dữ liệu HDFS thành splits, mỗi Map task đẩy 1 phần vào CSDL qua batch INSERT']])}
{callout('good','Use case tiêu biểu','Nhập bảng giao dịch từ data warehouse vào Hadoop để phân tích chuyên sâu · xuất kết quả Hive/HDFS ra bảng SQL cho ứng dụng kinh doanh.')}
"""))

SLIDES.append(slide("Quy trình Sqoop Import từng bước", f"""
<ol style="line-height:2.1">
<li>Sqoop kết nối tới CSDL nguồn qua <b>JDBC</b></li>
<li>Thực thi truy vấn (hoặc duyệt từng bảng), <b>chia dữ liệu</b> theo điều kiện WHERE hoặc primary key</li>
<li>Khởi chạy job MapReduce <b>chỉ gồm Map task</b>: mỗi task nhập 1 phần dữ liệu song song</li>
<li>Ghi kết quả xuống HDFS (text/CSV hoặc Avro/Parquet), hoặc thẳng vào Hive/HBase nếu được chỉ định</li>
</ol>
{callout('good', 'Vì sao song song', 'Chia nhỏ theo primary key cho phép nhiều Map task cùng nhập dữ liệu đồng thời: tăng tốc đáng kể so với import tuần tự.')}
"""))

# ===================== PHẦN 6: Kafka, Oozie, ZooKeeper =====================
SLIDES.append(divider(6, 8, "Kafka, Oozie, ZooKeeper", [
    "Kafka: nền tảng streaming pub-sub", "Oozie: lập lịch workflow dạng DAG",
    "ZooKeeper: dịch vụ điều phối phân tán", "Vai trò trong toàn hệ sinh thái"]))

SLIDES.append(slide("Apache Kafka: streaming thời gian thực", f"""
<p>Phát triển tại <b>LinkedIn</b>: nền tảng <b>publish-subscribe</b> phân tán: producer gửi thông điệp vào <i>topic</i>,
consumer đăng ký nhận từ topic đó.</p>
{tbl(['Đặc điểm','Giải thích'],
     [['Thông lượng &amp; độ bền cao','Hàng triệu thông điệp/giây, ghi commit log tuần tự, nhân bản giữa broker'],
      ['Partition','Mỗi topic chia nhiều partition: tăng song song; Kafka đảm bảo thứ tự <i>trong từng partition</i>'],
      ['Multi-subscriber','Nhiều consumer group độc lập đọc cùng dữ liệu mà không ảnh hưởng nhau']])}
{callout('info','Vai trò trong hệ sinh thái','Tầng thu thập/phân phối sự kiện (ingest): nguồn dữ liệu đầu vào liên tục cho Spark, Storm hoặc lưu vào HDFS/HBase.')}
"""))

SLIDES.append(slide("Ví dụ minh hoạ: Kafka trong pipeline thu thập log", f"""
<p style="color:var(--muted);font-size:.85rem">Minh hoạ dựa trên ví dụ sách nêu (thu thập log sự kiện người dùng vào topic "website_events"): diễn giải thêm để dễ hình dung, không phải trích nguyên văn.</p>
<ol style="line-height:2.1">
<li>Hàng trăm máy chủ web sinh ra sự kiện người dùng (click, xem trang...) liên tục</li>
<li>Mỗi sự kiện được gửi (<b>produce</b>) vào topic <code>website_events</code></li>
<li>Topic được chia thành nhiều <b>partition</b> để tăng thông lượng ghi song song</li>
<li>Ứng dụng Hadoop/Spark <b>consume</b> dòng sự kiện này để xử lý gần thời gian thực</li>
</ol>
{callout('good', 'Điểm mấu chốt', 'Producer (máy chủ web) và consumer (Spark/Hadoop) không kết nối trực tiếp: Kafka đứng giữa như một hàng đợi bền vững, chịu lỗi.')}
"""))

SLIDES.append(figslide("Hình gốc: log của Kafka, thiết kế quanh offset", "kafka_fig2.png",
    "Nguồn: Kreps, Narkhede, Rao. <i>Kafka: a Distributed Messaging System for Log Processing</i>, NetDB 2011, Figure 2.",
    [["Mỗi partition là 1 log chia thành nhiều segment file", "Partition của topic; segment file trên đĩa broker"],
     ["Message được đánh địa chỉ bằng <b>offset</b> logic trong log, không có message id riêng", "Offset: consumer tự nhớ vị trí đã đọc, broker không giữ trạng thái này (stateless broker)"],
     ["Chỉ ghi nối vào cuối (append), đọc tuần tự, xóa theo thời gian lưu giữ (điển hình 7 ngày)", "Retention theo thời gian; consumer có thể tua lại offset cũ để đọc lại"]], side=True, img_w="40%"))

SLIDES.append(figslide("Hình gốc: Kafka tại LinkedIn, nơi dữ liệu chảy vào Hadoop", "kafka_fig3.png",
    "Nguồn: Kreps, Narkhede, Rao. <i>Kafka: a Distributed Messaging System for Log Processing</i>, NetDB 2011, Figure 3.",
    [["Frontend gửi log qua load balancer tới các broker ở datacenter chính", "Producer → broker, đẩy theo lô"],
     ["Dịch vụ thời gian thực đọc trực tiếp từ broker", "Consumer xử lý gần thời gian thực"],
     ["Datacenter phân tích có cụm Kafka kéo dữ liệu về, nuôi <b>Hadoop</b> và kho dữ liệu (DWH)", "MapReduce đọc thẳng từ Kafka qua input format riêng, ghi kết quả vào HDFS"],
     ["Bài báo nêu cỡ năm 2011: hàng trăm GB và gần 1 tỉ thông điệp mỗi ngày, trễ đầu-cuối khoảng 10 giây", "Đây là lý do Kafka nằm ở tầng thu thập của hệ sinh thái"]], side=True, img_w="42%"))

SLIDES.append(slide("Apache Oozie: lập lịch workflow", f"""
<p>Hệ thống quản lý &amp; lập lịch luồng công việc (workflow scheduler) cho Hadoop: định nghĩa chuỗi job
(MapReduce → Hive → shell script...) và quản lý thực thi tuần tự/song song.</p>
{callout('good','Mô hình DAG','Workflow mô tả dưới dạng <b>đồ thị có hướng không chu trình</b>: node là action/control node, cạnh là luồng thực thi (có điều kiện).')}
<p><b>Ví dụ:</b> chạy job MapReduce A → nếu thành công chạy job Hive B, nếu thất bại gửi email rồi kết thúc.</p>
<p><i>Coordinator</i>: lên lịch lặp lại workflow theo thời gian (mỗi giờ/ngày) hoặc khi dữ liệu mới đến HDFS.</p>
"""))

SLIDES.append(slide("Apache ZooKeeper: dịch vụ điều phối", tbl(
    ["Chức năng", "Mô tả ngắn"],
    [["Quản lý cấu hình", "Lưu &amp; phân phát thông tin cấu hình cho các node"],
     ["Đặt tên (naming)", "Không gian tên chung để dịch vụ đăng ký &amp; tìm nhau"],
     ["Đồng bộ hoá phân tán", "Cơ chế khoá, hàng rào (barrier) tránh xung đột"],
     ["Dịch vụ nhóm", "Theo dõi thành viên trong 1 nhóm node (vd RegionServer)"],
     ["Bầu chọn leader", "Đảm bảo đúng 1 node làm leader tại 1 thời điểm (ephemeral znode)"]]
)))

SLIDES.append(slide("Cơ sở tin cậy của ZooKeeper", f"""
<p>ZooKeeper dùng thuật toán <b>ZAB</b> (ZooKeeper Atomic Broadcast: thuộc họ thuật toán Paxos) để đảm bảo
tất cả server ZooKeeper (chạy thành cụm nhỏ) duy trì <b>cùng một trạng thái</b>.</p>
{callout('good', 'Tính nhất quán tuần tự', 'Các thay đổi áp dụng theo mô hình nhất quán tuần tự; client có thể đăng ký <b>watch</b> để được thông báo ngay khi dữ liệu thay đổi hoặc node mới xuất hiện/biến mất.')}
<p>Nhờ đó, các node trong hệ phân tán không cần liên lạc peer-to-peer phức tạp: chỉ cần dựa vào ZooKeeper như một "trọng tài chung" tin cậy.</p>
"""))

SLIDES.append(figslide("Hình gốc: cấu trúc Chubby, nguồn cảm hứng của ZooKeeper", "chubby_fig1.png",
    "Nguồn: Burrows. <i>The Chubby lock service for loosely-coupled distributed systems</i>, OSDI 2006, Figure 1.",
    [["1 Chubby cell gồm 5 server (replica), chọn ra 1 master bằng giao thức đồng thuận", "1 ZooKeeper ensemble (thường 3 hoặc 5 server), bầu 1 leader"],
     ["Cần đa số replica còn sống (3/5) thì cell mới hoạt động", "Quorum: đa số server phải sống, nếu không dịch vụ dừng"],
     ["Client application liên lạc qua chubby library bằng RPC", "Client dùng thư viện ZooKeeper; znode, watch, ephemeral node thay cho khóa/tệp nhỏ của Chubby"]], side=True, img_w="44%"))

SLIDES.append(figslide("Hình gốc: Chubby xử lý mất master ra sao, ý tưởng cho failover của ZooKeeper", "chubby_fig2.png",
    "Nguồn: Burrows. <i>The Chubby lock service</i>, OSDI 2006, Figure 2 (grace period khi master chuyển giao; thời gian chạy từ trái sang phải, không theo tỉ lệ).",
    [["Client giữ <b>session lease</b>, gia hạn bằng KeepAlive tới master", "Session ZooKeeper có timeout, client gửi ping/heartbeat để giữ session"],
     ["Master chết: client hết lease, vào <b>grace period</b>, chặn lời gọi API chứ chưa huỷ session", "Client mất kết nối nhưng chưa hết timeout: chờ kết nối lại tới server khác"],
     ["Master mới được bầu trong vài giây, client nối lại và tiếp tục", "Leader mới được bầu (ZAB), session còn hạn thì giữ nguyên znode tạm"]], side=False, img_w="82%"))

SLIDES.append(slide("Vị trí của ZooKeeper trong hệ sinh thái Hadoop", tbl(["Thành phần", "ZooKeeper dùng để"], [
    ["HDFS High Availability", "Giám sát NameNode &amp; kích hoạt failover"],
    ["YARN", "Lưu thông tin ResourceManager chủ"],
    ["HBase", "Theo dõi RegionServer &amp; điều phối Master"],
    ["Kafka (bản cũ)", "Quản lý thông tin broker, chủ đề, phân vùng"],
]) + callout('info', 'Vai trò tổng thể', 'ZooKeeper là "người giữ nhịp" thầm lặng phía sau: giảm độ phức tạp phát triển hệ phân tán nhờ các primitive tin cậy có sẵn.')))

# ===================== PHẦN 7: Tổng kết =====================
SLIDES.append(divider(7, 8, "Tổng kết", [
    "Sơ đồ toàn cảnh hệ sinh thái Hadoop", "Tổng kết nội dung chương 2",
    "Công nghệ và nơi khởi nguồn", "Lộ trình phát triển", "Tài liệu tham khảo"]))

SLIDES.append(slide("Toàn cảnh hệ sinh thái Hadoop", tbl(
    ["Tầng", "Thành phần", "Vai trò"],
    [["Thu thập", logo_img("apachekafka.svg", 26) + " Kafka", "Streaming sự kiện thời gian thực"],
     ["Lưu trữ", logo_img("apachehadoop.svg", 26) + " HDFS, " + logo_img("apachehbase.svg", 26) + " HBase", "Tệp phân tán &amp; NoSQL thời gian thực"],
     ["Tính toán batch", logo_img("apachehadoop.svg", 26) + " MapReduce", "Mô hình Map + Reduce song song"],
     ["Phân tích", logo_img("apachehive.svg", 26) + " Hive, " + logo_img("pig.gif", 28) + " Pig", "SQL-like &amp; kịch bản data flow"],
     ["Quản trị luồng", logo_img("oozie.png", 22) + " Oozie", "Lập lịch workflow dạng DAG"],
     ["Vận hành", logo_img("zookeeper.svg", 28) + " ZooKeeper", "Điều phối, đồng bộ, bầu leader"],
     ["Điều phối tài nguyên", logo_img("apachehadoop.svg", 26) + " YARN", "Quản lý tài nguyên đa ứng dụng"],
     ["Tích hợp RDBMS", logo_img("sqoop.png", 22) + " Sqoop", "Import/export với CSDL quan hệ"]], dense=True
)))

SLIDES.append(slide("Mỗi công nghệ ra đời để giải một bài toán của một công ty", tbl(
    ["Công nghệ", "Khởi nguồn tại", "Bài toán gốc"],
    [[logo_img("apachehadoop.svg") + " Hadoop (HDFS + MapReduce)", logo_img("yahoo.svg", 28) + " Yahoo!", "Lập chỉ mục web, mô phỏng GFS và MapReduce của Google"],
     [logo_img("pig.gif", 44) + " Pig", logo_img("yahoo.svg", 28) + " Yahoo Research", "Viết MapReduce bằng Java quá tốn công"],
     [logo_img("apachehive.svg") + " Hive", logo_img("meta.svg", 30) + " Facebook", "Dân phân tích muốn dùng SQL trên kho dữ liệu hàng chục PB"],
     [logo_img("apachehbase.svg") + " HBase", "Powerset (theo Bigtable của " + logo_img("google.svg", 24) + " Google)", "Đọc ghi ngẫu nhiên theo khoá trên bảng khổng lồ"],
     [logo_img("sqoop.png", 30) + " Sqoop", "Cloudera", "Đưa dữ liệu giữa RDBMS và Hadoop"],
     [logo_img("apachekafka.svg") + " Kafka", logo_img("linkedin.svg", 28) + " LinkedIn", "Thu thập luồng sự kiện hoạt động người dùng"],
     [logo_img("oozie.png", 30) + " Oozie", logo_img("yahoo.svg", 28) + " Yahoo!", "Điều phối chuỗi job Hadoop phụ thuộc nhau"],
     [logo_img("zookeeper.svg", 44) + " ZooKeeper", logo_img("yahoo.svg", 28) + " Yahoo Research", "Điều phối, bầu leader (theo Chubby của Google)"],
     [logo_img("tez.jpg", 30) + " Tez, " + logo_img("apachespark.svg", 30) + " Spark, " + logo_img("apacheflink.svg", 30) + " Flink", "Cộng đồng Apache", "Engine chạy trên YARN, thay MapReduce cho tác vụ lặp/tương tác"]],
    dense=True)))

SLIDES.append(slide("Lộ trình phát triển: từ 2 bài báo Google tới hệ sinh thái", f"""
<p style="font-size:.9rem">Nét đứt xám = ý tưởng từ bài báo Google; nét liền = phụ thuộc lúc chạy (công cụ chạy trên Hadoop, HBase và Kafka dùng ZooKeeper, Kafka nạp dữ liệu vào HDFS).</p>
{tech_timeline_svg()}
"""))

SLIDES.append(slide("Tổng kết chương 2", f"""
<p>Hai nền tảng chính <b>HDFS</b> (lưu trữ tin cậy, mở rộng trên phần cứng rẻ) và <b>MapReduce</b> (lập trình
song song đơn giản) tạo lõi Hadoop. <b>YARN</b> tách quản lý tài nguyên, biến cụm thành hạ tầng đa nhiệm.</p>
<p>Các dự án mở rộng đáp ứng nhu cầu đa dạng: <b>Hive</b> (SQL-like), <b>Pig</b> (ETL kịch bản),
<b>HBase</b> (NoSQL thời gian thực), <b>Sqoop</b> (tích hợp RDBMS), <b>Kafka</b> (streaming),
<b>Oozie</b> (workflow), <b>ZooKeeper</b> (điều phối).</p>
{callout('good', 'Thông điệp chính', 'Sức mạnh Hadoop không nằm ở riêng HDFS, mà ở <b>toàn bộ hệ sinh thái phối hợp</b>: thu thập → lưu trữ → tính toán → phân tích → quản trị → vận hành.')}
"""))

SLIDES.append(slide("Thuật ngữ quan trọng (tra cứu nhanh)", tbl(
    ["Thuật ngữ", "Giải nghĩa ngắn"],
    [["NameNode / DataNode", "Node quản lý metadata / node lưu block dữ liệu thật trong HDFS"],
     ["Block &amp; Replication", "Đơn vị chia nhỏ tệp (64–128MB) &amp; cơ chế nhân bản (mặc định 3 lần)"],
     ["ResourceManager / NodeManager", "Quản lý tài nguyên toàn cục / tác nhân quản lý tài nguyên từng node (YARN)"],
     ["ApplicationMaster", "Tiến trình lập lịch riêng cho mỗi ứng dụng chạy trên YARN"],
     ["HiveQL / Pig Latin", "Ngôn ngữ truy vấn giống SQL (Hive) / ngôn ngữ kịch bản data flow (Pig)"],
     ["Column family", "Nhóm các cột trong bảng wide-column của HBase"],
     ["Topic / Partition", "Chủ đề thông điệp / đơn vị chia nhỏ 1 topic trong Kafka để song song hoá"],
     ["DAG", "Đồ thị có hướng không chu trình: mô hình workflow của Oozie"],
     ["Znode", "Đơn vị dữ liệu trong cây thư mục phân tán của ZooKeeper"]], dense=True
)))

SLIDES.append(slide("Tài liệu tham khảo", f"""
<p><b>Nguồn duy nhất của toàn bộ nội dung trình bày:</b></p>
{tbl(['Mục','Chi tiết'],
     [['Giáo trình','<i>Lưu trữ và Xử lý Dữ liệu Lớn</i>: Trần Văn Đặng, Nguyễn Hữu Đức, Nguyễn Bình Minh, Trần Việt Trung'],
      ['Đơn vị','Trường Công nghệ Thông tin &amp; Truyền thông, Đại học Bách Khoa Hà Nội (2024)'],
      ['Chương sử dụng','Chương 2: Hệ sinh thái Hadoop, tr. 23–36'],
      ['Phân công','Thầy Tạ Duy Hoàng: Nhóm 1 phụ trách Chương 2 (thông báo 05/10, trình bày từ tuần 12/10)']])}
"""))

# ===================== PHẦN 8 (BONUS): Ứng dụng liên ngành =====================
SLIDES.append(divider(8, 8, "Bonus: Ứng dụng liên ngành", [
    "Bài toán: tìm điểm chia cây quyết định", "Vì sao cần kỹ thuật streaming (sketch)",
    "Vì sao cần mô hình tính toán song song lớn (MPC)", "3 bài báo của giảng viên môn học",
    "Tài liệu tham khảo mở rộng (8 bài báo gốc)"]))

SLIDES.append(slide("Bài toán: tìm điểm chia cây quyết định", f"""
<p>Khi dựng <b>cây quyết định</b> từ trên xuống (CART, ID3), ở mỗi nút phải chọn <b>ngưỡng chia</b> $j$ trên 1 thuộc tính
($x_i \\le j$ hay $x_i &gt; j$) sao cho sai số sau chia nhỏ nhất: MSE (hồi quy), tỉ lệ phân loại sai hoặc Gini (phân loại).</p>
{tbl(['Ý của bài báo','Hệ quả'],
     [['Chọn ngưỡng chia tối ưu = dựng cây sâu 1 (<i>decision stump</i>), cũng là weak learner của AdaBoost','Lặp lại thuật toán này để dựng cây sâu hơn'],
      ['Mỗi lần tính sai số tại $j$ chỉ cần <b>số phần tử (và nhãn) nằm trong 1 khoảng</b> của $[1,N]$','Bài toán quy về đếm theo khoảng trên dữ liệu rất lớn'],
      ['Nhiều thuộc tính: chạy riêng từng thuộc tính rồi chọn tốt nhất','Bộ nhớ nhân thêm hệ số $d$ (số thuộc tính)']])}
{callout('info', 'Liên hệ với môn học', 'Đếm theo khoảng cùng họ bài toán rank/quantile mà streaming đã học (q-digest, MRL, KLL). Lưu ý: chính các bài báo dùng <b>reservoir sampling</b> và <b>Count-Min sketch</b> (phân rã dyadic) chứ không dùng quantile sketch.')}
"""))

SLIDES.append(imgs_slide("Hình gốc: ví dụ chọn ngưỡng chia, optimal split j = 4", [
    ("ta_fig1_split.png", "Figure 1 (arXiv:2403.19867v4): trái là hồi quy (đường chấm là trung bình 2 nhóm), phải là phân loại; cả hai có ngưỡng tối ưu $j=4$.", 62),
    ("ta3_fig1.png", "Figure 1 (arXiv:2604.20394v2): $\\mu(j^\\star)$ và $\\gamma(j^\\star)$ là giá trị dự đoán của 2 phía ngưỡng $j^\\star$.", 30)],
    maxh=240, body_after=callout('info', 'Cách đọc', 'Chọn $j$ nghĩa là cắt trục $x$ làm 2 đoạn $[1,j]$ và $[j+1,N]$ rồi mỗi đoạn dự đoán bằng 1 giá trị (trung bình hoặc nhãn đa số). Sai số của mọi $j$ chỉ phụ thuộc số đếm trong 2 đoạn.')))

SLIDES.append(slide("Kết nối 1: động lực của streaming", f"""
<p>Theo bài báo: dữ liệu thường <b>quá lớn để nạp vào bộ nhớ chính của 1 máy</b>, nên được đọc dạng luồng từ đĩa hoặc qua mạng,
dùng bộ nhớ dưới tuyến tính, lý tưởng là <b>1 lượt duyệt</b> (cho phép vài lượt).</p>
{tbl(['Công cụ','Dùng để làm gì trong bài toán chọn ngưỡng chia'],
     [['Reservoir sampling / lấy mẫu','Ước lượng số phần tử và nhãn trong 1 khoảng $R\\subseteq[1,N]$ khi luồng chỉ có thêm phần tử'],
      ['Count-Min sketch + phân rã dyadic','Ước lượng số đếm theo khoảng, còn xử lý được luồng có xoá; thêm hệ số $\\log N$ về bộ nhớ'],
      ['Sai số cộng $\\varepsilon$ so với tối ưu','Đánh đổi bộ nhớ nhỏ (cỡ $\\tilde O(1/\\varepsilon)$ hoặc $\\tilde O(1/\\varepsilon^2)$) lấy ngưỡng "đủ tốt"']])}
"""))

SLIDES.append(slide("Kết nối 2: động lực của tính toán song song lớn", f"""
<p>Mô hình <b>MPC</b> (Massively Parallel Computation) trong bài báo là phép trừu tượng hoá của MapReduce, Hadoop và Spark:</p>
{tbl(['Thành phần MPC','Ý nghĩa','Ứng với Hadoop'],
     [['$m$ quan sát chia cho $m^{1-\\beta}$ máy','Dữ liệu phân tán, không máy nào giữ hết','Block của HDFS rải trên DataNode'],
      ['Mỗi máy chỉ có bộ nhớ $\\tilde O(m^{\\beta})$','Bộ nhớ mỗi máy dưới tuyến tính','Bộ nhớ mỗi container/task'],
      ['Mỗi vòng: mọi máy gửi/nhận thông điệp rồi tính cục bộ','Đồng bộ theo vòng','Map → Shuffle → Reduce'],
      ['Độ phức tạp = <b>số vòng</b>','Ít vòng = ít lần shuffle tốn kém','Số job MapReduce nối tiếp']])}
{callout('good', 'Kết quả của bài báo trong MPC', 'Hồi quy và phân loại: bộ nhớ mỗi máy $\\tilde O(\\sqrt m)$, chỉ $O(1)$ vòng, sai số $\\le \\mathrm{OPT}+1/\\sqrt m$ (bài 2, Figure 3).')}
"""))

SLIDES.append(slide("Hai thế giới gặp nhau", tbl(
    ["", "Streaming (nửa đầu môn học)", "Massively Parallel / Hadoop (Chương 2)"],
    [["Ràng buộc chính", "Bộ nhớ nhỏ, 1 hoặc vài lượt duyệt dữ liệu", "Mỗi máy bộ nhớ nhỏ, độ phức tạp tính bằng số vòng giao tiếp"],
     ["Công cụ trong bài báo", "Reservoir sampling, Count-Min sketch (dyadic)", "Thuật toán MPC: $O(1)$ vòng, đúng mô hình của MapReduce/Hadoop/Spark"],
     ["Mục tiêu chung", "Chọn ngưỡng chia cây quyết định sai số $\\le \\mathrm{OPT}+\\varepsilon$, tốn ít bộ nhớ nhất", "Cùng bài toán, tốn ít vòng giao tiếp nhất"]]
) + callout('warn', 'Điểm khác với công trình nền tảng', 'Domingos-Hulten (KDD 2000) giả định luồng vô hạn, dữ liệu i.i.d. và chỉ xét phân loại. Các bài của thầy không cần giả định đó, có cả hồi quy, và có đảm bảo chứng minh được.')))

SLIDES.append(slide("Bài báo 1: Finding Decision Tree Splits in Streaming and MPC (arXiv 2024)", f"""
<figure style="margin:6px 0 12px"><img src="../assets/images/papers/ta1_title.png" alt="Tên bài báo và tác giả" style="max-width:620px;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff"><figcaption style="font-size:.78rem;color:var(--muted);margin-top:4px">Trang đầu bài báo, arXiv:2403.19867v1 [cs.DS], 28/03/2024.</figcaption></figure>
{tblock('Bài toán &amp; kết quả chính', [
    'Đầu vào: 1 luồng quan sát <i>x</i><sub>i</sub> ∈ [N] cùng nhãn <i>y</i><sub>i</sub> ∈ [0, M] (hồi quy) hoặc {-1, +1} (phân loại).',
    'Mục tiêu: tìm ngưỡng chia j tối ưu, cực tiểu sai số bình phương trung bình (hồi quy) hoặc tỉ lệ phân loại sai (phân loại).',
    'Kết quả: nhiều thuật toán streaming dùng bộ nhớ dưới tuyến tính (sublinear) và số lượt duyệt dữ liệu nhỏ, mở rộng được sang mô hình <b>Massively Parallel Computation (MPC)</b> — bài báo gọi đây là phép trừu tượng hoá của MapReduce, Hadoop và Spark.',
    'Bổ sung cho công trình nền tảng của Domingos &amp; Hulten (KDD 2000) về học cây quyết định trên luồng dữ liệu.'])}
"""))

SLIDES.append(slide("Bài báo 2: Constructing Decision Trees from Data Streams (ISIT 2025)", f"""
<figure style="margin:6px 0 12px"><img src="../assets/images/papers/ta2_title.png" alt="Tên bài báo và tác giả" style="max-width:560px;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff"><figcaption style="font-size:.78rem;color:var(--muted);margin-top:4px">Trang đầu bài báo, arXiv:2403.19867v4 [cs.DS], 16/04/2025, công bố tại ISIT 2025 (cùng mã arXiv với bài 1, bản sửa đổi sâu, đổi tên).</figcaption></figure>
{tblock('Khác biệt so với bài báo 1', [
    'Bỏ giả định dữ liệu <i>i.i.d.</i> (độc lập, cùng phân phối) mà bài báo 1 vẫn dùng.',
    'Thêm tiêu chí Gini impurity cho bài toán phân loại, bên cạnh sai số bình phương trung bình và tỉ lệ phân loại sai.',
    'Mục tiêu mở rộng: không chỉ tìm 1 điểm chia mà <b>dựng cả cây quyết định</b> trực tiếp từ luồng dữ liệu.',
    'Mở rộng thuật toán sang đúng mô hình <b>MapReduce</b> (thay vì MPC tổng quát ở bài báo 1).'])}
"""))

SLIDES.append(slide("Bài báo 3: Nearly Optimal Bounds for Decision Tree Splits (ESA 2026)", f"""
<figure style="margin:6px 0 12px"><img src="../assets/images/papers/ta3_title.png" alt="Tên bài báo và tác giả" style="max-width:560px;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff"><figcaption style="font-size:.78rem;color:var(--muted);margin-top:4px">Trang đầu bài báo, arXiv:2604.20394v2 [cs.DS], 07/07/2026, công bố tại ESA 2026.</figcaption></figure>
{tblock('Cận trên &amp; cận dưới gần tối ưu', [
    'Hồi quy (nhãn trong {0,…,M}): thuật toán 1 lượt duyệt, bộ nhớ Õ(M²/ε), sai số cộng ε so với điểm chia tối ưu — cải tiến thuật toán 2 lượt duyệt của Phạm &amp; cộng sự (ISIT 2025, chính là bài báo 2).',
    'Cận dưới khớp: chứng minh Ω(M²/ε) bộ nhớ là cần thiết, suy ra bằng reduction từ bài toán Index.',
    'Phân loại: thuật toán 1 lượt duyệt, bộ nhớ Õ(1/ε) cho điểm chia Gini tối ưu — cải tiến thuật toán Õ(1/ε²) trước đó; cận dưới khớp Ω(1/ε) (Gini) và Ω(1/ε) (tỉ lệ phân loại sai).',
    'Kỹ thuật: khai thác tính Lipschitz của hàm mất mát, kết hợp reservoir sampling với Count–Min sketch hỗ trợ truy vấn khoảng (range query).'])}
"""))

SLIDES.append(slide("Hình gốc: bảng kết quả streaming và MPC dùng chung tham số $\\beta$", """<div style="display:flex;flex-direction:column;align-items:center;gap:12px">
<figure style="margin:0;width:62%"><img src="../assets/images/papers/ta_fig2_stream.png" alt="" style="width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff"><figcaption style="font-size:.76rem;color:var(--muted);margin-top:4px">Figure 2 (arXiv:2403.19867v4): streaming, cột Space và No. of passes.</figcaption></figure>
<figure style="margin:0;width:62%"><img src="../assets/images/papers/ta_fig3_mpc.png" alt="" style="width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff"><figcaption style="font-size:.76rem;color:var(--muted);margin-top:4px">Figure 3 (cùng bài): MPC, cột Space per machine và No. of rounds.</figcaption></figure></div>"""))

SLIDES.append(slide("Streaming và MPC trả giá cho cùng một phép đếm theo khoảng", f"""
<p style="margin:0 0 8px">Mọi ngưỡng $j$ chỉ cần các số đếm $f_R$ (kèm nhãn) trên khoảng $R\\subseteq[1,N]$. Hai mô hình khác nhau ở thứ phải <b>trả giá</b>:</p>
{tbl(['', 'Streaming', 'MPC (MapReduce, Hadoop, Spark)'],
     [['Tài nguyên khan hiếm', 'Bộ nhớ của 1 máy', 'Bộ nhớ $\\\\tilde O(m^{{\\\\beta}})$ của <i>mỗi</i> máy, $m^{{1-\\\\beta}}$ máy'],
      ['Chi phí được đếm', 'Số lượt duyệt (pass)', 'Số vòng giao tiếp (round)'],
      ['Ví dụ trong bài', '1 lượt, $\\\\tilde O(M^2/\\\\varepsilon)$ (bài 3)', '$O(1)$ vòng, $\\\\tilde O(\\\\sqrt m)$/máy; hoặc $O(1/\\\\beta)$ vòng, $\\\\tilde O(m^{{\\\\beta}}/\\\\varepsilon^2)$/máy (bài 2)']], dense=True)}
{callout('info', 'Đánh đổi nằm ngay trong công thức', 'Chọn $\\\\beta$ nhỏ để mỗi máy dùng ít bộ nhớ thì số vòng $O(1/\\\\beta)$ tăng. "Vòng" đắt vì (Figure 1, bài MapReduce) map ghi file trung gian lên <b>đĩa cục bộ</b> rồi reduce đọc từ xa: mỗi vòng thêm là 1 lần shuffle qua mạng.')}
"""))

SLIDES.append(slide("Streaming đã có cận dưới khớp, MPC thì các bài đã đọc chưa có", f"""
{tbl(['Điểm nối', 'Căn cứ', 'Mức chắc chắn'],
     [['Sắp xếp theo $x$ trong $O(1)$ vòng là bước đầu của thuật toán MPC', 'Bài 1, mục 4; bài MapReduce có ví dụ <i>Distributed Sort</i>', 'Nêu trong bài'],
      ['MPC là phép trừu tượng hoá MapReduce, Hadoop, Spark', 'Bài 2, mục 1', 'Nêu trong bài'],
      ['Count-Min cộng được từng ô: mỗi mapper dựng sketch riêng, reducer cộng lại (như <i>combiner</i>)', 'Tính chất đã biết của Count-Min', 'Suy luận của nhóm']], dense=True)}
{callout('good', 'Đã chứng minh (streaming, bài 3)', 'Hồi quy: 1 lượt cần $\\\\Omega(M^2/\\\\varepsilon)$ bộ nhớ, thuật toán $\\\\tilde O(M^2/\\\\varepsilon)$ đạt đúng mức đó. Phân loại: $\\\\Omega(1/\\\\varepsilon)$ khớp $\\\\tilde O(1/\\\\varepsilon)$. <b>Còn mở:</b> bài 3 không nhắc MPC, bảng MPC của bài 2 chỉ có cận trên.')}
"""))

REFS = [
    ["[1]", "S. Ghemawat, H. Gobioff, S.-T. Leung. <i>The Google File System.</i> SOSP 2003.", "HDFS (Phần 1–2)"],
    ["[2]", "J. Dean, S. Ghemawat. <i>MapReduce: Simplified Data Processing on Large Clusters.</i> OSDI 2004.", "MapReduce (Phần 1, 3)"],
    ["[3]", "F. Chang et al. <i>Bigtable: A Distributed Storage System for Structured Data.</i> OSDI 2006.", "HBase (Phần 5)"],
    ["[4]", "M. Burrows. <i>The Chubby lock service for loosely-coupled distributed systems.</i> OSDI 2006.", "ZooKeeper / ZAB (Phần 6)"],
    ["[5]", "J. Kreps, N. Narkhede, J. Rao. <i>Kafka: a Distributed Messaging System for Log Processing.</i> NetDB 2011.", "Kafka (Phần 6)"],
    ["[6]", "H. Phạm, H. Ta, H. T. Vu. <i>Finding Decision Tree Splits in Streaming and Massively Parallel Models.</i> arXiv:2403.19867v1, 2024.", "Bonus (Phần 8)"],
    ["[7]", "H. Phạm, H. Ta, H. T. Vu. <i>Constructing Decision Trees from Data Streams.</i> ISIT 2025 (arXiv:2403.19867v4).", "Bonus (Phần 8)"],
    ["[8]", "H. Ta, H. T. Vu. <i>Nearly Optimal Bounds for Computing Decision Tree Splits in Data Streams.</i> ESA 2026 (arXiv:2604.20394v2).", "Bonus (Phần 8)"],
]
SLIDES.append(slide("Tài liệu tham khảo mở rộng (ngoài giáo trình)", f"""
<p>Ngoài giáo trình chính (Chương 2, tr.23–36, xem slide Tài liệu tham khảo ở Phần 7), nội dung liên hệ tới <b>8 bài báo gốc</b>
sau: 5 bài nền tảng của từng công nghệ Apache, 3 bài nghiên cứu của giảng viên môn học dùng ở phần bonus.</p>
{tbl(["#", "Trích dẫn", "Dùng ở"], REFS, dense=True)}
<p style="color:var(--muted);font-size:.82rem">Bản PDF cả 8 bài báo: nhóm đã tải về, đọc trực tiếp phần Abstract và Introduction (mục 1) của từng bài, không trích dẫn gián tiếp qua nguồn thứ cấp.</p>
"""))

SLIDES.append(f"""<div class="mdeck-slide"><div class="kicker">Cảm ơn đã theo dõi</div>
<h2>Nhóm 1: Hệ sinh thái Hadoop</h2>
<p>{" · ".join(MEMBERS)}</p>
<p style="color:var(--muted)">Môn Lưu trữ &amp; xử lý dữ liệu lớn, giảng viên Tạ Duy Hoàng</p></div>""")

# ---- gắn logo công nghệ vào góc phải các slide tương ứng ----
LOGO_FOR = [("Nguồn gốc: 2 bài báo", "google.svg"), ("Bốn thành phần cốt lõi", "apachehadoop.svg"), ("Scale-out so với", "apachehadoop.svg"),
            ("Mục tiêu thiết kế của HDFS", "apachehadoop.svg"), ("Kiến trúc master/slave", "apachehadoop.svg"), ("Khái niệm block", "apachehadoop.svg"),
            ("Cơ chế nhân bản", "apachehadoop.svg"), ("NameNode và rủi ro", "apachehadoop.svg"), ("Hạn chế của HDFS", "apachehadoop.svg"),
            ("Mô hình lập trình MapReduce", "apachehadoop.svg"), ("Vai trò MapReduce", "apachehadoop.svg"), ("MapReduce tích hợp", "apachehadoop.svg"),
            ("Lý do tách YARN", "apachehadoop.svg"), ("Quy trình 1 ứng dụng", "apachehadoop.svg"), ("Lợi ích YARN", "apachehadoop.svg"),
            ("Tiêu chí chọn giữa HDFS", "apachehbase.svg"), ("Toàn cảnh hệ sinh thái", "apachehadoop.svg"), ("Tổng kết chương 2", "apachehadoop.svg"),
            ("Lộ trình phát triển", "apachehadoop.svg"), ("Ví dụ minh hoạ: dung lượng", "apachehadoop.svg"),
            ("Hình gốc: cách Bigtable", "apachehbase.svg"), ("Hình gốc: tablet được lưu", "apachehbase.svg"),
            ("Hình gốc: luồng ghi của GFS", "apachehadoop.svg"), ("Hình gốc: MapReduce lan nhanh", "google.svg"),
            ("Hình gốc: Chubby xử lý", "zookeeper.svg"), ("Hình gốc: Kafka tại LinkedIn", "apachekafka.svg"),
            ("Tài liệu tham khảo mở rộng", "google.svg"),
            ("Tổng quan Apache Hadoop", "apachehadoop.svg"), ("Kiến trúc YARN", "apachehadoop.svg"), ("Hình gốc: kiến trúc GFS", "apachehadoop.svg"),
            ("Hình gốc: luồng thực thi MapReduce", "apachehadoop.svg"),
            ("Apache Hive", "apachehive.svg"), ("Cơ chế hoạt động của Hive", "apachehive.svg"), ("Apache Pig", "pig.gif"),
            ("Apache HBase", "apachehbase.svg"), ("Điểm khác biệt giữa HBase", "apachehbase.svg"), ("Hình gốc: mô hình dữ liệu Bigtable", "apachehbase.svg"),
            ("Apache Sqoop", "sqoop.png"), ("Quy trình Sqoop", "sqoop.png"),
            ("Apache Kafka", "apachekafka.svg"), ("Ví dụ minh hoạ: Kafka", "apachekafka.svg"), ("Hình gốc: log của Kafka", "apachekafka.svg"),
            ("Apache Oozie", "oozie.png"), ("Apache ZooKeeper", "zookeeper.svg"), ("Cơ sở tin cậy của ZooKeeper", "zookeeper.svg"),
            ("Vị trí của ZooKeeper", "zookeeper.svg"), ("Hình gốc: cấu trúc Chubby", "zookeeper.svg")]
for _i, _s in enumerate(SLIDES):
    _m = re.search(r"<h2>(.*?)</h2>", _s)
    if not _m or 'part-divider' in _s[:80]:
        continue
    for _pref, _f in LOGO_FOR:
        if _m.group(1).startswith(_pref):
            SLIDES[_i] = _s.replace('<div class="mdeck-slide">',
                f'<div class="mdeck-slide has-logo"><img class="tech-logo" src="../assets/images/logos/{_f}" alt="logo">', 1)
            break

# ---- áp theme HUST: cover, divider, nội dung (xoay 4 biến thể theo từng Phần), kết ----
_part = -1
for _i, _s in enumerate(SLIDES):
    if _i == 0:
        _cls = "cover"
    elif _i == len(SLIDES) - 1:
        _cls = "endcard"
    elif 'part-divider' in _s[:90]:
        _part += 1
        continue
    else:
        _cls = f"th{max(_part, 0) % 4}"
    _s2 = re.sub(r'<div class="mdeck-slide( [^"]*)?">', lambda m: f'<div class="mdeck-slide{m.group(1) or ""} {_cls}">', _s, count=1)
    if _cls.startswith("th"):
        _s2 = _s2.replace('</h2>', '</h2><img class="hust-emblem" src="../assets/images/hust_logo.png" alt="HUST">', 1)
    SLIDES[_i] = _s2

SLIDES[0] = SLIDES[0].replace("__SLIDE_COUNT__", str(len(SLIDES)))

DECK = f"""<div class="mdeck"><div class="mdeck-canvas-wrap"><div class="mdeck-viewport">{''.join(SLIDES)}</div></div>
<div class="mdeck-bar">
  <button class="mdeck-prev">◀ Trước</button><button class="mdeck-next">Sau ▶</button>
  <span class="mdeck-count"></span><div class="mdeck-dots"></div>
  <button class="mdeck-fs">⛶ Toàn màn hình</button>
</div></div>"""

rel_lang = ""
rel_root = "../"
# Theme HUST (đỏ chính thức #ce1628, theo beamerthemeHUST.sty của nhóm) — chỉ override biến màu
# --accent/--accent2 CỤC BỘ cho trang này qua <style> riêng, không chỉnh _shared/common.css chung.
HUST_THEME = """<style>
:root{--accent:#ce1628;--accent2:#8a0f1f}
:root[data-theme="dark"]{--accent:#ff5a68;--accent2:#ffb3b8}
.hust-logo-row{display:flex;align-items:center;gap:16px;margin-bottom:8px}
.hust-logo-row img{height:56px;width:auto}
.tech-logo{position:absolute;top:24px;right:40px;height:56px;max-width:170px;width:auto;object-fit:contain;background:#fff;border:1px solid var(--border);border-radius:8px;padding:4px 8px}

/* ---- Theme slide HUST (nền Beamer HUST: băng navy + đường đỏ, logo chân trang) ---- */
.mdeck-slide{--text:#1b2433;--muted:#566074;--panel:#fff;--border:#d5dae6;--code:#eef2fa;--hred:#ce1628;--hnavy:#003366;
  color:var(--text);background-color:#fff;background-size:100% 100%;background-repeat:no-repeat;padding:104px 60px 66px}
.mdeck-slide.th0{background-image:url(../assets/images/hust-theme/content-full.png)}
.mdeck-slide.th1{background-image:url(../assets/images/hust-theme/content-hust-full.png)}
.mdeck-slide.th2{background-image:url(../assets/images/hust-theme/content-logo.png)}
.mdeck-slide.th3{background-image:url(../assets/images/hust-theme/content-hust.png)}
.mdeck-slide.th0 h2,.mdeck-slide.th1 h2,.mdeck-slide.th2 h2,.mdeck-slide.th3 h2{position:absolute;left:60px;right:96px;top:0;height:68px;
  margin:0;display:flex;align-items:center;color:#fff;font-size:1.42rem;line-height:1.15}
.mdeck-slide.has-logo h2{right:230px;padding-right:0}
.mdeck-slide .hust-emblem{position:absolute;top:6px;right:20px;height:56px;width:auto}
.mdeck-slide.part-divider{background-image:url(../assets/images/hust-theme/section.png);padding:0 80px}
.mdeck-slide.part-divider h2{position:static;color:#fff}
.mdeck-slide.cover{background-image:url(../assets/images/hust-theme/title.png);padding:150px 560px 70px 70px;align-items:flex-start}
.mdeck-slide.cover h2{font-size:2.3rem}
.mdeck-slide.endcard{background-image:url(../assets/images/hust-theme/end-empty.png);padding:150px 60px 70px 540px;align-items:flex-start}
.mdeck-slide b,.mdeck-slide strong{color:var(--hred)}
.mdeck-slide.part-divider b,.mdeck-slide.part-divider strong{color:#fff}
.mdeck-slide p,.mdeck-slide li{font-size:1.04rem;line-height:1.42}
.mdeck-slide table{font-size:.92rem}
.mdeck-slide table.dense{font-size:.8rem}
.mdeck-slide h3{font-size:1.12rem}
.tblock{border-color:var(--hnavy)}.tblock .tblock-h{background:var(--hnavy)}
.tech-logo{top:6px;right:90px;height:56px}

.tblock{border:1px solid var(--accent);border-radius:10px;overflow:hidden;margin:10px 0;background:var(--panel)}
.tblock .tblock-h{background:var(--accent);color:#fff;font-weight:800;padding:7px 16px;font-size:.98rem}
.tblock ol{margin:0;padding:10px 16px 10px 34px}
.tblock li{margin:5px 0;line-height:1.45}
</style>"""
body = f"""<div class="hero"><div class="hust-logo-row"><img src="{rel_root}assets/images/hust_logo.png" alt="Logo Đại học Bách Khoa Hà Nội"></div>
<div class="kicker">Bài tập lớn · Nhóm 1</div>
<h1>Hệ sinh thái Hadoop: Chương 2</h1>
<p>Slide thuyết trình môn <b>Lưu trữ &amp; xử lý dữ liệu lớn</b> (giảng viên Tạ Duy Hoàng), nhóm {", ".join(MEMBERS)}.
Nội dung bám sát 100% Chương 2 giáo trình chính thức của môn học (IT4931_lecture_notes.pdf, tr.23–36), không bổ sung nội dung ngoài phạm vi sách.</p></div>
{DECK}
<div class="callout info" style="margin-top:20px"><div class="lbl">Nguồn</div>
Trần Văn Đặng, Nguyễn Hữu Đức, Nguyễn Bình Minh, Trần Việt Trung. <i>Lưu trữ và Xử lý Dữ liệu Lớn</i>, Chương 2: Hệ sinh thái Hadoop, tr.23–36. Trường CNTT&amp;TT, ĐH Bách Khoa Hà Nội, 2024.
&nbsp;·&nbsp; <a href="../data/source/IT4931_lecture_notes.pdf" target="_blank">📄 Xem giáo trình gốc (PDF)</a>
<div style="margin-top:10px"><b>Tám bài báo gốc dùng trong bài (bản PDF):</b>
<ol style="margin:6px 0 0;padding-left:22px;line-height:1.55;font-size:.92rem">
<li>S. Ghemawat, H. Gobioff, S.-T. Leung. <i>The Google File System.</i> SOSP 2003. <a href="../data/source/papers/GFS_Ghemawat2003.pdf" target="_blank">📄 PDF</a></li>
<li>J. Dean, S. Ghemawat. <i>MapReduce: Simplified Data Processing on Large Clusters.</i> OSDI 2004. <a href="../data/source/papers/MapReduce_Dean2004.pdf" target="_blank">📄 PDF</a></li>
<li>F. Chang et al. <i>Bigtable: A Distributed Storage System for Structured Data.</i> OSDI 2006. <a href="../data/source/papers/Bigtable_Chang2006.pdf" target="_blank">📄 PDF</a></li>
<li>M. Burrows. <i>The Chubby lock service for loosely-coupled distributed systems.</i> OSDI 2006. <a href="../data/source/papers/Chubby_Burrows2006.pdf" target="_blank">📄 PDF</a></li>
<li>J. Kreps, N. Narkhede, J. Rao. <i>Kafka: a Distributed Messaging System for Log Processing.</i> NetDB 2011. <a href="../data/source/papers/Kafka_Kreps2011.pdf" target="_blank">📄 PDF</a></li>
<li>H. Phạm, H. Ta, H. T. Vu. <i>Finding Decision Tree Splits in Streaming and Massively Parallel Models.</i> arXiv:2403.19867v1, 2024. <a href="../data/source/papers/Pham_Ta_Vu_2024_arXiv2403.19867v1.pdf" target="_blank">📄 PDF</a></li>
<li>H. Phạm, H. Ta, H. T. Vu. <i>Constructing Decision Trees from Data Streams.</i> ISIT 2025 (arXiv:2403.19867v4). <a href="../data/source/papers/Pham_Ta_Vu_2025_arXiv2403.19867v4.pdf" target="_blank">📄 PDF</a></li>
<li>H. Ta, H. T. Vu. <i>Nearly Optimal Bounds for Computing Decision Tree Splits in Data Streams.</i> ESA 2026 (arXiv:2604.20394v2). <a href="../data/source/papers/Ta_Vu_2026_arXiv2604.20394v2.pdf" target="_blank">📄 PDF</a></li>
</ol></div></div>
"""

html = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{HEAD_THEME_SCRIPT}
<title>Nhóm 1: Hệ sinh thái Hadoop (Chương 2)</title>
<link rel="stylesheet" href="{rel_root}_shared/common.css">
<link rel="stylesheet" href="{rel_root}_shared/deck.css">
<link rel="stylesheet" href="{rel_root}_shared/glossary.css">
{KATEX}
{HUST_THEME}
</head>
<body>
{topbar(rel_lang, rel_root)}
<div class="wrap">
{body}
</div>
{footer(rel_root)}
<script src="{rel_root}_shared/deck.js"></script>
<script src="{rel_root}_shared/glossary.js"></script>
</body></html>"""

out = ROOT / "vi" / "group-1-slides.html"
out.write_text(html, encoding="utf-8")
print(f"Đã sinh {out} ({len(SLIDES)} slide)")
