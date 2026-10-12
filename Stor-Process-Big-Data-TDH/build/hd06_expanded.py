# -*- coding: utf-8 -*-
"""Bản MỞ RỘNG SÂU của module hd-06-oozie-zookeeper (n=30) — viết độc lập, chưa thay thế file gốc.
Giữ nguyên mọi fact lịch sử đã verify qua web search trong phiên làm việc trước (Oozie: Yahoo! 2008,
top-level Apache 2012; ZooKeeper: Yahoo Research ~2007, mô phỏng Chubby của Google/Mike Burrows,
ZAB là biến thể Paxos). Mở từ 4 part/6 slide/12 quiz lên 9 part/~27 slide/22 quiz, theo chuẩn
02-module-content-standard.md (9 thành phần bắt buộc, ví dụ ≥2-3 ngành có nhãn (minh hoạ), bảng HTML
thật, giọng văn đa lớp: nôm na → kỹ thuật → bảng/công thức → phép tính từng bước)."""

HD06_EXPANDED = dict(n=30, slug="hd-06-oozie-zookeeper",
 title="Oozie & ZooKeeper: điều phối workflow, và \"xương sống vô hình\" của hệ phân tán",
 tag="Lịch sử Oozie · ZooKeeper (Chubby/ZAB) · Tổng kết chương",
 intro="ZooKeeper là công nghệ ít ai 'nhìn thấy' trực tiếp nhưng gần như MỌI hệ thống phân tán lớn (HBase, Kafka cũ, Solr, Mesos) đều phụ thuộc vào nó để tồn tại. Oozie là lớp điều phối để các job Hadoop không phải chạy rời rạc, thủ công.",
 parts=[

  # ---------------- PHẦN 1: Vì sao cần điều phối workflow ----------------
  dict(title="Nhu cầu về một \"người điều phối\" riêng trong cụm Hadoop", bullets=[
    "Pipeline xử lý dữ liệu thực tế hiếm khi chỉ có 1 job — thường là chuỗi nhiều bước phụ thuộc nhau",
    "Chạy thủ công bằng cron job: dễ vỡ khi 1 bước lỗi hoặc chạy chậm hơn dự kiến",
    "Oozie ra đời ở Yahoo! năm 2008 để giải quyết đúng bài toán này"],
   slides=[
    dict(h="🗣️ Nói nôm na: Oozie", body="""
      <p><b>Nói nôm na:</b> Oozie giống một "quản đốc dây chuyền sản xuất" — nó không tự làm việc gì cả,
      chỉ đứng ra ra lệnh: "bước 2 chỉ được bắt đầu khi bước 1 báo cáo xong, nếu bước 1 lỗi thì dừng cả
      dây chuyền lại, không để sản phẩm lỗi trôi xuống bước sau."</p>
      <p><b>Giải thích kỹ thuật:</b> một pipeline xử lý dữ liệu thực tế hiếm khi chỉ có 1 job MapReduce —
      thường là chuỗi nhiều bước: chạy Sqoop import dữ liệu mới → chạy Hive script làm sạch → chạy job
      MapReduce tổng hợp → gửi email báo cáo hoàn tất. Nếu làm thủ công (cron job gọi lần lượt từng bước),
      rất dễ vỡ khi 1 bước lỗi hoặc chạy chậm hơn dự kiến — bước sau vẫn cứ chạy theo giờ đã đặt, dù dữ
      liệu đầu vào của nó chưa sẵn sàng hoặc bị lỗi.</p>
      {callout_info}
    """.format(callout_info='<div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>Oozie được '
      'phát triển lần đầu tại Yahoo! năm 2008 để giải quyết chính xác bài toán điều phối và lập lịch cho '
      'các triển khai Hadoop quy mô lớn; được mở ra như một dự án Apache (incubator) năm 2011, và trở '
      'thành Apache top-level project năm 2012. Nguồn: '
      '<a href="https://attic.apache.org/projects/oozie.html" target="_blank">Apache Attic — Oozie</a>, '
      '<a href="https://www.dremio.com/wiki/apache-oozie" target="_blank">Dremio — What is Apache Oozie?</a>.</div>')),
    dict(h="Ví dụ minh hoạ ở 3 ngành khác nhau: điều phối nhiều bước phụ thuộc", body="""
      <p>Khái niệm "bước sau chỉ chạy khi bước trước xong" không phải riêng của Big Data — nó xuất hiện ở
      rất nhiều lĩnh vực khác. Ba ví dụ minh hoạ:</p>
      <table><tr><th>Ngành</th><th>Quy trình nhiều bước phụ thuộc (minh hoạ)</th><th>Nếu bỏ qua kiểm tra phụ thuộc</th></tr>
      <tr><td>Sản xuất ô tô</td><td>Lắp khung xe → sơn khung → lắp ghế/nội thất → kiểm tra chất lượng</td>
      <td>Sơn trước khi lắp khung xong → xe bị méo, sơn không đều</td></tr>
      <tr><td>Y tế (minh hoạ)</td><td>Lấy máu xét nghiệm → có kết quả xét nghiệm → bác sĩ kê đơn thuốc</td>
      <td>Kê đơn thuốc trước khi có kết quả xét nghiệm → thuốc không phù hợp, nguy hiểm cho bệnh nhân</td></tr>
      <tr><td>Big Data (đúng bài toán Chương 2)</td><td>Sqoop import → Hive clean → MapReduce tổng hợp → gửi email báo cáo</td>
      <td>Gửi email báo cáo dựa trên dữ liệu chưa được làm sạch → báo cáo sai, người nhận tin tưởng nhầm</td></tr></table>
      <div class="callout warn"><div class="lbl">Bẫy hay gặp khi dùng cron job thay vì Oozie</div>Cron job
      chỉ biết "tới giờ X thì chạy lệnh Y" — nó KHÔNG biết bước trước đã xong hay chưa, đã thành công hay
      thất bại. Oozie khác: nó chủ động KIỂM TRA trạng thái của bước trước rồi mới quyết định chạy bước sau.</div>
    """)]),

  # ---------------- PHẦN 2: DAG & các loại action của Oozie ----------------
  dict(title="DAG là \"ngôn ngữ\" Oozie dùng để mô tả thứ tự phụ thuộc", bullets=[
    "Workflow Oozie là đồ thị có hướng không chu trình (DAG) của các \"action\"",
    "Oozie hỗ trợ nhiều loại action: MapReduce, Pig/Hive script, Java/Shell, SSH, email",
    "DAG ở đây mô tả thứ tự giữa các JOB hoàn chỉnh, khác DAG ở Lập lịch 03 (giữa các TASK nhỏ)"],
   slides=[
    dict(h="🗣️ Nói nôm na: DAG của Oozie so với DAG đã học", body="""
      <p><b>Nói nôm na:</b> nếu DAG ở Lập lịch 03 là "bản vẽ chi tiết từng con vít phải siết trước/sau" bên
      trong 1 cái máy, thì DAG của Oozie là "bản vẽ tổng thể cả nhà máy": công đoạn A (cả 1 cái máy chạy
      xong) → công đoạn B (cả 1 cái máy khác chạy xong) → ... Oozie không quan tâm bên trong mỗi công đoạn
      làm gì, chỉ quan tâm thứ tự giữa các công đoạn.</p>
      <p><b>Giải thích kỹ thuật:</b> Oozie biểu diễn workflow dưới dạng <b>DAG</b> (đồ thị có hướng không
      chu trình) các "action" — đúng khái niệm DAG đã học ở <a href="../ll-03-dag-mapreduce/index.html">
      Lập lịch 03 — Lập lịch DAG, MapReduce và vị trí dữ liệu</a>, nhưng ở đây DAG biểu diễn thứ tự phụ
      thuộc giữa các JOB hoàn chỉnh (1 job MapReduce, 1 script Hive...), không phải giữa các TASK nhỏ trong
      1 job.</p>
      <div class="callout good"><div class="lbl">🔗 Liên hệ trực tiếp</div>Cùng 1 khái niệm toán học (DAG,
      critical path) được áp dụng ở 2 TẦNG khác nhau của hệ thống: tầng task (bên trong 1 job, Lập lịch 03)
      và tầng job (giữa nhiều job, Oozie) — một minh chứng cho việc lý thuyết lập lịch áp dụng được xuyên
      suốt nhiều mức trừu tượng khác nhau của cùng 1 hệ thống thực tế.</div>"""),
    dict(h="Các loại action Oozie hỗ trợ — không chỉ MapReduce", body="""
      <p>Oozie không chỉ điều phối job MapReduce — nó là 1 "nhạc trưởng" điều khiển nhiều loại công việc
      khác nhau trong cùng 1 pipeline:</p>
      <table><tr><th>Loại action</th><th>Dùng để làm gì</th><th>Ví dụ trong pipeline báo cáo doanh số</th></tr>
      <tr><td>MapReduce action</td><td>Chạy 1 job MapReduce thuần</td><td>Tổng hợp doanh số theo khu vực</td></tr>
      <tr><td>Pig/Hive action</td><td>Chạy 1 script PigLatin/HiveQL</td><td>Làm sạch dữ liệu bán hàng thô</td></tr>
      <tr><td>Java action</td><td>Chạy 1 class Java tuỳ ý</td><td>Tính toán nghiệp vụ phức tạp không có sẵn trong Hive</td></tr>
      <tr><td>Shell action</td><td>Chạy 1 lệnh shell trên máy chủ</td><td>Dọn dẹp thư mục tạm sau khi xử lý xong</td></tr>
      <tr><td>SSH action</td><td>Chạy lệnh trên 1 máy chủ khác qua SSH</td><td>Đồng bộ kết quả sang hệ thống báo cáo bên ngoài cụm</td></tr>
      <tr><td>Email action</td><td>Gửi email thông báo</td><td>Báo cáo hoàn tất hoặc báo lỗi cho quản trị viên</td></tr></table>
      <div class="callout info"><div class="lbl">Vì sao điều này quan trọng</div>Một pipeline dữ liệu thật
      hiếm khi "thuần Hadoop" — nó thường phải gọi ra ngoài (script dọn dẹp, gửi email, đồng bộ hệ thống
      khác). Oozie cho phép khai báo TẤT CẢ các bước này trong 1 workflow DUY NHẤT, có kiểm tra phụ thuộc
      xuyên suốt, thay vì phải tự viết 1 script điều phối riêng.</div>""")]),

  # ---------------- PHẦN 3: Workflow có nhánh rẽ (fork/join) ----------------
  dict(title="Khi 2 bước KHÔNG phụ thuộc nhau — fork và join", bullets=[
    "Không phải mọi bước đều phải chạy tuần tự — một số bước có thể chạy song song",
    "Oozie hỗ trợ \"fork\" (tách thành nhiều nhánh song song) và \"join\" (chờ tất cả nhánh xong mới tiếp tục)",
    "Ví dụ: vừa tính báo cáo doanh số VÙA tính báo cáo tồn kho cùng lúc, rồi mới gộp lại gửi email tổng hợp"],
   slides=[
    dict(h="🗣️ Nói nôm na: fork và join", body="""
      <p><b>Nói nôm na:</b> giống việc 2 đầu bếp trong cùng 1 nhà hàng cùng làm 2 món khác nhau cho 1 bàn
      (món khai vị và món chính) CÙNG LÚC, không ai phải chờ ai — nhưng người phục vụ chỉ mang cả 2 món ra
      bàn khi CẢ HAI đều đã xong (đây là "join"). Nếu bắt 2 đầu bếp làm lần lượt (nấu khai vị xong mới nấu
      món chính), khách sẽ phải chờ lâu hơn hẳn mà không có lý do kỹ thuật gì bắt buộc.</p>
      <p><b>Giải thích kỹ thuật:</b> "fork" trong Oozie tách workflow thành nhiều nhánh action chạy SONG
      SONG (không phụ thuộc nhau); "join" là điểm workflow CHỜ tất cả các nhánh đã fork ra hoàn thành rồi
      mới tiếp tục bước kế tiếp. Dùng fork/join khi 2 bước không có quan hệ phụ thuộc dữ liệu thật — chạy
      song song giúp giảm tổng thời gian hoàn thành pipeline (giống Makespan đã học ở Lập lịch 01-02: tận
      dụng nhiều "máy" cùng lúc thay vì xếp hàng 1 máy).</p>
      <div class="callout warn"><div class="lbl">Bẫy hay gặp</div>Fork/join chỉ đúng khi 2 nhánh THỰC SỰ
      độc lập dữ liệu. Nếu nhánh B cần đọc kết quả của nhánh A mà vẫn fork chạy song song, workflow sẽ chạy
      "thành công" về mặt kỹ thuật nhưng cho KẾT QUẢ SAI (B đọc dữ liệu cũ/rỗng của A).</div>"""),
    dict(h="Ví dụ: workflow có fork/join cho pipeline báo cáo doanh số + tồn kho", body="""
      <p>Mở rộng workflow 4 bước tuyến tính đã học (Sqoop → Hive clean → MapReduce → Email) thành workflow
      có nhánh rẽ, khi công ty cần CẢ báo cáo doanh số VÀ báo cáo tồn kho trong 1 lần gửi email:</p>
      <div class="pd-formula"><div class="pd-formula-label">Workflow có fork/join</div>
      <div class="pd-formula-math">\\text{Sqoop import} \\to \\text{Hive clean} \\to \\text{fork}\\begin{cases}\\text{MapReduce doanh số}\\\\\\text{MapReduce tồn kho}\\end{cases}\\to \\text{join} \\to \\text{Gửi email tổng hợp}</div></div>
      <p>Hai nhánh "MapReduce doanh số" và "MapReduce tồn kho" đọc từ 2 bảng dữ liệu ĐỘC LẬP (đã được Hive
      clean chung ở bước trước) — không nhánh nào cần đọc kết quả của nhánh kia, nên fork song song là AN
      TOÀN và giúp pipeline chạy nhanh hơn so với chạy tuần tự 2 nhánh này.</p>
      <table><tr><th>Cách chạy</th><th>Thời gian mỗi nhánh (giả định, minh hoạ)</th><th>Tổng thời gian 2 nhánh</th></tr>
      <tr><td>Tuần tự (không fork)</td><td>Doanh số: 8 phút, Tồn kho: 5 phút</td><td>8+5 = 13 phút</td></tr>
      <tr><td>Song song (có fork/join)</td><td>Doanh số: 8 phút, Tồn kho: 5 phút (chạy cùng lúc)</td><td>max(8,5) = 8 phút</td></tr></table>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Nếu có 1 nhánh thứ 3 "MapReduce báo
      cáo nhân sự" chạy song song, mất 12 phút, tổng thời gian của cả 3 nhánh fork là bao nhiêu?
      (Đáp: max(8,5,12) = 12 phút — join luôn phải chờ nhánh CHẬM NHẤT, giống nguyên lý Makespan.)</div>""")]),

  # ---------------- PHẦN 4: ZooKeeper — nguồn gốc từ Chubby ----------------
  dict(title="ZooKeeper: lấy cảm hứng từ Chubby của Google", bullets=[
    "Ra đời ở Yahoo Research khoảng 2007, mở nguồn trên SourceForge cùng năm",
    "Mô phỏng theo Chubby (Google, paper Mike Burrows) — dịch vụ lock phân tán nội bộ của Google",
    "Vì sao các hệ thống phân tán cần 1 dịch vụ coordination RIÊNG, không tự cài đặt bên trong từng hệ thống"],
   slides=[
    dict(h="🗣️ Nói nôm na: lý do cần ZooKeeper", body="""
      <p><b>Nói nôm na:</b> tưởng tượng 10 công ty con của 1 tập đoàn, mỗi công ty tự thuê 1 nhân viên lễ
      tân riêng để "biết ai đang có mặt trong toà nhà, ai là trưởng phòng hiện tại". Rất tốn kém và dễ sai
      lệch giữa các công ty. Giải pháp: thuê 1 nhân viên lễ tân CHUNG cho cả toà nhà, mọi công ty con hỏi
      người này khi cần biết "ai đang có mặt" hay "ai đang là trưởng phòng" — ZooKeeper chính là nhân viên
      lễ tân chung đó cho các hệ thống phân tán.</p>
      <div class="callout info"><div class="lbl">📚 Nguồn lịch sử</div>ZooKeeper được mô hình hoá theo dịch
      vụ lock Chubby của Google (paper của Mike Burrows), và ban đầu được phát triển tại Yahoo Research
      khoảng năm 2007, mở nguồn trên SourceForge cùng năm đó. Kỹ sư Yahoo (trong đó có Ben Reed và Flavio
      Junqueira) khi đọc paper Chubby nhận thấy đây chính là công cụ có thể giải quyết nhiều vấn đề sản xuất
      ("production problems") họ đang gặp phải, và xây một phiên bản tương đương, tổng quát hoá giao diện
      Chubby thành dịch vụ "coordination-as-a-service" dùng chung cho nhiều hệ thống.
      Nguồn: <a href="https://en.wikipedia.org/wiki/Apache_ZooKeeper" target="_blank">Apache ZooKeeper — Wikipedia</a>.</div>"""),
    dict(h="Ví dụ minh hoạ ở 3 ngành: \"coordination-as-a-service\" không phải khái niệm riêng của Big Data", body="""
      <p>Ý tưởng "1 dịch vụ chung đứng ra điều phối, thay vì mỗi hệ thống tự làm riêng" xuất hiện ở nhiều
      lĩnh vực khác, không chỉ phân tán máy tính:</p>
      <table><tr><th>Ngành</th><th>"Dịch vụ điều phối chung" (minh hoạ)</th><th>Nếu mỗi bên tự làm riêng</th></tr>
      <tr><td>Hàng không</td><td>Đài kiểm soát không lưu (1 đài chung cho mọi máy bay trong vùng)</td>
      <td>Mỗi máy bay tự quyết định độ cao/hướng bay riêng → nguy cơ va chạm rất cao</td></tr>
      <tr><td>Tài chính (minh hoạ)</td><td>Sàn giao dịch chứng khoán (1 nơi chung công bố giá khớp lệnh)</td>
      <td>Mỗi nhà đầu tư tự thoả thuận giá riêng → giá cả hỗn loạn, không ai biết giá "thật" là bao nhiêu</td></tr>
      <tr><td>Hệ thống phân tán (Big Data)</td><td>ZooKeeper (1 dịch vụ chung cho HBase, Kafka cũ, Solr, Mesos...)</td>
      <td>Mỗi hệ thống tự cài thuật toán bầu leader/đồng thuận riêng → dễ sai, tốn công, khó kiểm chứng đúng</td></tr></table>
    """)]),

  # ---------------- PHẦN 5: znode — persistent/ephemeral/sequential ----------------
  dict(title="Znode: \"viên gạch\" dữ liệu mà ZooKeeper quản lý", bullets=[
    "Znode persistent: tồn tại tới khi bị xoá chủ động, giống file thường",
    "Znode ephemeral: tự biến mất khi session tạo ra nó kết thúc (client chết/mất kết nối)",
    "Znode sequential: tự được gắn thêm số thứ tự tăng dần (zxid) khi tạo"],
   slides=[
    dict(h="📖 Giải thích cho người mới bắt đầu: 3 loại znode", body="""
      <details class="explain"><summary>📖 Bấm để xem giải thích đơn giản nhất về znode</summary>
      <p>ZooKeeper tổ chức dữ liệu giống 1 hệ thống thư mục nhỏ (giống cây thư mục của HDFS/UNIX), mỗi "nút"
      trong cây gọi là 1 <b>znode</b>. Có 3 đặc tính znode có thể mang, kết hợp được với nhau:</p>
      <table><tr><th>Loại znode</th><th>Nói nôm na</th><th>Tồn tại tới khi nào</th></tr>
      <tr><td>Persistent (bền)</td><td>Giống 1 tấm bảng thông báo dán cố định trên tường</td>
      <td>Tới khi có ai đó CHỦ ĐỘNG xoá nó</td></tr>
      <tr><td>Ephemeral (tạm thời)</td><td>Giống vé xem phim: chỉ có giá trị khi người giữ vé còn ở trong
      rạp — khách ra khỏi rạp (session kết thúc), vé tự động mất hiệu lực</td>
      <td>Tới khi session (kết nối) của client tạo ra nó bị đóng — dù chủ động (client thoát) hay bị động
      (client sập, mất mạng)</td></tr>
      <tr><td>Sequential (tuần tự)</td><td>Giống số thứ tự rút ở quầy ngân hàng — mỗi lần rút, số luôn LỚN
      HƠN số trước đó, không ai trùng số với ai</td>
      <td>Không ảnh hưởng thời gian sống — chỉ là ZooKeeper tự thêm 1 số (zxid) tăng dần vào TÊN znode khi
      tạo, 2 đặc tính "sequential" và "ephemeral" có thể dùng ĐỒNG THỜI trên cùng 1 znode</td></tr></table>
      <p>Bầu leader bằng "znode tuần tự" (đã học ở phần sau) chính là dùng znode có CẢ 2 đặc tính:
      <b>ephemeral</b> (để tự rớt khỏi cuộc bầu cử khi node đó chết) VÀ <b>sequential</b> (để có 1 con số
      duy nhất, không trùng, dùng so sánh "ai nhỏ hơn").</p>
      </details>"""),
    dict(h="Ví dụ minh hoạ ≥2 ngành: khi nào dùng loại znode nào", body="""
      <table><tr><th>Tình huống</th><th>Loại znode phù hợp</th><th>Vì sao</th></tr>
      <tr><td>Lưu cấu hình hệ thống (vd số lượng region tối đa của HBase)</td><td>Persistent</td>
      <td>Cấu hình phải tồn tại xuyên suốt, không biến mất khi 1 client đọc xong rồi ngắt kết nối</td></tr>
      <tr><td>Đánh dấu "node X đang sống" trong cluster</td><td>Ephemeral</td>
      <td>Nếu node X chết (session ngắt), znode phải TỰ mất đi ngay — không cần ai dọn dẹp thủ công</td></tr>
      <tr><td>Bầu leader giữa nhiều ứng viên</td><td>Ephemeral + Sequential</td>
      <td>Vừa cần tự rớt khi ứng viên chết (ephemeral), vừa cần 1 số thứ tự duy nhất để so sánh (sequential)</td></tr></table>
      <p><b>Ví dụ ở ngành khác (minh hoạ):</b> trong quản lý nhân sự 1 công ty, hồ sơ nhân viên (persistent,
      tồn tại dù nhân viên đang nghỉ phép) khác với "đèn báo đang có mặt tại văn phòng" (ephemeral, tự tắt
      khi nhân viên quẹt thẻ ra khỏi cổng) — cùng 1 hệ thống quản lý nhưng cần 2 loại trạng thái sống khác
      hẳn nhau, giống phân biệt persistent/ephemeral trong ZooKeeper.</p>""")]),

  # ---------------- PHẦN 6: ZAB/Paxos — đồng thuận phân tán ----------------
  dict(title="ZAB: làm sao nhiều node \"đồng ý\" với nhau mà không cần 1 trọng tài tuyệt đối tin cậy", bullets=[
    "ZAB (ZooKeeper Atomic Broadcast) là biến thể của thuật toán Paxos",
    "Nguyên tắc cốt lõi: mọi thay đổi phải được leader đề xuất VÀ đa số (majority) follower xác nhận",
    "Vì sao cần \"đa số\" mà không phải \"tất cả\" — bài toán chịu lỗi khi 1 vài node chết/mất kết nối"],
   slides=[
    dict(h="📖 Giải thích cho người mới bắt đầu: nhu cầu \"đồng thuận\" (consensus)", body="""
      <details class="explain"><summary>📖 Bấm để xem giải thích đơn giản nhất về đồng thuận phân tán</summary>
      <p>Nếu chỉ có 1 máy duy nhất lưu trạng thái hệ thống, không có vấn đề gì — máy đó nói gì cũng là "sự
      thật". Nhưng ZooKeeper chạy trên NHIỀU máy (để chịu lỗi): nếu để từng máy tự quyết định trạng thái
      riêng, các máy có thể "cãi nhau" (máy A nghĩ X là leader, máy B nghĩ Y là leader) — đây gọi là tình
      trạng "split-brain", rất nguy hiểm vì hệ thống phía trên (HBase, Kafka cũ) không biết tin ai.</p>
      <p><b>Giải pháp đồng thuận (Paxos/ZAB):</b> mọi thay đổi trạng thái phải qua 2 bước: (1) 1 node
      <b>leader</b> ĐỀ XUẤT thay đổi, (2) phải có <b>ĐA SỐ</b> (majority, vd 3/5 node) các node
      <b>follower</b> XÁC NHẬN đã nhận được đề xuất đó, mới coi thay đổi là "chính thức". Vì sao là ĐA SỐ
      mà không phải TẤT CẢ? Vì nếu bắt phải 100% node xác nhận, chỉ 1 node chết là toàn hệ thống TÊ LIỆT
      không quyết định được gì nữa — đòi hỏi ĐA SỐ vẫn cho phép hệ thống hoạt động khi có một số node chết,
      miễn số node còn sống vẫn chiếm đa số.</p>
      </details>"""),
    dict(h="Ví dụ minh hoạ ≥2 ngành: vì sao \"đa số\" là lựa chọn đúng, không phải \"tất cả\" hay \"1 người\"", body="""
      <table><tr><th>Ngành</th><th>Cơ chế quyết định (minh hoạ)</th><th>Vấn đề nếu dùng \"1 người quyết\" hoặc \"phải 100% đồng ý\"</th></tr>
      <tr><td>Chính trị/Luật pháp (minh hoạ)</td><td>Quốc hội thông qua luật cần quá bán (&gt;50%) phiếu bầu, không cần 100%</td>
      <td>Nếu cần 100% đồng thuận, chỉ 1 người vắng mặt/phản đối là luật không bao giờ được thông qua</td></tr>
      <tr><td>Y tế (minh hoạ)</td><td>Hội đồng y khoa quyết định phác đồ điều trị phức tạp cần đa số bác sĩ chuyên khoa đồng ý</td>
      <td>Nếu chỉ 1 bác sĩ quyết định (giống "1 leader không ai xác nhận"), rủi ro sai sót cao không có kiểm tra chéo</td></tr>
      <tr><td>Hệ thống phân tán (ZAB/Paxos)</td><td>Leader đề xuất, ĐA SỐ follower xác nhận mới chính thức</td>
      <td>1 leader không kiểm tra chéo → rủi ro sai; bắt 100% đồng ý → 1 node chết là tê liệt cả hệ thống</td></tr></table>
      <div class="callout warn"><div class="lbl">Bẫy hay gặp</div>"Đa số" được tính trên tổng số node CẤU
      HÌNH BAN ĐẦU của cluster, không phải trên số node ĐANG SỐNG tại thời điểm đó — đây là lý do cluster
      ZooKeeper luôn khuyến nghị cấu hình SỐ LẺ node (3, 5, 7): với 5 node, cần tối thiểu 3 xác nhận; nếu 2
      node chết, 3 node còn lại vẫn là "đa số của 5", hệ thống vẫn hoạt động bình thường.</div>""")]),

  # ---------------- PHẦN 7: 4 chức năng cốt lõi ----------------
  dict(title="4 chức năng cốt lõi ZooKeeper cung cấp", bullets=[
    "Quản lý thành viên nhóm, bầu cử leader, quản lý cấu hình động, giám sát trạng thái hệ thống",
    "Mỗi chức năng đều có thể cài đặt riêng cho từng hệ thống — nhưng cài đúng và an toàn rất khó",
    "ZooKeeper là \"thư viện dùng chung\" cho 4 bài toán coordination lặp lại ở hầu hết hệ thống phân tán"],
   slides=[
    dict(h="Bảng 4 chức năng, kèm ví dụ cụ thể ở ≥2 hệ thống khác nhau", body="""
      <table><tr><th>Chức năng</th><th>Ý nghĩa thực tế</th><th>Ví dụ ở HBase</th><th>Ví dụ ở Kafka (bản cũ trước KRaft)</th></tr>
      <tr><td>Quản lý thành viên nhóm (group membership)</td><td>Biết chính xác node nào đang sống trong cluster tại mọi thời điểm</td>
      <td>Biết region server nào đang hoạt động</td><td>Biết broker nào đang hoạt động trong cluster</td></tr>
      <tr><td>Bầu cử leader (leader election)</td><td>Khi node leader cũ chết, nhanh chóng và AN TOÀN chọn ra 1 leader mới duy nhất</td>
      <td>Bầu HMaster (master điều phối region server)</td><td>Bầu Controller broker (quản lý metadata partition)</td></tr>
      <tr><td>Quản lý cấu hình động</td><td>Thay đổi cấu hình hệ thống mà không cần restart từng node</td>
      <td>Cập nhật danh sách region server mà không restart cả cluster</td><td>Cập nhật danh sách topic/partition</td></tr>
      <tr><td>Giám sát trạng thái hệ thống</td><td>Theo dõi sức khoẻ cluster theo thời gian thực</td>
      <td>Phát hiện region server chết để điều phối lại region</td><td>Phát hiện broker chết để điều phối lại partition leader</td></tr></table>
      <div class="callout good"><div class="lbl">Điểm chung quan trọng nhất</div>Cả 4 chức năng đều là bài
      toán "biết đúng sự thật chung" trong 1 hệ thống nhiều máy — đúng chủ đề mà ZAB/Paxos (phần trước) giải
      quyết ở tầng thuật toán nền. ZooKeeper đóng gói sẵn thuật toán khó đó, để HBase/Kafka/Solr không phải
      tự cài đặt lại từ đầu (và dễ sai).</div>""")]),

  # ---------------- PHẦN 8: xương sống vô hình + ví dụ 5 ứng viên ----------------
  dict(title="\"Xương sống vô hình\": khi ZooKeeper lỗi, mọi thứ phía trên đều lỗi theo", bullets=[
    "HBase, Kafka cũ, Solr, Mesos đều phụ thuộc ZooKeeper để coordination",
    "Người dùng cuối không bao giờ \"thấy\" ZooKeeper trực tiếp — nhưng khi nó lỗi, hệ thống phía trên ngừng đúng",
    "Mở rộng ví dụ bầu leader: 5 ứng viên thay vì 3, và khi 2 ứng viên cùng chết liên tiếp"],
   slides=[
    dict(h="🌍 Ảnh hưởng tới thế giới — vì sao gọi là \"xương sống vô hình\"", body="""
      <div class="callout good"><div class="lbl">🌍 Ảnh hưởng tới thế giới</div>ZooKeeper trở thành thành
      phần coordination nền tảng cho rất nhiều hệ thống phân tán lớn: HBase (bầu leader cho region server),
      Kafka bản cũ trước KRaft (quản lý metadata cluster), Apache Solr (coordination cho SolrCloud), Apache
      Mesos (quản lý trạng thái cluster). Phần lớn người dùng cuối không bao giờ "thấy" ZooKeeper trực tiếp
      — nhưng khi ZooKeeper gặp sự cố, toàn bộ hệ thống phía trên (HBase, Kafka cũ...) đều ngừng hoạt động
      đúng. Đây là lý do nó được gọi là "xương sống vô hình" của hệ phân tán.</div>
      <p><b>Ví dụ minh hoạ ở ngành khác (minh hoạ):</b> hệ thống định vị GPS là "xương sống vô hình" của rất
      nhiều ứng dụng hiện đại (bản đồ, gọi xe, giao hàng) — người dùng ứng dụng gọi xe không bao giờ "thấy"
      vệ tinh GPS, nhưng khi tín hiệu GPS yếu/mất, hàng loạt ứng dụng phía trên đều lỗi theo, dù bản thân
      ứng dụng gọi xe không có lỗi code nào.</p>"""),
    dict(h="Ví dụ mở rộng: bầu leader với 5 ứng viên, và khi 2 ứng viên liên tiếp chết", body="""
      <p>Mở rộng ví dụ 3 ứng viên đã học sang 5 ứng viên tạo znode tuần tự:</p>
      <table><tr><th>Ứng viên</th><th>znode được tạo</th></tr>
      <tr><td>Node A</td><td><code>/election/candidate-0000000014</code></td></tr>
      <tr><td>Node B</td><td><code>/election/candidate-0000000009</code></td></tr>
      <tr><td>Node C</td><td><code>/election/candidate-0000000011</code></td></tr>
      <tr><td>Node D</td><td><code>/election/candidate-0000000007</code></td></tr>
      <tr><td>Node E</td><td><code>/election/candidate-0000000016</code></td></tr></table>
      <p><b>Bước 1:</b> số thứ tự nhỏ nhất trong 5 znode trên là 0000000007 (Node D) → <b>Node D là leader</b>.</p>
      <p><b>Bước 2:</b> giả sử Node D chết — znode của D (ephemeral) tự bị xoá. So sánh 4 znode còn lại
      (14, 9, 11, 16) → nhỏ nhất là 9 (Node B) → <b>Node B là leader mới</b>.</p>
      <p><b>Bước 3:</b> ngay sau đó Node B CŨNG chết (2 ứng viên chết liên tiếp) — znode của B tự bị xoá. So
      sánh 3 znode còn lại (14, 11, 16) → nhỏ nhất là 11 (Node C) → <b>Node C là leader mới</b>.</p>
      <div class="callout good"><div class="lbl">Tự kiểm tra ngay</div>Trong suốt quá trình 2 lần chết liên
      tiếp ở trên, có lúc nào hệ thống KHÔNG có leader nào không? (Đáp: Không — mỗi lần 1 znode ephemeral bị
      xoá, ZooKeeper thông báo ngay cho các node còn lại qua watch, việc bầu lại leader mới diễn ra gần như
      lập tức, miễn vẫn còn ĐA SỐ node sống để đạt đồng thuận theo ZAB.)</div>""")]),

  # ---------------- PHẦN 9: TỔNG KẾT CẢ CHƯƠNG (giữ nguyên nội dung gốc) ----------------
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
      "thiết kế" cả hệ sinh thái này từ đầu.</div>""")]),
 ],

 quiz=[
  # --- Oozie (mới) ---
  dict(q="Oozie biểu diễn thứ tự phụ thuộc giữa các bước bằng cấu trúc gì?", opts=[
     "Danh sách tuyến tính đơn giản", "Đồ thị có hướng không chu trình (DAG) của các action",
     "Bảng băm", "Cây nhị phân tìm kiếm"],
   correct=1, explain="DAG của Oozie mô tả thứ tự phụ thuộc giữa các JOB hoàn chỉnh, khác DAG ở Lập lịch 03 (giữa các TASK)."),
  dict(q="Oozie hỗ trợ loại action nào để gửi thông báo khi workflow hoàn tất hoặc lỗi?", opts=["MapReduce action", "Email action", "Shell action", "SSH action"],
   correct=1, explain="Email action là loại action chuyên để gửi thông báo cho người quản trị/người nhận báo cáo."),
  dict(q="Trong workflow có fork/join, 2 nhánh chạy song song để giảm tổng thời gian pipeline. Điều kiện bắt buộc để làm vậy AN TOÀN là gì?", opts=[
     "2 nhánh phải cùng loại action", "2 nhánh phải thực sự độc lập dữ liệu, không nhánh nào đọc kết quả của nhánh kia",
     "2 nhánh phải chạy trên cùng 1 máy", "Không có điều kiện gì, luôn an toàn"],
   correct=1, explain="Nếu nhánh B cần dữ liệu của nhánh A mà vẫn fork song song, workflow sẽ cho kết quả sai (B đọc dữ liệu cũ/rỗng)."),
  dict(q="Với 3 nhánh fork có thời gian chạy 8, 5, 12 phút, tổng thời gian của điểm join là bao nhiêu?", opts=["25 phút (8+5+12)", "12 phút (max của 3 nhánh)", "5 phút (min của 3 nhánh)", "8 phút (trung bình)"],
   correct=1, explain="Join luôn phải chờ nhánh CHẬM NHẤT hoàn thành — đúng nguyên lý Makespan đã học ở Lập lịch 01-02."),
  dict(q="Trong workflow Oozie 4 bước (Sqoop → Hive clean → MapReduce → Email), nếu bước Hive clean thất bại, điều gì xảy ra?", opts=[
     "Oozie vẫn chạy tiếp các bước sau với dữ liệu cũ", "Oozie dừng workflow, không chạy MapReduce/Email, báo lỗi đúng điểm hỏng",
     "Toàn bộ cluster Hadoop dừng hoạt động", "Email báo cáo vẫn được gửi nhưng ghi chú lỗi"],
   correct=1, explain="Lợi ích chính của điều phối workflow có khai báo phụ thuộc rõ ràng, so với chạy cron job thủ công không kiểm tra."),
  # --- ZooKeeper nguồn gốc & znode (mới) ---
  dict(q="ZooKeeper được mô phỏng theo hệ thống nào của Google?", opts=["Bigtable", "GFS", "Chubby (dịch vụ lock phân tán)", "Spanner"],
   correct=2, explain="ZooKeeper dựa trên ý tưởng từ paper Chubby của Mike Burrows (Google)."),
  dict(q="ZooKeeper ra đời ở đâu, khoảng năm nào?", opts=["Yahoo Research, khoảng 2007", "Facebook, 2010", "LinkedIn, 2011", "Powerset, 2008"],
   correct=0, explain="Phát triển ở Yahoo Research khoảng 2007, mở nguồn trên SourceForge cùng năm."),
  dict(q="Znode loại 'ephemeral' tự biến mất khi nào?", opts=[
     "Không bao giờ tự biến mất, phải xoá thủ công", "Khi session (kết nối) của client tạo ra nó kết thúc, dù chủ động hay do client chết",
     "Sau 24 giờ cố định", "Khi ZooKeeper restart"],
   correct=1, explain="Giống vé xem phim: chỉ có giá trị khi người giữ vé (session) còn 'trong rạp' — session kết thúc là znode tự mất."),
  dict(q="Đặc tính 'sequential' của znode nghĩa là gì?", opts=[
     "Znode tự xoá sau 1 khoảng thời gian", "ZooKeeper tự gắn thêm 1 số thứ tự (zxid) tăng dần vào tên znode khi tạo, không trùng ai",
     "Znode chỉ cho phép 1 client truy cập", "Znode luôn là bản sao của znode khác"],
   correct=1, explain="Giống số thứ tự rút ở quầy ngân hàng — luôn tăng dần, không trùng."),
  dict(q="Bầu leader bằng znode tuần tự cần kết hợp 2 đặc tính znode nào?", opts=["Persistent + Sequential", "Ephemeral + Sequential", "Persistent + Ephemeral", "Chỉ cần Sequential"],
   correct=1, explain="Ephemeral để tự rớt khỏi bầu cử khi ứng viên chết, Sequential để có số thứ tự duy nhất dùng so sánh."),
  # --- ZAB/Paxos (mới) ---
  dict(q="ZAB (dùng trong ZooKeeper) là biến thể của thuật toán đồng thuận nào?", opts=["Raft", "Paxos", "Two-Phase Commit", "Gossip protocol"],
   correct=1, explain="ZAB (ZooKeeper Atomic Broadcast) là một biến thể của Paxos."),
  dict(q="Vì sao ZAB/Paxos yêu cầu ĐA SỐ (majority) follower xác nhận, không phải TẤT CẢ?", opts=[
     "Vì đa số nhanh hơn", "Vì nếu bắt 100% xác nhận, chỉ 1 node chết là toàn hệ thống tê liệt không quyết định được gì nữa",
     "Vì ZooKeeper không hỗ trợ xác nhận 100%", "Không có lý do kỹ thuật, chỉ là quy ước"],
   correct=1, explain="Đa số cho phép hệ thống vẫn hoạt động khi có một số node chết, miễn số node sống vẫn chiếm đa số."),
  dict(q="Với cluster ZooKeeper 5 node, cần tối thiểu bao nhiêu node xác nhận để đạt 'đa số'?", opts=["2", "3", "4", "5"],
   correct=1, explain="3/5 là đa số (quá bán) — nếu 2 node chết, 3 node còn lại vẫn đủ đa số để hệ thống tiếp tục hoạt động."),
  dict(q="Tình trạng 'split-brain' trong hệ phân tán là gì?", opts=[
     "Hệ thống chạy quá chậm", "Các node 'cãi nhau' về trạng thái (vd node A nghĩ X là leader, node B nghĩ Y là leader)",
     "Hệ thống hết dung lượng lưu trữ", "Lỗi cú pháp trong code"],
   correct=1, explain="Đây chính là vấn đề mà cơ chế đồng thuận (Paxos/ZAB) được thiết kế để ngăn chặn."),
  # --- 4 chức năng & xương sống vô hình (mới) ---
  dict(q="4 chức năng cốt lõi ZooKeeper cung cấp gồm những gì?", opts=[
     "Lưu trữ file lớn, nén dữ liệu, mã hoá, backup", "Quản lý thành viên nhóm, bầu cử leader, quản lý cấu hình động, giám sát trạng thái hệ thống",
     "Chạy MapReduce, Pig, Hive, Sqoop", "Tạo báo cáo, gửi email, lập lịch cron"],
   correct=1, explain="4 chức năng coordination nền tảng mà nhiều hệ thống phân tán dùng chung qua ZooKeeper."),
  dict(q="Trong HBase, ZooKeeper được dùng để bầu cử thành phần nào?", opts=["DataNode", "HMaster (master điều phối region server)", "NameNode", "JobTracker"],
   correct=1, explain="HMaster là thành phần điều phối trung tâm của HBase, được bầu qua ZooKeeper."),
  dict(q="Hệ thống nào KHÔNG phụ thuộc vào ZooKeeper để coordination (theo nội dung đã học)?", opts=[
     "HBase (bầu leader region server)", "Kafka bản cũ trước KRaft (quản lý metadata cluster)", "Apache Solr (SolrCloud)", "RDBMS truyền thống đơn lẻ không phân tán"],
   correct=3, explain="RDBMS đơn lẻ không cần coordination phân tán kiểu ZooKeeper; HBase/Kafka cũ/Solr/Mesos đều phụ thuộc vào nó."),
  dict(q="Với 5 ứng viên tạo znode tuần tự có zxid 14, 9, 11, 7, 16 — ai là leader ban đầu?", opts=["Node có zxid=16", "Node có zxid=14", "Node có zxid=7", "Node có zxid=9"],
   correct=2, explain="zxid nhỏ nhất (7) là leader."),
  dict(q="Tiếp câu trên: nếu node có zxid=7 chết, rồi node có zxid=9 cũng chết liên tiếp, ai là leader cuối cùng (trong số 14, 11, 16 còn lại)?", opts=["zxid=14", "zxid=11", "zxid=16", "Không còn leader"],
   correct=1, explain="Sau khi loại 7 và 9, zxid nhỏ nhất trong (14, 11, 16) là 11."),
  # --- Tổng kết (giữ nguyên từ bản gốc) ---
  dict(q="Theo dòng thời gian tổng kết, công nghệ nào ra đời SỚM NHẤT làm nền tảng cho cả hệ sinh thái?", opts=[
     "Kafka (LinkedIn)", "2 paper GFS và MapReduce của Google (2003-2004)", "YARN (2012)", "Hive (Facebook)"],
   correct=1, explain="2 paper Google là điểm khởi nguồn, truyền cảm hứng trực tiếp cho Hadoop và hầu hết công nghệ sau đó."),
  dict(q="Bài học lớn nhất rút ra từ việc nhìn lại lịch sử toàn Chương 2 là gì?", opts=[
     "Tất cả công nghệ đều do 1 nhóm ở Google thiết kế sẵn từ đầu", "Hệ sinh thái Hadoop là kết quả của NHIỀU công ty khác nhau giải quyết bài toán nội bộ riêng, rồi mã nguồn mở hoá và ghép lại qua Apache Software Foundation",
     "Mọi công nghệ trong hệ sinh thái đều ra đời cùng 1 năm", "Hệ sinh thái Hadoop không còn công nghệ nào được dùng tới ngày nay"],
   correct=1, explain="Đây là thông điệp tổng kết chính của cả 6 module deep-dive: hệ sinh thái là 'ghép lại' từ nhiều lời giải độc lập, không phải thiết kế tập trung."),
  dict(q="Công nghệ nào trong hệ sinh thái đã chính thức bị 'nghỉ hưu' (Apache Attic), cho thấy không phải mọi thành phần đều tồn tại mãi?", opts=["Hive", "HBase", "Sqoop", "ZooKeeper"],
   correct=2, explain="Sqoop bị retired vào Apache Attic tháng 6/2021, nhường vai trò ETL batch cho các giải pháp CDC streaming."),
 ])
