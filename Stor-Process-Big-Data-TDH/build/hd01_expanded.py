# -*- coding: utf-8 -*-
"""Bản MỞ RỘNG SÂU của module hd-01-hadoop-hdfs (n=25), viết theo chuẩn 02-module-content-standard.md
(build-complete-self-study-system): mỗi khái niệm có nói nôm na -> giải thích kỹ thuật -> ví dụ >=2-3
ngành có nhãn (minh hoạ)/(giả định) -> bảng HTML thật -> phép tính từng bước. Mọi fact lịch sử giữ
đúng nguyên những gì đã verify qua web search trong phiên làm việc trước (Nutch, GFS/MapReduce paper
Google, tên Hadoop, Yahoo, Cloudera/Hortonworks) - không thêm fact lịch sử mới chưa verify. Rack
awareness/heartbeat/small-files problem là kiến trúc HDFS tiêu chuẩn đã công bố chính thức trong tài
liệu Apache Hadoop, không cần trích nguồn lịch sử riêng (khác với các fact về "ai tạo ra, năm nào").
KHÔNG sửa hadoop_deepdive_content.py gốc - file này để merge sau."""

HD01_EXPANDED = dict(
 n=25, slug="hd-01-hadoop-hdfs", title="Vì sao Hadoop ra đời, và HDFS giải quyết bài toán gì",
 tag="Lịch sử Hadoop · Kiến trúc HDFS",
 intro="Hadoop không phải một sản phẩm được thiết kế trong phòng họp — nó ra đời từ nhu cầu rất cụ thể của một công cụ tìm kiếm mã nguồn mở đang chết dần vì không mở rộng được.",
 parts=[

  # ---------------------------------------------------------------- PHẦN 1
  dict(title="Từ Nutch tới Hadoop: một câu chuyện có thật", bullets=[
    "2002: Doug Cutting & Mike Cafarella xây Nutch — công cụ tìm kiếm mở, nhưng kiến trúc không scale",
    "2003-2004: hai bài báo của Google (GFS, MapReduce) chỉ ra lối ra",
    "2006: Cutting vào Yahoo, phần lưu trữ+xử lý của Nutch được tách ra, đặt tên Hadoop",
    "Hadoop không phải sản phẩm của 1 công ty — nó là mô hình mã nguồn mở điển hình"],
   slides=[
    dict(h="Nutch: công cụ tìm kiếm sinh ra Hadoop", body="""
      <p>🗣️ <b>Nói nôm na:</b> giống như một nhóm sinh viên tự viết phần mềm quản lý thư viện cho trường
      mình, rồi nhận ra trường càng đông, chương trình càng ì ạch — cho tới khi đọc được 2 bài hướng dẫn
      "cách Google quản lý thư viện khổng lồ của họ" và quyết định viết lại từ đầu theo cách đó.</p>
      <p>Trước khi có Hadoop, Doug Cutting và Mike Cafarella đã xây <b>Apache Nutch</b> (2002) — một công cụ
      tìm kiếm web mã nguồn mở. Vấn đề: muốn thu thập và đánh chỉ mục cả Internet, Nutch cần lưu trữ và xử lý
      dữ liệu ở quy mô vượt xa khả năng một máy chủ, nhưng chưa có kiến trúc phân tán phù hợp.</p>
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>Doug Cutting và Mike Cafarella hình thành
      ý tưởng Hadoop dựa trên bài báo <i>Google File System</i> (tháng 10/2003); phát triển ban đầu nằm trong
      dự án Apache Nutch, rồi tách sang dự án con Hadoop vào tháng 1/2006.
      Nguồn: <a href="https://en.wikipedia.org/wiki/Apache_Hadoop" target="_blank">Apache Hadoop — Wikipedia</a>,
      <a href="https://informationweek.com/software-services/hadoop-at-10-doug-cutting-on-making-big-data-work" target="_blank">InformationWeek — Hadoop at 10</a>.</div>
      <p>Đây là chi tiết quan trọng để hiểu <b>vì sao</b> Hadoop có 2 trụ cột tách biệt (lưu trữ HDFS + xử lý
      MapReduce) — vì chính 2 bài báo Google mà Cutting/Cafarella đọc cũng tách biệt 2 vấn đề đó.</p>
      <table><tr><th>Thời điểm</th><th>Sự kiện</th></tr>
      <tr><td>2002</td><td>Nutch ra đời — công cụ tìm kiếm mở, chạy được nhưng không mở rộng được khi dữ liệu lớn</td></tr>
      <tr><td>10/2003</td><td>Google công bố paper GFS — mô hình lưu trữ phân tán cho dữ liệu khổng lồ</td></tr>
      <tr><td>2004</td><td>Google công bố paper MapReduce — mô hình xử lý song song đơn giản hoá</td></tr>
      <tr><td>01/2006</td><td>Phần lưu trữ + xử lý của Nutch tách ra thành dự án con Hadoop, Cutting gia nhập Yahoo!</td></tr></table>"""),
    dict(h="Nguồn gốc cái tên \"Hadoop\"", body="""
      <p>🗣️ <b>Nói nôm na:</b> không có ý nghĩa kỹ thuật gì cả — giống việc một công ty đặt tên sản phẩm
      theo tên con mèo của người sáng lập, miễn là cái tên dễ nhớ và chưa ai dùng.</p>
      <div class="callout good"><div class="lbl">📚 Nguồn lịch sử</div>Doug Cutting (khi đó làm ở Yahoo!) đặt
      tên Hadoop theo <b>tên con voi nhồi bông</b> của con trai ông. Theo lời Cutting: "Cái tên con tôi đặt cho
      một con voi nhồi bông màu vàng. Ngắn, dễ đánh vần, dễ đọc, vô nghĩa, và chưa ai dùng — đó là tiêu chí đặt
      tên của tôi." Con voi này giờ "nghỉ hưu" trong tủ đồ của Cutting, chỉ được mang ra trong các buổi keynote.
      Nguồn: <a href="https://www.cio.com/article/3027631/apache-hadoop-turns-10.html" target="_blank">CIO.com — Apache Hadoop turns 10</a>.</div>
      <p>Chi tiết này không phải giai thoại vô bổ: nó cho thấy văn hoá đặt tên "ngắn - dễ nhớ - không gây hiểu
      lầm về công nghệ" của cả hệ sinh thái Hadoop sau này (Pig, Hive, ZooKeeper, Oozie, Sqoop... đều là tên
      vật/khái niệm đời thường, không phải từ viết tắt).</p>"""),
    dict(h="Vì sao mã nguồn mở là điều kiện bắt buộc, không phải lựa chọn phong cách", body="""
      <p>🗣️ <b>Nói nôm na:</b> giống việc nhiều trường đại học cùng góp sách vào 1 thư viện chung, thay vì
      mỗi trường tự xây 1 thư viện riêng — ai cũng được dùng, ai cũng có thể đóng góp sửa lỗi/thêm sách.</p>
      <p>Google KHÔNG công bố mã nguồn GFS/MapReduce — chỉ công bố Ý TƯỞNG qua 2 bài báo khoa học. Cutting/
      Cafarella phải tự viết lại toàn bộ từ đầu dựa trên ý tưởng đó. Việc Hadoop sau đó được đưa vào Apache
      Software Foundation (mã nguồn mở, miễn phí, ai cũng sửa/đóng góp được) là lý do nó lan rộng nhanh hơn
      bất kỳ hệ thống thương mại đóng nào ở cùng thời điểm.</p>
      <table><tr><th>Ngành</th><th>Ví dụ tương tự &quot;mô hình mở&quot; so với &quot;đóng&quot;</th></tr>
      <tr><td>Y tế <i>(minh hoạ)</i></td><td>Phác đồ điều trị công khai trên tạp chí y khoa (ai cũng áp dụng, phản biện được) so với công thức thuốc độc quyền 1 công ty giữ kín</td></tr>
      <tr><td>Giáo dục <i>(minh hoạ)</i></td><td>Giáo trình mở (OpenCourseWare) nhiều trường cùng chỉnh sửa, so với giáo trình nội bộ chỉ 1 trường được dùng</td></tr>
      <tr><td>Nông nghiệp <i>(minh hoạ)</i></td><td>Giống lúa lai được công bố quy trình lai tạo cho nông dân tự nhân, so với giống độc quyền chỉ 1 công ty bán hạt giống</td></tr></table>
      <div class="callout warn"><div class="lbl">Cảnh báo hiểu nhầm phổ biến</div>Hadoop không "sao chép" GFS/
      MapReduce — nó là 1 bản <b>triển khai lại độc lập</b> dựa trên Ý TƯỞNG công bố trong paper, không phải
      Google cho Hadoop dùng chung mã nguồn.</div>""")]),

  # ---------------------------------------------------------------- PHẦN 2
  dict(title="Kiến trúc Master/Slave: NameNode & DataNode", bullets=[
    "NameNode (master) chỉ giữ metadata — không giữ dữ liệu thật",
    "DataNode (slave) giữ dữ liệu thật, xử lý I/O trực tiếp",
    "Ví dụ đa ngành: thư viện trung tâm, bệnh viện tuyến trên, tổng đài điều phối"],
   slides=[
    dict(h="Vai trò của NameNode và DataNode", body="""
      <p>🗣️ <b>Nói nôm na:</b> NameNode giống như quyển SỔ MỤC LỤC của thư viện — ghi "cuốn sách X nằm ở
      kệ nào, phòng nào" nhưng không giữ cuốn sách thật; DataNode giống các KỆ SÁCH thật, nơi nội dung sách
      nằm vật lý.</p>
      <p>HDFS theo kiến trúc <b>Master/Slave</b>: <b>NameNode</b> (master) chỉ lưu <i>metadata</i> — cấu trúc
      thư mục, tên tệp, và bảng ánh xạ tệp → vị trí các block trên DataNode nào. <b>DataNode</b> (slave) mới
      là nơi lưu dữ liệu thật và trực tiếp phục vụ đọc/ghi.</p>
      <ul class="pd-legend"><li><b>fsimage</b><span>ảnh chụp toàn bộ namespace tại một thời điểm</span></li>
      <li><b>edit log</b><span>nhật ký các thay đổi từ sau fsimage gần nhất — NameNode phát lại log này khi
      khởi động để khôi phục trạng thái mới nhất</span></li></ul>
      <table><tr><th>Ngành</th><th>Vai trò giống NameNode (chỉ biết &quot;ở đâu&quot;)</th><th>Vai trò giống DataNode (giữ nội dung thật)</th></tr>
      <tr><td>Y tế <i>(minh hoạ)</i></td><td>Hệ thống tra cứu mã hồ sơ bệnh nhân tại bệnh viện tuyến trên</td><td>Tập hồ sơ giấy/điện tử thật lưu tại từng khoa/phòng khám</td></tr>
      <tr><td>Logistics <i>(minh hoạ)</i></td><td>Phần mềm điều phối trung tâm biết "lô hàng mã X đang ở kho nào"</td><td>Hàng hoá thật nằm trong từng kho hàng khu vực</td></tr>
      <tr><td>Viễn thông <i>(minh hoạ)</i></td><td>Tổng đài điều phối biết "cuộc gọi này nên chuyển tới trạm nào"</td><td>Trạm phát sóng thật xử lý tín hiệu</td></tr></table>
      <div class="callout warn"><div class="lbl">Vì sao đây là điểm yếu kiến trúc ban đầu</div>Vì toàn bộ
      metadata chỉ nằm ở 1 NameNode, nên bản Hadoop 1.0 có 1 <b>Single Point of Failure</b>: NameNode hỏng là
      cả cụm mất khả năng định vị dữ liệu, dù dữ liệu vật lý trên DataNode vẫn còn nguyên. Hadoop 2.0 sau này
      giải quyết bằng Standby NameNode (High Availability) — khác với Secondary NameNode (chỉ gộp log, không
      phải bản dự phòng nóng, xem Phần 6).</div>"""),
    dict(h="📖 Giải thích cho người mới bắt đầu: lý do tách hai vai trò", body="""
      <details>
      <summary><b>Bấm để xem giải thích cực đơn giản</b></summary>
      <p>Hãy tưởng tượng bạn quản lý một kho hàng khổng lồ với 10 triệu món đồ. Nếu bạn để MỘT người vừa
      phải NHỚ "món đồ A nằm ở kệ 347, món đồ B nằm ở kệ 892..." (tức là vai trò ghi nhớ vị trí), VỪA phải
      tự tay đi lấy từng món đồ khi có người hỏi (tức là vai trò vận chuyển vật lý) — người đó sẽ kiệt sức
      ngay khi kho lớn lên.</p>
      <p>Giải pháp: tách thành 2 việc. Một người (hoặc 1 cuốn sổ) CHỈ cần nhớ vị trí — đây là NameNode.
      Nhiều người khác (DataNode) mỗi người phụ trách 1 khu vực kệ hàng, chỉ cần lấy đúng món khi được chỉ
      tới đúng vị trí. Nhờ vậy có thể tăng số "người lấy hàng" (DataNode) lên hàng nghìn mà "cuốn sổ ghi vị
      trí" (NameNode) không cần phình to tương ứng — vì nó chỉ ghi VỊ TRÍ, không ghi NỘI DUNG món hàng.</p>
      </details>"""),
    dict(h="fsimage & edit log: vì sao NameNode không mất trí nhớ khi khởi động lại", body="""
      <p>🗣️ <b>Nói nôm na:</b> giống việc kế toán công ty giữ 1 cuốn sổ cái tổng hợp cuối tháng (fsimage) và
      1 cuốn sổ nháp ghi từng giao dịch mới trong tháng (edit log) — muốn biết số dư hiện tại, chỉ cần lấy
      sổ cái tháng trước, rồi cộng/trừ theo đúng từng dòng trong sổ nháp.</p>
      <p>Khi NameNode khởi động lại, nó không cần "nhớ lại từ đầu": nó đọc <b>fsimage</b> gần nhất (ảnh chụp
      toàn bộ namespace), rồi phát lại toàn bộ <b>edit log</b> (các thay đổi từ sau fsimage đó) để tái tạo
      đúng trạng thái mới nhất trước khi dừng.</p>
      <table><tr><th>Ngành</th><th>Tương tự fsimage</th><th>Tương tự edit log</th></tr>
      <tr><td>Ngân hàng <i>(minh hoạ)</i></td><td>Bảng sao kê số dư đầu kỳ</td><td>Lịch sử từng giao dịch trong kỳ</td></tr>
      <tr><td>Phần mềm kế toán <i>(minh hoạ)</i></td><td>File backup cuối tuần</td><td>Nhật ký thao tác hàng ngày từ sau backup</td></tr></table>""")]),

  # ---------------------------------------------------------------- PHẦN 3
  dict(title="Block: chia tệp lớn thành khối quản lý được", bullets=[
    "Tệp chia thành block lớn (64MB → 128MB)",
    "Vì sao không dùng block nhỏ như hệ file thường (4KB)",
    "Small-files problem: khi HDFS gặp quá nhiều tệp nhỏ"],
   slides=[
    dict(h="Block và lý do kích thước lớn", body="""
      <p>🗣️ <b>Nói nôm na:</b> giống việc chia 1 cuộn vải khổng lồ thành các súc vải 50 mét, thay vì cắt
      thành hàng triệu miếng vải 10cm — quản lý vài trăm súc vải dễ hơn hẳn quản lý hàng triệu miếng nhỏ,
      dù tổng khối lượng vải là như nhau.</p>
      <p>Mỗi tệp trong HDFS được <b>chia thành nhiều block</b> (khối dữ liệu) thay vì lưu nguyên khối như hệ
      file thông thường.</p>
      <div class="pd-formula"><div class="pd-formula-label">Kích thước block mặc định</div>
      <div class="pd-formula-math">64\\text{ MB (ban đầu)} \\to 128\\text{ MB (mặc định từ các bản sau)}</div></div>
      <table><tr><th>Ngành</th><th>Ví dụ chia khối lớn thay vì đơn vị nhỏ</th></tr>
      <tr><td>Xuất bản <i>(minh hoạ)</i></td><td>Một bộ sách 20 tập được đóng gói vận chuyển theo TẬP (không tách rời từng trang) để giảm số đơn hàng cần theo dõi</td></tr>
      <tr><td>Logistics <i>(minh hoạ)</i></td><td>Hàng hoá đóng theo pallet 1 tấn, không theo từng gói nhỏ 1kg, để giảm số nhãn mã vận đơn cần quản lý</td></tr>
      <tr><td>Y tế <i>(minh hoạ)</i></td><td>Phim X-quang 1 ca khám lưu thành 1 bộ file duy nhất, không tách từng lát cắt CT riêng lẻ, để hồ sơ không bị phân mảnh</td></tr></table>
      <div class="callout info"><div class="lbl">Vì sao block lớn, không nhỏ như hệ file thường (4KB)</div>
      Block lớn giảm số lượng entry metadata mà NameNode phải giữ trong RAM — đây là lý do HDFS tối ưu cho
      "vài trăm MB đến vài TB" một tệp, không phải cho rất nhiều tệp nhỏ.</div>"""),
    dict(h="Small-files problem: khi lý thuyết \"block lớn\" trở thành vấn đề thật", body="""
      <p>🗣️ <b>Nói nôm na:</b> nếu bạn có 1 triệu tờ giấy ghi chú 1 trang, dù mỗi tờ rất nhẹ, việc quản lý
      1 triệu HỒ SƠ RIÊNG LẺ (mỗi hồ sơ cần 1 mục trong danh bạ) nặng hơn hẳn so với quản lý 10 cuốn sách
      1000 trang — kể cả khi tổng số trang bằng nhau.</p>
      <p>Mỗi tệp trong HDFS (dù chỉ 1KB) vẫn cần ÍT NHẤT 1 entry metadata trên NameNode (giữ tên tệp, quyền,
      vị trí block). Nếu hệ thống chứa hàng triệu tệp nhỏ, RAM của NameNode (hữu hạn) có thể bị "ngập" bởi
      entry metadata, dù tổng dung lượng dữ liệu thật rất nhỏ.</p>
      <table><tr><th>Tình huống <i>(giả định, minh hoạ nguyên lý)</i></th><th>Số tệp</th><th>Dung lượng thật</th><th>Số entry metadata</th><th>Vấn đề?</th></tr>
      <tr><td>Lưu 1.000 video, mỗi video 1GB</td><td>1.000</td><td>1.000 GB</td><td>1.000</td><td>Không — đúng use case HDFS</td></tr>
      <tr><td>Lưu 10 triệu ảnh thumbnail, mỗi ảnh 20KB</td><td>10.000.000</td><td>~200 GB</td><td>10.000.000</td><td>Có — RAM NameNode phải giữ 10 triệu entry cho lượng dữ liệu nhỏ hơn hẳn</td></tr></table>
      <div class="callout warn"><div class="lbl">Cảnh báo bẫy hiểu nhầm</div>Người mới học dễ nghĩ "HDFS lưu
      được dữ liệu lớn nên lưu tệp nào cũng tốt" — SAI. HDFS tối ưu cho SỐ LƯỢNG TỆP VỪA PHẢI, KÍCH THƯỚC MỖI
      TỆP LỚN; giải pháp thực tế cho hàng triệu tệp nhỏ là gộp chúng lại (vd dùng Hadoop Archive/SequenceFile)
      trước khi đưa vào HDFS, không lưu trực tiếp từng tệp nhỏ riêng lẻ.</div>""")]),

  # ---------------------------------------------------------------- PHẦN 4
  dict(title="Replication: nhân bản để chịu lỗi", bullets=[
    "Mỗi block nhân bản 3 lần trên các DataNode khác nhau",
    "Ví dụ đa ngành: dự phòng dữ liệu ngân hàng, hồ sơ y tế đa viện, kho hàng đa khu vực",
    "Tính xác suất mất dữ liệu khi nhiều bản sao cùng hỏng"],
   slides=[
    dict(h="Cơ chế nhân bản (replication)", body="""
      <p>🗣️ <b>Nói nôm na:</b> giống việc một gia đình quan trọng luôn in 3 bản giấy khai sinh và gửi lưu ở
      3 nơi khác nhau (nhà, cơ quan, người thân) — mất 1 bản ở 1 nơi không sao, vẫn còn 2 bản ở nơi khác.</p>
      <p>Mỗi block được <b>replicate</b> (nhân bản) thành nhiều bản sao, phân phối trên các DataNode <b>khác
      nhau</b> trong cụm.</p>
      <div class="pd-formula"><div class="pd-formula-label">Hệ số nhân bản mặc định</div>
      <div class="pd-formula-math">3\\text{ bản sao trên 3 DataNode khác nhau}</div></div>
      <table><tr><th>Ngành</th><th>Ví dụ nhân bản để chịu lỗi</th></tr>
      <tr><td>Ngân hàng <i>(minh hoạ)</i></td><td>Dữ liệu giao dịch được sao lưu đồng thời ở trung tâm dữ liệu chính và trung tâm dự phòng ở thành phố khác</td></tr>
      <tr><td>Y tế <i>(minh hoạ)</i></td><td>Hồ sơ bệnh án quan trọng được lưu cả ở bệnh viện điều trị và hệ thống bảo hiểm y tế trung ương</td></tr>
      <tr><td>Hành chính công <i>(minh hoạ)</i></td><td>Giấy chứng nhận quyền sử dụng đất lưu bản gốc ở văn phòng đăng ký đất đai VÀ bản sao ở sở tài nguyên môi trường cấp tỉnh</td></tr></table>
      <div class="callout good"><div class="lbl">Vì sao nhân bản giúp chịu lỗi</div>Khi 1 DataNode hỏng, hệ thống vẫn còn bản sao trên node khác: NameNode tự động điều phối sao chép lại để duy trì đủ số bản sao mặc định.</div>"""),
    dict(h="Rack awareness: không đặt cả 3 bản sao trong cùng 1 \"toà nhà\"", body="""
      <p>🗣️ <b>Nói nôm na:</b> nếu bạn in 3 bản hợp đồng quan trọng nhưng cất cả 3 bản trong CÙNG MỘT
      két sắt, thì két sắt cháy là mất sạch cả 3 — nhân bản chỉ thật sự an toàn khi các bản sao được đặt ở
      những nơi KHÔNG CÙNG gặp rủi ro chung.</p>
      <p>HDFS tổ chức DataNode theo <b>rack</b> (nhóm máy chủ cùng 1 tủ mạng/nguồn điện). Chính sách đặt bản
      sao tiêu chuẩn: 2 bản sao trên 2 node khác nhau trong CÙNG 1 rack (đọc/ghi nhanh vì cùng mạng nội bộ),
      và 1 bản sao trên 1 rack KHÁC (chịu được rủi ro cả rack chết, vd mất điện toàn tủ mạng).</p>
      <table><tr><th>Ngành</th><th>Ví dụ &quot;không để tất cả trong 1 chỗ&quot;</th></tr>
      <tr><td>Logistics <i>(minh hoạ)</i></td><td>Một công ty vận chuyển không để toàn bộ hàng dự phòng trong 1 kho duy nhất — chia ra ít nhất 2 kho ở 2 khu vực khác nhau, tránh 1 kho ngập lụt làm mất toàn bộ</td></tr>
      <tr><td>Tài chính <i>(minh hoạ)</i></td><td>Quỹ đầu tư không dồn hết tiền vào 1 loại tài sản — phân bổ sang nhiều loại để 1 rủi ro không "quét sạch" cả quỹ</td></tr></table>
      <div class="callout info"><div class="lbl">Đánh đổi có chủ đích</div>2 bản trong cùng rack (nhanh, tiết kiệm băng thông mạng giữa rack) + 1 bản rack khác (an toàn hơn khi rủi ro ở mức cả rack) — cân bằng giữa HIỆU NĂNG và AN TOÀN, không chọn tuyệt đối 1 trong 2 hướng.</div>"""),
    dict(h="Phép tính: xác suất mất dữ liệu khi 2 DataNode cùng hỏng đồng thời", body="""
      <p>Ví dụ đơn giản hoá để minh hoạ nguyên lý (không phải công thức xác suất phần cứng thật, chỉ dùng số
      <i>giả định</i> dễ hiểu): giả sử xác suất 1 DataNode cụ thể hỏng trong 1 năm là 2% (0,02), các lần hỏng
      độc lập với nhau, và 1 block có 3 bản sao trên 3 DataNode khác nhau.</p>
      <p><b>Bước 1 — xác suất 1 bản sao cụ thể còn sống sau 1 năm:</b></p>
      <div class="pd-formula"><div class="pd-formula-math">P(\\text{sống}) = 1 - 0{,}02 = 0{,}98</div></div>
      <p><b>Bước 2 — xác suất CẢ 3 bản sao cùng hỏng trong năm đó (mất hẳn block):</b></p>
      <div class="pd-formula"><div class="pd-formula-math">P(\\text{mất cả 3}) = 0{,}02^3 = 0{,}000008 = 0{,}0008\\%</div></div>
      <p><b>Bước 3 — so sánh với trường hợp CHỈ 1 bản sao duy nhất (không nhân bản):</b></p>
      <div class="pd-formula"><div class="pd-formula-math">P(\\text{mất, không nhân bản}) = 0{,}02 = 2\\%</div></div>
      <table><tr><th>Số bản sao</th><th>Xác suất mất dữ liệu trong năm <i>(giả định)</i></th></tr>
      <tr><td>1 (không nhân bản)</td><td>2%</td></tr>
      <tr><td>2</td><td>0,02² = 0,04%</td></tr>
      <tr><td>3 (mặc định HDFS)</td><td>0,02³ = 0,0008%</td></tr></table>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Nếu xác suất hỏng 1 node tăng lên 10%
      (phần cứng cũ, kém tin cậy hơn), xác suất mất dữ liệu với 3 bản sao là bao nhiêu? (Đáp: 0,1³ = 0,001 =
      0,1% — vẫn nhỏ hơn rất nhiều so với 10% nếu không nhân bản, cho thấy nhân bản hiệu quả nhất khi rủi ro
      từng node ĐỘC LẬP với nhau — đây cũng là lý do rack awareness ở slide trước quan trọng: nếu 3 bản sao
      cùng rack, rủi ro KHÔNG còn độc lập khi cả rack mất điện cùng lúc.)</div>""")]),

  # ---------------------------------------------------------------- PHẦN 5
  dict(title="Cơ chế chịu lỗi tự động: heartbeat & tái nhân bản", bullets=[
    "DataNode gửi heartbeat định kỳ cho NameNode",
    "Mất heartbeat → NameNode coi node đã chết → ra lệnh tái nhân bản",
    "Toàn bộ quá trình không cần ứng dụng/người quản trị can thiệp"],
   slides=[
    dict(h="Heartbeat: cách NameNode phát hiện DataNode còn sống", body="""
      <p>🗣️ <b>Nói nôm na:</b> giống hệ thống giám sát y tế từ xa cho người cao tuổi — thiết bị đeo tay gửi
      tín hiệu "tôi vẫn ổn" mỗi vài phút; nếu trung tâm giám sát không nhận được tín hiệu trong 1 khoảng thời
      gian, họ coi đó là dấu hiệu bất thường và cử người tới kiểm tra.</p>
      <p>Mỗi DataNode gửi <b>heartbeat</b> (tín hiệu "tôi vẫn sống") định kỳ cho NameNode. Nếu NameNode không
      nhận được heartbeat từ 1 DataNode trong một khoảng thời gian cấu hình được, nó coi DataNode đó đã chết.</p>
      <table><tr><th>Ngành</th><th>Ví dụ cơ chế heartbeat</th></tr>
      <tr><td>Y tế <i>(minh hoạ)</i></td><td>Thiết bị theo dõi nhịp tim từ xa gửi tín hiệu định kỳ về trung tâm cấp cứu</td></tr>
      <tr><td>Vận tải <i>(minh hoạ)</i></td><td>Xe tải gắn GPS gửi vị trí định kỳ về trung tâm điều phối — mất tín hiệu quá lâu thì điều phối cử người kiểm tra</td></tr>
      <tr><td>An ninh <i>(minh hoạ)</i></td><td>Trạm gác báo cáo định kỳ "khu vực an toàn" về trung tâm chỉ huy</td></tr></table>
      <details><summary><b>📖 Giải thích cho người mới bắt đầu: vì sao không hỏi liên tục ngay lập tức mà phải chờ?</b></summary>
      <p>Nếu NameNode phải chủ động hỏi "còn sống không?" tới TỪNG DataNode mọi lúc, với hàng nghìn DataNode,
      NameNode sẽ bận rộn liên tục chỉ để hỏi thăm, không còn thời gian xử lý yêu cầu thật của client. Thay
      vào đó, để DataNode TỰ CHỦ ĐỘNG gửi tín hiệu về — nhàn hơn cho NameNode, và dễ phát hiện lỗi hơn (nếu 1
      DataNode bị treo hoàn toàn, nó sẽ không gửi được heartbeat, lộ ra ngay).</p></details>"""),
    dict(h="Khi một DataNode hỏng giữa đường", body="""
      <p>Giả sử sau khi ghi xong, <b>DN5</b> (đang giữ 1 bản sao của block B1) gặp lỗi phần cứng.</p>
      <ol><li>DataNode gửi heartbeat định kỳ cho NameNode; khi NameNode không nhận heartbeat từ DN5
      trong một khoảng thời gian, nó coi DN5 đã chết.</li>
      <li>NameNode rà soát metadata: block B1 hiện chỉ còn 2 bản sao hợp lệ (trên DN2, DN7) — thiếu 1 so với
      hệ số nhân bản mặc định 3.</li>
      <li>NameNode ra lệnh cho DN2 (hoặc DN7) sao chép thêm 1 bản của B1 sang một DataNode còn sống khác,
      khôi phục lại đủ 3 bản sao — toàn bộ quá trình này KHÔNG cần ứng dụng phía trên biết hay can thiệp.</li></ol>
      <div class="callout warn"><div class="lbl">Điểm mấu chốt cần nhớ</div>HDFS không "ngăn" lỗi phần cứng
      xảy ra — nó <b>giả định lỗi là bình thường</b> và xây cơ chế tự phục hồi xung quanh giả định đó. Đây
      chính là tư duy "chịu lỗi qua dư thừa" khác hẳn triết lý RDBMS truyền thống (ngăn lỗi bằng phần cứng đắt,
      RAID chuyên dụng).</div>""")]),

  # ---------------------------------------------------------------- PHẦN 6
  dict(title="Secondary NameNode vs Standby NameNode: nhầm lẫn phổ biến nhất của HDFS", bullets=[
    "Secondary NameNode: chỉ gộp fsimage+edit log định kỳ — KHÔNG phải bản dự phòng",
    "Standby NameNode (Hadoop 2.0, HA): thực sự thay thế được NameNode chính khi lỗi",
    "Ví dụ đa ngành để phân biệt rõ 2 khái niệm"],
   slides=[
    dict(h="Vì sao tên gọi \"Secondary\" lại gây hiểu lầm nghiêm trọng", body="""
      <p>🗣️ <b>Nói nôm na:</b> "Secondary NameNode" giống như một NHÂN VIÊN DỌN DẸP SỔ SÁCH — định kỳ gộp
      sổ cái cũ với sổ nháp mới cho GỌN lại, nhưng KHÔNG NGỒI SẴN Ở BÀN LÀM VIỆC để thay thế kế toán trưởng
      ngay khi người đó vắng mặt. "Standby NameNode" mới đúng là một KẾ TOÁN TRƯỞNG DỰ BỊ, luôn cập nhật
      đồng bộ với kế toán trưởng chính, sẵn sàng ngồi vào vị trí ngay khi cần.</p>
      <table><tr><th></th><th>Secondary NameNode (Hadoop 1.0)</th><th>Standby NameNode / HA (Hadoop 2.0+)</th></tr>
      <tr><td>Việc chính</td><td>Định kỳ gộp fsimage + edit log cho gọn (checkpoint)</td><td>Luôn đồng bộ trạng thái mới nhất với NameNode chính</td></tr>
      <tr><td>Khi NameNode chính chết</td><td>KHÔNG thay thế được ngay — phải khởi động lại NameNode từ fsimage cũ, có thể mất dữ liệu gần nhất chưa checkpoint</td><td>Chuyển đổi (failover) sang ngay, gần như không mất dữ liệu</td></tr>
      <tr><td>Giải quyết SPOF?</td><td>Không</td><td>Có — đây chính là lý do Standby NameNode ra đời</td></tr></table>
      <table><tr><th>Ngành</th><th>Tương tự Secondary NameNode</th><th>Tương tự Standby NameNode</th></tr>
      <tr><td>Doanh nghiệp <i>(minh hoạ)</i></td><td>Nhân viên lưu trữ định kỳ sao lưu hồ sơ cuối tháng</td><td>Phó giám đốc luôn nắm mọi quyết định của giám đốc, sẵn sàng thay thế ngay</td></tr>
      <tr><td>Hàng không <i>(minh hoạ)</i></td><td>Nhật ký bay được lưu trữ định kỳ sau mỗi chuyến</td><td>Cơ phó luôn theo sát mọi thao tác của cơ trưởng, có thể điều khiển ngay khi cần</td></tr></table>
      <div class="callout warn"><div class="lbl">Bẫy thi/thực hành phổ biến nhất về HDFS</div>Rất nhiều người
      học (và cả tài liệu không chính xác) nhầm "Secondary NameNode" là "NameNode dự phòng" — chỉ vì tên gọi
      giống nhau. Đây là lỗi hiểu nhầm phổ biến nhất khi học HDFS, cần nhớ kỹ: Secondary ≠ dự phòng.</div>""")]),

  # ---------------------------------------------------------------- PHẦN 7
  dict(title="Write-once, read-many: HDFS khác hệ file thường ở đâu", bullets=[
    "HDFS chỉ hỗ trợ ghi thêm vào cuối tệp (append), không sửa giữa tệp",
    "Tối ưu cho đọc tuần tự khối lượng lớn, không phải truy cập ngẫu nhiên nhanh",
    "Ví dụ đa ngành: hồ sơ y tế chỉ thêm trang mới, sổ kế toán không tẩy xoá"],
   slides=[
    dict(h="Mục tiêu thiết kế của HDFS", body="""
      <p>🗣️ <b>Nói nôm na:</b> giống quyển SỔ NHẬT KÝ chỉ được viết thêm trang mới ở cuối, không được xé
      hay viết chèn vào giữa các trang cũ — mọi thứ đã viết ra là cố định, chỉ có thể nối thêm.</p>
      <p>HDFS tối ưu cho các tệp <b>kích thước lớn</b> (hàng trăm MB đến TB), mô hình truy cập
      <b>write-once, read-many</b> (ghi một lần, đọc nhiều lần). Khác biệt so với hệ thống tập tin UNIX
      thông thường: chỉ hỗ trợ thao tác ghi thêm dữ liệu vào cuối tệp (APPEND), không hỗ trợ sửa/ghi đè vào
      giữa tệp.</p>
      <table><tr><th>Ngành</th><th>Ví dụ &quot;chỉ thêm, không sửa giữa&quot;</th></tr>
      <tr><td>Y tế <i>(minh hoạ)</i></td><td>Hồ sơ bệnh án: mỗi lần khám chỉ THÊM 1 trang mới, không tẩy xoá/sửa trang khám cũ — đảm bảo truy vết lịch sử điều trị trung thực</td></tr>
      <tr><td>Kế toán <i>(minh hoạ)</i></td><td>Sổ kế toán theo nguyên tắc không tẩy xoá — sai thì ghi thêm 1 dòng điều chỉnh, không sửa dòng cũ</td></tr>
      <tr><td>Pháp lý <i>(minh hoạ)</i></td><td>Biên bản cuộc họp đã ký không được sửa lại — muốn đính chính phải thêm 1 phụ lục mới</td></tr></table>
      <div class="callout warn"><div class="lbl">Đánh đổi có chủ đích</div>Thiết kế để đạt <b>thông lượng
      cao</b> thay vì <b>độ trễ thấp</b>: phù hợp xử lý batch (đọc toàn bộ tệp lớn 1 lần) hơn truy vấn tương
      tác thời gian thực (sửa 1 dòng, đọc 1 bản ghi ngẫu nhiên — đây là lý do HBase, không phải HDFS trực
      tiếp, được dùng cho truy cập ngẫu nhiên tốc độ cao, xem module <code>hd-04</code>).</div>""")]),

  # ---------------------------------------------------------------- PHẦN 8 (giữ + mở rộng ví dụ gốc)
  dict(title="Ví dụ minh hoạ: ghi một tệp 300MB vào HDFS", bullets=[
    "Tệp 300MB với block 128MB → 3 block (128+128+44)",
    "Mỗi block có 3 bản sao → tổng 9 lượt ghi vật lý trên các DataNode",
    "Thử lại với hệ số nhân bản khác — tổng chi phí lưu trữ thay đổi ra sao"],
   slides=[
    dict(h="Từng bước: client ghi 1 tệp 300MB", body="""
      <p>Giả sử client ghi tệp <code>bao_cao.csv</code> dung lượng 300MB vào HDFS với block size 128MB,
      hệ số nhân bản 3:</p>
      <table><tr><th>Bước</th><th>Diễn ra gì</th></tr>
      <tr><td>1</td><td>Client hỏi NameNode: "tôi muốn ghi tệp này" → NameNode chia tệp thành 3 block:
      B1 (128MB), B2 (128MB), B3 (44MB)</td></tr>
      <tr><td>2</td><td>NameNode trả về danh sách DataNode cho từng block (vd B1 → DN2, DN5, DN7)</td></tr>
      <tr><td>3</td><td>Client ghi trực tiếp tới DataNode đầu tiên của mỗi block; DataNode đó tự chuyển tiếp
      (pipeline) bản sao sang 2 DataNode còn lại</td></tr>
      <tr><td>4</td><td>Khi đủ 3×3 = 9 bản ghi vật lý hoàn tất, NameNode cập nhật metadata, xác nhận ghi
      thành công</td></tr></table>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Nếu hệ số nhân bản đổi thành 2 thay vì 3,
      tổng số lượt ghi vật lý cho tệp này sẽ là bao nhiêu? (Đáp: 3 block × 2 bản sao = 6 lượt ghi — ít tốn
      dung lượng hơn nhưng khả năng chịu lỗi giảm, chỉ chịu được 1 DataNode hỏng thay vì tối đa 2.)</div>"""),
    dict(h="Chi phí lưu trữ thật: dung lượng vật lý cần, với các hệ số nhân bản khác nhau", body="""
      <p>Tệp 300MB "hữu ích" nhưng chiếm dung lượng vật lý GẤP hệ số nhân bản lần. Đây là phép tính chi phí
      thực tế mà kỹ sư hạ tầng phải cân nhắc khi lập kế hoạch dung lượng cụm.</p>
      <table><tr><th>Hệ số nhân bản</th><th>Dung lượng vật lý cần cho tệp 300MB</th><th>Chịu được tối đa bao nhiêu DataNode hỏng ĐỒNG THỜI mà không mất block?</th></tr>
      <tr><td>1 (không nhân bản)</td><td>300MB</td><td>0</td></tr>
      <tr><td>2</td><td>600MB</td><td>1</td></tr>
      <tr><td>3 (mặc định)</td><td>900MB</td><td>2</td></tr></table>
      <div class="callout info"><div class="lbl">Đánh đổi thật trong vận hành</div>Với 10.000 tệp tương tự
      (300MB/tệp), hệ số nhân bản 3 cần ~2,93TB vật lý cho 2,93TB dữ liệu "hữu ích" × 3 — đây là lý do các tổ
      chức lớn đôi khi giảm hệ số nhân bản xuống 2 cho dữ liệu ít quan trọng (log tạm) để tiết kiệm chi phí,
      và GIỮ 3 (hoặc cao hơn) cho dữ liệu quan trọng — hệ số nhân bản có thể đặt RIÊNG cho từng tệp/thư mục,
      không bắt buộc đồng nhất toàn cụm.</div>""")]),

  # ---------------------------------------------------------------- PHẦN 9
  dict(title="Khi một DataNode hỏng giữa đường: toàn cảnh tái nhân bản", bullets=[
    "NameNode phát hiện qua mất heartbeat", "Rà soát metadata tìm block thiếu bản sao",
    "Ra lệnh tái nhân bản tự động, không cần can thiệp của con người"],
   slides=[
    dict(h="Toàn cảnh: từ lúc hỏng tới lúc phục hồi hoàn chỉnh", body="""
      <p>Ghép lại toàn bộ chuỗi sự kiện khi 1 DataNode hỏng (tổng hợp từ các khái niệm đã học ở Phần 2, 5):</p>
      <ol><li><b>Phát hiện (Phần 5):</b> NameNode không nhận heartbeat từ DataNode trong khoảng thời gian cấu
      hình → coi node đã chết.</li>
      <li><b>Chẩn đoán (Phần 2):</b> NameNode dò metadata (ánh xạ block → DataNode) để tìm TẤT CẢ block có
      bản sao nằm trên node vừa chết.</li>
      <li><b>Khôi phục (Phần 4):</b> với mỗi block thiếu bản sao, NameNode chọn 1 DataNode còn sống (ưu tiên
      theo rack awareness) để nhận thêm 1 bản sao mới, khôi phục đủ hệ số nhân bản mặc định.</li>
      <li><b>Hoàn tất:</b> metadata được cập nhật; nếu client đang đọc/ghi đúng lúc này, hệ thống tự động
      chuyển hướng sang bản sao còn sống khác — ứng dụng phía trên hầu như không nhận ra sự cố.</li></ol>
      <div class="callout warn"><div class="lbl">Điểm mấu chốt cần nhớ</div>HDFS không "ngăn" lỗi phần cứng
      xảy ra — nó <b>giả định lỗi là bình thường</b> và xây cơ chế tự phục hồi xung quanh giả định đó. Đây
      chính là tư duy "chịu lỗi qua dư thừa" khác hẳn triết lý RDBMS truyền thống (ngăn lỗi bằng phần cứng đắt,
      RAID chuyên dụng).</div>""")]),

  # ---------------------------------------------------------------- PHẦN 10
  dict(title="Ảnh hưởng của Hadoop/HDFS tới thế giới", bullets=[
    "2008: Hadoop trở thành dự án Apache cấp cao nhất (top-level project)",
    "Khai sinh 2 công ty thương mại lớn: Cloudera (2008), Hortonworks (2011)",
    "Đặt nền tảng cho toàn bộ ngành công nghiệp 'Big Data' và sau này là data lake/lakehouse trên cloud"],
   slides=[
    dict(h="Từ một dự án nội bộ Yahoo tới chuẩn công nghiệp", body="""
      <p>Yahoo! là công ty đầu tiên triển khai Hadoop ở quy mô sản xuất lớn (phục vụ đánh chỉ mục tìm kiếm),
      và là nơi nuôi dưỡng dự án trong giai đoạn đầu then chốt (2006 trở đi). Hadoop trở thành dự án Apache
      cấp cao nhất năm 2008.</p>
      <div class="callout good"><div class="lbl">🌍 Ảnh hưởng tới thế giới</div>
      Hadoop là nền tảng mở đầu cho tư duy "lưu trữ rẻ, mở rộng ngang, chấp nhận lỗi phần cứng" — tư duy này
      sau đó định hình toàn bộ kiến trúc <b>data lake</b> trên cloud (AWS S3 + EMR, Azure Data Lake, GCS +
      Dataproc): thay HDFS bằng object storage, nhưng triết lý "scale-out, lưu trước xử lý sau" vẫn giữ
      nguyên tới ngày nay trong các nền tảng data lakehouse (Delta Lake, Iceberg, Hudi).</div>
      <p>Hai công ty thương mại lớn nhất của hệ sinh thái Hadoop — <b>Cloudera</b> (2008) và
      <b>Hortonworks</b> (2011, sau sáp nhập lại với Cloudera năm 2019) — ra đời trực tiếp từ nhu cầu đóng gói,
      hỗ trợ doanh nghiệp triển khai Hadoop, cho thấy quy mô ảnh hưởng kinh tế thực sự của công nghệ này.</p>
      <table><tr><th>Lĩnh vực ngày nay</th><th>Di sản trực tiếp từ HDFS</th></tr>
      <tr><td>Data lake trên cloud (S3, GCS, ADLS)</td><td>Triết lý lưu trữ rẻ, mở rộng ngang, tách khỏi engine xử lý</td></tr>
      <tr><td>Data lakehouse (Delta Lake, Iceberg, Hudi)</td><td>Giữ nguyên "lưu trước, xử lý sau" nhưng thêm transaction/schema evolution mà HDFS gốc không có</td></tr>
      <tr><td>Hệ thống NoSQL/wide-column (HBase, Cassandra)</td><td>Kế thừa trực tiếp triết lý chịu lỗi qua nhân bản của HDFS (xem module <code>hd-04</code>)</td></tr></table>""")])
 ],
 quiz=[
  dict(q="Hadoop ra đời trực tiếp từ dự án nào, và vì vấn đề gì?", opts=[
     "Dự án Nutch (công cụ tìm kiếm), vì Nutch không mở rộng được khi dữ liệu lớn",
     "Dự án nghiên cứu học thuật thuần túy, không liên quan sản phẩm thật",
     "Một hackathon nội bộ Google", "Một yêu cầu trực tiếp từ khách hàng của Yahoo"],
   correct=0, explain="Nutch (2002, Cutting & Cafarella) là công cụ tìm kiếm mở gặp giới hạn mở rộng, dẫn tới việc tách phần lưu trữ/xử lý ra thành Hadoop sau khi đọc 2 bài báo GFS/MapReduce của Google."),
  dict(q="Hadoop được đặt tên theo điều gì?", opts=[
     "Viết tắt của 'Hadoop Distributed Architecture for Online Processing'",
     "Tên một thuật toán nén dữ liệu", "Tên con voi nhồi bông của con trai Doug Cutting", "Tên công ty sáng lập"],
   correct=2, explain="Không có ý nghĩa kỹ thuật gì — Cutting chọn vì ngắn, dễ phát âm, chưa ai dùng."),
  dict(q="Google có cho Hadoop dùng chung mã nguồn GFS/MapReduce không?", opts=[
     "Có, Hadoop sao chép trực tiếp mã nguồn Google", "Không — Google chỉ công bố Ý TƯỞNG qua paper, Hadoop là bản triển khai lại độc lập",
     "Có, nhưng chỉ phần MapReduce", "Không liên quan gì tới Google"],
   correct=1, explain="Google công bố ý tưởng qua 2 paper khoa học (GFS, MapReduce); Cutting/Cafarella viết lại hoàn toàn mới dựa trên ý tưởng đó."),
  dict(q="Trong kiến trúc HDFS, NameNode chịu trách nhiệm chính về điều gì?", opts=[
     "Lưu toàn bộ dữ liệu thật của mọi tệp", "Lưu metadata: namespace, ánh xạ tệp → block → DataNode",
     "Chạy các tác vụ MapReduce", "Nhân bản vật lý từng block"],
   correct=1, explain="NameNode chỉ giữ metadata (fsimage + edit log); dữ liệu thật và việc nhân bản do DataNode xử lý."),
  dict(q="fsimage và edit log phối hợp ra sao khi NameNode khởi động lại?", opts=[
     "Chỉ cần đọc fsimage, bỏ qua edit log", "Đọc fsimage gần nhất rồi PHÁT LẠI edit log để tái tạo trạng thái mới nhất",
     "Chỉ cần đọc edit log từ đầu, bỏ qua fsimage", "NameNode không lưu trạng thái, luôn khởi động từ trống"],
   correct=1, explain="fsimage là ảnh chụp, edit log là các thay đổi từ sau đó — kết hợp cả 2 mới ra trạng thái đầy đủ."),
  dict(q="Vì sao Hadoop 1.0 coi NameNode là một Single Point of Failure?", opts=[
     "Vì NameNode chạy chậm hơn DataNode", "Vì mọi metadata chỉ tồn tại ở 1 NameNode, hỏng là mất khả năng định vị dữ liệu",
     "Vì NameNode không hỗ trợ nhân bản", "Vì NameNode cần GPU"],
   correct=1, explain="Dữ liệu vật lý trên DataNode vẫn còn, nhưng không ai biết nó ở đâu nếu NameNode (và metadata) hỏng — đây là động lực ra đời Standby NameNode (HA) ở Hadoop 2.0."),
  dict(q="Secondary NameNode và Standby NameNode khác nhau cốt lõi ở điểm nào?", opts=[
     "Chúng là một, chỉ đổi tên", "Secondary NameNode chỉ gộp fsimage+edit log định kỳ, KHÔNG thay thế được NameNode chính khi lỗi; Standby NameNode (HA) mới thực sự failover được",
     "Secondary NameNode nhanh hơn Standby NameNode", "Standby NameNode chỉ dùng để lưu dữ liệu, không liên quan metadata"],
   correct=1, explain="Đây là nhầm lẫn phổ biến nhất về HDFS: cái tên 'Secondary' gây hiểu lầm là 'dự phòng', nhưng nó chỉ làm việc checkpoint/gộp log."),
  dict(q="Block size lớn (64MB/128MB) trong HDFS giúp giải quyết vấn đề gì?", opts=[
     "Tăng độ trễ đọc/ghi", "Giảm số lượng entry metadata mà NameNode phải lưu trong RAM",
     "Giảm hệ số nhân bản cần thiết", "Tăng số lượng tệp nhỏ có thể lưu hiệu quả"],
   correct=1, explain="Block lớn → ít block hơn cho cùng dung lượng dữ liệu → ít metadata hơn trên NameNode. Hệ quả phụ: HDFS KÉM hiệu quả với rất nhiều tệp nhỏ (small-files problem)."),
  dict(q="'Small-files problem' của HDFS là gì?", opts=[
     "HDFS không lưu được tệp nhỏ hơn 1MB", "Rất nhiều tệp nhỏ làm phình số entry metadata trên NameNode, dù tổng dung lượng dữ liệu nhỏ",
     "Tệp nhỏ bị tự động xoá sau 1 thời gian", "Tệp nhỏ luôn bị lỗi khi đọc"],
   correct=1, explain="Mỗi tệp (dù nhỏ) vẫn cần ít nhất 1 entry metadata — hàng triệu tệp nhỏ có thể làm ngập RAM NameNode."),
  dict(q="Một tệp 300MB với block size 128MB được chia thành mấy block?", opts=["2 block", "3 block (128+128+44)", "4 block", "300 block"],
   correct=1, explain="⌈300/128⌉ = 3 block: hai block đầy 128MB, block cuối 44MB."),
  dict(q="Với tệp 300MB chia 3 block, hệ số nhân bản 3, tổng số lượt ghi vật lý trên các DataNode là bao nhiêu?", opts=["3", "6", "9", "12"],
   correct=2, explain="3 block × 3 bản sao/block = 9 lượt ghi vật lý."),
  dict(q="Với hệ số nhân bản 2 thay vì 3 cho cùng tệp 300MB (3 block), tổng lượt ghi vật lý là bao nhiêu?", opts=["3", "6", "9", "12"],
   correct=1, explain="3 block × 2 bản sao = 6 lượt ghi — ít tốn dung lượng hơn nhưng chỉ chịu được 1 DataNode hỏng, không phải 2."),
  dict(q="Nếu xác suất 1 DataNode hỏng trong năm là 2% (độc lập), xác suất mất HẲN 1 block có 3 bản sao là bao nhiêu (giả định đơn giản)?", opts=["2%", "0,04%", "0,0008%", "6%"],
   correct=2, explain="0,02³ = 0,000008 = 0,0008% — xác suất CẢ 3 bản sao cùng hỏng, nhỏ hơn rất nhiều so với 1 bản sao duy nhất (2%)."),
  dict(q="Rack awareness trong HDFS giải quyết vấn đề gì mà nhân bản đơn thuần (không quan tâm vị trí) không giải quyết được?", opts=[
     "Tăng tốc độ ghi dữ liệu duy nhất", "Tránh đặt tất cả bản sao trong cùng 1 rack — để rủi ro mất cả rack (vd mất điện) không làm mất luôn cả block",
     "Giảm hệ số nhân bản cần thiết", "Không liên quan tới chịu lỗi"],
   correct=1, explain="Nếu 3 bản sao cùng rack, rủi ro không còn độc lập — cả rack mất điện là mất cả 3 bản. Chính sách tiêu chuẩn: 2 bản cùng rack (nhanh) + 1 bản rack khác (an toàn hơn)."),
  dict(q="DataNode thông báo 'còn sống' cho NameNode bằng cơ chế gì?", opts=[
     "NameNode chủ động gọi hỏi liên tục từng DataNode", "DataNode tự động gửi heartbeat định kỳ cho NameNode",
     "Qua email tự động", "Không có cơ chế nào, chỉ phát hiện khi client báo lỗi"],
   correct=1, explain="Heartbeat định kỳ từ DataNode giúp NameNode phát hiện lỗi mà không cần tốn tài nguyên hỏi liên tục từng node."),
  dict(q="Khi một DataNode giữ bản sao của 1 block bị lỗi, hệ thống phản ứng ra sao?", opts=[
     "Toàn bộ tệp bị xoá để đảm bảo nhất quán", "NameNode phát hiện qua heartbeat và ra lệnh tái nhân bản sang DataNode khác",
     "Client phải tự ghi lại toàn bộ tệp", "Không có cơ chế tự động, cần quản trị viên can thiệp thủ công"],
   correct=1, explain="Cơ chế heartbeat + tái nhân bản tự động là nền tảng của khả năng chịu lỗi HDFS, không cần ứng dụng hay người quản trị can thiệp."),
  dict(q="HDFS theo mô hình truy cập nào, khác gì so với hệ file UNIX thông thường?", opts=[
     "Đọc-ghi tự do như hệ file thường", "Write-once, read-many — chỉ hỗ trợ ghi thêm (append) vào cuối tệp, không sửa giữa tệp",
     "Chỉ đọc, không ghi được bao giờ", "Chỉ ghi, không đọc lại được"],
   correct=1, explain="Khác hệ file UNIX thường (có thể sửa bất kỳ vị trí), HDFS chỉ hỗ trợ append — phù hợp xử lý batch hơn giao dịch ngẫu nhiên."),
  dict(q="Hadoop trở thành dự án Apache cấp cao nhất (top-level project) vào năm nào?", opts=["2004", "2006", "2008", "2012"],
   correct=2, explain="2006 là năm Hadoop tách thành dự án con từ Nutch; 2008 mới là năm trở thành top-level Apache project."),
  dict(q="Hai công ty thương mại lớn nhất xây quanh hệ sinh thái Hadoop là gì?", opts=[
     "Confluent và Databricks", "Cloudera và Hortonworks", "MongoDB Inc. và Snowflake", "Oracle và IBM"],
   correct=1, explain="Cloudera (2008) và Hortonworks (2011) — hai công ty này sau sáp nhập lại năm 2019."),
  dict(q="Triết lý 'scale-out, lưu trước xử lý sau' của Hadoop ảnh hưởng trực tiếp tới kiến trúc nào phổ biến hiện nay?", opts=[
     "Máy chủ mainframe tập trung", "Data lake/lakehouse trên cloud (S3+EMR, Delta Lake, Iceberg)",
     "Cơ sở dữ liệu quan hệ truyền thống on-premise duy nhất", "Không có ảnh hưởng gì tới kiến trúc hiện đại"],
   correct=1, explain="HDFS được thay bằng object storage (S3/GCS/ADLS) nhưng tư duy lưu trữ rẻ + mở rộng ngang vẫn là nền tảng của data lake/lakehouse ngày nay."),
 ])
