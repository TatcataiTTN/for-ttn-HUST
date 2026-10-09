# -*- coding: utf-8 -*-
"""10 module "Lập lịch trong hệ thống phân tán", bám sát 100% nội dung lap_lich_50_slides.pdf
(50/50 trang, đã đọc toàn bộ bằng pdftotext trước khi soạn). Mọi số liệu, ví dụ, chứng minh lấy
nguyên từ slide gốc (không tự bịa số liệu); mỗi slide ghi rõ "Nguồn: lap_lich_50_slides.pdf, tr.X".
Cấu trúc dict giống hệt modules_content.py để build_module_page() trong gen_site.py tái dùng được
nguyên vẹn. n tiếp nối từ 15 để không đụng logic 14 buổi cũ."""

SCHED_MODULES = [
# ---------------------------------------------------------------- 15
dict(n=15, slug="ll-01-mo-hinh-lap-lich", title="Mô hình bài toán lập lịch",
 tag="Nhập môn lập lịch · liên hệ Spark/YARN/Kafka",
 intro="Lập lịch nằm ở khắp các tầng của hệ thống phân tán: Spark DAGScheduler/TaskScheduler, "
       "YARN cấp tài nguyên, Kafka gán partition cho consumer. Buổi này xây mô hình toán học chung "
       "trước khi học từng thuật toán cụ thể.",
 parts=[
  dict(title="Lập lịch nằm ở đâu trong hệ thống?", bullets=[
    "Spark DAGScheduler quyết định stage nào đủ điều kiện chạy",
    "Spark TaskScheduler gửi task tới tài nguyên thực thi nào",
    "YARN cấp tài nguyên cho ứng dụng/hàng đợi nào",
    "Kafka consumer group: consumer nào phụ trách partition nào"],
   slides=[
    dict(h="Bốn quyết định lập lịch thật trong hệ phân tán", body="""
      <p>Trước khi học thuật toán, cần thấy lập lịch không phải bài toán lý thuyết suông — nó là quyết định
      thật mà 4 thành phần dưới đây đưa ra liên tục, với những mục tiêu khác nhau, và các tầng có thể cùng
      hoạt động song song.</p>
      <table><tr><th>Thành phần</th><th>Quyết định</th><th>Mô hình liên quan</th></tr>
      <tr><td>Spark DAGScheduler</td><td>Stage nào đã đủ điều kiện chạy?</td><td>Phụ thuộc DAG</td></tr>
      <tr><td>Spark TaskScheduler</td><td>Gửi task đến tài nguyên thực thi nào?</td><td>Phân công tác vụ, vị trí dữ liệu</td></tr>
      <tr><td>Hadoop YARN</td><td>Cấp tài nguyên cho ứng dụng/hàng đợi nào?</td><td>Phân bổ công bằng, giới hạn dung lượng</td></tr>
      <tr><td>Kafka consumer group</td><td>Consumer nào phụ trách partition nào?</td><td>Cân bằng tải, chi phí tái phân công</td></tr></table>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.3 (trích tài liệu Spark/Hadoop/Kafka ở cuối bài).</p>"""),
    dict(h="Job, task và đơn vị thực thi", body="""
      <p><b>Job</b>: một công việc của người dùng, có thể gồm nhiều tác vụ. <b>Task</b>: đơn vị công việc
      được giao cho một tài nguyên thực thi. Trong mô hình toán học, một "máy" chỉ chạy đúng một task tại
      một thời điểm — nhưng một máy vật lý hoặc một Spark executor có thể có <b>nhiều đơn vị thực thi song
      song</b>.</p>
      <div class="callout info"><div class="lbl">Ví dụ quy đổi</div>3 máy vật lý, mỗi máy cho phép chạy 4 task
      đồng thời → mô hình đơn giản có $m = 3 \\times 4 = 12$ đơn vị thực thi.</div>
      <p style="color:var(--muted);font-size:.85rem">Phải xác định rõ "máy" trong mô hình trước khi áp dụng thuật toán.
      Nguồn: lap_lich_50_slides.pdf, tr.4.</p>""")]),
  dict(title="Ký hiệu, mục tiêu và giả thiết", bullets=[
    "n, m, pj, rj, Sj, Cj, wj",
    "Mục tiêu: Cmax, tổng Cj, tổng có trọng số, flow time",
    "Giả thiết quyết định bài toán: offline/online, ngắt/không, độc lập/DAG"],
   slides=[
    dict(h="Ký hiệu chuẩn dùng xuyên suốt", body="""
      <ul class="pd-legend">
      <li><b>n, m</b><span>số tác vụ, số máy</span></li>
      <li><b>$p_j$</b><span>thời gian xử lý tác vụ j</span></li>
      <li><b>$r_j$</b><span>thời điểm tác vụ j đến</span></li>
      <li><b>$S_j, C_j$</b><span>thời điểm bắt đầu, kết thúc</span></li>
      <li><b>$w_j > 0$</b><span>trọng số ưu tiên</span></li></ul>
      <div class="pd-formula"><div class="pd-formula-label">Ba nhóm mục tiêu thường gặp</div>
      <div class="pd-formula-math">\\min C_{max},\\ C_{max}=\\max_j C_j \\quad\\Big|\\quad \\min\\sum_j C_j\\ \\text{hoặc}\\ \\min\\sum_j w_jC_j \\quad\\Big|\\quad \\min\\sum_j (C_j-r_j)</div></div>
      <p style="color:var(--muted);font-size:.85rem">Công bằng cần một định nghĩa riêng về phần tài nguyên được chia (buổi ll-06, ll-07).
      Nguồn: lap_lich_50_slides.pdf, tr.5.</p>"""),
    dict(h="Giả thiết nào cũng làm đổi bài toán", body="""
      <table><tr><th>Câu hỏi</th><th>Các lựa chọn</th></tr>
      <tr><td>Thời điểm biết tin</td><td>Offline: biết trước. Online: chỉ biết khi công việc đến.</td></tr>
      <tr><td>Ngắt tác vụ</td><td>Không ngắt; hoặc ngắt rồi tiếp tục phần còn lại.</td></tr>
      <tr><td>Năng lực máy</td><td>Cùng tốc độ; hoặc thời gian xử lý phụ thuộc máy.</td></tr>
      <tr><td>Phụ thuộc</td><td>Độc lập; hoặc có thứ tự trước-sau theo DAG.</td></tr>
      <tr><td>Chi phí phụ</td><td>Truyền dữ liệu, khởi động, chuyển trạng thái, lỗi máy.</td></tr></table>
      <div class="callout warn"><div class="lbl">Lưu ý phạm vi</div>Các ví dụ trong 10 buổi này là dữ liệu giả
      định để minh hoạ thuật toán. Bảo đảm lý thuyết chỉ đúng dưới đúng giả thiết đã nêu ở từng bài.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.6.</p>""")]),
 ],
 quiz=[
  dict(q="Trong mô hình lập lịch, Spark TaskScheduler quyết định điều gì?",
   opts=["Stage nào đủ điều kiện chạy","Gửi task đến tài nguyên thực thi nào","Cấp tài nguyên cho hàng đợi nào","Consumer nào đọc partition nào"],
   correct=1, explain="DAGScheduler quyết định stage; TaskScheduler mới là nơi gửi task tới tài nguyên thực thi cụ thể."),
  dict(q="3 máy vật lý, mỗi máy chạy song song 4 task, mô hình có bao nhiêu đơn vị thực thi m?",
   opts=["m = 3","m = 4","m = 7","m = 12"], correct=3, explain="m = 3 × 4 = 12, đúng ví dụ slide tr.4."),
  dict(q="$S_j$ và $C_j$ lần lượt là gì?",
   opts=["Số tác vụ và số máy","Thời điểm bắt đầu và kết thúc của tác vụ j","Trọng số và thời gian xử lý","Thời điểm đến và thời gian xử lý"],
   correct=1, explain="S_j: start, C_j: completion — ký hiệu chuẩn slide tr.5."),
  dict(q="Mục tiêu $\\min C_{max}$ nghĩa là gì?",
   opts=["Giảm tổng thời gian xử lý mọi tác vụ","Giảm thời điểm hoàn thành tác vụ kết thúc muộn nhất","Giảm số tác vụ bị trễ","Tăng số máy đang bận"],
   correct=1, explain="C_max = max_j C_j — thời điểm hoàn thành toàn bộ, cần tối thiểu hoá."),
  dict(q="Giả thiết \"online\" trong lập lịch nghĩa là gì?",
   opts=["Biết trước toàn bộ tác vụ ngay từ đầu","Chỉ biết một tác vụ khi nó thực sự đến","Mọi tác vụ chạy trên cùng 1 máy","Tác vụ không bao giờ bị ngắt"],
   correct=1, explain="Offline biết trước, online chỉ biết tin khi công việc đến — ảnh hưởng trực tiếp thuật toán có thể dùng."),
  dict(q="Vì sao phải xác định rõ \"máy\" trong mô hình trước khi áp dụng thuật toán?",
   opts=["Vì thuật toán chỉ chạy được trên máy vật lý","Vì một máy vật lý/Spark executor có thể có nhiều đơn vị thực thi song song, ảnh hưởng số liệu m","Vì lý thuyết không áp dụng được cho cụm ảo hoá","Vì mỗi tác vụ cần một máy riêng biệt"],
   correct=1, explain="m trong mô hình là số 'đơn vị thực thi', không nhất thiết bằng số máy vật lý."),
 ]),

# ---------------------------------------------------------------- 16
dict(n=16, slug="ll-02-list-scheduling-lpt", title="List Scheduling & LPT cho tác vụ độc lập",
 tag="Makespan, 2 cận dưới, bảo đảm xấp xỉ",
 intro="Bài toán nền tảng nhất: n tác vụ độc lập, m máy giống nhau, giảm makespan Cmax. Hai thuật toán "
       "đơn giản — List Scheduling và LPT — đã có bảo đảm xấp xỉ chứng minh được từ 1969.",
 parts=[
  dict(title="Bài toán và hai cận dưới", bullets=[
    "n tác vụ độc lập, m máy giống nhau, giảm Cmax",
    "Cận dưới: W/m và max_j p_j",
    "Ví dụ A-F: m=3, W=30, OPT≥10"],
   slides=[
    dict(h="Bài toán phân công tác vụ độc lập", body="""
      <p>Có n tác vụ, m máy giống nhau. Tất cả tác vụ sẵn sàng tại $t=0$. Mỗi tác vụ chạy liên tục trên đúng
      một máy, bỏ qua chi phí truyền dữ liệu.</p>
      <div class="pd-formula"><div class="pd-formula-label">Mục tiêu</div>
      <div class="pd-formula-math">\\min_{\\{J_1,\\dots,J_m\\}} \\max_{1\\le i\\le m}\\sum_{j\\in J_i} p_j</div></div>
      <table><tr><th>Tác vụ</th><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td></tr>
      <tr><th>$p_j$</th><td>2</td><td>3</td><td>4</td><td>6</td><td>7</td><td>8</td></tr></table>
      <p>$m=3$. Ví dụ này dùng xuyên suốt buổi học — liên hệ: các task độc lập trong 1 stage Spark hoặc 1 pha Map.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.7.</p>"""),
    dict(h="Hai cận dưới cho thời gian tối ưu", body="""
      <div class="pd-formula"><div class="pd-formula-label">OPT ≥</div>
      <div class="pd-formula-math">\\text{OPT} \\ge \\max\\Big(\\tfrac{W}{m}, \\max_j p_j\\Big),\\quad W=\\sum_j p_j</div></div>
      <ul class="pd-legend"><li><b>W/m</b><span>các máy phải chia hết tổng khối lượng công việc</span></li>
      <li><b>$\\max_j p_j$</b><span>một tác vụ không thể chạy nhanh hơn thời gian của chính nó</span></li></ul>
      <p>Với ví dụ: $W=30$, $m=3$, $\\max_j p_j=8$, nên $\\text{OPT}\\ge 10$. Lịch (8+2, 7+3, 6+4) đạt đúng 10,
      nên $\\text{OPT}=10$.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.8.</p>""")]),
  dict(title="Thuật toán List Scheduling", bullets=[
    "Giao tác vụ tiếp theo cho máy đang tải nhỏ nhất",
    "Ví dụ: thứ tự A,B,C,D,E,F → Cmax=12",
    "Bảo đảm (2-1/m)·OPT"],
   slides=[
    dict(h="List Scheduling: giao máy tải nhỏ nhất", body="""
      <ol style="line-height:2">
      <li>Khởi tạo tải $L_i=0$ cho mỗi máy</li>
      <li>Duyệt các tác vụ theo thứ tự đã cho</li>
      <li>Với tác vụ j, chọn i có $L_i$ nhỏ nhất (hoà thì chọn chỉ số nhỏ hơn)</li>
      <li>Đặt $S_j=L_i$, $C_j=L_i+p_j$, cập nhật $L_i\\gets L_i+p_j$</li></ol>
      <p>Với thứ tự A,B,C,D,E,F trong ví dụ: $C_{max}=12$, tỉ lệ $C_{max}/\\text{OPT}=1{,}2$. Thứ tự xét tác vụ
      ảnh hưởng trực tiếp tới kết quả.</p>
      <p style="color:var(--muted);font-size:.85rem">Độ phức tạp: duyệt mọi máy O(nm), dùng min-heap O(m+n log m).
      Nguồn: lap_lich_50_slides.pdf, tr.9-10.</p>"""),
    dict(h="Vì sao List Scheduling bảo đảm gần 2 lần OPT", body="""
      <p>Gọi j là tác vụ kết thúc cuối cùng. Khi giao j, tải nhỏ nhất không vượt tải trung bình của các tác
      vụ đã giao, nên $S_j \\le (W-p_j)/m$.</p>
      <div class="pd-formula"><div class="pd-formula-label">Bảo đảm xấp xỉ (Graham, 1969)</div>
      <div class="pd-formula-math">C_{max} = S_j+p_j \\le \\Big(2-\\tfrac{1}{m}\\Big)\\,\\text{OPT}</div></div>
      <div class="callout good"><div class="lbl">Ý nghĩa</div>Thuật toán cực đơn giản, nhưng có bảo đảm đúng cho
      MỌI bộ dữ liệu hợp lệ — không chỉ trường hợp may mắn.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.11; định lý gốc: Graham (1969).</p>""")]),
  dict(title="LPT và giới hạn của nó", bullets=[
    "Xét tác vụ dài trước: F,E,D,C,B,A → Cmax=10=OPT",
    "Bảo đảm (4/3-1/3m)·OPT",
    "Phản ví dụ: LPT chưa chắc tối ưu"],
   slides=[
    dict(h="LPT: Longest Processing Time first", body="""
      <ol style="line-height:2"><li>Sắp tác vụ theo $p_j$ giảm dần</li>
      <li>Áp dụng List Scheduling theo thứ tự vừa sắp</li></ol>
      <p>Thứ tự mới: F(8), E(7), D(6), C(4), B(3), A(2). Trực giác: xếp khối lớn trước, dùng khối nhỏ lấp phần
      tải còn thiếu. Trong ví dụ, LPT đạt $C_{max}=10=\\text{OPT}$ — cải thiện từ 12 (List Scheduling theo thứ
      tự gốc) xuống 10.</p>
      <div class="pd-formula"><div class="pd-formula-label">Bảo đảm LPT</div>
      <div class="pd-formula-math">C_{max}^{LPT} \\le \\Big(\\tfrac{4}{3}-\\tfrac{1}{3m}\\Big)\\text{OPT}</div></div>
      <p style="color:var(--muted);font-size:.85rem">Chi phí sắp xếp O(n log n), cần biết hoặc ước lượng $p_j$.
      Nguồn: lap_lich_50_slides.pdf, tr.12-13.</p>"""),
    dict(h="LPT có thể chưa tối ưu", body="""
      <p>Hai máy, năm tác vụ có thời gian 3, 3, 2, 2, 2.</p>
      <table><tr><th></th><th>LPT</th><th>Lịch tối ưu</th></tr>
      <tr><td>M1</td><td>3+2+2=7</td><td>3+3=6</td></tr>
      <tr><td>M2</td><td>3+2=5</td><td>2+2+2=6</td></tr></table>
      <p>$C_{max}^{LPT}/\\text{OPT} = 7/6 = 4/3-1/(3\\cdot 2)$ — đúng bằng cận trên lý thuyết, cho thấy bảo đảm
      LPT là <b>chặt</b> (tight), không thể cải thiện thêm bằng phân tích tốt hơn.</p>
      <div class="callout warn"><div class="lbl">Liên hệ Spark/MapReduce</div>Trong một stage đã sẵn sàng, nhiều
      task xử lý các partition khác nhau — kích thước dữ liệu lệch nhau làm thời gian chạy lệch nhau. List
      Scheduling/LPT là mô hình CƠ SỞ để phân tích, không phải mô tả mặc định của Spark TaskScheduler (cần
      thêm vị trí dữ liệu, bộ nhớ, chi phí shuffle — xem buổi ll-03).</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.14-15.</p>""")]),
 ],
 quiz=[
  dict(q="Hai cận dưới của OPT trong bài toán phân công tác vụ độc lập là gì?",
   opts=["n và m","W/m và max_j p_j","W và m","p_j nhỏ nhất và lớn nhất"], correct=1,
   explain="OPT ≥ max(W/m, max_j p_j) — cả hai đều là ràng buộc vật lý không thể vượt qua."),
  dict(q="Với ví dụ A(2),B(3),C(4),D(6),E(7),F(8), m=3, OPT bằng bao nhiêu?",
   opts=["8","9","10","12"], correct=2, explain="W=30, W/m=10, max p_j=8 → OPT≥10, và có lịch đạt đúng 10."),
  dict(q="List Scheduling theo thứ tự A,B,C,D,E,F trong ví dụ cho Cmax bằng bao nhiêu?",
   opts=["10","11","12","13"], correct=2, explain="Cmax=12, tỉ lệ Cmax/OPT=1,2 — đúng số liệu slide tr.9-10."),
  dict(q="LPT theo thứ tự F,E,D,C,B,A trong CÙNG ví dụ đó cho Cmax bằng bao nhiêu?",
   opts=["9","10","11","12"], correct=1, explain="LPT đạt Cmax=10=OPT trong ví dụ này — cải thiện so với thứ tự gốc."),
  dict(q="Bảo đảm xấp xỉ của List Scheduling là gì?",
   opts=["(2-1/m)·OPT","(4/3-1/3m)·OPT","2·OPT đúng với mọi m","OPT đúng tuyệt đối"], correct=0,
   explain="Graham (1969): Cmax ≤ (2-1/m)·OPT cho List Scheduling bất kỳ thứ tự nào."),
  dict(q="Bảo đảm xấp xỉ của LPT là gì?",
   opts=["(2-1/m)·OPT","(4/3-1/3m)·OPT","OPT đúng tuyệt đối","Không có bảo đảm"], correct=1,
   explain="LPT có bảo đảm chặt hơn List Scheduling thường: (4/3-1/3m)·OPT."),
  dict(q="Ví dụ 2 máy, 5 tác vụ (3,3,2,2,2) cho thấy điều gì về LPT?",
   opts=["LPT luôn tối ưu","LPT có thể KHÔNG tối ưu, đạt đúng cận trên lý thuyết 4/3-1/(3m)","LPT luôn tệ hơn List Scheduling thường","LPT không áp dụng được khi m=2"],
   correct=1, explain="Cmax/OPT = 7/6, khớp đúng cận lý thuyết — chứng tỏ bảo đảm LPT là chặt (tight), không chỉ là cận lỏng."),
  dict(q="Vì sao Cmax trong List Scheduling không vượt quá (2-1/m)·OPT?",
   opts=["Vì mọi máy đều có tải bằng nhau","Vì tải nhỏ nhất lúc giao tác vụ cuối không vượt tải trung bình (W-p_j)/m","Vì thuật toán luôn chọn tác vụ ngắn nhất trước","Vì số tác vụ luôn chia hết cho m"],
   correct=1, explain="Đây là lập luận chứng minh cốt lõi ở slide tr.11."),
  dict(q="LPT cần thông tin gì mà List Scheduling thường không bắt buộc?",
   opts=["Số máy m","Biết hoặc ước lượng trước p_j của mọi tác vụ để sắp xếp","Thời điểm đến r_j","Trọng số w_j"],
   correct=1, explain="LPT phải sắp theo p_j giảm dần trước khi chạy, nên cần biết/ước lượng p_j trước."),
 ]),

# ---------------------------------------------------------------- 17
dict(n=17, slug="ll-03-dag-mapreduce", title="Lập lịch DAG, MapReduce và vị trí dữ liệu",
 tag="Critical path, rào chắn Map→Shuffle→Reduce",
 intro="Khi tác vụ có quan hệ trước-sau (DAG), List Scheduling cần thêm quy tắc chọn tác vụ sẵn sàng. "
       "Buổi này còn minh hoạ rào chắn giữa các pha trong MapReduce và quy tắc chọn máy theo vị trí dữ liệu.",
 parts=[
  dict(title="Lập lịch trên DAG", bullets=[
    "DAG: (u,v)∈E ⟹ S_v≥C_u",
    "Ví dụ 6 tác vụ, đường găng A→C→E, OPT≥10",
    "List Scheduling cho DAG: đếm tiền nhiệm, tập sẵn sàng"],
   slides=[
    dict(h="Bài toán lập lịch có quan hệ trước-sau", body="""
      <p>DAG là đồ thị có hướng không chu trình. Cho $G=(V,E)$, đỉnh j là tác vụ có thời gian $p_j$.</p>
      <div class="pd-formula"><div class="pd-formula-label">Ràng buộc thứ tự</div>
      <div class="pd-formula-math">(u,v)\\in E \\implies S_v \\ge C_u</div></div>
      <p>Có m máy giống nhau, mỗi máy chạy 1 tác vụ tại 1 thời điểm, không ngắt, bỏ qua chi phí truyền dữ liệu.
      Mục tiêu vẫn là $\\min C_{max}$. <b>Tác vụ sẵn sàng</b>: chưa chạy và mọi tiền nhiệm đã hoàn thành.</p>
      <div class="callout info"><div class="lbl">Liên hệ</div>DAG của các stage trong Spark, và phụ thuộc giữa
      các pha xử lý, chính là đồ thị này.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.16.</p>"""),
    dict(h="Ví dụ DAG 6 tác vụ và đường găng", body="""
      <p>$m=2$. DAG: A(3)→C(4)→E(3), B(2)→D(2)→F(2) (và các cạnh chéo khác theo slide gốc).
      $W = 3+2+4+2+3+2 = 16$. Đường đi dài nhất (đường găng): A→C→E, tổng $3+4+3=10$.</p>
      <div class="pd-formula"><div class="pd-formula-label">Cận dưới</div>
      <div class="pd-formula-math">\\text{OPT} \\ge \\max\\{W/m, \\text{độ dài đường găng}\\} = \\max\\{8,10\\}=10</div></div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.17.</p>"""),
    dict(h="List Scheduling áp dụng cho DAG", body="""
      <ol style="line-height:2">
      <li>Đếm số tiền nhiệm chưa hoàn thành của từng tác vụ</li>
      <li>Đưa tác vụ có số đếm bằng 0 vào tập sẵn sàng</li>
      <li>Khi có máy rảnh, chọn 1 tác vụ sẵn sàng và cho chạy</li>
      <li>Khi tác vụ kết thúc, giảm số đếm của tác vụ kế tiếp, bổ sung tác vụ mới sẵn sàng</li></ol>
      <p>Trong ví dụ, chạy đúng quy trình này cho $C_{max}=10=\\text{OPT}$ — máy rảnh ở $t=2$ (M2 chờ) là do
      <b>phụ thuộc dữ liệu</b>, không phải thiếu việc tổng thể.</p>
      <div class="callout good"><div class="lbl">Nguyên tắc</div>Không để máy rảnh nếu vẫn có tác vụ sẵn sàng có
      thể chạy.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.18-20.</p>""")]),
  dict(title="MapReduce và vị trí dữ liệu", bullets=[
    "Ưu tiên theo b(v): phần đường găng còn lại",
    "Bảo đảm Cmax ≤ (2-1/m)·OPT cho DAG",
    "Ví dụ MapReduce có rào chắn: Cmax=10",
    "Vị trí dữ liệu: máy rảnh chưa chắc hoàn thành sớm"],
   slides=[
    dict(h="Ưu tiên theo phần đường găng còn lại", body="""
      <p>Đặt $b(v)$ là độ dài đường đi dài nhất bắt đầu tại v (tính cả $p_v$):
      $b(v) = p_v + \\max_{(v,u)\\in E} b(u)$, bằng $p_v$ khi v không có đỉnh kế tiếp.</p>
      <p>Tính $b(v)$ theo thứ tự tô pô đảo trong $O(|V|+|E|)$. Khi chọn trong tập sẵn sàng, ưu tiên tác vụ có
      $b(v)$ lớn hơn. Đây là quy tắc chọn trong List Scheduling, <b>không bảo đảm tối ưu mọi DAG</b> nhưng giúp
      ưu tiên đúng các tác vụ nằm trên đường găng.</p>
      <div class="pd-formula"><div class="pd-formula-label">Bảo đảm cho DAG (chi phí truyền dữ liệu = 0)</div>
      <div class="pd-formula-math">C_{max} \\le \\tfrac{W}{m} + \\Big(1-\\tfrac1m\\Big)L \\le \\Big(2-\\tfrac1m\\Big)\\text{OPT}</div></div>
      <p style="color:var(--muted);font-size:.85rem">L: độ dài đường găng. Kết quả cổ điển của Graham.
      Nguồn: lap_lich_50_slides.pdf, tr.20-21.</p>"""),
    dict(h="Ví dụ MapReduce: rào chắn giữa các pha", body="""
      <p>2 chỗ chạy task, 4 task Map dài 4,3,2,1. Sau toàn bộ Map là 1 pha shuffle dài 2, rồi 2 task Reduce
      dài 3,2.</p>
      <div class="pd-formula"><div class="pd-formula-label">Makespan</div>
      <div class="pd-formula-math">C_{max} = \\underbrace{5}_{\\text{Map bằng LPT}} + \\underbrace{2}_{\\text{shuffle}} + \\underbrace{3}_{\\text{Reduce}} = 10</div></div>
      <div class="callout warn"><div class="lbl">Mô hình giảng dạy</div>Trong Hadoop thực tế, một phần shuffle
      có thể chồng lấp với Map — ví dụ này cố ý dùng rào chắn cứng để tính được bằng tay.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.22-23.</p>"""),
    dict(h="Vị trí dữ liệu: máy rảnh chưa chắc hoàn thành sớm", body="""
      <p>Một task cần 4 đơn vị xử lý, dữ liệu nằm ở M1.</p>
      <table><tr><th>Lựa chọn</th><th>Chờ máy</th><th>Lấy dữ liệu</th><th>Kết thúc</th></tr>
      <tr><td>Chạy tại M1</td><td>3</td><td>0</td><td>3+0+4=7</td></tr>
      <tr><td>Chạy tại M2</td><td>0</td><td>5</td><td>0+5+4=9</td></tr></table>
      <p>Quy tắc tham lam: chọn máy có $\\hat C_i = \\text{thời gian chờ}+\\text{thời gian lấy dữ liệu}+p_j$ nhỏ
      nhất. Nếu thời gian lấy dữ liệu ở M2 chỉ là 1, nên chọn M2 vì $1+4=5 < 7$.</p>
      <div class="callout info"><div class="lbl">Liên hệ</div>Đây chính là nguyên tắc ưu tiên dữ liệu cục bộ
      (data locality) trong Spark DAGScheduler/Hadoop — mô hình dự báo đơn giản, không phải cơ chế thật đầy đủ.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.24.</p>""")]),
 ],
 quiz=[
  dict(q="Ràng buộc DAG (u,v)∈E nghĩa là gì?",
   opts=["S_v ≥ C_u (v chỉ bắt đầu sau khi u hoàn thành)","u phải chạy sau v","u và v phải chạy cùng lúc","Không có ràng buộc thứ tự"],
   correct=0, explain="Cạnh (u,v) nghĩa là v phụ thuộc u, chỉ bắt đầu khi u đã xong."),
  dict(q="Tác vụ \"sẵn sàng\" trong lập lịch DAG nghĩa là gì?",
   opts=["Đã chạy xong","Chưa chạy và mọi tiền nhiệm đã hoàn thành","Có thời gian xử lý ngắn nhất","Nằm trên đường găng"],
   correct=1, explain="Đúng định nghĩa slide tr.16."),
  dict(q="Trong ví dụ DAG 6 tác vụ (m=2), đường găng là đường nào và độ dài bao nhiêu?",
   opts=["B→D→F, độ dài 6","A→C→E, độ dài 10","A→D→F, độ dài 7","Không có đường găng"],
   correct=1, explain="A(3)→C(4)→E(3), tổng 3+4+3=10, đúng số liệu slide tr.17."),
  dict(q="b(v) trong quy tắc ưu tiên DAG được định nghĩa thế nào?",
   opts=["Số tiền nhiệm của v","Độ dài đường đi dài nhất bắt đầu tại v, tính cả p_v","Thời gian xử lý trung bình","Số lượng hậu duệ của v"],
   correct=1, explain="b(v) = p_v + max b(u) trên các cạnh (v,u) — dùng để ưu tiên tác vụ nằm trên đường găng."),
  dict(q="Trong ví dụ MapReduce có rào chắn (Map LPT=5, shuffle=2, Reduce=3), Cmax bằng bao nhiêu?",
   opts=["8","9","10","12"], correct=2, explain="Cmax = 5+2+3 = 10, do rào chắn cứng giữa các pha (mô hình giảng dạy)."),
  dict(q="Trong ví dụ vị trí dữ liệu, vì sao nên chạy task tại M2 dù dữ liệu nằm ở M1?",
   opts=["M2 luôn nhanh hơn M1","Nếu thời gian lấy dữ liệu ở M2 đủ nhỏ, tổng thời gian (chờ+lấy dữ liệu+xử lý) có thể nhỏ hơn chạy tại M1","M1 đang hỏng","Luật bắt buộc chạy tại máy có ít tải nhất"],
   correct=1, explain="Quy tắc tham lam so sánh Ĉ_i = chờ + lấy dữ liệu + p_j giữa các lựa chọn, không mặc định ưu tiên máy có dữ liệu."),
  dict(q="Bảo đảm xấp xỉ của List Scheduling trên DAG (chi phí truyền dữ liệu = 0) là gì?",
   opts=["(2-1/m)·OPT, giống hệt trường hợp tác vụ độc lập","OPT đúng tuyệt đối","(4/3)·OPT","Không có bảo đảm nào cho DAG"],
   correct=0, explain="Cmax ≤ W/m + (1-1/m)L ≤ (2-1/m)·OPT — cùng dạng bảo đảm với tác vụ độc lập."),
 ]),

# ---------------------------------------------------------------- 18
dict(n=18, slug="ll-04-fifo-spt-smith", title="FIFO, SPT và quy tắc Smith",
 tag="Tổng thời gian hoàn thành trên 1 máy",
 intro="Trên một máy, thứ tự chạy không đổi makespan nhưng thay đổi mạnh tổng thời gian hoàn thành. "
       "SPT và quy tắc Smith là hai kết quả tối ưu kinh điển, chứng minh được bằng lập luận đổi chỗ.",
 parts=[
  dict(title="Bài toán và FIFO", bullets=[
    "1 máy, giảm tổng Cj",
    "Ví dụ A(10),B(1),C(1): FIFO cho tổng 33",
    "Makespan không đổi, nhưng tổng Cj thay đổi mạnh theo thứ tự"],
   slides=[
    dict(h="Bài toán trên 1 máy: giảm tổng thời gian hoàn thành", body="""
      <p>Một máy, các tác vụ độc lập đều sẵn sàng tại $t=0$, không bị ngắt.</p>
      <div class="pd-formula"><div class="pd-formula-label">Mục tiêu</div>
      <div class="pd-formula-math">\\min \\sum_{j=1}^n C_j</div></div>
      <p>Tối thiểu hoá tổng này cũng tối thiểu hoá trung bình $\\tfrac1n\\sum_j C_j$.</p>
      <table><tr><th>Tác vụ</th><td>A</td><td>B</td><td>C</td></tr><tr><th>$p_j$</th><td>10</td><td>1</td><td>1</td></tr></table>
      <p>Tổng thời gian xử lý luôn là 12, makespan (không khoảng rảnh) luôn là 12 — nhưng <b>thứ tự chạy vẫn
      làm thay đổi mạnh tổng thời gian hoàn thành</b>.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.25.</p>"""),
    dict(h="FIFO: xử lý theo thứ tự vào hàng đợi", body="""
      <p>Khi máy rảnh, lấy công việc ở đầu hàng đợi. Thứ tự A,B,C:</p>
      <p>$(C_A,C_B,C_C)=(10,11,12)$, $\\sum_j C_j = 33$, trung bình $33/3=11$.</p>
      <div class="callout info"><div class="lbl">Liên hệ</div>Spark có chế độ FIFO giữa các job trong một
      SparkContext — cơ chế nhiều task của Spark phức tạp hơn hàng đợi một máy này.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.26.</p>""")]),
  dict(title="SPT và quy tắc Smith", bullets=[
    "SPT: ngắn trước, tổng giảm còn 15",
    "Chứng minh tối ưu bằng đổi chỗ",
    "Smith: ưu tiên theo p_j/w_j tăng dần"],
   slides=[
    dict(h="SPT: công việc ngắn chạy trước", body="""
      <ol style="line-height:2"><li>Sắp tác vụ theo $p_j$ tăng dần</li><li>Chạy lần lượt theo thứ tự đó — $O(n\\log n)$</li></ol>
      <p>Thứ tự B,C,A: $(C_B,C_C,C_A)=(1,2,12)$, $\\sum_j C_j=15$. Trung bình giảm từ 11 xuống 5 — makespan vẫn
      bằng 12, chỉ tổng thời gian hoàn thành đổi.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.27.</p>"""),
    dict(h="Chứng minh SPT tối ưu bằng đổi chỗ", body="""
      <p>Xét 2 tác vụ kề nhau a, b bắt đầu từ thời điểm t, với $p_a>p_b$.</p>
      <div class="pd-formula"><div class="pd-formula-label">So sánh 2 thứ tự</div>
      <div class="pd-formula-math">\\text{Chạy } a\\text{ rồi }b: 2t+2p_a+p_b \\quad|\\quad \\text{Chạy }b\\text{ rồi }a: 2t+2p_b+p_a</div></div>
      <p>Đổi chỗ a,b làm tổng giảm một lượng $p_a-p_b>0$. Tác vụ trước cặp này không đổi, tổng độ dài cặp vẫn
      bằng $p_a+p_b$ nên tác vụ phía sau không bị ảnh hưởng. Loại bỏ mọi cặp ngược thứ tự sẽ thu được lịch SPT
      tối ưu — SPT là trường hợp mọi trọng số bằng nhau của quy tắc Smith.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.28.</p>"""),
    dict(h="Smith: ưu tiên theo thời gian chia trọng số", body="""
      <p>Mỗi tác vụ có trọng số $w_j>0$, mục tiêu $\\min\\sum_j w_jC_j$.</p>
      <div class="pd-formula"><div class="pd-formula-label">Quy tắc Smith</div>
      <div class="pd-formula-math">\\text{Sắp theo } p_j/w_j \\text{ tăng dần}</div></div>
      <p>Ví dụ: A($p{=}6,w{=}1$), B($p{=}3,w{=}3$), C($p{=}2,w{=}2$). Thứ tự A,B,C cho $\\sum w_jC_j=55$; theo
      Smith (B,C,A) chỉ còn $30$.</p>
      <div class="callout warn"><div class="lbl">Lưu ý</div>Trọng số $w_j$ ở đây (mức ưu tiên công việc) khác với
      trọng số chia tài nguyên trong lập lịch công bằng (buổi ll-06, ll-07).</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.28-29.</p>""")]),
 ],
 quiz=[
  dict(q="Trong ví dụ A(10),B(1),C(1), FIFO theo thứ tự A,B,C cho tổng Cj bằng bao nhiêu?",
   opts=["15","24","33","36"], correct=2, explain="(C_A,C_B,C_C)=(10,11,12), tổng = 33, đúng slide tr.26."),
  dict(q="SPT theo thứ tự B,C,A trong CÙNG ví dụ đó cho tổng Cj bằng bao nhiêu?",
   opts=["12","15","24","33"], correct=1, explain="(C_B,C_C,C_A)=(1,2,12), tổng = 15 — giảm hơn một nửa so với FIFO."),
  dict(q="Makespan trong ví dụ A(10),B(1),C(1) có đổi theo thứ tự chạy không?",
   opts=["Có, makespan đổi theo thứ tự","Không, makespan luôn bằng tổng p_j = 12 vì không có khoảng rảnh","Chỉ đổi khi dùng SPT","Chỉ đổi khi dùng FIFO"],
   correct=1, explain="Makespan trên 1 máy không khoảng rảnh luôn bằng tổng thời gian xử lý, bất kể thứ tự."),
  dict(q="Lập luận chứng minh SPT tối ưu dựa trên kỹ thuật gì?",
   opts=["Quy hoạch động","Đổi chỗ (exchange argument) hai tác vụ kề nhau","Chia để trị","Quy nạp trên số máy"],
   correct=1, explain="So sánh tổng C_a+C_b giữa 2 thứ tự liền kề, chứng minh đổi chỗ cặp ngược thứ tự luôn làm giảm tổng."),
  dict(q="Quy tắc Smith sắp tác vụ theo tiêu chí nào?",
   opts=["p_j tăng dần","w_j giảm dần","p_j/w_j tăng dần","w_j/p_j tăng dần"], correct=2,
   explain="Sắp theo tỉ số p_j/w_j tăng dần — SPT là trường hợp đặc biệt khi mọi w_j bằng nhau."),
  dict(q="Trong ví dụ Smith (A: p=6,w=1; B: p=3,w=3; C: p=2,w=2), tổng w_jC_j tối ưu (thứ tự B,C,A) là bao nhiêu?",
   opts=["30","40","55","60"], correct=0, explain="Σw_jC_j = 3·3+2·5+1·11 = 30, đúng số liệu slide tr.29."),
  dict(q="Trọng số w_j trong quy tắc Smith khác gì với trọng số trong lập lịch công bằng (DRF)?",
   opts=["Không có gì khác, cùng một khái niệm","w_j của Smith là mức ưu tiên công việc, còn DRF dùng để chia phần tài nguyên công bằng giữa người dùng","DRF không dùng trọng số","Smith chỉ áp dụng khi w_j=0"],
   correct=1, explain="Hai khái niệm trọng số phục vụ hai mục tiêu khác nhau — lưu ý được nêu rõ ở slide tr.29."),
 ]),

# ---------------------------------------------------------------- 19
dict(n=19, slug="ll-05-srpt", title="SRPT và hàng đợi công việc động",
 tag="Lập lịch ngắt được, liên hệ Spark FIFO/FAIR",
 intro="Khi công việc đến tại các thời điểm khác nhau và được phép ngắt, SRPT (Shortest Remaining "
       "Processing Time) tối ưu tổng thời gian trong hệ thống — nền tảng lý thuyết cho hàng đợi công việc thật.",
 parts=[
  dict(title="SRPT: công việc đến theo thời gian", bullets=[
    "Ngắt được, luôn ưu tiên thời gian còn lại nhỏ nhất",
    "Ví dụ A(0,8), B(1,2): SRPT=12, FIFO=17",
    "SRPT tối ưu tổng (Cj-rj)"],
   slides=[
    dict(h="SRPT: ưu tiên thời gian còn lại nhỏ nhất", body="""
      <p>Một máy, biết $p_j$ khi công việc đến. Cho phép ngắt và tiếp tục, không mất chi phí. SRPT: luôn chạy
      công việc đã đến có thời gian xử lý <b>còn lại</b> nhỏ nhất.</p>
      <p>Ví dụ: $A:(r_A,p_A)=(0,8)$, $B:(r_B,p_B)=(1,2)$. SRPT chạy A từ 0→1, ngắt để chạy B từ 1→3 (ngắn hơn
      phần còn lại của A), rồi tiếp tục A từ 3→10.</p>
      <div class="pd-formula"><div class="pd-formula-label">Tổng thời gian trong hệ thống</div>
      <div class="pd-formula-math">\\sum_j (C_j-r_j) = (10-0)+(3-1) = 12</div></div>
      <p>FIFO không ngắt: A chạy [0,8], B chạy [8,10], tổng $= 8+9=17$ — tệ hơn SRPT đáng kể.</p>
      <div class="callout good"><div class="lbl">Kết quả</div>SRPT tối ưu tổng thời gian trong hệ thống dưới các
      giả thiết trên (Schrage, 1968). Không áp dụng trực tiếp khi có trọng số hoặc chi phí ngắt.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.30.</p>""")]),
  dict(title="Liên hệ với hàng đợi công việc thật", bullets=[
    "Bảng so sánh FIFO/SPT/Smith/SRPT/FAIR",
    "Spark có FIFO và FAIR, không có SRPT trực tiếp"],
   slides=[
    dict(h="Bốn chính sách, bốn loại thông tin cần có", body="""
      <table><tr><th>Chính sách</th><th>Thông tin cần có</th><th>Cách dùng mô hình</th></tr>
      <tr><td>FIFO</td><td>Thứ tự đến</td><td>Chính sách cơ sở dễ triển khai</td></tr>
      <tr><td>SPT / Smith</td><td>Ước lượng thời gian, thêm trọng số với Smith</td><td>So sánh độ trễ của các yêu cầu</td></tr>
      <tr><td>SRPT</td><td>Thời gian còn lại và khả năng ngắt</td><td>Mô hình lý tưởng cho công việc đến động</td></tr>
      <tr><td>FAIR</td><td>Phần tài nguyên của job/pool</td><td>Chia sẻ tài nguyên giữa nhiều công việc</td></tr></table>
      <div class="callout warn"><div class="lbl">Lưu ý quan trọng</div>Spark có FIFO và FAIR giữa các job trong
      một SparkContext. <b>Không thể suy ra</b> rằng bật FAIR sẽ thực thi SPT hoặc SRPT — đây là các chính sách
      khác nhau về bản chất, chỉ là mô hình phân tích để so sánh khái niệm.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.31-32.</p>""")]),
 ],
 quiz=[
  dict(q="SRPT luôn ưu tiên chạy công việc nào?",
   opts=["Đến trước nhất","Có thời gian xử lý còn lại nhỏ nhất trong số đã đến","Có trọng số lớn nhất","Có thời gian xử lý tổng lớn nhất"],
   correct=1, explain="Đúng định nghĩa: Shortest Remaining Processing Time."),
  dict(q="Trong ví dụ A(0,8), B(1,2), SRPT cho tổng (Cj-rj) bằng bao nhiêu?",
   opts=["10","12","15","17"], correct=1, explain="(10-0)+(3-1)=12, đúng slide tr.30."),
  dict(q="FIFO không ngắt cho CÙNG ví dụ A(0,8),B(1,2) cho tổng (Cj-rj) bằng bao nhiêu?",
   opts=["12","15","17","20"], correct=2, explain="A chạy [0,8], B chạy [8,10]: tổng = 8+9 = 17."),
  dict(q="SRPT tối ưu dưới giả thiết nào?",
   opts=["Biết độ dài tác vụ, ngắt được và không mất chi phí ngắt","Không cần biết độ dài tác vụ trước","Chỉ áp dụng khi có trọng số","Chỉ áp dụng cho DAG"],
   correct=0, explain="Kết quả Schrage (1968) yêu cầu đúng các giả thiết này — không áp dụng trực tiếp khi có trọng số/chi phí ngắt."),
  dict(q="Spark Job Scheduling hỗ trợ trực tiếp SRPT giữa các job không?",
   opts=["Có, SRPT là chính sách mặc định","Không — Spark chỉ có FIFO và FAIR, không suy ra được là đang chạy SRPT/SPT","Có, nhưng chỉ khi bật chế độ Dynamic Allocation","Không liên quan tới Spark"],
   correct=1, explain="Lưu ý rõ ở slide tr.31-32: không được suy diễn bật FAIR tương đương SRPT/SPT."),
 ]),

# ---------------------------------------------------------------- 20
dict(n=20, slug="ll-06-cong-bang-tai-nguyen", title="Công bằng tài nguyên: max-min & progressive filling",
 tag="Chia 1 loại tài nguyên",
 intro="Khi nhiều người dùng/hàng đợi chia một cụm dùng chung, cần một định nghĩa chặt chẽ về 'công bằng'. "
       "Max-min fairness và thuật toán progressive filling là nền tảng trước khi học DRF (buổi sau).",
 parts=[
  dict(title="Max-min fairness và progressive filling", bullets=[
    "Bài toán: B tổng tài nguyên, nhu cầu d_i mỗi người",
    "Công bằng max-min: không tăng người này mà không giảm người đang nhận ít hơn",
    "Progressive filling: tăng đều tới khi đạt nhu cầu"],
   slides=[
    dict(h="Bài toán chia một loại tài nguyên", body="""
      <p>Tổng tài nguyên $B$. Người dùng i có nhu cầu tối đa $d_i$. Chọn lượng cấp $x_i$ sao cho
      $0\\le x_i\\le d_i$ và $\\sum_i x_i \\le B$.</p>
      <div class="pd-formula"><div class="pd-formula-label">Công bằng max-min</div>
      <div class="pd-formula-math">\\text{Không thể tăng } x_i \\text{ mà không giảm } x_k \\text{ của người } k \\text{ đang nhận} \\le x_i</div></div>
      <p>Ví dụ: $B=12$ CPU, ba người dùng $(d_1,d_2,d_3)=(2,8,8)$. Chia đều 4 mỗi người vượt nhu cầu người 1 —
      cần phân phối lại phần dư.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.33.</p>"""),
    dict(h="Progressive filling: tăng đều phần cấp", body="""
      <ol style="line-height:2"><li>Ban đầu cấp 0 cho mọi người</li>
      <li>Tăng đều phần cấp của người chưa đạt nhu cầu</li>
      <li>Khi một người đạt nhu cầu, giữ nguyên phần cấp người đó</li>
      <li>Tiếp tục đến khi hết tài nguyên hoặc mọi nhu cầu đều đủ</li></ol>
      <table><tr><th>Giai đoạn</th><th>$x_1$</th><th>$x_2$</th><th>$x_3$</th><th>Tổng</th></tr>
      <tr><td>Tăng đều đến mức 2</td><td>2</td><td>2</td><td>2</td><td>6</td></tr>
      <tr><td>Giữ người 1, chia 6 còn lại</td><td>2</td><td>5</td><td>5</td><td>12</td></tr></table>
      <div class="pd-formula"><div class="pd-formula-label">Công thức</div>
      <div class="pd-formula-math">x_i = \\min\\{d_i,\\lambda\\},\\quad \\lambda=5</div></div>
      <p style="color:var(--muted);font-size:.85rem">Với nhu cầu đã biết, có thể sắp các $d_i$ để tính mức tăng
      trong $O(n\\log n)$. Nguồn: lap_lich_50_slides.pdf, tr.34.</p>""")]),
 ],
 quiz=[
  dict(q="Công bằng max-min nghĩa là gì?",
   opts=["Mọi người nhận đúng bằng nhau","Không thể tăng phần cấp của một người mà không giảm phần của người đang nhận ít hơn hoặc bằng", "Người có nhu cầu cao nhất luôn được ưu tiên","Tổng tài nguyên luôn được dùng hết"],
   correct=1, explain="Đúng định nghĩa chuẩn slide tr.33."),
  dict(q="Với B=12, (d1,d2,d3)=(2,8,8), progressive filling cho kết quả cuối cùng (x1,x2,x3) là gì?",
   opts=["(4,4,4)","(2,5,5)","(2,8,2)","(0,6,6)"], correct=1, explain="x_i=min(d_i,λ), λ=5 → (2,5,5), tổng=12, đúng slide tr.34."),
  dict(q="Trong progressive filling, điều gì xảy ra khi một người đạt đúng nhu cầu d_i?",
   opts=["Người đó bị loại khỏi hệ thống","Phần cấp của người đó được GIỮ NGUYÊN, phần tăng đều tiếp tục dồn cho người chưa đủ","Người đó nhận thêm gấp đôi","Toàn bộ quá trình dừng lại"],
   correct=1, explain="Bước 3 của thuật toán: giữ nguyên phần cấp của người đã đạt nhu cầu."),
  dict(q="Độ phức tạp tính các mức tăng trong progressive filling khi đã biết nhu cầu là bao nhiêu?",
   opts=["O(n)","O(n log n)","O(n²)","O(2ⁿ)"], correct=1, explain="Có thể sắp các d_i để tính mức tăng trong O(n log n), theo slide tr.34."),
 ]),

# ---------------------------------------------------------------- 21
dict(n=21, slug="ll-07-drf", title="DRF — Dominant Resource Fairness",
 tag="Nhiều loại tài nguyên, liên hệ YARN/Spark FAIR",
 intro="Khi cụm có nhiều loại tài nguyên (CPU, RAM...) và người dùng có nhu cầu lệch nhau, chia công bằng "
       "một loại tài nguyên có thể làm loại khác quá tải. DRF (Ghodsi và cộng sự, NSDI 2011) giải quyết việc này.",
 parts=[
  dict(title="Mô hình DRF và dominant share", bullets=[
    "d loại tài nguyên, dominant share s_i = max_r (x_i a_ir / R_r)",
    "DRF: max-min fairness trên dominant share",
    "Ví dụ: 9 CPU, 18GB RAM, 2 người dùng"],
   slides=[
    dict(h="Bài toán chia nhiều loại tài nguyên", body="""
      <p>Có $d$ loại tài nguyên, loại r có dung lượng $R_r$. Một task của người dùng i cần $a_{ir}$ đơn vị tài
      nguyên loại r. $x_i$ là số task của người dùng i được cấp đồng thời.</p>
      <div class="pd-formula"><div class="pd-formula-label">Ràng buộc & dominant share</div>
      <div class="pd-formula-math">\\sum_i x_i a_{ir} \\le R_r \\ (\\forall r), \\qquad s_i = \\max_r \\frac{x_i a_{ir}}{R_r}</div></div>
      <p><b>DRF</b>: thực hiện công bằng max-min trên các dominant share $s_i$ thay vì trên từng loại tài nguyên
      riêng lẻ.</p>
      <div class="callout warn"><div class="lbl">Vì sao cần DRF</div>Người dùng có thể thiên về CPU hoặc RAM —
      chia công bằng 1 loại tài nguyên đơn lẻ có thể làm loại khác quá tải hoặc lãng phí.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.34-35; Ghodsi và cộng sự (2011), NSDI.</p>"""),
    dict(h="Ví dụ DRF: hai người dùng, nhu cầu khác nhau", body="""
      <p>Cụm có 9 CPU, 18GB RAM. Hai người dùng đủ task để tiếp tục nhận tài nguyên.</p>
      <table><tr><th>Người dùng</th><th>CPU/task</th><th>RAM/task</th><th>Tài nguyên trội</th></tr>
      <tr><td>A</td><td>1</td><td>4GB</td><td>RAM: 4/18 &gt; 1/9</td></tr>
      <tr><td>B</td><td>3</td><td>1GB</td><td>CPU: 3/9 &gt; 1/18</td></tr></table>
      <p>$s_A = 2x_A/9$, $s_B=x_B/3$. Ràng buộc khả thi: $x_A+3x_B\\le 9$, $4x_A+x_B\\le 18$.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.35.</p>""")]),
  dict(title="Tính DRF và liên hệ YARN/Spark", bullets=[
    "Tăng đều dominant share: s=2/3, (xA,xB)=(3,2)",
    "Cấp phát theo từng task, chọn s_i nhỏ nhất",
    "YARN Fair/Capacity Scheduler, Spark FAIR"],
   slides=[
    dict(h="Tăng đều dominant share chung", body="""
      <p>Đặt dominant share chung bằng $s$: $x_A=\\tfrac92 s$, $x_B=3s$. Thay vào 2 ràng buộc:</p>
      <div class="pd-formula"><div class="pd-formula-label">CPU đầy trước</div>
      <div class="pd-formula-math">\\tfrac92 s + 9s \\le 9 \\Rightarrow s\\le\\tfrac23 \\quad(\\text{RAM cho }s\\le\\tfrac67)</div></div>
      <p>CPU đầy trước nên $s=2/3$, suy ra $x_A=3$, $x_B=2$. Tổng sử dụng: $3+3\\cdot2=9$ CPU và $4\\cdot3+2=14$
      GB RAM. Hai người có <b>cùng dominant share</b> nhưng số task được cấp khác nhau.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.36.</p>"""),
    dict(h="DRF theo từng task — cấp phát rời rạc", body="""
      <p>Quy tắc: chọn người có $s_i$ nhỏ nhất trong số có task vừa tài nguyên còn lại, cấp thêm 1 task (hoà
      chọn A trước).</p>
      <table><tr><th>Bước</th><th>Cấp cho</th><th>(xA,xB)</th><th>(sA,sB)</th><th>CPU dùng</th><th>RAM dùng</th></tr>
      <tr><td>1</td><td>A</td><td>(1,0)</td><td>(2/9,0)</td><td>1</td><td>4</td></tr>
      <tr><td>2</td><td>B</td><td>(1,1)</td><td>(2/9,1/3)</td><td>4</td><td>5</td></tr>
      <tr><td>3</td><td>A</td><td>(2,1)</td><td>(4/9,1/3)</td><td>5</td><td>9</td></tr>
      <tr><td>4</td><td>B</td><td>(2,2)</td><td>(4/9,2/3)</td><td>8</td><td>10</td></tr>
      <tr><td>5</td><td>A</td><td>(3,2)</td><td>(2/3,2/3)</td><td>9</td><td>14</td></tr></table>
      <p>Dừng vì hết CPU — trùng nghiệm liên tục ở bước trước. Task nguyên hoặc máy riêng biệt có thể làm thay
      đổi bảo đảm lý thuyết.</p>
      <div class="callout good"><div class="lbl">Liên hệ YARN/Spark</div>YARN Fair Scheduler chia tài nguyên
      giữa ứng dụng/hàng đợi, có thể cấu hình DRF để xét cả CPU lẫn bộ nhớ. YARN Capacity Scheduler quản lý
      phần dung lượng bảo đảm và giới hạn hàng đợi. Spark FAIR chia sẻ tài nguyên giữa job/pool trong 1
      SparkContext. Khi Spark chạy trên YARN: YARN cấp tài nguyên cho ứng dụng Spark, rồi ứng dụng Spark tự
      dùng tài nguyên đó cho các task của mình — hai tầng lập lịch độc lập.</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.37-38.</p>""")]),
 ],
 quiz=[
  dict(q="Dominant share s_i của người dùng i được định nghĩa thế nào?",
   opts=["Tổng tài nguyên người i đang dùng","max_r (x_i·a_ir / R_r) — tỉ lệ lớn nhất trong các loại tài nguyên","Số task người i đang chạy","Trọng số ưu tiên của người i"],
   correct=1, explain="Dominant share lấy tỉ lệ LỚN NHẤT trong các loại tài nguyên — đây là loại tài nguyên 'trội' của người đó."),
  dict(q="Vì sao cần DRF thay vì chia công bằng từng loại tài nguyên riêng lẻ?",
   opts=["DRF tính toán nhanh hơn","Người dùng có thể thiên về CPU hoặc RAM khác nhau — chia công bằng 1 loại có thể làm loại khác quá tải","DRF chỉ áp dụng được cho 1 loại tài nguyên","Không có lý do, chỉ là lựa chọn tuỳ ý"],
   correct=1, explain="Đây là động lực chính nêu ở slide tr.34 — users lệch nhu cầu resource khác nhau."),
  dict(q="Trong ví dụ 9 CPU/18GB RAM, người dùng A (1 CPU, 4GB/task) có tài nguyên trội là gì?",
   opts=["CPU, vì 1/9 > 4/18","RAM, vì 4/18 > 1/9","Cả hai bằng nhau","Không xác định được"],
   correct=1, explain="4/18 ≈ 0,222 > 1/9 ≈ 0,111 nên RAM là tài nguyên trội của A."),
  dict(q="Kết quả cuối cùng (liên tục) của ví dụ DRF 2 người dùng là gì?",
   opts=["(xA,xB)=(2,3), s=1/2","(xA,xB)=(3,2), s=2/3, dùng hết 9 CPU và 14GB RAM","(xA,xB)=(4,1), s=8/9","(xA,xB)=(1,1), s=2/9"],
   correct=1, explain="CPU đầy trước ở s=2/3, cho (xA,xB)=(3,2) — đúng số liệu slide tr.36."),
  dict(q="DRF theo từng task chọn người nào để cấp task tiếp theo?",
   opts=["Người có s_i LỚN nhất","Người có s_i NHỎ nhất trong số còn vừa tài nguyên","Người đến trước","Người có trọng số cao nhất"],
   correct=1, explain="Quy tắc: luôn ưu tiên người có dominant share nhỏ nhất, đúng tinh thần max-min fairness."),
  dict(q="YARN Fair Scheduler và YARN Capacity Scheduler khác nhau ở điểm nào theo nội dung đã học?",
   opts=["Không khác gì nhau","Fair Scheduler chia tài nguyên giữa ứng dụng/hàng đợi (có thể cấu hình DRF); Capacity Scheduler quản lý phần dung lượng bảo đảm và giới hạn hàng đợi","Capacity Scheduler chỉ dùng cho Spark","Fair Scheduler không áp dụng được cho YARN"],
   correct=1, explain="Hai cơ chế khác nhau trong cùng YARN, đúng như liên hệ ở slide tr.38."),
 ]),

# ---------------------------------------------------------------- 22
dict(n=22, slug="ll-08-kafka-roundrobin-range", title="Kafka: Round Robin & Range assignor",
 tag="Phân công partition theo số lượng",
 intro="Kafka consumer group phải gán mỗi partition cho đúng 1 consumer. Round Robin và Range là hai "
       "assignor built-in, cân bằng SỐ LƯỢNG partition nhưng không nhất thiết cân bằng TẢI xử lý.",
 parts=[
  dict(title="Bài toán và Round Robin", bullets=[
    "6 partition, 3 consumer, tải khác nhau aj",
    "Round Robin: cân bằng số lượng, không cân bằng tải",
    "LPT theo tải: phương án cân bằng tải tốt hơn"],
   slides=[
    dict(h="Bài toán phân công partition trong consumer group", body="""
      <p>Partition là một phần dữ liệu của topic. Consumer là tiến trình đọc/xử lý. Xét consumer group
      truyền thống: 6 partition, 3 consumer — mỗi partition giao cho đúng 1 consumer đủ điều kiện.</p>
      <table><tr><th>Partition</th><td>P1</td><td>P2</td><td>P3</td><td>P4</td><td>P5</td><td>P6</td></tr>
      <tr><th>Tải giả định $a_j$</th><td>8</td><td>7</td><td>6</td><td>3</td><td>2</td><td>1</td></tr></table>
      <p>Đặt $P_i$ là tập partition của consumer i, $L_i=\\sum_{j\\in P_i}a_j$. Hai mục tiêu khác nhau: cân bằng
      <b>số lượng</b> ($|P_i|$ gần nhau) và cân bằng <b>tải</b> (làm nhỏ $\\max_i L_i$).</p>
      <p style="color:var(--muted);font-size:.85rem">Phạm vi: consumer group dùng cơ chế gán partition, không
      phải share group mới của Kafka. Nguồn: lap_lich_50_slides.pdf, tr.39.</p>"""),
    dict(h="Round Robin: phân công lần lượt theo vòng", body="""
      <p>Giả sử mọi consumer đăng ký cùng các topic. Lần lượt giao $P_1,\\dots,P_6$ cho $C_1,C_2,C_3$ rồi quay
      lại $C_1$.</p>
      <table><tr><th>Consumer</th><th>Partition nhận</th><th>Số lượng</th><th>Tổng tải</th></tr>
      <tr><td>C1</td><td>P1, P4</td><td>2</td><td>8+3=11</td></tr>
      <tr><td>C2</td><td>P2, P5</td><td>2</td><td>7+2=9</td></tr>
      <tr><td>C3</td><td>P3, P6</td><td>2</td><td>6+1=7</td></tr></table>
      <p>$\\max_i L_i=11$, $\\max_i|P_i|-\\min_i|P_i|=0$ — <b>số partition bằng nhau nhưng tải xử lý vẫn khác
      nhau</b>. Đây là RoundRobinAssignor của Kafka.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.40.</p>""")]),
  dict(title="Range assignor và so sánh với LPT", bullets=[
    "Range: chia đoạn liên tiếp theo từng topic",
    "LPT theo tải: tối ưu cho ví dụ (max Li=9)"],
   slides=[
    dict(h="Range: chia các đoạn liên tiếp theo từng topic", body="""
      <p>Topic có n partition, m consumer cùng đăng ký. Đặt $q=\\lfloor n/m\\rfloor$, $r=n\\bmod m$: r consumer
      đầu nhận $q+1$ partition, còn lại nhận $q$.</p>
      <table><tr><th>Consumer</th><th>Đoạn nhận</th><th>Tổng tải</th></tr>
      <tr><td>C1</td><td>P1, P2</td><td>8+7=15</td></tr>
      <tr><td>C2</td><td>P3, P4</td><td>6+3=9</td></tr>
      <tr><td>C3</td><td>P5, P6</td><td>2+1=3</td></tr></table>
      <p>Range cân bằng số lượng theo <b>từng topic</b> — tải lệch hẳn (15 so với 3) vì tải không tương quan
      với thứ tự partition. Nhiều topic có thể tạo lệch tổng số partition hơn nữa.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.41.</p>"""),
    dict(h="LPT theo tải: phương án để so sánh", body="""
      <p>Giả sử biết tải $a_j$ và mọi consumer cùng năng lực. Sắp partition theo tải giảm dần, giao partition
      tiếp theo cho consumer đang có tải nhỏ nhất — chính là List Scheduling/LPT học ở buổi ll-02, áp dụng cho
      bài toán Kafka.</p>
      <table><tr><th>Consumer</th><th>Partition nhận</th><th>Tổng tải</th></tr>
      <tr><td>C1</td><td>P1, P6</td><td>8+1=9</td></tr>
      <tr><td>C2</td><td>P2, P5</td><td>7+2=9</td></tr>
      <tr><td>C3</td><td>P3, P4</td><td>6+3=9</td></tr></table>
      <p>Tổng tải 27, cận dưới $27/3=9$ — phương án này tối ưu cho ví dụ. Tuy vậy, Kafka built-in không có
      assignor LPT-theo-tải sẵn; cần đo tải và xây cơ chế phân công tuỳ biến (custom `ConsumerPartitionAssignor`)
      để áp dụng ý tưởng này trong thực tế.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.42.</p>""")]),
 ],
 quiz=[
  dict(q="Round Robin cân bằng tiêu chí nào giữa các consumer?",
   opts=["Tải xử lý Li","Số lượng partition |Pi|","Cả hai như nhau","Không cân bằng gì"],
   correct=1, explain="Round Robin chỉ đảm bảo số lượng partition bằng nhau, không đảm bảo tải."),
  dict(q="Trong ví dụ 6 partition tải (8,7,6,3,2,1), Round Robin cho max Li bằng bao nhiêu?",
   opts=["9","10","11","15"], correct=2, explain="C1 nhận P1,P4: 8+3=11 — tải lớn nhất, đúng slide tr.40."),
  dict(q="Range assignor chia partition theo nguyên tắc nào?",
   opts=["Ngẫu nhiên","Theo tải xử lý giảm dần","Chia đoạn liên tiếp theo từng topic (q=⌊n/m⌋ partition liền kề mỗi consumer)","Theo round robin xen kẽ"],
   correct=2, explain="Range chia đoạn LIÊN TIẾP, khác hẳn cách xen kẽ của Round Robin."),
  dict(q="Trong ví dụ, Range assignor cho tải lớn nhất bằng bao nhiêu, và vì sao tệ hơn Round Robin?",
   opts=["9, vì Range cân bằng tải tốt hơn","15, vì partition tải cao (P1,P2) đều rơi vào cùng 1 consumer do chia liên tiếp","11, bằng với Round Robin","3, Range luôn tối ưu nhất"],
   correct=1, explain="C1 nhận P1,P2 liên tiếp: 8+7=15 — tệ hơn cả Round Robin vì partition tải cao đứng cạnh nhau."),
  dict(q="Phương án LPT theo tải trong ví dụ 6 partition cho kết quả gì?",
   opts=["Không cân bằng được","Cả 3 consumer đều có tải đúng bằng 9 — đạt cận dưới 27/3, tối ưu","Giống hệt Round Robin","Giống hệt Range"],
   correct=1, explain="LPT theo tải đạt max Li=9=27/3, tối ưu cho ví dụ này, đúng slide tr.42."),
  dict(q="Kafka có sẵn một assignor built-in chạy đúng LPT theo tải không?",
   opts=["Có, đó là RangeAssignor","Có, đó là RoundRobinAssignor","Không — cần tự đo tải và xây assignor tuỳ biến để áp dụng ý tưởng LPT", "Có, mặc định từ Kafka 3.0"],
   correct=2, explain="Slide tr.42 nêu rõ: LPT là phương án để SO SÁNH, cần cơ chế phân công tuỳ biến mới áp dụng được thực tế."),
 ]),

# ---------------------------------------------------------------- 23
dict(n=23, slug="ll-09-kafka-sticky-rebalance", title="Kafka: tái cân bằng & nguyên tắc Sticky",
 tag="Giảm di chuyển khi consumer rời nhóm",
 intro="Khi một consumer rời nhóm, phân công lại toàn bộ theo Round Robin gây xáo trộn không cần thiết — "
       "mất cache, phải chuyển trạng thái. Nguyên tắc sticky giữ tối đa phân công cũ còn hợp lệ.",
 parts=[
  dict(title="Tái cân bằng và nguyên tắc sticky", bullets=[
    "Phân công lại toàn bộ: 4/6 partition đổi consumer",
    "Sticky: chỉ 2/6 partition đổi — tối thiểu",
    "Cân bằng tải và giảm di chuyển là 2 tiêu chí cạnh tranh"],
   slides=[
    dict(h="Tái cân bằng khi một consumer rời nhóm", body="""
      <p>Bắt đầu từ phân công Round Robin (buổi ll-08): C1={P1,P4}, C2={P2,P5}, C3={P3,P6}. Consumer C2 rời
      nhóm. Nếu phân công lại toàn bộ theo vòng C1, C3:</p>
      <table><tr><th>Partition</th><th>Consumer cũ</th><th>Consumer mới</th><th>Có chuyển?</th></tr>
      <tr><td>P1</td><td>C1</td><td>C1</td><td>Không</td></tr>
      <tr><td>P2</td><td>C2</td><td>C3</td><td>Có</td></tr>
      <tr><td>P3</td><td>C3</td><td>C1</td><td>Có</td></tr>
      <tr><td>P4</td><td>C1</td><td>C3</td><td>Có</td></tr>
      <tr><td>P5</td><td>C2</td><td>C1</td><td>Có</td></tr>
      <tr><td>P6</td><td>C3</td><td>C3</td><td>Không</td></tr></table>
      <p>Có 4 partition đổi consumer, dù chỉ P2, P5 là <b>bắt buộc</b> phải chuyển (vì mất consumer cũ). Phân
      công lại toàn bộ làm mất cache hoặc phải chuyển/khôi phục trạng thái không cần thiết.</p>
      <p style="color:var(--muted);font-size:.85rem">Động cơ giữ phân công cũ khi rebalance: StickyAssignor.
      Nguồn: lap_lich_50_slides.pdf, tr.43.</p>"""),
    dict(h="Nguyên tắc sticky: giữ lại phân công còn hợp lệ", body="""
      <ol style="line-height:2"><li>Giữ C1:{P1,P4} và C3:{P3,P6} nguyên vẹn</li>
      <li>Xét partition mất chủ theo thứ tự P2, P5</li>
      <li>Giao cho consumer có ít partition hơn, hoà thì chọn C1</li></ol>
      <table><tr><th>Consumer</th><th>Sau khi bổ sung</th><th>Số lượng</th><th>Tải</th></tr>
      <tr><td>C1</td><td>P1,P4,P2</td><td>3</td><td>18</td></tr>
      <tr><td>C3</td><td>P3,P6,P5</td><td>3</td><td>9</td></tr></table>
      <p>Chỉ 2 partition chuyển — đây là <b>tối thiểu</b> vì P2, P5 bắt buộc đổi chủ. StickyAssignor của Kafka
      ưu tiên cân bằng số partition rồi giữ phân công cũ.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.44.</p>""")]),
  dict(title="Cân bằng tải và giảm di chuyển: 2 tiêu chí cạnh tranh", bullets=[
    "3 phương án: Round Robin lại / giữ hoà chọn C1 / giữ xét thêm tải",
    "Hàm mục tiêu kết hợp max load + λ·số di chuyển"],
   slides=[
    dict(h="So sánh 3 phương án tái cân bằng", body="""
      <p>Vẫn giữ các partition cũ nhưng đổi cách chọn: giao P5 cho C1, P2 cho C3 — $L_1=8+3+2=13$,
      $L_3=6+1+7=14$.</p>
      <table><tr><th>Phương án</th><th>Tải lớn nhất</th><th>Số partition chuyển D</th></tr>
      <tr><td>Round Robin lại toàn bộ</td><td>16</td><td>4</td></tr>
      <tr><td>Giữ phân công, hoà chọn C1</td><td>18</td><td>2</td></tr>
      <tr><td>Giữ phân công, xét thêm tải</td><td>14</td><td>2</td></tr></table>
      <div class="pd-formula"><div class="pd-formula-label">Hàm mục tiêu mở rộng</div>
      <div class="pd-formula-math">\\min_f \\Big[\\max_i L_i(f) + \\lambda D(f)\\Big],\\quad \\lambda\\ge 0</div></div>
      <p>f là phân công mới, $\\lambda$ là hệ số đổi chi phí chuyển về cùng thang đo với tải. <b>Cân bằng tải và
      giảm di chuyển là hai tiêu chí cạnh tranh</b> — không có phương án nào thắng tuyệt đối cả hai, cần chọn
      $\\lambda$ phù hợp với mức độ ưu tiên thực tế.</p>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.45-46.</p>""")]),
 ],
 quiz=[
  dict(q="Khi C2 rời nhóm, phân công lại TOÀN BỘ theo Round Robin làm bao nhiêu partition đổi consumer?",
   opts=["2","4","6","0"], correct=1, explain="4/6 partition đổi, dù chỉ 2 (P2, P5) là bắt buộc phải đổi — slide tr.43."),
  dict(q="Bao nhiêu partition BẮT BUỘC phải đổi consumer khi C2 rời nhóm (bất kể thuật toán nào)?",
   opts=["0","2 (các partition thuộc C2 cũ)","4","6"], correct=1, explain="P2, P5 từng thuộc C2 — chắc chắn phải đổi chủ vì consumer đó không còn."),
  dict(q="Nguyên tắc sticky ưu tiên điều gì khi tái cân bằng?",
   opts=["Luôn phân công lại từ đầu để đơn giản","Giữ tối đa phân công cũ còn hợp lệ, chỉ xử lý phần mất chủ","Luôn chọn consumer có tải thấp nhất bất kể lịch sử","Bỏ qua cân bằng số lượng"],
   correct=1, explain="Giữ C1:{P1,P4} và C3:{P3,P6}, chỉ xét lại 2 partition mất chủ — đúng cách StickyAssignor hoạt động."),
  dict(q="Trong 3 phương án so sánh ở slide, phương án nào có D (số partition chuyển) nhỏ nhất VÀ tải cân bằng hơn phương án sticky cơ bản?",
   opts=["Round Robin lại toàn bộ","Giữ phân công, hoà chọn C1","Giữ phân công, xét thêm tải (D=2, tải lớn nhất=14)","Không phương án nào tốt hơn"],
   correct=2, explain="D=2 bằng phương án sticky cơ bản nhưng tải lớn nhất giảm từ 18 xuống 14 — đúng số liệu slide tr.45."),
  dict(q="Hàm mục tiêu mở rộng min[max_i Li(f) + λD(f)] dùng để làm gì?",
   opts=["Chỉ tối ưu tải, bỏ qua số lần chuyển","Kết hợp cả tải lớn nhất VÀ số partition phải chuyển, với λ điều chỉnh mức đánh đổi","Chỉ tối ưu số lần chuyển, bỏ qua tải","Tính tổng tải của mọi consumer"],
   correct=1, explain="λ là hệ số đổi chi phí chuyển về cùng thang đo với tải, cho phép cân bằng 2 tiêu chí cạnh tranh."),
 ]),

# ---------------------------------------------------------------- 24
dict(n=24, slug="ll-10-tong-ket-lap-lich", title="Tổng kết: chọn thuật toán & bài tập",
 tag="Bảng tra cứu, 3 bài tập có đáp số",
 intro="Khép lại 10 buổi lập lịch bằng bảng tra cứu chọn thuật toán theo bài toán, 3 bài tập có đáp số "
       "lấy nguyên từ slide gốc, và danh mục đầy đủ tài liệu tham khảo.",
 parts=[
  dict(title="Bảng chọn thuật toán theo bài toán", bullets=[
    "8 dòng tra cứu nhanh: bài toán → thuật toán → điều kiện cần nhớ"],
   slides=[
    dict(h="Bảng tra cứu chọn thuật toán", body="""
      <table><tr><th>Bài toán</th><th>Thuật toán cơ bản</th><th>Điều kiện cần nhớ</th></tr>
      <tr><td>Tác vụ độc lập</td><td>List Scheduling / LPT</td><td>Giảm makespan, máy giống nhau</td></tr>
      <tr><td>Tác vụ có phụ thuộc</td><td>List Scheduling trên DAG</td><td>Chỉ chọn tác vụ đã sẵn sàng</td></tr>
      <tr><td>Một máy, giảm ΣCj</td><td>SPT</td><td>Tất cả có sẵn từ đầu</td></tr>
      <tr><td>Một máy, giảm Σ wⱼCⱼ</td><td>Smith</td><td>Biết pj, wj, có sẵn từ đầu</td></tr>
      <tr><td>Một máy, tác vụ đến động</td><td>SRPT</td><td>Biết độ dài, ngắt không mất phí</td></tr>
      <tr><td>Chia tài nguyên</td><td>Tăng đều / DRF</td><td>Định nghĩa rõ nhu cầu và công bằng</td></tr>
      <tr><td>Gán partition theo số lượng</td><td>Round Robin / Range</td><td>Phụ thuộc subscription</td></tr>
      <tr><td>Giảm di chuyển partition</td><td>Nguyên tắc sticky</td><td>Ưu tiên giữ phân công hợp lệ</td></tr></table>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.46-47.</p>""")]),
  dict(title="3 bài tập có đáp số (nguyên văn slide gốc)", bullets=[
    "LPT 2 máy: tìm lịch tốt hơn", "Progressive filling 3 người dùng", "Tái cân bằng: ít nhất bao nhiêu partition đổi"],
   slides=[
    dict(h="Bài 1 & Bài 2", body="""
      <div class="callout info"><div class="lbl">Bài 1</div>Hai máy, các tác vụ có thời gian 5, 4, 3, 2, 2.
      Chạy LPT, hoà chọn máy 1. Tính makespan và tìm một lịch tốt hơn.<br>
      <b>Đáp số:</b> LPT cho tải (9, 7). Lịch (5+3, 4+2+2) có tải (8, 8) và tối ưu.</div>
      <div class="callout info"><div class="lbl">Bài 2</div>Có 15 đơn vị tài nguyên, nhu cầu ba người là
      (3, 4, 20). Dùng progressive filling để tìm phần cấp công bằng.<br>
      <b>Đáp số:</b> Tăng đến (3,3,3), rồi (3,4,4), cuối cùng (3,4,8).</div>
      <p style="color:var(--muted);font-size:.85rem">Nguồn: lap_lich_50_slides.pdf, tr.47 (đáp số giữ nguyên văn slide gốc).</p>"""),
    dict(h="Bài 3 & Tài liệu tham khảo", body="""
      <div class="callout info"><div class="lbl">Bài 3</div>Consumer rời nhóm đang giữ 4 partition. Ít nhất bao
      nhiêu partition phải đổi consumer nếu vẫn giữ nguyên các partition còn lại?<br>
      <b>Đáp số:</b> Ít nhất 4. Có đạt được đồng thời với cân bằng hay không còn tuỳ subscription và ràng buộc.</div>
      <table><tr><th>Tài liệu thuật toán</th></tr>
      <tr><td>[1] R. L. Graham (1969). Bounds on Multiprocessing Timing Anomalies. SIAM J. Applied Math.</td></tr>
      <tr><td>[2] W. E. Smith (1956). Various Optimizers for Single-Stage Production. Naval Research Logistics Quarterly.</td></tr>
      <tr><td>[3] L. Schrage (1968). A Proof of the Optimality of SRPT Discipline. Operations Research.</td></tr>
      <tr><td>[4] A. Ghodsi và cộng sự (2011). Dominant Resource Fairness. NSDI 2011.</td></tr></table>
      <table><tr><th>Tài liệu chính thức hệ thống</th></tr>
      <tr><td>[5] Apache Spark: Job Scheduling (3.5.6), Cluster Mode Overview, TaskScheduler/DAGScheduler.</td></tr>
      <tr><td>[6] Apache Hadoop YARN (3.4.0): Fair Scheduler, Capacity Scheduler.</td></tr>
      <tr><td>[7] Apache Hadoop MapReduce (3.4.0): MapReduce Tutorial.</td></tr>
      <tr><td>[8] Apache Kafka Consumer API (3.7.2): RoundRobinAssignor, RangeAssignor, StickyAssignor.</td></tr></table>
      <p style="color:var(--muted);font-size:.85rem">Phạm vi đối chiếu: đúng các phiên bản nêu trên — cấu hình/giao thức
      phiên bản khác có thể thay đổi. Nguồn: lap_lich_50_slides.pdf, tr.47-50.</p>""")]),
 ],
 quiz=[
  dict(q="Hai máy, tác vụ (5,4,3,2,2), LPT (hoà chọn máy 1) cho makespan bao nhiêu?",
   opts=["7","8","9","10"], correct=2, explain="LPT cho tải (9,7) → makespan 9, đúng đáp số Bài 1 slide tr.47."),
  dict(q="Lịch tốt hơn cho bài toán trên (5,4,3,2,2; 2 máy) đạt makespan bao nhiêu?",
   opts=["7","8","9","10"], correct=1, explain="Lịch (5+3, 4+2+2) có tải (8,8) — tốt hơn LPT (9,7), đúng đáp số Bài 1."),
  dict(q="15 đơn vị tài nguyên, nhu cầu 3 người (3,4,20), progressive filling cho kết quả cuối cùng là gì?",
   opts=["(3,4,8)","(5,5,5)","(3,3,9)","(0,0,15)"], correct=0, explain="Tăng đến (3,3,3)→(3,4,4)→cuối cùng (3,4,8), đúng đáp số Bài 2."),
  dict(q="Consumer rời nhóm đang giữ 4 partition, ít nhất bao nhiêu partition phải đổi consumer?",
   opts=["1","2","4","6"], correct=2, explain="Ít nhất 4 — đúng số partition mà consumer đó đang giữ, đáp số Bài 3."),
  dict(q="Bài báo gốc chứng minh bảo đảm xấp xỉ của List Scheduling/LPT là của ai?",
   opts=["W. E. Smith (1956)","R. L. Graham (1969)","L. Schrage (1968)","A. Ghodsi và cộng sự (2011)"],
   correct=1, explain="[1] Graham (1969), Bounds on Multiprocessing Timing Anomalies."),
  dict(q="DRF (Dominant Resource Fairness) được công bố ở đâu, bởi ai?",
   opts=["Graham, SIAM 1969","Smith, Naval Research Logistics 1956","Ghodsi và cộng sự, NSDI 2011","Schrage, Operations Research 1968"],
   correct=2, explain="[4] A. Ghodsi và cộng sự (2011), Dominant Resource Fairness, NSDI 2011."),
  dict(q="Theo bảng chọn thuật toán, bài toán \"một máy, giảm Σ wⱼCⱼ\" dùng thuật toán nào?",
   opts=["SPT","Smith","SRPT","DRF"], correct=1, explain="Smith xử lý đúng trường hợp có trọng số wⱼ; SPT chỉ là trường hợp đặc biệt khi mọi wⱼ bằng nhau."),
 ]),
]
