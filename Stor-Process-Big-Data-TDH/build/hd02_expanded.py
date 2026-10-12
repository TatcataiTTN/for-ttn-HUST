# -*- coding: utf-8 -*-
"""Bản mở rộng SÂU của module hd-02-mapreduce-yarn (n=26), viết trực tiếp (không qua fork) sau khi
agent fork gốc bị rate-limit. Giữ nguyên 100% các callout lịch sử/nguồn đã có trong bản gốc
(hadoop_deepdive_content.py), chỉ MỞ RỘNG thêm theo đúng chuẩn 02-module-content-standard.md:
mỗi khái niệm có 🗣️ nói nôm na → giải thích kỹ thuật → ví dụ ≥2-3 ngành (nhãn (minh hoạ) rõ ràng)
→ bảng HTML → câu hỏi kiểm tra ngay. n/slug/title/tag giữ nguyên để không vỡ phần khác của site."""

HD02_EXPANDED = dict(n=26, slug="hd-02-mapreduce-yarn",
 title="MapReduce & YARN: từ mô hình lập trình tới hệ điều hành cụm",
 tag="Lịch sử MapReduce · Vì sao YARN ra đời",
 intro="MapReduce giải quyết bài toán xử lý; nhưng chính MapReduce bản đầu lại tạo ra một điểm nghẽn mới — JobTracker. Câu chuyện YARN là câu chuyện sửa lỗi kiến trúc của chính Hadoop, và câu chuyện đó còn lặp lại 1 lần nữa 10 năm sau với Kubernetes.",
 parts=[

  # ---------------- PHẦN 1 ----------------
  dict(title="MapReduce: mô hình lập trình từ Google", bullets=[
    "Google công bố MapReduce năm 2004 (Dean & Ghemawat)",
    "Mô hình: Map → Shuffle & Sort → Reduce trên cặp key-value",
    "Ưu điểm được thiết kế có chủ đích: đơn giản, linh hoạt, khả mở"],
   slides=[
    dict(h="🗣️ Nói nôm na: MapReduce là gì trước khi vào kỹ thuật", body="""
      <p><b>Nói nôm na:</b> hãy tưởng tượng bạn cần đếm tổng số phiếu bầu cho 5 ứng viên, nhưng có 10 triệu
      lá phiếu rải ở 1000 phòng khác nhau. Cách ngu nhất: 1 người đi gom hết 10 triệu phiếu về 1 bàn rồi đếm.
      Cách MapReduce làm: mỗi phòng tự đếm phiếu CỦA PHÒNG MÌNH trước (đây là <b>Map</b>), rồi gửi riêng từng
      kết quả theo TỪNG ứng viên về 1 người tổng hợp chuyên trách ứng viên đó (đây là <b>Shuffle</b>), người
      đó chỉ cần cộng các số đã đếm sẵn lại (đây là <b>Reduce</b>) — không ai phải đụng tay vào cả 10 triệu
      lá phiếu gốc.</p>
      <div class="callout good"><div class="lbl">📖 Giải thích cho người mới bắt đầu</div>
      <details><summary>Bấm để xem giải thích cực đơn giản về vì sao phải tách 3 bước</summary>
      <p>Nếu không tách 3 bước, bạn phải viết 1 chương trình vừa biết "lấy dữ liệu ở đâu", vừa biết "chia
      việc cho 1000 phòng ra sao", vừa biết "nếu 1 phòng báo cáo trễ/sai thì làm gì", vừa biết "cộng tổng
      kiểu gì" — tất cả trộn chung trong 1 đoạn code. MapReduce tách phần "logic nghiệp vụ" (đếm 1 lá phiếu,
      cộng 2 số) ra khỏi phần "logic hạ tầng" (chia việc, chịu lỗi, gửi dữ liệu) — người viết code chỉ cần lo
      2 hàm nhỏ (map, reduce), còn framework tự lo toàn bộ phần hạ tầng phức tạp còn lại.</p></details></div>
      {callout_info}
      <p style="margin-top:10px">Trước MapReduce, kỹ sư Google phải tự viết code xử lý song song/phân tán
      cho từng bài toán — dễ lỗi, khó bảo trì, logic phân tán (chia việc, xử lý lỗi node, gộp kết quả) trộn
      lẫn với logic nghiệp vụ. MapReduce tách 2 phần này: người viết code chỉ cần định nghĩa 2 hàm
      <code>map</code> và <code>reduce</code>, còn framework tự lo phân tán, chịu lỗi, gộp kết quả.</p>
      <table><tr><th>Giai đoạn</th><th>Việc làm</th></tr>
      <tr><td>Map</td><td>Đọc từng bản ghi đầu vào (key, value), sinh ra 0 hoặc nhiều cặp (key', value') trung gian</td></tr>
      <tr><td>Shuffle &amp; Sort</td><td>Hadoop tự gộp và sắp xếp output của mọi Mapper theo key', chia vào các partition — mỗi partition là đầu vào của 1 Reducer</td></tr>
      <tr><td>Reduce</td><td>Mỗi Reducer nhận toàn bộ value' của 1 key', xử lý và sinh ra cặp (key'', value'') cuối cùng</td></tr></table>
      <div class="callout info"><div class="lbl">Nguồn: materials/hangout/2024/2_hadoop_ecosystem_vn.pdf (Chương 2)</div>
      Ví dụ Word Count trong giáo trình chính là minh hoạ kinh điển nhất của mô hình này: Map phát ra (từ, 1)
      cho mỗi từ, Reduce cộng tổng các giá trị 1 theo từng từ khoá.</div>""".replace("{callout_info}","")),
    dict(h="Ví dụ minh hoạ MapReduce ở 3 ngành khác nhau (đều minh hoạ, không phải số liệu thật)", body="""
      <p>Để thấy MapReduce không phải khái niệm "chỉ dùng cho dữ liệu máy tính", dưới đây là cùng 1 cơ chế
      Map → Shuffle &amp; Sort → Reduce áp vào 3 ngành khác hẳn nhau:</p>
      <table><tr><th>Ngành</th><th>Map (chia nhỏ, xử lý cục bộ)</th><th>Shuffle&amp;Sort (gộp theo "khoá")</th><th>Reduce (tổng hợp cuối)</th></tr>
      <tr><td>Bầu cử (minh hoạ)</td><td>Mỗi phòng phiếu tự đếm phiếu của ứng viên</td><td>Gộp kết quả theo TỪNG ứng viên từ mọi phòng</td><td>Cộng tổng phiếu toàn quốc cho mỗi ứng viên</td></tr>
      <tr><td>Bán lẻ (minh hoạ)</td><td>Mỗi chi nhánh siêu thị tự tính doanh số theo từng mặt hàng trong ngày</td><td>Gộp theo TỪNG mặt hàng từ mọi chi nhánh</td><td>Tổng doanh số toàn hệ thống theo mặt hàng</td></tr>
      <tr><td>Y tế (minh hoạ)</td><td>Mỗi bệnh viện tự đếm số ca mắc theo từng loại bệnh trong tuần</td><td>Gộp theo TỪNG loại bệnh từ mọi bệnh viện</td><td>Tổng số ca mắc toàn tỉnh theo loại bệnh (phục vụ cảnh báo dịch)</td></tr></table>
      <div class="callout warn"><div class="lbl">Bẫy hay gặp</div>Nhiều người tưởng "Shuffle" là bước xáo
      trộn ngẫu nhiên — SAI. Shuffle trong MapReduce là GOM DỮ LIỆU THEO ĐÚNG KHOÁ (key) lại một chỗ, hoàn
      toàn có trật tự, không phải xáo trộn vô nghĩa.</div>"""),
    dict(h="Combiner & Partitioner — chi tiết hay bị bỏ qua", body="""
      <p>Giáo trình gốc không nhấn vào 2 thành phần tối ưu quan trọng này — nhưng thiếu chúng, MapReduce thực
      tế sẽ chậm hơn rất nhiều so với lý thuyết:</p>
      <ul class="pd-legend"><li><b>Combiner</b><span>một "mini-Reducer" chạy ngay trên node Map, gộp trước
      các giá trị cùng key TRƯỚC khi gửi qua mạng tới Reducer — giảm mạnh lưu lượng shuffle. Với Word Count,
      combiner cộng tổng từng từ ngay tại Mapper trước khi gửi đi.</span></li>
      <li><b>Partitioner</b><span>quyết định cặp (key', value') trung gian nào đi vào Reducer nào — mặc định
      dùng hash(key) mod số-Reducer, đảm bảo mọi value' của cùng 1 key' luôn vào đúng 1 Reducer duy nhất.</span></li></ul>
      <p><b>🗣️ Nói nôm na về Combiner:</b> giống việc mỗi chi nhánh ngân hàng (minh hoạ) tự cộng sổ quỹ của
      chi nhánh mình trước khi gửi báo cáo về hội sở, thay vì gửi từng tờ biên lai lẻ về cho hội sở tự cộng —
      hội sở chỉ nhận 1 số tổng mỗi chi nhánh, không phải hàng nghìn tờ biên lai.</p>
      <div class="callout warn"><div class="lbl">Bẫy hay gặp</div>Combiner chỉ áp dụng được khi hàm reduce có
      tính <b>kết hợp và giao hoán</b> (associative, commutative) — như cộng tổng, lấy max/min. Với phép tính
      trung bình (average), combiner ngây thơ sẽ cho kết quả SAI nếu không cẩn thận (phải gộp cả tổng và số
      lượng, không gộp trực tiếp giá trị trung bình).</div>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Nếu Mapper 1 có điểm trung bình 8,0
      (từ 10 bài) và Mapper 2 có điểm trung bình 6,0 (từ 2 bài), Combiner "ngây thơ" lấy trung bình của
      (8,0; 6,0) = 7,0 — sai ở đâu? (Đáp: trung bình đúng phải tính lại theo TỔNG điểm/TỔNG số bài =
      (10×8,0 + 2×6,0)/(10+2) = 92/12 ≈ 7,67, không phải trung bình đơn giản của 2 trung bình con có trọng
      số khác nhau.)</div>"""),
    dict(h="Ví dụ tính toán: mức giảm lưu lượng shuffle nhờ Combiner", body="""
      <p>Giả sử 1 văn bản có 9.000 từ, chia cho 3 Mapper (mỗi Mapper xử lý 3.000 từ), và trong 3.000 từ đó
      có trung bình 500 từ khác nhau (nhiều từ lặp lại nhiều lần).</p>
      <ol><li><b>Không có Combiner:</b> mỗi Mapper gửi đúng 3.000 cặp (word, 1) qua mạng → tổng 3 Mapper gửi
      3 × 3.000 = 9.000 cặp.</li>
      <li><b>Có Combiner:</b> mỗi Mapper tự gộp trước thành tối đa 500 cặp (word, count) → tổng 3 Mapper gửi
      3 × 500 = 1.500 cặp.</li>
      <li>Mức giảm lưu lượng = (9.000 − 1.500) / 9.000 = 83,3%.</li></ol>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Nếu văn bản có RẤT ÍT từ lặp lại (gần
      như mỗi từ chỉ xuất hiện 1 lần, ví dụ danh sách 3.000 mã khách hàng duy nhất), Combiner còn giúp được
      bao nhiêu? (Đáp: gần như KHÔNG giúp gì — nếu mỗi key chỉ xuất hiện 1 lần, Combiner không có gì để gộp,
      vẫn phải gửi gần như đủ 3.000 cặp. Combiner chỉ hiệu quả khi dữ liệu có nhiều key LẶP LẠI.)</div>""")]),

  # ---------------- PHẦN 2 ----------------
  dict(title="Giới hạn của Hadoop 1.0: JobTracker là điểm nghẽn", bullets=[
    "1 JobTracker duy nhất quản lý TOÀN BỘ job + giám sát TaskTracker trên mọi node",
    "Giới hạn thực tế: cụm tối đa ~4.000 node, ~40.000 task đồng thời",
    "JobTracker vừa là lập lịch tài nguyên, vừa là giám sát tiến trình — gộp 2 vai trò khác nhau vào 1 chỗ"],
   slides=[
    dict(h="Vai trò quá tải của JobTracker", body="""
      <p>Trong Hadoop 1.0, <b>JobTracker</b> (chạy trên 1 node duy nhất) đảm nhiệm cả 2 việc hoàn toàn khác
      nhau: (1) quản lý tài nguyên cụm (máy nào còn trống để giao việc), và (2) theo dõi tiến trình của mọi
      MapReduce job. <b>TaskTracker</b> chạy trên từng node, thực thi task và báo cáo tiến trình ngược lại
      cho JobTracker.</p>
      <div class="callout warn"><div class="lbl">📚 Nguồn lịch sử</div>Có 1 JobTracker duy nhất tạo ra giới
      hạn mở rộng thực tế: kích thước cụm tối đa khoảng hơn 4.000 node, và số lượng task đồng thời giới hạn ở
      khoảng 40.000 — vượt ngưỡng này, JobTracker trở thành nút nghẽn hiệu năng và điểm lỗi đơn (SPOF).
      Nguồn: <a href="https://www.infoworld.com/article/2171598/hadoop-2-big-data-s-big-leap-forward.html" target="_blank">InfoWorld — Hadoop 2: Big data's big leap forward</a>.</div>
      <p>Đây chính là động lực trực tiếp dẫn tới YARN: tách vai trò "quản lý tài nguyên" (ResourceManager) ra
      khỏi vai trò "theo dõi 1 job cụ thể" (ApplicationMaster, giờ mỗi job có 1 cái riêng thay vì dồn hết vào
      1 JobTracker).</p>"""),
    dict(h="🗣️ Nói nôm na về điểm nghẽn — 3 ngành khác nhau cùng 1 bài học", body="""
      <p><b>Nói nôm na:</b> JobTracker giống 1 người quản lý duy nhất phải vừa quyết định "phòng nào còn
      trống để nhận khách", vừa tự tay ghi chép tiến độ phục vụ của TẤT CẢ phòng trong 1 khách sạn 5000
      phòng — tới một quy mô nào đó, 1 người không thể theo kịp.</p>
      <table><tr><th>Ngành</th><th>"JobTracker" trong ngành đó</th><th>Điểm nghẽn xảy ra khi nào</th></tr>
      <tr><td>Khách sạn (minh hoạ)</td><td>1 lễ tân vừa xếp phòng vừa theo dõi tiến độ dọn phòng mọi tầng</td><td>Khi số phòng vượt quá khả năng 1 người nhớ/ghi chép kịp</td></tr>
      <tr><td>Bệnh viện (minh hoạ)</td><td>1 điều phối viên vừa phân bác sĩ theo ca vừa theo dõi tiến độ mọi ca mổ</td><td>Khi số ca mổ đồng thời vượt quá khả năng theo dõi của 1 người</td></tr>
      <tr><td>Call center (minh hoạ)</td><td>1 trưởng ca vừa phân cuộc gọi cho nhân viên vừa theo dõi tiến độ xử lý từng cuộc</td><td>Khi số cuộc gọi đồng thời vượt khả năng giám sát 1 người</td></tr></table>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Trong cả 3 ví dụ trên, giải pháp
      "YARN-style" sẽ là gì? (Đáp: tách thành 2 vai trò riêng — 1 người/hệ thống lo PHÂN BỔ tài nguyên tổng
      thể (phòng/bác sĩ/nhân viên), và MỖI ca/job/cuộc gọi có 1 người theo dõi tiến độ RIÊNG của chính nó,
      không dồn hết việc theo dõi về 1 người.)</div>""")]),

  # ---------------- PHẦN 3 ----------------
  dict(title="YARN (Hadoop 2.0, 2012): tách resource management khỏi xử lý", bullets=[
    "ResourceManager (toàn cụm) + NodeManager (mỗi node) + ApplicationMaster (mỗi job)",
    "YARN = Yet Another Resource Negotiator — đúng nghĩa đen, một cái tên tự trào",
    "Hệ quả quan trọng nhất: KHÔNG CHỈ MapReduce mới chạy được trên cụm Hadoop nữa"],
   slides=[
    dict(h="Ba vai trò mới của YARN", body="""
      <div class="pd-formula"><div class="pd-formula-label">Kiến trúc YARN</div>
      <div class="pd-formula-math">\\text{ResourceManager (1/cụm)} + \\text{NodeManager (1/node)} + \\text{ApplicationMaster (1/job)}</div></div>
      <ul class="pd-legend"><li><b>ResourceManager</b><span>quản lý toàn bộ tài nguyên cụm (CPU, RAM theo
      Container), quyết định cấp bao nhiêu tài nguyên cho ứng dụng nào</span></li>
      <li><b>NodeManager</b><span>chạy trên mỗi node, báo cáo tài nguyên khả dụng của node đó, giám sát
      Container chạy trên node mình</span></li>
      <li><b>ApplicationMaster</b><span>MỖI job có 1 ApplicationMaster riêng, tự thương lượng tài nguyên với
      ResourceManager cho job của mình — đây là điểm khác biệt cốt lõi: trách nhiệm theo dõi tiến trình được
      PHÂN TÁN ra từng job, không dồn về 1 JobTracker duy nhất nữa</span></li></ul>
      <div class="callout good"><div class="lbl">📖 Giải thích cho người mới bắt đầu</div>
      <details><summary>Bấm để xem ví dụ cực đơn giản về "Container" là gì</summary>
      <p>Container trong YARN không phải Docker container — nó chỉ là 1 "gói" tài nguyên được cấp (vd 2 CPU
      core + 4GB RAM) mà ApplicationMaster xin từ ResourceManager để chạy 1 task cụ thể. Giống việc bạn đặt
      trước "1 bàn 4 người" ở nhà hàng (minh hoạ) — bàn đó (Container) được cấp cho nhóm bạn dùng trong 1
      khoảng thời gian, dùng xong thì trả lại cho nhà hàng cấp cho nhóm khác.</p></details></div>
      <div class="callout good"><div class="lbl">Vì sao đây là bước nhảy kiến trúc, không chỉ bản vá lỗi</div>
      YARN biến Hadoop từ "một hệ thống chỉ chạy được MapReduce" thành "một hệ điều hành cấp tài nguyên cho
      NHIỀU loại ứng dụng khác nhau cùng lúc" — đây là lý do Spark, Tez, Flink đều có thể chạy trên cùng 1 cụm
      Hadoop với YARN làm lớp cấp phát tài nguyên bên dưới.</div>"""),
    dict(h="Capacity Scheduler vs Fair Scheduler — 2 chính sách chia tài nguyên của YARN", body="""
      <p>ResourceManager không tự nghĩ ra cách chia Container — nó dùng 1 trong các "chính sách lập lịch"
      (scheduler) có thể cấu hình được. 2 chính sách phổ biến nhất:</p>
      <table><tr><th>Chính sách</th><th>Cách chia</th><th>Phù hợp khi</th></tr>
      <tr><td>Capacity Scheduler</td><td>Chia cụm thành các "hàng đợi" (queue) có % tài nguyên cố định cho
      từng phòng/nhóm (vd phòng Data Engineering 60%, phòng Data Science 40%)</td><td>Nhiều team dùng chung 1
      cụm, cần đảm bảo mỗi team LUÔN có 1 phần tài nguyên tối thiểu, không bị team khác "nuốt" hết</td></tr>
      <tr><td>Fair Scheduler</td><td>Chia công bằng động giữa các job đang chạy — tăng đều phần cấp tới khi
      đạt nhu cầu hoặc hết tài nguyên</td><td>Khối lượng công việc biến động, muốn mọi job được đối xử công
      bằng theo thời gian thực mà không cần đặt % cố định trước</td></tr></table>
      <div class="callout info"><div class="lbl">🔗 Liên hệ trực tiếp</div>Fair Scheduler chính là bài toán
      công bằng tài nguyên đã học ở <a href="../ll-07-drf/index.html">Lập lịch 07 — DRF</a> và
      <a href="../ll-06-cong-bang-tai-nguyen/index.html">Lập lịch 06 — progressive filling</a>: đây là lý
      thuyết max-min fairness được triển khai thực tế trong YARN, không phải khái niệm tách biệt.</div>"""),
    dict(h="Ví dụ minh hoạ: 2 job xin tài nguyên đồng thời", body="""
      <p>Giả sử cụm có tổng 20 Container trống. Job A (Spark) xin 12 Container, Job B (MapReduce) xin 10
      Container, nộp gần như cùng lúc.</p>
      <table><tr><th>Bước</th><th>ResourceManager làm gì</th></tr>
      <tr><td>1</td><td>ApplicationMaster của Job A và Job B đều gửi yêu cầu tài nguyên tới ResourceManager</td></tr>
      <tr><td>2</td><td>ResourceManager áp dụng chính sách lập lịch (Capacity Scheduler hoặc Fair Scheduler —
      xem lại liên hệ với buổi Lập lịch 06/07 công bằng tài nguyên) để chia 20 Container đang có</td></tr>
      <tr><td>3</td><td>Ví dụ dùng Fair Scheduler: Job A nhận 11 Container, Job B nhận 9 — không ai nhận đủ
      100% yêu cầu ngay, nhưng cả hai được cấp một phần công bằng và tiếp tục xin thêm khi có Container trống</td></tr></table>
      <div class="callout info"><div class="lbl">🔗 Liên hệ trực tiếp</div>Đây chính là bài toán công bằng tài
      nguyên đã học ở <a href="../ll-07-drf/index.html">Lập lịch 07 — DRF</a>: YARN Fair Scheduler/Capacity
      Scheduler là triển khai THỰC TẾ của đúng lý thuyết max-min fairness/DRF đó, không phải khái niệm tách
      biệt.</div>"""),
    dict(h="Ví dụ tính toán: 3 job xin tài nguyên qua Fair Scheduler (progressive filling)", body="""
      <p>Cụm có 30 Container. 3 job xin lần lượt: Job X=8, Job Y=14, Job Z=20 (tổng yêu cầu 42 &gt; 30).</p>
      <ol><li>Sắp theo yêu cầu tăng dần: X(8) &lt; Y(14) &lt; Z(20).</li>
      <li>Chia đều mức "trần" tăng dần: nếu chia đều 30/3=10 cho mỗi job, X chỉ cần 8 (dư 2) → dư 2 Container
      này dồn tiếp cho Y, Z.</li>
      <li>Còn 22 Container chia cho Y, Z: chia đều 22/2=11 — nhưng Y chỉ cần 14 (chưa đạt), Z cần 20 (chưa
      đạt) → cả 2 đều nhận 11.</li>
      <li>Vậy phân bổ cuối: X=8 (đủ), Y=11 (thiếu 3), Z=11 (thiếu 9) — tổng cấp = 8+11+11=30, đúng bằng tổng
      Container có.</li></ol>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Vì sao Job Z (yêu cầu nhiều nhất) lại
      KHÔNG được ưu tiên cấp nhiều hơn Job Y? (Đáp: progressive filling không ưu tiên theo "ai xin nhiều
      hơn" — nó tăng ĐỀU mức cấp cho mọi job đang thiếu, nên 2 job cùng chưa đạt nhu cầu (Y và Z) luôn nhận
      PHẦN TĂNG THÊM bằng nhau tại mỗi thời điểm, đúng nguyên lý max-min fairness.)</div>""")]),

  # ---------------- PHẦN 4 ----------------
  dict(title="Ảnh hưởng tới thế giới: từ YARN tới tư duy 'hệ điều hành cụm'", bullets=[
    "YARN mở đường cho Spark thay thế MapReduce làm engine xử lý chính (giữ nguyên lớp resource negotiation)",
    "Tư duy tách 'quản lý tài nguyên' khỏi 'logic ứng dụng' là tiền thân trực tiếp của Kubernetes"],
   slides=[
    dict(h="Từ YARN tới Kubernetes: cùng một ý tưởng, 10 năm sau", body="""
      <p>YARN ra đời năm 2012 để giải quyết đúng 1 bài toán: làm sao nhiều loại ứng dụng khác nhau có thể
      xin và được cấp tài nguyên (CPU/RAM) một cách công bằng trên cùng 1 cụm máy, mà không cần biết gì về
      logic nội bộ của ứng dụng khác.</p>
      <div class="callout good"><div class="lbl">🌍 Ảnh hưởng tới thế giới</div>Đây chính xác là bài toán mà
      <b>Kubernetes</b> (ra đời 2014 ở Google, dựa trên kinh nghiệm hệ thống nội bộ Borg) giải quyết cho toàn
      bộ ngành công nghiệp phần mềm nói chung, không chỉ Big Data: YARN là minh chứng sớm cho thấy việc tách
      lớp "cấp phát tài nguyên cụm" ra khỏi lớp "logic ứng dụng cụ thể" là một ý tưởng kiến trúc đúng đắn và
      bền vững — ý tưởng này lặp lại ở quy mô lớn hơn nhiều với Kubernetes ngày nay.</div>
      <table><tr><th></th><th>YARN (2012)</th><th>Kubernetes (2014)</th></tr>
      <tr><td>Lớp cấp tài nguyên</td><td>ResourceManager + NodeManager</td><td>kube-scheduler + kubelet</td></tr>
      <tr><td>Đơn vị cấp phát</td><td>Container (CPU/RAM)</td><td>Pod (1+ container Docker/OCI)</td></tr>
      <tr><td>"Người đại diện" cho từng ứng dụng</td><td>ApplicationMaster</td><td>Controller/Operator (khái niệm tương đồng, không giống 100%)</td></tr>
      <tr><td>Phạm vi ứng dụng</td><td>Chủ yếu xử lý dữ liệu lớn (Spark, Hive, MapReduce...)</td><td>Bất kỳ ứng dụng containerized nào</td></tr></table>
      <p>Hệ quả trực tiếp với Hadoop: nhờ YARN, khi Apache Spark ra đời và chứng minh xử lý in-memory nhanh
      hơn MapReduce rất nhiều lần cho các bài toán lặp (machine learning, graph), các công ty có thể CHUYỂN
      engine xử lý từ MapReduce sang Spark mà KHÔNG cần xây lại toàn bộ cụm — chỉ cần Spark biết "nói chuyện"
      với YARN. Đây là lý do MapReduce dần mất vai trò engine chính, nhưng YARN (ý tưởng resource negotiation)
      vẫn tồn tại.</p>""")])
 ],
 quiz=[
  dict(q="MapReduce tách biệt điều gì khỏi logic nghiệp vụ của người lập trình?", opts=[
     "Logic bảo mật", "Logic phân tán: chia việc, xử lý lỗi node, gộp kết quả", "Logic giao diện người dùng", "Logic cơ sở dữ liệu"],
   correct=1, explain="Người viết chỉ định nghĩa map/reduce; framework tự lo phân tán/chịu lỗi/gộp kết quả."),
  dict(q="Trong ví dụ 'đếm phiếu bầu' minh hoạ MapReduce, bước nào tương ứng với Shuffle?", opts=[
     "Mỗi phòng tự đếm phiếu của phòng mình", "Gửi riêng kết quả theo TỪNG ứng viên về người tổng hợp chuyên trách ứng viên đó",
     "Cộng tổng phiếu toàn quốc", "In phiếu bầu"],
   correct=1, explain="Shuffle gom dữ liệu theo đúng khoá (ở đây là 'ứng viên') lại một chỗ, không phải bước đếm hay bước tổng hợp cuối."),
  dict(q="Combiner trong MapReduce chỉ dùng đúng khi hàm reduce có tính chất gì?", opts=[
     "Không có điều kiện gì", "Kết hợp và giao hoán (associative, commutative)", "Chỉ dùng với số nguyên", "Chỉ dùng khi có 1 Reducer duy nhất"],
   correct=1, explain="Với trung bình (average) chẳng hạn, combiner ngây thơ cho kết quả sai nếu không gộp đúng (tổng + số lượng)."),
  dict(q="Văn bản 9.000 từ chia 3 Mapper (3.000 từ/Mapper, trung bình 500 từ khác nhau/Mapper). Combiner giảm lưu lượng shuffle khoảng bao nhiêu %?", opts=["25%", "50%", "83,3%", "100%"],
   correct=2, explain="Không combiner: 9.000 cặp gửi đi. Có combiner: 3×500=1.500 cặp. Giảm = (9.000-1.500)/9.000 ≈ 83,3%."),
  dict(q="Combiner giúp ÍT nhất trong trường hợp nào?", opts=[
     "Dữ liệu có rất nhiều từ lặp lại", "Dữ liệu gần như mỗi key chỉ xuất hiện 1 lần (vd danh sách mã khách hàng duy nhất)",
     "Số Mapper rất nhỏ", "Reducer chạy rất nhanh"],
   correct=1, explain="Nếu mỗi key chỉ xuất hiện 1 lần, Combiner không có gì để gộp — gần như không giảm được lưu lượng."),
  dict(q="Trong Hadoop 1.0, JobTracker đồng thời đảm nhiệm bao nhiêu vai trò khác nhau?", opts=[
     "1 vai trò duy nhất: theo dõi tiến trình", "2 vai trò: quản lý tài nguyên cụm VÀ theo dõi tiến trình mọi job",
     "3 vai trò gồm cả lưu trữ dữ liệu", "0, JobTracker chỉ chuyển tiếp thông điệp"],
   correct=1, explain="Gộp 2 vai trò khác nhau vào 1 node là nguyên nhân chính gây nghẽn và SPOF."),
  dict(q="Giới hạn thực tế của cụm Hadoop 1.0 (theo JobTracker) khoảng bao nhiêu node?", opts=["400 node", "~4.000 node", "40.000 node", "Không giới hạn"],
   correct=1, explain="Khoảng hơn 4.000 node và ~40.000 task đồng thời là giới hạn thực tế được ghi nhận."),
  dict(q="YARN viết tắt của gì, và ý nghĩa cái tên đó?", opts=[
     "Yet Another Resource Negotiator — một cái tên tự trào của nhóm phát triển", "Yarn Architecture for Resource Networks",
     "Young Allocation Resource Node", "Không viết tắt gì, chỉ là tên thương hiệu"],
   correct=0, explain="YARN = Yet Another Resource Negotiator, đặt tên có chủ đích hài hước vì đây là framework quản lý tài nguyên 'thêm một cái nữa'."),
  dict(q="ApplicationMaster trong YARN khác JobTracker cũ ở điểm cốt lõi nào?", opts=[
     "ApplicationMaster chạy trên máy nhanh hơn", "MỖI job có 1 ApplicationMaster riêng, thay vì dồn theo dõi mọi job vào 1 JobTracker",
     "ApplicationMaster không cần tài nguyên", "Không có khác biệt, chỉ đổi tên"],
   correct=1, explain="Đây là thay đổi kiến trúc cốt lõi: phân tán trách nhiệm theo dõi tiến trình ra từng job."),
  dict(q="Container trong YARN là gì?", opts=[
     "Một Docker container thật", "1 'gói' tài nguyên (vd CPU+RAM) được cấp cho 1 task cụ thể trong 1 khoảng thời gian",
     "Một ổ đĩa lưu trữ dữ liệu", "Một loại máy chủ vật lý riêng biệt"],
   correct=1, explain="Container KHÔNG phải Docker container — chỉ là đơn vị cấp phát tài nguyên logic trong YARN."),
  dict(q="Khác biệt chính giữa Capacity Scheduler và Fair Scheduler là gì?", opts=[
     "Không có khác biệt", "Capacity Scheduler chia theo % cố định cho từng hàng đợi/nhóm; Fair Scheduler chia công bằng động theo thời gian thực giữa các job đang chạy",
     "Fair Scheduler chỉ dùng được với 1 job", "Capacity Scheduler không hỗ trợ nhiều team"],
   correct=1, explain="Capacity Scheduler phù hợp khi cần đảm bảo mỗi team có tài nguyên tối thiểu cố định; Fair Scheduler phù hợp khi tải biến động, cần công bằng động."),
  dict(q="Nhờ YARN, điều gì trở nên khả thi mà Hadoop 1.0 không làm được?", opts=[
     "Lưu trữ dữ liệu lớn hơn", "Chạy nhiều loại ứng dụng khác nhau (Spark, Tez, MapReduce...) cùng lúc trên 1 cụm",
     "Tăng hệ số nhân bản HDFS", "Giảm kích thước block"],
   correct=1, explain="Trước YARN, cụm Hadoop chỉ chạy được MapReduce; YARN biến Hadoop thành nền tảng đa ứng dụng."),
  dict(q="YARN ra đời vào năm nào, cùng với phiên bản Hadoop nào?", opts=["2008, Hadoop 1.0", "2010, Hadoop 1.5", "2012, Hadoop 2.0", "2015, Hadoop 3.0"],
   correct=2, explain="YARN được đưa ra từ Hadoop 2.0, năm 2012."),
  dict(q="Trong ví dụ 3 job (X=8, Y=14, Z=20) xin tổng cộng 42 Container trên cụm chỉ có 30, kết quả Fair Scheduler (progressive filling) cấp cho mỗi job là bao nhiêu?", opts=[
     "X=8, Y=11, Z=11", "X=14, Y=8, Z=8", "X=10, Y=10, Z=10", "X=0, Y=0, Z=30"],
   correct=0, explain="X đạt đủ 8 (dư để dồn cho Y,Z); 22 Container còn lại chia đều cho Y,Z (cả 2 đều chưa đạt nhu cầu) → mỗi job 11."),
  dict(q="Vì sao Job Z (yêu cầu nhiều nhất, 20 Container) không được ưu tiên cấp nhiều hơn Job Y trong ví dụ trên?", opts=[
     "Vì Z nộp yêu cầu sau", "Vì progressive filling tăng đều mức cấp cho mọi job đang thiếu, không ưu tiên theo mức yêu cầu", "Vì Z có lỗi", "Vì ResourceManager ưu tiên job nhỏ"],
   correct=1, explain="Đúng nguyên lý max-min fairness: hai job cùng chưa đạt nhu cầu luôn nhận phần tăng thêm bằng nhau."),
  dict(q="Trong ví dụ 2 job xin 12 và 10 Container trên cụm chỉ có 20 Container trống, Fair Scheduler làm gì?", opts=[
     "Chỉ cấp cho job nộp trước, job sau phải chờ", "Chia một phần công bằng cho cả hai, không ai nhận đủ 100% ngay lập tức",
     "Từ chối cả hai yêu cầu", "Tạo thêm Container mới ngay lập tức"],
   correct=1, explain="Fair Scheduler chia sẻ công bằng tài nguyên hiện có, đúng nguyên lý max-min fairness đã học ở module Lập lịch 06/07."),
  dict(q="Ý tưởng kiến trúc nào của YARN lặp lại ở quy mô lớn hơn trong Kubernetes?", opts=[
     "Lưu trữ phân tán có nhân bản", "Tách lớp cấp phát tài nguyên cụm khỏi lớp logic ứng dụng cụ thể",
     "Ngôn ngữ lập trình Java", "Mô hình key-value"],
   correct=1, explain="Kubernetes (2014, dựa trên Borg của Google) áp dụng đúng ý tưởng này cho toàn ngành phần mềm, không chỉ Big Data."),
  dict(q="Trong bảng so sánh YARN/Kubernetes, 'Pod' của Kubernetes tương ứng gần nhất với khái niệm nào của YARN?", opts=["ResourceManager", "NodeManager", "Container", "ApplicationMaster"],
   correct=2, explain="Cả Container (YARN) và Pod (Kubernetes) đều là đơn vị cấp phát tài nguyên cho 1 đơn vị công việc/ứng dụng chạy trên cụm."),
  dict(q="Vì sao Spark có thể dần thay thế MapReduce làm engine xử lý chính mà không cần xây lại cụm?", opts=[
     "Vì Spark không cần tài nguyên", "Vì Spark nói chuyện với YARN giống MapReduce, chỉ thay đổi engine xử lý phía trên lớp resource negotiation",
     "Vì Spark lưu trữ dữ liệu khác HDFS hoàn toàn", "Vì Spark không chạy trên cụm Hadoop được"],
   correct=1, explain="YARN tách biệt resource negotiation khỏi engine xử lý — đây là lý do engine có thể thay đổi (MapReduce → Spark) mà hạ tầng cấp tài nguyên giữ nguyên."),
  dict(q="Partitioner mặc định trong MapReduce dùng cơ chế gì để chọn Reducer cho 1 key?", opts=[
     "Ngẫu nhiên hoàn toàn", "hash(key) mod số-Reducer", "Theo thứ tự xuất hiện trong file", "Theo kích thước giá trị"],
   correct=1, explain="hash(key) mod R đảm bảo mọi value của cùng 1 key luôn vào đúng 1 Reducer duy nhất."),
 ])
