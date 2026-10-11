# -*- coding: utf-8 -*-
"""Sinh 1 file slide TỔNG HỢP riêng cho bộ tự học sâu "Hệ sinh thái Hadoop" (6 module hd-01..hd-06),
hoàn toàn TÁCH BIỆT khỏi group-1-slides.html gốc (không sửa file đó, không dùng chung script gen_group1.py).
Mục đích: 1 deck duy nhất để nhóm trình bày/ôn lại nhanh lịch sử - động lực - ảnh hưởng của cả Chương 2,
kèm 1 dòng thời gian tổng hợp ở cuối. Nội dung tóm lược lại đúng các fact đã trích nguồn trong
hadoop_deepdive_content.py — không thêm fact mới ở đây."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen_site import HEAD_THEME_SCRIPT, KATEX, topbar, footer

ROOT = pathlib.Path(__file__).parent.parent

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

def callout(kind, label, text):
    return f'<div class="callout {kind}"><div class="lbl">{label}</div>{text}</div>'

SLIDES = []

# ---------- Title ----------
SLIDES.append(f"""<div class="mdeck-slide"><div class="kicker">IT4931: Lưu trữ &amp; xử lý dữ liệu lớn · Tự học sâu Chương 2</div>
<h2>Hệ sinh thái Hadoop: Lịch sử, Động lực, Ảnh hưởng</h2>
<p style="font-size:1.05rem;color:var(--muted)">Bản deep-dive riêng cho nhóm tự học — tách biệt hoàn toàn khỏi
slide thuyết trình bài tập lớn của Nhóm 1 (group-1-slides.html)</p>
<p style="color:var(--muted);font-size:.9rem">Giảng viên: Tạ Duy Hoàng &nbsp;·&nbsp; Môn Lưu trữ &amp; xử lý dữ liệu lớn &nbsp;·&nbsp; __SLIDE_COUNT__ slide</p></div>""")

SLIDES.append(slide("Vì sao có bản deck này?", f"""
<p>Nhóm đã đọc <i>group-1-slides.html</i> (55 slide bám đúng Chương 2 giáo trình, tr.23–36) và nhận xét
<i>"nửa sau đúng không hiểu gì"</i>. Bản deck này KHÔNG lặp lại Chương 2 — nó trả lời 3 câu hỏi mà Chương 2
không trả lời: công nghệ này <b>ra đời từ đâu</b>, <b>vì động lực gì</b>, và <b>ảnh hưởng tới thế giới ra sao</b>.</p>
{tbl(["Phần","Công nghệ","Trọng tâm"],
     [["1","Hadoop &amp; HDFS","Nutch → 2 paper Google → Yahoo → kiến trúc Master/Slave"],
      ["2","MapReduce &amp; YARN","Mô hình Google 2004 → JobTracker nghẽn → YARN 2012"],
      ["3","Pig &amp; Hive","Yahoo Research vs Facebook — 2 triết lý ngôn ngữ khác nhau"],
      ["4","HBase &amp; Sqoop","Bigtable → Powerset → Facebook Messages; cầu nối RDBMS↔Hadoop"],
      ["5","Kafka","LinkedIn 2010-2011 → log-centric architecture → Confluent"],
      ["6","Oozie &amp; ZooKeeper","Điều phối workflow; Chubby → ZAB → 'xương sống vô hình'"]])}
{callout('info','Mỗi module đầy đủ (lịch sử, ví dụ, demo tương tác, 11-12 câu quiz) nằm ở', 'site: mục "🐘 Hệ sinh thái Hadoop — Tự học sâu" trên trang chủ. Deck này chỉ tóm lược để trình bày/ôn nhanh.')}
"""))

# ===================== PHẦN 1: Hadoop & HDFS =====================
SLIDES.append(divider(1, 6, "Hadoop &amp; HDFS", [
    "Nutch (2002) không scale được → đọc 2 paper Google", "2006: Cutting vào Yahoo, Hadoop tách từ Nutch",
    "Tên: con voi nhồi bông của con trai Doug Cutting", "Kiến trúc Master/Slave: NameNode/DataNode, block, replication"]))

SLIDES.append(slide("Từ một công cụ tìm kiếm thất bại, tới chuẩn công nghiệp", f"""
<p>Doug Cutting &amp; Mike Cafarella xây <b>Nutch</b> (2002) — công cụ tìm kiếm mở không scale được. Đọc paper
<b>GFS</b> (2003) và <b>MapReduce</b> (2004) của Google, họ tách phần lưu trữ/xử lý ra thành dự án con
<b>Hadoop</b> (tháng 1/2006), ngay khi Cutting gia nhập Yahoo!.</p>
{callout('good','Tên Hadoop từ đâu?','Tên con voi nhồi bông của con trai Doug Cutting — tiêu chí: ngắn, dễ đọc, vô nghĩa, chưa ai dùng.')}
{callout('warn','Điểm yếu kiến trúc ban đầu','1 NameNode duy nhất giữ mọi metadata → Single Point of Failure ở Hadoop 1.0 (khắc phục bằng Standby NameNode ở Hadoop 2.0, KHÁC Secondary NameNode).')}
"""))

SLIDES.append(slide("HDFS: 2 quyết định thiết kế quyết định tất cả", tbl(
    ["Quyết định", "Giá trị", "Vì sao"],
    [["Block size", "64MB → 128MB", "Giảm số entry metadata trên NameNode"],
     ["Hệ số nhân bản", "3 bản sao/block, trên 3 DataNode khác nhau", "Chịu lỗi qua dư thừa, không ngăn lỗi phần cứng"]]
) + callout('info','🌍 Ảnh hưởng tới thế giới','2008: Hadoop thành top-level Apache project → Cloudera (2008), Hortonworks (2011) → đặt nền tảng cho data lake/lakehouse (S3+EMR, Delta Lake, Iceberg) ngày nay.')))

# ===================== PHẦN 2: MapReduce & YARN =====================
SLIDES.append(divider(2, 6, "MapReduce &amp; YARN", [
    "MapReduce (Dean &amp; Ghemawat, Google 2004): Map→Shuffle&amp;Sort→Reduce",
    "Hadoop 1.0: JobTracker vừa quản lý tài nguyên vừa theo dõi job → nghẽn, SPOF",
    "YARN (Hadoop 2.0, 2012): tách ResourceManager / NodeManager / ApplicationMaster"]))

SLIDES.append(slide("JobTracker: khi 1 thành phần làm quá nhiều việc", f"""
<p>Hadoop 1.0: <b>JobTracker</b> (1 node duy nhất) vừa quản lý tài nguyên cụm, vừa theo dõi tiến trình MỌI
MapReduce job. Giới hạn thực tế: ~4.000 node, ~40.000 task đồng thời — vượt ngưỡng này là nghẽn.</p>
{callout('good','YARN sửa gì?','ResourceManager (tài nguyên toàn cụm) + NodeManager (mỗi node) + ApplicationMaster (MỖI JOB có 1 cái riêng) — phân tán trách nhiệm theo dõi tiến trình ra từng job.')}
{callout('info','🌍 Ảnh hưởng tới thế giới','Tách "cấp phát tài nguyên" khỏi "logic ứng dụng" là ý tưởng lặp lại 10 năm sau ở quy mô lớn hơn: Kubernetes (Google, 2014, dựa trên Borg). Nhờ YARN, Spark dần thay MapReduce làm engine xử lý chính mà không cần xây lại cụm.')}
"""))

# ===================== PHẦN 3: Pig & Hive =====================
SLIDES.append(divider(3, 6, "Pig &amp; Hive", [
    "Pig (Yahoo Research, ~2006): PigLatin — thủ tục, giữa SQL và MapReduce thuần",
    "Hive (Facebook, Sen Sarma &amp; Thusoo, phát hành 10/2010): HiveQL — khai báo như SQL",
    "Cùng giải 1 vấn đề (viết MapReduce tay quá cực), 2 triết lý ngôn ngữ khác nhau"]))

SLIDES.append(slide("Từ 6 người dùng tới 20-30% cả công ty", f"""
<p>Facebook 2006: dữ liệu vào Hadoop tăng từ vài chục GB/ngày lên ~15 TB/ngày trong vài năm. Khi 15PB nằm
trong warehouse, chỉ <b>6 người</b> dùng được (phải biết viết MapReduce Java). Tới khi Thusoo rời Facebook
(2011): <b>20-30% toàn công ty</b> dùng hạ tầng phân tích mỗi tháng — nhờ HiveQL.</p>
{tbl(["","Pig (PigLatin)","Hive (HiveQL)"],[["Phong cách","Thủ tục (dataflow)","Khai báo (giống SQL)"],["Thế mạnh","Join/transform nhiều bước","Truy vấn tổng hợp, báo cáo"]])}
{callout('info','🌍 Di sản lớn nhất của Hive không phải HiveQL','Hive Metastore (catalog schema) trở thành chuẩn de-facto mà Presto/Trino/Spark SQL ngày nay đều tương thích — hạ tầng "âm thầm" sống lâu hơn ngôn ngữ truy vấn.')}
"""))

# ===================== PHẦN 4: HBase & Sqoop =====================
SLIDES.append(divider(4, 6, "HBase &amp; Sqoop", [
    "HBase (Powerset, phát hành 28/3/2008): mô phỏng Bigtable (Google, 2006) cho NLP search",
    "Facebook Messages (11/2010): ca sử dụng nổi tiếng nhất — nhưng đã migrate sang MyRocks (2018)",
    "Sqoop (Aaron Kimball, Cloudera, 5/2009): cầu nối RDBMS↔HDFS — bị retired vào Apache Attic 6/2021"]))

SLIDES.append(slide("Không công nghệ nào tồn tại mãi — và điều đó không sao cả", f"""
<p>HBase lấy cảm hứng trực tiếp từ paper <b>Bigtable</b> (Google, 2006); Powerset xây bản mã nguồn mở này cho
bài toán tìm kiếm ngôn ngữ tự nhiên. Facebook chọn HBase cho hệ thống Messages (11/2010) — minh chứng công
khai lớn nhất ở quy mô hàng trăm triệu người dùng ở thời điểm đó.</p>
{callout('warn','Bài học trung thực','Facebook migrate Messages sang MyRocks năm 2018. Sqoop — cầu nối RDBMS↔Hadoop của Cloudera (2009) — bị retired vào Apache Attic tháng 6/2021 khi CDC streaming (Debezium+Kafka) thay vai trò ETL batch của nó.')}
{callout('good','Thiết kế row key quan trọng thế nào','Dùng timestamp làm tiền tố row key → "hotspotting" (mọi row mới dồn vào 1 region) — đây là lỗi thiết kế schema HBase phổ biến nhất.')}
"""))

# ===================== PHẦN 5: Kafka =====================
SLIDES.append(divider(5, 6, "Apache Kafka", [
    "LinkedIn 2010-2011: Jay Kreps, Neha Narkhede, Jun Rao — Kreps viết phần lớn Kafka kỳ nghỉ Giáng sinh",
    "Kafka = log phân tán (giữ lại message), KHÔNG phải message queue truyền thống (xoá sau khi đọc)",
    "Confluent (2014, 500.000 USD từ LinkedIn) → IPO 2021, doanh thu &gt;300 triệu USD/năm"]))

SLIDES.append(slide("Từ bài toán activity-stream nội bộ, tới triết lý kiến trúc dữ liệu toàn ngành", f"""
<p>LinkedIn cần chuyển dữ liệu sự kiện (click, view, log) từ hàng trăm nguồn tới hàng trăm hệ thống tiêu thụ,
tin cậy và mở rộng được — công cụ pub-sub cũ không đáp ứng. Kafka ra đời như 1 <b>log bất biến</b>, không phải
hàng đợi thông thường.</p>
{callout('info','🌍 Ảnh hưởng tới thế giới','Khai sinh triết lý "event sourcing"/"log-centric architecture": log là nguồn sự thật duy nhất, mọi hệ thống khác là "view" xây lại từ đó. Nền tảng hạ tầng dữ liệu tại Uber, Netflix, Airbnb ngày nay.')}
{callout('good','🔗 Liên hệ lập lịch đã học','Bài toán gán/tái cân bằng partition cho consumer (RoundRobin/Range/Sticky) đã có demo tương tác đầy đủ ở Lập lịch 08-09 — Kafka không chỉ là lý thuyết, mà là hệ thống chạy thật ở quy mô triệu sự kiện/giây.')}
"""))

# ===================== PHẦN 6: Oozie & ZooKeeper + Tổng kết =====================
SLIDES.append(divider(6, 6, "Oozie, ZooKeeper &amp; Tổng kết", [
    "Oozie (Yahoo!, 2008): điều phối workflow DAG của nhiều job Hadoop phụ thuộc nhau",
    "ZooKeeper (Yahoo Research, ~2007): mô phỏng Chubby (Google) — ZAB (biến thể Paxos)",
    "Tổng kết: 1 dòng thời gian — hệ sinh thái KHÔNG do 1 công ty thiết kế từ đầu"]))

SLIDES.append(slide("ZooKeeper: \"xương sống vô hình\" của hệ phân tán", f"""
<p>ZooKeeper mô phỏng theo dịch vụ lock <b>Chubby</b> của Google (paper Mike Burrows), dùng <b>ZAB</b> (biến
thể Paxos) để đạt đồng thuận phân tán. 4 chức năng cốt lõi: quản lý thành viên nhóm, bầu cử leader, quản lý
cấu hình động, giám sát trạng thái hệ thống.</p>
{callout('warn','Vì sao "vô hình"','HBase (bầu leader region server), Kafka bản cũ trước KRaft, Solr (SolrCloud), Mesos đều phụ thuộc ZooKeeper — người dùng cuối không bao giờ thấy nó trực tiếp, nhưng khi nó lỗi, mọi hệ thống phía trên ngừng đúng.')}
"""))

SLIDES.append(slide("Dòng thời gian: hệ sinh thái Hadoop là lịch sử của NHIỀU công ty", tbl(
    ["Năm", "Công nghệ", "Nơi ra đời", "Bài toán nội bộ ban đầu"],
    [["2003-2004", "GFS, MapReduce (paper)", "Google", "Lưu trữ &amp; xử lý chỉ mục web quy mô Internet"],
     ["2006", "Hadoop (tách từ Nutch)", "Yahoo!", "Công cụ tìm kiếm mở không scale được"],
     ["2006-2008", "Pig", "Yahoo Research", "MapReduce quá cấp thấp cho nghiên cứu ad hoc"],
     ["2007", "ZooKeeper", "Yahoo Research", "Cần coordination phân tán kiểu Chubby"],
     ["2008", "HBase", "Powerset", "Tìm kiếm NLP cần CSDL kiểu Bigtable"],
     ["2008", "Oozie", "Yahoo!", "Điều phối nhiều job Hadoop phụ thuộc nhau"],
     ["2009", "Sqoop", "Cloudera", "Cầu nối RDBMS cũ ↔ Hadoop mới"],
     ["2010-2011", "Hive", "Facebook", "Data warehouse chỉ 6 người dùng được vì quá khó"],
     ["2010-2011", "Kafka", "LinkedIn", "Activity-stream bùng nổ, pub-sub cũ không chịu được"],
     ["2012", "YARN", "Yahoo!/Hortonworks", "JobTracker nghẽn, cần tách resource management"]]
)))

SLIDES.append(slide("Bài học lớn nhất của cả Chương 2", f"""
{callout('good', 'Không ai "thiết kế" cả hệ sinh thái này từ đầu', 'Mỗi công nghệ ra đời ở MỘT công ty khác nhau (Google, Yahoo, Powerset, Cloudera, Facebook, LinkedIn), để giải quyết MỘT bài toán nội bộ cụ thể — rồi được mã nguồn mở hoá và ghép lại qua Apache Software Foundation thành "hệ sinh thái".')}
<p>Đây là lý do học Chương 2 bằng cách nhớ "10 công nghệ" sẽ rất khó — nhưng học bằng cách hiểu <b>mỗi công
nghệ là lời giải cho đúng 1 bài toán cụ thể của đúng 1 công ty</b> thì mọi thứ khớp vào nhau tự nhiên.</p>
<p style="color:var(--muted)">Chi tiết đầy đủ (ví dụ từng bước, demo tương tác chạy thật, quiz 11-12 câu/module,
và nguồn trích dẫn cho MỌI fact lịch sử) nằm ở 6 module <code>hd-01..hd-06</code> trên trang chủ.</p>
"""))

SLIDES.append(f"""<div class="mdeck-slide"><div class="kicker">Hết phần tự học sâu</div>
<h2>Hệ sinh thái Hadoop: Lịch sử, Động lực, Ảnh hưởng</h2>
<p style="color:var(--muted)">Quay lại 6 module đầy đủ trên trang chủ để làm ví dụ, chạy demo, và làm quiz tự kiểm tra.</p></div>""")

SLIDES[0] = SLIDES[0].replace("__SLIDE_COUNT__", str(len(SLIDES)))

DECK = f"""<div class="mdeck"><div class="mdeck-canvas-wrap"><div class="mdeck-viewport">{''.join(SLIDES)}</div></div>
<div class="mdeck-bar">
  <button class="mdeck-prev">◀ Trước</button><button class="mdeck-next">Sau ▶</button>
  <span class="mdeck-count"></span><div class="mdeck-dots"></div>
  <button class="mdeck-fs">⛶ Toàn màn hình</button>
</div></div>"""

rel_lang = ""
rel_root = "../"
body = f"""<div class="hero"><div class="kicker">Tự học sâu · Chương 2</div>
<h1>Hệ sinh thái Hadoop: Lịch sử, Động lực, Ảnh hưởng</h1>
<p>Bản deck tổng hợp riêng cho nhóm tự học, tách biệt hoàn toàn khỏi slide thuyết trình bài tập lớn của Nhóm 1.
Mọi fact lịch sử trong deck này đã được trích nguồn đầy đủ trong 6 module chi tiết tương ứng (xem link cuối trang).</p></div>
{DECK}
<div class="callout info" style="margin-top:20px"><div class="lbl">Nguồn &amp; 6 module chi tiết</div>
Nội dung kỹ thuật cốt lõi: <i>IT4931_lecture_notes.pdf</i> (Chương 2, tr.23–36) và <i>materials/hangout/2024/2_hadoop_ecosystem_vn.pdf</i>.
Lịch sử/động lực/ảnh hưởng: xác nhận qua web search (xem từng module để có URL nguồn cụ thể).
&nbsp;·&nbsp; <a href="modules/hd-01-hadoop-hdfs/index.html">Hadoop 01</a> ·
<a href="modules/hd-02-mapreduce-yarn/index.html">02</a> ·
<a href="modules/hd-03-pig-hive/index.html">03</a> ·
<a href="modules/hd-04-hbase-sqoop/index.html">04</a> ·
<a href="modules/hd-05-kafka/index.html">05</a> ·
<a href="modules/hd-06-oozie-zookeeper/index.html">06</a>
&nbsp;·&nbsp; <a href="group-1-slides.html">Slide thuyết trình gốc của Nhóm 1 (Chương 2, không sửa)</a></div>
"""

html = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{HEAD_THEME_SCRIPT}
<title>Hệ sinh thái Hadoop: Lịch sử, Động lực, Ảnh hưởng — Tự học sâu</title>
<link rel="stylesheet" href="{rel_root}_shared/common.css">
<link rel="stylesheet" href="{rel_root}_shared/deck.css">
<link rel="stylesheet" href="{rel_root}_shared/glossary.css">
{KATEX}
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

out = ROOT / "vi" / "hadoop-deep-dive-slides.html"
out.write_text(html, encoding="utf-8")
print(f"Đã sinh {out} ({len(SLIDES)} slide)")
