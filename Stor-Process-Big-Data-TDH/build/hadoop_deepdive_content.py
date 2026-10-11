# -*- coding: utf-8 -*-
"""Module tự học SÂU "Hệ sinh thái Hadoop" (Chương 2, IT4931_lecture_notes.pdf, tr.23-36) — tách biệt
hoàn toàn khỏi group-1-slides.html (không sửa file đó). Mục tiêu: không lặp lại nguyên văn Chương 2,
mà đi sâu vào lịch sử ra đời thật, động lực nghiệp vụ, và ảnh hưởng tới thế giới của từng công nghệ —
dành riêng cho nhóm tự học (Trao đổi.md: "nửa sau đúng không hiểu gì").

Nguồn:
  - Nội dung kỹ thuật cốt lõi: materials/hangout/2024/2_hadoop_ecosystem_vn.pdf (Chương 2 gốc) +
    IT4931_lecture_notes.pdf tr.23-36 (đã host sẵn trong repo từ trước, có tiền lệ).
  - Paper gốc trong materials/papers/ (Garg 2013 "Apache Kafka", Decandia et al. 2007 Dynamo) — chỉ
    trích dẫn bibliographic, KHÔNG copy file có bản quyền vào git repo.
  - Lịch sử/động lực/ảnh hưởng: xác nhận qua web search ngày 2026-10-11, mỗi fact có URL nguồn trong
    callout "📚 Nguồn lịch sử" — không suy đoán năm/tên người nếu chưa xác nhận được.
"""

HADOOP_MODULES = [
# ---------------------------------------------------------------- 25
dict(n=25, slug="hd-01-hadoop-hdfs", title="Vì sao Hadoop ra đời, và HDFS giải quyết bài toán gì",
 tag="Lịch sử Hadoop · Kiến trúc HDFS",
 intro="Hadoop không phải một sản phẩm được thiết kế trong phòng họp — nó ra đời từ nhu cầu rất cụ thể của một công cụ tìm kiếm mã nguồn mở đang chết dần vì không mở rộng được.",
 parts=[
  dict(title="Từ Nutch tới Hadoop: một câu chuyện có thật", bullets=[
    "2002: Doug Cutting & Mike Cafarella xây Nutch — công cụ tìm kiếm mở, nhưng kiến trúc không scale",
    "2003-2004: hai bài báo của Google (GFS, MapReduce) chỉ ra lối ra",
    "2006: Cutting vào Yahoo, phần lưu trữ+xử lý của Nutch được tách ra, đặt tên Hadoop"],
   slides=[
    dict(h="Nutch: công cụ tìm kiếm sinh ra Hadoop", body="""
      <p>Trước khi có Hadoop, Doug Cutting và Mike Cafarella đã xây <b>Apache Nutch</b> (2002) — một công cụ
      tìm kiếm web mã nguồn mở. Vấn đề: muốn thu thập và đánh chỉ mục cả Internet, Nutch cần lưu trữ và xử lý
      dữ liệu ở quy mô vượt xa khả năng một máy chủ, nhưng chưa có kiến trúc phân tán phù hợp.</p>
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>Doug Cutting và Mike Cafarella hình thành
      ý tưởng Hadoop dựa trên bài báo <i>Google File System</i> (tháng 10/2003); phát triển ban đầu nằm trong
      dự án Apache Nutch, rồi tách sang dự án con Hadoop vào tháng 1/2006.
      Nguồn: <a href="https://en.wikipedia.org/wiki/Apache_Hadoop" target="_blank">Apache Hadoop — Wikipedia</a>,
      <a href="https://informationweek.com/software-services/hadoop-at-10-doug-cutting-on-making-big-data-work" target="_blank">InformationWeek — Hadoop at 10</a>.</div>
      <p>Đây là chi tiết quan trọng để hiểu <b>vì sao</b> Hadoop có 2 trụ cột tách biệt (lưu trữ HDFS + xử lý
      MapReduce) — vì chính 2 bài báo Google mà Cutting/Cafarella đọc cũng tách biệt 2 vấn đề đó.</p>"""),
    dict(h="Vì sao tên là \"Hadoop\"?", body="""
      <p>Không phải một từ viết tắt kỹ thuật nào cả.</p>
      <div class="callout good"><div class="lbl">📚 Nguồn lịch sử</div>Doug Cutting (khi đó làm ở Yahoo!) đặt
      tên Hadoop theo <b>tên con voi nhồi bông</b> của con trai ông. Theo lời Cutting: "Cái tên con tôi đặt cho
      một con voi nhồi bông màu vàng. Ngắn, dễ đánh vần, dễ đọc, vô nghĩa, và chưa ai dùng — đó là tiêu chí đặt
      tên của tôi." Con voi này giờ "nghỉ hưu" trong tủ đồ của Cutting, chỉ được mang ra trong các buổi keynote.
      Nguồn: <a href="https://www.cio.com/article/3027631/apache-hadoop-turns-10.html" target="_blank">CIO.com — Apache Hadoop turns 10</a>.</div>
      <p>Chi tiết này không phải giai thoại vô bổ: nó cho thấy văn hoá đặt tên "ngắn - dễ nhớ - không gây hiểu
      lầm về công nghệ" của cả hệ sinh thái Hadoop sau này (Pig, Hive, ZooKeeper, Oozie, Sqoop... đều là tên
      vật/khái niệm đời thường, không phải từ viết tắt).</p>""")]),
  dict(title="Kiến trúc HDFS: Master/Slave", bullets=[
    "NameNode quản lý namespace & metadata, DataNode lưu dữ liệu thật",
    "Tệp chia thành block lớn (64MB/128MB) để giảm chi phí quản lý metadata",
    "Mỗi block nhân bản 3 lần trên các DataNode khác nhau để chịu lỗi"],
   slides=[
    dict(h="NameNode & DataNode: ai làm gì?", body="""
      <p>HDFS theo kiến trúc <b>Master/Slave</b>: <b>NameNode</b> (master) chỉ lưu <i>metadata</i> — cấu trúc
      thư mục, tên tệp, và bảng ánh xạ tệp → vị trí các block trên DataNode nào. <b>DataNode</b> (slave) mới
      là nơi lưu dữ liệu thật và trực tiếp phục vụ đọc/ghi.</p>
      <ul class="pd-legend"><li><b>fsimage</b><span>ảnh chụp toàn bộ namespace tại một thời điểm</span></li>
      <li><b>edit log</b><span>nhật ký các thay đổi từ sau fsimage gần nhất — NameNode phát lại log này khi
      khởi động để khôi phục trạng thái mới nhất</span></li></ul>
      <div class="callout warn"><div class="lbl">Vì sao đây là điểm yếu kiến trúc ban đầu</div>Vì toàn bộ
      metadata chỉ nằm ở 1 NameNode, nên bản Hadoop 1.0 có 1 <b>Single Point of Failure</b>: NameNode hỏng là
      cả cụm mất khả năng định vị dữ liệu, dù dữ liệu vật lý trên DataNode vẫn còn nguyên. Hadoop 2.0 sau này
      giải quyết bằng Standby NameNode (High Availability) — khác với Secondary NameNode (chỉ gộp log, không
      phải bản dự phòng nóng).</div>"""),
    dict(h="Block & Replication: hai quyết định thiết kế cốt lõi", body="""
      <p>Hai lựa chọn thiết kế này quyết định toàn bộ hiệu năng và độ tin cậy của HDFS:</p>
      <div class="pd-formula"><div class="pd-formula-label">Kích thước block mặc định</div>
      <div class="pd-formula-math">64\\text{ MB (ban đầu)} \\to 128\\text{ MB (mặc định từ các bản sau)}</div></div>
      <div class="pd-formula"><div class="pd-formula-label">Hệ số nhân bản mặc định</div>
      <div class="pd-formula-math">3\\text{ bản sao, đặt trên 3 DataNode khác nhau (thường khác rack)}</div></div>
      <div class="callout info"><div class="lbl">Vì sao block lớn, không nhỏ như hệ file thường (4KB)</div>
      Block lớn giảm số lượng entry metadata mà NameNode phải giữ trong RAM — đây là lý do HDFS tối ưu cho
      "vài trăm MB đến vài TB" một tệp, không phải cho rất nhiều tệp nhỏ: nhiều tệp nhỏ sẽ làm phình metadata
      và trở thành nút nghẽn bộ nhớ của NameNode (bài toán "small files problem" nổi tiếng của HDFS).</div>""")]),
  dict(title="Ví dụ minh hoạ: ghi một tệp 300MB vào HDFS", bullets=[
    "Tệp 300MB với block 128MB → 3 block (128+128+44)",
    "Mỗi block có 3 bản sao → tổng 9 lượt ghi vật lý trên các DataNode",
    "Mô phỏng: 1 DataNode hỏng → NameNode phát hiện, ra lệnh tái nhân bản"],
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
    dict(h="Khi một DataNode hỏng giữa đường", body="""
      <p>Giả sử sau khi ghi xong, <b>DN5</b> (đang giữ 1 bản sao của block B1) gặp lỗi phần cứng.</p>
      <ol><li>DataNode gửi <i>heartbeat</i> định kỳ cho NameNode; khi NameNode không nhận heartbeat từ DN5
      trong một khoảng thời gian, nó coi DN5 đã chết.</li>
      <li>NameNode rà soát metadata: block B1 hiện chỉ còn 2 bản sao hợp lệ (trên DN2, DN7) — thiếu 1 so với
      hệ số nhân bản mặc định 3.</li>
      <li>NameNode ra lệnh cho DN2 (hoặc DN7) sao chép thêm 1 bản của B1 sang một DataNode còn sống khác,
      khôi phục lại đủ 3 bản sao — toàn bộ quá trình này KHÔNG cần ứng dụng phía trên biết hay can thiệp.</li></ol>
      <div class="callout warn"><div class="lbl">Điểm mấu chốt cần nhớ</div>HDFS không "ngăn" lỗi phần cứng
      xảy ra — nó <b>giả định lỗi là bình thường</b> và xây cơ chế tự phục hồi xung quanh giả định đó. Đây
      chính là tư duy "chịu lỗi qua dư thừa" khác hẳn triết lý RDBMS truyền thống (ngăn lỗi bằng phần cứng đắt,
      RAID chuyên dụng).</div>""")]),
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
      hỗ trợ doanh nghiệp triển khai Hadoop, cho thấy quy mô ảnh hưởng kinh tế thực sự của công nghệ này.</p>""")])
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
  dict(q="Trong kiến trúc HDFS, NameNode chịu trách nhiệm chính về điều gì?", opts=[
     "Lưu toàn bộ dữ liệu thật của mọi tệp", "Lưu metadata: namespace, ánh xạ tệp → block → DataNode",
     "Chạy các tác vụ MapReduce", "Nhân bản vật lý từng block"],
   correct=1, explain="NameNode chỉ giữ metadata (fsimage + edit log); dữ liệu thật và việc nhân bản do DataNode xử lý."),
  dict(q="Vì sao Hadoop 1.0 coi NameNode là một Single Point of Failure?", opts=[
     "Vì NameNode chạy chậm hơn DataNode", "Vì mọi metadata chỉ tồn tại ở 1 NameNode, hỏng là mất khả năng định vị dữ liệu",
     "Vì NameNode không hỗ trợ nhân bản", "Vì NameNode cần GPU"],
   correct=1, explain="Dữ liệu vật lý trên DataNode vẫn còn, nhưng không ai biết nó ở đâu nếu NameNode (và metadata) hỏng — đây là động lực ra đời Standby NameNode (HA) ở Hadoop 2.0."),
  dict(q="Block size lớn (64MB/128MB) trong HDFS giúp giải quyết vấn đề gì?", opts=[
     "Tăng độ trễ đọc/ghi", "Giảm số lượng entry metadata mà NameNode phải lưu trong RAM",
     "Giảm hệ số nhân bản cần thiết", "Tăng số lượng tệp nhỏ có thể lưu hiệu quả"],
   correct=1, explain="Block lớn → ít block hơn cho cùng dung lượng dữ liệu → ít metadata hơn trên NameNode. Hệ quả phụ: HDFS KÉM hiệu quả với rất nhiều tệp nhỏ (small-files problem)."),
  dict(q="Một tệp 300MB với block size 128MB được chia thành mấy block?", opts=["2 block", "3 block (128+128+44)", "4 block", "300 block"],
   correct=1, explain="⌈300/128⌉ = 3 block: hai block đầy 128MB, block cuối 44MB."),
  dict(q="Với tệp 300MB chia 3 block, hệ số nhân bản 3, tổng số lượt ghi vật lý trên các DataNode là bao nhiêu?", opts=["3", "6", "9", "12"],
   correct=2, explain="3 block × 3 bản sao/block = 9 lượt ghi vật lý."),
  dict(q="Khi một DataNode giữ bản sao của 1 block bị lỗi, hệ thống phản ứng ra sao?", opts=[
     "Toàn bộ tệp bị xoá để đảm bảo nhất quán", "NameNode phát hiện qua heartbeat và ra lệnh tái nhân bản sang DataNode khác",
     "Client phải tự ghi lại toàn bộ tệp", "Không có cơ chế tự động, cần quản trị viên can thiệp thủ công"],
   correct=1, explain="Cơ chế heartbeat + tái nhân bản tự động là nền tảng của khả năng chịu lỗi HDFS, không cần ứng dụng hay người quản trị can thiệp."),
  dict(q="Hadoop trở thành dự án Apache cấp cao nhất (top-level project) vào năm nào?", opts=["2004", "2006", "2008", "2012"],
   correct=2, explain="2006 là năm Hadoop tách thành dự án con từ Nutch; 2008 mới là năm trở thành top-level Apache project."),
  dict(q="Hai công ty thương mại lớn nhất xây quanh hệ sinh thái Hadoop là gì?", opts=[
     "Confluent và Databricks", "Cloudera và Hortonworks", "MongoDB Inc. và Snowflake", "Oracle và IBM"],
   correct=1, explain="Cloudera (2008) và Hortonworks (2011) — hai công ty này sau sáp nhập lại năm 2019."),
  dict(q="Triết lý 'scale-out, lưu trước xử lý sau' của Hadoop ảnh hưởng trực tiếp tới kiến trúc nào phổ biến hiện nay?", opts=[
     "Máy chủ mainframe tập trung", "Data lake/lakehouse trên cloud (S3+EMR, Delta Lake, Iceberg)",
     "Cơ sở dữ liệu quan hệ truyền thống on-premise duy nhất", "Không có ảnh hưởng gì tới kiến trúc hiện đại"],
   correct=1, explain="HDFS được thay bằng object storage (S3/GCS/ADLS) nhưng tư duy lưu trữ rẻ + mở rộng ngang vẫn là nền tảng của data lake/lakehouse ngày nay."),
  dict(q="Secondary NameNode trong Hadoop 1.0 khác gì so với Standby NameNode (HA) của Hadoop 2.0?", opts=[
     "Chúng là một, chỉ đổi tên", "Secondary NameNode chỉ gộp fsimage+edit log định kỳ, KHÔNG phải bản dự phòng nóng; Standby NameNode mới thực sự có thể thay thế NameNode chính khi lỗi",
     "Secondary NameNode nhanh hơn Standby NameNode", "Standby NameNode chỉ dùng để lưu dữ liệu, không liên quan metadata"],
   correct=1, explain="Đây là nhầm lẫn phổ biến nhất về HDFS: Secondary NameNode KHÔNG phải cơ chế failover."),
 ]),

# ---------------------------------------------------------------- 26
dict(n=26, slug="hd-02-mapreduce-yarn", title="MapReduce & YARN: từ mô hình lập trình tới hệ điều hành cụm",
 tag="Lịch sử MapReduce · Vì sao YARN ra đời",
 intro="MapReduce giải quyết bài toán xử lý; nhưng chính MapReduce bản đầu lại tạo ra một điểm nghẽn mới — JobTracker. Câu chuyện YARN là câu chuyện sửa lỗi kiến trúc của chính Hadoop.",
 parts=[
  dict(title="MapReduce: mô hình lập trình từ Google", bullets=[
    "Google công bố MapReduce năm 2004 (Dean & Ghemawat)", "Mô hình: Map → Shuffle & Sort → Reduce trên cặp key-value",
    "Ưu điểm được thiết kế có chủ đích: đơn giản, linh hoạt, khả mở"],
   slides=[
    dict(h="Vì sao Google cần MapReduce?", body="""
      <p>Trước MapReduce, kỹ sư Google phải tự viết code xử lý song song/phân tán cho từng bài toán — dễ lỗi,
      khó bảo trì, logic phân tán (chia việc, xử lý lỗi node, gộp kết quả) trộn lẫn với logic nghiệp vụ.
      MapReduce tách 2 phần này: người viết code chỉ cần định nghĩa 2 hàm <code>map</code> và <code>reduce</code>,
      còn framework tự lo phân tán, chịu lỗi, gộp kết quả.</p>
      <table><tr><th>Giai đoạn</th><th>Việc làm</th></tr>
      <tr><td>Map</td><td>Đọc từng bản ghi đầu vào (key, value), sinh ra 0 hoặc nhiều cặp (key', value') trung gian</td></tr>
      <tr><td>Shuffle &amp; Sort</td><td>Hadoop tự gộp và sắp xếp output của mọi Mapper theo key', chia vào các partition — mỗi partition là đầu vào của 1 Reducer</td></tr>
      <tr><td>Reduce</td><td>Mỗi Reducer nhận toàn bộ value' của 1 key', xử lý và sinh ra cặp (key'', value'') cuối cùng</td></tr></table>
      <div class="callout info"><div class="lbl">Nguồn: materials/hangout/2024/2_hadoop_ecosystem_vn.pdf (Chương 2)</div>
      Ví dụ Word Count trong giáo trình chính là minh hoạ kinh điển nhất của mô hình này: Map phát ra (từ, 1)
      cho mỗi từ, Reduce cộng tổng các giá trị 1 theo từng từ khoá.</div>"""),
    dict(h="Combiner & Partitioner — chi tiết hay bị bỏ qua", body="""
      <p>Giáo trình gốc không nhấn vào 2 thành phần tối ưu quan trọng này — nhưng thiếu chúng, MapReduce thực
      tế sẽ chậm hơn rất nhiều so với lý thuyết:</p>
      <ul class="pd-legend"><li><b>Combiner</b><span>một "mini-Reducer" chạy ngay trên node Map, gộp trước
      các giá trị cùng key TRƯỚC khi gửi qua mạng tới Reducer — giảm mạnh lưu lượng shuffle. Với Word Count,
      combiner cộng tổng từng từ ngay tại Mapper trước khi gửi đi.</span></li>
      <li><b>Partitioner</b><span>quyết định cặp (key', value') trung gian nào đi vào Reducer nào — mặc định
      dùng hash(key) mod số-Reducer, đảm bảo mọi value' của cùng 1 key' luôn vào đúng 1 Reducer duy nhất.</span></li></ul>
      <div class="callout warn"><div class="lbl">Bẫy hay gặp</div>Combiner chỉ áp dụng được khi hàm reduce có
      tính <b>kết hợp và giao hoán</b> (associative, commutative) — như cộng tổng, lấy max/min. Với phép tính
      trung bình (average), combiner ngây thơ sẽ cho kết quả SAI nếu không cẩn thận (phải gộp cả tổng và số
      lượng, không gộp trực tiếp giá trị trung bình).</div>""")]),
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
      1 JobTracker).</p>""")]),
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
      <div class="callout good"><div class="lbl">Vì sao đây là bước nhảy kiến trúc, không chỉ bản vá lỗi</div>
      YARN biến Hadoop từ "một hệ thống chỉ chạy được MapReduce" thành "một hệ điều hành cấp tài nguyên cho
      NHIỀU loại ứng dụng khác nhau cùng lúc" — đây là lý do Spark, Tez, Flink đều có thể chạy trên cùng 1 cụm
      Hadoop với YARN làm lớp cấp phát tài nguyên bên dưới.</div>"""),
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
      biệt.</div>""")]),
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
  dict(q="Combiner trong MapReduce chỉ dùng đúng khi hàm reduce có tính chất gì?", opts=[
     "Không có điều kiện gì", "Kết hợp và giao hoán (associative, commutative)", "Chỉ dùng với số nguyên", "Chỉ dùng khi có 1 Reducer duy nhất"],
   correct=1, explain="Với trung bình (average) chẳng hạn, combiner ngây thơ cho kết quả sai nếu không gộp đúng (tổng + số lượng)."),
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
  dict(q="Nhờ YARN, điều gì trở nên khả thi mà Hadoop 1.0 không làm được?", opts=[
     "Lưu trữ dữ liệu lớn hơn", "Chạy nhiều loại ứng dụng khác nhau (Spark, Tez, MapReduce...) cùng lúc trên 1 cụm",
     "Tăng hệ số nhân bản HDFS", "Giảm kích thước block"],
   correct=1, explain="Trước YARN, cụm Hadoop chỉ chạy được MapReduce; YARN biến Hadoop thành nền tảng đa ứng dụng."),
  dict(q="YARN ra đời vào năm nào, cùng với phiên bản Hadoop nào?", opts=["2008, Hadoop 1.0", "2010, Hadoop 1.5", "2012, Hadoop 2.0", "2015, Hadoop 3.0"],
   correct=2, explain="YARN được đưa ra từ Hadoop 2.0, năm 2012."),
  dict(q="Trong ví dụ 2 job xin 12 và 10 Container trên cụm chỉ có 20 Container trống, Fair Scheduler làm gì?", opts=[
     "Chỉ cấp cho job nộp trước, job sau phải chờ", "Chia một phần công bằng cho cả hai, không ai nhận đủ 100% ngay lập tức",
     "Từ chối cả hai yêu cầu", "Tạo thêm Container mới ngay lập tức"],
   correct=1, explain="Fair Scheduler chia sẻ công bằng tài nguyên hiện có, đúng nguyên lý max-min fairness đã học ở module Lập lịch 06/07."),
  dict(q="Ý tưởng kiến trúc nào của YARN lặp lại ở quy mô lớn hơn trong Kubernetes?", opts=[
     "Lưu trữ phân tán có nhân bản", "Tách lớp cấp phát tài nguyên cụm khỏi lớp logic ứng dụng cụ thể",
     "Ngôn ngữ lập trình Java", "Mô hình key-value"],
   correct=1, explain="Kubernetes (2014, dựa trên Borg của Google) áp dụng đúng ý tưởng này cho toàn ngành phần mềm, không chỉ Big Data."),
  dict(q="Vì sao Spark có thể dần thay thế MapReduce làm engine xử lý chính mà không cần xây lại cụm?", opts=[
     "Vì Spark không cần tài nguyên", "Vì Spark nói chuyện với YARN giống MapReduce, chỉ thay đổi engine xử lý phía trên lớp resource negotiation",
     "Vì Spark lưu trữ dữ liệu khác HDFS hoàn toàn", "Vì Spark không chạy trên cụm Hadoop được"],
   correct=1, explain="YARN tách biệt resource negotiation khỏi engine xử lý — đây là lý do engine có thể thay đổi (MapReduce → Spark) mà hạ tầng cấp tài nguyên giữ nguyên."),
  dict(q="Partitioner mặc định trong MapReduce dùng cơ chế gì để chọn Reducer cho 1 key?", opts=[
     "Ngẫu nhiên hoàn toàn", "hash(key) mod số-Reducer", "Theo thứ tự xuất hiện trong file", "Theo kích thước giá trị"],
   correct=1, explain="hash(key) mod R đảm bảo mọi value của cùng 1 key luôn vào đúng 1 Reducer duy nhất."),
 ]),

# ---------------------------------------------------------------- 27
dict(n=27, slug="hd-03-pig-hive", title="Pig & Hive: hai cách khác nhau để \"thoát\" khỏi việc viết MapReduce tay",
 tag="Lịch sử Pig (Yahoo) & Hive (Facebook)",
 intro="Cùng giải quyết một vấn đề — viết MapReduce bằng Java quá cực — nhưng Yahoo và Facebook chọn hai triết lý ngôn ngữ hoàn toàn khác nhau. Hive thắng về lâu dài, nhưng không phải vì HiveQL.",
 parts=[
  dict(title="Apache Pig: dataflow procedural từ Yahoo Research", bullets=[
    "Ra đời ở Yahoo Research khoảng 2006, mã nguồn mở hoá 2007, bản phát hành đầu tiên 9/2008",
    "PigLatin: ngôn ngữ nằm giữa SQL (khai báo) và MapReduce thuần (thủ tục)",
    "Trình biên dịch Pig chạy trên máy client, dịch PigLatin script thành chuỗi MapReduce job"],
   slides=[
    dict(h="Vì sao Yahoo cần một ngôn ngữ \"ở giữa\"?", body="""
      <p>Các nhà nghiên cứu ở Yahoo nhận ra 2 cực đoan đều có vấn đề: viết MapReduce tay bằng Java quá chi
      tiết, khó tái dùng, khó bảo trì; nhưng SQL khai báo thuần lại không đủ linh hoạt cho các luồng xử lý dữ
      liệu phức tạp, nhiều bước biến đổi tuần tự.</p>
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>Apache Pig được phát triển tại Yahoo
      Research khoảng năm 2006, với mục tiêu cho các nhà nghiên cứu một cách tuỳ biến (ad hoc) để tạo và chạy
      MapReduce job trên tập dữ liệu rất lớn. PigLatin được thiết kế để nằm ở "điểm ngọt" giữa phong cách khai
      báo của SQL và phong cách thủ tục cấp thấp của MapReduce. Mã nguồn mở hoá qua Apache Incubator mùa thu
      2007, bản phát hành đầu tiên tháng 9/2008.
      Nguồn: <a href="https://en.wikipedia.org/wiki/Apache_Pig" target="_blank">Apache Pig — Wikipedia</a>.</div>
      <p>Pig đặc biệt mạnh ở các phép toán <b>Join</b> và <b>Transformation</b> nhiều bước — vì PigLatin là
      <i>procedural dataflow</i> (bạn viết từng bước biến đổi tuần tự, giống một pipeline), không phải khai
      báo "muốn gì" như SQL.</p>""")]),
  dict(title="Apache Hive: SQL-on-Hadoop từ Facebook", bullets=[
    "Ra đời ở Facebook (Joydeep Sen Sarma & Ashish Thusoo), release đầu tiên 10/2010",
    "Động lực: dữ liệu Facebook tăng từ 10 GB/ngày lên 15 TB/ngày trong vài năm",
    "HiveQL: để kỹ sư/analyst vốn chỉ biết SQL cũng khai thác được Hadoop, không cần biết Java/MapReduce"],
   slides=[
    dict(h="Từ 6 người dùng tới 20-30% toàn công ty", body="""
      <div class="callout good"><div class="lbl">📚 Nguồn lịch sử</div>Khi Facebook bắt đầu đưa dữ liệu vào
      Hadoop năm 2006, lượng dữ liệu nhập vào khoảng vài chục GB/ngày, và tăng lên khoảng 15 TB/ngày chỉ sau
      vài năm. Những người tạo ra Hive nhận ra: để khai thác tốt Hadoop, kỹ sư phải viết MapReduce Java phức
      tạp — không thể dạy kỹ năng này cho toàn bộ team kỹ sư và phân tích đang tăng nhanh. Khi 15 petabyte đã
      nằm trong data warehouse, chỉ có 6 người dùng dữ liệu đó; tới khi Thusoo rời Facebook năm 2011, 20-30%
      toàn công ty truy cập hạ tầng phân tích dữ liệu mỗi tháng.
      Nguồn: <a href="https://celerdata.com/glossary/apache-hive" target="_blank">CelerData — What is Apache Hive?</a>,
      <a href="https://www.nextplatform.com/2015/06/17/co-creator-of-hive-brings-facebook-lessons-to-analytics-platform" target="_blank">The Next Platform</a>.</div>
      <p>Đây là con số ấn tượng nhất của toàn bộ hệ sinh thái Hadoop: Hive không chỉ là một công cụ kỹ thuật,
      mà là công cụ <b>dân chủ hoá dữ liệu</b> trong một tổ chức — biến "dữ liệu lớn" từ thứ chỉ vài chuyên gia
      động được, thành thứ cả công ty dùng hàng ngày, chỉ bằng SQL quen thuộc.</p>"""),
    dict(h="HiveQL hoạt động ra sao?", body="""
      <p>Giống Pig, trình biên dịch Hive chạy trên máy client: chuyển HiveQL script thành MapReduce job, rồi
      đệ trình lên cụm. Khác Pig, HiveQL là ngôn ngữ <b>khai báo</b> giống SQL — người dùng chỉ nói "tôi muốn
      kết quả gì" (SELECT ... GROUP BY ...), không cần viết từng bước biến đổi.</p>
      <table><tr><th>Tiêu chí</th><th>Pig (PigLatin)</th><th>Hive (HiveQL)</th></tr>
      <tr><td>Phong cách</td><td>Thủ tục (procedural dataflow)</td><td>Khai báo (declarative, giống SQL)</td></tr>
      <tr><td>Đối tượng dùng chính</td><td>Nhà nghiên cứu/kỹ sư dữ liệu viết pipeline nhiều bước</td><td>Analyst/kỹ sư quen SQL, cần truy vấn data warehouse</td></tr>
      <tr><td>Thế mạnh</td><td>Join &amp; Transformation phức tạp, nhiều bước tuần tự rõ ràng</td><td>Truy vấn tổng hợp, báo cáo kiểu data-warehouse</td></tr></table>""")]),
  dict(title="Ví dụ minh hoạ: cùng 1 bài toán, 2 cách viết", bullets=[
    "Bài toán: tổng doanh số theo từng nhân viên (giống ví dụ MapReduce ở Chương 2 gốc)",
    "PigLatin: LOAD → GROUP BY → FOREACH ... GENERATE SUM(...)",
    "HiveQL: SELECT employee, SUM(sale) FROM orders GROUP BY employee"],
   slides=[
    dict(h="Từ bài toán gốc tới 2 đoạn script", body="""
      <p>Nhắc lại bài toán ở Chương 2 gốc: đầu vào là tệp văn bản chứa (order ID, employee name, sale amount),
      đầu ra là tổng doanh số theo từng nhân viên — đúng bài toán MapReduce group-by-aggregate kinh điển.</p>
      <div class="pd-formula"><div class="pd-formula-label">PigLatin (thủ tục, từng bước)</div>
      <div class="pd-formula-math">\\text{orders = LOAD 'orders.csv'; grouped = GROUP orders BY employee; result = FOREACH grouped GENERATE group, SUM(orders.sale);}</div></div>
      <div class="pd-formula"><div class="pd-formula-label">HiveQL (khai báo, 1 câu)</div>
      <div class="pd-formula-math">\\text{SELECT employee, SUM(sale) FROM orders GROUP BY employee;}</div></div>
      <div class="callout warn"><div class="lbl">Điều cả hai đều giống nhau phía dưới</div>Dù cú pháp khác hẳn
      nhau, CẢ HAI đều được trình biên dịch dịch thành cùng 1 dạng MapReduce job bên dưới: bước Map đọc từng
      dòng và phát ra (employee, sale); bước Shuffle&amp;Sort gộp theo employee; bước Reduce cộng tổng — đúng
      luồng dữ liệu đã học ở Chương 2 gốc. Pig/Hive không thay đổi MapReduce, chỉ thay đổi CÁCH VIẾT để tạo ra
      nó.</div>""")]),
  dict(title="Ảnh hưởng tới thế giới: di sản lớn nhất của Hive không phải HiveQL", bullets=[
    "Hive Metastore trở thành chuẩn de-facto lưu schema bảng cho cả hệ sinh thái sau này",
    "Presto, Spark SQL, Trino ngày nay vẫn tương thích/đọc được Hive Metastore"],
   slides=[
    dict(h="Hive Metastore: di sản bền lâu hơn cả HiveQL", body="""
      <p>HiveQL ngày nay phần lớn bị thay thế bởi Spark SQL hoặc Presto/Trino khi cần hiệu năng truy vấn tương
      tác cao hơn (Hive thế hệ đầu chạy trên MapReduce nên có độ trễ cao, tối ưu cho batch chứ không phải truy
      vấn nhanh). Nhưng có một phần của Hive hầu như công cụ nào sau này cũng phải tương thích:</p>
      <div class="callout good"><div class="lbl">🌍 Ảnh hưởng tới thế giới</div><b>Hive Metastore</b> — thành
      phần lưu schema của mọi bảng (tên cột, kiểu dữ liệu, vị trí file trên HDFS/S3, định dạng...) — trở thành
      chuẩn de-facto mà cả Presto, Trino, Spark SQL, Impala ngày nay đều đọc và tương thích được. Khi một công
      ty nói "data warehouse trên Hadoop/S3 của chúng tôi dùng Hive Metastore", điều đó có nghĩa MỌI công cụ
      xử lý dữ liệu hiện đại (dù không dùng HiveQL để truy vấn) vẫn có thể "nhìn thấy" và đọc đúng các bảng đó.</div>
      <p>Đây là một bài học kiến trúc quan trọng: thành phần sống lâu nhất của một hệ thống không nhất thiết là
      phần "hào nhoáng" nhất (ngôn ngữ truy vấn), mà thường là phần hạ tầng âm thầm bên dưới (schema catalog)
      mà mọi công cụ khác phụ thuộc vào.</p>""")])
 ],
 quiz=[
  dict(q="Apache Pig ra đời ở đâu, với mục tiêu gì?", opts=[
     "Facebook, để thay thế SQL hoàn toàn", "Yahoo Research, cho nhà nghiên cứu cách tuỳ biến tạo/chạy MapReduce job trên dữ liệu lớn",
     "Google, để thay thế GFS", "LinkedIn, để xử lý activity stream"],
   correct=1, explain="Pig ra đời ở Yahoo Research khoảng 2006, giải quyết vấn đề MapReduce thuần quá cấp thấp/cứng nhắc."),
  dict(q="PigLatin được thiết kế nằm ở đâu trên phổ 'khai báo (SQL) - thủ tục (MapReduce)'?", opts=[
     "Hoàn toàn khai báo như SQL", "Hoàn toàn thủ tục như MapReduce thuần", "Ở điểm giữa — có cấu trúc dataflow thủ tục nhưng mức trừu tượng cao hơn MapReduce Java", "Không liên quan tới cả hai"],
   correct=2, explain="PigLatin là procedural dataflow, trung gian giữa SQL khai báo và MapReduce thủ tục cấp thấp."),
  dict(q="Apache Hive do ai đồng sáng tạo tại Facebook?", opts=[
     "Doug Cutting & Mike Cafarella", "Joydeep Sen Sarma & Ashish Thusoo", "Jay Kreps & Neha Narkhede", "Jeff Dean & Sanjay Ghemawat"],
   correct=1, explain="Hammerbacher có vai trò giới thiệu/hạ tầng Hadoop ở Facebook, nhưng Sen Sarma và Thusoo là người đồng sáng tạo chính Hive."),
  dict(q="Động lực chính khiến Facebook xây Hive là gì?", opts=[
     "Muốn thay thế hoàn toàn MapReduce bằng công nghệ mới", "Dữ liệu tăng vọt (10s GB/ngày → 15 TB/ngày) mà chỉ kỹ sư Java mới khai thác được Hadoop, không scale ra toàn công ty được",
     "Google yêu cầu tương thích chuẩn", "Giảm chi phí phần cứng"],
   correct=1, explain="Cần một cách để kỹ sư/analyst quen SQL cũng khai thác được Hadoop mà không cần viết MapReduce Java."),
  dict(q="Theo nguồn lịch sử, tỉ lệ nhân sự Facebook dùng hạ tầng phân tích dữ liệu mỗi tháng đã thay đổi ra sao?", opts=[
     "Giữ nguyên ở mức 6 người", "Từ 6 người dùng (khi 15PB dữ liệu) tăng lên 20-30% toàn công ty (tới năm 2011)",
     "Giảm dần theo thời gian", "Tăng lên 100% ngay lập tức"],
   correct=1, explain="Đây là minh chứng cho hiệu quả 'dân chủ hoá dữ liệu' mà Hive mang lại."),
  dict(q="Bản phát hành đầu tiên của Apache Hive là khi nào?", opts=["2006", "2008", "10/2010", "2015"],
   correct=2, explain="Tháng 10/2010 là bản phát hành đầu tiên của Hive, theo nguồn lịch sử đã trích."),
  dict(q="Sự khác biệt cốt lõi giữa PigLatin và HiveQL là gì?", opts=[
     "Không có khác biệt, cùng 1 ngôn ngữ", "PigLatin thủ tục (viết từng bước biến đổi), HiveQL khai báo (nói muốn kết quả gì, giống SQL)",
     "PigLatin chỉ chạy trên Spark", "HiveQL không hỗ trợ GROUP BY"],
   correct=1, explain="Đây là sự khác biệt triết lý ngôn ngữ cốt lõi giữa 2 công cụ."),
  dict(q="Cả script PigLatin và HiveQL cho bài toán tổng doanh số theo nhân viên, sau khi biên dịch, đều chuyển thành gì bên dưới?", opts=[
     "Truy vấn SQL trực tiếp trên RDBMS", "Một hoặc nhiều MapReduce job (Map đọc dòng, Shuffle&Sort gộp theo employee, Reduce cộng tổng)",
     "Mã máy biên dịch trực tiếp", "Không cần biên dịch, chạy trực tiếp trên NameNode"],
   correct=1, explain="Cả hai chỉ là 2 cách VIẾT khác nhau để sinh ra cùng luồng MapReduce Map→Shuffle&Sort→Reduce."),
  dict(q="Thành phần nào của Hive có ảnh hưởng lâu dài nhất, được cả Presto/Trino/Spark SQL tương thích ngày nay?", opts=[
     "Cú pháp HiveQL", "Hive Metastore (catalog lưu schema bảng)", "Giao diện web Hive", "Thuật toán tối ưu truy vấn Hive"],
   correct=1, explain="Hive Metastore trở thành chuẩn de-facto lưu schema mà hầu hết công cụ xử lý dữ liệu hiện đại đều tương thích, dù không dùng HiveQL."),
  dict(q="Vì sao Hive thế hệ đầu (chạy trên MapReduce) không phù hợp cho truy vấn tương tác nhanh?", opts=[
     "Vì HiveQL không hỗ trợ SELECT", "Vì MapReduce tối ưu cho xử lý batch, có độ trễ cao, không phù hợp truy vấn cần phản hồi nhanh",
     "Vì Hive không đọc được HDFS", "Vì Hive chỉ chạy trên 1 node"],
   correct=1, explain="Đây là lý do Presto/Trino/Spark SQL ra đời sau để giải quyết nhu cầu truy vấn nhanh hơn, dù vẫn có thể dùng chung Hive Metastore."),
  dict(q="Pig mã nguồn mở hoá và có bản phát hành đầu tiên vào khi nào?", opts=[
     "Mở nguồn 2007, phát hành đầu tiên 9/2008", "Mở nguồn 2010, phát hành đầu tiên 2011", "Mở nguồn 2004, phát hành đầu tiên 2005", "Chưa từng mã nguồn mở"],
   correct=0, explain="Mùa thu 2007 mở nguồn qua Apache Incubator, bản phát hành chính thức đầu tiên tháng 9/2008."),
 ]),

# ---------------------------------------------------------------- 28
dict(n=28, slug="hd-04-hbase-sqoop", title="HBase & Sqoop: NoSQL lấy cảm hứng từ Bigtable, và cầu nối với thế giới RDBMS cũ",
 tag="Lịch sử HBase (Powerset/Bigtable) · Sqoop (Cloudera)",
 intro="HBase không phải ý tưởng của Hadoop — nó là bản sao chép (re-implementation) mã nguồn mở của một hệ thống nội bộ của Google. Và Sqoop nhắc chúng ta rằng công nghệ Big Data không tồn tại mãi.",
 parts=[
  dict(title="HBase: lấy cảm hứng trực tiếp từ Bigtable của Google", bullets=[
    "Powerset xây HBase (phát hành 28/3/2008) để phục vụ tìm kiếm ngôn ngữ tự nhiên (NLP)",
    "Mô hình theo sát paper Bigtable (Google, 2006): CSDL cột mở rộng phân tán",
    "HBase = 'hệ quản trị CSDL của Hadoop', lưu trên HDFS"],
   slides=[
    dict(h="Từ bài toán tìm kiếm ngôn ngữ tự nhiên tới HBase", body="""
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>HBase ban đầu do công ty Powerset xây
      dựng, phát hành lần đầu ngày 28/3/2008 — mô hình dữ liệu và kiến trúc lấy cảm hứng trực tiếp từ hệ thống
      Bigtable của Google (công bố qua paper năm 2006). Powerset cần xử lý khối lượng dữ liệu khổng lồ cho bài
      toán tìm kiếm ngôn ngữ tự nhiên (NLP), và nhận thấy mô hình "CSDL cột mở rộng phân tán" của Bigtable là
      lời giải phù hợp — nhưng Bigtable là hệ thống nội bộ đóng của Google, nên Powerset xây một bản mã nguồn
      mở tương đương, chạy trên nền HDFS thay vì GFS.
      Nguồn: <a href="https://en.wikipedia.org/wiki/Apache_HBase" target="_blank">Apache HBase — Wikipedia</a>.</div>
      <p>HBase được xem như "hệ quản trị CSDL của Hadoop": dữ liệu tổ chức logic thành bảng (hàng × cột), kích
      thước bảng có thể tới Terabyte/Petabyte, hàng ngàn cột, hỗ trợ hàng trăm ngàn thao tác INSERT/giây.</p>
      <div class="callout warn"><div class="lbl">Nhưng là NoSQL — đánh đổi có chủ đích</div>So với RDBMS
      truyền thống, HBase không có ngôn ngữ truy vấn mức cao như SQL — phải dùng API <code>get</code>/<code>put</code>/
      <code>scan</code> theo khoá (row key). Đây là đánh đổi: bỏ tính linh hoạt truy vấn để đạt khả mở và
      băng thông ghi cực cao.</div>""")]),
  dict(title="Facebook Messages 2010: ca sử dụng nổi tiếng nhất của HBase", bullets=[
    "Facebook chọn HBase cho hệ thống Messages mới (triển khai tháng 11/2010)",
    "Là minh chứng HBase có thể vận hành ở quy mô hàng trăm triệu người dùng",
    "Nhưng: Facebook sau đó đã chuyển Messages sang MyRocks (2018) — công nghệ không tồn tại mãi"],
   slides=[
    dict(h="Vì sao Facebook chọn HBase cho Messages?", body="""
      <div class="callout good"><div class="lbl">📚 Nguồn lịch sử</div>Để xây hệ thống tin nhắn mới, Facebook
      đã dựng nhiều prototype và thử nghiệm trên nhiều nền tảng lưu trữ phân tán khác nhau — HBase (mô phỏng
      theo Bigtable của Google) là nền tảng thắng cuộc, và Facebook triển khai hệ thống Messages dựa trên
      HBase vào tháng 11/2010.
      Nguồn: <a href="https://www.theregister.com/2010/12/17/facebook_messages_tech" target="_blank">The Register — Facebook Messages tech</a>.</div>
      <p>Đây là minh chứng công khai lớn nhất ở thời điểm đó cho thấy HBase/mô hình Bigtable có thể vận hành
      ổn định ở quy mô hàng trăm triệu người dùng hoạt động — câu chuyện này góp phần lớn khiến HBase trở
      thành lựa chọn NoSQL hàng đầu trong hệ sinh thái Hadoop suốt nhiều năm sau.</p>
      <div class="callout warn"><div class="lbl">Bài học trung thực: không công nghệ nào tồn tại mãi</div>
      Facebook sau đó đã di chuyển (migrate) hạ tầng Messages từ HBase sang MyRocks (một storage engine dựa
      trên RocksDB) vào năm 2018. Điều này không có nghĩa HBase "thất bại" — mà cho thấy lựa chọn công nghệ
      luôn gắn với một giai đoạn và một bộ yêu cầu cụ thể, và các hệ thống lớn tiếp tục tiến hoá khi yêu cầu
      thay đổi theo thời gian.</div>""")]),
  dict(title="Apache Sqoop: cầu nối RDBMS cũ ↔ Hadoop mới", bullets=[
    "Aaron Kimball (Cloudera) phát triển, nộp patch đầu tiên tháng 5/2009",
    "Giải quyết bài toán rất thực tế: doanh nghiệp có hàng chục năm dữ liệu trong RDBMS, không thể bỏ qua khi chuyển sang Hadoop",
    "Trở thành Apache top-level project tháng 4/2012 — nhưng bị \"nghỉ hưu\" (Apache Attic) tháng 6/2021"],
   slides=[
    dict(h="Sqoop giải quyết bài toán gì, và hoạt động ra sao?", body="""
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>Sqoop do Aaron Kimball cùng nhóm phát
      triển tại Cloudera xây dựng, bắt đầu như một contrib module của Hadoop từ tháng 5/2009 (patch đầu tiên:
      HADOOP-5815). Tháng 4/2010 tách khỏi Hadoop contrib, do Cloudera duy trì trên GitHub; ngày 23/7/2011
      được incubate thành dự án Apache; tháng 4/2012 trở thành Apache top-level project.
      Nguồn: <a href="https://en.wikipedia.org/wiki/Sqoop" target="_blank">Sqoop — Wikipedia</a>.</div>
      <p>Bài toán Sqoop giải quyết rất thực tế: hầu hết doanh nghiệp lớn đã có hàng chục năm dữ liệu nằm trong
      RDBMS (Oracle, MySQL, SQL Server...) từ trước khi Hadoop ra đời. Không ai muốn/có thể bỏ dữ liệu đó —
      Sqoop cho phép <b>import</b> (toàn bộ bảng, 1 bảng, hoặc 1 phần bảng) từ RDBMS vào HDFS qua job Map-only
      hoặc MapReduce, và <b>export</b> dữ liệu ngược lại từ HDFS ra RDBMS.</p>"""),
    dict(h="Vì sao Sqoop bị \"nghỉ hưu\" năm 2021 — bài học về chu kỳ sống công nghệ", body="""
      <div class="callout warn"><div class="lbl">📚 Nguồn lịch sử</div>Dự án Apache Sqoop chính thức bị
      retired (chuyển vào Apache Attic — nơi lưu các dự án Apache không còn được duy trì tích cực) vào tháng
      6/2021. Nguồn: <a href="https://en.wikipedia.org/wiki/Sqoop" target="_blank">Sqoop — Wikipedia</a>.</div>
      <p>Lý do thực tế (không phải vì Sqoop "làm sai" điều gì): cách doanh nghiệp đồng bộ dữ liệu giữa RDBMS và
      hệ thống Big Data đã dịch chuyển sang các công cụ Change Data Capture (CDC) streaming thời gian thực
      (ví dụ Debezium kết hợp Kafka — xem buổi tiếp theo) thay vì các job batch import/export định kỳ kiểu
      Sqoop. Đây là một ví dụ rõ ràng cho quy luật chung của ngành: công cụ ETL batch dần nhường vai trò cho
      kiến trúc streaming khi yêu cầu độ trễ dữ liệu ngày càng khắt khe hơn.</p>""")]),
  dict(title="Ví dụ minh hoạ: thiết kế row key HBase & 1 lệnh Sqoop import", bullets=[
    "Thiết kế row key cho bảng log sự kiện người dùng (tránh hotspotting)",
    "1 câu lệnh Sqoop import bảng 'orders' từ MySQL vào HDFS"],
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
      đúng vấn đề "hotspotting" nêu trên — mất hết lợi thế phân tán ghi của HBase.)</div>"""),
    dict(h="1 lệnh Sqoop import thực tế", body="""
      <div class="pd-formula"><div class="pd-formula-label">Sqoop import bảng orders từ MySQL vào HDFS</div>
      <div class="pd-formula-math">\\text{sqoop import --connect jdbc:mysql://host/db --table orders --target-dir /data/orders}</div></div>
      <p>Kết quả: Sqoop sinh 1 job Map-only (không cần Reduce vì đây chỉ là copy dữ liệu, không tổng hợp), mỗi
      Mapper đọc 1 phần của bảng <code>orders</code> (chia theo khoá chính), ghi ra các tệp văn bản trong thư
      mục HDFS <code>/data/orders</code>, các trường phân tách bởi dấu phẩy mặc định.</p>""")])
 ],
 quiz=[
  dict(q="HBase lấy cảm hứng kiến trúc trực tiếp từ hệ thống nào của Google?", opts=["GFS", "MapReduce", "Bigtable", "Chubby"],
   correct=2, explain="HBase là bản mã nguồn mở theo mô hình Bigtable (paper Google 2006), chạy trên HDFS."),
  dict(q="Công ty nào ban đầu xây dựng HBase, và để giải quyết bài toán gì?", opts=[
     "Facebook, cho hệ thống Messages", "Powerset, cho tìm kiếm ngôn ngữ tự nhiên (NLP)", "Cloudera, cho ETL", "LinkedIn, cho activity stream"],
   correct=1, explain="Powerset xây HBase (phát hành 28/3/2008) để phục vụ bài toán tìm kiếm NLP ở quy mô lớn."),
  dict(q="Khác biệt chính giữa HBase và RDBMS truyền thống là gì?", opts=[
     "HBase nhanh hơn ở mọi tác vụ", "HBase là NoSQL, không có ngôn ngữ truy vấn mức cao như SQL, dùng API get/put/scan theo khoá",
     "HBase không hỗ trợ lưu bảng lớn", "HBase chạy trên 1 máy duy nhất"],
   correct=1, explain="Đánh đổi: bỏ ngôn ngữ truy vấn linh hoạt để đạt khả mở/băng thông ghi cao."),
  dict(q="Facebook triển khai hệ thống Messages dựa trên HBase vào thời điểm nào?", opts=["2008", "11/2010", "2015", "2021"],
   correct=1, explain="Tháng 11/2010, sau khi thử nghiệm nhiều nền tảng lưu trữ phân tán khác."),
  dict(q="Điều gì xảy ra với hệ thống Messages của Facebook sau đó (2018)?", opts=[
     "Vẫn dùng HBase không đổi tới nay", "Facebook migrate sang MyRocks (dựa trên RocksDB)", "Facebook đóng dịch vụ Messages", "Facebook quay lại dùng RDBMS truyền thống"],
   correct=1, explain="Đây là bài học về chu kỳ sống công nghệ: không hệ thống nào tồn tại mãi dù từng rất thành công."),
  dict(q="Aaron Kimball phát triển Sqoop ở công ty nào, nộp patch đầu tiên khi nào?", opts=[
     "Yahoo, 2006", "Cloudera, 5/2009", "Facebook, 2010", "Google, 2004"],
   correct=1, explain="Aaron Kimball tại Cloudera, patch đầu tiên HADOOP-5815 nộp tháng 5/2009."),
  dict(q="Sqoop giải quyết bài toán thực tế gì cho doanh nghiệp?", opts=[
     "Thay thế hoàn toàn RDBMS", "Trung chuyển dữ liệu theo khối giữa Hadoop và RDBMS có cấu trúc (import/export)",
     "Tăng tốc truy vấn SQL", "Mã hoá dữ liệu nhạy cảm"],
   correct=1, explain="Doanh nghiệp có nhiều năm dữ liệu trong RDBMS — Sqoop là cầu nối 2 chiều với HDFS."),
  dict(q="Apache Sqoop hiện ở trạng thái nào (tính tới thời điểm viết bài)?", opts=[
     "Vẫn đang phát triển tích cực", "Đã bị retired, chuyển vào Apache Attic từ tháng 6/2021", "Chưa từng chính thức công bố", "Vừa được tách thành 2 dự án mới"],
   correct=1, explain="Sqoop bị retired tháng 6/2021 khi CDC streaming (vd Debezium+Kafka) thay thế vai trò ETL batch của nó."),
  dict(q="Vì sao dùng timestamp làm tiền tố row key trong HBase là thiết kế nguy hiểm khi ghi dữ liệu liên tục?", opts=[
     "Vì timestamp không phải số", "Vì mọi row mới đều có khoá lớn nhất, dồn ghi vào 1 region 'nóng' duy nhất (hotspotting)",
     "Vì HBase không hỗ trợ timestamp", "Vì row key phải là số nguyên"],
   correct=1, explain="Đây là vấn đề hotspotting kinh điển trong thiết kế schema HBase."),
  dict(q="Trong câu lệnh 'sqoop import --connect ... --table orders --target-dir /data/orders', job sinh ra có cần bước Reduce không?", opts=[
     "Có, luôn cần Reduce để tổng hợp", "Không, đây là job Map-only vì chỉ copy dữ liệu, không tổng hợp", "Chỉ cần Reduce nếu bảng có khoá chính", "Phụ thuộc vào kích thước bảng"],
   correct=1, explain="Sqoop import là copy dữ liệu theo phân vùng, không cần bước tổng hợp Reduce."),
  dict(q="HBase được gọi là gì trong hệ sinh thái Hadoop?", opts=["Công cụ ETL", "'Hệ quản trị CSDL của Hadoop'", "Hệ thống lập lịch workflow", "Công cụ coordination phân tán"],
   correct=1, explain="Vì lưu dữ liệu có cấu trúc dạng bảng trên HDFS với khả năng đọc/ghi tốc độ cao, HBase đóng vai trò tương tự 1 hệ quản trị CSDL cho Hadoop."),
 ]),

# ---------------------------------------------------------------- 29
dict(n=29, slug="hd-05-kafka", title="Apache Kafka: từ bài toán nội bộ LinkedIn tới xương sống streaming của cả ngành",
 tag="Lịch sử Kafka (LinkedIn) · Kiến trúc · Confluent",
 intro="Kafka không được thiết kế như một message queue thông thường — nó được thiết kế lại từ đầu như một log phân tán, vì các hệ thống pub-sub cũ không chịu được quy mô activity-stream của LinkedIn.",
 parts=[
  dict(title="LinkedIn, 2010-2011: động lực ra đời Kafka", bullets=[
    "Jay Kreps, Neha Narkhede, Jun Rao cùng xây Kafka khi làm ở LinkedIn",
    "Vấn đề: dữ liệu activity-stream (click, view, log) tăng bùng nổ, công cụ pub-sub cũ không đáp ứng được",
    "Kreps viết phần lớn Kafka trong kỳ nghỉ Giáng sinh; mã nguồn mở hoá đầu năm 2011"],
   slides=[
    dict(h="Vì sao các công cụ cũ không đủ dùng?", body="""
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>Apache Kafka được phát triển năm 2010
      bởi Jay Kreps, Neha Narkhede và Jun Rao khi họ làm việc tại LinkedIn, và trở thành nền tảng mã nguồn mở
      vào đầu năm 2011. Jay Kreps — kiến trúc sư chính cho hạ tầng dữ liệu tại LinkedIn — đã viết phần lớn
      Kafka trong kỳ nghỉ Giáng sinh. Nguồn gốc hệ thống nằm ở chỗ các công cụ trước đó thiếu những thuộc tính
      cần có của một hệ thống phân tán hiện đại để chuyển dữ liệu an toàn ở quy mô mà một công ty tăng trưởng
      nhanh như LinkedIn cần.
      Nguồn: <a href="https://www.frontier-enterprise.com/?p=15028" target="_blank">Frontier Enterprise — Kafka history</a>,
      <a href="https://developer.confluent.io/podcast/jay-kreps-on-the-last-10-years-of-apache-kafka-and-event-streaming" target="_blank">Confluent — Jay Kreps podcast</a>.</div>
      <p>Jun Rao trước đó là nhà nghiên cứu ở IBM Almaden, chuyên về CSDL và hệ thống phân tán; Neha Narkhede
      sau khi rời Oracle gia nhập LinkedIn và dẫn dắt mảng hạ tầng streams. Cả ba hợp lực giải quyết đúng 1 bài
      toán: làm sao chuyển dữ liệu sự kiện (activity data) từ hàng trăm nguồn khác nhau tới hàng trăm hệ thống
      tiêu thụ khác nhau (báo cáo, Hadoop, cảnh báo thời gian thực...) một cách tin cậy và có thể mở rộng.</p>
      <div class="callout good"><div class="lbl">📄 Nguồn tham khảo đã có trong materials.zip</div>
      Garg, N. (2013). <i>Apache Kafka</i>. Packt Publishing — tài liệu kỹ thuật chi tiết về kiến trúc Kafka
      (đã có sẵn trong <code>materials/papers/</code>, chỉ trích dẫn bibliographic, không host lại file).</div>""")]),
  dict(title="Kiến trúc Kafka: log phân tán, không phải message queue thường", bullets=[
    "Producer ghi vào Topic, Topic chia thành nhiều Partition",
    "Broker lưu trữ, ZooKeeper điều phối cluster metadata (ở các bản Kafka trước KRaft)",
    "Consumer đọc theo Offset — Kafka giữ log, không xoá message sau khi đọc như queue truyền thống"],
   slides=[
    dict(h="Vì sao gọi Kafka là 'log phân tán' chứ không phải 'message queue'?", body="""
      <p>Khác biệt cốt lõi: một message queue truyền thống (RabbitMQ kiểu cũ) XOÁ message sau khi được 1
      consumer đọc xong. Kafka thì giữ nguyên message trong 1 khoảng thời gian cấu hình được (retention), và
      CHO PHÉP nhiều consumer group độc lập đọc lại cùng dữ liệu đó, mỗi group tự theo dõi vị trí đọc riêng
      bằng <b>offset</b> của mình.</p>
      <ul class="pd-legend"><li><b>Topic</b><span>một luồng dữ liệu được đặt tên (vd "user-clicks")</span></li>
      <li><b>Partition</b><span>Topic được chia thành nhiều partition để phân tán tải — đây chính là bài toán
      gán partition cho consumer đã học ở <a href="../ll-08-kafka-roundrobin-range/index.html">Lập lịch 08</a>
      và <a href="../ll-09-kafka-sticky-rebalance/index.html">Lập lịch 09</a></span></li>
      <li><b>Broker</b><span>server lưu trữ thật các partition</span></li>
      <li><b>Offset</b><span>vị trí đọc hiện tại của 1 consumer group trong 1 partition — KHÔNG phải vị trí
      toàn cục, mỗi consumer group có offset riêng</span></li></ul>
      <div class="callout info"><div class="lbl">🔗 Liên hệ trực tiếp, không viết lại thuật toán</div>Việc gán
      partition cho consumer (RoundRobinAssignor/RangeAssignor/StickyAssignor) và bài toán tái cân bằng khi 1
      consumer rời nhóm đã được giải thích đầy đủ, kèm demo tương tác thật, ở
      <a href="../ll-08-kafka-roundrobin-range/index.html">Lập lịch 08</a> và
      <a href="../ll-09-kafka-sticky-rebalance/index.html">Lập lịch 09</a> — module này không lặp lại, chỉ
      liên kết tới đúng nội dung đó.</div>""")]),
  dict(title="Confluent (2014): từ dự án nội bộ tới công ty tỷ đô", bullets=[
    "Kreps, Narkhede, Rao thành lập Confluent năm 2014 với 500.000 USD đầu tư từ LinkedIn",
    "Mô hình: mã nguồn mở Kafka + dịch vụ/tiện ích thương mại xung quanh",
    "Confluent IPO năm 2021, doanh thu hàng năm vượt 300 triệu USD tại thời điểm nộp hồ sơ"],
   slides=[
    dict(h="Vì sao 3 kỹ sư LinkedIn lập công ty riêng?", body="""
      <div class="callout good"><div class="lbl">📚 Nguồn lịch sử</div>Dù vẫn hài lòng làm việc tại LinkedIn,
      cả ba liên tục nhận được yêu cầu hỗ trợ và đề xuất xây thêm tiện ích cho Kafka từ các công ty khác đang
      dùng nó. Họ nhận ra có cơ hội kinh doanh thực sự trong việc tạo và thương mại hoá công cụ xung quanh
      Kafka, trong khi vẫn duy trì gốc mã nguồn mở. Confluent được thành lập năm 2014 với khoản đầu tư khoảng
      500.000 USD từ LinkedIn.
      Nguồn: <a href="https://www.hpcwire.com/bigdatawire/2014/11/10/linkedin-spinoff-confluent-extend-kafka" target="_blank">HPCwire — LinkedIn spinoff Confluent</a>,
      <a href="https://www.cnbc.com/2021/06/01/linkedin-backed-confluent-files-s-1-as-yearly-sales-top-300-million.html" target="_blank">CNBC — Confluent S-1 filing</a>.</div>
      <p>Đây là một mẫu hình lặp lại nhiều lần trong ngành dữ liệu lớn: công nghệ giải quyết bài toán nội bộ
      của 1 công ty lớn (LinkedIn, giống Hadoop ra đời từ Yahoo) → mã nguồn mở hoá → chính người tạo ra nó
      thành lập công ty thương mại hoá nó.</p>""")]),
  dict(title="Ảnh hưởng tới thế giới: kiến trúc 'log-centric' định hình lại cách công ty xử lý dữ liệu", bullets=[
    "Uber, Netflix, Airbnb đều dùng Kafka làm xương sống event streaming",
    "Khai sinh tư duy kiến trúc 'event sourcing'/'log là nguồn sự thật duy nhất' (log as single source of truth)"],
   slides=[
    dict(h="Từ activity-stream nội bộ tới chuẩn kiến trúc dữ liệu hiện đại", body="""
      <div class="callout good"><div class="lbl">🌍 Ảnh hưởng tới thế giới</div>Kafka không chỉ là một công
      cụ nhắn tin — nó khai sinh một triết lý kiến trúc: dùng 1 log sự kiện bất biến (immutable log) làm
      "nguồn sự thật duy nhất" (single source of truth), mọi hệ thống khác (database, cache, dashboard phân
      tích thời gian thực, mô hình machine learning) đều là "view" được xây lại từ log đó. Triết lý này (gọi
      là <i>event sourcing</i>/<i>log-centric architecture</i>) hiện là nền tảng hạ tầng dữ liệu tại các công
      ty công nghệ lớn nhất: Uber (theo dõi chuyến đi thời gian thực), Netflix (telemetry/đề xuất nội dung),
      Airbnb (pipeline dữ liệu sự kiện người dùng).</p>
      <p>Điều này nối thẳng với nội dung đã học ở <a href="../ll-05-srpt/index.html">Lập lịch 05 — SRPT và
      hàng đợi công việc động</a>: Kafka chính là lớp hạ tầng hàng đợi thực tế mà các hệ thống xử lý luồng như
      Spark Streaming/Flink đọc dữ liệu đầu vào từ đó, biến lý thuyết lập lịch hàng đợi thành hệ thống chạy
      thật ở quy mô hàng triệu sự kiện/giây.</p>""")])
 ],
 quiz=[
  dict(q="Kafka được phát triển bởi 3 kỹ sư nào, tại công ty nào?", opts=[
     "Jay Kreps, Neha Narkhede, Jun Rao — tại LinkedIn", "Doug Cutting, Mike Cafarella — tại Yahoo",
     "Jeff Dean, Sanjay Ghemawat — tại Google", "Joydeep Sen Sarma, Ashish Thusoo — tại Facebook"],
   correct=0, explain="Ba người này phát triển Kafka tại LinkedIn năm 2010, mã nguồn mở hoá đầu 2011."),
  dict(q="Jay Kreps được cho là đã viết phần lớn Kafka trong hoàn cảnh nào?", opts=[
     "Một hackathon công khai", "Kỳ nghỉ Giáng sinh", "Trong lúc thực tập đại học", "Theo yêu cầu trực tiếp từ khách hàng bên ngoài"],
   correct=1, explain="Theo nguồn lịch sử đã trích, Kreps viết phần lớn Kafka trong kỳ nghỉ Giáng sinh khi làm ở LinkedIn."),
  dict(q="Khác biệt cốt lõi giữa Kafka ('log phân tán') và message queue truyền thống là gì?", opts=[
     "Kafka nhanh hơn ở mọi trường hợp", "Kafka giữ lại message sau khi đọc (retention), cho nhiều consumer group đọc lại độc lập; queue truyền thống xoá message sau khi đọc",
     "Kafka không hỗ trợ nhiều consumer", "Không có khác biệt thực sự"],
   correct=1, explain="Đây là khác biệt triết lý kiến trúc quan trọng nhất của Kafka so với message queue cổ điển."),
  dict(q="Trong Kafka, 'offset' đại diện cho điều gì?", opts=[
     "Độ trễ mạng giữa producer và broker", "Vị trí đọc hiện tại của MỘT consumer group trong MỘT partition cụ thể",
     "Số lượng broker trong cluster", "Kích thước tối đa của 1 message"],
   correct=1, explain="Mỗi consumer group có offset riêng — không phải vị trí đọc toàn cục chung cho mọi người."),
  dict(q="Bài toán gán partition cho consumer (RoundRobin/Range/Sticky) đã được học chi tiết ở đâu trong site này?", opts=[
     "Chính module này, phần kiến trúc Kafka", "Lập lịch 08 và Lập lịch 09 (có demo tương tác thật)", "Không có trong site này", "Module Hive & Pig"],
   correct=1, explain="Module này chủ động liên kết tới Lập lịch 08/09 thay vì lặp lại nội dung, đúng nguyên tắc tránh trùng lặp."),
  dict(q="Confluent được thành lập năm nào, với khoản đầu tư ban đầu từ đâu?", opts=[
     "2010, tự vốn hoàn toàn", "2014, khoảng 500.000 USD từ LinkedIn", "2018, từ quỹ chính phủ", "2021, từ IPO"],
   correct=1, explain="Confluent thành lập năm 2014 với khoảng 500.000 USD đầu tư từ LinkedIn."),
  dict(q="Mô hình kinh doanh của Confluent là gì?", opts=[
     "Đóng toàn bộ mã nguồn, bán license độc quyền", "Giữ Kafka mã nguồn mở, thương mại hoá dịch vụ/tiện ích xung quanh nó",
     "Chỉ bán phần cứng chuyên dụng", "Không có mô hình kinh doanh rõ ràng"],
   correct=1, explain="Confluent duy trì gốc mã nguồn mở Kafka, kinh doanh qua dịch vụ/tiện ích/nền tảng cloud xung quanh."),
  dict(q="Công ty nào KHÔNG được nêu là ví dụ dùng Kafka làm xương sống event streaming trong bài học này?", opts=["Uber", "Netflix", "Airbnb", "Nokia"],
   correct=3, explain="Uber, Netflix, Airbnb được nêu làm ví dụ; Nokia không được đề cập trong nội dung đã học."),
  dict(q="Triết lý kiến trúc mà Kafka khai sinh, coi log sự kiện là 'nguồn sự thật duy nhất', được gọi là gì?", opts=[
     "Object-oriented architecture", "Event sourcing / log-centric architecture", "Relational normalization", "Master-slave replication"],
   correct=1, explain="Event sourcing/log-centric architecture: mọi hệ thống khác là 'view' xây lại từ log bất biến."),
  dict(q="Jun Rao có kinh nghiệm nền tảng gì trước khi tham gia phát triển Kafka?", opts=[
     "Kỹ sư phần cứng tại Intel", "Nhà nghiên cứu tại IBM Almaden, chuyên CSDL và hệ thống phân tán", "Giảng viên đại học về mạng máy tính", "Không có kinh nghiệm liên quan"],
   correct=1, explain="Jun Rao từng là nghiên cứu viên ở IBM Almaden, nghiên cứu CSDL/hệ thống phân tán trước khi vào LinkedIn."),
  dict(q="Kafka liên hệ trực tiếp tới lý thuyết lập lịch hàng đợi nào đã học trước đó?", opts=[
     "List Scheduling & LPT (Lập lịch 02)", "SRPT và hàng đợi công việc động (Lập lịch 05)", "DRF (Lập lịch 07)", "Không liên hệ tới lý thuyết lập lịch nào"],
   correct=1, explain="Kafka là lớp hạ tầng hàng đợi thực tế cho các hệ thống xử lý luồng, nối trực tiếp lý thuyết SRPT/hàng đợi vào hệ thống chạy thật."),
  dict(q="Paper/tài liệu nào trong materials.zip được dùng làm nguồn chính cho kiến trúc Kafka trong module này?", opts=[
     "Dean & Ghemawat (2004) MapReduce", "Garg (2013) 'Apache Kafka', Packt Publishing", "Decandia et al. (2007) Dynamo", "Ghodsi et al. (2011) DRF"],
   correct=1, explain="Garg (2013) là tài liệu kỹ thuật về Kafka có sẵn trong materials/papers/, trích dẫn bibliographic, không host file."),
 ]),

# ---------------------------------------------------------------- 30
dict(n=30, slug="hd-06-oozie-zookeeper", title="Oozie & ZooKeeper: điều phối workflow, và \"xương sống vô hình\" của hệ phân tán",
 tag="Lịch sử Oozie · ZooKeeper (Chubby/ZAB) · Tổng kết chương",
 intro="ZooKeeper là công nghệ ít ai 'nhìn thấy' trực tiếp nhưng gần như MỌI hệ thống phân tán lớn (HBase, Kafka cũ, Solr, Mesos) đều phụ thuộc vào nó để tồn tại. Oozie là lớp điều phối để các job Hadoop không phải chạy rời rạc, thủ công.",
 parts=[
  dict(title="Apache Oozie: điều phối workflow trên cụm Hadoop", bullets=[
    "Ra đời ở Yahoo! năm 2008, mã nguồn mở qua Apache năm 2011, top-level project 2012",
    "Workflow là đồ thị có hướng không chu trình (DAG) của các action",
    "Hỗ trợ đa dạng: MapReduce, Pig/Hive script, Java/Shell, SSH, email"],
   slides=[
    dict(h="Vì sao cần một hệ thống điều phối riêng?", body="""
      <p>Một pipeline xử lý dữ liệu thực tế hiếm khi chỉ có 1 job MapReduce — thường là chuỗi nhiều bước: chạy
      Sqoop import dữ liệu mới → chạy Hive script làm sạch → chạy job MapReduce tổng hợp → gửi email báo cáo
      hoàn tất. Nếu làm thủ công (cron job gọi lần lượt từng bước), rất dễ vỡ khi 1 bước lỗi hoặc chạy chậm
      hơn dự kiến.</p>
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>Oozie được phát triển lần đầu tại
      Yahoo! năm 2008 để giải quyết chính xác bài toán điều phối và lập lịch cho các triển khai Hadoop quy mô
      lớn; được mở ra như một dự án Apache (incubator) năm 2011, và trở thành Apache top-level project năm
      2012. Nguồn: <a href="https://attic.apache.org/projects/oozie.html" target="_blank">Apache Attic — Oozie</a>,
      <a href="https://www.dremio.com/wiki/apache-oozie" target="_blank">Dremio — What is Apache Oozie?</a>.</div>
      <p>Oozie biểu diễn workflow dưới dạng <b>DAG</b> (đồ thị có hướng không chu trình) các "action" — đúng
      khái niệm DAG đã học ở <a href="../ll-03-dag-mapreduce/index.html">Lập lịch 03 — Lập lịch DAG,
      MapReduce và vị trí dữ liệu</a>, nhưng ở đây DAG biểu diễn thứ tự phụ thuộc giữa các JOB hoàn chỉnh,
      không phải giữa các TASK nhỏ trong 1 job.</p>""")]),
  dict(title="Apache ZooKeeper: lấy cảm hứng từ Chubby của Google", bullets=[
    "Ra đời ở Yahoo Research khoảng 2007, mở nguồn trên SourceForge cùng năm",
    "Mô phỏng theo Chubby (Google, paper Mike Burrows) — dịch vụ lock phân tán nội bộ của Google",
    "Dùng thuật toán ZAB (biến thể Paxos) để đạt đồng thuận (consensus) phân tán"],
   slides=[
    dict(h="Từ paper Chubby của Google tới dịch vụ mở cho mọi người", body="""
      <div class="callout good"><div class="lbl">📚 Nguồn lịch sử</div>ZooKeeper được mô hình hoá theo dịch
      vụ lock Chubby của Google (paper của Mike Burrows), và ban đầu được phát triển tại Yahoo Research
      khoảng năm 2007, mở nguồn trên SourceForge cùng năm đó. Kỹ sư Yahoo (trong đó có Ben Reed và Flavio
      Junqueira) khi đọc paper Chubby nhận thấy đây chính là công cụ có thể giải quyết nhiều vấn đề sản xuất
      ("production problems") họ đang gặp phải, và xây một phiên bản tương đương, tổng quát hoá giao diện
      Chubby thành dịch vụ "coordination-as-a-service" dùng chung cho nhiều hệ thống.
      Nguồn: <a href="https://en.wikipedia.org/wiki/Apache_ZooKeeper" target="_blank">Apache ZooKeeper — Wikipedia</a>.</div>
      <p>ZooKeeper dùng <b>ZAB</b> (ZooKeeper Atomic Broadcast) — một biến thể của thuật toán Paxos — để đạt
      đồng thuận phân tán: mọi thay đổi trạng thái phải được 1 "leader" đề xuất và đa số (majority) các node
      "follower" xác nhận trước khi được coi là chính thức.</p>
      <div class="callout warn"><div class="lbl">Liên kết video đã có trong Chương 2 gốc</div>Chương 2 gốc
      (slide gốc) đã dẫn 1 video giới thiệu thuật toán PAXOS — module này đi sâu hơn: PAXOS/ZAB không chỉ là
      lý thuyết hàn lâm, mà là CƠ CHẾ THẬT đứng sau việc ZooKeeper có thể trả lời đúng "ai đang là leader" dù
      nhiều node cùng tham gia bầu cử đồng thời.</div>"""),
    dict(h="4 chức năng cốt lõi ZooKeeper cung cấp", body="""
      <table><tr><th>Chức năng</th><th>Ý nghĩa thực tế</th></tr>
      <tr><td>Quản lý thành viên nhóm (group membership)</td><td>Biết chính xác node nào đang sống trong cluster tại mọi thời điểm</td></tr>
      <tr><td>Bầu cử leader (leader election)</td><td>Khi node leader cũ chết, nhanh chóng và AN TOÀN chọn ra 1 leader mới duy nhất (không bao giờ có 2 leader cùng lúc)</td></tr>
      <tr><td>Quản lý cấu hình động</td><td>Thay đổi cấu hình hệ thống mà không cần restart từng node</td></tr>
      <tr><td>Giám sát trạng thái hệ thống</td><td>Theo dõi sức khoẻ cluster theo thời gian thực</td></tr></table>
      <div class="callout good"><div class="lbl">🌍 Ảnh hưởng tới thế giới — \"xương sống vô hình\"</div>
      ZooKeeper trở thành thành phần coordination nền tảng cho rất nhiều hệ thống phân tán lớn: HBase (bầu
      leader cho region server), Kafka bản cũ trước KRaft (quản lý metadata cluster), Apache Solr (coordination
      cho SolrCloud), Apache Mesos (quản lý trạng thái cluster). Phần lớn người dùng cuối không bao giờ "thấy"
      ZooKeeper trực tiếp — nhưng khi ZooKeeper gặp sự cố, toàn bộ hệ thống phía trên (HBase, Kafka cũ...) đều
      ngừng hoạt động đúng. Đây là lý do nó được gọi là "xương sống vô hình" của hệ phân tán.</div>""")]),
  dict(title="Ví dụ minh hoạ: bầu leader ZooKeeper & 1 workflow Oozie 4 bước", bullets=[
    "Bầu leader bằng znode tuần tự (sequential znode) — zxid nhỏ nhất thắng",
    "Workflow Oozie: Sqoop import → Hive clean → MapReduce tổng hợp → gửi email"],
   slides=[
    dict(h="Bầu leader bằng znode tuần tự — từng bước", body="""
      <p>Một cách triển khai leader election phổ biến trên ZooKeeper: mỗi node ứng viên tạo 1 <b>znode tuần
      tự</b> (sequential znode) dưới cùng 1 đường dẫn cha, ví dụ <code>/election/candidate-</code>. ZooKeeper
      tự gắn thêm 1 số thứ tự tăng dần (zxid) vào tên mỗi znode được tạo.</p>
      <table><tr><th>Node</th><th>znode được tạo</th></tr>
      <tr><td>Node A</td><td><code>/election/candidate-0000000007</code></td></tr>
      <tr><td>Node B</td><td><code>/election/candidate-0000000005</code></td></tr>
      <tr><td>Node C</td><td><code>/election/candidate-0000000009</code></td></tr></table>
      <p>Quy tắc: node tạo được znode có số thứ tự <b>nhỏ nhất</b> trong số các znode con hiện có sẽ là
      leader → ở đây là <b>Node B</b> (0000000005). Nếu Node B chết, znode của nó tự bị xoá (vì là znode
      "ephemeral" gắn với session của B); các node còn lại kiểm tra lại danh sách con, znode nhỏ nhất còn lại
      (Node A, 0000000007) trở thành leader mới — không cần bất kỳ node nào "thông báo" trực tiếp cho node
      khác.</p>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Nếu sau đó Node D tham gia muộn và tạo
      znode <code>candidate-0000000011</code>, ai là leader hiện tại? (Đáp: vẫn là Node A với
      0000000007 — Node D có số thứ tự lớn hơn, không giành được vai trò leader khi A còn sống.)</div>"""),
    dict(h="1 workflow Oozie 4 bước, có phụ thuộc rõ ràng", body="""
      <p>Workflow Oozie cho pipeline "cập nhật báo cáo doanh số hàng ngày":</p>
      <div class="pd-formula"><div class="pd-formula-label">DAG 4 action (ký hiệu A → B nghĩa là B chỉ chạy khi A xong)</div>
      <div class="pd-formula-math">\\text{Sqoop import} \\to \\text{Hive clean} \\to \\text{MapReduce tổng hợp} \\to \\text{Gửi email báo cáo}</div></div>
      <p>Nếu bước "Hive clean" thất bại, Oozie KHÔNG chạy tiếp "MapReduce tổng hợp" hay "Gửi email" — toàn bộ
      workflow dừng và báo lỗi đúng tại điểm hỏng, thay vì gửi 1 email báo cáo dựa trên dữ liệu chưa được làm
      sạch (lỗi rất nguy hiểm nếu chạy bằng cron job thủ công không kiểm tra phụ thuộc).</p>""")]),
  dict(title="Tổng kết Chương 2 dưới góc nhìn lịch sử: 1 dòng thời gian", bullets=[
    "2003-04: 2 paper Google (GFS, MapReduce) khởi nguồn mọi thứ",
    "2006-2008: Hadoop, Pig, Hive, HBase, ZooKeeper ra đời gần như cùng lúc ở Yahoo/Facebook/Powerset",
    "2009-2012: Sqoop, Oozie, YARN hoàn thiện hệ sinh thái; 2010-2011: Kafka ra đời ở LinkedIn"],
   slides=[
    dict(h="Một hệ sinh thái, nhưng không phải một công ty", body="""
      <p>Điều đáng chú ý nhất khi nhìn lại lịch sử cả Chương 2: <b>hệ sinh thái Hadoop không do 1 công ty hay
      1 nhóm thiết kế từ đầu</b> — mỗi công nghệ ra đời ở một công ty khác nhau, để giải quyết một bài toán nội
      bộ cụ thể của công ty đó, rồi được mã nguồn mở hoá và ghép lại thành "hệ sinh thái" qua Apache Software
      Foundation:</p>
      <table><tr><th>Năm</th><th>Công nghệ</th><th>Nơi ra đời</th><th>Bài toán nội bộ ban đầu</th></tr>
      <tr><td>2003-2004</td><td>GFS, MapReduce (paper)</td><td>Google</td><td>Lưu trữ &amp; xử lý chỉ mục web quy mô Internet</td></tr>
      <tr><td>2006</td><td>Hadoop (tách từ Nutch)</td><td>Yahoo!</td><td>Công cụ tìm kiếm mở không scale được</td></tr>
      <tr><td>2006-2008</td><td>Pig</td><td>Yahoo Research</td><td>MapReduce quá cấp thấp cho nghiên cứu ad hoc</td></tr>
      <tr><td>2007</td><td>ZooKeeper</td><td>Yahoo Research</td><td>Cần coordination phân tán kiểu Chubby của Google</td></tr>
      <tr><td>2008</td><td>HBase</td><td>Powerset</td><td>Tìm kiếm ngôn ngữ tự nhiên cần CSDL kiểu Bigtable</td></tr>
      <tr><td>2008</td><td>Oozie</td><td>Yahoo!</td><td>Điều phối nhiều job Hadoop phụ thuộc nhau</td></tr>
      <tr><td>2009</td><td>Sqoop</td><td>Cloudera</td><td>Cầu nối dữ liệu RDBMS cũ ↔ Hadoop mới cho doanh nghiệp</td></tr>
      <tr><td>2010-2011</td><td>Hive</td><td>Facebook</td><td>Data warehouse Hadoop chỉ 6 người dùng được vì quá khó</td></tr>
      <tr><td>2010-2011</td><td>Kafka</td><td>LinkedIn</td><td>Activity-stream bùng nổ, pub-sub cũ không chịu được</td></tr>
      <tr><td>2012</td><td>YARN</td><td>Yahoo!/Hortonworks</td><td>JobTracker nghẽn, cần tách resource management</td></tr></table>
      <div class="callout good"><div class="lbl">🌍 Bài học lớn nhất của cả Chương 2</div>"Hệ sinh thái Hadoop"
      thực ra là lịch sử của NHIỀU công ty cùng đối mặt một dạng bài toán giống nhau (dữ liệu vượt quá 1 máy)
      ở những thời điểm gần nhau (2006-2012), và văn hoá mã nguồn mở của Apache Software Foundation là thứ
      cho phép các giải pháp riêng lẻ đó ghép lại thành 1 hệ sinh thái liên vận hành được — không ai đó ngồi
      "thiết kế" cả hệ sinh thái này từ đầu.</div>""")])
 ],
 quiz=[
  dict(q="Apache Oozie ra đời ở đâu, năm nào?", opts=["Facebook, 2010", "Yahoo!, 2008", "LinkedIn, 2011", "Google, 2004"],
   correct=1, explain="Oozie phát triển lần đầu tại Yahoo! năm 2008 để điều phối job Hadoop quy mô lớn."),
  dict(q="Workflow trong Oozie được biểu diễn dưới dạng cấu trúc gì?", opts=[
     "Danh sách tuyến tính đơn giản", "Đồ thị có hướng không chu trình (DAG) của các action", "Cây nhị phân", "Bảng băm"],
   correct=1, explain="Giống khái niệm DAG đã học ở Lập lịch 03, nhưng ở mức JOB hoàn chỉnh, không phải TASK."),
  dict(q="ZooKeeper được mô phỏng theo hệ thống nào của Google?", opts=["Bigtable", "GFS", "Chubby (dịch vụ lock phân tán)", "Spanner"],
   correct=2, explain="ZooKeeper dựa trên ý tưởng từ paper Chubby của Mike Burrows (Google)."),
  dict(q="ZooKeeper ra đời ở đâu, khoảng năm nào?", opts=["Yahoo Research, khoảng 2007", "Facebook, 2010", "LinkedIn, 2011", "Powerset, 2008"],
   correct=0, explain="Phát triển ở Yahoo Research khoảng 2007, mở nguồn trên SourceForge cùng năm."),
  dict(q="ZAB (dùng trong ZooKeeper) là biến thể của thuật toán đồng thuận nào?", opts=["Raft", "Paxos", "Two-Phase Commit", "Gossip protocol"],
   correct=1, explain="ZAB (ZooKeeper Atomic Broadcast) là một biến thể của Paxos."),
  dict(q="Trong bầu leader bằng znode tuần tự, node nào trở thành leader?", opts=[
     "Node tạo znode cuối cùng (số thứ tự lớn nhất)", "Node tạo znode có số thứ tự NHỎ NHẤT trong các znode con hiện có",
     "Node có địa chỉ IP nhỏ nhất", "Node khởi động ZooKeeper đầu tiên"],
   correct=1, explain="Quy tắc: số thứ tự (zxid) nhỏ nhất trong các znode con hiện có sẽ là leader."),
  dict(q="Khi leader hiện tại chết, điều gì xảy ra với znode của nó, và hệ quả là gì?", opts=[
     "Znode vẫn còn, hệ thống không có leader mới", "Znode (ephemeral) tự bị xoá do gắn với session đã chết; node còn lại có số thứ tự nhỏ nhất kế tiếp trở thành leader mới",
     "Toàn bộ cluster phải khởi động lại", "ZooKeeper tự chọn leader ngẫu nhiên"],
   correct=1, explain="Đây là cơ chế bầu leader an toàn, tự động, không cần node nào 'thông báo' trực tiếp cho node khác."),
  dict(q="Hệ thống nào KHÔNG phụ thuộc vào ZooKeeper để coordination (theo nội dung đã học)?", opts=[
     "HBase (bầu leader region server)", "Kafka bản cũ trước KRaft (quản lý metadata cluster)", "Apache Solr (SolrCloud)", "RDBMS truyền thống đơn lẻ không phân tán"],
   correct=3, explain="RDBMS đơn lẻ không cần coordination phân tán kiểu ZooKeeper; HBase/Kafka cũ/Solr/Mesos đều phụ thuộc vào nó."),
  dict(q="Trong workflow Oozie 4 bước (Sqoop → Hive clean → MapReduce → Email), nếu bước Hive clean thất bại, điều gì xảy ra?", opts=[
     "Oozie vẫn chạy tiếp các bước sau với dữ liệu cũ", "Oozie dừng workflow, không chạy MapReduce/Email, báo lỗi đúng điểm hỏng", "Toàn bộ cluster Hadoop dừng hoạt động", "Email báo cáo vẫn được gửi nhưng ghi chú lỗi"],
   correct=1, explain="Đây là lợi ích chính của điều phối workflow có khai báo phụ thuộc rõ ràng, so với chạy cron job thủ công không kiểm tra."),
  dict(q="Theo dòng thời gian tổng kết, công nghệ nào ra đời SỚM NHẤT làm nền tảng cho cả hệ sinh thái?", opts=[
     "Kafka (LinkedIn)", "2 paper GFS và MapReduce của Google (2003-2004)", "YARN (2012)", "Hive (Facebook)"],
   correct=1, explain="2 paper Google là điểm khởi nguồn, truyền cảm hứng trực tiếp cho Hadoop và hầu hết công nghệ sau đó."),
  dict(q="Bài học lớn nhất rút ra từ việc nhìn lại lịch sử toàn Chương 2 là gì?", opts=[
     "Tất cả công nghệ đều do 1 nhóm ở Google thiết kế sẵn từ đầu", "Hệ sinh thái Hadoop là kết quả của NHIỀU công ty khác nhau giải quyết bài toán nội bộ riêng, rồi mã nguồn mở hoá và ghép lại qua Apache Software Foundation",
     "Mọi công nghệ trong hệ sinh thái đều ra đời cùng 1 năm", "Hệ sinh thái Hadoop không còn công nghệ nào được dùng tới ngày nay"],
   correct=1, explain="Đây là thông điệp tổng kết chính của cả 6 module deep-dive: hệ sinh thái là 'ghép lại' từ nhiều lời giải độc lập, không phải thiết kế tập trung."),
  dict(q="Công nghệ nào trong hệ sinh thái đã chính thức bị 'nghỉ hưu' (Apache Attic), cho thấy không phải mọi thành phần đều tồn tại mãi?", opts=["Hive", "HBase", "Sqoop", "ZooKeeper"],
   correct=2, explain="Sqoop bị retired vào Apache Attic tháng 6/2021, nhường vai trò ETL batch cho các giải pháp CDC streaming."),
 ]),
]
