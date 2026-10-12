# -*- coding: utf-8 -*-
"""Bổ sung cho hd-04 (Bigtable), hd-05 (Kafka), hd-06 (Chubby + bản đồ tổng hợp). Mọi con số lấy từ
bài báo gốc trong References/Foundational hoặc là phép tính hiển thị từng bước từ các con số đó."""
from hd_add_common import fig, logo, logos, two
from timeline_svg import tech_timeline_svg

# =====================================================================================================
# HD-04: HBase <- Bigtable
# =====================================================================================================
PART_BT = dict(
 title="Đọc trực tiếp bài báo Bigtable (OSDI 2006): mô hình dữ liệu, tablet, compaction và vai trò của Chubby",
 bullets=[
  "Bigtable là một bản đồ đa chiều đã sắp xếp: (row, column, timestamp) → giá trị",
  "Tìm tablet qua 3 tầng: Chubby → root tablet → METADATA → tablet người dùng ($2^{34}$ tablet)",
  "Ghi vào memtable rồi thành SSTable; 3 loại compaction; vì sao đọc ngẫu nhiên đắt",
  "Chubby giữ khoá master, danh sách tablet server và vị trí khởi đầu"],
 slides=[
  dict(h="Bài báo Bigtable: một bản đồ đa chiều, thưa, đã sắp xếp", body=logos("apachehbase.svg", "google.svg", h=38) + two(
   fig("bigtable_fig1.png", "Nguồn: Chang et al., <i>Bigtable</i>, OSDI 2006, Figure 1 (bảng Webtable; khoá hàng là URL đảo ngược).", 190), """
   <p>🗣️ <b>Nói nôm na:</b> một cuốn sổ cái khổng lồ, mỗi ô được tra bằng 3 toạ độ: <b>hàng</b> (ai/cái gì), <b>cột</b>
   (thuộc tính nào), <b>thời điểm</b> (phiên bản nào). Sổ được sắp theo tên hàng và chia thành các tập giấy (tablet).</p>""", "46%") + """
   <table><tr><th>Khái niệm trong bài</th><th>Chi tiết</th><th>Trong HBase</th></tr>
   <tr><td>Bản đồ đa chiều</td><td>&quot;Sparse, distributed, persistent multidimensional sorted map&quot;; giá trị là mảng byte không diễn giải</td><td>Bảng HBase lưu byte thô</td></tr>
   <tr><td>Row key</td><td>Chuỗi bất kỳ tới 64 KB (thường 10 đến 100 byte); đọc/ghi một hàng là nguyên tử; sắp theo thứ tự từ điển</td><td>Row key, ghi nguyên tử trên 1 hàng</td></tr>
   <tr><td>Column family</td><td>Đơn vị kiểm soát truy cập; nên chỉ vài trăm family, ít khi đổi; cột có dạng <code>family:qualifier</code></td><td>Column family</td></tr>
   <tr><td>Timestamp</td><td>Mỗi ô nhiều phiên bản, lưu theo thứ tự timestamp giảm dần để đọc bản mới nhất trước</td><td>Cell version</td></tr>
   <tr><td>Giao dịch</td><td>Chỉ có giao dịch trên <b>một hàng</b>, không có giao dịch tổng quát qua nhiều hàng</td><td>Cùng giới hạn</td></tr></table>
   <div class="callout info"><div class="lbl">Quy mô và ứng dụng</div>Thiết kế để mở rộng tới petabyte trên hàng nghìn máy; được hơn 60 sản phẩm của Google dùng,
   gồm Google Analytics, Google Finance, Orkut, Personalized Search, Writely và Google Earth.</div>"""),
  dict(h="Hình gốc: tìm tablet qua 3 tầng, và phép tính vì sao đủ cho $2^{34}$ tablet", body=two(
   fig("bigtable_fig4.png", "Nguồn: Chang et al., OSDI 2006, Figure 4 (phân cấp 3 tầng giống B+-tree).", 270), """
   <ol style="margin:0;padding-left:20px;line-height:1.5">
   <li><b>Tầng 1:</b> một file trong <b>Chubby</b> chứa vị trí <i>root tablet</i>.</li>
   <li><b>Tầng 2:</b> root tablet (tablet đầu của bảng METADATA, không bao giờ bị tách) chứa vị trí mọi METADATA tablet.</li>
   <li><b>Tầng 3:</b> mỗi METADATA tablet chứa vị trí một tập tablet của người dùng.</li></ol>
   <p style="font-size:.92rem">Mỗi hàng METADATA khoảng 1 KB trong bộ nhớ. Client lưu đệm vị trí; nếu bộ nhớ đệm rỗng cần <b>3</b> lượt gọi mạng
   (có 1 lần đọc Chubby), nếu đệm cũ có thể tới <b>6</b> lượt.</p>""", "46%") + """
   <p><b>Phép tính từng bước</b> (METADATA tablet giới hạn 128 MB, mỗi hàng ≈ 1 KB):</p>
   <div class="pd-formula"><div class="pd-formula-math">\\frac{128\\ \\text{MB}}{1\\ \\text{KB}} = 2^{17}\\ \\text{hàng};\\quad 2^{17}\\times 2^{17} = 2^{34}\\ \\text{tablet};\\quad 2^{34}\\times 128\\ \\text{MB} = 2^{34}\\times 2^{27} = 2^{61}\\ \\text{byte}</div></div>
   <p>Root tablet trỏ tới tối đa $2^{17}$ METADATA tablet, mỗi METADATA tablet trỏ tới $2^{17}$ tablet người dùng: 3 tầng là đủ, không cần tầng thứ tư.
   Trong HBase hiện đại cấu trúc gọn hơn: ZooKeeper lưu vị trí của bảng meta, bảng meta chứa vị trí từng region (tablet).</p>"""),
  dict(h="Hình gốc: một tablet được ghi, đọc và nén gọn thế nào", body=two(
   fig("bigtable_fig5.png", "Nguồn: Chang et al., OSDI 2006, Figure 5 (Tablet Representation).", 230), """
   <ul style="margin:0;padding-left:20px;line-height:1.5"><li><b>tablet log</b>: nhật ký commit trên GFS; ghi trước khi báo thành công (tương ứng WAL của HBase)</li>
   <li><b>memtable</b>: bộ đệm đã sắp xếp trong RAM chứa các cập nhật mới (MemStore)</li>
   <li><b>SSTable</b>: tệp bất biến, đã sắp xếp, trên GFS; có chỉ mục khối, khối thường 64 KB (HFile)</li></ul>""", "44%") + """
   <table><tr><th>Loại compaction</th><th>Làm gì</th><th>Mục đích</th></tr>
   <tr><td><b>Minor</b></td><td>Memtable đầy thì đóng băng, ghi ra một SSTable mới</td><td>Giảm bộ nhớ, rút ngắn log cần phát lại khi phục hồi</td></tr>
   <tr><td><b>Merging</b></td><td>Gộp vài SSTable và memtable thành 1 SSTable mới</td><td>Giới hạn số tệp phải đọc</td></tr>
   <tr><td><b>Major</b></td><td>Viết lại mọi SSTable thành đúng 1, <b>loại bỏ dữ liệu đã xoá</b></td><td>Thu hồi chỗ trống, đảm bảo dữ liệu xoá thật sự biến mất</td></tr></table>
   <p>Đọc là một <i>chế độ xem gộp</i> của memtable và các SSTable (đều đã sắp xếp nên gộp hiệu quả). Hai tối ưu hay dùng: <b>Bloom filter</b> cho biết SSTable
   <i>có thể</i> chứa cặp hàng/cột không (tránh đọc đĩa vô ích, kể cả khi tra hàng không tồn tại) và <b>locality group</b> gom các column family thường đọc cùng nhau vào cùng SSTable.</p>"""),
  dict(h="Số liệu thực nghiệm: vì sao đọc ngẫu nhiên đắt hơn ghi, và mở rộng không tuyến tính", body="""
   <p>🗣️ <b>Nói nôm na:</b> muốn đọc 1 dòng chữ mà phải mượn cả quyển 64 trang về, đọc 1 dòng rồi trả: đó là đọc ngẫu nhiên trên khối 64 KB.
   Còn ghi thì như viết tiếp vào một cuốn nhật ký duy nhất.</p>
   <table><tr><th>Quan sát trong bài</th><th>Phép tính / lý do</th></tr>
   <tr><td>1 tablet server đọc ngẫu nhiên ≈ <b>1200 lượt/giây</b> ≈ <b>75 MB/s</b> từ GFS</td><td>Mỗi lượt kéo cả khối 64 KB nhưng chỉ dùng 1 giá trị 1000 byte: hệ số khuếch đại $64\\ \\text{KB} / 1000\\ \\text{B} \\approx 65$; $1200 \\times 64\\ \\text{KB} \\approx 77\\ \\text{MB/s}$</td></tr>
   <tr><td>Đọc tuần tự nhanh hơn ngẫu nhiên</td><td>Mỗi khối 64 KB lấy từ GFS được cất vào block cache và phục vụ 64 yêu cầu kế tiếp</td></tr>
   <tr><td>Ghi nhanh hơn đọc ngẫu nhiên; ghi ngẫu nhiên ≈ ghi tuần tự</td><td>Mọi ghi của 1 tablet server nối vào <b>một</b> commit log, dùng group commit để đẩy lên GFS</td></tr>
   <tr><td>Đọc ngẫu nhiên khi locality group đặt trong bộ nhớ nhanh hơn rất nhiều</td><td>Không cần lấy khối 64 KB từ GFS</td></tr>
   <tr><td>Từ 1 lên 500 tablet server, thông lượng tổng tăng <b>hơn 100 lần</b>, không phải 500 lần</td><td>Mở rộng tốt nhưng <i>không tuyến tính</i>: hiệu quả mỗi máy giảm khi cụm lớn</td></tr></table>
   <div class="callout warn"><div class="lbl">Bài học thiết kế row key</div>Vì mỗi lần đọc đắt, thiết kế row key sao cho dữ liệu hay đọc cùng nhau nằm kề nhau (ví dụ URL đảo ngược gom trang cùng tên miền)
   là cách tận dụng bộ đệm khối và giảm số lần đọc đĩa. Đây là gốc rễ của lời khuyên về row key ở phần trước.</div>"""),
  dict(h="Chubby trong Bigtable: giữ khoá master, quản lý tablet server, lưu vị trí khởi đầu", body="""
   <p>Bài báo liệt kê Bigtable dùng Chubby cho: <b>(1)</b> bảo đảm tối đa một master hoạt động; <b>(2)</b> lưu vị trí khởi đầu của dữ liệu; <b>(3)</b> phát hiện tablet server và xác nhận server chết;
   <b>(4)</b> lưu schema; <b>(5)</b> lưu danh sách kiểm soát truy cập.</p>
   <table><tr><th>Tình huống</th><th>Cơ chế trong bài</th><th>Tương ứng HBase + ZooKeeper</th></tr>
   <tr><td>Tablet server khởi động</td><td>Tạo và giữ khoá độc quyền trên một tệp tên duy nhất trong thư mục servers của Chubby</td><td>RegionServer tạo znode tạm (ephemeral)</td></tr>
   <tr><td>Phát hiện server chết</td><td>Master hỏi trạng thái khoá; nếu server mất khoá, master tự lấy khoá rồi xoá tệp để server không phục vụ được nữa</td><td>Znode tạm biến mất khi session hết hạn</td></tr>
   <tr><td>Master khởi động</td><td>4 bước: lấy khoá master duy nhất; quét thư mục servers; hỏi từng server các tablet đang giữ; quét bảng METADATA</td><td>Bầu HMaster, quét znode RegionServer</td></tr>
   <tr><td>Master mất phiên Chubby</td><td>Master <b>tự kết thúc</b> để không mắc kẹt do lỗi mạng giữa master và Chubby</td><td>HMaster dừng khi mất session ZooKeeper</td></tr></table>
   <div class="callout info"><div class="lbl">Cái giá của việc dựa vào Chubby</div>Nếu Chubby không khả dụng lâu, Bigtable cũng không khả dụng. Đo trên 14 cụm Bigtable
   dùng 11 instance Chubby: trung bình chỉ <b>0,0047%</b> số giờ-server có dữ liệu không truy cập được vì Chubby, cụm bị ảnh hưởng nặng nhất là <b>0,0326%</b>.
   Con số nhỏ, nhưng chính là lý do gọi Chubby/ZooKeeper là &quot;xương sống vô hình&quot; ở module hd-06.</div>"""),
 ])

QUIZ_BT = [
 dict(q="Theo bài báo Bigtable, mỗi giá trị trong bảng được tra bằng bộ ba chỉ số nào?",
  opts=["Hàng, cột, timestamp", "Tablet, SSTable, offset", "Hàng, tablet, server", "Cột, family, khoá chính"],
  correct=0, explain="Bigtable là bản đồ đa chiều được lập chỉ mục bởi row key, column key và timestamp."),
 dict(q="Vì sao 3 tầng (Chubby, root tablet, METADATA) đủ để địa chỉ 2^34 tablet?",
  opts=["Vì mỗi tầng chỉ trỏ tới 2 tablet", "Vì Chubby lưu toàn bộ vị trí", "Vì mỗi METADATA tablet 128 MB chứa 2^17 hàng 1 KB, và root trỏ tới 2^17 METADATA tablet: 2^17 × 2^17 = 2^34", "Vì client luôn giữ đủ bộ đệm"],
  correct=2, explain="128 MB / 1 KB = 2^17 hàng. Hai tầng sau nhân với nhau cho 2^34 tablet; nhân 128 MB cho 2^61 byte."),
 dict(q="Một tablet server đọc ngẫu nhiên khối 64 KB nhưng chỉ dùng giá trị 1000 byte. Hệ số khuếch đại đọc xấp xỉ bao nhiêu?",
  opts=["Khoảng 6", "Khoảng 16", "Khoảng 65", "Khoảng 640"],
  correct=2, explain="64 KB / 1000 byte ≈ 65. Đây là lý do đọc ngẫu nhiên đắt và Bloom filter, block cache, row key tốt có giá trị lớn."),
 dict(q="Major compaction khác minor compaction ở điểm nào?",
  opts=["Major chỉ ghi memtable ra đĩa", "Major viết lại mọi SSTable thành đúng 1 và loại bỏ dữ liệu đã xoá", "Major chỉ chạy khi master khởi động", "Major xoá commit log"],
  correct=1, explain="Minor đóng băng memtable ra SSTable mới; major gộp tất cả SSTable thành một và dọn dữ liệu đã xoá."),
 dict(q="Khi master Bigtable mất phiên Chubby, nó làm gì?",
  opts=["Tiếp tục chạy với bộ nhớ đệm", "Tự bầu lại bằng cách hỏi các tablet server", "Giao quyền cho tablet server đầu tiên", "Tự kết thúc"],
  correct=3, explain="Master tự kết thúc để cụm không bị lỗi do mạng giữa master và Chubby. Thay đổi này không làm đổi việc gán tablet cho server."),
 dict(q="Từ 1 lên 500 tablet server, thông lượng tổng của Bigtable trong bài tăng cỡ nào?",
  opts=["Đúng 500 lần", "Hơn 100 lần, không phải 500 lần", "Chỉ khoảng 10 lần", "Không đổi"],
  correct=1, explain="Bài báo nêu thông lượng tổng tăng hơn một trăm lần: mở rộng tốt nhưng không tuyến tính."),
 dict(q="Vì sao Bigtable dùng một commit log duy nhất cho mỗi tablet server thay vì mỗi tablet một log?",
  opts=["Để dễ xoá log", "Để tránh rất nhiều tệp ghi đồng thời trên GFS gây nhiều lần seek đĩa", "Vì mỗi tablet quá nhỏ", "Vì Chubby yêu cầu"],
  correct=1, explain="Nếu mỗi tablet một log, nhiều tệp được ghi cùng lúc trên GFS gây nhiều seek. Gộp mutation của nhiều tablet vào 1 log và dùng group commit."),
]

HD04 = dict(inserts=[(1, PART_BT)], quiz=QUIZ_BT,
            logo_heads={"Mô hình 'cột mở rộng' (wide-column) khác bảng thông thường": ["apachehbase.svg", "google.svg"],
                        "Bài toán và cơ chế hoạt động của Sqoop": ["sqoop.png"]})

# =====================================================================================================
# HD-05: Kafka
# =====================================================================================================
PART_KF = dict(
 title="Đọc trực tiếp bài báo Kafka (NetDB 2011): thiết kế, điều phối bằng ZooKeeper và số liệu LinkedIn",
 bullets=[
  "Vì sao Scribe, Flume, JMS chưa đủ, và chọn mô hình pull thay vì push",
  "Log chia segment, địa chỉ bằng offset, broker không giữ trạng thái",
  "Bốn registry trong ZooKeeper (ephemeral và persistent), ví dụ chia partition",
  "Hình triển khai ở LinkedIn: dữ liệu chảy vào Hadoop; số liệu so với ActiveMQ và RabbitMQ"],
 slides=[
  dict(h="Bài báo Kafka: vì sao log aggregator và JMS chưa đủ", body=logos("apachekafka.svg", "linkedin.svg", h=36) + """
   <p>🗣️ <b>Nói nôm na:</b> các hệ thống cũ giống bưu điện được thiết kế để chuyển thư quan trọng và theo dõi từng lá thư;
   LinkedIn cần một hệ thống giống băng chuyền hàng loạt: nhanh, chịu được hàng triệu mẩu tin nhỏ, ai muốn lấy thì tự đến lấy.</p>
   <table><tr><th>Hệ thống trước đó</th><th>Hạn chế được bài báo nêu</th></tr>
   <tr><td>Scribe (Facebook), Data Highway (Yahoo), Flume (Cloudera)</td><td>Chủ yếu để <b>nạp log vào kho dữ liệu hoặc Hadoop</b> xử lý ngoại tuyến; hầu hết dùng mô hình <b>push</b>; không phục vụ tiêu thụ thời gian thực</td></tr>
   <tr><td>Hệ nhắn tin kiểu JMS (ví dụ ActiveMQ)</td><td>Không có API cho producer gộp nhiều tin vào một yêu cầu; không dễ chia và lưu tin trên nhiều máy; broker phải giữ trạng thái giao hàng của từng tin</td></tr></table>
   <p><b>Vì sao pull thay vì push?</b> Bài báo: với mô hình pull, mỗi consumer lấy dữ liệu theo tốc độ tối đa mình chịu được, không bị đẩy ngập; và dễ <b>tua lại</b> (rewind) một consumer.</p>
   <div class="callout info"><div class="lbl">Bối cảnh khối lượng dữ liệu (theo chính bài báo)</div>Bài báo dẫn rằng mỗi ngày China Mobile thu 5 đến 8 TB bản ghi cuộc gọi và Facebook thu gần 6 TB sự kiện
   hoạt động của người dùng. Log không còn là thứ phụ: nó là nguyên liệu của cả dây chuyền dữ liệu của công ty internet.</div>"""),
  dict(h="Hình gốc: log chia segment, địa chỉ bằng offset, broker không giữ trạng thái", body=two(
   fig("kafka_fig2.png", "Nguồn: Kreps, Narkhede, Rao, <i>Kafka: a Distributed Messaging System for Log Processing</i>, NetDB 2011, Figure 2.", 300), """
   <ul style="margin:0;padding-left:20px;line-height:1.5">
   <li>Mỗi partition là một <b>log</b> gồm các <b>segment file</b> cỡ xấp xỉ nhau (ví dụ 1 GB); producer luôn <b>nối</b> vào segment cuối.</li>
   <li>Flush ra đĩa sau một số tin hoặc một khoảng thời gian; tin chỉ lộ ra cho consumer <b>sau khi flush</b>.</li>
   <li>Không có message id riêng: tin được gọi bằng <b>offset logic</b>; offset tin kế = offset hiện tại + độ dài tin hiện tại.</li>
   <li>Broker giữ trong RAM danh sách offset đã sắp xếp, gồm offset đầu của mỗi segment, để tìm segment chứa offset được hỏi.</li></ul>""", "40%") + """
   <table><tr><th>Quyết định thiết kế trong bài</th><th>Lý do</th></tr>
   <tr><td><b>Broker không giữ trạng thái</b>: consumer tự nhớ đã đọc tới đâu</td><td>Giảm độ phức tạp và chi phí ở broker; đổi lại việc xoá tin dựa vào thời gian chứ không dựa vào việc mọi consumer đã đọc</td></tr>
   <tr><td>Xoá theo thời gian lưu giữ, điển hình <b>7 ngày</b></td><td>Consumer chậm hoặc ngoại tuyến vẫn kịp đọc; hiệu năng không giảm khi dữ liệu lớn</td></tr>
   <tr><td>Consumer có thể <b>tua lại</b> offset cũ</td><td>Sửa lỗi logic rồi phát lại; nạp ETL vào Hadoop; checkpoint offset nhỏ nhất của dữ liệu chưa flush</td></tr></table>"""),
  dict(h="Lựa chọn hiệu năng trong bài: không cache riêng, dùng page cache và sendfile", body="""
   <table><tr><th>Lựa chọn</th><th>Lý do bài báo nêu</th></tr>
   <tr><td><b>Không cache tin trong tiến trình Kafka</b>, dựa vào page cache của hệ điều hành</td><td>Tránh lưu hai lần; cache vẫn ấm khi broker khởi động lại; ít chi phí dọn rác bộ nhớ nên triển khai bằng ngôn ngữ chạy trên máy ảo vẫn hiệu quả</td></tr>
   <tr><td>Truy cập tuần tự cả khi ghi và đọc</td><td>Consumer thường chỉ chậm hơn producer một chút nên heuristic của hệ điều hành (write-through, read-ahead) rất hiệu quả</td></tr>
   <tr><td><b>sendfile</b></td><td>Cách thông thường gửi byte từ tệp ra socket cần <b>4 lần sao chép dữ liệu và 2 lời gọi hệ thống</b>; sendfile chuyển thẳng từ kênh tệp sang kênh socket, bỏ được 2 lần sao chép và 1 lời gọi</td></tr>
   <tr><td><b>Gộp lô</b> khi gửi và khi kéo</td><td>Mỗi yêu cầu kéo nhiều tin (thường vài trăm KB), chia nhỏ chi phí RPC</td></tr>
   <tr><td>CRC cho từng tin</td><td>Phát hiện hỏng log sau lỗi I/O và lỗi mạng</td></tr></table>
   <div class="callout good"><div class="lbl">Ý nghĩa</div>Phần lớn sức mạnh của Kafka đến từ việc <b>làm ít hơn</b> (không theo dõi trạng thái từng tin, không cache riêng, không truy cập ngẫu nhiên), chứ không phải từ thuật toán phức tạp hơn.
   Đây cũng là lý do Kafka dễ chạy ở tốc độ gần giới hạn của đĩa và mạng.</div>"""),
  dict(h="Điều phối bằng ZooKeeper trong bài 2011: bốn registry và ví dụ chia partition", body="""
   <p>Bài báo quyết định <b>partition là đơn vị song song nhỏ nhất</b>: tại một thời điểm, mọi tin của một partition chỉ do <b>một</b> consumer trong mỗi consumer group đọc.
   Nhờ vậy consumer chỉ cần phối hợp khi <i>cân bằng lại</i> (rebalance), một việc hiếm. Để phối hợp họ dùng ZooKeeper:</p>
   <table><tr><th>Registry trong ZooKeeper</th><th>Nội dung</th><th>Loại znode</th></tr>
   <tr><td>Broker registry</td><td>Host, cổng, tập topic và partition trên broker</td><td><b>Ephemeral</b></td></tr>
   <tr><td>Consumer registry</td><td>Consumer group và các topic đăng ký</td><td><b>Ephemeral</b></td></tr>
   <tr><td>Ownership registry</td><td>Với mỗi partition, id consumer đang sở hữu</td><td><b>Ephemeral</b></td></tr>
   <tr><td>Offset registry</td><td>Offset tin cuối cùng đã tiêu thụ của mỗi partition</td><td><b>Persistent</b></td></tr></table>
   <p><b>Ví dụ chia partition (minh hoạ, theo quy tắc range-partition của bài):</b> topic có 6 partition P0..P5, consumer group có C1, C2.</p>
   <table><tr><th>Thời điểm</th><th>Consumer</th><th>Partition nhận</th></tr>
   <tr><td>Hai consumer</td><td>C1 · C2</td><td>C1 = {P0, P1, P2} · C2 = {P3, P4, P5}</td></tr>
   <tr><td>C3 gia nhập (watcher báo thay đổi), cân bằng lại</td><td>C1 · C2 · C3</td><td>C1 = {P0, P1} · C2 = {P2, P3} · C3 = {P4, P5}</td></tr></table>
   <p style="font-size:.92rem">Nếu C3 muốn lấy P2 khi C2 chưa kịp nhả, C3 nhả hết partition đang giữ, chờ một chút rồi thử lại: bài báo nói quá trình thường ổn định sau vài lần thử.
   Bài báo cũng khuyên tạo <b>nhiều partition hơn nhiều so với số consumer</b> (over-partitioning) để tải thật sự cân bằng. Vì ba registry là ephemeral, broker hoặc consumer chết thì mục của nó tự biến mất và các watcher kích hoạt rebalance.</p>"""),
  dict(h="Cam kết giao hàng, thứ tự, và điều bài báo 2011 chưa có: replication", body="""
   <table><tr><th>Chủ đề</th><th>Điều bài báo nêu</th></tr>
   <tr><td>Cam kết giao hàng</td><td>Chỉ đảm bảo <b>at-least-once</b>. Exactly-once cần two-phase commit và không cần cho ứng dụng của họ. Thường mỗi tin giao đúng 1 lần cho mỗi consumer group; nhưng nếu consumer chết không tắt sạch, consumer thay thế có thể nhận trùng các tin sau offset cuối cùng đã ghi vào ZooKeeper</td></tr>
   <tr><td>Thứ tự</td><td>Đảm bảo thứ tự trong <b>cùng một partition</b>; không đảm bảo thứ tự giữa các partition</td></tr>
   <tr><td>Toàn vẹn</td><td>CRC mỗi tin; chạy quy trình phục hồi để loại tin có CRC sai</td></tr>
   <tr><td>Độ bền</td><td>Nếu broker chết, tin chưa tiêu thụ trên đó <b>không truy cập được</b>; nếu đĩa hỏng hẳn thì mất vĩnh viễn. Bài báo ghi <b>kế hoạch tương lai</b> là thêm replication có sẵn</td></tr></table>
   <div class="callout warn"><div class="lbl">Cách đọc cho đúng thời điểm</div>Phần replication (leader, follower, ISR) ở các phần trước của module này mô tả Kafka các phiên bản sau.
   Năm 2011 bài báo còn xem đó là việc sẽ làm. Khi gặp câu hỏi &quot;Kafka có nhân bản không&quot;, cần hỏi lại &quot;phiên bản nào, thời điểm nào&quot;.</div>
   <p>Nếu ứng dụng không chịu được trùng tin, bài báo gợi ý tự khử trùng bằng offset hoặc một khoá duy nhất trong tin: thường rẻ hơn two-phase commit và không bắt mọi người dùng cùng trả giá.</p>"""),
  dict(h="Hình gốc: Kafka tại LinkedIn, nơi dữ liệu chảy vào Hadoop", body=two(
   fig("kafka_fig3.png", "Nguồn: Kreps, Narkhede, Rao, NetDB 2011, Figure 3 (Kafka Deployment).", 330), """
   <ul style="margin:0;padding-left:20px;line-height:1.5">
   <li><b>Datacenter chính:</b> frontend gửi log theo lô qua <b>load balancer</b> tới các broker; dịch vụ thời gian thực đọc trực tiếp.</li>
   <li><b>Datacenter phân tích</b> (gần cụm Hadoop và kho dữ liệu): một cụm Kafka riêng chạy các consumer nhúng kéo dữ liệu từ datacenter chính.</li>
   <li><b>Nạp vào Hadoop</b> bằng một <i>Kafka input format</i> để job MapReduce đọc thẳng từ Kafka; broker không trạng thái và offset do client lưu khiến task MapReduce có thể lỗi và chạy lại mà không mất hay lặp tin.</li>
   <li>Tuần tự hoá bằng <b>Avro</b>, lưu id schema trong mỗi tin.</li></ul>""", "44%") + """
   <table><tr><th>Số liệu năm 2011 (theo bài báo)</th><th>Giá trị</th></tr>
   <tr><td>Dữ liệu mới mỗi ngày</td><td>Hàng trăm GB, gần <b>1 tỉ</b> thông điệp</td></tr>
   <tr><td>Độ trễ đầu-cuối cả pipeline (tới phân tích)</td><td>Khoảng <b>10 giây</b></td></tr></table>"""),
  dict(h="Số liệu thực nghiệm: Kafka so với ActiveMQ và RabbitMQ", body="""
   <p>Bài báo chạy thử trên 2 máy Linux (mỗi máy 8 nhân 2 GHz, 16 GB RAM, 6 ổ đĩa RAID 10, nối 1 Gb), so Kafka với ActiveMQ v5.4 và RabbitMQ v2.4. Producer gửi 10 triệu tin 200 byte.</p>
   <table><tr><th>Phép đo</th><th>Kafka</th><th>So sánh</th></tr>
   <tr><td>Producer, lô 1 tin</td><td>≈ <b>50.000</b> tin/giây</td><td>ActiveMQ và RabbitMQ không có cách gộp lô dễ dàng nên chỉ chạy lô 1</td></tr>
   <tr><td>Producer, lô 50 tin</td><td>≈ <b>400.000</b> tin/giây</td><td>Gộp lô tăng thông lượng gần một bậc độ lớn; 1 producer gần chạm trần đường 1 Gb</td></tr>
   <tr><td>Consumer</td><td>≈ <b>22.000</b> tin/giây</td><td>Hơn 4 lần ActiveMQ và RabbitMQ</td></tr>
   <tr><td>Chi phí thêm mỗi tin</td><td><b>9 byte</b></td><td>ActiveMQ <b>144 byte</b> (ActiveMQ dùng nhiều không gian hơn khoảng 70%)</td></tr></table>
   <p><b>Vì sao Kafka nhanh hơn (theo bài báo):</b> broker không phải duy trì trạng thái giao hàng của từng tin (ActiveMQ tốn thời gian ghi trang B-Tree quản lý metadata); header nhẹ, không phải header JMS nặng;
   gộp lô; sendfile giảm chi phí truyền.</p>
   <div class="callout info"><div class="lbl">Đọc kết quả cho công bằng</div>Chính bài báo thừa nhận ActiveMQ và RabbitMQ có <b>nhiều tính năng hơn</b> Kafka: phép so sánh cho thấy cái giá của các tính năng đó
   (theo dõi từng tin, header nặng), không phải kết luận &quot;Kafka tốt hơn mọi mặt&quot;.</div>"""),
 ])

QUIZ_KF = [
 dict(q="Theo bài báo Kafka, vì sao dùng mô hình pull thay vì push?",
  opts=["Vì pull luôn nhanh hơn push", "Mỗi consumer lấy theo tốc độ tối đa mình chịu được, không bị đẩy ngập, và dễ tua lại", "Vì push không dùng được với Hadoop", "Vì pull bắt buộc phải có ZooKeeper"],
  correct=1, explain="Bài báo nêu pull giúp consumer tiêu thụ theo năng lực và việc rewind dễ hơn trong mô hình pull."),
 dict(q="Tại sao tin trong Kafka được gọi bằng offset logic thay vì message id riêng?",
  opts=["Để dễ mã hoá bằng Avro", "Tránh duy trì cấu trúc chỉ mục truy cập ngẫu nhiên tốn seek đĩa; offset tin kế = offset hiện tại + độ dài tin", "Vì Kafka không lưu tin", "Vì offset ngẫu nhiên hơn"],
  correct=1, explain="Bài báo: bỏ chỉ mục ánh xạ message id sang vị trí; id tăng nhưng không liên tục, tính tin kế bằng cách cộng độ dài tin hiện tại."),
 dict(q="Trong bài 2011, registry nào của Kafka trong ZooKeeper là persistent (không phải ephemeral)?",
  opts=["Broker registry", "Consumer registry", "Ownership registry", "Offset registry"],
  correct=3, explain="Broker, consumer và ownership registry là ephemeral nên tự biến mất khi chết; offset registry persistent để lưu tiến độ đọc."),
 dict(q="Topic có 6 partition, consumer group có 3 consumer. Theo range-partition, mỗi consumer nhận bao nhiêu partition?",
  opts=["Mỗi consumer 1 partition", "Mỗi consumer 2 partition", "Một consumer 4, hai consumer 1", "Mỗi consumer 6 partition"],
  correct=1, explain="6 partition chia cho 3 consumer: 2 partition mỗi consumer (ví dụ C1={P0,P1}, C2={P2,P3}, C3={P4,P5})."),
 dict(q="Với sendfile, bài báo nói tiết kiệm được bao nhiêu so với cách gửi thông thường (4 lần sao chép, 2 lời gọi hệ thống)?",
  opts=["Bỏ 2 lần sao chép và 1 lời gọi hệ thống", "Bỏ toàn bộ sao chép", "Bỏ 1 lần sao chép", "Chỉ giảm lời gọi hệ thống"],
  correct=0, explain="sendfile chuyển trực tiếp từ kênh tệp sang kênh socket, tránh 2 trong 4 lần sao chép và 1 trong 2 lời gọi hệ thống."),
 dict(q="Bài báo Kafka 2011 nói gì về replication?",
  opts=["Đã có sẵn replication 3 bản như HDFS", "Không cần replication vì có ZooKeeper", "Replication chỉ dành cho consumer", "Là kế hoạch tương lai; hiện broker chết thì tin chưa tiêu thụ không truy cập được"],
  correct=3, explain="Bài báo ghi rõ kế hoạch thêm replication tích hợp; replication/ISR trong các phần trước thuộc các phiên bản sau."),
 dict(q="Vì sao Kafka chỉ đảm bảo at-least-once trong bài báo?",
  opts=["Vì exactly-once cần two-phase commit và không cần cho ứng dụng của họ; trùng tin hiếm khi xảy ra", "Vì Kafka không có offset", "Vì consumer không thể ack", "Vì ZooKeeper không đủ nhanh"],
  correct=0, explain="Trùng tin chỉ xảy ra khi consumer chết không tắt sạch, nhận lại các tin sau offset cuối cùng ghi vào ZooKeeper."),
 dict(q="Số liệu chi phí thêm mỗi tin trong thực nghiệm của bài báo là bao nhiêu?",
  opts=["Kafka 144 byte, ActiveMQ 9 byte", "Kafka 9 byte, ActiveMQ 144 byte", "Cả hai 9 byte", "Cả hai 144 byte"],
  correct=1, explain="Kafka 9 byte mỗi tin so với 144 byte của ActiveMQ; ActiveMQ dùng nhiều không gian hơn khoảng 70% để lưu cùng 10 triệu tin."),
]

HD05 = dict(inserts=[(1, PART_KF)], quiz=QUIZ_KF,
            logo_heads={"Hạn chế của các công cụ trước Kafka": ["apachekafka.svg", "linkedin.svg"],
                        "KRaft: Kafka tự quản lý metadata bằng giao thức Raft, không cần ZooKeeper": ["apachekafka.svg", "zookeeper.svg"]})

# =====================================================================================================
# HD-06: Oozie, ZooKeeper <- Chubby ; bản đồ tổng hợp
# =====================================================================================================
PART_CHUBBY = dict(
 title="Đọc trực tiếp bài báo Chubby (OSDI 2006): lock service, session, grace period, name service",
 bullets=[
  "Chubby ra đời vì sao: thay những cuộc bầu primary tuỳ tiện bằng một dịch vụ khoá dùng chung",
  "Cấu trúc một cell: 5 replica, 1 master, đa số mới sống",
  "Session, KeepAlive, lease và grace period khi master chết",
  "Bất ngờ: Chubby phổ biến nhất như một name server; phép tính 9 triệu yêu cầu"],
 slides=[
  dict(h="Chubby ra đời vì sao: lock service thay vì thư viện đồng thuận", body=logos("zookeeper.svg", "google.svg", h=40) + """
   <p>🗣️ <b>Nói nôm na:</b> trước khi có Chubby, mỗi nhóm kỹ sư tự nghĩ cách &quot;ai làm trưởng nhóm&quot; theo kiểu của mình; có nhóm cẩu thả, có nhóm phải nhờ người trực
   bấm nút. Chubby là một &quot;phòng bảo vệ chung&quot; trả lời một câu duy nhất, đáng tin: <i>ai đang giữ chìa khoá?</i></p>
   <table><tr><th>Lý do chọn lock service (bài báo nêu)</th><th>Giải thích</th></tr>
   <tr><td>Nhà phát triển thường không lo sẵn tính sẵn sàng cao</td><td>Hệ thống bắt đầu là prototype; thêm nhân bản và bầu primary về sau dễ hơn nếu gọi một khoá thay vì viết lại để tham gia giao thức đồng thuận</td></tr>
   <tr><td>Cần công bố kết quả bầu</td><td>Cho phép đọc ghi tệp nhỏ để primary được bầu tự công bố địa chỉ</td></tr>
   <tr><td>Giao diện khoá quen thuộc</td><td>Lập trình viên đã biết khoá, dù hay dùng sai khi phân tán</td></tr>
   <tr><td>Cần ít server hơn</td><td>Một dịch vụ khoá giúp ngay cả một client duy nhất cũng tiến triển an toàn; thư viện đồng thuận cần quorum phía client</td></tr></table>
   <div class="callout info"><div class="lbl">Ai dùng Chubby trong chính bài báo</div>GFS dùng khoá Chubby để chỉ định <b>master</b>; Bigtable dùng để bầu master, để master khám phá tablet server và để client tìm master;
   cả hai dùng Chubby làm nơi lưu một lượng nhỏ metadata ở vị trí &quot;ai cũng biết&quot;, nghĩa là làm gốc của cấu trúc dữ liệu phân tán. Một Chubby cell có thể phục vụ <b>mười nghìn máy</b> 4 bộ xử lý.</div>"""),
  dict(h="Hình gốc: cấu trúc một Chubby cell, 5 replica và một master", body=two(
   fig("chubby_fig1.png", "Nguồn: Burrows, <i>The Chubby lock service for loosely-coupled distributed systems</i>, OSDI 2006, Figure 1.", 230), """
   <ul style="margin:0;padding-left:20px;line-height:1.5">
   <li>Một <b>cell</b> gồm vài server (thường <b>5</b>) gọi là replica, đặt khác rack để giảm lỗi tương quan.</li>
   <li>Replica dùng <b>giao thức đồng thuận</b> bầu master: cần phiếu của đa số và lời hứa không bầu master khác trong vài giây (<i>master lease</i>).</li>
   <li>Chỉ master khởi xướng đọc/ghi cơ sở dữ liệu; replica khác sao chép cập nhật.</li>
   <li>Ghi được xác nhận khi tới <b>đa số</b> replica; đọc do master một mình phục vụ.</li></ul>""", "40%") + """
   <table><tr><th>Điểm</th><th>Số liệu trong bài</th></tr>
   <tr><td>Số replica cần sống để cell hoạt động</td><td>3 trong 5</td></tr>
   <tr><td>Bầu master mới</td><td>Thường vài giây; hai lần gần đây mất 6 s và 4 s, có lần tới 30 s</td></tr>
   <tr><td>Client tìm master</td><td>Hỏi các replica trong DNS, replica không phải master trả lời danh tính master</td></tr>
   <tr><td>Quy mô client</td><td>Nhiều instance phục vụ vài chục nghìn client; từng thấy <b>90.000</b> client nối thẳng tới một master</td></tr></table>
   <p style="font-size:.92rem">Đối chiếu ZooKeeper: một <i>ensemble</i> thường 3 hoặc 5 server, bầu một <i>leader</i>, ghi cần đa số (quorum). Ý tưởng đồng nhất, chi tiết giao thức khác nhau (Chubby dùng Paxos, ZooKeeper dùng ZAB).</p>"""),
  dict(h="Session, KeepAlive và lease: cách Chubby biết client còn sống", body="""
   <table><tr><th>Cơ chế</th><th>Chi tiết bài báo nêu</th></tr>
   <tr><td><b>Session</b></td><td>Quan hệ giữa client và cell, duy trì bằng các lần &quot;bắt tay&quot; định kỳ gọi là <b>KeepAlive</b></td></tr>
   <tr><td><b>Lease</b></td><td>Master gia hạn lease khi tạo session, khi chuyển master và khi trả lời KeepAlive. Mặc định kéo dài thêm <b>12 giây</b>; master quá tải có thể kéo tới khoảng <b>60 giây</b> để giảm số KeepAlive phải xử lý</td></tr>
   <tr><td>KeepAlive bị giữ lại</td><td>Master chủ động <i>chưa trả lời</i> KeepAlive tới khi lease cũ gần hết; client gửi ngay KeepAlive mới sau mỗi phản hồi, nên hầu như luôn có một KeepAlive đang chờ ở master</td></tr>
   <tr><td>Sự kiện và vô hiệu bộ đệm</td><td>Được gắn kèm vào phản hồi KeepAlive; vì vậy client không thể giữ session mà không xác nhận việc vô hiệu hoá cache</td></tr>
   <tr><td>Tải thực tế</td><td>RPC chủ yếu là KeepAlive; đọc dưới 10% tải; rất ít ghi và lấy khoá</td></tr></table>
   <div class="callout good"><div class="lbl">Ý tưởng đáng nhớ</div>Chubby biến &quot;còn sống hay không&quot; thành một khái niệm <b>có thời hạn</b> (lease). Không ai cần hỏi liên tục &quot;còn sống không&quot;: chỉ cần gia hạn, và
   quá hạn thì coi như mất. Đây chính là session và timeout của ZooKeeper; khi session hết hạn thì znode tạm (ephemeral) của client biến mất.</div>"""),
  dict(h="Hình gốc: grace period khi master chết, ý tưởng cho failover của ZooKeeper", body=fig("chubby_fig2.png",
   "Nguồn: Burrows, OSDI 2006, Figure 2 (thời gian chạy từ trái sang phải, không theo tỉ lệ).", 235) + """
   <table><tr><th>Diễn biến trên hình</th><th>Ý nghĩa</th><th>Trong ZooKeeper</th></tr>
   <tr><td>Master cũ chết trước khi trả lời KeepAlive, lease của client (C2) hết hạn</td><td>Client tạm hết lease nhưng chưa biết session còn sống không</td><td>Client chuyển sang trạng thái mất kết nối nhưng chưa hết timeout</td></tr>
   <tr><td>Client xoá cache, bắt đầu <b>grace period</b>, <b>chặn</b> lời gọi API (không huỷ session) và báo sự kiện <i>jeopardy</i></td><td>Ứng dụng tạm dừng thay vì thấy dữ liệu không nhất quán</td><td>Client chờ, tự nối lại tới server khác trong ensemble</td></tr>
   <tr><td>Master mới được bầu; KeepAlive đầu bị từ chối vì sai <i>epoch</i>, KeepAlive thứ hai thành công, sự kiện <i>safe</i></td><td>Ứng dụng tiếp tục như không có chuyện gì</td><td>Leader mới (ZAB), session còn hạn thì znode tạm còn nguyên</td></tr>
   <tr><td>Nếu bầu quá lâu, hết grace period</td><td>Client coi session hết hạn, báo lỗi cho ứng dụng</td><td>Session expired, znode tạm bị xoá</td></tr></table>"""),
  dict(h="Chubby làm name server: bài toán DNS và phép tính 9 triệu yêu cầu", body="""
   <p>Bài báo kể một bất ngờ: dù thiết kế để làm dịch vụ khoá, cách dùng <b>phổ biến nhất</b> của Chubby là làm <b>name server</b>.</p>
   <p>🗣️ <b>Nói nôm na:</b> DNS giống danh bạ in sẵn có hạn dùng (TTL): hết hạn thì phải tra lại. Nếu muốn danh bạ cập nhật nhanh, hạn dùng phải ngắn, và lượng người tra lại tăng vọt.
   Chubby giống nhóm chat: có thay đổi thì được báo ngay, không cần ai hỏi đi hỏi lại.</p>
   <table><tr><th>Bước tính (số liệu bài báo)</th><th>Kết quả</th></tr>
   <tr><td>1 job có 3.000 tiến trình, mỗi tiến trình nói chuyện với mọi tiến trình khác</td><td>$3\\,000^2 = 9\\,000\\,000$ yêu cầu tra tên</td></tr>
   <tr><td>Muốn bộ đệm DNS của job đó nhỏ như vậy phải tra lại thường xuyên</td><td>Khoảng <b>150.000</b> lượt tra/giây</td></tr>
   <tr><td>Một server DNS 2 CPU 2,6 GHz xử lý được cỡ 50.000 yêu cầu/giây</td><td>$150\\,000 / 50\\,000 = 3$ server chỉ cho <b>một</b> job 3.000 tiến trình</td></tr>
   <tr><td>Chubby dùng vô hiệu bộ đệm có chủ đích thay vì hết hạn theo thời gian</td><td>Một nhịp KeepAlive đều đặn đủ giữ <i>vô số</i> mục cache khi không có thay đổi</td></tr></table>
   <div class="callout warn"><div class="lbl">Cái giá đã phải trả</div>Khi mới triển khai name service trên Chubby, một job 3.000 tiến trình (9 triệu yêu cầu) có thể làm master &quot;quỵ gối&quot;.
   Giải pháp là máy chủ <b>proxy</b> gộp KeepAlive và đọc (giảm lưu lượng KeepAlive tới hệ số số client mỗi proxy, có thể 10.000 trở lên) và máy chủ chuyển giao thức sang DNS. Bài học dùng chung cho ZooKeeper: một dịch vụ điều phối
   nên giữ tải ghi rất thấp và tải đọc/giữ phiên được giảm bằng bộ đệm, proxy hay observer.</div>"""),
  dict(h="ZooKeeper và Chubby: giống ý tưởng, khác API", body="""
   <table><tr><th>Khía cạnh</th><th>Chubby (bài báo 2006)</th><th>ZooKeeper (Apache)</th></tr>
   <tr><td>Mô hình dữ liệu</td><td>Cây thư mục và <b>tệp nhỏ</b>, đọc/ghi cả tệp</td><td>Cây <b>znode</b>, mỗi znode giữ dữ liệu nhỏ</td></tr>
   <tr><td>Nút tạm</td><td>Ephemeral file: xoá khi không còn client giữ mở</td><td>Ephemeral znode: xoá khi session kết thúc</td></tr>
   <tr><td>Thông báo thay đổi</td><td>Event gắn vào phản hồi KeepAlive</td><td>Watch</td></tr>
   <tr><td>Khoá</td><td>Mỗi tệp/thư mục là khoá đọc-ghi <b>advisory</b>, có sequencer chống yêu cầu chậm</td><td>Không có API khoá riêng: khoá và bầu leader xây bằng znode tuần tự + ephemeral</td></tr>
   <tr><td>Đồng thuận</td><td>Paxos giữa 5 replica</td><td>ZAB (ZooKeeper Atomic Broadcast), họ Paxos</td></tr>
   <tr><td>Session</td><td>KeepAlive + lease, mặc định 12 s, grace period khi chuyển master</td><td>Heartbeat + session timeout</td></tr>
   <tr><td>Triển khai</td><td>Nội bộ Google, không mở</td><td>Mã nguồn mở, nền cho HBase, Kafka cũ, Hadoop HA</td></tr></table>
   <div class="callout info"><div class="lbl">Lưu ý về mức chắc chắn</div>Cột Chubby lấy từ bài báo. Cột ZooKeeper tóm tắt các khái niệm đã học ở các phần trước của module này; đây là đối chiếu về ý tưởng, không phải hai hệ thống có cùng API.</div>"""),
 ])

PART_MAP = dict(
 title="Bản đồ tổng hợp: lộ trình, liên kết giữa các công nghệ và tám bài báo gốc",
 bullets=[
  "Bốn nhánh: nghiên cứu nền tảng (Google), lõi Hadoop, công cụ hệ sinh thái, streaming",
  "Nét đứt = ý tưởng từ bài báo; nét liền = phụ thuộc lúc chạy",
  "Mỗi module của chuỗi này khớp với bài báo nào"],
 slides=[
  dict(h="Lộ trình nhiều nhánh: từ các bài báo Google tới hệ sinh thái Hadoop", body="""
   <p style="font-size:.95rem;margin:0 0 4px">Nét đứt xám = ý tưởng từ bài báo Google; nét liền = phụ thuộc lúc chạy (công cụ chạy trên Hadoop, HBase và Kafka dùng ZooKeeper, Kafka nạp dữ liệu vào HDFS).</p>
   """ + tech_timeline_svg()),
  dict(h="Mỗi module tương ứng bài báo nào, và logo công nghệ", body="""
   <table><tr><th>Module</th><th>Công nghệ</th><th>Bài báo nền tảng</th><th>Nơi công bố</th></tr>
   <tr><td>hd-01</td><td>""" + logo("apachehadoop.svg", 30) + """ HDFS</td><td>The Google File System (Ghemawat, Gobioff, Leung)</td><td>SOSP 2003</td></tr>
   <tr><td>hd-02</td><td>""" + logo("apachehadoop.svg", 30) + """ MapReduce, YARN</td><td>MapReduce: Simplified Data Processing on Large Clusters (Dean, Ghemawat)</td><td>OSDI 2004</td></tr>
   <tr><td>hd-03</td><td>""" + logo("pig.gif", 34) + logo("apachehive.svg", 30) + """ Pig, Hive</td><td>Không có một bài báo học thuật gốc; dựa trên MapReduce</td><td>Yahoo, Facebook</td></tr>
   <tr><td>hd-04</td><td>""" + logo("apachehbase.svg", 30) + logo("sqoop.png", 26) + """ HBase, Sqoop</td><td>Bigtable (Chang et al.)</td><td>OSDI 2006</td></tr>
   <tr><td>hd-05</td><td>""" + logo("apachekafka.svg", 30) + """ Kafka</td><td>Kafka: a Distributed Messaging System for Log Processing (Kreps, Narkhede, Rao)</td><td>NetDB 2011</td></tr>
   <tr><td>hd-06</td><td>""" + logo("oozie.png", 26) + logo("zookeeper.svg", 34) + """ Oozie, ZooKeeper</td><td>The Chubby lock service (Burrows)</td><td>OSDI 2006</td></tr>
   <tr><td>hd-07</td><td>Streaming và MPC</td><td>3 bài của thầy Tạ Duy Hoàng và cộng sự về chọn ngưỡng chia cây quyết định</td><td>arXiv 2024, ISIT 2025, ESA 2026</td></tr></table>
   <div class="callout good"><div class="lbl">Một nhận xét chung</div>Trong 5 bài nền tảng, bài nào cũng bắt đầu từ <b>một ràng buộc thực tế</b> (hỏng hóc là thường, tệp rất lớn, ghi nối thêm, tải KeepAlive chiếm đa số, log phải đi nhanh)
   rồi suy ra thiết kế. Việc đọc bài báo gốc giúp phân biệt phần nào là <i>nguyên lý</i> còn nguyên giá trị và phần nào là chi tiết của một thời điểm, như replication của Kafka 2011.</div>"""),
 ])

QUIZ_CH = [
 dict(q="Theo bài báo Chubby, để một Chubby cell hoạt động cần bao nhiêu replica còn sống trong tổng số 5?",
  opts=["2", "3", "4", "5"],
  correct=1, explain="Đa số, tức 3 trong 5, mới đủ để bầu master và xác nhận ghi."),
 dict(q="Mặc định lease Chubby kéo dài thêm bao lâu mỗi lần gia hạn, và master quá tải có thể kéo tới đâu?",
  opts=["1 giây, tới 5 giây", "12 giây, tới khoảng 60 giây", "60 giây, tới 10 phút", "5 phút, tới 1 giờ"],
  correct=1, explain="Mặc định 12 giây; khi quá tải master tăng tới khoảng 60 giây để giảm số KeepAlive phải xử lý."),
 dict(q="Grace period của Chubby phục vụ mục đích gì?",
  opts=["Tăng tốc đọc từ cache", "Cho client không vội huỷ session khi master chết mà chờ master mới trong thời gian ngắn", "Xoá tất cả khoá đang giữ", "Chuyển client sang cell khác ngay lập tức"],
  correct=1, explain="Client chặn lời gọi API, báo jeopardy, chờ master mới; nếu kịp (safe) tiếp tục như không có chuyện gì, nếu không thì session hết hạn."),
 dict(q="Một job 3.000 tiến trình, mỗi tiến trình nói chuyện với mọi tiến trình khác. Số lượt tra tên cần cỡ nào?",
  opts=["Khoảng 3.000", "Khoảng 6.000", "Khoảng 9 triệu", "Khoảng 9 tỉ"],
  correct=2, explain="3.000² = 9.000.000. Bài báo nói đây từng làm master Chubby quỵ khi mới triển khai name service."),
 dict(q="Vì sao Chubby dùng vô hiệu bộ đệm (invalidation) thay vì TTL như DNS?",
  opts=["Vì TTL không được hỗ trợ", "Vì một nhịp KeepAlive đều đặn đủ giữ nhiều mục cache vô thời hạn, khi không có thay đổi", "Vì invalidation rẻ hơn mọi trường hợp", "Vì client không có bộ đệm"],
  correct=1, explain="DNS với TTL ngắn làm tải tra cứu tăng vọt; Chubby chỉ gửi thông báo khi có thay đổi thật."),
 dict(q="Điểm khác chính giữa khoá của Chubby và cách làm khoá trên ZooKeeper là gì?",
  opts=["Chubby không có khoá", "ZooKeeper có API khoá riêng còn Chubby thì không", "Chubby có khoá advisory trên từng tệp; ZooKeeper dựng khoá bằng znode tuần tự và ephemeral", "Hai hệ thống giống hệt nhau"],
  correct=2, explain="Chubby mỗi tệp/thư mục là khoá đọc-ghi advisory; ZooKeeper cung cấp các nguyên liệu (znode, ephemeral, watch) để lập trình viên tự dựng khoá và bầu leader."),
 dict(q="Nhận định nào đúng về mức độ Bigtable phụ thuộc Chubby theo bài báo?",
  opts=["Không phụ thuộc", "Nếu Chubby không khả dụng lâu thì Bigtable cũng không khả dụng; đo được trung bình 0,0047% giờ-server bị ảnh hưởng", "Chỉ phụ thuộc khi khởi động", "Phụ thuộc hoàn toàn nên cứ 1 giờ lại mất dữ liệu"],
  correct=1, explain="Chubby nằm trên đường găng của master, vị trí khởi đầu và danh sách server; trung bình chỉ 0,0047% giờ-server bị ảnh hưởng, cụm tệ nhất 0,0326%."),
 dict(q="Bài học chung nào của bài báo Chubby áp dụng cho ZooKeeper?",
  opts=["Nên ghi dữ liệu lớn vào dịch vụ điều phối", "Nên giữ tải ghi rất thấp và giảm tải đọc, giữ phiên bằng bộ đệm hoặc proxy", "Nên cho mọi client nối thẳng tới leader", "Nên bỏ session"],
  correct=1, explain="Tải của Chubby chủ yếu là KeepAlive, đọc dưới 10% và rất ít ghi; vì vậy các cơ chế giảm tải KeepAlive là then chốt."),
]

HD06 = dict(inserts=[(4, PART_CHUBBY), (9, PART_MAP)], quiz=QUIZ_CH,
            logo_heads={"🗣️ Nói nôm na: Oozie": ["oozie.png"],
                        "🗣️ Nói nôm na: lý do cần ZooKeeper": ["zookeeper.svg", "google.svg"]})
