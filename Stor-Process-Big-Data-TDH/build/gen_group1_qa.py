# -*- coding: utf-8 -*-
"""Sinh slide trả lời 10 câu hỏi ôn tập cuối Chương 2 (IT4931, tr.37-38) -> vi/group-1-slides-QA.html.
Tái dùng helper và theme HUST của gen_group1.py (đọc phần đầu file và khối CSS, không chạy lại deck gốc)."""
import pathlib, re, sys

HERE = pathlib.Path(__file__).parent
SRC = (HERE / "gen_group1.py").read_text(encoding="utf-8")
NS = {"__file__": str(HERE / "gen_group1.py"), "__name__": "gen_group1_helpers"}
exec(compile(SRC[:SRC.index("SLIDES = []")], "gen_group1_helpers", "exec"), NS)
slide, tbl, callout, tblock, logo_img = NS["slide"], NS["tbl"], NS["callout"], NS["tblock"], NS["logo_img"]
HEAD_THEME_SCRIPT, KATEX, topbar, footer, ROOT, MEMBERS = (NS[k] for k in
    ("HEAD_THEME_SCRIPT", "KATEX", "topbar", "footer", "ROOT", "MEMBERS"))
_a = SRC.index('HUST_THEME = """<style>')
_b = SRC.index("</style>\"\"\"", _a) + len("</style>\"\"\"")
exec(SRC[_a:_b], NS)
HUST_THEME = NS["HUST_THEME"] + """<style>
.qa-pre{margin:6px 0;padding:8px 12px;background:var(--code);border:1px solid var(--border);border-radius:8px;
  font:12.5px/1.4 ui-monospace,Menlo,Consolas,monospace;white-space:pre;overflow:hidden;color:#1b2433}
.qa-cols{display:flex;gap:16px;align-items:flex-start}.qa-cols>*{flex:1;min-width:0}
.qa-cap{font-size:.8rem;color:var(--muted);margin:2px 0 0}
.qa-q{font-size:.92rem;color:var(--muted);margin:0 0 8px}
</style>"""


def pre(code):
    code = code.strip("\n").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<pre class="qa-pre">{code}</pre>'


def cols(*parts):
    return '<div class="qa-cols">' + "".join(f"<div>{p}</div>" for p in parts) + "</div>"


def pipeline_svg():
    def box(x, y, w, h, txt, fill="#fff", stroke="#003366", bold=False):
        return (f'<foreignObject x="{x}" y="{y}" width="{w}" height="{h}"><div xmlns="http://www.w3.org/1999/xhtml" '
                f'style="box-sizing:border-box;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center;'
                f'text-align:center;background:{fill};border:2px solid {stroke};border-radius:10px;padding:4px 6px;'
                f'font:{"700" if bold else "600"} 13px sans-serif;color:#1b2433;line-height:1.2">{txt}</div></foreignObject>')
    def arrow(x1, y1, x2, y2, col="#566074"):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2" marker-end="url(#ar)"/>')
    s = ['<svg viewBox="0 0 1100 330" width="100%" role="img" aria-label="Pipeline phân tích log truy cập">',
         '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#566074"/></marker></defs>']
    s.append(box(8, 118, 130, 70, "Web server<br/>log click, xem, mua"))
    s.append(box(188, 118, 130, 70, "Kafka<br/>topic access_logs", "#fbeaec", "#ce1628", True))
    s.append(box(380, 28, 170, 70, "Flink / Spark Streaming", "#eef2fa"))
    s.append(box(380, 208, 170, 70, "Sink ghi HDFS<br/>(Spark, Kafka Connect)", "#eef2fa"))
    s.append(box(600, 28, 190, 70, "Chỉ số thời gian thực<br/>HBase (tra theo userID)"))
    s.append(box(600, 208, 170, 70, "HDFS<br/>Parquet dt/hour", "#fbeaec", "#ce1628", True))
    s.append(box(820, 208, 120, 70, "Hive<br/>bảng external", "#eef2fa"))
    s.append(box(970, 208, 122, 70, "Sqoop<br/>RDBMS, BI"))
    s += [arrow(138, 153, 186, 153), arrow(318, 140, 378, 70), arrow(318, 166, 378, 236),
          arrow(550, 63, 598, 63), arrow(550, 243, 598, 243), arrow(770, 243, 818, 243), arrow(940, 243, 968, 243)]
    s.append('<rect x="590" y="292" width="502" height="34" rx="8" fill="#003366"/>')
    s.append('<foreignObject x="590" y="292" width="502" height="34"><div xmlns="http://www.w3.org/1999/xhtml" '
             'style="height:34px;display:flex;align-items:center;justify-content:center;color:#fff;font:700 13px sans-serif">'
             'Oozie Coordinator: gộp file, thêm partition, HiveQL, Sqoop, báo lỗi</div></foreignObject>')
    s.append('</svg>')
    return "".join(s)


SL = []  # (số câu, html slide)


def add(q, title, body, kicker=None):
    SL.append((q, slide(title, body, kicker)))


# ---------------- mở đầu ----------------
SL.append((0, f"""<div class="mdeck-slide"><div class="kicker">IT4931: Lưu trữ &amp; xử lý dữ liệu lớn · Bài tập lớn</div>
<h2>Hệ sinh thái Hadoop: Trả lời câu hỏi ôn tập</h2>
<p style="font-size:1.05rem;color:var(--muted)">10 câu cuối Chương 2 (giáo trình tr.37–38)</p>
<p><b>Nhóm 1</b> · {" · ".join(MEMBERS)}</p>
<p style="color:var(--muted);font-size:.9rem">Giảng viên: Tạ Duy Hoàng &nbsp;·&nbsp; __SLIDE_COUNT__ slide</p></div>"""))

add(0, "Mười câu hỏi và hướng trả lời", tbl(
    ["Câu", "Nội dung", "Ý chính của đáp án"],
    [["1", "Kiến trúc tổng thể Hadoop", "HDFS lưu trữ, MapReduce xử lý, YARN quản lý tài nguyên"],
     ["2", "HDFS so với hệ tập tin UNIX", "Block lớn, ghi một lần đọc nhiều lần, metadata tách riêng"],
     ["3", "Chia block, nhân bản, NameNode và DataNode", "Block 128 MB, 3 bản sao, NameNode tự sao chép lại"],
     ["4", "Đặc điểm nổi bật của MapReduce", "Đơn giản, data locality, chịu lỗi tự động"],
     ["5", "Hive và Pig", "SQL-like cho phân tích, data flow cho ETL"],
     ["6", "Quy trình thực thi MapReduce", "Split, Map, Shuffle và Sort, Reduce"],
     ["7", "Tổng doanh số theo customer_id", "Map (customer_id, amount), Reduce cộng"],
     ["8", "Dữ liệu lệch (skew)", "Một khoá dồn vào một reducer; combiner, salting, skew join"],
     ["9", "Pipeline phân tích log", "Kafka, HDFS, Hive, Oozie, Spark hoặc Flink"],
     ["10", "Số dư cuối của mỗi account_id", "Deposit cộng, withdrawal trừ, rồi cộng theo khoá"]], dense=True))

# ---------------- Câu 1 ----------------
add(1, "Câu 1: Kiến trúc tổng thể của Hadoop", f"""
<p class="qa-q">Trình bày kiến trúc tổng thể của Hadoop; vai trò của HDFS, MapReduce và YARN.</p>
{tbl(['Thành phần', 'Vai trò'],
     [['HDFS', 'Lưu tệp lớn tin cậy trên cụm: chia block, nhân bản 3 lần'],
      ['MapReduce', 'Mô hình lập trình xử lý batch song song, người dùng chỉ viết Map và Reduce'],
      ['YARN', 'Quản lý tài nguyên và lập lịch, cho nhiều ứng dụng chạy chung một cụm'],
      ['Hadoop Common', 'Thư viện và tiện ích dùng chung']])}
{callout('good', 'Kiến trúc scale-out', 'Mở rộng bằng cách thêm máy phổ thông, coi hỏng hóc là bình thường: tự nhân bản dữ liệu, tự chuyển tác vụ sang node khác. <b>Hadoop 1.x:</b> MapReduce vừa xử lý vừa quản lý tài nguyên. <b>Hadoop 2.x:</b> YARN tách phần quản lý tài nguyên, MapReduce chỉ còn là một framework cạnh Spark, Flink, Tez.')}
""")

# ---------------- Câu 2 ----------------
add(2, "Câu 2: HDFS so với hệ tập tin UNIX", f"""
{tbl(['Tiêu chí', 'UNIX file system', 'HDFS'],
     [['Phạm vi', 'Một máy', 'Cụm hàng nghìn node'],
      ['Đơn vị lưu', 'Block cỡ 4 KB', 'Block 64 MB hoặc 128 MB'],
      ['Mô hình truy cập', 'Đọc ghi ngẫu nhiên, sửa tại chỗ (POSIX)', 'Ghi một lần, đọc nhiều lần; chỉ append ở cuối tệp'],
      ['Mục tiêu', 'Độ trễ thấp, đa dụng', 'Thông lượng cao cho tệp trăm MB đến TB'],
      ['Quản lý dữ liệu', 'Metadata và dữ liệu cùng một máy', 'NameNode giữ metadata trong RAM, DataNode giữ block'],
      ['Chịu lỗi', 'Dựa vào phần cứng (RAID, sao lưu)', 'Phần mềm: mỗi block nhân bản 3 DataNode'],
      ['Tệp nhỏ', 'Không vấn đề', 'Kém hiệu quả vì metadata nằm hết trong RAM NameNode']], dense=True)}
{callout('info', 'Đánh đổi', 'HDFS hy sinh một số tính năng POSIX để đổi lấy khả năng mở rộng và chịu lỗi ở quy mô petabyte.')}
""")

# ---------------- Câu 3 ----------------
add(3, "Câu 3: Chia block và nhân bản trong HDFS", f"""
{tblock('Quy trình', [
    'Tệp được chia thành các <b>block</b>, mặc định 64 MB hoặc 128 MB.',
    'Mỗi block nhân bản mặc định <b>3 bản</b> trên 3 DataNode khác nhau.',
    'Ví dụ tệp 1 GB, block 128 MB: <b>8 block</b>, <b>24 bản sao</b>, cần khoảng 3 GB dung lượng thật.',
    'Một DataNode hỏng: dữ liệu không mất vì còn bản ở node khác; NameNode tự điều phối sao chép lại cho đủ 3 bản.'])}
{callout('good', 'Tính sẵn sàng và chịu lỗi', 'Chịu lỗi nằm ở tầng phần mềm (nhân bản), không cần phần cứng đắt tiền và không cần quản trị viên can thiệp.')}
""")

add(3, "Câu 3: Vai trò của NameNode và DataNode", f"""
{tbl(['', 'NameNode (master)', 'DataNode (slave)'],
     [['Lưu gì', 'Metadata: cấu trúc thư mục, tên tệp, ánh xạ tệp sang block và vị trí', 'Các block dữ liệu thật'],
      ['Việc chính', 'Điều phối truy cập của client, phát hiện thiếu bản sao và ra lệnh sao chép lại', 'Xử lý trực tiếp yêu cầu đọc ghi của client, báo tình trạng về NameNode'],
      ['Khi đọc tệp', 'Trả về vị trí các block', 'Gửi dữ liệu thẳng cho client']])}
{callout('warn', 'Điểm lỗi duy nhất', 'NameNode giữ toàn bộ metadata. Secondary NameNode định kỳ sao lưu và hợp nhất edit log để phục hồi nhanh metadata; đây là điểm khôi phục, không phải bản sao chạy song song thay thế ngay.')}
""")

# ---------------- Câu 4 ----------------
add(4, "Câu 4: Đặc điểm nổi bật của MapReduce", f"""
{tbl(['Đặc điểm', 'Ý nghĩa trong môi trường phân tán'],
     [['Đơn giản', 'Lập trình viên chỉ viết hai hàm Map và Reduce'],
      ['Tự động hoá phần khó', 'Framework tự chia việc, phân phối tác vụ, thu gộp kết quả trung gian, xử lý lỗi'],
      ['Data locality', 'Đặt tác vụ gần nơi dữ liệu nằm, ít kéo dữ liệu qua mạng'],
      ['Minimal data exchange', 'Hạn chế trao đổi dữ liệu giữa các node'],
      ['Chịu lỗi tự động', 'Tác vụ của node hỏng được chạy lại ở node khác'],
      ['Mở rộng cao', 'Hàng nghìn node, hàng petabyte, xử lý theo lô'],
      ['Tích hợp hệ sinh thái', 'Hive, Pig, Sqoop đều dịch hoặc chạy thành job MapReduce']], dense=True)}
{callout('warn', 'Hạn chế', 'Độ trễ cao với tác vụ lặp và tương tác, nên có Spark và Flink; MapReduce vẫn phù hợp batch truyền thống.')}
""")

# ---------------- Câu 5 ----------------
add(5, "Câu 5: Vai trò của Hive và Pig", f"""
{tbl(['Tiêu chí', logo_img('apachehive.svg', 26) + ' Hive', logo_img('pig.gif', 28) + ' Pig'],
     [['Nguồn gốc', 'Facebook', 'Yahoo!'],
      ['Ngôn ngữ', 'HiveQL, gần SQL (SELECT, JOIN, GROUP BY)', 'Pig Latin, kịch bản mô tả luồng dữ liệu'],
      ['Mô hình', 'Bảng, schema-on-read trên HDFS', 'Chuỗi bước: đọc, lọc, biến đổi, gộp nhóm, join, sắp xếp'],
      ['Người dùng', 'Nhà phân tích quen SQL', 'Kỹ sư dữ liệu làm ETL phức tạp'],
      ['Thực thi', 'Dịch thành MapReduce, Tez hoặc Spark', 'Dịch thành chuỗi job MapReduce'],
      ['Độ trễ', 'Cỡ phút (batch)', 'Cỡ phút (batch)']], dense=True)}
""")

add(5, "Câu 5: Khi nào chọn Hive thay vì Pig", f"""
{tblock('Chọn Hive khi', [
    'Người dùng quen SQL và không muốn học lập trình.',
    'Dữ liệu dạng bảng, mục tiêu là báo cáo, tổng hợp, phân tích kinh doanh hoặc tích hợp công cụ BI.',
    'Chấp nhận độ trễ batch cỡ phút.'])}
{tblock('Chọn Pig khi', [
    'Cần nhiều bước biến đổi hoặc join phức tạp, viết thành một script tuần tự dễ bảo trì.',
    'Cần chèn logic riêng bằng UDF (Java, Python).'])}
{callout('info', 'Điểm chung', 'Cả hai đều nhằm đơn giản hoá việc dùng Hadoop và cuối cùng quy về job MapReduce chạy trên cụm.')}
""")

# ---------------- Câu 6 ----------------
add(6, "Câu 6: Các bước thực thi một chương trình MapReduce", f"""
{tbl(['Bước', 'Việc xảy ra'],
     [['1. Input split', 'Dữ liệu trên HDFS chia thành split, mỗi split giao một map task, ưu tiên chạy ở node giữ block'],
      ['2. Map', 'Đọc từng bản ghi, sinh cặp (key, value) trung gian, ghi ra đĩa cục bộ; Combiner có thể gộp cục bộ trước'],
      ['3. Shuffle', 'Chia cặp trung gian theo key cho các reducer (hash(key) mod R), reducer kéo phần của mình qua mạng; bước tốn kém nhất'],
      ['4. Sort', 'Mỗi reducer sắp theo key, gom thành (key, [value, ...])'],
      ['5. Reduce', 'Gọi hàm reduce cho từng key, ghi output lên HDFS, mỗi reducer một file']], dense=True)}
{callout('info', 'Chịu lỗi', 'Tác vụ lỗi hoặc node hỏng được framework tự chạy lại.')}
""")

add(6, "Câu 6: Ví dụ đếm từ (WordCount) với 2 split", f"""
{tbl(['Giai đoạn', 'Nội dung'],
     [['Split 1', '<code>hadoop hdfs hadoop</code>'],
      ['Split 2', '<code>hdfs yarn hadoop</code>'],
      ['Map', 'Map 1: (hadoop,1) (hdfs,1) (hadoop,1) &nbsp;|&nbsp; Map 2: (hdfs,1) (yarn,1) (hadoop,1)'],
      ['Shuffle và Sort (2 reducer)', 'R1: hadoop → [1,1,1] &nbsp;|&nbsp; R2: hdfs → [1,1], yarn → [1]'],
      ['Reduce', '(hadoop,3) (hdfs,2) (yarn,1)']])}
{callout('good', 'Với Combiner', 'Dùng chính hàm cộng làm Combiner: Map 1 gửi (hadoop,2) (hdfs,1) thay vì 3 cặp, giảm lưu lượng shuffle.')}
""")

# ---------------- Câu 7 ----------------
MAP7 = """#!/usr/bin/env python3
import sys
for line in sys.stdin:
    f = line.strip().split(",")
    if len(f) != 5 or f[0] == "order_id":
        continue
    print(f"{f[1]}\\t{float(f[4])}")"""
RED = """#!/usr/bin/env python3
import sys
cur, total = None, 0.0
for line in sys.stdin:
    k, v = line.rstrip("\\n").split("\\t")
    if k != cur:
        if cur is not None:
            print(f"{cur}\\t{total}")
        cur, total = k, 0.0
    total += float(v)
if cur is not None:
    print(f"{cur}\\t{total}")"""
add(7, "Câu 7: Tổng doanh số theo customer_id, ý tưởng", f"""
{pre('''map(dòng):
    bỏ qua header
    emit(customer_id, amount)

reduce(customer_id, danh_sách_amount):
    emit(customer_id, sum(danh_sách_amount))''')}
{callout('good', 'Combiner', 'Phép cộng có tính kết hợp nên dùng chính reducer làm Combiner để giảm dữ liệu shuffle.')}
{tbl(['Đầu vào mẫu', 'Sau Map', 'Kết quả Reduce'],
     [['1001,C001,Keyboard,Electronics,25.0<br/>1002,C002,Book,Education,10.5<br/>1003,C001,Mouse,Electronics,15.0',
       '(C001, 25.0)<br/>(C002, 10.5)<br/>(C001, 15.0)', '<b>C001 40.0</b><br/><b>C002 10.5</b>']], dense=True)}
""")

add(7, "Câu 7: Mã Python (Hadoop Streaming) và kết quả", f"""
{cols('<b>sales_mapper.py</b>' + pre(MAP7), '<b>sum_reducer.py</b>' + pre(RED))}
{pre('''python3 sales_mapper.py < sales.csv | sort | python3 sum_reducer.py
C001    40.0
C002    10.5''')}
<p class="qa-cap">Chạy thử cục bộ, <code>sort</code> mô phỏng shuffle. Trên cụm: <code>hadoop jar hadoop-streaming.jar -mapper sales_mapper.py -combiner sum_reducer.py -reducer sum_reducer.py</code></p>
""")

# ---------------- Câu 8 ----------------
add(8, "Câu 8: Nguyên nhân MapReduce kém hiệu quả khi dữ liệu lệch", f"""
{tblock('Cơ chế gây lệch', [
    'Reducer được chọn theo <code>hash(key) mod R</code>: mọi bản ghi của một khoá đi về cùng một reducer.',
    'Một khoá chiếm phần lớn bản ghi (khách VIP, giá trị null, ngày khuyến mãi) làm reducer đó quá tải.',
    'Reducer này chạy lâu hơn nhiều (straggler), cả job phải chờ; các reducer khác ngồi không nên thêm máy cũng không nhanh hơn.',
    'Reducer quá tải có thể tràn bộ nhớ hoặc đĩa; join có khoá nóng gặp lỗi tương tự.'])}
""")

add(8, "Câu 8: Kỹ thuật cải thiện hiệu suất", f"""
{tbl(['Kỹ thuật', 'Cách làm', 'Điều kiện'],
     [['Combiner, in-mapper combining', 'Gộp cục bộ phía map, mỗi map gửi 1 cặp cho mỗi khoá', 'Phép toán có tính kết hợp (tổng, đếm, max)'],
      ['Salting', 'Giai đoạn 1: khoá thành key#k (k ngẫu nhiên trong K) để chia khoá nóng cho K reducer. Giai đoạn 2: bỏ hậu tố, gộp tiếp', 'Tính từng phần rồi gộp được'],
      ['Partitioner tuỳ chỉnh', 'Lấy mẫu để chia khoảng khoá đều hoặc gán khoá nóng cho nhiều reducer', 'Biết hoặc ước lượng được phân phối'],
      ['Skew join', 'Xử lý riêng khoá nóng; bảng nhỏ đưa vào bộ nhớ mọi mapper (map-side join); Pig skewed join, Hive skew join', 'Một bảng đủ nhỏ, hoặc biết khoá nóng'],
      ['Tách khoá đặc biệt', 'Xử lý riêng null, giá trị mặc định', 'Biết khoá gây lệch'],
      ['Tăng số reducer', 'Giảm tải mỗi reducer', 'Chỉ giúp khi lệch nhẹ']], dense=True)}
""")

SALT = """# salt1_mapper.py (giai đoạn 1)
import sys, random
K = 4
for line in sys.stdin:
    f = line.strip().split(",")
    if len(f) != 5 or f[0] == "order_id":
        continue
    print(f"{f[1]}#{random.randrange(K)}\\t{float(f[4])}")"""
SALT2 = """# salt2_mapper.py (giai đoạn 2)
import sys
for line in sys.stdin:
    k, v = line.rstrip("\\n").split("\\t")
    print(f"{k.split('#')[0]}\\t{v}")"""
add(8, "Câu 8: Minh hoạ salting, K = 4", f"""
{cols(pre(SALT), pre(SALT2))}
{tbl(['Tập 2000 đơn, khoá C001 có 1800 đơn', 'Bản ghi mỗi reducer cho C001'],
     [['Không salting', '1800 trên 1 reducer'],
      ['Salting K = 4', '463, 433, 462, 442 (đo được); tổng cuối vẫn <b>C001 1800.0</b>']], dense=True)}
""")

# ---------------- Câu 9 ----------------
add(9, "Câu 9: Kiến trúc pipeline phân tích log truy cập", f"""
<p class="qa-q">Website thương mại điện tử lưu lượng lớn: thu thập log real-time, lưu lâu dài, phân tích hành vi người dùng.</p>
{pipeline_svg()}
<p class="qa-cap">YARN chạy Spark, Flink, Hive. ZooKeeper phục vụ điều phối (HBase, HDFS HA, Kafka bản cũ).</p>
""")

add(9, "Câu 9: Đáp ứng ba yêu cầu của đề", f"""
{tbl(['Yêu cầu', 'Thành phần', 'Cách làm'],
     [['Thu thập log real-time', logo_img('apachekafka.svg', 26) + ' Kafka', 'Web server là producer, gửi vào topic access_logs; nhiều partition (khoá theo user_id hoặc session_id), nhân bản 3, giữ cấu hình được (ví dụ 7 ngày) để đọc lại'],
      ['Lưu trữ log lâu dài', logo_img('apachehadoop.svg', 26) + ' HDFS', 'Spark, Flink hoặc Kafka Connect ghi Parquet hoặc ORC, phân vùng dt/hour, nhân bản 3'],
      ['Phân tích hành vi người dùng', logo_img('apachehive.svg', 26) + ' Hive, Spark, Flink', 'Hive batch trên bảng external theo phân vùng; Flink hoặc Spark Streaming tính chỉ số theo cửa sổ thời gian'],
      ['Điều phối định kỳ', logo_img('oozie.png', 22) + ' Oozie', 'Coordinator mỗi giờ hoặc ngày: gộp file nhỏ, thêm partition, chạy HiveQL, Sqoop xuất kết quả, gửi thông báo']], dense=True)}
{callout('info', 'Lưu ý thiết kế', 'Gom log thành tệp lớn (vài trăm MB) vì HDFS kém với tệp nhỏ; dùng định dạng cột để Hive đọc ít dữ liệu; Kafka là bộ đệm nên consumer chậm hoặc gián đoạn không làm mất log; cần tra theo userID độ trễ thấp thì ghi thêm vào HBase.')}
""")

HQL = """CREATE EXTERNAL TABLE access_logs (
  user_id STRING, session_id STRING, url STRING,
  action STRING, ts TIMESTAMP)
PARTITIONED BY (dt STRING, hour STRING)
STORED AS PARQUET LOCATION '/data/access_logs';

-- Top 10 sản phẩm được xem nhiều nhất trong ngày
SELECT url, COUNT(*) AS views
FROM access_logs WHERE dt = '2023-01-01' AND action = 'view'
GROUP BY url ORDER BY views DESC LIMIT 10;"""
HQL2 = """-- Tỉ lệ chuyển đổi theo ngày
SELECT dt,
  COUNT(DISTINCT CASE WHEN action='purchase'
        THEN session_id END) /
  COUNT(DISTINCT CASE WHEN action='view'
        THEN session_id END) AS conversion
FROM access_logs GROUP BY dt;"""
add(9, "Câu 9: Ví dụ HiveQL cho phân tích hành vi", f"""
{cols(pre(HQL), pre(HQL2) + '<p class="qa-cap">Bảng external trỏ vào thư mục log, truy vấn chỉ đọc phân vùng cần dùng.</p>')}
""")

# ---------------- Câu 10 ----------------
BAL = """#!/usr/bin/env python3
import sys
for line in sys.stdin:
    f = line.strip().split(",")
    if len(f) != 5 or f[0] == "transaction_id":
        continue
    amount = float(f[3])
    if f[2] == "deposit":
        print(f"{f[1]}\\t{amount}")
    elif f[2] == "withdrawal":
        print(f"{f[1]}\\t{-amount}")"""
add(10, "Câu 10: Số dư cuối của mỗi account_id, ý tưởng", f"""
{pre('''map(dòng):
    bỏ qua header
    nếu type == "deposit":     emit(account_id, +amount)
    nếu type == "withdrawal":  emit(account_id, -amount)

reduce(account_id, danh_sách_giá_trị):
    emit(account_id, sum(danh_sách_giá_trị))''')}
{callout('good', 'Thứ tự không quan trọng', 'Phép cộng giao hoán và kết hợp nên số dư cuối không phụ thuộc thứ tự giao dịch: không cần cột timestamp, và có thể dùng reducer làm Combiner.')}
""")

add(10, "Câu 10: Mã Python và kết quả", f"""
{cols('<b>bal_mapper.py</b>' + pre(BAL), '<b>Kết quả với 3 dòng mẫu</b>' + pre('''python3 bal_mapper.py < transactions.csv \\
  | sort | python3 sum_reducer.py
A101    400.0
A102    1000.0''') + '<p class="qa-cap">A101 = 500 − 100 = 400; A102 = 1000. Reducer dùng lại sum_reducer.py ở Câu 7. Giao dịch type khác bị bỏ qua.</p>')}
""")

# ---------------- kết ----------------
SL.append((99, f"""<div class="mdeck-slide"><div class="kicker">Cảm ơn đã theo dõi</div>
<h2>Nhóm 1: Hệ sinh thái Hadoop</h2>
<p>{" · ".join(MEMBERS)}</p>
<p style="color:var(--muted)">Môn Lưu trữ &amp; xử lý dữ liệu lớn, giảng viên Tạ Duy Hoàng</p></div>"""))

# ---------------- theme + ghép trang ----------------
SLIDES = []
for i, (q, s) in enumerate(SL):
    if q == 0 and i == 0:
        cls = "cover"
    elif q == 99:
        cls = "endcard"
    else:
        cls = f"th{q % 4}"
    s = re.sub(r'<div class="mdeck-slide( [^"]*)?">', lambda m: f'<div class="mdeck-slide{m.group(1) or ""} {cls}">', s, count=1)
    if cls.startswith("th"):
        s = s.replace("</h2>", '</h2><img class="hust-emblem" src="../assets/images/hust_logo.png" alt="HUST">', 1)
    SLIDES.append(s)
SLIDES[0] = SLIDES[0].replace("__SLIDE_COUNT__", str(len(SLIDES)))

DECK = f"""<div class="mdeck"><div class="mdeck-canvas-wrap"><div class="mdeck-viewport">{''.join(SLIDES)}</div></div>
<div class="mdeck-bar">
  <button class="mdeck-prev">◀ Trước</button><button class="mdeck-next">Sau ▶</button>
  <span class="mdeck-count"></span><div class="mdeck-dots"></div>
  <button class="mdeck-fs">⛶ Toàn màn hình</button>
</div></div>"""
rel_lang, rel_root = "", "../"
body = f"""<div class="hero"><div class="hust-logo-row"><img src="{rel_root}assets/images/hust_logo.png" alt="Logo Đại học Bách Khoa Hà Nội"></div>
<div class="kicker">Bài tập lớn · Nhóm 1</div>
<h1>Hệ sinh thái Hadoop: Trả lời câu hỏi ôn tập</h1>
<p>Đáp án 10 câu ôn tập cuối Chương 2, môn <b>Lưu trữ &amp; xử lý dữ liệu lớn</b>. Slide thuyết trình chính: <a href="group-1-slides.html">group-1-slides.html</a>.</p></div>
{DECK}
<div class="callout info" style="margin-top:20px"><div class="lbl">Nguồn</div>
Trần Văn Đặng, Nguyễn Hữu Đức, Nguyễn Bình Minh, Trần Việt Trung. <i>Lưu trữ và Xử lý Dữ liệu Lớn</i>, Chương 2: Hệ sinh thái Hadoop, tr.23–38. Trường CNTT&amp;TT, ĐH Bách Khoa Hà Nội, 2024.
&nbsp;·&nbsp; <a href="../data/source/IT4931_lecture_notes.pdf" target="_blank">📄 Xem giáo trình gốc (PDF)</a></div>
"""
html = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{HEAD_THEME_SCRIPT}
<title>Nhóm 1: Trả lời câu hỏi ôn tập Chương 2</title>
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
out = ROOT / "vi" / "group-1-slides-QA.html"
out.write_text(html, encoding="utf-8")
print(f"Đã sinh {out} ({len(SLIDES)} slide)")
