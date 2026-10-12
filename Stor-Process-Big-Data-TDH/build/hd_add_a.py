# -*- coding: utf-8 -*-
"""Bổ sung cho hd-01, hd-02, hd-03: đọc trực tiếp bài báo GFS (SOSP 2003) và MapReduce (OSDI 2004),
thêm ví dụ lấy từ chính bài báo, logo công nghệ. Mọi con số trích từ bài báo gốc trong thư mục
References/Foundational, hoặc là phép tính có hiển thị từng bước từ các con số đó. Các ví dụ tự dựng
được gắn nhãn (minh hoạ)/(giả định)."""
from hd_add_common import fig, logo, logos, two

# =====================================================================================================
# HD-01: HDFS <- GFS
# =====================================================================================================
PART_GFS = dict(
 title="Đọc trực tiếp bài báo Google File System (SOSP 2003): từ giả định thiết kế tới HDFS",
 bullets=[
  "Bốn quan sát về khối lượng công việc của Google dẫn tới toàn bộ thiết kế GFS",
  "Hình gốc kiến trúc: 1 master + nhiều chunkserver; client không bao giờ đọc/ghi dữ liệu qua master",
  "Luồng ghi: lease 60 giây, pipeline dữ liệu, thứ tự do primary quyết định",
  "Hot spot, nhân bản lại có ưu tiên, trải bản sao qua các rack: những chi tiết HDFS thừa hưởng"],
 slides=[
  dict(h="Bài báo GFS: bốn quan sát về khối lượng công việc dẫn tới cả thiết kế", body=logos("apachehadoop.svg", "google.svg") + """
   <p>🗣️ <b>Nói nôm na:</b> trước khi xây nhà kho, người thiết kế hỏi hàng hoá thực tế là gì: pallet nặng hay
   gói nhỏ lẻ, ai lấy hàng, bao lâu có một xe hỏng. GFS làm đúng như vậy: nhóm tác giả không thiết kế một hệ
   file "hoàn hảo" nói chung, mà thiết kế cho đúng 4 quan sát về công việc của Google, kể cả khi 4 quan sát
   đó đi ngược lại giả định của các hệ file cũ.</p>
   <table><tr><th>Quan sát trong bài báo</th><th>Quyết định thiết kế</th><th>Dấu vết ở HDFS</th></tr>
   <tr><td><b>Hỏng hóc là chuyện thường:</b> hàng trăm tới hàng nghìn máy rẻ tiền, luôn có máy đang hỏng</td>
   <td>Giám sát liên tục, phát hiện lỗi, tự phục hồi, mỗi chunk có 3 bản sao mặc định</td>
   <td>Heartbeat, nhân bản 3 lần, tái nhân bản tự động</td></tr>
   <tr><td><b>Tệp rất lớn:</b> tệp nhiều GB là bình thường, quản lý hàng tỉ tệp cỡ KB là &quot;khó xử lý&quot;</td>
   <td>Chunk 64 MB, chấp nhận tệp nhỏ nhưng không tối ưu cho chúng</td>
   <td>Block 64 rồi 128 MB, small-files problem</td></tr>
   <tr><td><b>Ghi nối thêm, hiếm khi ghi đè:</b> ghi ngẫu nhiên giữa tệp &quot;gần như không tồn tại&quot;</td>
   <td>Tối ưu cho append và đọc tuần tự, không cache dữ liệu ở client</td>
   <td>Write-once, read-many; append</td></tr>
   <tr><td><b>Băng thông bền vững quan trọng hơn độ trễ:</b> ứng dụng xử lý theo lô</td>
   <td>Thiết kế cho thông lượng, nới lỏng mô hình nhất quán, thêm <i>record append</i> nguyên tử</td>
   <td>Thông lượng cao thay vì độ trễ thấp</td></tr></table>
   <div class="callout info"><div class="lbl">Quy mô lúc công bố (2003)</div>Cụm lớn nhất có hơn 1000 nút lưu trữ,
   hơn 300 TB đĩa, và hàng trăm client truy cập liên tục. Tức là Hadoop học theo một hệ thống đã chạy thật ở
   quy mô nghìn máy, không phải một ý tưởng trên giấy.</div>"""),
  dict(h="Hình gốc: kiến trúc GFS và cách client đọc một tệp", body="""
   """ + two(fig("gfs_fig1.png", "Nguồn: Ghemawat, Gobioff, Leung, <i>The Google File System</i>, SOSP 2003, Figure 1.", 270), """
   <ul style="margin:0;padding-left:20px;line-height:1.5"><li><b>master</b>: giữ toàn bộ metadata trong RAM: không gian tên, ánh xạ tệp → chunk,
   vị trí các bản sao; tương ứng NameNode</li>
   <li><b>chunkserver</b>: lưu chunk như tệp Linux thường; tương ứng DataNode</li>
   <li><b>client</b>: hỏi master <i>một lần</i> để biết chunk nằm ở đâu, lưu đệm kết quả, rồi nói chuyện thẳng với
   chunkserver (mũi tên dày trên hình)</li></ul>""", "50%") + """
   <p><b>Phép tính từng bước:</b> vì sao metadata nằm gọn trong RAM của master? Bài báo nêu master giữ <i>dưới 64 byte</i>
   metadata cho mỗi chunk 64 MB. Với 1 PB dữ liệu ($2^{50}$ byte):</p>
   <div class="pd-formula"><div class="pd-formula-math">\\frac{2^{50}}{2^{26}} = 2^{24} = 16\\,777\\,216\\ \\text{chunk};\\quad 16\\,777\\,216 \\times 64\\ \\text{byte} = 2^{30}\\ \\text{byte} = 1\\ \\text{GiB}</div></div>
   <p>Một petabyte dữ liệu cần chưa tới 1 GiB metadata: đây là lý do chọn chunk lớn và chọn <b>một master duy nhất</b>.
   HDFS có con số riêng cho mỗi block, nhưng nguyên lý giống hệt: RAM của NameNode quyết định số block quản lý được.</p>
   <div class="callout good"><div class="lbl">Client không cache dữ liệu, chỉ cache metadata</div>Bài báo giải thích:
   ứng dụng đọc tuần tự tệp khổng lồ nên cache dữ liệu ở client không có lợi, bỏ nó giúp loại bỏ luôn vấn đề
   nhất quán cache. Chunkserver cũng không cache vì bộ đệm của Linux đã làm việc đó.</div>"""),
  dict(h="Hình gốc: luồng ghi, lease 60 giây và pipeline dữ liệu", body=two(fig("gfs_fig2.png",
   "Nguồn: Ghemawat, Gobioff, Leung, SOSP 2003, Figure 2 (mũi tên mảnh = điều khiển, mũi tên dày = dữ liệu).", 330), """
   <ol style="margin:0 0 8px;padding-left:20px;line-height:1.5">
   <li>Client hỏi master ai đang giữ <b>lease</b> (primary) và vị trí các replica.</li>
   <li>Master trả lời; client lưu đệm.</li>
   <li>Client đẩy <b>dữ liệu</b> tới mọi replica theo một chuỗi, theo thứ tự bất kỳ.</li>
   <li>Khi mọi replica đã nhận, client gửi yêu cầu ghi tới primary.</li>
   <li>Primary đánh số thứ tự, áp dụng, rồi chuyển yêu cầu cho các secondary.</li>
   <li>Secondary báo đã xong; 7. primary báo lại cho client.</li></ol>""", "40%") + """
   <p>🗣️ <b>Nói nôm na:</b> như một tổ trưởng điều ca. Hàng hoá (dữ liệu) được chuyền tay nhau dọc theo dây chuyền cho
   nhanh, còn quyết định &quot;ai ghi trước, ai ghi sau&quot; do một người (primary) ghi vào sổ để mọi nơi giống nhau.</p>
   <table><tr><th>Chi tiết trong bài</th><th>Ý nghĩa</th></tr>
   <tr><td>Lease của primary có timeout ban đầu <b>60 giây</b>, có thể gia hạn</td><td>Master mất liên lạc với primary vẫn có thể cấp lease mới sau khi lease cũ hết hạn, không sợ hai primary cùng lúc</td></tr>
   <tr><td>Dữ liệu đi theo <b>chuỗi</b> tới máy &quot;gần&quot; nhất chưa nhận, không rẽ nhánh kiểu cây</td><td>Mỗi máy dùng trọn băng thông ra của mình thay vì chia nhỏ cho nhiều người nhận</td></tr>
   <tr><td>Thời gian lý tưởng đẩy $B$ byte tới $R$ replica: $B/T + R\\cdot L$</td><td>Với $T=100$ Mbps và $L<1$ ms, 1 MB mất khoảng 80 ms: $8\\ \\text{Mb}/100\\ \\text{Mbps}=80$ ms</td></tr></table>
   <p style="font-size:.9rem;color:var(--muted)">HDFS ghi cũng theo pipeline DataNode, và gói xác nhận (ack) chạy ngược về client: cùng nguyên tắc tách luồng dữ liệu khỏi luồng điều khiển.</p>"""),
  dict(h="Hot spot trong GFS: bài học về một tệp quá nóng", body="""
   <p>🗣️ <b>Nói nôm na:</b> một cuốn sách duy nhất, cả lớp 300 người cùng ập vào xin đọc lúc 8 giờ sáng: thư viện có
   nhiều kệ cũng vô ích, vì cuốn đó chỉ nằm ở vài kệ.</p>
   <p>Bài báo kể lại một sự cố có thật khi GFS mới được dùng bởi hệ thống xếp lịch lô: một tệp thực thi được ghi vào
   GFS thành tệp <b>1 chunk</b>, rồi khởi chạy trên <b>hàng trăm máy cùng lúc</b>. Vài chunkserver giữ chunk đó bị
   hàng trăm yêu cầu đồng thời đè sập.</p>
   <table><tr><th>Cách khắc phục trong bài</th><th>Ý nghĩa tổng quát</th><th>Tình huống tương tự (minh hoạ)</th></tr>
   <tr><td>Lưu các tệp thực thi như vậy với <b>hệ số nhân bản cao hơn</b></td><td>Dữ liệu &quot;nóng&quot; cần nhiều bản sao hơn dữ liệu nguội</td><td>Thư viện in nhiều bản cho giáo trình bắt buộc</td></tr>
   <tr><td>Làm hệ thống xếp lịch <b>giãn thời điểm khởi động</b> các ứng dụng</td><td>Giảm đỉnh tải thay vì chỉ thêm tài nguyên</td><td>Nhà trường chia nhiều đợt đăng ký học phần</td></tr>
   <tr><td>Hướng lâu dài: cho client đọc dữ liệu từ <b>client khác</b></td><td>Biến người đọc thành nguồn phát</td><td>Chia sẻ ngang hàng khi cập nhật phần mềm</td></tr></table>
   <div class="callout warn"><div class="lbl">Liên hệ với Hadoop</div>Hadoop có đúng nguyên lý này: các tệp mà mọi task cùng
   cần (ví dụ jar của job) được nhân bản nhiều hơn mặc định (cấu hình mặc định của MapReduce là 10 bản), để tránh
   cùng một DataNode bị hàng nghìn task xin cùng lúc. Bản chất vẫn là hot spot GFS năm 2003.</div>"""),
  dict(h="Chịu lỗi theo bài báo: nhân bản lại có ưu tiên, trải bản sao qua các rack", body="""
   <p>Bài báo mô tả khá chi tiết cách master xử lý khi chunk mất bản sao. Mỗi chi tiết đều có dấu vết ở HDFS:</p>
   <table><tr><th>Cơ chế trong GFS</th><th>Chi tiết bài báo nêu</th><th>Tương ứng HDFS</th></tr>
   <tr><td>Phát hiện chunkserver chết</td><td>Master và mọi chunkserver trao đổi <i>HeartBeat</i> định kỳ</td><td>Heartbeat DataNode → NameNode</td></tr>
   <tr><td>Nhân bản lại</td><td>Ngay khi số bản sao khả dụng thấp hơn mục tiêu; chunk mất <b>2</b> bản được ưu tiên hơn chunk mất 1 bản; chunk của tệp còn sống ưu tiên hơn chunk của tệp vừa xoá</td><td>Hàng đợi under-replicated, ưu tiên cao cho block còn ít bản sao nhất</td></tr>
   <tr><td>Chọn nơi đặt bản mới</td><td>Cân bằng dung lượng đĩa, giới hạn số lần &quot;clone&quot; đồng thời trên 1 chunkserver, <b>trải qua nhiều rack</b></td><td>Rack awareness</td></tr>
   <tr><td>Phát hiện bản cũ (stale)</td><td>Dùng số phiên bản chunk; bản stale không bao giờ tham gia ghi hay được trả cho client, bị dọn rác sớm nhất có thể</td><td>Generation stamp của block</td></tr>
   <tr><td>Phát hiện dữ liệu hỏng</td><td>Checksum trên từng chunk</td><td>Checksum khi đọc/ghi block</td></tr></table>
   <p><b>Tại sao trải qua nhiều rack?</b> Bài báo nêu hai lý do: nếu cả rack mất điện hoặc mất switch, vẫn còn bản sao ở rack khác; và việc đọc có thể tận dụng
   băng thông tổng của nhiều rack. Đổi lại, ghi phải đi qua nhiều rack, một đánh đổi bài báo chấp nhận có chủ đích.</p>"""),
 ])

QUIZ_GFS = [
 dict(q="Theo bài báo GFS, master giữ khoảng bao nhiêu metadata cho mỗi chunk 64 MB?",
  opts=["Dưới 64 byte cho mỗi chunk", "Khoảng 64 KB cho mỗi chunk", "Bằng đúng kích thước chunk, tức 64 MB", "Không giữ gì, chỉ chunkserver mới giữ"],
  correct=0, explain="Bài báo nêu master giữ dưới 64 byte metadata cho mỗi chunk 64 MB, nên metadata của cả petabyte vẫn nằm gọn trong RAM một máy."),
 dict(q="Phép tính: 1 PB dữ liệu chia chunk 64 MB, mỗi chunk dưới 64 byte metadata. Tổng metadata tối đa cỡ nào?",
  opts=["Khoảng 1 TiB", "Khoảng 1 GiB", "Khoảng 64 MiB", "Khoảng 16 GiB"],
  correct=1, explain="2^50 / 2^26 = 2^24 = 16.777.216 chunk; nhân 64 byte = 2^30 byte = 1 GiB. Đây là lý do một master duy nhất vẫn đủ."),
 dict(q="Lease mà GFS master cấp cho replica primary có timeout ban đầu bao lâu, và để làm gì?",
  opts=["60 phút; để chunkserver tự bầu primary", "5 giây; để kiểm tra checksum", "60 giây; giảm tải quản lý ở master và cố định thứ tự biến đổi", "Không có timeout, lease vĩnh viễn"],
  correct=2, explain="Lease mở đầu 60 giây, có thể gia hạn. Primary đánh số thứ tự các biến đổi nên thứ tự toàn cục xác định bởi lease và số thứ tự."),
 dict(q="Vì sao GFS tách luồng dữ liệu khỏi luồng điều khiển khi ghi?",
  opts=["Để dữ liệu đi theo chuỗi tới máy gần nhất chưa nhận, tận dụng trọn băng thông ra mỗi máy, còn primary lo thứ tự ghi",
        "Để master có thể kiểm tra nội dung từng gói dữ liệu",
        "Để client không cần biết vị trí các replica",
        "Để tránh phải dùng TCP"],
  correct=0, explain="Dữ liệu pipeline theo mạng, điều khiển đi qua primary. Với T=100 Mbps, 1 MB phân phối lý tưởng chỉ khoảng 80 ms."),
 dict(q="Sự cố hot spot đầu tiên của GFS xảy ra trong tình huống nào và được sửa ra sao?",
  opts=["Tệp thực thi 1 chunk bị hàng trăm máy khởi chạy cùng lúc; sửa bằng nhân bản nhiều hơn và giãn thời điểm khởi động",
        "Master hết RAM; sửa bằng thêm master thứ hai",
        "Chunkserver hỏng đĩa; sửa bằng chunk nhỏ hơn",
        "Client cache sai; sửa bằng bỏ cache metadata"],
  correct=0, explain="Dữ liệu nóng cần hệ số nhân bản cao hơn, và nên giảm đỉnh tải bằng cách giãn thời điểm khởi động."),
 dict(q="Khi một chunk mất 2 bản sao so với chunk chỉ mất 1 bản, master GFS xử lý thế nào?",
  opts=["Xử lý như nhau theo thứ tự đến", "Ưu tiên cao hơn cho chunk mất 2 bản", "Bỏ qua cả hai cho tới khi người vận hành can thiệp", "Chỉ nhân bản lại chunk của tệp đã xoá"],
  correct=1, explain="Chunk càng ít bản sao càng nguy cơ mất dữ liệu cao, nên được ưu tiên; chunk của tệp còn sống cũng được ưu tiên hơn chunk của tệp vừa xoá."),
]

HD01 = dict(inserts=[(1, PART_GFS)], quiz=QUIZ_GFS,
            logo_heads={"Nutch: công cụ tìm kiếm sinh ra Hadoop": ["apachehadoop.svg", "yahoo.svg"]})

# =====================================================================================================
# HD-02: MapReduce
# =====================================================================================================
PART_MR = dict(
 title="Đọc trực tiếp bài báo MapReduce (OSDI 2004): luồng thực thi, số liệu thật và cách chịu lỗi",
 bullets=[
  "Sáu bước thực thi trong hình gốc, và mỗi thành phần tương ứng gì trong Hadoop",
  "Sáu ví dụ ngay trong bài báo: một khung, nhiều bài toán khác nhau",
  "Số liệu thật: 29.423 job tháng 8/2004, mỗi job trung bình 157 máy",
  "Chịu lỗi bằng tái thực thi, backup task, chọn số task M và R"],
 slides=[
  dict(h="Hình gốc: sáu bước thực thi và tên gọi tương ứng trong Hadoop", body=logos("apachehadoop.svg", "google.svg") + two(
   fig("mr_fig1.png", "Nguồn: Dean, Ghemawat, <i>MapReduce: Simplified Data Processing on Large Clusters</i>, OSDI 2004, Figure 1.", 320), """
   <ol style="margin:0;padding-left:20px;line-height:1.5">
   <li><b>fork</b>: chương trình người dùng khởi tạo master và các worker; dữ liệu vào chia thành $M$ split.</li>
   <li>Master giao <b>map task</b> và <b>reduce task</b> cho các worker rảnh.</li>
   <li>Map worker <b>đọc</b> split, gọi hàm map, giữ cặp trung gian trong bộ nhớ.</li>
   <li>Định kỳ <b>ghi xuống đĩa cục bộ</b>, chia thành $R$ vùng theo hàm phân vùng (ví dụ hash(key) mod $R$).</li>
   <li>Reduce worker <b>đọc từ xa</b> (remote read) các vùng của mình từ đĩa của map worker, rồi sắp theo khoá.</li>
   <li>Gọi hàm reduce, <b>ghi</b> tệp đầu ra (vào hệ file phân tán).</li></ol>""", "46%") + """
   <table><tr><th>Trong bài báo</th><th>Trong Hadoop</th></tr>
   <tr><td>Master</td><td>JobTracker (Hadoop 1.x), ApplicationMaster (YARN)</td></tr>
   <tr><td>Worker</td><td>TaskTracker (1.x), NodeManager chạy container (2.x)</td></tr>
   <tr><td>Bước (5) remote read + sắp xếp</td><td>Giai đoạn <b>shuffle &amp; sort</b></td></tr>
   <tr><td>Tệp trung gian trên đĩa cục bộ</td><td>Map output spill trên đĩa của node chạy map</td></tr></table>"""),
  dict(h="Sáu ví dụ ngay trong bài báo: một khung, nhiều bài toán", body="""
   <p>🗣️ <b>Nói nôm na:</b> MapReduce giống một dây chuyền chia bài tập: mỗi người chỉ cần biết làm 1 việc nhỏ
   (map: gắn nhãn từng phiếu, reduce: gộp các phiếu cùng nhãn). Bài báo chứng minh khung đó đủ rộng bằng 6 ví dụ
   thật của Google (đây là ví dụ <i>trong bài báo</i>, không phải ví dụ tự dựng).</p>
   <table><tr><th>Bài toán</th><th>Hàm map</th><th>Hàm reduce</th></tr>
   <tr><td>Distributed Grep</td><td>Phát ra dòng nào khớp mẫu</td><td>Hàm đồng nhất: chỉ sao chép dữ liệu trung gian ra đầu ra</td></tr>
   <tr><td>Đếm lượt truy cập URL</td><td>Từ log phát ra cặp $\\langle URL, 1\\rangle$</td><td>Cộng các giá trị cùng URL, phát ra $\\langle URL, tổng\\rangle$</td></tr>
   <tr><td>Đồ thị liên kết ngược</td><td>Với mỗi liên kết từ trang <i>source</i> tới <i>target</i>, phát ra $\\langle target, source\\rangle$</td><td>Gom danh sách source cho mỗi target</td></tr>
   <tr><td>Term-vector theo host</td><td>Phát ra $\\langle host, term\\ vector\\rangle$ cho mỗi tài liệu</td><td>Cộng các term-vector của cùng host, bỏ từ hiếm</td></tr>
   <tr><td>Chỉ mục ngược (inverted index)</td><td>Phát ra $\\langle word, documentID\\rangle$</td><td>Sắp các documentID, phát ra $\\langle word, list(documentID)\\rangle$</td></tr>
   <tr><td>Sắp xếp phân tán (distributed sort)</td><td>Trích khoá, phát ra $\\langle key, record\\rangle$</td><td>Phát ra tất cả cặp không đổi; việc sắp xếp do hàm phân vùng và thứ tự khoá lo</td></tr></table>
   <div class="callout good"><div class="lbl">Vì sao chọn đúng 6 ví dụ này</div>Chúng phủ cả lọc, đếm, đảo quan hệ, gộp theo nhóm và sắp xếp. Ví dụ
   <i>Distributed Sort</i> còn là bước đầu của thuật toán MPC trong các bài báo của thầy (module hd-07): sắp theo $x$ trong $O(1)$ vòng.</div>"""),
  dict(h="Số liệu thật: 29.423 job trong tháng 8/2004 và mức tăng chỉ sau 18 tháng", body="""
   <div style="display:flex;gap:18px;align-items:flex-start;justify-content:center">""" + fig("mr_fig4.png", "Figure 4: số chương trình MapReduce trong kho mã, từ 0 (đầu 2003) lên gần 900 (9/2004).", 270) +
   fig("mr_table1.png", "Table 1: job MapReduce chạy tháng 8/2004 (Dean, Ghemawat, OSDI 2004).", 270) + """</div>
   <p><b>Phép tính từ bảng (số liệu gốc của bài báo):</b></p>
   <table><tr><th>Đại lượng</th><th>Tính</th><th>Ý nghĩa</th></tr>
   <tr><td>Dữ liệu trung gian so với đầu vào</td><td>758 / 3.288 ≈ 23%</td><td>Map đã lọc/rút gọn dữ liệu trước khi shuffle</td></tr>
   <tr><td>Dữ liệu đầu ra so với đầu vào</td><td>193 / 3.288 ≈ 5,9%</td><td>Kết quả cuối nhỏ hơn đầu vào cỡ 17 lần</td></tr>
   <tr><td>Đầu vào mỗi map task</td><td>3.288 TB / 29.423 job / 3.351 map task ≈ 33 MB</td><td>Khớp khuyến nghị 16 đến 64 MB mỗi task (xem slide sau)</td></tr>
   <tr><td>Số map task trên mỗi reduce task</td><td>3.351 / 55 ≈ 61</td><td>Pha map rộng hơn pha reduce hàng chục lần</td></tr></table>
   <div class="callout warn"><div class="lbl">Con số quan trọng nhất</div>Mỗi job trung bình có <b>1,2</b> lần worker chết (trên 157 máy). Hỏng hóc không phải biến cố hiếm mà là chuyện xảy ra
   ở hầu như mọi job, nên chịu lỗi phải là phần lõi của khung, không phải tính năng thêm vào.</div>"""),
  dict(h="Chịu lỗi theo bài báo: tái thực thi là cơ chế chính, backup task cứu đuôi dài", body="""
   <table><tr><th>Tình huống</th><th>Cách xử lý trong bài báo</th><th>Vì sao</th></tr>
   <tr><td>Worker không trả lời</td><td>Master ping định kỳ; worker im lặng bị coi là chết</td><td>Phát hiện lỗi đơn giản</td></tr>
   <tr><td>Map task <b>đã xong</b> trên máy chết</td><td><b>Chạy lại</b></td><td>Đầu ra nằm trên đĩa cục bộ của máy đó nên không còn đọc được</td></tr>
   <tr><td>Reduce task đã xong trên máy chết</td><td>Không cần chạy lại</td><td>Đầu ra nằm trong hệ file toàn cục</td></tr>
   <tr><td>Straggler: 1 máy chậm bất thường ở những task cuối</td><td>Gần xong thì master chạy thêm <b>backup execution</b>, task xong khi một trong hai bản xong</td><td>Một máy chậm kéo dài cả job</td></tr>
   <tr><td>Bản ghi gây lỗi lặp lại</td><td>Sau hơn 1 lần lỗi trên cùng bản ghi, master bỏ qua bản ghi đó ở lần chạy lại</td><td>Một dòng dữ liệu xấu không làm hỏng cả job</td></tr></table>
   <p><b>Hai thí nghiệm trong bài (sort):</b></p>
   <ul style="margin:6px 0 0;padding-left:20px;line-height:1.5">
   <li>Cố ý <b>giết 200 trong 1746 worker</b> giữa chừng: job vẫn xong sau 933 giây, chỉ chậm hơn 5% so với chạy bình thường.</li>
   <li><b>Tắt backup task</b>: job mất 1283 giây, chậm hơn <b>44%</b>: vài task đuôi kéo dài thêm khoảng 300 giây sau khi gần như mọi task khác đã xong.</li></ul>
   <div class="callout info"><div class="lbl">Ý nghĩa chung</div>Nhờ hàm map và reduce là hàm thuần (cùng đầu vào cho cùng đầu ra), chạy lại hay chạy hai bản không đổi kết quả:
   đó là điều kiện để &quot;tái thực thi&quot; trở thành cơ chế chịu lỗi chính.</div>"""),
  dict(h="Chọn số task M và R, và vì sao dữ liệu nằm sẵn trên máy lại quan trọng", body="""
   <p>🗣️ <b>Nói nôm na:</b> chia 1000 bài kiểm tra cho 10 giám khảo, bạn chia thành 10 xấp hay 1000 tờ lẻ? Xấp lớn thì có người xong sớm ngồi chơi, tờ lẻ thì mất công phát từng tờ.
   MapReduce chọn khoảng giữa: chia vừa đủ nhỏ để cân tải, vừa đủ lớn để điều phối không quá tốn.</p>
   <table><tr><th>Quy tắc trong bài báo</th><th>Số liệu</th></tr>
   <tr><td>Mỗi map task xử lý chừng</td><td><b>16 đến 64 MB</b> đầu vào (để tối ưu <i>data locality</i>)</td></tr>
   <tr><td>$R$ chọn bằng</td><td>một bội số nhỏ của số worker dự kiến dùng</td></tr>
   <tr><td>Ví dụ job thật</td><td>$M = 200\\,000$, $R = 5\\,000$, <b>2.000 worker</b></td></tr>
   <tr><td>Giới hạn thực tế</td><td>Master phải đưa ra $O(M+R)$ quyết định lập lịch và giữ $O(M\\times R)$ trạng thái trong bộ nhớ</td></tr></table>
   <p><b>Tính:</b> $M\\times R = 200\\,000 \\times 5\\,000 = 10^9$ cặp (map task, reduce task) mà master phải theo dõi: đó là lý do không thể chọn $M$ và $R$ lớn vô hạn.</p>
   <p><b>Data locality:</b> dữ liệu đầu vào nằm trên đĩa của chính các máy trong cụm, do GFS chia khối 64 MB và giữ thường 3 bản sao. Master xếp map task lên máy đang giữ một bản sao,
   hoặc máy gần nó, để phần lớn dữ liệu đọc ở đĩa cục bộ thay vì qua mạng. Đây cũng là lý do Hadoop đặt tính toán gần dữ liệu thay vì kéo dữ liệu về chỗ tính.</p>"""),
 ])

QUIZ_MR = [
 dict(q="Theo Figure 1 của bài MapReduce, reduce worker lấy dữ liệu của map worker bằng cách nào?",
  opts=["Map worker đẩy trực tiếp qua bộ nhớ chung", "Đọc từ xa (remote read) từ đĩa cục bộ của map worker", "Qua hệ file toàn cục như tệp đầu ra", "Qua master chuyển tiếp từng cặp"],
  correct=1, explain="Map ghi cặp trung gian xuống đĩa cục bộ chia thành R vùng; master báo vị trí và reduce worker đọc từ xa (bước 5)."),
 dict(q="Vì sao map task đã hoàn thành trên máy chết phải chạy lại, còn reduce task đã hoàn thành thì không?",
  opts=["Vì hàm map chậm hơn hàm reduce", "Vì reduce chạy trên máy mạnh hơn", "Vì master chỉ nhớ được các reduce task",
        "Vì đầu ra map nằm trên đĩa cục bộ của máy chết, còn đầu ra reduce nằm trong hệ file toàn cục"],
  correct=3, explain="Đầu ra map không còn truy cập được khi máy chết; đầu ra reduce đã lưu ở hệ file phân tán nên còn nguyên."),
 dict(q="Trong thí nghiệm sort, tắt cơ chế backup task làm job chậm hơn bao nhiêu?",
  opts=["Khoảng 5%", "Khoảng 10%", "Khoảng 44%", "Khoảng 200%"],
  correct=2, explain="Job mất 1283 giây, chậm hơn 44%, vì vài task đuôi (straggler) kéo dài. Con số 5% là mức chậm khi giết 200 trong 1746 worker."),
 dict(q="Từ Table 1: 3.288 TB đầu vào, 29.423 job, trung bình 3.351 map task mỗi job. Mỗi map task xử lý khoảng bao nhiêu dữ liệu?",
  opts=["Khoảng 3 MB", "Khoảng 33 MB", "Khoảng 330 MB", "Khoảng 3 GB"],
  correct=1, explain="3.288 TB / 29.423 ≈ 0,112 TB mỗi job ≈ 112 GB; chia 3.351 task ≈ 33 MB, nằm trong khoảng 16 đến 64 MB mà bài báo khuyến nghị."),
 dict(q="Với M = 200.000 map task và R = 5.000 reduce task, số cặp (map, reduce) master phải theo dõi cỡ nào?",
  opts=["Khoảng 205.000", "Khoảng 40 triệu", "Khoảng 1 tỉ (10^9)", "Khoảng 1.000 tỉ"],
  correct=2, explain="M × R = 200.000 × 5.000 = 10^9. Vì master giữ O(M × R) trạng thái nên M và R không thể tăng vô hạn."),
 dict(q="Ví dụ Distributed Sort trong bài báo, hàm reduce làm gì?",
  opts=["Phát ra mọi cặp không đổi; việc sắp xếp do phân vùng và thứ tự khoá đảm nhiệm", "Tự thực hiện thuật toán quicksort trên mọi cặp", "Gộp các bản ghi trùng khoá thành một", "Đếm số bản ghi của mỗi khoá"],
  correct=0, explain="Map trích khoá và phát <key, record>; reduce chỉ phát lại. Khung đã sắp xếp khoá trung gian nên đầu ra theo thứ tự."),
 dict(q="Vì sao chạy lại hay chạy song song hai bản của cùng một task (backup) không làm sai kết quả?",
  opts=["Vì master chọn ngẫu nhiên kết quả", "Vì hàm map và reduce là hàm thuần: cùng đầu vào cho cùng đầu ra", "Vì dữ liệu chỉ được đọc một lần", "Vì mỗi task chạy trên một máy riêng biệt"],
  correct=1, explain="Tính xác định (thuần) của hàm cho phép tái thực thi và backup: task xong khi một trong hai bản xong."),
]

HD02 = dict(inserts=[(1, PART_MR)], quiz=QUIZ_MR,
            logo_heads={"Ba vai trò mới của YARN": ["apachehadoop.svg"],
                        "🗣️ Nói nôm na: MapReduce là gì trước khi vào kỹ thuật": ["apachehadoop.svg", "google.svg"]})

# =====================================================================================================
# HD-03: Pig / Hive  (ví dụ lấy từ bài MapReduce, viết lại bằng Pig và HiveQL)
# =====================================================================================================
PART_PIGHIVE_PAPER = dict(
 title="Ví dụ từ bài MapReduce, viết lại bằng Pig và Hive: đếm lượt truy cập URL và đồ thị liên kết ngược",
 bullets=[
  "Hai bài toán gốc trong bài MapReduce (2004), giờ chỉ còn 2 đến 3 dòng script",
  "Tính tay có combiner: 10 cặp giảm còn 6 cặp",
  "Đồ thị liên kết ngược bằng Pig (GROUP) và HiveQL (collect_list)"],
 slides=[
  dict(h="Đếm lượt truy cập URL: cùng một bài, ba cách viết, có tính tay", body=logos("pig.gif", "apachehive.svg", "apachehadoop.svg", h=36) + """
   <p>Trong bài MapReduce, ví dụ <i>Count of URL Access Frequency</i>: map đọc log phát ra $\\langle URL,1\\rangle$,
   reduce cộng lại. Với Pig hay Hive, cùng bài toán không còn cần viết hai hàm Java.</p>
   <table><tr><th>Cách viết</th><th>Mã</th></tr>
   <tr><td>MapReduce (ý tưởng trong bài)</td><td>map: <code>emit(url, 1)</code>; reduce: cộng các giá trị cùng <code>url</code></td></tr>
   <tr><td>Pig Latin</td><td><code>log = LOAD 'log' AS (url:chararray); g = GROUP log BY url; c = FOREACH g GENERATE group, COUNT(log);</code></td></tr>
   <tr><td>HiveQL</td><td><code>SELECT url, COUNT(*) FROM log GROUP BY url;</code></td></tr></table>
   <p><b>Tính tay (dữ liệu giả định, 10 yêu cầu):</b> /home, /cart, /home, /home, /cart | /pay, /home, /search, /cart, /home (hai mapper, mỗi mapper 5 dòng).</p>
   <table><tr><th></th><th>Mapper A (5 dòng đầu)</th><th>Mapper B (5 dòng sau)</th><th>Cặp đi qua mạng</th></tr>
   <tr><td>Không combiner</td><td>5 cặp (url,1)</td><td>5 cặp (url,1)</td><td><b>10</b></td></tr>
   <tr><td>Có combiner</td><td>(/home,3) (/cart,2)</td><td>(/pay,1) (/home,2) (/search,1) (/cart,1)</td><td><b>6</b>, giảm 40%</td></tr></table>
   <p>Reduce cộng: /home = 3 + 2 = <b>5</b>; /cart = 2 + 1 = <b>3</b>; /pay = 1; /search = 1; tổng 10 yêu cầu, khớp. Pig và Hive đều
   dịch bài này thành đúng chuỗi map, combine, shuffle, reduce ở trên.</p>"""),
  dict(h="Đồ thị liên kết ngược: gom danh sách thay vì cộng số", body="""
   <p>Ví dụ thứ hai trong bài MapReduce: <i>Reverse Web-Link Graph</i>. Map phát $\\langle target, source\\rangle$ cho mỗi liên kết;
   reduce gom danh sách các <i>source</i> trỏ tới mỗi <i>target</i>. Khác ví dụ trước: reduce không cộng số mà <b>gom thành danh sách</b>.</p>
   <table><tr><th>Cách viết</th><th>Mã</th></tr>
   <tr><td>Pig Latin</td><td><code>links = LOAD 'links' AS (source:chararray, target:chararray); g = GROUP links BY target; rev = FOREACH g GENERATE group, links.source;</code></td></tr>
   <tr><td>HiveQL</td><td><code>SELECT target, collect_list(source) FROM links GROUP BY target;</code></td></tr></table>
   <p><b>Tính tay (dữ liệu giả định, 6 liên kết source → target):</b> A→C, B→C, D→C, A→B, C→A, D→A.</p>
   <table><tr><th>Bước</th><th>Kết quả</th></tr>
   <tr><td>Map phát $\\langle target, source\\rangle$</td><td>(C,A) (C,B) (C,D) (B,A) (A,C) (A,D)</td></tr>
   <tr><td>Shuffle nhóm theo target</td><td>A: [C, D] · B: [A] · C: [A, B, D]</td></tr>
   <tr><td>Reduce ghi danh sách</td><td>A ← {C, D} · B ← {A} · C ← {A, B, D}</td></tr></table>
   <div class="callout good"><div class="lbl">Kiểm tra nhanh</div>Tổng độ dài các danh sách = 2 + 1 + 3 = 6 = số liên kết ban đầu: không mất cũng không dư.
   Đây là cách Google xây chỉ mục ngược các liên kết, và là một trong những bài toán gốc khiến MapReduce ra đời.</div>"""),
 ])

PART_PIGHIVE_MAP = dict(
 title="Pig và Hive trên bản đồ hệ sinh thái: ai tạo ra, vì bài toán nào",
 bullets=[
  "Pig: Yahoo Research, Hive: Facebook, cùng giải nỗi đau 'viết Java MapReduce quá tốn công'",
  "Tez, Spark, Flink: các engine chạy trên YARN thay MapReduce",
  "Bảng tổng hợp có logo từng công nghệ"],
 slides=[
  dict(h="Bản đồ nguồn gốc: công nghệ nào sinh ra ở đâu, để giải quyết gì", body="""
   <table><tr><th>Công nghệ</th><th>Khởi nguồn</th><th>Nỗi đau gốc</th><th>Liên hệ với module này</th></tr>
   <tr><td>""" + logo("pig.gif", 40) + """ Pig</td><td>""" + logo("yahoo.svg", 26) + """ Yahoo Research</td><td>Viết MapReduce bằng Java quá tốn công</td><td>Ngôn ngữ dataflow thủ tục</td></tr>
   <tr><td>""" + logo("apachehive.svg", 36) + """ Hive</td><td>""" + logo("meta.svg", 26) + """ Facebook</td><td>Dân phân tích muốn dùng SQL trên kho dữ liệu hàng chục PB</td><td>SQL khai báo, Metastore</td></tr>
   <tr><td>""" + logo("tez.jpg", 30) + """ Tez</td><td>Cộng đồng Apache (Hortonworks dẫn dắt Stinger)</td><td>MapReduce quá chậm cho truy vấn tương tác</td><td>Engine thay thế của Hive</td></tr>
   <tr><td>""" + logo("apachespark.svg", 30) + """ Spark</td><td>Cộng đồng Apache</td><td>Tác vụ lặp cần giữ dữ liệu trong bộ nhớ</td><td>Hive on Spark, Pig on Spark</td></tr>
   <tr><td>""" + logo("apacheflink.svg", 30) + """ Flink</td><td>Cộng đồng Apache</td><td>Xử lý luồng thời gian thực</td><td>Cạnh tranh trên cùng YARN</td></tr></table>
   <div class="callout info"><div class="lbl">Điểm chung</div>Pig và Hive không thay MapReduce, mà <b>che</b> nó đi: cả hai đều dịch ra job MapReduce (và sau này Tez, Spark),
   nên mọi điều đã học về shuffle, combiner, số vòng ở module hd-02 vẫn là &quot;giá thật&quot; phía dưới mỗi câu lệnh.</div>"""),
 ])

QUIZ_PH = [
 dict(q="Trong ví dụ đếm lượt truy cập 10 yêu cầu qua 2 mapper, combiner làm giảm số cặp đi qua mạng từ 10 xuống 6. Mức giảm là bao nhiêu?",
  opts=["20%", "30%", "40%", "60%"],
  correct=2, explain="(10 - 6) / 10 = 40%. Mapper A gộp thành (/home,3), (/cart,2); mapper B gộp thành 4 cặp: tổng 6."),
 dict(q="Hàm nào của Hive dùng để gom danh sách các source cho mỗi target trong bài đồ thị liên kết ngược?",
  opts=["SUM", "collect_list", "COUNT(*)", "ROW_NUMBER"],
  correct=1, explain="SELECT target, collect_list(source) FROM links GROUP BY target gom danh sách; tương đương GROUP rồi FOREACH GENERATE group, links.source trong Pig."),
 dict(q="Với 6 liên kết A→C, B→C, D→C, A→B, C→A, D→A, đồ thị liên kết ngược có danh sách nào cho C?",
  opts=["{A, B, D}", "{A, D}", "{C}", "{B, C}"],
  correct=0, explain="Các liên kết trỏ tới C là từ A, B và D. Tổng độ dài các danh sách (2+1+3) bằng 6 liên kết ban đầu."),
 dict(q="Điểm khác nhau chính giữa bài đếm URL và bài đồ thị liên kết ngược ở bước reduce là gì?",
  opts=["Đếm URL cộng số, còn đồ thị liên kết ngược gom thành danh sách", "Đếm URL không cần shuffle", "Đồ thị liên kết ngược không cần hàm map", "Hai bài hoàn toàn giống nhau"],
  correct=0, explain="Reduce của bài đếm cộng các giá trị 1; reduce của bài đồ thị gom các source thành danh sách."),
 dict(q="Pig và Hive liên hệ thế nào với MapReduce theo cách nhìn của module này?",
  opts=["Thay thế hoàn toàn MapReduce", "Che MapReduce đi nhưng vẫn dịch xuống chuỗi job, nên shuffle và số vòng vẫn là giá thật", "Chỉ dùng cho dữ liệu nhỏ", "Không liên quan tới Hadoop"],
  correct=1, explain="Cả hai dịch câu lệnh ra job MapReduce (hoặc Tez, Spark), vì vậy kiến thức về shuffle và combiner vẫn áp dụng."),
]

HD03 = dict(inserts=[(4, PART_PIGHIVE_PAPER), (9, PART_PIGHIVE_MAP)], quiz=QUIZ_PH,
            logo_heads={"Động lực của Yahoo khi tạo ngôn ngữ \"ở giữa\"": ["pig.gif", "yahoo.svg"],
                        "Từ 6 người dùng tới 20-30% toàn công ty": ["apachehive.svg", "meta.svg"]})
