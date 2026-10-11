# -*- coding: utf-8 -*-
# Bản mở rộng SÂU HƠN của module hd-05-kafka (n=29).
# Giữ nguyên 100% các callout lịch sử/nguồn/liên hệ đã có trong bản gốc
# (hadoop_deepdive_content.py, dict n=29) — chỉ MỞ RỘNG thêm part/slide/quiz mới.
# 2 link nội bộ bắt buộc giữ nguyên, không viết lại thuật toán gán partition:
#   ../ll-08-kafka-roundrobin-range/index.html
#   ../ll-09-kafka-sticky-rebalance/index.html
#
# Facts lịch sử mới dùng trong bản mở rộng (KRaft/KIP-500), đã verify bằng WebSearch:
#   - KIP-500 (loại bỏ phụ thuộc ZooKeeper) + KIP-595 (giao thức Raft cho metadata quorum)
#   - Kafka 2.8.0: early access KRaft; Kafka 3.3.1: KRaft production-ready;
#     Kafka 4.0 (cuối 2024): gỡ bỏ hoàn toàn hỗ trợ ZooKeeper, KRaft là chế độ duy nhất.
#   Nguồn: https://www.conduktor.io/glossary/understanding-kraft-mode-in-kafka ,
#          https://www.confluent.io/blog/removing-zookeeper-dependency-in-kafka/

HD05_EXPANDED = dict(
 n=29, slug="hd-05-kafka", title="Apache Kafka: từ bài toán nội bộ LinkedIn tới xương sống streaming của cả ngành",
 tag="Lịch sử Kafka (LinkedIn) · Kiến trúc · Confluent",
 intro="Kafka không được thiết kế như một message queue thông thường — nó được thiết kế lại từ đầu như một log phân tán, vì các hệ thống pub-sub cũ không chịu được quy mô activity-stream của LinkedIn.",
 parts=[

  # ---------- PART 1 (giữ nguyên bullets + slide gốc, thêm 1 slide mới) ----------
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
      (đã có sẵn trong <code>materials/papers/</code>, chỉ trích dẫn bibliographic, không host lại file).</div>"""),
    dict(h="Bài toán 'N nguồn ghi tới M hệ thống đọc' — không chỉ của LinkedIn", body="""
      <p>🗣️ <b>Nói nôm na:</b> trước Kafka, LinkedIn giống một văn phòng có 50 người cần gửi báo cáo cho 50
      người khác — nếu mỗi người tự gửi email riêng cho từng người nhận, số "đường dây" liên lạc tăng theo
      kiểu N×M, cực kỳ rối và dễ vỡ khi 1 người đổi vai trò. Kafka giống việc lập 1 bảng tin chung duy nhất:
      ai cần gửi tin thì dán 1 lần, ai cần đọc thì tự ra bảng tin đọc — số "đường dây" giảm từ N×M xuống N+M.</p>
      <p>Về mặt kỹ thuật, trước khi có Kafka, LinkedIn phải xây nhiều đường ống point-to-point riêng biệt giữa
      từng cặp (nguồn dữ liệu, hệ thống tiêu thụ): log hành vi người dùng → hệ thống báo cáo, log hành vi
      người dùng → hệ thống gợi ý, log hành vi người dùng → cảnh báo gian lận... Mỗi đường ống phải tự lo
      việc chịu lỗi, tốc độ, định dạng. Kafka tập trung hoá thành 1 lớp trung gian pub-sub duy nhất.</p>
      <p>Bài toán "nhiều nguồn ghi, nhiều nơi đọc, cần độ tin cậy cao" không chỉ riêng công nghệ:</p>
      <ul class="pd-legend">
      <li><b>Ngân hàng (minh hoạ)</b><span>nhiều chi nhánh ghi giao dịch, nhiều hệ thống (chống gian lận, báo
      cáo tuân thủ, tính lãi) cùng cần đọc lại đúng những giao dịch đó theo đúng thứ tự</span></li>
      <li><b>Hãng hàng không (minh hoạ)</b><span>nhiều sân bay ghi sự kiện check-in/cất-hạ cánh, nhiều hệ
      thống (lịch bay, hành lý, thông báo khách) cùng cần luồng sự kiện đó theo thời gian thực</span></li>
      <li><b>Sản xuất/nhà máy (minh hoạ)</b><span>nhiều cảm biến trên dây chuyền ghi số đo, nhiều hệ thống
      (bảo trì dự đoán, kiểm soát chất lượng, dashboard vận hành) cùng tiêu thụ luồng số đo đó</span></li>
      </ul>
      <div class="callout info"><div class="lbl">Vì sao LinkedIn là nơi bài toán này "chín" sớm nhất</div>
      LinkedIn tăng trưởng người dùng rất nhanh giai đoạn 2008-2011 trong khi lượng activity-stream (lượt
      xem hồ sơ, kết nối, tương tác) tăng theo cấp số nhân — đây là lý do ba kỹ sư LinkedIn chạm bài toán
      quy mô này trước phần lớn công ty cùng thời, buộc họ phải thiết kế lại từ đầu thay vì vá hệ thống cũ.</div>""")]),

  # ---------- PART 2 (giữ nguyên bullets + slide gốc, thêm slide mở rộng) ----------
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
      liên kết tới đúng nội dung đó.</div>"""),
    dict(h="Log phân tán vs Message Queue: so sánh trực diện qua 3 ngành khác nhau", body="""
      <p>🗣️ <b>Nói nôm na:</b> message queue truyền thống giống một tờ giấy nháp — ai đọc xong thì xé bỏ,
      người đến sau không còn gì để đọc lại. Kafka giống 1 cuốn sổ ghi chép (ledger) ngân hàng: mọi giao dịch
      được ghi vào sổ theo thứ tự, và nhiều người khác nhau (kiểm toán, khách hàng, bộ phận thuế) có thể quay
      lại tra đúng những dòng đó bao nhiêu lần tuỳ ý, miễn còn trong thời hạn lưu trữ.</p>
      <table><tr><th>Đặc điểm</th><th>Message queue truyền thống (vd RabbitMQ kiểu cũ)</th><th>Kafka (log phân tán)</th></tr>
      <tr><td>Message sau khi 1 consumer đọc xong</td><td>Bị xoá khỏi queue</td><td>Vẫn giữ nguyên tới hết thời gian retention</td></tr>
      <tr><td>Nhiều consumer group đọc cùng dữ liệu</td><td>Khó — message đã bị consumer đầu tiên "lấy mất"</td><td>Tự nhiên — mỗi group có offset riêng, đọc độc lập</td></tr>
      <tr><td>Đọc lại dữ liệu cũ (replay)</td><td>Không hỗ trợ (dữ liệu đã mất)</td><td>Hỗ trợ — chỉ cần "tua" offset về vị trí cũ</td></tr>
      <tr><td>Mô hình tư duy</td><td>Hàng đợi công việc cần xử lý 1 lần</td><td>Nhật ký sự kiện bất biến, nhiều "độc giả"</td></tr></table>
      <p>Ví dụ ở các ngành khác (minh hoạ) cho thấy đây không phải khác biệt kỹ thuật vụn vặt mà là khác biệt
      triết lý:</p>
      <ul class="pd-legend">
      <li><b>Tài chính/ngân hàng (minh hoạ)</b><span>Kafka giữ lại message giống 1 cuốn sổ ghi chép giao dịch
      ai cũng tra lại được nhiều lần, không phải tờ giấy nháp xé bỏ sau khi đọc</span></li>
      <li><b>Báo chí (minh hoạ)</b><span>Consumer Group giống nhiều nhóm phóng viên khác nhau cùng theo dõi 1
      kênh tin tức, mỗi nhóm tự ghi nhớ mình đã đọc tới đâu, không ảnh hưởng nhóm khác</span></li>
      <li><b>Sản xuất (minh hoạ)</b><span>Partition giống nhiều băng chuyền song song trong 1 nhà máy để tăng
      tốc độ xử lý — mỗi băng chuyền xử lý độc lập, tổng thông lượng cộng dồn lại</span></li>
      </ul>""")]),

  # ---------- PART 3 MỚI: Topic/Partition/Broker/Offset chi tiết ----------
  dict(title="Bốn khối nền tảng: Topic, Partition, Broker, Offset — nhìn kỹ từng khối", bullets=[
    "Topic là 'tên luồng', Partition là đơn vị song song hoá thật sự bên trong 1 Topic",
    "Mỗi Partition là 1 log vật lý được ghi tiếp (append-only), có vị trí tuyệt đối tăng dần",
    "Offset là toạ độ 3 chiều: (topic, partition, consumer group) — không có 'vị trí đọc toàn cục'"],
   slides=[
    dict(h="Topic và Partition: tên luồng vs đơn vị song song hoá", body="""
      <p>🗣️ <b>Nói nôm na:</b> Topic giống tên 1 tờ báo (vd "Báo Thể thao"); Partition giống việc tờ báo đó
      được in ở nhiều nhà máy in khác nhau, mỗi nhà máy in 1 phần số lượng bản để giao kịp giờ — tổng số báo
      phát hành không đổi, nhưng tốc độ in tăng lên nhiều lần vì chạy song song.</p>
      <p>Về kỹ thuật: 1 Topic là danh nghĩa (tên luồng dữ liệu); Partition mới là đơn vị lưu trữ và xử lý song
      song thật sự. Mỗi Partition là 1 log vật lý riêng, append-only (chỉ được ghi thêm vào cuối, không sửa
      giữa), và mỗi bản ghi trong partition có 1 số thứ tự tăng dần tuyệt đối — đây là vị trí VẬT LÝ trong
      partition, khác với offset ĐÃ ĐỌC của 1 consumer group (nói ở slide sau).</p>
      <table><tr><th>Ngành (minh hoạ)</th><th>Topic tương ứng với</th><th>Partition tương ứng với</th></tr>
      <tr><td>Bán lẻ</td><td>Luồng "đơn hàng mới"</td><td>Chia theo khu vực kho để xử lý song song</td></tr>
      <tr><td>Viễn thông</td><td>Luồng "cuộc gọi hoàn tất"</td><td>Chia theo vùng trạm phát sóng</td></tr>
      <tr><td>Game online</td><td>Luồng "hành động người chơi"</td><td>Chia theo server phòng chơi</td></tr></table>"""),
    dict(h="Broker: ai thực sự giữ dữ liệu?", body="""
      <p>🗣️ <b>Nói nôm na:</b> nếu Topic là tên tờ báo và Partition là các nhà in, thì Broker chính là toà
      nhà vật lý chứa máy in đó — nơi dữ liệu thật sự nằm trên đĩa.</p>
      <p>Một Kafka cluster gồm nhiều Broker (mỗi broker là 1 tiến trình Kafka chạy trên 1 máy/server). Mỗi
      Partition của mỗi Topic được giao cho 1 hoặc nhiều Broker lưu trữ — số lượng Broker giữ bản sao của 1
      Partition chính là <b>replication factor</b> (phân tích kỹ ở phần sau, kèm ví dụ mô phỏng mất broker).
      Producer và Consumer không cần biết chính xác dữ liệu nằm ở Broker nào — Kafka tự định tuyến dựa trên
      metadata cluster.</p>
      <div class="callout info"><div class="lbl">📖 Giải thích cho người mới bắt đầu</div>Nếu bạn quen CSDL
      quan hệ, có thể tạm hình dung: Topic giống 1 bảng (table) được "sharding" (chia mảnh) — mỗi Partition là
      1 mảnh, và Broker là máy chủ vật lý giữ mảnh đó, tương tự cách 1 CSDL phân tán chia bảng lớn ra nhiều
      node để tăng khả năng chịu tải.</div>"""),
    dict(h="Offset: vì sao phải gắn với MỘT consumer group cụ thể?", body="""
      <details><summary>📖 Giải thích cho người mới bắt đầu</summary>
      <p>Nhiều người mới học Kafka nhầm rằng offset là "vị trí đọc chung" của cả hệ thống — SAI. Offset luôn
      là bộ 3: (topic, partition, consumer group). Lý do: Kafka được thiết kế để NHIỀU hệ thống tiêu thụ độc
      lập cùng đọc 1 nguồn dữ liệu, mỗi hệ thống có tốc độ và mục đích khác nhau.</p>
      <p>Ví dụ (minh hoạ ngành báo chí): kênh tin tức gốc là 1 Topic duy nhất. Nhóm phóng viên A (viết tin
      nhanh) đọc rất sát thời gian thực, trong khi nhóm phóng viên B (viết phân tích chuyên sâu cuối ngày) chỉ
      đọc 1 lần/ngày. Nếu Kafka chỉ có 1 offset chung, nhóm B sẽ làm "tụt" vị trí đọc của nhóm A mỗi khi B đọc
      chậm — vô lý. Vì vậy mỗi consumer group ("nhóm A", "nhóm B") có offset lưu trữ riêng, hoàn toàn độc lập
      với group khác, dù cùng đọc 1 partition.</p></details>
      <p>Về mặt lưu trữ, Kafka lưu các offset đã commit của từng consumer group trong 1 topic nội bộ đặc biệt
      tên <code>__consumer_offsets</code> — nghĩa là chính cơ chế lưu offset cũng dùng lại ý tưởng log của
      Kafka, không cần hệ thống lưu trữ riêng bên ngoài.</p>""")]),

  # ---------- PART 4 MỚI: Producer/Consumer/Consumer Group + ví dụ A (lag per-group) ----------
  dict(title="Producer, Consumer Group — và vì sao LAG là khái niệm PER-GROUP", bullets=[
    "Producer ghi message vào Topic, có thể dùng key để giữ thứ tự cho từng 'đối tượng'",
    "Consumer Group: nhiều consumer hợp tác đọc 1 topic, chia nhau các partition",
    "Lag = log-end-offset trừ offset đã commit — PHẢI tính riêng cho từng consumer group"],
   slides=[
    dict(h="Producer và Consumer Group: ai ghi, ai đọc?", body="""
      <p>🗣️ <b>Nói nôm na:</b> Producer giống người đăng tin lên bảng tin chung; Consumer Group giống 1 "ca
      làm việc" gồm nhiều người cùng chia nhau đọc bảng tin đó cho nhanh — trong ca đó, mỗi tin chỉ 1 người
      đọc (để không ai làm trùng việc của người khác), nhưng CA KHÁC (group khác) vẫn đọc lại đầy đủ từ đầu
      theo tốc độ và mục đích riêng của ca đó.</p>
      <p>Producer chỉ cần biết TÊN Topic, không cần biết ai đang đọc. Producer có thể gửi kèm 1 "key" cho mỗi
      message (vd mã khách hàng) — Kafka dùng key này để quyết định message rơi vào Partition nào, đảm bảo
      mọi message của cùng 1 key luôn vào cùng 1 partition, giữ đúng thứ tự cho riêng key đó dù topic có
      nhiều partition chạy song song.</p>
      <ul class="pd-legend">
      <li><b>Trong 1 Consumer Group</b><span>các consumer CHIA NHAU partition — mỗi partition chỉ 1 consumer
      trong group đó đọc tại 1 thời điểm (đúng bài toán gán partition ở Lập lịch 08/09)</span></li>
      <li><b>Giữa các Consumer Group khác nhau</b><span>mỗi group đọc ĐỘC LẬP toàn bộ topic, không chia sẻ
      offset, không ảnh hưởng tới group khác</span></li>
      </ul>"""),
    dict(h="Ví dụ A — 2 consumer group cùng đọc 1 partition, lag khác nhau hoàn toàn", body="""
      <p>Giả sử topic "đơn-hàng-mới" chỉ có 1 partition để đơn giản hoá. Log-end-offset (tổng số message đã
      ghi vào partition) tăng đúng <b>10 message/batch</b>. Có 2 consumer group độc lập cùng đọc:</p>
      <ul class="pd-legend">
      <li><b>Group "dashboard"</b><span>tiêu thụ nhanh — xử lý được 9 message/batch</span></li>
      <li><b>Group "backup"</b><span>tiêu thụ chậm hơn — chỉ xử lý được 4 message/batch</span></li>
      </ul>
      <p>Lag của 1 group = log-end-offset − offset đã commit của CHÍNH group đó. Bắt đầu cả 2 group ở offset 0,
      log-end-offset ở 0:</p>
      <table><tr><th>Batch</th><th>Log-end-offset (tổng ghi)</th><th>Offset "dashboard"</th><th>Lag "dashboard"</th><th>Offset "backup"</th><th>Lag "backup"</th></tr>
      <tr><td>1</td><td>10</td><td>9</td><td>10−9 = <b>1</b></td><td>4</td><td>10−4 = <b>6</b></td></tr>
      <tr><td>2</td><td>20</td><td>18</td><td>20−18 = <b>2</b></td><td>8</td><td>20−8 = <b>12</b></td></tr>
      <tr><td>3</td><td>30</td><td>27</td><td>30−27 = <b>3</b></td><td>12</td><td>30−12 = <b>18</b></td></tr>
      </table>
      <p>Quan sát: tại CÙNG MỘT thời điểm (cùng log-end-offset), group "dashboard" có lag tăng chậm (1→2→3)
      vì gần theo kịp tốc độ ghi, còn group "backup" có lag tăng rất nhanh (6→12→18) vì luôn xử lý chậm hơn
      tốc độ ghi mới — nếu không tăng tốc, lag của "backup" sẽ tăng vô hạn theo thời gian. Đây chính là minh
      chứng số học rằng <b>lag không phải 1 con số chung của topic</b>, mà là 1 con số RIÊNG cho từng cặp
      (consumer group, partition) — đúng với nguyên lý offset per-group đã nêu ở slide trước.</p>
      <div class="callout warn"><div class="lbl">Ứng dụng thực tế của việc tách lag theo group</div>Nhờ tách
      lag theo group, team vận hành có thể biết CHÍNH XÁC group nào đang "đuối" (ở đây là "backup") để tăng
      số consumer cho group đó, mà không ảnh hưởng gì tới group "dashboard" đang chạy ổn.</div>""")]),

  # ---------- PART 5 MỚI: Retention ----------
  dict(title="Retention: Kafka giữ dữ liệu bao lâu, và vì sao con số này là lựa chọn thiết kế", bullets=[
    "Retention theo thời gian (vd 7 ngày) hoặc theo kích thước (vd tối đa 100GB/partition)",
    "Hết hạn retention, message cũ bị xoá dù chưa có consumer group nào đọc tới",
    "Retention dài hơn → replay/debug/backfill dễ hơn, nhưng tốn đĩa hơn — là một trade-off có chủ đích"],
   slides=[
    dict(h="Retention: 'hạn sử dụng' của message, không phải 'đọc xong thì xoá'", body="""
      <p>🗣️ <b>Nói nôm na:</b> retention giống hạn lưu trữ của camera an ninh — camera lưu 7 hoặc 30 ngày,
      sau đó dữ liệu cũ tự động bị ghi đè/xoá, BẤT KỂ có ai đã xem đoạn phim đó hay chưa. Khác hẳn với việc
      "xoá ngay khi 1 người xem xong" (như message queue truyền thống).</p>
      <p>Kafka cho phép cấu hình retention theo 2 kiểu, có thể dùng kết hợp:</p>
      <table><tr><th>Kiểu retention</th><th>Ví dụ cấu hình</th><th>Khi nào message bị xoá</th></tr>
      <tr><td>Theo thời gian</td><td><code>retention.ms</code> = 7 ngày</td><td>Message cũ hơn 7 ngày bị xoá, dù chưa consumer group nào đọc</td></tr>
      <tr><td>Theo kích thước</td><td><code>retention.bytes</code> = 100GB/partition</td><td>Khi partition vượt 100GB, dữ liệu cũ nhất bị xoá trước để nhường chỗ</td></tr></table>
      <p>Ví dụ ở các ngành khác (minh hoạ):</p>
      <ul class="pd-legend">
      <li><b>Y tế (minh hoạ)</b><span>log theo dõi thiết bị cần giữ đủ lâu để phục vụ kiểm tra sự cố ngược
      thời gian (root-cause analysis), nhưng không cần giữ vĩnh viễn</span></li>
      <li><b>Thương mại điện tử (minh hoạ)</b><span>log hành vi mua sắm giữ 7-30 ngày đủ để huấn luyện lại mô
      hình gợi ý, không cần giữ hàng năm vì hành vi khách hàng thay đổi nhanh</span></li>
      </ul>
      <div class="callout info"><div class="lbl">Trade-off cần nhớ</div>Retention dài hơn giúp "replay" dữ
      liệu cũ dễ hơn khi cần debug sự cố hoặc backfill 1 hệ thống tiêu thụ mới — nhưng tốn không gian đĩa và
      chi phí hạ tầng hơn. Không có con số "đúng" tuyệt đối, chỉ có lựa chọn phù hợp với nhu cầu nghiệp vụ.</div>""")]),

  # ---------- PART 6 MỚI: Replication factor + ví dụ B ----------
  dict(title="Replication factor: 1 Partition, nhiều bản sao trên nhiều Broker", bullets=[
    "Mỗi Partition có 1 broker giữ bản 'leader' và các broker khác giữ bản 'follower'",
    "Mọi đọc/ghi đi qua leader; follower chỉ đồng bộ theo, sẵn sàng thay thế khi cần",
    "Khi broker giữ leader chết, 1 follower được bầu làm leader mới — không mất dữ liệu nếu đủ bản sao"],
   slides=[
    dict(h="Vì sao 1 bản sao duy nhất là không đủ an toàn?", body="""
      <p>🗣️ <b>Nói nôm na:</b> replication factor trong Kafka giống 1 hãng hàng không luôn có ít nhất 2 phi
      công được huấn luyện lái cùng 1 tuyến bay — nếu phi công chính (leader) ốm bất ngờ, phi công phụ
      (follower) đã sẵn sàng thay ngay, chuyến bay không bị huỷ.</p>
      <p>Về kỹ thuật: <b>replication factor</b> là số Broker khác nhau cùng giữ 1 bản sao đầy đủ của 1
      Partition. Trong số các bản sao đó, đúng 1 bản được chọn làm <b>leader</b> — mọi lệnh ghi (từ Producer)
      và đọc (từ Consumer) đều đi qua broker giữ leader. Các bản còn lại là <b>follower</b>, liên tục kéo dữ
      liệu mới từ leader về để đồng bộ, nhưng (ở cấu hình phổ biến) không trực tiếp phục vụ đọc/ghi.</p>
      <table><tr><th>Ngành (minh hoạ)</th><th>Vai trò 'leader'</th><th>Vai trò 'follower'</th></tr>
      <tr><td>Hàng không</td><td>Phi công chính đang lái</td><td>Phi công phụ đã huấn luyện, sẵn sàng thay</td></tr>
      <tr><td>Bệnh viện</td><td>Bác sĩ trực chính ca đó</td><td>Bác sĩ dự phòng được gọi khi bác sĩ chính vắng</td></tr>
      <tr><td>Ngân hàng</td><td>Chi nhánh trung tâm xử lý giao dịch gốc</td><td>Chi nhánh sao lưu đồng bộ dữ liệu liên tục</td></tr></table>"""),
    dict(h="Ví dụ B — mô phỏng mất broker giữ leader, ai lên thay?", body="""
      <p>Giả sử 1 Partition có replication factor = 3, trải trên 3 broker khác nhau:</p>
      <table><tr><th>Broker</th><th>Vai trò ban đầu</th></tr>
      <tr><td>Broker 1</td><td><b>Leader</b> — phục vụ mọi đọc/ghi</td></tr>
      <tr><td>Broker 2</td><td>Follower — đồng bộ đầy đủ với leader</td></tr>
      <tr><td>Broker 3</td><td>Follower — đồng bộ đầy đủ với leader</td></tr></table>
      <p><b>Tình huống:</b> Broker 1 (đang giữ leader) gặp sự cố và ngừng hoạt động hoàn toàn.</p>
      <p><b>Diễn biến:</b> hệ thống coordination của cluster phát hiện Broker 1 không còn phản hồi, và trong
      số các follower còn "đồng bộ đủ mới" (in-sync replica), 1 trong Broker 2 hoặc Broker 3 được bầu làm
      leader mới — giả sử là Broker 2. Từ thời điểm đó, mọi Producer/Consumer tự động được định tuyến lại tới
      Broker 2 để tiếp tục đọc/ghi, KHÔNG mất dữ liệu (vì Broker 2 đã có bản sao đầy đủ trước đó). Broker 3
      vẫn tiếp tục làm follower, nhưng giờ đồng bộ theo leader mới là Broker 2.</p>
      <div class="callout info"><div class="lbl">🔗 Ai thực hiện việc 'bầu lại leader' này?</div>Đây chính
      là vai trò coordination mà site đã phân tích kỹ ở phần ZooKeeper/KRaft (xem part sau): trong các bản
      Kafka cũ, ZooKeeper theo dõi tình trạng broker và phối hợp bầu leader mới cho partition; ở các bản Kafka
      mới dùng KRaft, chính cụm "controller" nội bộ của Kafka (dùng giao thức Raft) tự làm việc này, không cần
      ZooKeeper nữa. Cơ chế bầu cử chi tiết bằng znode tuần tự cho vai trò coordination nói chung đã có ví dụ
      từng bước ở module Oozie &amp; ZooKeeper (n=30) — module này chỉ liên hệ vai trò, không lặp lại.</div>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Nếu replication factor chỉ bằng 1 (không
      có follower nào), khi Broker 1 chết thì điều gì xảy ra? (Đáp: mất quyền truy cập dữ liệu của partition
      đó cho tới khi Broker 1 phục hồi — có thể mất dữ liệu vĩnh viễn nếu đĩa của Broker 1 hỏng luôn. Đây là
      lý do replication factor ≥ 2 gần như luôn bắt buộc trong triển khai thực tế.)</div>""")]),

  # ---------- PART 7 MỚI: ZooKeeper cũ vs KRaft ----------
  dict(title="ZooKeeper trong Kafka cũ, và vì sao Kafka mới dần bỏ ZooKeeper (KRaft)", bullets=[
    "Kafka trước đây dùng ZooKeeper bên ngoài để lưu cluster metadata, bầu leader cho partition, theo dõi broker sống/chết",
    "KIP-500 (bỏ phụ thuộc ZooKeeper) + KIP-595 (giao thức Raft nội bộ) là nền tảng của KRaft",
    "Kafka 2.8.0: KRaft early access; Kafka 3.3.1: production-ready; Kafka 4.0 (cuối 2024): gỡ hoàn toàn ZooKeeper"],
   slides=[
    dict(h="Vai trò ZooKeeper trong Kafka 'kiểu cũ'", body="""
      <p>🗣️ <b>Nói nôm na:</b> ở Kafka bản cũ, ZooKeeper giống 1 "tổng đài điều phối" bên ngoài nhà máy —
      không trực tiếp sản xuất (không lưu message), nhưng biết chính xác máy nào (broker) đang chạy, máy nào
      đang là "trưởng ca" (leader) cho từng dây chuyền (partition), và gọi điện báo ngay khi 1 máy hỏng.</p>
      <p>Cụ thể, trong các bản Kafka trước KRaft, ZooKeeper (đã được phân tích sâu ở module n=30 — Oozie
      &amp; ZooKeeper, bao gồm nguồn gốc từ paper Chubby của Google và cơ chế bầu cử bằng znode tuần tự) giữ
      3 vai trò chính cho Kafka: lưu trữ cluster metadata (danh sách topic, partition, broker), theo dõi
      broker còn sống hay đã chết, và phối hợp bầu lại leader cho partition khi broker giữ leader cũ chết
      (đúng tình huống ở Ví dụ B phần trước).</p>
      <div class="callout warn"><div class="lbl">Hạn chế dần lộ ra khi Kafka cluster lớn lên</div>Khi số
      lượng partition tăng lên hàng trăm nghìn (ở các cluster rất lớn), việc đồng bộ metadata qua ZooKeeper
      trở thành điểm nghẽn: thời gian failover (chuyển leader khi có sự cố) chậm đi, và vận hành phải duy trì
      thêm 1 hệ thống phân tán riêng (ZooKeeper) bên cạnh Kafka — tăng độ phức tạp vận hành.</div>"""),
    dict(h="KRaft: Kafka tự quản lý metadata bằng giao thức Raft, không cần ZooKeeper", body="""
      <div class="callout good"><div class="lbl">📚 Nguồn kỹ thuật (đã verify qua WebSearch)</div>Cộng đồng
      Kafka đề xuất <b>KIP-500</b> (loại bỏ phụ thuộc ZooKeeper) cùng <b>KIP-595</b> (định nghĩa giao thức
      Raft dùng riêng cho "metadata quorum" — gọi tắt là <b>KRaft</b>, Kafka Raft). Ý tưởng: thay vì gọi ra 1
      hệ thống coordination bên ngoài (ZooKeeper), Kafka tự dùng lại chính mô hình log phân tán + đồng thuận
      Raft để 1 nhóm "controller" nội bộ tự lưu và đồng bộ metadata — không cần phần mềm thứ 3.
      Mốc thời gian: Kafka 2.8.0 có KRaft ở dạng early-access; Kafka 3.3.1 công bố KRaft production-ready;
      Kafka 4.0 (phát hành cuối năm 2024) gỡ bỏ hoàn toàn hỗ trợ ZooKeeper — KRaft trở thành chế độ DUY NHẤT.
      Nguồn: <a href="https://www.conduktor.io/glossary/understanding-kraft-mode-in-kafka" target="_blank">Conduktor — Understanding KRaft Mode in Kafka</a>,
      <a href="https://www.confluent.io/blog/removing-zookeeper-dependency-in-kafka/" target="_blank">Confluent — Removing ZooKeeper Dependency in Kafka</a>.</div>
      <table><tr><th>Khía cạnh</th><th>Kafka cũ (dùng ZooKeeper)</th><th>Kafka mới (KRaft)</th></tr>
      <tr><td>Nơi lưu cluster metadata</td><td>Cụm ZooKeeper riêng, bên ngoài Kafka</td><td>Log metadata nội bộ, do cụm controller Kafka tự quản lý</td></tr>
      <tr><td>Giao thức đồng thuận</td><td>ZAB (biến thể Paxos, của ZooKeeper)</td><td>Raft (KIP-595), tích hợp trực tiếp vào Kafka</td></tr>
      <tr><td>Số hệ thống phân tán cần vận hành</td><td>2 (Kafka + ZooKeeper)</td><td>1 (chỉ Kafka)</td></tr></table>
      <p>Lưu ý quan trọng: KRaft KHÔNG thay đổi bản chất "log phân tán" hay khái niệm Topic/Partition/Offset
      đã học ở các part trước — nó chỉ thay đổi CÁCH cluster tự quản lý metadata và bầu leader nội bộ, phần
      trải nghiệm Producer/Consumer không đổi.</p>""")]),

  # ---------- PART 8 MỚI: Delivery semantics ----------
  dict(title="At-most-once, At-least-once, Exactly-once: 3 mức 'cam kết giao hàng' của Kafka", bullets=[
    "At-most-once: có thể mất message, nhưng không bao giờ gửi/đọc trùng",
    "At-least-once: không bao giờ mất message, nhưng có thể trùng nếu lỗi xảy ra giữa lúc xử lý và lúc commit offset",
    "Exactly-once: không mất, không trùng — cần cơ chế bổ sung (idempotent producer, transaction) để đạt được"],
   slides=[
    dict(h="3 mức cam kết giao hàng, nhìn qua ví dụ giao đồ ăn (minh hoạ)", body="""
      <p>🗣️ <b>Nói nôm na (minh hoạ ngành giao hàng):</b> at-most-once giống 1 shipper gọi cửa ĐÚNG 1 LẦN rồi
      đi luôn, dù khách có nghe thấy hay không — có thể khách không nhận được đồ (mất), nhưng chắc chắn không
      bị giao 2 lần. At-least-once giống shipper CỨ GỌI CỬA LẠI nếu chưa chắc khách đã nhận — khách chắc chắn
      nhận được đồ, nhưng có rủi ro nhận trùng 2 lần nếu shipper hiểu nhầm là chưa giao thành công. Exactly-once
      giống khi cả 2 bên có 1 "mã xác nhận" duy nhất cho đơn đó — dù shipper gọi lại bao nhiêu lần, hệ thống
      vẫn biết đơn này ĐÃ giao, không tính giao trùng.</p>
      <table><tr><th>Mức cam kết</th><th>Có thể mất message?</th><th>Có thể trùng message?</th><th>Khi nào offset được commit</th></tr>
      <tr><td>At-most-once</td><td>Có</td><td>Không</td><td>TRƯỚC khi xử lý xong message (nếu xử lý lỗi giữa đường, message coi như đã "đọc", không đọc lại)</td></tr>
      <tr><td>At-least-once</td><td>Không</td><td>Có</td><td>SAU khi xử lý xong message (nếu crash trước khi commit, message bị đọc lại ở lần sau → có thể xử lý trùng)</td></tr>
      <tr><td>Exactly-once</td><td>Không</td><td>Không (về mặt hiệu lực)</td><td>Gắn với cơ chế idempotent producer / transaction để đảm bảo ghi+commit offset là 1 đơn vị nguyên tử</td></tr></table>
      <p>Ví dụ ở ngành khác (minh hoạ):</p>
      <ul class="pd-legend">
      <li><b>Ngân hàng (minh hoạ)</b><span>chuyển tiền PHẢI là exactly-once — trùng 1 lần ghi nợ là thiệt hại
      tài chính thật, mất 1 lần ghi có thể làm sai số dư</span></li>
      <li><b>Giám sát/log hệ thống (minh hoạ)</b><span>at-least-once thường đủ dùng — trùng vài dòng log
      không nguy hại, miễn không mất log quan trọng khi có sự cố</span></li>
      <li><b>Cảm biến đo nhiệt độ tần suất cao (minh hoạ)</b><span>at-most-once có thể chấp nhận được — mất
      1-2 điểm đo trong hàng nghìn điểm/giây không ảnh hưởng xu hướng chung</span></li>
      </ul>
      <div class="callout warn"><div class="lbl">Lựa chọn mức cam kết là quyết định thiết kế, không phải mặc định "tốt nhất"</div>
      Exactly-once luôn tốt về mặt lý thuyết nhưng tốn chi phí (độ trễ, độ phức tạp vận hành) cao hơn — hệ
      thống thực tế chọn mức cam kết dựa trên hậu quả thực sự của việc mất hay trùng dữ liệu, không chọn mức
      cao nhất một cách mù quáng.</div>""")]),

  # ---------- PART 9 (giữ nguyên 100% — Confluent) ----------
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

  # ---------- PART 10 (giữ nguyên slide gốc, thêm 1 slide mở rộng) ----------
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
      Airbnb (pipeline dữ liệu sự kiện người dùng).</div>
      <p>Điều này nối thẳng với nội dung đã học ở <a href="../ll-05-srpt/index.html">Lập lịch 05 — SRPT và
      hàng đợi công việc động</a>: Kafka chính là lớp hạ tầng hàng đợi thực tế mà các hệ thống xử lý luồng như
      Spark Streaming/Flink đọc dữ liệu đầu vào từ đó, biến lý thuyết lập lịch hàng đợi thành hệ thống chạy
      thật ở quy mô hàng triệu sự kiện/giây.</p>"""),
    dict(h="'Log là nguồn sự thật duy nhất' nghĩa là gì, cụ thể hơn — qua 3 ngành (minh hoạ)", body="""
      <p>🗣️ <b>Nói nôm na:</b> event sourcing giống việc 1 công ty quyết định không còn tin vào "số dư cuối
      kỳ" ghi sẵn trong sổ cái nữa, mà tin vào TOÀN BỘ lịch sử giao dịch — số dư chỉ là kết quả TÍNH LẠI từ
      lịch sử đó bất cứ lúc nào cần. Nếu 1 báo cáo bị sai, ta không "sửa số dư" trực tiếp, mà sửa/bổ sung
      đúng giao dịch gây lỗi trong lịch sử, rồi tính lại.</p>
      <table><tr><th>Ngành (minh hoạ)</th><th>'Log sự kiện' gốc</th><th>'View' được xây lại từ log</th></tr>
      <tr><td>Thương mại điện tử</td><td>Mọi lượt xem sản phẩm, thêm giỏ hàng, mua hàng</td><td>Dashboard doanh số, mô hình gợi ý sản phẩm</td></tr>
      <tr><td>Gọi xe công nghệ</td><td>Mọi sự kiện bắt đầu/kết thúc chuyến đi, vị trí GPS</td><td>Bản đồ mật độ xe thời gian thực, tính giá động (surge pricing)</td></tr>
      <tr><td>Streaming nội dung</td><td>Mọi lượt xem, tạm dừng, bỏ xem giữa video</td><td>Hệ gợi ý nội dung cá nhân hoá</td></tr></table>
      <p>Điểm mấu chốt về kỹ thuật: vì Kafka giữ log (không xoá ngay sau khi đọc — đúng tính chất "log phân
      tán" đã học ở Part 2), các "view" phía trên hoàn toàn có thể được XÂY LẠI TỪ ĐẦU bất cứ lúc nào (vd khi
      đổi logic tính toán, hoặc phát hiện lỗi trong view cũ), chỉ cần đọc lại log từ offset 0 — một khả năng
      mà hệ thống dùng message queue "xoá sau khi đọc" không thể làm được.</p>""")])
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
  dict(q="Trong Ví dụ A (2 consumer group đọc cùng 1 partition), vì sao group 'backup' có lag tăng nhanh hơn group 'dashboard'?", opts=[
     "Vì 'backup' đọc sai thứ tự message", "Vì tốc độ tiêu thụ của 'backup' (4/batch) thấp hơn nhiều so với tốc độ ghi mới (10/batch), trong khi 'dashboard' (9/batch) gần theo kịp",
     "Vì 'backup' dùng partition khác với 'dashboard'", "Vì ZooKeeper ưu tiên group 'dashboard' hơn"],
   correct=1, explain="Lag = log-end-offset − offset đã commit của riêng group đó; tốc độ tiêu thụ thấp hơn tốc độ ghi khiến lag tăng dần theo từng batch."),
  dict(q="Replication factor của 1 Partition trong Kafka thể hiện điều gì?", opts=[
     "Số lượng Topic trong cluster", "Số lượng Broker khác nhau cùng giữ 1 bản sao đầy đủ của Partition đó (1 leader + các follower)",
     "Số lượng Consumer Group đang đọc Partition đó", "Thời gian retention của Partition đó"],
   correct=1, explain="Replication factor = tổng số bản sao (leader + follower) của 1 partition, trải trên các broker khác nhau để chịu lỗi."),
  dict(q="Trong ví dụ mô phỏng mất broker giữ leader (replication factor = 3), điều gì xảy ra để hệ thống không mất dữ liệu?", opts=[
     "Dữ liệu buộc phải mất, không có cách khắc phục", "Một follower đã đồng bộ đủ mới được bầu làm leader mới, Producer/Consumer được định tuyến lại tới broker đó",
     "Toàn bộ Partition bị xoá và tạo lại từ đầu", "ZooKeeper/KRaft tự tạo lại dữ liệu đã mất từ Producer"],
   correct=1, explain="Vì các follower đã có bản sao đầy đủ trước khi leader cũ chết, 1 follower được bầu lên thay thế mà không mất dữ liệu."),
  dict(q="KRaft (KIP-500 + KIP-595) thay đổi điều gì trong kiến trúc Kafka?", opts=[
     "Thay đổi hoàn toàn khái niệm Topic/Partition/Offset mà consumer/producer thấy được",
     "Cho phép Kafka tự quản lý cluster metadata bằng giao thức Raft nội bộ, loại bỏ sự phụ thuộc vào ZooKeeper bên ngoài",
     "Thêm 1 lớp message queue truyền thống song song với log phân tán", "Chỉ áp dụng cho Kafka chạy trên Windows"],
   correct=1, explain="KRaft gỡ ZooKeeper khỏi vai trò coordination, dùng chính Kafka (giao thức Raft) để tự quản lý metadata; trải nghiệm producer/consumer không đổi."),
  dict(q="Theo mốc thời gian đã verify, phiên bản Kafka nào gỡ bỏ HOÀN TOÀN hỗ trợ ZooKeeper?", opts=[
     "Kafka 2.8.0", "Kafka 3.3.1", "Kafka 4.0 (cuối năm 2024)", "Kafka 1.0"],
   correct=2, explain="Kafka 2.8.0 có KRaft ở dạng early-access, Kafka 3.3.1 công bố production-ready, còn Kafka 4.0 (cuối 2024) mới gỡ bỏ hoàn toàn ZooKeeper."),
  dict(q="Mức cam kết giao hàng (delivery semantics) nào của Kafka có thể làm MẤT message nhưng KHÔNG BAO GIỜ gửi/đọc trùng?", opts=[
     "Exactly-once", "At-least-once", "At-most-once", "Không mức nào có đặc điểm này"],
   correct=2, explain="At-most-once commit offset trước khi xử lý xong — nếu lỗi giữa đường, message coi như đã đọc và không đọc lại, có thể mất nhưng không trùng."),
  dict(q="Vì sao 'exactly-once' được xem là mức cam kết tốn chi phí hơn, không nên chọn mặc định cho mọi hệ thống?", opts=[
     "Vì Kafka không hỗ trợ được exactly-once trong thực tế", "Vì cần thêm cơ chế như idempotent producer/transaction, tăng độ trễ và độ phức tạp vận hành so với mức cam kết thấp hơn",
     "Vì exactly-once chỉ hoạt động với 1 partition duy nhất", "Vì exactly-once làm mất khả năng replay dữ liệu"],
   correct=1, explain="Exactly-once cần cơ chế bổ sung để đảm bảo ghi+commit offset là 1 đơn vị nguyên tử, đổi lại độ trễ/độ phức tạp cao hơn — nên chọn mức cam kết theo hậu quả thực tế của việc mất/trùng dữ liệu."),
  dict(q="Retention trong Kafka khác gì so với việc 'xoá message ngay sau khi 1 consumer đọc xong' của message queue truyền thống?", opts=[
     "Không khác gì, chỉ đổi tên gọi", "Retention xoá message theo thời gian/kích thước đã cấu hình, KHÔNG phụ thuộc việc đã có consumer group nào đọc tới hay chưa",
     "Retention chỉ áp dụng khi không có consumer nào kết nối", "Retention làm Kafka không bao giờ xoá dữ liệu"],
   correct=1, explain="Retention là 'hạn sử dụng' theo cấu hình (vd 7 ngày hoặc giới hạn dung lượng), hoàn toàn độc lập với việc consumer group đã đọc tới đâu."),
 ])
