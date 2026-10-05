# -*- coding: utf-8 -*-
"""Sinh slide thuyết trình bài tập lớn Nhóm 1 — Chương 2: Hệ sinh thái Hadoop.
Nội dung bám sát IT4931_lecture_notes.pdf (Chương 2, tr.23-36, nhóm tác giả Trần Văn Đặng,
Nguyễn Hữu Đức, Nguyễn Bình Minh, Trần Việt Trung — ĐH Bách Khoa Hà Nội) — không bịa thêm
sự kiện/số liệu ngoài những gì sách nêu. Định dạng theo mẫu lap_lich_50_slides.pdf."""
import pathlib, sys
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

def tbl(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table><tr>{h}</tr>{r}</table>'

def formula(label, math):
    return f'<div class="pd-formula"><div class="pd-formula-label">{label}</div><div class="pd-formula-math">${math}$</div></div>'

def callout(kind, label, text):
    return f'<div class="callout {kind}"><div class="lbl">{label}</div>{text}</div>'

SLIDES = []

# ---------- Title ----------
SLIDES.append(f"""<div class="mdeck-slide"><div class="kicker">IT4931 — Lưu trữ &amp; xử lý dữ liệu lớn · Bài tập lớn</div>
<h2>Hệ sinh thái Hadoop</h2>
<p style="font-size:1.05rem;color:var(--muted)">Chương 2 — Lưu trữ và Xử lý Dữ liệu Lớn (Trần Văn Đặng, Nguyễn Hữu Đức, Nguyễn Bình Minh, Trần Việt Trung, ĐH Bách Khoa Hà Nội)</p>
<p><b>Nhóm 1</b> · {" · ".join(MEMBERS)}</p>
<p style="color:var(--muted);font-size:.9rem">Giảng viên: Tạ Duy Hoàng &nbsp;·&nbsp; Bài giảng chuyên đề &nbsp;·&nbsp; 48 slide</p></div>""")

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
SLIDES.append(divider(1, 7, "Vì sao cần Hadoop?", [
    "Bài toán: dữ liệu vượt quá khả năng 1 máy", "Apache Hadoop: nền tảng mã nguồn mở, kiến trúc scale-out",
    "Nguồn gốc: Google File System &amp; MapReduce", "4 thành phần cốt lõi"]))

SLIDES.append(slide("Apache Hadoop là gì?", f"""
<p>Nền tảng mã nguồn mở được thiết kế để <b>lưu trữ và xử lý khối lượng dữ liệu lớn trên cụm máy tính</b> —
cung cấp khả năng lưu trữ <i>scalable</i> (mở rộng được) và <i>reliable</i> (tin cậy), hỗ trợ xử lý song song
trên phần cứng thông dụng (commodity hardware).</p>
{callout('good','Kiến trúc scale-out', 'Mở rộng bằng cách <b>thêm máy</b> thay vì nâng cấp 1 máy duy nhất — cho phép mở rộng cụm lên hàng chục nghìn node.')}
{callout('warn','Triết lý chịu lỗi', 'Hỏng hóc phần cứng được xem là <b>điều bình thường</b>, không phải ngoại lệ — hệ thống tự động phát hiện lỗi, nhân bản dữ liệu và chuyển tác vụ sang node khác.')}
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
) + callout('info', 'Phối hợp', 'HDFS đảm bảo lưu trữ tin cậy · MapReduce cung cấp mô hình lập trình đơn giản · YARN điều phối hiệu quả tài nguyên — kết hợp giúp xử lý dữ liệu khổng lồ với chi phí hợp lý.')))

SLIDES.append(slide("Scale-out so với Scale-up", tbl(
    ["Tiêu chí", "Scale-up (truyền thống)", "Scale-out (Hadoop)"],
    [["Cách mở rộng", "Nâng cấp 1 máy chủ (thêm CPU/RAM đắt tiền)", "Thêm nhiều máy chủ rẻ tiền vào cụm"],
     ["Giới hạn mở rộng", "Bị chặn bởi phần cứng cao cấp nhất hiện có", "Mở rộng tới hàng chục nghìn node"],
     ["Xử lý lỗi", "1 máy hỏng = toàn hệ thống dừng", "Lỗi node là bình thường, tự động nhân bản &amp; chuyển tác vụ"],
     ["Chi phí", "Tăng phi tuyến khi nâng cấp máy đơn", "Tăng gần tuyến tính khi thêm node thông dụng"]]
) + callout('good', 'Vì sao quan trọng', 'Đây là lựa chọn kiến trúc nền tảng khiến Hadoop khả thi về chi phí cho bài toán dữ liệu petabyte — mọi thành phần khác (HDFS, YARN...) đều thiết kế xoay quanh triết lý scale-out này.')))

# ===================== PHẦN 2: HDFS =====================
SLIDES.append(divider(2, 7, "HDFS — lưu trữ phân tán", [
    "Mô hình write-once, read-many", "Kiến trúc master/slave: NameNode &amp; DataNode",
    "Block &amp; Replication (nhân bản)", "Hạn chế của HDFS"]))

SLIDES.append(slide("HDFS được tối ưu cho điều gì?", f"""
<p>HDFS tối ưu cho các tệp <b>kích thước lớn</b> (hàng trăm MB đến TB), mô hình truy cập
<b>write-once, read-many</b> (ghi một lần, đọc nhiều lần).</p>
{callout('warn','Đánh đổi có chủ đích', 'Thiết kế để đạt <b>thông lượng cao</b> thay vì <b>độ trễ thấp</b> — phù hợp xử lý batch hơn truy vấn tương tác thời gian thực.')}
<p>Chạy trên <b>phần cứng thông dụng</b> (không cần thiết bị lưu trữ chuyên dụng đắt tiền) — chấp nhận lỗi phần cứng xảy ra thường xuyên, bù lại bằng cơ chế chịu lỗi ở cấp phần mềm.</p>
"""))

SLIDES.append(slide("Kiến trúc master/slave: NameNode &amp; DataNode", f"""
<p><img src="../assets/diagrams/hdfs-architecture.svg" alt="Kiến trúc HDFS" style="border:1px solid var(--border);border-radius:10px;width:100%"></p>
<ul class="pd-legend"><li><b>NameNode</b><span>quản lý metadata: cấu trúc thư mục, tên tệp, ánh xạ tệp→block. Điều phối truy cập từ client.</span></li>
<li><b>DataNode</b><span>lưu trữ block dữ liệu thật, xử lý yêu cầu đọc/ghi từ client.</span></li></ul>
"""))

SLIDES.append(slide("Block là gì?", f"""
<p>Mỗi tệp trong HDFS được <b>chia thành nhiều block</b> (khối dữ liệu) thay vì lưu nguyên khối như hệ file thông thường.</p>
{formula('Kích thước block mặc định', '64\\text{ MB hoặc }128\\text{ MB}')}
{callout('info', 'Vì sao chia block', 'Block lớn giúp giảm chi phí quản lý metadata (ít block hơn so với chia nhỏ như hệ file truyền thống 4KB) và phù hợp mô hình đọc/ghi tuần tự khối lượng lớn mà HDFS hướng tới.')}
"""))

SLIDES.append(slide("Replication (nhân bản) hoạt động ra sao?", f"""
<p>Mỗi block được <b>replicate</b> (nhân bản) thành nhiều bản sao, phân phối trên các DataNode <b>khác nhau</b> trong cụm.</p>
{formula('Hệ số nhân bản mặc định', '3\\text{ bản sao trên 3 DataNode khác nhau}')}
{callout('good','Vì sao nhân bản giúp chịu lỗi', 'Khi 1 DataNode hỏng, hệ thống vẫn còn bản sao trên node khác — NameNode tự động điều phối sao chép lại để duy trì đủ số bản sao mặc định.')}
"""))

SLIDES.append(slide("Ví dụ minh hoạ: dung lượng vật lý thực cần", f"""
<p style="color:var(--muted);font-size:.85rem">Ví dụ số liệu tự tính để minh hoạ khái niệm — không trích từ sách, chỉ dùng đúng các thông số sách đã nêu (block 128MB, nhân bản 3 lần).</p>
{tbl(['Bước tính','Giá trị'],
     [['Kích thước tệp cần lưu', '1 TB = 1 048 576 MB'],
      ['Kích thước block', '128 MB'],
      ['Số block cần (1 048 576 / 128)', '= 8 192 block'],
      ['Hệ số nhân bản', '× 3'],
      ['<b>Dung lượng vật lý thực tế cần trên cụm</b>', '<b>= 3 TB</b> (gấp 3 lần dữ liệu gốc)']])}
{callout('warn', 'Đánh đổi', 'Nhân bản 3 lần giúp chịu lỗi tốt nhưng tốn gấp 3 lần dung lượng lưu trữ thật — đây là chi phí đổi lấy độ tin cậy của HDFS.')}
"""))

SLIDES.append(slide("NameNode có phải điểm yếu duy nhất?", f"""
<p>NameNode là thành phần <b>trung tâm duy nhất</b> giữ toàn bộ metadata — nếu NameNode gặp sự cố mà không có cơ chế dự phòng, cả hệ thống có nguy cơ mất khả năng xác định dữ liệu nằm ở đâu (dù dữ liệu thật vẫn còn nguyên trên DataNode).</p>
{callout('good', 'Cơ chế giảm thiểu rủi ro', '<i>Secondary NameNode</i> định kỳ sao lưu &amp; hợp nhất edit log của NameNode, hỗ trợ <b>phục hồi nhanh metadata</b> khi NameNode gặp sự cố — không phải bản sao chạy song song, mà là điểm khôi phục.')}
"""))

SLIDES.append(slide("Hạn chế của HDFS", tbl(["Hạn chế", "Lý do"], [
    ["Độ trễ truy xuất thấp (real-time)", "Tối ưu cho thông lượng tuần tự, không phải truy vấn ngẫu nhiên"],
    ["Số lượng lớn tệp nhỏ", "Metadata mọi tệp giữ trong bộ nhớ NameNode — giới hạn RAM"],
    ["Sửa đổi nội dung tuỳ ý", "Chỉ hỗ trợ <i>append</i> ở cuối tệp, không ghi đè giữa file"],
]) + callout('warn', 'Đánh đổi có chủ đích', 'HDFS hy sinh một số tính năng POSIX để đổi lấy khả năng mở rộng &amp; chịu lỗi vượt trội — nhờ đó lưu trữ được hàng petabyte trên cụm hàng nghìn node.')))

# ===================== PHẦN 3: MapReduce & YARN =====================
SLIDES.append(divider(3, 7, "MapReduce &amp; YARN", [
    "Mô hình lập trình Map + Reduce", "Vai trò MapReduce: Hadoop 1.x vs 2.x",
    "Vì sao cần tách YARN khỏi MapReduce", "Kiến trúc YARN: RM / AM / NM"]))

SLIDES.append(slide("Mô hình lập trình MapReduce", f"""
<p>Đề xuất bởi Google (2004) — framework đơn giản cho xử lý dữ liệu lớn song song, dựa trên 2 hàm do người lập trình định nghĩa:</p>
{tbl(['Giai đoạn','Việc của lập trình viên','Việc của framework'],
     [['Map (ánh xạ)','Viết hàm Map','Phân chia dữ liệu, phân phối tác vụ lên cụm'],
      ['Reduce (giảm thiểu)','Viết hàm Reduce','Thu gộp kết quả trung gian, xử lý lỗi tự động']])}
{callout('good','Điểm mạnh','Lập trình viên chỉ cần viết 2 hàm — phần song song hoá, phân phối, chịu lỗi đều do framework tự động đảm nhiệm.')}
"""))

SLIDES.append(slide("Vai trò MapReduce: Hadoop 1.x → 2.x", tbl(
    ["Phiên bản", "Vai trò MapReduce"],
    [["Hadoop 1.x", "Engine xử lý dữ liệu <b>chính</b>, cung cấp khả năng xử lý batch cho mọi bài toán"],
     ["Hadoop 2.x (có YARN)", "Trở thành <b>một trong nhiều</b> framework chạy trên cụm, cạnh tranh tài nguyên với Spark, Flink..."]]
) + f"""<p>Tối ưu hoá tận dụng hạ tầng: <b>Data Locality</b> (đặt tác vụ gần dữ liệu), <b>Minimal Data Exchange</b>,
<b>Fault Tolerance</b> tự động — nhờ đó chạy hiệu quả trên hàng nghìn node, xử lý hàng petabyte theo lô.</p>
{callout('warn','Hạn chế', 'Độ trễ cao cho tác vụ lặp/tương tác → động lực ra đời Spark, Flink. Vẫn là nền tảng quan trọng cho <i>batch processing</i> truyền thống.')}"""))

SLIDES.append(slide("MapReduce tích hợp với cả hệ sinh thái", f"""
<p>MapReduce không hoạt động đơn độc — nó là <b>engine thực thi phía sau</b> của nhiều công cụ khác:</p>
{tbl(['Công cụ','Dịch sang MapReduce như thế nào'],
     [['HDFS', 'MapReduce đọc/ghi dữ liệu trực tiếp qua HDFS'],
      ['YARN', 'Quản lý tài nguyên cho các job MapReduce chạy trên cụm'],
      ['Hive', 'Dịch câu lệnh HiveQL thành job MapReduce'],
      ['Pig', 'Dịch kịch bản Pig Latin thành job MapReduce'],
      ['Sqoop', 'Dùng MapReduce (chỉ Map task) để import/export dữ liệu']])}
{callout('good', 'Ý nghĩa', 'Đây là lý do MapReduce được gọi là "engine chung" — người dùng Hive/Pig/Sqoop không cần biết MapReduce chạy bên dưới, nhưng mọi tác vụ của họ cuối cùng đều quy về job MapReduce.')}
"""))

SLIDES.append(slide("Vì sao cần tách riêng YARN?", f"""
<p>Trong Hadoop 1.x, <b>MapReduce vừa xử lý dữ liệu vừa quản lý tài nguyên &amp; lập lịch</b> trên cụm —
dẫn đến hạn chế về hiệu năng và tính linh hoạt.</p>
{callout('good','Giải pháp Hadoop 2.x','YARN (Yet Another Resource Negotiator) tách biệt <b>quản lý tài nguyên</b> khỏi <b>xử lý dữ liệu</b>, biến Hadoop thành nền tảng tổng quát hơn — nhiều mô hình (MapReduce, Spark, Flink, Tez...) cùng chạy trên 1 cụm.')}
"""))

SLIDES.append(slide("Kiến trúc YARN", f"""<p><img src="../assets/diagrams/yarn-architecture.svg" alt="Kiến trúc YARN" style="border:1px solid var(--border);border-radius:10px;width:100%"></p>
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
{callout('info', 'Tự động hoá', 'Toàn bộ quá trình diễn ra tự động dưới sự điều phối của YARN — người dùng chỉ cần submit ứng dụng.')}
"""))

SLIDES.append(slide("Lợi ích YARN mang lại cho Hadoop", tbl(["Lợi ích", "Giải thích"], [
    ["Đa dạng hoá workload", "Nhiều loại ứng dụng chạy đồng thời (MapReduce, Spark, Flink, Tez...)"],
    ["Tăng tính linh hoạt", "Biến cụm Hadoop thành nền tảng đa năng, không chỉ dành cho MapReduce"],
    ["Mở rộng &amp; đa người dùng", "Cấu hình chính sách lập lịch: FIFO, Fair Scheduler, Capacity Scheduler"],
    ["Quản lý tài nguyên hiệu quả", "Phân bổ công bằng &amp; hiệu quả giữa các ứng dụng khác nhau"],
]) + callout('info', 'Ý nghĩa', 'YARN là bước ngoặt giúp hệ sinh thái Hadoop phát triển phong phú — Hive, Pig, Spark... có thể tích hợp và chạy chung 1 cụm thay vì hạ tầng riêng.')))

# ===================== PHẦN 4: Hive & Pig =====================
SLIDES.append(divider(4, 7, "Hive &amp; Pig — truy vấn và biến đổi dữ liệu", [
    "Apache Hive: data warehouse + HiveQL", "Apache Pig: Pig Latin, data flow",
    "Cả hai đều dịch sang job MapReduce", "So sánh 2 hướng tiếp cận"]))

SLIDES.append(slide("Apache Hive — data warehouse trên Hadoop", f"""
<p>Phát triển tại <b>Facebook</b> — cho phép truy vấn dữ liệu lớn bằng ngôn ngữ gần SQL (<b>HiveQL</b>): SELECT, JOIN, GROUP BY...
tự động dịch thành job MapReduce (hoặc Tez, Spark) để thực thi.</p>
{tbl(['Đặc trưng','Ý nghĩa'],
     [['Phù hợp phân tích dữ liệu lớn','Tối ưu cho truy vấn batch trên TB dữ liệu'],
      ['Thân thiện người dùng','Nhà phân tích dùng SQL quen thuộc, không cần viết Java MapReduce'],
      ['Schema on read','Dữ liệu lưu thô trên HDFS, schema chỉ định khi <i>đọc</i> — linh hoạt với dữ liệu đa dạng']])}
{callout('warn','Độ trễ','Tính bằng phút (do khởi tạo job MapReduce/Tez) — phù hợp batch hơn truy vấn tương tác tức thì.')}
"""))

SLIDES.append(slide("Hive hoạt động như thế nào?", f"""
<ol style="line-height:2.1">
<li>Người dùng viết câu lệnh <b>HiveQL</b> (SELECT, JOIN, GROUP BY...)</li>
<li>Hive <b>tự động dịch</b> câu lệnh thành job MapReduce (hoặc Tez, Spark) tương ứng</li>
<li>Job thực thi trên cụm Hadoop, đọc dữ liệu thô từ HDFS theo schema đã khai báo khi đọc</li>
<li>Kết quả trả về dưới dạng <b>bảng</b>, giống làm việc với CSDL truyền thống</li>
</ol>
{callout('good', 'Giá trị cốt lõi', 'Người dùng không cần biết MapReduce chạy bên dưới — chỉ cần viết SQL quen thuộc.')}
"""))

SLIDES.append(slide("Apache Pig — kịch bản xử lý dữ liệu", f"""
<p>Phát triển tại <b>Yahoo!</b> — thay vì SQL, Pig cung cấp ngôn ngữ kịch bản <b>Pig Latin</b> để biểu diễn luồng xử lý
(đọc, lọc, biến đổi, gộp nhóm, join, sắp xếp...) theo dạng <i>data flow</i>.</p>
{tbl(['Đặc điểm','Giải thích'],
     [['Độ dễ lập trình','Câu lệnh tuần tự, Pig tự song song hoá &amp; tối ưu'],
      ['Tối ưu hoá','Biết trước toàn bộ luồng → kết hợp bước, đẩy bộ lọc lên sớm'],
      ['Mở rộng (UDF)','Tự định nghĩa hàm bằng Java/Python chèn vào kịch bản']])}
<p>Pig Engine biên dịch kịch bản thành chuỗi job MapReduce — đặc biệt hiệu quả cho <b>transform &amp; join</b> dữ liệu phức tạp.</p>
"""))

SLIDES.append(slide("So sánh Hive vs Pig", tbl(["Tiêu chí", "Hive", "Pig"], [
    ["Ngôn ngữ", "HiveQL (giống SQL)", "Pig Latin (kịch bản)"],
    ["Đối tượng dùng", "Nhà phân tích quen SQL", "Kỹ sư dữ liệu, ETL phức tạp"],
    ["Mô hình dữ liệu", "Bảng (schema-on-read)", "Data flow tuần tự"],
    ["Engine thực thi", "Dịch sang MapReduce/Tez/Spark", "Dịch sang MapReduce"],
    ["Độ trễ", "Vài phút (batch)", "Vài phút (batch)"],
]) + callout('good', 'Điểm chung', 'Cả hai đều nhằm <b>đơn giản hoá sử dụng Hadoop</b>, không yêu cầu viết Java MapReduce thuần — cùng dịch công việc thành job MapReduce chạy trên cụm.')))

# ===================== PHẦN 5: HBase & Sqoop =====================
SLIDES.append(divider(5, 7, "HBase &amp; Sqoop", [
    "HBase: NoSQL wide-column trên Hadoop", "Mô hình Bigtable (Google)",
    "HBase vs RDBMS", "Sqoop: cầu nối Hadoop ↔ SQL"]))

SLIDES.append(slide("Apache HBase — \"cơ sở dữ liệu của Hadoop\"", f"""
<p>NoSQL phân tán xây trên Hadoop, thiết kế theo mô hình <b>Bigtable</b> (Google) — lưu bảng <b>hàng tỷ dòng, hàng triệu cột</b>,
hỗ trợ truy cập ngẫu nhiên độ trễ thấp.</p>
{callout('info','Ví von','Nếu HDFS giống hệ file, thì HBase giống <b>database chạy trên HDFS</b>, đọc/ghi theo kiểu bảng.')}
{tbl(['Đặc trưng','Giải thích'],
     [['Mô hình wide-column','Cột nhóm thành <i>column family</i>; mỗi ô có row key, tên cột, giá trị, timestamp'],
      ['Mở rộng cực lớn','Scale-out hàng trăm node, bảng hàng chục petabyte, tự động chia region'],
      ['Đọc/ghi thời gian thực','Hàng trăm nghìn INSERT/giây nhờ LSM-tree + commit log']])}
"""))

SLIDES.append(slide("HBase khác RDBMS ở đâu?", f"""
{callout('warn', 'Không phải RDBMS', 'HBase <b>không hỗ trợ SQL hay join phức tạp</b> — truy vấn qua API lập trình (Java/REST/Thrift) hoặc scan/get/put theo khoá. Không có transaction ACID đa bảng.')}
<p>Phù hợp cho: truy cập ngẫu nhiên theo khoá, khối lượng lớn (vd tra cứu/cập nhật theo userID) — hơn là phân tích ad-hoc.</p>
<p><b>Ví dụ thực tế:</b> Facebook Messaging từng dùng HBase lưu tin nhắn cho hàng trăm triệu người dùng, khai thác khả năng mở rộng linh hoạt.</p>
"""))

SLIDES.append(slide("Khi nào dùng HDFS+Hive, khi nào dùng HBase?", tbl(
    ["Nhu cầu", "Chọn"],
    [["Phân tích tổng hợp trên tập dữ liệu lớn (batch)", "HDFS + MapReduce/Hive"],
     ["Đọc/ghi ngẫu nhiên theo khoá, độ trễ thấp, gần thời gian thực", "HBase"],
     ["Truy vấn kiểu SQL, JOIN, GROUP BY phức tạp", "Hive (không phải HBase)"],
     ["Tra cứu/cập nhật theo userID với tốc độ cao", "HBase (không phải Hive)"]]
) + callout('info', 'Nguyên tắc chọn', 'Không có công cụ nào "tốt hơn" tuyệt đối — HDFS+Hive phục vụ phân tích tổng hợp, HBase phục vụ truy cập chi tiết từng bản ghi. Hai nhu cầu khác nhau, hai công cụ khác nhau.')))

SLIDES.append(slide("Apache Sqoop — cầu nối Hadoop ↔ RDBMS", f"""
<p>Tên ghép từ <b>SQL + Hadoop</b> — công cụ nhập/xuất dữ liệu hàng loạt giữa Hadoop và RDBMS (MySQL, PostgreSQL, Oracle...).</p>
{tbl(['Chiều', 'Cơ chế'],
     [['Import (RDBMS → HDFS)', 'Kết nối JDBC, khởi chạy job MapReduce chỉ gồm Map task — mỗi task nhập 1 phần bảng (theo WHERE/primary key)'],
      ['Export (HDFS → RDBMS)', 'Chia dữ liệu HDFS thành splits, mỗi Map task đẩy 1 phần vào CSDL qua batch INSERT']])}
{callout('good','Use case tiêu biểu','Nhập bảng giao dịch từ data warehouse vào Hadoop để phân tích chuyên sâu · xuất kết quả Hive/HDFS ra bảng SQL cho ứng dụng kinh doanh.')}
"""))

SLIDES.append(slide("Quy trình Sqoop Import từng bước", f"""
<ol style="line-height:2.1">
<li>Sqoop kết nối tới CSDL nguồn qua <b>JDBC</b></li>
<li>Thực thi truy vấn (hoặc duyệt từng bảng), <b>chia dữ liệu</b> theo điều kiện WHERE hoặc primary key</li>
<li>Khởi chạy job MapReduce <b>chỉ gồm Map task</b> — mỗi task nhập 1 phần dữ liệu song song</li>
<li>Ghi kết quả xuống HDFS (text/CSV hoặc Avro/Parquet), hoặc thẳng vào Hive/HBase nếu được chỉ định</li>
</ol>
{callout('good', 'Vì sao song song', 'Chia nhỏ theo primary key cho phép nhiều Map task cùng nhập dữ liệu đồng thời — tăng tốc đáng kể so với import tuần tự.')}
"""))

# ===================== PHẦN 6: Kafka, Oozie, ZooKeeper =====================
SLIDES.append(divider(6, 7, "Kafka, Oozie, ZooKeeper", [
    "Kafka: nền tảng streaming pub-sub", "Oozie: lập lịch workflow dạng DAG",
    "ZooKeeper: dịch vụ điều phối phân tán", "Vai trò trong toàn hệ sinh thái"]))

SLIDES.append(slide("Apache Kafka — streaming thời gian thực", f"""
<p>Phát triển tại <b>LinkedIn</b> — nền tảng <b>publish-subscribe</b> phân tán: producer gửi thông điệp vào <i>topic</i>,
consumer đăng ký nhận từ topic đó.</p>
{tbl(['Đặc điểm','Giải thích'],
     [['Thông lượng &amp; độ bền cao','Hàng triệu thông điệp/giây, ghi commit log tuần tự, nhân bản giữa broker'],
      ['Partition','Mỗi topic chia nhiều partition — tăng song song; Kafka đảm bảo thứ tự <i>trong từng partition</i>'],
      ['Multi-subscriber','Nhiều consumer group độc lập đọc cùng dữ liệu mà không ảnh hưởng nhau']])}
{callout('info','Vai trò trong hệ sinh thái','Tầng thu thập/phân phối sự kiện (ingest) — nguồn dữ liệu đầu vào liên tục cho Spark, Storm hoặc lưu vào HDFS/HBase.')}
"""))

SLIDES.append(slide("Ví dụ minh hoạ: Kafka trong pipeline thu thập log", f"""
<p style="color:var(--muted);font-size:.85rem">Minh hoạ dựa trên ví dụ sách nêu (thu thập log sự kiện người dùng vào topic "website_events") — diễn giải thêm để dễ hình dung, không phải trích nguyên văn.</p>
<ol style="line-height:2.1">
<li>Hàng trăm máy chủ web sinh ra sự kiện người dùng (click, xem trang...) liên tục</li>
<li>Mỗi sự kiện được gửi (<b>produce</b>) vào topic <code>website_events</code></li>
<li>Topic được chia thành nhiều <b>partition</b> để tăng thông lượng ghi song song</li>
<li>Ứng dụng Hadoop/Spark <b>consume</b> dòng sự kiện này để xử lý gần thời gian thực</li>
</ol>
{callout('good', 'Điểm mấu chốt', 'Producer (máy chủ web) và consumer (Spark/Hadoop) không kết nối trực tiếp — Kafka đứng giữa như một hàng đợi bền vững, chịu lỗi.')}
"""))

SLIDES.append(slide("Apache Oozie — lập lịch workflow", f"""
<p>Hệ thống quản lý &amp; lập lịch luồng công việc (workflow scheduler) cho Hadoop — định nghĩa chuỗi job
(MapReduce → Hive → shell script...) và quản lý thực thi tuần tự/song song.</p>
{callout('good','Mô hình DAG','Workflow mô tả dưới dạng <b>đồ thị có hướng không chu trình</b> — node là action/control node, cạnh là luồng thực thi (có điều kiện).')}
<p><b>Ví dụ:</b> chạy job MapReduce A → nếu thành công chạy job Hive B, nếu thất bại gửi email rồi kết thúc.</p>
<p><i>Coordinator</i>: lên lịch lặp lại workflow theo thời gian (mỗi giờ/ngày) hoặc khi dữ liệu mới đến HDFS.</p>
"""))

SLIDES.append(slide("Apache ZooKeeper — dịch vụ điều phối", tbl(
    ["Chức năng", "Mô tả ngắn"],
    [["Quản lý cấu hình", "Lưu &amp; phân phát thông tin cấu hình cho các node"],
     ["Đặt tên (naming)", "Không gian tên chung để dịch vụ đăng ký &amp; tìm nhau"],
     ["Đồng bộ hoá phân tán", "Cơ chế khoá, hàng rào (barrier) tránh xung đột"],
     ["Dịch vụ nhóm", "Theo dõi thành viên trong 1 nhóm node (vd RegionServer)"],
     ["Bầu chọn leader", "Đảm bảo đúng 1 node làm leader tại 1 thời điểm (ephemeral znode)"]]
)))

SLIDES.append(slide("Vì sao ZooKeeper đáng tin cậy?", f"""
<p>ZooKeeper dùng thuật toán <b>ZAB</b> (ZooKeeper Atomic Broadcast — thuộc họ thuật toán Paxos) để đảm bảo
tất cả server ZooKeeper (chạy thành cụm nhỏ) duy trì <b>cùng một trạng thái</b>.</p>
{callout('good', 'Tính nhất quán tuần tự', 'Các thay đổi áp dụng theo mô hình nhất quán tuần tự; client có thể đăng ký <b>watch</b> để được thông báo ngay khi dữ liệu thay đổi hoặc node mới xuất hiện/biến mất.')}
<p>Nhờ đó, các node trong hệ phân tán không cần liên lạc peer-to-peer phức tạp — chỉ cần dựa vào ZooKeeper như một "trọng tài chung" tin cậy.</p>
"""))

SLIDES.append(slide("ZooKeeper được dùng ở đâu trong Hadoop?", tbl(["Thành phần", "ZooKeeper dùng để"], [
    ["HDFS High Availability", "Giám sát NameNode &amp; kích hoạt failover"],
    ["YARN", "Lưu thông tin ResourceManager chủ"],
    ["HBase", "Theo dõi RegionServer &amp; điều phối Master"],
    ["Kafka (bản cũ)", "Quản lý thông tin broker, chủ đề, phân vùng"],
]) + callout('info', 'Vai trò tổng thể', 'ZooKeeper là "người giữ nhịp" thầm lặng phía sau — giảm độ phức tạp phát triển hệ phân tán nhờ các primitive tin cậy có sẵn.')))

# ===================== PHẦN 7: Tổng kết =====================
SLIDES.append(divider(7, 7, "Tổng kết", [
    "Sơ đồ toàn cảnh hệ sinh thái Hadoop", "Tổng kết nội dung chương 2",
    "Câu hỏi thảo luận nhanh", "Tài liệu tham khảo"]))

SLIDES.append(slide("Toàn cảnh hệ sinh thái Hadoop", tbl(
    ["Tầng", "Thành phần", "Vai trò"],
    [["Thu thập", "Kafka", "Streaming sự kiện thời gian thực"],
     ["Lưu trữ", "HDFS, HBase", "Tệp phân tán &amp; NoSQL thời gian thực"],
     ["Tính toán batch", "MapReduce", "Mô hình Map + Reduce song song"],
     ["Phân tích", "Hive, Pig", "SQL-like &amp; kịch bản data flow"],
     ["Quản trị luồng", "Oozie", "Lập lịch workflow dạng DAG"],
     ["Vận hành", "ZooKeeper", "Điều phối, đồng bộ, bầu leader"],
     ["Điều phối tài nguyên", "YARN", "Quản lý tài nguyên đa ứng dụng"],
     ["Tích hợp RDBMS", "Sqoop", "Import/export với CSDL quan hệ"]]
)))

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
     ["DAG", "Đồ thị có hướng không chu trình — mô hình workflow của Oozie"],
     ["Znode", "Đơn vị dữ liệu trong cây thư mục phân tán của ZooKeeper"]]
)))

SLIDES.append(slide("Câu hỏi thảo luận nhanh", f"""
<ol style="line-height:2">
<li>Vì sao HDFS chọn đánh đổi độ trễ thấp để lấy thông lượng cao? Đánh đổi này hợp lý trong tình huống nào?</li>
<li>So với MapReduce chạy trực tiếp trên Hadoop 1.x, vai trò của MapReduce thay đổi ra sao sau khi có YARN?</li>
<li>Hive và Pig cùng dịch sang job MapReduce — vậy điểm khác biệt cốt lõi giữa 2 công cụ nằm ở đâu?</li>
<li>Vì sao HBase không hỗ trợ SQL/join phức tạp lại vẫn được coi là một thành phần quan trọng của hệ sinh thái?</li>
</ol>
<p style="color:var(--muted);font-size:.88rem">Dùng để thảo luận tại lớp — không có đáp số cố định, trả lời dựa trên nội dung Chương 2.</p>
"""))

SLIDES.append(slide("Tài liệu tham khảo", f"""
<p><b>Nguồn duy nhất của toàn bộ nội dung trình bày:</b></p>
{tbl(['Mục','Chi tiết'],
     [['Giáo trình','<i>Lưu trữ và Xử lý Dữ liệu Lớn</i> — Trần Văn Đặng, Nguyễn Hữu Đức, Nguyễn Bình Minh, Trần Việt Trung'],
      ['Đơn vị','Trường Công nghệ Thông tin &amp; Truyền thông, Đại học Bách Khoa Hà Nội (2024)'],
      ['Chương sử dụng','Chương 2 — Hệ sinh thái Hadoop, tr. 23–36'],
      ['Phân công','Thầy Tạ Duy Hoàng — Nhóm 1 phụ trách Chương 2 (thông báo 05/10, trình bày từ tuần 12/10)']])}
"""))

SLIDES.append(f"""<div class="mdeck-slide"><div class="kicker">Cảm ơn đã theo dõi</div>
<h2>Nhóm 1 — Hệ sinh thái Hadoop</h2>
<p>{" · ".join(MEMBERS)}</p>
<p style="color:var(--muted)">Môn Lưu trữ &amp; xử lý dữ liệu lớn — Giảng viên Tạ Duy Hoàng</p></div>""")

DECK = f"""<div class="mdeck"><div class="mdeck-viewport">{''.join(SLIDES)}</div>
<div class="mdeck-bar">
  <button class="mdeck-prev">◀ Trước</button><button class="mdeck-next">Sau ▶</button>
  <span class="mdeck-count"></span><div class="mdeck-dots"></div>
  <button class="mdeck-fs">⛶ Toàn màn hình</button>
</div></div>"""

rel_lang = ""
rel_root = "../"
body = f"""<div class="hero"><div class="kicker">Bài tập lớn · Nhóm 1</div>
<h1>Hệ sinh thái Hadoop — Chương 2</h1>
<p>Slide thuyết trình môn <b>Lưu trữ &amp; xử lý dữ liệu lớn</b> (giảng viên Tạ Duy Hoàng) — nhóm {", ".join(MEMBERS)}.
Nội dung bám sát 100% Chương 2 giáo trình chính thức của môn học (IT4931_lecture_notes.pdf, tr.23–36), không bổ sung nội dung ngoài phạm vi sách.</p></div>
{DECK}
<div class="callout info" style="margin-top:20px"><div class="lbl">Nguồn</div>
Trần Văn Đặng, Nguyễn Hữu Đức, Nguyễn Bình Minh, Trần Việt Trung. <i>Lưu trữ và Xử lý Dữ liệu Lớn</i>, Chương 2 —
Hệ sinh thái Hadoop, tr.23–36. Trường CNTT&amp;TT, ĐH Bách Khoa Hà Nội, 2024.
&nbsp;·&nbsp; <a href="../data/source/IT4931_lecture_notes.pdf" target="_blank">📄 Xem giáo trình gốc (PDF)</a></div>
"""

html = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{HEAD_THEME_SCRIPT}
<title>Nhóm 1 — Hệ sinh thái Hadoop (Chương 2)</title>
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
</body></html>"""

out = ROOT / "vi" / "group-1-slides.html"
out.write_text(html, encoding="utf-8")
print("Đã sinh", out, "—", len(SLIDES), "slide")
