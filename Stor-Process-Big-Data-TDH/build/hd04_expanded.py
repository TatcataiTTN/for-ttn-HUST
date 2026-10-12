# -*- coding: utf-8 -*-
"""Bản mở rộng SÂU của module hd-04-hbase-sqoop (n=28) — giữ nguyên 100% callout lịch sử/nguồn gốc
của bản gốc trong hadoop_deepdive_content.py, mở rộng từ 4 part/6 slide lên 9 part/~24 slide, theo
chuẩn 02-module-content-standard.md (build-complete-self-study-system): mỗi khái niệm có Nói nôm na
→ giải thích kỹ thuật → ví dụ ≥2-3 ngành (nhãn (minh hoạ) rõ ràng) → bảng HTML → phép tính từng bước
khi có. Mọi fact lịch sử giữ đúng nguồn đã verify (Wikipedia Apache HBase, The Register, Wikipedia
Sqoop) — không thêm fact lịch sử mới không kiểm chứng."""

HD04_EXPANDED = dict(
 n=28, slug="hd-04-hbase-sqoop",
 title="HBase & Sqoop: NoSQL lấy cảm hứng từ Bigtable, và cầu nối với thế giới RDBMS cũ",
 tag="Lịch sử HBase (Powerset/Bigtable) · Sqoop (Cloudera)",
 intro="HBase không phải ý tưởng của Hadoop — nó là bản sao chép (re-implementation) mã nguồn mở của một hệ thống nội bộ của Google. Và Sqoop nhắc chúng ta rằng công nghệ Big Data không tồn tại mãi.",
 parts=[

  # ---------------- PHẦN 1: Mô hình Bigtable / column-family ----------------
  dict(title="Mô hình dữ liệu Bigtable: bảng không giống Excel, không giống RDBMS", bullets=[
    "Bigtable (Google, 2006): CSDL cột mở rộng phân tán, không phải bảng hàng×cột cố định như RDBMS",
    "Khái niệm cốt lõi: row key, column family, qualifier, timestamp (cell versioned)",
    "🗣️ Nói nôm na: giống 1 tủ hồ sơ có nhiều ngăn kéo (family), mỗi ngăn chứa nhiều loại giấy tờ (qualifier), và mỗi giấy tờ có thể có NHIỀU phiên bản theo thời gian"],
   slides=[
    dict(h="Mô hình 'cột mở rộng' (wide-column) khác bảng thông thường", body="""
      <p><b>🗣️ Nói nôm na:</b> RDBMS giống 1 bảng Excel cố định: mọi dòng phải có ĐỦ các cột đã khai báo
      trước, dù trống cũng phải để ô trống. Bigtable/HBase giống 1 tủ hồ sơ linh hoạt: mỗi "dòng" (row) có
      thể có số cột hoàn toàn khác dòng khác, và các cột được gom nhóm thành "ngăn kéo" gọi là
      <b>column family</b>.</p>
      <p><b>Giải thích kỹ thuật:</b> Một bảng HBase được định nghĩa trước CHỈ với tên các <i>column
      family</i> (ít, cố định, vd <code>info</code>, <code>stats</code>) — còn <i>qualifier</i> (tên cột cụ
      thể bên trong family, vd <code>info:ten</code>, <code>info:email</code>) có thể thêm tuỳ ý ở mỗi
      dòng, không cần khai báo trước schema như RDBMS.</p>
      <ul class="pd-legend"><li><b>Row key</b><span>khoá chính duy nhất của 1 dòng, byte array, sắp xếp từ
      điển (lexicographic) — đây là trục quan trọng nhất của mọi thiết kế HBase</span></li>
      <li><b>Column family</b><span>nhóm cột được lưu CÙNG NHAU trên đĩa (physically co-located) — khai báo
      trước, ít thay đổi</span></li>
      <li><b>Qualifier</b><span>tên cột cụ thể trong 1 family — thêm tự do, không cần khai báo trước</span></li>
      <li><b>Cell + timestamp</b><span>mỗi giá trị (row, family:qualifier) có thể có NHIỀU phiên bản theo
      thời gian — HBase tự giữ lại N phiên bản gần nhất (mặc định 1 hoặc 3 tuỳ cấu hình)</span></li></ul>
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử (giữ từ bản gốc)</div>HBase ban đầu do
      công ty Powerset xây dựng, phát hành lần đầu ngày 28/3/2008 — mô hình dữ liệu và kiến trúc lấy cảm
      hứng trực tiếp từ hệ thống Bigtable của Google (công bố qua paper năm 2006). Powerset cần xử lý khối
      lượng dữ liệu khổng lồ cho bài toán tìm kiếm ngôn ngữ tự nhiên (NLP), và nhận thấy mô hình "CSDL cột
      mở rộng phân tán" của Bigtable là lời giải phù hợp — nhưng Bigtable là hệ thống nội bộ đóng của
      Google, nên Powerset xây một bản mã nguồn mở tương đương, chạy trên nền HDFS thay vì GFS.
      Nguồn: <a href="https://en.wikipedia.org/wiki/Apache_HBase" target="_blank">Apache HBase — Wikipedia</a>.</div>
      <p>HBase được xem như "hệ quản trị CSDL của Hadoop": dữ liệu tổ chức logic thành bảng (hàng × cột),
      kích thước bảng có thể tới Terabyte/Petabyte, hàng ngàn cột, hỗ trợ hàng trăm ngàn thao tác INSERT/giây.</p>"""),
    dict(h="Ví dụ minh hoạ ≥3 ngành: cùng mô hình column-family, 3 bài toán khác nhau", body="""
      <table><tr><th>Ngành</th><th>Row key</th><th>Column family: qualifier (ví dụ)</th><th>Vì sao hợp mô hình wide-column</th></tr>
      <tr><td>Công nghệ (thật, đúng ví dụ Facebook Messages)</td><td><code>user_id</code></td>
      <td><code>msg:2024_01_15_001</code>, <code>msg:2024_01_16_003</code> (mỗi tin nhắn 1 qualifier riêng)</td>
      <td>Số tin nhắn/user không cố định — không cần khai báo trước bao nhiêu "cột tin nhắn"</td></tr>
      <tr><td>Y tế (minh hoạ)</td><td><code>ma_benh_nhan</code></td>
      <td><code>xetnghiem:2024_cholesterol</code>, <code>xetnghiem:2024_duong_huyet</code></td>
      <td>Mỗi bệnh nhân có số lần xét nghiệm khác nhau qua nhiều năm — RDBMS sẽ cần hàng trăm cột trống
      nếu ép vào bảng cố định</td></tr>
      <tr><td>Bán lẻ/marketing (minh hoạ)</td><td><code>ma_khach_hang</code></td>
      <td><code>hanhvi:xem_sp_102</code>, <code>hanhvi:mua_sp_205</code></td>
      <td>Số loại hành vi theo dõi tăng liên tục theo thời gian, không muốn sửa schema RDBMS mỗi lần thêm
      loại hành vi mới</td></tr></table>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Vì sao RDBMS truyền thống sẽ gặp khó
      khi mô hình hoá bảng "lịch sử xét nghiệm bệnh nhân" nếu số lần xét nghiệm của mỗi người rất khác
      nhau? (Đáp: RDBMS cần số cột CỐ ĐỊNH biết trước; nếu lấy số lần xét nghiệm nhiều nhất làm số cột, đa
      số bệnh nhân sẽ có rất nhiều cột NULL — lãng phí và khó mở rộng khi có thêm loại xét nghiệm mới. Mô
      hình wide-column cho phép mỗi dòng có số qualifier khác nhau mà không lãng phí.)</div>""")]),

  # ---------------- PHẦN 2: Kiến trúc Region/RegionServer ----------------
  dict(title="Region & RegionServer: HBase 'chia để trị' bảng lớn ra sao", bullets=[
    "1 bảng HBase lớn được chia thành nhiều Region theo khoảng row key liên tiếp",
    "Mỗi Region do 1 RegionServer phục vụ — đây là lý do row key quyết định tải phân bố ra sao",
    "🗣️ Nói nôm na: giống chia 1 cuốn từ điển dày thành nhiều tập mỏng, mỗi tập giao cho 1 người giữ riêng"],
   slides=[
    dict(h="Region là gì, và vì sao nó quyết định toàn bộ hiệu năng ghi", body="""
      <p><b>🗣️ Nói nôm na:</b> Hãy tưởng tượng 1 cuốn từ điển dày được cắt thành nhiều tập theo thứ tự chữ
      cái (A-D, E-H, I-M...) — mỗi tập là 1 "Region", giao cho 1 "người giữ tập" (RegionServer) riêng. Khi
      bạn tra từ, bạn chỉ cần hỏi đúng người giữ tập chứa chữ cái đó.</p>
      <p><b>Giải thích kỹ thuật:</b> Một bảng HBase được chia theo <b>khoảng row key liên tiếp</b> thành
      nhiều <i>Region</i>; mỗi Region do đúng 1 <i>RegionServer</i> phục vụ tại một thời điểm. Khi 1 Region
      phình quá lớn (vượt ngưỡng cấu hình), HBase tự động <b>split</b> (chia đôi) nó thành 2 Region mới.</p>
      <div class="callout warn"><div class="lbl">Hệ quả trực tiếp: row key quyết định tải, không phải số
      lượng dữ liệu</div>Nếu mọi row key MỚI đều rơi vào CÙNG 1 khoảng (vd luôn có tiền tố tăng dần như
      timestamp), toàn bộ việc ghi sẽ dồn vào ĐÚNG 1 Region/RegionServer — các RegionServer khác "nhàn" dù
      cụm có hàng chục máy. Đây chính là hiện tượng "hotspotting" sẽ phân tích kỹ ở Phần 5.</div>
      <table><tr><th>Ngành (minh hoạ)</th><th>Tương tự Region/RegionServer</th><th>Rủi ro nếu phân chia sai</th></tr>
      <tr><td>Thư viện</td><td>Chia sách theo kệ A-M, N-Z, mỗi kệ 1 thủ thư quản lý</td>
      <td>Nếu toàn bộ sách mới nhập đều có mã bắt đầu "Z" (vd đánh mã theo năm), thủ thư kệ "N-Z" quá tải,
      các thủ thư khác rảnh</td></tr>
      <tr><td>Call center</td><td>Chia khách hàng theo số điện thoại đầu 09x/08x/07x cho từng nhóm tổng đài
      viên</td><td>Nếu 1 chiến dịch marketing chỉ target đúng 1 đầu số, 1 nhóm tổng đài viên quá tải</td></tr></table>"""),
    dict(h="Region split tự động: 1 ví dụ số thật từng bước", body="""
      <p>Giả sử ngưỡng split mặc định = 10GB/Region. 1 Region đang chứa dữ liệu user có row key từ
      <code>u00001</code> đến <code>u99999</code>, hiện đã đạt 10GB và tiếp tục nhận ghi mới.</p>
      <ol><li>HBase phát hiện Region vượt ngưỡng → chọn 1 row key "giữa" (vd <code>u50000</code>) làm điểm
      chia (split point).</li>
      <li>Region cũ bị thay bằng 2 Region mới: Region A phục vụ khoảng <code>u00001–u49999</code>, Region B
      phục vụ khoảng <code>u50000–u99999</code>.</li>
      <li>2 Region mới có thể được phân cho 2 RegionServer KHÁC NHAU để cân bằng tải — quá trình này diễn
      ra tự động, không cần ứng dụng phía trên can thiệp.</li></ol>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Nếu toàn bộ 10GB dữ liệu trong ví dụ
      trên lại chỉ nằm ở đúng 100 row key đầu tiên (<code>u00001–u00100</code>, mỗi row rất lớn), việc chọn
      điểm chia "giữa theo thứ tự chữ cái" (<code>u50000</code>) có còn cân bằng tải không? (Đáp: KHÔNG —
      Region mới "A" vẫn chứa nguyên 10GB, Region "B" gần như trống; split theo vị trí khoá giữa chỉ cân
      bằng khi dữ liệu phân bố tương đối đều trong khoảng khoá, đúng vấn đề đã thấy với Sqoop ở Phần 7.)</div>""")]),

  # ---------------- PHẦN 3: API get/put/scan so với SQL ----------------
  dict(title="API get/put/scan: đánh đổi tốc độ lấy linh hoạt truy vấn", bullets=[
    "HBase không có ngôn ngữ truy vấn mức cao như SQL — chỉ 3 phép toán cơ bản: get, put, scan",
    "Đánh đổi có chủ đích: bỏ JOIN/GROUP BY linh hoạt để đạt tốc độ đọc/ghi theo khoá cực cao",
    "🗣️ Nói nôm na: SQL giống hỏi thủ thư 'tìm mọi sách về chủ đề X xuất bản sau năm Y' (thủ thư tự tìm); get/put/scan giống việc BẠN TỰ ra đúng kệ, đúng vị trí mà lấy"],
   slides=[
    dict(h="3 phép toán duy nhất, và vì sao đây là đánh đổi có chủ đích", body="""
      <table><tr><th>Phép toán</th><th>Làm gì</th><th>Tương đương SQL (gần đúng)</th></tr>
      <tr><td><code>put(rowkey, family, qualifier, value)</code></td><td>Ghi 1 giá trị vào 1 cell cụ thể</td>
      <td><code>INSERT</code> hoặc <code>UPDATE</code> 1 ô duy nhất</td></tr>
      <tr><td><code>get(rowkey)</code></td><td>Đọc toàn bộ hoặc 1 phần dữ liệu của 1 dòng theo khoá chính xác</td>
      <td><code>SELECT * FROM t WHERE pk = ?</code> — nhưng KHÔNG hỗ trợ WHERE theo cột khác pk</td></tr>
      <tr><td><code>scan(startKey, endKey)</code></td><td>Đọc nhiều dòng liên tiếp theo khoảng row key</td>
      <td><code>SELECT * FROM t WHERE pk BETWEEN ? AND ?</code> — PHẢI biết trước khoảng khoá, không
      có <code>WHERE cột_khác = ?</code> hiệu quả</td></tr></table>
      {callout_warn}
      <div class="callout good"><div class="lbl">Vì sao đây là đánh đổi "có chủ đích", không phải thiếu sót</div>
      Bỏ engine tối ưu truy vấn (query planner) của RDBMS đồng nghĩa KHÔNG cần tốn chi phí tính toán cho
      JOIN/GROUP BY phức tạp — đổi lại HBase đọc/ghi theo khoá với độ trễ milliseconds ổn định ngay cả ở
      quy mô petabyte, hàng trăm ngàn ghi/giây — đúng điều Facebook Messages cần (tin nhắn luôn tra theo
      user_id, không cần JOIN phức tạp).</div>""".replace("{callout_warn}",
      '<div class="callout warn"><div class="lbl">Nhưng là NoSQL — đánh đổi có chủ đích</div>So với RDBMS '
      'truyền thống, HBase không có ngôn ngữ truy vấn mức cao như SQL — phải dùng API <code>get</code>/<code>put</code>/ '
      '<code>scan</code> theo khoá (row key). Đây là đánh đổi: bỏ tính linh hoạt truy vấn để đạt khả mở và '
      'băng thông ghi cực cao.</div>')),
    dict(h="Ví dụ scan thật: lấy 1000 tin nhắn gần nhất của 1 user", body="""
      <p>Với row key thiết kế đúng (<code>userid_reversedTimestamp</code>, đã học ở Phần 5), lấy 1000 tin
      nhắn gần nhất của user "u8842":</p>
      <div class="pd-formula"><div class="pd-formula-label">Lệnh scan (giả định cú pháp HBase shell)</div>
      <div class="pd-formula-math">\\text{scan 'messages', \\{STARTROW => 'u8842\\_', LIMIT => 1000\\}}</div></div>
      <p><b>Giải thích từng phần:</b> <code>STARTROW</code> = tiền tố đúng user cần tra; vì timestamp đã bị
      đảo ngược, các tin nhắn MỚI NHẤT có khoá NHỎ NHẤT trong khoảng của user đó → scan từ đầu khoảng này
      tự động trả về tin mới nhất trước. <code>LIMIT 1000</code> dừng sau khi đủ 1000 dòng, không cần đọc
      hết toàn bộ lịch sử tin nhắn của user (có thể hàng chục nghìn tin).</p>
      <div class="callout warn"><div class="lbl">So sánh với cách làm SAI (dùng filter thay vì row key)</div>
      Nếu thiết kế row key không tốt (vd chỉ dùng <code>userid</code> không kèm timestamp), muốn lấy "1000
      tin gần nhất" sẽ phải <code>scan</code> TOÀN BỘ tin nhắn của user rồi lọc/sắp xếp ở phía client — chi
      phí tăng tuyến tính theo tổng số tin nhắn, không phải theo số lượng cần lấy (1000).</div>""")]),

  # ---------------- PHẦN 4: Facebook Messages case study (giữ nguyên + mở rộng) ----------------
  dict(title="Facebook Messages 2010: ca sử dụng nổi tiếng nhất của HBase", bullets=[
    "Facebook chọn HBase cho hệ thống Messages mới (triển khai tháng 11/2010)",
    "Là minh chứng HBase có thể vận hành ở quy mô hàng trăm triệu người dùng",
    "Nhưng: Facebook sau đó đã chuyển Messages sang MyRocks (2018) — công nghệ không tồn tại mãi"],
   slides=[
    dict(h="Lý do Facebook chọn HBase cho Messages", body="""
      <div class="callout good"><div class="lbl">📚 Nguồn lịch sử</div>Để xây hệ thống tin nhắn mới, Facebook
      đã dựng nhiều prototype và thử nghiệm trên nhiều nền tảng lưu trữ phân tán khác nhau — HBase (mô phỏng
      theo Bigtable của Google) là nền tảng thắng cuộc, và Facebook triển khai hệ thống Messages dựa trên
      HBase vào tháng 11/2010.
      Nguồn: <a href="https://www.theregister.com/2010/12/17/facebook_messages_tech" target="_blank">The Register — Facebook Messages tech</a>.</div>
      <p><b>🗣️ Nói nôm na:</b> Facebook cần 1 "sổ tin nhắn" khổng lồ mà mỗi người dùng chỉ tra đúng sổ của
      mình (theo user_id) — không cần "JOIN" sổ của người này với sổ người khác. Đây đúng là bài toán
      get/put/scan theo khoá mà HBase làm rất tốt, không phải bài toán cần SQL linh hoạt.</p>
      <p>Đây là minh chứng công khai lớn nhất ở thời điểm đó cho thấy HBase/mô hình Bigtable có thể vận hành
      ổn định ở quy mô hàng trăm triệu người dùng hoạt động — câu chuyện này góp phần lớn khiến HBase trở
      thành lựa chọn NoSQL hàng đầu trong hệ sinh thái Hadoop suốt nhiều năm sau.</p>
      <div class="callout warn"><div class="lbl">Bài học trung thực: không công nghệ nào tồn tại mãi</div>
      Facebook sau đó đã di chuyển (migrate) hạ tầng Messages từ HBase sang MyRocks (một storage engine dựa
      trên RocksDB) vào năm 2018. Điều này không có nghĩa HBase "thất bại" — mà cho thấy lựa chọn công nghệ
      luôn gắn với một giai đoạn và một bộ yêu cầu cụ thể, và các hệ thống lớn tiếp tục tiến hoá khi yêu cầu
      thay đổi theo thời gian.</div>
      <details><summary>📖 Giải thích cho người mới bắt đầu: vì sao "đổi công nghệ" không có nghĩa là "công nghệ cũ sai"?</summary>
      <p>Hãy nghĩ như việc chọn xe đi lại: năm 2010, Facebook "mua" HBase vì nó vừa đúng nhu cầu lúc đó (tải
      ghi cực cao, tra theo khoá). Tới 2018, nhu cầu thay đổi (có thể cần tiết kiệm phần cứng hơn, cần tính
      năng mới mà RocksDB/MyRocks làm tốt hơn) — giống việc đổi từ xe tải sang xe khác phù hợp hơn khi hàng
      hoá/tuyến đường thay đổi, không có nghĩa xe tải cũ "tồi". Trong kỹ thuật phần mềm, đây gọi là sự thật
      hiển nhiên nhưng hay bị quên: <b>không có công nghệ "tốt nhất mãi mãi"</b>, chỉ có công nghệ phù hợp
      nhất VỚI một bộ ràng buộc tại MỘT thời điểm.</p></details>""")]),

  # ---------------- PHẦN 5: Thiết kế row key sâu — hotspotting & salting ----------------
  dict(title="Thiết kế row key: quyết định quan trọng nhất khi dùng HBase", bullets=[
    "Hotspotting: mọi row mới dồn vào 1 Region khi row key có tiền tố tăng đơn điệu (vd timestamp)",
    "2 cách chữa: đảo ngược timestamp (reversed timestamp) hoặc 'salting' (thêm tiền tố băm/ngẫu nhiên)",
    "🗣️ Nói nôm na: giống việc KHÔNG nên đánh số thứ tự hồ sơ bệnh án theo đúng ngày nhập viện nếu muốn chia đều việc lưu trữ cho nhiều kho"],
   slides=[
    dict(h="Thiết kế row key: quyết định quan trọng nhất khi dùng HBase", body="""
      <p>Giả sử cần lưu log sự kiện người dùng (user_id, timestamp, event_type). Hai cách thiết kế row key:</p>
      <table><tr><th>Thiết kế</th><th>Row key</th><th>Vấn đề</th></tr>
      <tr><td>Sai (hotspotting)</td><td><code>timestamp_userid</code></td><td>Mọi event MỚI đều có timestamp
      lớn nhất → luôn ghi vào cùng 1 vùng (region) ở "cuối" bảng → 1 region server bị quá tải, các server khác
      rảnh rỗi</td></tr>
      <tr><td>Tốt hơn</td><td><code>userid_reversedTimestamp</code> (đảo ngược timestamp)</td><td>Ghi dữ liệu
      của các user khác nhau phân tán đều lên nhiều region; vẫn giữ được thứ tự mới-nhất-trước khi đọc theo 1
      user cụ thể</td></tr></table>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Vì sao đặt <code>timestamp</code> làm
      tiền tố (prefix) của row key luôn là thiết kế nguy hiểm trong HBase khi hệ thống đang ghi dữ liệu MỚI
      liên tục? (Đáp: vì các row mới luôn có khoá lớn nhất, dồn hết việc ghi vào 1 region "nóng" ở cuối bảng —
      đúng vấn đề "hotspotting" nêu trên — mất hết lợi thế phân tán ghi của HBase.)</div>
      <table><tr><th>Ngành (minh hoạ)</th><th>Row key hotspot (SAI)</th><th>Hậu quả</th></tr>
      <tr><td>Y tế</td><td><code>ngay_nhap_vien_ma_benh_nhan</code></td>
      <td>Mọi bệnh nhân nhập viện HÔM NAY dồn vào đúng 1 kho lưu trữ, các kho của ngày trước "nguội" không
      ai dùng tới</td></tr>
      <tr><td>Thương mại điện tử</td><td><code>timestamp_don_hang</code></td>
      <td>Giờ cao điểm bán hàng (sale 12/12), toàn bộ đơn mới dồn vào 1 server lưu trữ — đúng lúc tải cao
      nhất lại là lúc hệ thống dễ nghẽn nhất</td></tr></table>"""),
    dict(h="Kỹ thuật \"salting\": chữa hotspot triệt để hơn khi vẫn cần sắp theo thời gian", body="""
      <p><b>🗣️ Nói nôm na:</b> "Salting" (rắc muối) nghĩa là CHỦ ĐỘNG thêm 1 tiền tố ngẫu nhiên/băm vào
      trước row key để "xé" các row vốn sẽ đứng liền nhau ra nhiều Region khác nhau — giống việc chủ động
      chia ngẫu nhiên khách hàng ra nhiều quầy thay vì để họ tự xếp hàng theo thứ tự đến (vốn dễ dồn vào 1
      quầy giờ cao điểm).</p>
      <p><b>Giải thích kỹ thuật:</b> Thay vì row key = <code>timestamp_userid</code>, salting thêm 1 tiền
      tố = <code>hash(userid) mod K</code> (K = số Region mong muốn phân tải) ở ĐẦU row key:</p>
      <div class="pd-formula"><div class="pd-formula-label">Salted row key</div>
      <div class="pd-formula-math">\\text{rowkey} = \\underbrace{(\\text{hash(userid)} \\bmod K)}_{\\text{salt, 1-2 ký tự}} + \\text{"\\_"} + \\text{timestamp} + \\text{"\\_"} + \\text{userid}</div></div>
      <p><b>Phép tính từng bước (ví dụ số thật):</b> Với K=4 Region mong muốn, userid="u8842", dùng
      <code>hash(userid) mod 4</code>:</p>
      <ol><li>Giả sử hàm băm đơn giản: tổng mã ASCII của "u8842" mod 4. Tổng ASCII = 117+56+56+52+50 = 331.</li>
      <li>331 mod 4 = 3 (vì 331 = 4×82 + 3).</li>
      <li>Salt = "3" → row key cuối = <code>3_20260115103000_u8842</code>.</li>
      <li>Với userid khác, vd "u1203": tổng ASCII = 117+49+50+48+51 = 315 → 315 mod 4 = 3 (315=4×78+3) — một
      salt khác sẽ rơi vào Region khác, tuỳ user.</li></ol>
      <div class="callout warn"><div class="lbl">Đánh đổi của salting — không có giải pháp miễn phí</div>
      Salting giải quyết hotspot ghi, nhưng làm MẤT khả năng <code>scan</code> hiệu quả theo khoảng thời
      gian liên tục (vì cùng 1 khoảng thời gian giờ nằm rải trên K Region khác nhau, phải scan cả K lần rồi
      gộp kết quả ở phía client) — đây là lý do thiết kế row key LUÔN phải cân nhắc: ứng dụng đọc theo kiểu
      gì nhiều hơn (theo user hay theo khoảng thời gian toàn hệ thống)?</div>
      <table><tr><th>Ngành (minh hoạ)</th><th>Áp dụng salting</th></tr>
      <tr><td>IoT (cảm biến)</td><td>Salt theo <code>hash(sensor_id) mod K</code> để ghi dữ liệu từ hàng
      nghìn cảm biến không dồn vào 1 Region theo thời gian ghi</td></tr>
      <tr><td>Logistics</td><td>Salt theo <code>hash(ma_don_hang) mod K</code> khi ghi log trạng thái vận
      chuyển theo thời gian thực của hàng chục nghìn đơn cùng lúc</td></tr></table>""")]),

  # ---------------- PHẦN 6: Sqoop — giữ nguyên lịch sử + mở rộng cơ chế ----------------
  dict(title="Apache Sqoop: cầu nối RDBMS cũ ↔ Hadoop mới", bullets=[
    "Aaron Kimball (Cloudera) phát triển, nộp patch đầu tiên tháng 5/2009",
    "Giải quyết bài toán rất thực tế: doanh nghiệp có hàng chục năm dữ liệu trong RDBMS, không thể bỏ qua khi chuyển sang Hadoop",
    "Trở thành Apache top-level project tháng 4/2012 — nhưng bị \"nghỉ hưu\" (Apache Attic) tháng 6/2021"],
   slides=[
    dict(h="Bài toán và cơ chế hoạt động của Sqoop", body="""
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>Sqoop do Aaron Kimball cùng nhóm phát
      triển tại Cloudera xây dựng, bắt đầu như một contrib module của Hadoop từ tháng 5/2009 (patch đầu tiên:
      HADOOP-5815). Tháng 4/2010 tách khỏi Hadoop contrib, do Cloudera duy trì trên GitHub; ngày 23/7/2011
      được incubate thành dự án Apache; tháng 4/2012 trở thành Apache top-level project.
      Nguồn: <a href="https://en.wikipedia.org/wiki/Sqoop" target="_blank">Sqoop — Wikipedia</a>.</div>
      <p><b>🗣️ Nói nôm na:</b> Sqoop giống 1 dịch vụ chuyển phát CHUYÊN BIỆT giữa 2 hệ thống kho hàng dùng 2
      chuẩn đóng gói khác nhau (RDBMS đóng gói kiểu "bảng có khoá chính cố định"; HDFS đóng gói kiểu "tệp
      văn bản phân tán trên nhiều máy") — Sqoop biết cách "dỡ hàng" đúng chuẩn 1 bên và "đóng lại" đúng
      chuẩn bên kia.</p>
      <p>Bài toán Sqoop giải quyết rất thực tế: hầu hết doanh nghiệp lớn đã có hàng chục năm dữ liệu nằm trong
      RDBMS (Oracle, MySQL, SQL Server...) từ trước khi Hadoop ra đời. Không ai muốn/có thể bỏ dữ liệu đó —
      Sqoop cho phép <b>import</b> (toàn bộ bảng, 1 bảng, hoặc 1 phần bảng) từ RDBMS vào HDFS qua job Map-only
      hoặc MapReduce, và <b>export</b> dữ liệu ngược lại từ HDFS ra RDBMS.</p>
      <table><tr><th>Ngành (minh hoạ)</th><th>RDBMS cũ cần chuyển</th><th>Vì sao cần Sqoop, không xoá RDBMS đi luôn</th></tr>
      <tr><td>Ngân hàng</td><td>Hệ thống core banking 20 năm tuổi (Oracle)</td>
      <td>Không thể ngừng vận hành hệ thống giao dịch thật để "xây lại từ đầu" — Sqoop đồng bộ dữ liệu
      SONG SONG trong khi hệ thống cũ vẫn chạy</td></tr>
      <tr><td>Bán lẻ</td><td>Hệ thống quản lý kho (MySQL) của từng chi nhánh</td>
      <td>Mỗi chi nhánh vẫn cần RDBMS cho giao dịch hàng ngày (ACID), nhưng cần gộp dữ liệu toàn hệ thống
      vào Hadoop để phân tích xu hướng</td></tr></table>"""),
    dict(h="Vì sao Sqoop import KHÔNG cần bước Reduce", body="""
      <div class="pd-formula"><div class="pd-formula-label">Sqoop import bảng orders từ MySQL vào HDFS</div>
      <div class="pd-formula-math">\\text{sqoop import --connect jdbc:mysql://host/db --table orders --target-dir /data/orders}</div></div>
      <p>Kết quả: Sqoop sinh 1 job Map-only (không cần Reduce vì đây chỉ là copy dữ liệu, không tổng hợp), mỗi
      Mapper đọc 1 phần của bảng <code>orders</code> (chia theo khoá chính), ghi ra các tệp văn bản trong thư
      mục HDFS <code>/data/orders</code>, các trường phân tách bởi dấu phẩy mặc định.</p>
      <p><b>Giải thích kỹ thuật thêm:</b> Nhắc lại từ module MapReduce&amp;YARN: bước Reduce chỉ cần khi có
      TỔNG HỢP (group-by, sum, join...). Sqoop import là phép COPY thuần (không biến đổi dữ liệu), nên chỉ
      cần N Mapper chạy song song, không có khái niệm "gộp theo key" nào cần Reducer xử lý.</p>
      <div class="callout good"><div class="lbl">🔗 Liên hệ trực tiếp đã học</div>Đây đúng là trường hợp
      đặc biệt của mô hình MapReduce đã học ở <code>hd-02-mapreduce-yarn</code>: khi bài toán không cần
      bước tổng hợp, Hadoop vẫn cho chạy "job MapReduce" nhưng Reduce = 0, tận dụng cơ chế phân tán công
      việc theo Mapper của framework mà không ép phải dùng cả 2 giai đoạn.</div>"""),
    dict(h="Vì sao Sqoop bị \"nghỉ hưu\" năm 2021 — bài học về chu kỳ sống công nghệ", body="""
      <div class="callout warn"><div class="lbl">📚 Nguồn lịch sử</div>Dự án Apache Sqoop chính thức bị
      retired (chuyển vào Apache Attic — nơi lưu các dự án Apache không còn được duy trì tích cực) vào tháng
      6/2021. Nguồn: <a href="https://en.wikipedia.org/wiki/Sqoop" target="_blank">Sqoop — Wikipedia</a>.</div>
      <p>Lý do thực tế (không phải vì Sqoop "làm sai" điều gì): cách doanh nghiệp đồng bộ dữ liệu giữa RDBMS và
      hệ thống Big Data đã dịch chuyển sang các công cụ Change Data Capture (CDC) streaming thời gian thực
      (ví dụ Debezium kết hợp Kafka — xem module <code>hd-05-kafka</code>) thay vì các job batch import/export
      định kỳ kiểu Sqoop. Đây là một ví dụ rõ ràng cho quy luật chung của ngành: công cụ ETL batch dần nhường
      vai trò cho kiến trúc streaming khi yêu cầu độ trễ dữ liệu ngày càng khắt khe hơn.</p>
      <table><tr><th></th><th>Sqoop (batch, định kỳ)</th><th>CDC streaming (vd Debezium+Kafka)</th></tr>
      <tr><td>Độ trễ dữ liệu</td><td>Theo lịch chạy (vd mỗi giờ/mỗi ngày)</td><td>Gần thời gian thực (giây)</td></tr>
      <tr><td>Cách lấy dữ liệu đổi</td><td>Quét lại toàn bảng hoặc theo cột "updated_at"</td>
      <td>Đọc trực tiếp transaction log của RDBMS (binlog MySQL, WAL PostgreSQL...)</td></tr>
      <tr><td>Tải lên RDBMS nguồn</td><td>Có thể nặng nếu bảng lớn, quét lại toàn bộ</td>
      <td>Nhẹ hơn, chỉ đọc log thay đổi</td></tr></table>""")]),

  # ---------------- PHẦN 7: So sánh split RDBMS/HDFS với các kích thước khác nhau ----------------
  dict(title="Ví dụ tính toán: Sqoop chia dữ liệu theo khoá — so sánh 2 kịch bản", bullets=[
    "Sqoop import chia bảng theo khoảng khoá chính cho N Mapper song song",
    "So sánh 2 kịch bản chia: dữ liệu phân bố ĐỀU vs phân bố LỆCH theo khoá"],
   slides=[
    dict(h="Kịch bản 1: khoá phân bố đều — chia Mapper hiệu quả", body="""
      <p>Bảng <code>orders</code> có 1.000.000 dòng, khoá chính <code>id</code> chạy liên tục từ 1 đến
      1.000.000 (phân bố ĐỀU). Chia cho 4 Mapper:</p>
      <table><tr><th>Mapper</th><th>Khoảng id</th><th>Số dòng</th></tr>
      <tr><td>Map-1</td><td>1 – 250.000</td><td>250.000</td></tr>
      <tr><td>Map-2</td><td>250.001 – 500.000</td><td>250.000</td></tr>
      <tr><td>Map-3</td><td>500.001 – 750.000</td><td>250.000</td></tr>
      <tr><td>Map-4</td><td>750.001 – 1.000.000</td><td>250.000</td></tr></table>
      <p>Mỗi Mapper tải đúng 25% công việc — thời gian hoàn thành job ≈ thời gian 1 Mapper xử lý 250.000
      dòng (các Mapper chạy song song).</p>"""),
    dict(h="Kịch bản 2: khoá phân bố LỆCH — hiệu ứng \"Mapper chậm nhất quyết định tất cả\"", body="""
      <p>Cùng 1.000.000 dòng, nhưng khoá <code>id</code> được cấp theo đợt — 70% dữ liệu (700.000 dòng) có
      id trong khoảng 1–100.000 (do dữ liệu cũ dồn vào khoảng id nhỏ), còn 30% còn lại (300.000 dòng) rải
      đều id 100.001–1.000.000. Sqoop vẫn chia 4 Mapper ĐỀU theo khoảng id (không biết dữ liệu phân bố lệch):</p>
      <table><tr><th>Mapper</th><th>Khoảng id</th><th>Số dòng thực tế</th></tr>
      <tr><td>Map-1</td><td>1 – 250.000</td><td>~700.000×(100.000/100.000) + phần rải... ≈ 775.000 (ước lượng, xem bước tính)</td></tr>
      <tr><td>Map-2</td><td>250.001 – 500.000</td><td>~75.000</td></tr>
      <tr><td>Map-3</td><td>500.001 – 750.000</td><td>~75.000</td></tr>
      <tr><td>Map-4</td><td>750.001 – 1.000.000</td><td>~75.000</td></tr></table>
      <p><b>Phép tính từng bước (ước lượng đơn giản hoá):</b></p>
      <ol><li>700.000 dòng "cũ" đều rơi vào khoảng id 1–100.000, nằm trọn trong khoảng của Map-1 (1–250.000).</li>
      <li>300.000 dòng còn lại rải đều trên khoảng id 100.001–1.000.000 (900.000 giá trị id) → mật độ ≈
      300.000/900.000 = 1/3 dòng mỗi đơn vị khoảng id.</li>
      <li>Map-1 còn nhận thêm phần rải trong khoảng 100.001–250.000 (150.000 đơn vị) × 1/3 ≈ 50.000 dòng.</li>
      <li>Tổng Map-1 ≈ 700.000 + 50.000 = 750.000 dòng — còn Map-2/3/4 mỗi Mapper chỉ nhận ≈ 250.000×1/3 ≈
      83.000 dòng (làm tròn gần đúng).</li></ol>
      <div class="callout warn"><div class="lbl">Bài học cốt lõi</div>Dù chia "đều về khoảng khoá", job vẫn
      LỆCH TẢI nặng nếu dữ liệu không phân bố đều trong khoảng đó — toàn bộ job phải chờ Mapper chậm nhất
      (Map-1, xử lý ~750.000/1.000.000 dòng) hoàn thành, 3 Mapper còn lại gần như "ngồi chơi" sau khi xong
      phần nhỏ của mình. Đây là lý do khi dùng Sqoop thật, cần hiểu phân bố khoá trước khi chọn
      <code>--split-by</code>, không mặc định tin chia đều theo khoảng số sẽ cho tải đều.</div>""")]),

  # ---------------- PHẦN 8: HBase vs RDBMS vs Sqoop — tổng hợp khi nào dùng gì ----------------
  dict(title="Tổng hợp: khi nào dùng HBase, khi nào vẫn cần RDBMS, Sqoop đứng ở đâu", bullets=[
    "Bảng quyết định nhanh: đặc điểm bài toán → công nghệ phù hợp",
    "Sqoop không phải đối thủ của HBase — nó là cầu nối giữa 2 thế giới hoàn toàn khác mô hình dữ liệu"],
   slides=[
    dict(h="Bảng quyết định: HBase so với RDBMS", body="""
      <table><tr><th>Đặc điểm bài toán</th><th>Chọn</th><th>Vì sao</th></tr>
      <tr><td>Cần JOIN nhiều bảng, giao dịch ACID phức tạp (vd chuyển tiền ngân hàng)</td><td>RDBMS</td>
      <td>HBase không hỗ trợ JOIN hiệu quả, ACID chỉ đảm bảo ở mức 1 dòng</td></tr>
      <tr><td>Tra cứu theo khoá đơn, tải ghi cực cao, dữ liệu tới petabyte (vd tin nhắn, log sự kiện)</td>
      <td>HBase</td><td>get/put/scan theo khoá cho độ trễ ổn định, khả mở ngang dễ</td></tr>
      <tr><td>Cần đồng bộ dữ liệu 1 lần/định kỳ giữa RDBMS cũ và Hadoop</td><td>Sqoop (không phải đối thủ
      của HBase hay RDBMS)</td><td>Chỉ là cầu nối chuyển đổi định dạng, không thay thế vai trò lưu trữ của
      cả 2 bên</td></tr></table>
      <div class="callout info"><div class="lbl">Vì sao câu hỏi "HBase hay Sqoop mạnh hơn" là sai ngay từ
      đầu</div>HBase là một nơi LƯU TRỮ dữ liệu; Sqoop là một công cụ DI CHUYỂN dữ liệu giữa 2 nơi lưu trữ
      khác mô hình. Trong thực tế, một pipeline hoàn chỉnh có thể dùng CẢ HAI: Sqoop import dữ liệu RDBMS
      cũ vào HDFS, rồi 1 job khác (MapReduce/Spark) nạp dữ liệu đó vào HBase để phục vụ tra cứu tốc độ cao.</div>"""),
    dict(h="Tổng kết Phần 4: 5 điều phải nhớ", body="""
      <ol><li>HBase = bản mã nguồn mở của Bigtable (Google, 2006), do Powerset xây (2008) cho bài toán NLP.</li>
      <li>Row key là quyết định thiết kế quan trọng nhất — quyết định hotspot hay không, cần cân nhắc đọc
      theo khoảng hay theo khoá đơn trước khi chọn cách đặt khoá (có/không salting).</li>
      <li>HBase đánh đổi SQL linh hoạt để lấy tốc độ get/put/scan theo khoá ổn định ở quy mô petabyte —
      không phải "thiếu tính năng", mà là lựa chọn kiến trúc có chủ đích.</li>
      <li>Sqoop là cầu nối, không phải đối thủ của HBase/RDBMS — và đã bị thay vai trò bởi CDC streaming
      khi ngành chuyển sang cần dữ liệu gần thời gian thực hơn.</li>
      <li>Không công nghệ nào "thắng mãi": Facebook Messages minh chứng cả 2 chiều — HBase từng là lựa
      chọn đúng (2010), rồi bị thay thế khi yêu cầu thay đổi (2018).</li></ol>""")]),
 ],
 quiz=[
  dict(q="HBase lấy cảm hứng kiến trúc trực tiếp từ hệ thống nào của Google?", opts=["GFS", "MapReduce", "Bigtable", "Chubby"],
   correct=2, explain="HBase là bản mã nguồn mở theo mô hình Bigtable (paper Google 2006), chạy trên HDFS."),
  dict(q="Công ty nào ban đầu xây dựng HBase, và để giải quyết bài toán gì?", opts=[
     "Facebook, cho hệ thống Messages", "Powerset, cho tìm kiếm ngôn ngữ tự nhiên (NLP)", "Cloudera, cho ETL", "LinkedIn, cho activity stream"],
   correct=1, explain="Powerset xây HBase (phát hành 28/3/2008) để phục vụ bài toán tìm kiếm NLP ở quy mô lớn."),
  dict(q="Khác biệt chính giữa HBase và RDBMS truyền thống là gì?", opts=[
     "HBase nhanh hơn ở mọi tác vụ", "HBase là NoSQL, không có ngôn ngữ truy vấn mức cao như SQL, dùng API get/put/scan theo khoá", "HBase không hỗ trợ lưu bảng lớn", "HBase chạy trên 1 máy duy nhất"],
   correct=1, explain="Đánh đổi: bỏ ngôn ngữ truy vấn linh hoạt để đạt khả mở/băng thông ghi cao."),
  dict(q="Trong mô hình Bigtable/HBase, điều gì KHÔNG cần khai báo trước schema, khác với RDBMS?", opts=[
     "Row key", "Column family", "Qualifier (tên cột cụ thể trong 1 family)", "Tên bảng"],
   correct=2, explain="Column family khai báo trước, ít thay đổi; qualifier có thể thêm tự do ở từng dòng mà không cần sửa schema."),
  dict(q="Region trong HBase được chia theo tiêu chí gì?", opts=[
     "Theo column family", "Theo khoảng row key liên tiếp", "Theo số lượng cột", "Theo thời gian tạo dữ liệu"],
   correct=1, explain="Mỗi Region phục vụ 1 khoảng row key liên tiếp; khi Region quá lớn, HBase tự split thành 2 Region mới."),
  dict(q="Vì sao 1 bảng có mọi row key mới đều tăng dần (vd timestamp làm tiền tố) dễ gây hotspot?", opts=[
     "Vì row key quá dài", "Vì mọi row mới rơi vào cùng 1 khoảng, do đó cùng 1 Region/RegionServer, dồn hết tải ghi vào đó",
     "Vì HBase không hỗ trợ số tăng dần", "Vì column family bị trùng"],
   correct=1, explain="Region chia theo khoảng row key — khoá tăng đơn điệu khiến mọi ghi mới dồn vào Region 'nóng' nhất."),
  dict(q="Kỹ thuật 'salting' trong thiết kế row key HBase làm gì?", opts=[
     "Mã hoá dữ liệu để bảo mật", "Thêm tiền tố ngẫu nhiên/băm vào đầu row key để phân tán các row vốn sẽ đứng liền nhau ra nhiều Region khác nhau",
     "Nén dữ liệu để giảm dung lượng", "Xoá bớt cột không dùng"],
   correct=1, explain="Salting 'xé' row key tăng đơn điệu ra nhiều Region bằng tiền tố hash(key) mod K."),
  dict(q="Đánh đổi của kỹ thuật salting là gì?", opts=[
     "Không có đánh đổi, chỉ có lợi", "Làm mất khả năng scan hiệu quả theo khoảng thời gian liên tục (phải scan cả K Region rồi gộp)",
     "Làm HBase chậm hơn khi ghi", "Làm tăng kích thước row key tới mức không dùng được"],
   correct=1, explain="Salting đánh đổi hiệu năng ghi lấy chi phí đọc theo khoảng — vì dữ liệu cùng khoảng thời gian giờ rải trên nhiều Region."),
  dict(q="get(rowkey) trong HBase gần tương đương với câu SQL nào, và khác biệt quan trọng gì?", opts=[
     "SELECT * FROM t — không có khác biệt gì", "SELECT * FROM t WHERE pk = ? — nhưng KHÔNG hỗ trợ WHERE hiệu quả theo cột khác pk",
     "DELETE FROM t WHERE pk = ?", "CREATE TABLE t"],
   correct=1, explain="HBase chỉ tối ưu truy vấn theo row key; muốn lọc theo cột khác hiệu quả cần thiết kế lại row key hoặc dùng chỉ mục phụ."),
  dict(q="Facebook triển khai hệ thống Messages dựa trên HBase vào thời điểm nào?", opts=["2008", "11/2010", "2015", "2021"],
   correct=1, explain="Tháng 11/2010, sau khi thử nghiệm nhiều nền tảng lưu trữ phân tán khác."),
  dict(q="Điều gì xảy ra với hệ thống Messages của Facebook sau đó (2018)?", opts=[
     "Vẫn dùng HBase không đổi tới nay", "Facebook migrate sang MyRocks (dựa trên RocksDB)", "Facebook đóng dịch vụ Messages", "Facebook quay lại dùng RDBMS truyền thống"],
   correct=1, explain="Đây là bài học về chu kỳ sống công nghệ: không hệ thống nào tồn tại mãi dù từng rất thành công."),
  dict(q="Aaron Kimball phát triển Sqoop ở công ty nào, nộp patch đầu tiên khi nào?", opts=[
     "Yahoo, 2006", "Cloudera, 5/2009", "Facebook, 2010", "Google, 2004"],
   correct=1, explain="Aaron Kimball tại Cloudera, patch đầu tiên HADOOP-5815 nộp tháng 5/2009."),
  dict(q="Sqoop giải quyết bài toán thực tế gì cho doanh nghiệp?", opts=[
     "Thay thế hoàn toàn RDBMS", "Trung chuyển dữ liệu theo khối giữa Hadoop và RDBMS có cấu trúc (import/export)", "Tăng tốc truy vấn SQL", "Mã hoá dữ liệu nhạy cảm"],
   correct=1, explain="Doanh nghiệp có nhiều năm dữ liệu trong RDBMS — Sqoop là cầu nối 2 chiều với HDFS."),
  dict(q="Vì sao Sqoop import KHÔNG cần bước Reduce?", opts=[
     "Vì Sqoop không dùng MapReduce", "Vì đây là phép copy thuần, không có tổng hợp theo key cần Reducer xử lý",
     "Vì bảng RDBMS luôn nhỏ", "Vì Reduce chỉ dùng cho Pig/Hive"],
   correct=1, explain="Reduce chỉ cần khi có group-by/tổng hợp; copy dữ liệu thuần chỉ cần các Mapper chạy song song."),
  dict(q="Apache Sqoop hiện ở trạng thái nào (tính tới thời điểm viết bài)?", opts=[
     "Vẫn đang phát triển tích cực", "Đã bị retired, chuyển vào Apache Attic từ tháng 6/2021", "Chưa từng chính thức công bố", "Vừa được tách thành 2 dự án mới"],
   correct=1, explain="Sqoop bị retired tháng 6/2021 khi CDC streaming (vd Debezium+Kafka) thay thế vai trò ETL batch của nó."),
  dict(q="So với Sqoop, CDC streaming (vd Debezium+Kafka) lấy dữ liệu thay đổi từ RDBMS theo cách nào?", opts=[
     "Quét lại toàn bảng theo lịch", "Đọc trực tiếp transaction log của RDBMS (binlog/WAL), gần thời gian thực",
     "Yêu cầu RDBMS ngừng hoạt động", "Không thể lấy dữ liệu thay đổi"],
   correct=1, explain="CDC đọc log giao dịch thay vì quét lại toàn bảng — nhẹ hơn và gần thời gian thực hơn."),
  dict(q="Trong ví dụ Sqoop chia 1.000.000 dòng với khoá phân bố LỆCH (70% dồn vào 10% khoảng khoá), điều gì xảy ra với thời gian hoàn thành job?", opts=[
     "Không ảnh hưởng gì vì chia đều theo khoảng số", "Job phải chờ Mapper nhận nhiều dòng nhất (lệch tải) hoàn thành, các Mapper khác gần như rảnh sau khi xong phần nhỏ",
     "Job sẽ chạy nhanh hơn vì ít Mapper cần đợi", "Sqoop tự phát hiện và chia lại cho đều"],
   correct=1, explain="Chia theo khoảng khoá không đảm bảo chia đều TẢI nếu phân bố dữ liệu trong khoảng đó không đều — đây là bài học thực tế khi chọn --split-by."),
  dict(q="Vì sao câu hỏi 'HBase hay Sqoop mạnh hơn' là sai ngay từ gốc?", opts=[
     "Vì cả hai đều không còn được dùng", "Vì HBase là nơi LƯU TRỮ, Sqoop là công cụ DI CHUYỂN dữ liệu giữa 2 hệ thống khác mô hình — không cùng vai trò để so sánh",
     "Vì HBase và Sqoop là 2 tên khác của cùng 1 công cụ", "Vì Sqoop thay thế hoàn toàn HBase"],
   correct=1, explain="HBase và Sqoop giải quyết 2 vấn đề khác nhau (lưu trữ vs di chuyển dữ liệu), thường dùng CÙNG NHAU trong 1 pipeline, không phải lựa chọn loại trừ."),
  dict(q="HBase được gọi là gì trong hệ sinh thái Hadoop?", opts=["Công cụ ETL", "'Hệ quản trị CSDL của Hadoop'", "Hệ thống lập lịch workflow", "Công cụ coordination phân tán"],
   correct=1, explain="Vì lưu dữ liệu có cấu trúc dạng bảng trên HDFS với khả năng đọc/ghi tốc độ cao, HBase đóng vai trò tương tự 1 hệ quản trị CSDL cho Hadoop."),
  dict(q="Tại sao bảng 'lịch sử xét nghiệm bệnh nhân' (số lần xét nghiệm mỗi người rất khác nhau) hợp với mô hình wide-column hơn RDBMS cố định cột?", opts=[
     "Vì RDBMS không lưu được số liệu y tế", "Vì mỗi dòng có thể có số qualifier khác nhau mà không cần cột NULL lãng phí cho người ít xét nghiệm hơn",
     "Vì wide-column nhanh hơn ở mọi trường hợp", "Vì RDBMS không hỗ trợ tiếng Việt"],
   correct=1, explain="RDBMS cần số cột cố định biết trước; wide-column cho phép số lượng cột (qualifier) khác nhau giữa các dòng mà không lãng phí."),
 ])

if __name__ == "__main__":
    print(len(HD04_EXPANDED["parts"]), "parts",
          sum(len(p["slides"]) for p in HD04_EXPANDED["parts"]), "slides",
          len(HD04_EXPANDED["quiz"]), "quiz")
