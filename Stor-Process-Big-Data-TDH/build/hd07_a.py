# -*- coding: utf-8 -*-
"""Module hd-07 (phần 1/2): Ba bài báo của thầy Tạ Duy Hoàng về chọn ngưỡng chia cây quyết định.
Nguồn: arXiv:2403.19867v1 (03/2024), arXiv:2403.19867v4 (04/2025, ISIT 2025), arXiv:2604.20394v2 (07/2026, ESA 2026),
đọc trực tiếp từ file PDF trong thư mục References. Mọi định lý, bảng kết quả, tên thuật toán đều theo bài báo;
ví dụ tính tay tự dựng được gắn nhãn (minh hoạ)/(giả định). Chỗ nào là suy luận của nhóm đều ghi rõ."""
from hd_add_common import fig, logo, logos, two

PARTS_A = []

# --------------------------------------------------------------------------------------------- PHẦN 1
PARTS_A.append(dict(
 title="Bối cảnh: cây quyết định, và vì sao chọn ngưỡng chia quy về một phép đếm theo khoảng",
 bullets=[
  "Cây quyết định xây từ trên xuống (CART, ID3): mỗi nút phải chọn một ngưỡng chia",
  "Hình thức hoá: luồng $(x_i, y_i)$, ngưỡng $j$, sai số MSE, tỉ lệ phân loại sai, Gini",
  "Ví dụ tính tay: 8 điểm, thử mọi ngưỡng, ngưỡng tốt nhất là $j=4$"],
 slides=[
  dict(h="Cây quyết định xây từ trên xuống, và vì sao chọn ngưỡng chia là việc lặp lại nhiều nhất", body="""
   <p>🗣️ <b>Nói nôm na:</b> trò chơi &quot;20 câu hỏi&quot;: mỗi câu hỏi chia tập đáp án làm hai. Câu hỏi hay là câu chia thật &quot;sạch&quot;: một bên gần như toàn đáp án giống nhau.
   Với dữ liệu số, một câu hỏi có dạng &quot;tuổi nhỏ hơn hay bằng 30?&quot;, con số 30 chính là <b>ngưỡng chia</b>.</p>
   <p>Các thuật toán cổ điển <b>CART</b> và <b>ID3</b> dựng cây từ trên xuống: ở mỗi nút, thử các ngưỡng và chọn ngưỡng làm tiêu chí
   (Gini impurity, tỉ lệ phân loại sai hoặc entropy cho phân loại; sai số bình phương trung bình cho hồi quy) tốt nhất, rồi lặp lại ở hai nhánh con.
   Cây quyết định là nền của hầu hết các mô hình tập hợp mạnh trên dữ liệu dạng bảng: random forest, AdaBoost, gradient boosting, XGBoost, LightGBM, CatBoost.</p>
   <table><tr><th>Ngành</th><th>Ngưỡng chia điển hình (minh hoạ)</th><th>Điều cần tối ưu</th></tr>
   <tr><td>Ngân hàng</td><td>&quot;Thu nhập tháng ≤ 15 triệu?&quot;</td><td>Hai nhóm con có tỉ lệ nợ xấu khác nhau nhất</td></tr>
   <tr><td>Y tế</td><td>&quot;Huyết áp tâm thu ≤ 140?&quot;</td><td>Hai nhóm con có mức nguy cơ khác nhau nhất</td></tr>
   <tr><td>Nông nghiệp</td><td>&quot;Lượng mưa tháng ≤ 120 mm?&quot;</td><td>Hai nhóm con có năng suất trung bình khác nhau nhất</td></tr></table>
   <div class="callout info"><div class="lbl">Vì sao dùng thuật toán tham lam</div>Các bài báo nhắc rằng tìm cây quyết định <b>tối ưu</b> là bài toán NP-hard, nên người ta dùng heuristic tham lam từng nút.
   Vì mỗi nút của mỗi cây trong mỗi mô hình tập hợp đều phải chọn ngưỡng, <b>chọn ngưỡng chia là phép toán lõi bị lặp lại hàng tỉ lần</b>. Đó là lý do đáng làm nó rẻ về bộ nhớ.</div>"""),
  dict(h="Hình thức hoá: luồng quan sát, ngưỡng $j$ và ba loại sai số", body=two(
   fig("ta_fig1_split.png", "Figure 1 (arXiv:2403.19867v4): trái là hồi quy, phải là phân loại; cả hai có ngưỡng tối ưu $j=4$.", 205), """
   <ul style="margin:0;padding-left:20px;line-height:1.5">
   <li>Luồng $(x_1,y_1),\\dots,(x_m,y_m)$ với $x_i\\in[N]=\\{1,\\dots,N\\}$ (số thực được rời rạc hoá vì máy tính có độ chính xác hữu hạn).</li>
   <li>Nhãn: $y_i\\in[0,M]$ (hồi quy) hoặc $y_i\\in\\{-1,+1\\}$ (phân loại).</li>
   <li>Ngưỡng $j$ chia thành hai đoạn $[1,j]$ và $[j+1,N]$.</li></ul>""", "48%") + """
   <div class="pd-formula"><div class="pd-formula-label">Hồi quy: sai số bình phương trung bình</div>
   <div class="pd-formula-math">L_{\\mathrm{MSE}}(j)=\\frac1m\\Big(\\sum_{x_i\\le j}(y_i-\\mu(j))^2+\\sum_{x_i>j}(y_i-\\gamma(j))^2\\Big),\\quad \\mu(j)=\\overline{y}_{[1,j]},\\ \\gamma(j)=\\overline{y}_{[j+1,N]}</div></div>
   <div class="pd-formula"><div class="pd-formula-label">Phân loại: tỉ lệ phân loại sai ($f_{\\pm1,R}$ là số điểm nhãn $\\pm1$ trong đoạn $R$)</div>
   <div class="pd-formula-math">L_{\\mathrm{mis}}(j)=\\frac1m\\Big(\\min\\{f_{-1,[1,j]},f_{+1,[1,j]}\\}+\\min\\{f_{-1,[j+1,N]},f_{+1,[j+1,N]}\\}\\Big)</div></div>
   <p><b>Mục tiêu:</b> tìm $\\hat j$ với $L(\\hat j)\\le \\mathrm{OPT}+\\varepsilon$ (sai số cộng $\\varepsilon$) hoặc $L(\\hat j)\\le(1+\\varepsilon)\\mathrm{OPT}$ (sai số nhân), trong đó $\\mathrm{OPT}=\\min_j L(j)$.
   Trên hình: ở hồi quy, hai đường chấm là trung bình hai phía; ở phân loại, mỗi phía dự đoán theo nhãn đa số.</p>
   <div class="callout good"><div class="lbl">Điều cần nhìn ra</div>Để tính $L(j)$ ta chỉ cần, với mỗi phía của ngưỡng, ba con số: <b>số điểm, tổng nhãn, tổng bình phương nhãn</b> (hồi quy), hoặc số điểm theo từng nhãn (phân loại).
   Tức là toàn bộ bài toán quy về <b>đếm theo khoảng</b>, đúng như cách các bài báo gọi các đại lượng $f_R$.</div>"""),
  dict(h="Ví dụ tính tay: 8 điểm, thử mọi ngưỡng, ngưỡng tốt nhất là $j=4$", body="""
   <p><b>Dữ liệu (giả định, tự dựng cho khớp ý Figure 1):</b> $m=8$ điểm, $x=1,\\dots,8$ và $y=(6,8,7,7,2,3,2,1)$.
   Dùng $\\mathrm{SSE}(R)=q_R-s_R^2/n_R$ với $n_R$ = số điểm, $s_R$ = tổng $y$, $q_R$ = tổng $y^2$ của đoạn $R$ (suy ra từ $\\sum(y-\\bar y)^2=q-s^2/n$).</p>
   <table><tr><th>$j$</th><th>Trái $(n,s,q)$</th><th>SSE trái</th><th>Phải $(n,s,q)$</th><th>SSE phải</th><th>Tổng</th><th>$L(j)=\\text{Tổng}/8$</th></tr>
   <tr><td>1</td><td>(1, 6, 36)</td><td>0</td><td>(7, 30, 180)</td><td>$180-900/7\\approx51{,}43$</td><td>51,43</td><td>6,43</td></tr>
   <tr><td>2</td><td>(2, 14, 100)</td><td>2</td><td>(6, 22, 116)</td><td>$116-484/6\\approx35{,}33$</td><td>37,33</td><td>4,67</td></tr>
   <tr><td>3</td><td>(3, 21, 149)</td><td>2</td><td>(5, 15, 67)</td><td>22</td><td>24</td><td>3,00</td></tr>
   <tr><td><b>4</b></td><td>(4, 28, 198)</td><td>2</td><td>(4, 8, 18)</td><td>2</td><td><b>4</b></td><td><b>0,50</b></td></tr>
   <tr><td>5</td><td>(5, 30, 202)</td><td>22</td><td>(3, 6, 14)</td><td>2</td><td>24</td><td>3,00</td></tr>
   <tr><td>6</td><td>(6, 33, 211)</td><td>29,5</td><td>(2, 3, 5)</td><td>0,5</td><td>30</td><td>3,75</td></tr>
   <tr><td>7</td><td>(7, 35, 215)</td><td>40</td><td>(1, 1, 1)</td><td>0</td><td>40</td><td>5,00</td></tr></table>
   <p>Không chia ($j=0$ hoặc $j=8$): $216-36^2/8=54$, $L=6{,}75$. Ngưỡng tối ưu là <b>$j=4$</b> với $\\mathrm{OPT}=0{,}5$, đúng như ví dụ trên Figure 1.
   Mẹo tính nhanh: dùng <b>tổng tiền tố</b> của $n$, $s$, $q$, rồi phía phải bằng tổng toàn bộ trừ phía trái. Có thể tự thử lại trong mô phỏng cuối trang.</p>"""),
 ]))

# --------------------------------------------------------------------------------------------- PHẦN 2
PARTS_A.append(dict(
 title="Hai mô hình tính toán: streaming (đếm lượt duyệt và bộ nhớ) và MPC (đếm số vòng)",
 bullets=[
  "Streaming: bộ nhớ dưới tuyến tính, 1 hoặc vài lượt duyệt, cập nhật $O(1)$",
  "MPC: $m$ quan sát chia cho $m^{1-\\beta}$ máy, mỗi máy $\\tilde O(m^{\\beta})$ bộ nhớ, đo bằng số vòng",
  "Hai mô hình khác nhau ở thứ khan hiếm, nhưng cùng trả giá cho một phép đếm theo khoảng"],
 slides=[
  dict(h="Mô hình streaming: lượt duyệt, bộ nhớ, thời gian cập nhật", body="""
   <p>🗣️ <b>Nói nôm na:</b> băng chuyền hàng chạy qua trước mặt bạn một lần; bạn chỉ có một cái túi nhỏ để ghi chú, không thể chất cả hàng xuống đất rồi đếm.
   Muốn xem lại thì phải chạy băng chuyền lần nữa, đó là một <i>lượt duyệt</i> (pass) thêm.</p>
   <table><tr><th>Đại lượng</th><th>Ý nghĩa trong bài báo</th></tr>
   <tr><td>Bộ nhớ (space)</td><td>Dưới tuyến tính: $o(m)$ và $o(N)$. Ký hiệu $\\tilde O(\\cdot)$ giấu các hệ số polylog</td></tr>
   <tr><td>Số lượt duyệt (passes)</td><td>Lý tưởng là 1; cho phép vài lượt; có thuật toán đổi bộ nhớ lấy số lượt qua tham số $\\beta$</td></tr>
   <tr><td>Thời gian cập nhật (update time)</td><td>Chi phí xử lý mỗi phần tử đến, thường $O(1)$</td></tr>
   <tr><td>Thời gian hậu xử lý (post-processing)</td><td>Chi phí tính đáp án sau khi luồng kết thúc</td></tr>
   <tr><td>Luồng chỉ thêm (insertion-only) và luồng động</td><td>Luồng động có cả xoá; dùng Count-Min sketch với phân rã dyadic, thêm hệ số $\\log N$ vào bộ nhớ và thời gian</td></tr>
   <tr><td>$D$</td><td>Số giá trị phân biệt của $x_i$; có thể lớn tới $N$</td></tr></table>
   <div class="callout info"><div class="lbl">Vì sao bài toán này đáng phải làm</div>Bài báo nêu 3 lý do: (1) dữ liệu thường quá lớn để nạp vào bộ nhớ chính một máy và được đọc dạng luồng từ đĩa hoặc mạng;
   (2) đặc trưng có số giá trị $N$ rất lớn (đặc trưng thứ bậc cao, đặc trưng ghép) làm bộ nhớ và thời gian phình ra; (3) trong mô hình tập hợp thường phải huấn luyện <b>rất nhiều đặc trưng và rất nhiều cây song song</b>, nên dùng $o(N)$ bộ nhớ cho mỗi đặc trưng mỗi cây giảm mạnh dấu chân bộ nhớ tổng.</div>"""),
  dict(h="Mô hình MPC: $m$ quan sát, $m^{1-\\beta}$ máy, mỗi máy $\\tilde O(m^{\\beta})$ bộ nhớ", body="""
   <p>MPC (Massively Parallel Computation) là mô hình lý thuyết mà các bài báo gọi là <b>phép trừu tượng hoá của MapReduce, Hadoop và Spark</b>. Có $m$ quan sát chia cho $m^{1-\\beta}$ máy, mỗi máy có bộ nhớ
   $\\tilde O(m^{\\beta})$ với $0<\\beta<1$. Trong mỗi <b>vòng</b> đồng bộ, mọi máy có thể gửi và nhận thông điệp từ mọi máy khác rồi tính cục bộ. <b>Độ phức tạp của thuật toán là số vòng.</b></p>
   <div class="pd-formula"><div class="pd-formula-label">Tổng bộ nhớ của cụm</div><div class="pd-formula-math">m^{1-\\beta}\\times m^{\\beta}=m</div></div>
   <p>Tổng bộ nhớ chỉ vừa đủ chứa dữ liệu một lần: cụm không thể &quot;ôm&quot; cả dữ liệu vào một máy, và cũng không thể dư sức nhân bản. <b>Ví dụ (minh hoạ, bỏ hằng số và polylog):</b> $m=10^6$ quan sát.</p>
   <table><tr><th>$\\beta$</th><th>Số máy $m^{1-\\beta}$</th><th>Bộ nhớ mỗi máy $m^{\\beta}$</th><th>Số vòng cỡ $1/\\beta$</th></tr>
   <tr><td>$1/3$</td><td>10.000</td><td>100</td><td>3</td></tr>
   <tr><td>$1/2$</td><td>1.000</td><td>1.000</td><td>2</td></tr>
   <tr><td>$2/3$</td><td>100</td><td>10.000</td><td>1,5 (tức vài vòng)</td></tr></table>
   <p>Cụm càng nhiều máy nhỏ ($\\beta$ nhỏ) thì mỗi máy càng ít bộ nhớ và số vòng tăng theo $1/\\beta$. Đây là đánh đổi mà các bài báo gọi tên bằng cùng một tham số $\\beta$ cho cả streaming và MPC.</p>
   <div class="callout good"><div class="lbl">Đối chiếu với Chương 2</div>Máy ↔ container/DataNode; bộ nhớ mỗi máy ↔ bộ nhớ một task; một vòng ↔ một job MapReduce có shuffle (module hd-02). Theo bài MapReduce, mỗi vòng thêm nghĩa là map ghi file trung gian xuống đĩa cục bộ rồi reduce đọc từ xa: đó là lý do <b>đếm số vòng</b>.</div>"""),
  dict(h="Hai mô hình đặt cạnh nhau: cùng một bài toán, hai thứ khan hiếm", body="""
   <table><tr><th></th><th>Streaming</th><th>MPC (MapReduce, Hadoop, Spark)</th></tr>
   <tr><td><b>Dữ liệu</b></td><td>Một luồng đi qua một máy</td><td>$m$ quan sát chia cho $m^{1-\\beta}$ máy</td></tr>
   <tr><td><b>Thứ khan hiếm</b></td><td>Bộ nhớ của một máy</td><td>Bộ nhớ của mỗi máy</td></tr>
   <tr><td><b>Chi phí được đếm</b></td><td>Số lượt duyệt dữ liệu</td><td>Số vòng giao tiếp</td></tr>
   <tr><td><b>Kết quả điển hình (hồi quy)</b></td><td>1 lượt, bộ nhớ $\\tilde O(M^2/\\varepsilon)$ (bài 3)</td><td>$O(1)$ vòng, mỗi máy $\\tilde O(\\sqrt m)$, sai số $\\mathrm{OPT}+1/\\sqrt m$ (bài 2)</td></tr>
   <tr><td><b>Đánh đổi theo $\\beta$</b></td><td>$O(1/\\beta)$ lượt, bộ nhớ $\\tilde O(N^{\\beta}/\\varepsilon^2)$</td><td>$O(1/\\beta)$ vòng, mỗi máy $\\tilde O(m^{\\beta}/\\varepsilon^2)$</td></tr>
   <tr><td><b>Công cụ chính</b></td><td>Lấy mẫu, Count-Min sketch với phân rã dyadic</td><td>Lấy mẫu cục bộ, một máy trung tâm, gửi đi các ứng viên</td></tr></table>
   <div class="callout warn"><div class="lbl">Cách đọc đúng</div>Hai dòng $O(1/\\beta)$ cho thấy cùng một thuật toán &quot;đoán sai số + tìm nhị phân&quot; được chạy ở hai mô hình: tham số $\\beta$ quyết định mỗi lần mô phỏng được bao nhiêu bước tìm nhị phân cùng lúc.
   Chi tiết nằm ở các phần 4 và 6 của module này.</div>"""),
 ]))

# --------------------------------------------------------------------------------------------- PHẦN 3
PARTS_A.append(dict(
 title="Công trình nền tảng (Domingos-Hulten) và khoảng trống mà các bài báo của thầy lấp",
 bullets=[
  "VFDT (KDD 2000): luồng vô hạn, i.i.d., chỉ phân loại; được trích dẫn hơn 3000 lần",
  "Các hướng liên quan: rừng ngẫu nhiên thích nghi, concept drift, scikit-multiflow, River",
  "Các bài của thầy: không giả định vô hạn, không giả định i.i.d., có hồi quy, có chứng minh"],
 slides=[
  dict(h="Công trình nền tảng: Domingos-Hulten (KDD 2000) và những người đi tiếp", body="""
   <p>Các bài báo gọi công trình của <b>Domingos và Hulten (KDD 2000)</b> là công trình &quot;nền tảng&quot; (seminal) về học cây quyết định trên luồng dữ liệu; theo chú thích trong bài, được trích dẫn hơn 3000 lần
   (theo Google Scholar tại thời điểm viết bài). Bài báo <b>Hulten, Spencer, Domingos (KDD 2001)</b> mở rộng sang luồng thay đổi theo thời gian.</p>
   <table><tr><th>Công trình</th><th>Điều bài báo thầy nêu</th></tr>
   <tr><td>Domingos-Hulten 2000</td><td>Xét luồng <b>vô hạn</b> các quan sát được rút <b>độc lập từ một phân phối chưa biết</b> (i.i.d.); chỉ bài toán <b>phân loại</b>, không xét hồi quy; định lượng số mẫu cần để tìm ngưỡng tốt nhất và chặn xác suất một mẫu đi lệch nhánh so với cây dựng từ toàn bộ dữ liệu; giả định một mẫu tới lá ở mỗi tầng với xác suất hằng số</td></tr>
   <tr><td>Ben-Haim và Tom-Tov</td><td>Heuristic cây quyết định cho dữ liệu luồng song song, dùng <b>histogram trực tuyến</b>; chạy tốt trong thực tế</td></tr>
   <tr><td>Gomes và cộng sự</td><td>Rừng ngẫu nhiên thích nghi cho phân loại trên luồng thay đổi theo thời gian</td></tr>
   <tr><td>Hệ thống mã nguồn mở</td><td>Các gói C++ và Python như <b>scikit-multiflow</b> và <b>River</b> được dùng thương mại rộng rãi; hướng phổ biến khác là phát hiện concept drift</td></tr>
   <tr><td>Tatti; Silva và cộng sự; Assis và cộng sự</td><td>Tìm ngưỡng chia trên luồng thưa; tính ngưỡng chia trong môi trường học liên kết (federated); độ bền cấu trúc trong luồng tiến hoá</td></tr></table>
   <p style="font-size:.92rem;color:var(--muted)">Các công trình trên chủ yếu là <i>heuristic và hệ thống</i>. Điểm chung: ít có đảm bảo chứng minh được về <b>bộ nhớ và số lượt duyệt</b> cho bài toán chọn ngưỡng chia.</p>"""),
  dict(h="Khoảng trống và đóng góp: so sánh trực diện", body="""
   <table><tr><th>Tiêu chí</th><th>Domingos-Hulten (2000)</th><th>Các bài của thầy (2024 đến 2026)</th></tr>
   <tr><td>Độ dài luồng</td><td>Vô hạn</td><td>Hữu hạn, không cần giả định vô hạn</td></tr>
   <tr><td>Giả định phân phối</td><td>i.i.d. (độc lập, cùng phân phối)</td><td><b>Không</b> giả định i.i.d.</td></tr>
   <tr><td>Bài toán</td><td>Chỉ phân loại</td><td>Hồi quy, phân loại (misclassification, Gini), thuộc tính phân loại</td></tr>
   <tr><td>Kiểu đảm bảo</td><td>Chặn xác suất theo số mẫu, dưới giả định i.i.d.</td><td>Đảm bảo <b>cộng $\\varepsilon$ hoặc nhân $(1+\\varepsilon)$ so với tối ưu</b>, kèm cận bộ nhớ và số lượt/vòng; bài 3 có cận dưới khớp</td></tr>
   <tr><td>Mô hình song song</td><td>Không xét</td><td>Có phần MPC (MapReduce, Hadoop, Spark)</td></tr></table>
   <div class="callout good"><div class="lbl">Vì sao &quot;không i.i.d.&quot; quan trọng (ví dụ trong bài 1)</div>Dữ liệu thu vào <b>buổi sáng</b> có thể phân phối khác dữ liệu thu vào <b>buổi tối</b>. Nếu luồng được thu theo thời gian và phân phối đổi dần,
   giả định i.i.d. sai ngay từ đầu, còn thuật toán của thầy vẫn đúng vì nó chỉ dùng số đếm theo khoảng của <i>chính luồng đã thấy</i>.</div>
   <div class="callout info"><div class="lbl">Khiêm tốn có chủ đích</div>Chính các bài báo viết rằng kết quả của họ &quot;không so sánh trực tiếp được&quot; (not directly comparable) với Domingos-Hulten mà <b>bổ sung</b> (complement): hai bên trả lời hai câu hỏi hơi khác nhau.</div>"""),
 ]))

# --------------------------------------------------------------------------------------------- PHẦN 4
PARTS_A.append(dict(
 title="Bài báo 1 (arXiv 03/2024): bộ ba thuật toán cho hồi quy và bước đầu sang MPC",
 bullets=[
  "Thuật toán 1 lượt chính xác: lưu ba bảng đếm $A_t$, $B_t$, $C_t$, bộ nhớ $\\tilde O(D)$",
  "Thuật toán 2 lượt xấp xỉ cộng $\\varepsilon$: lấy mẫu chọn ứng viên, rồi đếm chính xác trên ứng viên",
  "Thuật toán nhiều lượt xấp xỉ $(1+\\varepsilon)$: đoán sai số, tìm nhị phân; đổi lượt lấy bộ nhớ qua $\\beta$"],
 slides=[
  dict(h="Bài báo 1: ba kết quả chính cho hồi quy và hai cho phân loại", body=fig("ta1_title.png", "Trang đầu bài báo 1, arXiv:2403.19867v1 [cs.DS], 28/03/2024.", 90) + """
   <p><b>Finding Decision Tree Splits in Streaming and Massively Parallel Models</b> (Huy Phạm, Tạ Duy Hoàng, Hoa T. Vu), arXiv:2403.19867v1, 28/03/2024. Tóm tắt: thuật toán streaming tìm ngưỡng chia tối ưu với bộ nhớ dưới tuyến tính và ít lượt, mở rộng được sang MPC, bổ sung cho Domingos-Hulten.</p>
   <table><tr><th>Bài toán</th><th>Bộ nhớ</th><th>Số lượt</th><th>Đảm bảo</th></tr>
   <tr><td>Hồi quy</td><td>$\\tilde O(D)$</td><td>1</td><td>Tối ưu, $L(j)=\\mathrm{OPT}$ (tất định)</td></tr>
   <tr><td>Hồi quy, $M=O(1)$</td><td>$\\tilde O(1/\\varepsilon)$</td><td>2</td><td>$L(j)\\le \\mathrm{OPT}+\\varepsilon$</td></tr>
   <tr><td>Hồi quy</td><td>$\\tilde O(1/\\varepsilon^2)$</td><td>$O(\\log N)$</td><td>$L(j)\\le(1+\\varepsilon)\\mathrm{OPT}$</td></tr>
   <tr><td>Phân loại (số)</td><td>$\\tilde O(1/\\varepsilon)$</td><td>1</td><td>$L(j)\\le \\mathrm{OPT}+\\varepsilon$</td></tr>
   <tr><td>Phân loại (số)</td><td>$\\tilde O(1/\\varepsilon^2)$</td><td>$O(\\log N)$</td><td>$L(j)\\le(1+\\varepsilon)\\mathrm{OPT}$</td></tr>
   <tr><td>Phân loại (thuộc tính phân loại)</td><td>$\\tilde O(N/\\varepsilon)$</td><td>1</td><td>$L(A,B)\\le \\mathrm{OPT}+\\varepsilon$; cận dưới $\\Omega(N)$ cho mọi thuật toán hằng số lượt</td></tr></table>
   <div class="callout info"><div class="lbl">Ghi chú về phạm vi</div>Nhóm tìm cây quyết định chỉ <b>một điểm chia</b> (cây sâu 1, còn gọi là <i>decision stump</i>, cũng là weak learner của AdaBoost); để dựng cây sâu hơn thì áp dụng lặp lại thuật toán,
   thêm lượt duyệt. Với nhiều thuộc tính, chạy riêng từng thuộc tính rồi chọn tốt nhất: bộ nhớ nhân thêm hệ số $d$.</div>"""),
  dict(h="Thuật toán 1 lượt chính xác: ba bảng đếm $A_t$, $B_t$, $C_t$", body="""
   <p>🗣️ <b>Nói nôm na:</b> với mỗi giá trị $x$ đã thấy, giữ ba ô ghi chú: <b>đã gặp mấy lần</b> ($A$), <b>tổng các nhãn</b> ($B$), <b>tổng bình phương các nhãn</b> ($C$). Hết luồng thì gộp các ô lại là tính được sai số của mọi ngưỡng.</p>
   <table><tr><th>Bước</th><th>Việc làm</th></tr>
   <tr><td>Khi $(x_i,y_i)$ đến</td><td>$A_{x_i}\\mathrel{+}=1$; $B_{x_i}\\mathrel{+}=y_i$; $C_{x_i}\\mathrel{+}=y_i^2$ (bảng băm, $O(1)$ mỗi lần)</td></tr>
   <tr><td>Hết luồng, cho mỗi giá trị $j$</td><td>Tính tổng tiền tố $\\sum_{t\\le j}A_t,B_t,C_t$ và tổng hậu tố; suy ra $\\mu(j)$ và $\\gamma(j)$</td></tr>
   <tr><td>Công thức</td><td>$mL(j)=\\sum_{t\\le j}(C_t+\\mu^2A_t-2\\mu B_t)+\\sum_{t>j}(C_t+\\gamma^2A_t-2\\gamma B_t)$</td></tr>
   <tr><td>Trả về</td><td>$\\arg\\min_j L(j)$</td></tr></table>
   <p><b>Vì sao đúng:</b> khai triển $(y_i-\\mu)^2=y_i^2+\\mu^2-2y_i\\mu$ rồi gom theo giá trị $x$: mọi thứ chỉ còn phụ thuộc $A_t$, $B_t$, $C_t$. Bộ nhớ $\\tilde O(D)$ vì chỉ cần 3 ô cho mỗi giá trị phân biệt; thời gian hậu xử lý $O(D)$ nhờ tổng tiền tố.</p>
   <p><b>Kiểm tra bằng ví dụ 8 điểm</b> (mỗi $x$ xuất hiện một lần nên $A_t=1$, $B_t=y_t$, $C_t=y_t^2$): với $j=4$, trái có $\\sum A=4$, $\\sum B=28$, $\\sum C=198$, nên $\\mu=7$ và phần trái $=198+7^2\\cdot 4-2\\cdot 7\\cdot 28=198+196-392=2$; phải có $\\sum A=4$, $\\sum B=8$, $\\sum C=18$, nên $\\gamma=2$ và phần phải $=18+16-32=2$; tổng $4$, $L=4/8=0{,}5$, khớp bảng tính tay.</p>
   <div class="callout warn"><div class="lbl">Điểm yếu</div>Bộ nhớ tỉ lệ với $D$, có thể bằng $N$. Khi $N$ rất lớn (đặc trưng thứ bậc cao) ta cần xấp xỉ: đó là việc của hai thuật toán sau.</div>"""),
  dict(h="Thuật toán 2 lượt xấp xỉ cộng $\\varepsilon$: lấy mẫu chọn ứng viên, rồi đếm chính xác", body="""
   <p><b>Ý tưởng:</b> không cần thử mọi ngưỡng. Nếu chọn được khoảng $1/\\varepsilon$ ứng viên sao cho giữa hai ứng viên liên tiếp có <b>không quá $\\varepsilon m$ quan sát</b>, thì ngưỡng tốt nhất trong số ứng viên chỉ kém tối ưu thêm $O(\\varepsilon)$.</p>
   <table><tr><th>Lượt</th><th>Việc làm</th></tr>
   <tr><td><b>Lượt 1</b></td><td>Lấy mẫu mỗi $x_i$ độc lập với xác suất $p=C\\log N/(m\\varepsilon)$. Tập ứng viên $S$ gồm các giá trị được lấy mẫu, giá trị kề bên, cùng $0$ và $N$</td></tr>
   <tr><td><b>Lượt 2</b></td><td>Với mỗi đoạn giữa hai ứng viên liên tiếp, đếm chính xác $A_t,B_t,C_t$; rồi tính $L(j)$ tại các ứng viên bằng tổng tiền tố; trả về ứng viên tốt nhất</td></tr></table>
   <p><b>Hai bổ đề then chốt</b> (nhắc lại khi chứng minh):</p>
   <ul style="margin:4px 0;padding-left:20px;line-height:1.5">
   <li><b>Đơn điệu:</b> với tập $S'\\subseteq S$ thì $g(S')\\le g(S)$, trong đó $g(S)=\\sum_{z\\in S}(z-\\mu(S))^2$: thêm phần tử không bao giờ làm tổng bình phương lệch <i>giảm</i>.</li>
   <li><b>Gần như liên tục (kiểu Lipschitz):</b> với $j'>j$ và $b$ là số quan sát trong $(j,j']$ thì $L(j')\\le L(j)+\\dfrac{5bM^2}{4m}$. Dịch ngưỡng qua ít quan sát thì sai số chỉ đổi chút.</li></ul>
   <p><b>Kiểm chứng bổ đề trên ví dụ 8 điểm</b> ($M=8$, $m=8$): dịch từ $j=4$ sang $j'=5$ vượt qua $b=1$ quan sát, vế phải $=0{,}5+5\\cdot1\\cdot64/(4\\cdot8)=10{,}5$; thực tế $L(5)=3\\le10{,}5$. Cận đúng nhưng khá lỏng, vì nó phải đúng cho mọi dữ liệu.</p>
   <div class="callout info"><div class="lbl">Cách đọc của nhóm (không phải câu chữ của bài báo)</div>Tính chất &quot;giữa hai ứng viên có không quá $\\varepsilon m$ quan sát&quot; chính là tính chất của một xấp xỉ phân vị (quantile): lấy mẫu ngẫu nhiên cho ta các điểm chia gần đều theo số lượng quan sát.
   Điều này nối thẳng với kiến thức quantile sketch đã học ở nửa đầu môn, dù bài báo dùng lấy mẫu chứ không dùng q-digest, MRL hay KLL.</div>"""),
  dict(h="Thuật toán nhiều lượt $(1+\\varepsilon)$: đoán sai số, tìm nhị phân, và đổi lượt lấy bộ nhớ", body="""
   <p>🗣️ <b>Nói nôm na:</b> trò đoán số: &quot;sai số của phía trái và phía phải của ngưỡng tối ưu cỡ bao nhiêu?&quot;. Thử đoán theo thang nhân $(1+\\varepsilon)$: $0,1+\\varepsilon,(1+\\varepsilon)^2,\\dots$.
   Với mỗi cặp đoán, dùng <b>tìm nhị phân</b> trên $[1,N]$: thử $j$ giữa, nếu cả hai phía đều trong giới hạn đoán thì $j$ khả thi, còn nếu một phía vượt thì loại bỏ nửa tương ứng.</p>
   <table><tr><th>Tình huống tại điểm thử $j$</th><th>Kết luận (nhờ tính đơn điệu)</th></tr>
   <tr><td>Cả hai phía trong giới hạn đoán</td><td>$j$ khả thi, lưu lại $L$</td></tr>
   <tr><td>Cả hai phía vượt giới hạn</td><td>Cặp đoán này sai, bỏ qua</td></tr>
   <tr><td>Chỉ phía trái vượt</td><td>Mọi ngưỡng bên phải $j$ còn tệ hơn: tìm tiếp bên trái</td></tr>
   <tr><td>Chỉ phía phải vượt</td><td>Mọi ngưỡng bên trái $j$ còn tệ hơn: tìm tiếp bên phải</td></tr></table>
   <p>Mỗi bước tìm nhị phân cần 2 lượt duyệt để tính $\\mu(j)$, $\\gamma(j)$ và hai sai số, nên được $O(\\log N)$ lượt, bộ nhớ $\\tilde O(1/\\varepsilon^2)$ (số cặp đoán). <b>Đổi lượt lấy bộ nhớ:</b> thay vì chạy $r$ bước nhị phân bằng $2r$ lượt, ta kiểm tra luôn
   $2^{r+1}-1$ ngưỡng có thể gặp trong 2 lượt, với bộ nhớ $\\tilde O(2^r)$. Đặt $2^r=N^{\\beta}$ thì cần lặp $O(1/\\beta)$ lần: <b>$O(1/\\beta)$ lượt, bộ nhớ $\\tilde O(N^{\\beta}/\\varepsilon^2)$.</b></p>
   <table><tr><th>Ví dụ (minh hoạ): $N=2^{20}\\approx10^6$</th><th>$r$ (bước nhị phân mỗi đợt)</th><th>Số đợt $20/r$</th><th>Số lượt $\\approx 2\\times$ số đợt</th><th>Số ngưỡng kiểm tra mỗi đợt $2^{r+1}-1$</th></tr>
   <tr><td>Ít bộ nhớ nhất</td><td>1</td><td>20</td><td>40</td><td>3</td></tr>
   <tr><td>Trung gian</td><td>5</td><td>4</td><td>8</td><td>63</td></tr>
   <tr><td>Nhiều bộ nhớ hơn</td><td>10</td><td>2</td><td>4</td><td>2047</td></tr></table>"""),
 ]))
