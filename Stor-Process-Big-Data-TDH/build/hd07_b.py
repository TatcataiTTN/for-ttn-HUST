# -*- coding: utf-8 -*-
"""Module hd-07 (phần 2/2): bài 2 (phân loại, Gini, MPC), bài 3 (một lượt, cận dưới), nối với Hadoop, tổng kết, quiz."""
from hd_add_common import fig, logo, logos, two

PARTS_B = []

# --------------------------------------------------------------------------------------------- PHẦN 5
PARTS_B.append(dict(
 title="Bài báo 2 (arXiv v4 04/2025, ISIT 2025): thêm Gini, thuộc tính phân loại, nhiều thuộc tính và luồng có xoá",
 bullets=[
  "Khác bài 1: thêm Gini, tổng quát hoá lượt-bộ nhớ qua $\\beta$, viết lại phần MPC",
  "Phân loại: lấy mẫu, ước lượng số đếm, Hoeffding và hợp xác suất (union bound)",
  "Thuộc tính phân loại: bộ nhớ $\\tilde O(N/\\varepsilon)$ và cận dưới $\\Omega(N)$",
  "Luồng có xoá: Count-Min sketch với phân rã dyadic, thêm hệ số $\\log N$"],
 slides=[
  dict(h="Bài báo 2: Constructing Decision Trees from Data Streams, những gì thay đổi so với bài 1", body=two(
   fig("ta2_title.png", "Trang đầu arXiv:2403.19867v4 [cs.DS], 16/04/2025, công bố tại ISIT 2025.", 80), """
   <p style="font-size:.95rem;margin:4px 0">Cùng mã arXiv với bài 1 (v1 và v4 của cùng một bản thảo), nhưng v4 được sửa sâu và đổi tên.</p>""", "44%") + """
   <table><tr><th>Nội dung</th><th>Bài 1 (v1, 03/2024)</th><th>Bài 2 (v4, 04/2025)</th></tr>
   <tr><td>Giả định i.i.d. và luồng vô hạn</td><td>Không dùng</td><td>Không dùng (cả hai)</td></tr>
   <tr><td>Tiêu chí phân loại</td><td>Tỉ lệ phân loại sai</td><td>Thêm <b>Gini impurity</b>: $\\tilde O(1/\\varepsilon^2)$ bộ nhớ, 1 lượt, sai số cộng $\\varepsilon$</td></tr>
   <tr><td>Thuật toán nhiều lượt</td><td>$O(\\log N)$ lượt, $\\tilde O(1/\\varepsilon^2)$ bộ nhớ</td><td>$O(1/\\beta)$ lượt, $\\tilde O(N^{\\beta}/\\varepsilon^2)$ bộ nhớ: đặt $\\beta=1/\\log N$ thì quay về kết quả cũ</td></tr>
   <tr><td>MPC</td><td>Chủ yếu $\\alpha=1/2$ (một vòng hằng số)</td><td>Viết lại theo $\\beta$ (Theorem 13, 14), tóm tắt nêu thẳng MapReduce</td></tr>
   <tr><td>Công trình liên quan nêu thêm</td><td>Domingos-Hulten 2000</td><td>Thêm Hulten-Spencer-Domingos 2001</td></tr></table>
   <div class="callout info"><div class="lbl">Cách đọc tên bài</div>Thuật toán trong bài vẫn <b>tìm một điểm chia</b> (cây sâu 1); tên &quot;Constructing Decision Trees&quot; phản ánh mục tiêu lớn hơn, vì muốn cây sâu hơn thì áp dụng lặp lại thuật toán,
   như cả hai bản đều nhắc.</div>"""),
  dict(h="Phân loại bằng lấy mẫu: ước lượng số đếm, rồi Hoeffding và hợp xác suất", body="""
   <p>Với tỉ lệ phân loại sai, $L(j)$ chỉ gồm 4 số đếm theo khoảng: $f_{-1,[1,j]}$, $f_{+1,[1,j]}$, $f_{-1,(j,N]}$, $f_{+1,(j,N]}$. Thuật toán 1 lượt trong bài chỉ làm 3 việc:</p>
   <table><tr><th>Bước</th><th>Nội dung</th></tr>
   <tr><td>1. Lấy mẫu</td><td>Giữ mỗi cặp $(x_i,y_i)$ độc lập với xác suất $p=C\\log N/(\\varepsilon m)$</td></tr>
   <tr><td>2. Ước lượng</td><td>Gọi $k$ là số điểm được lấy mẫu có nhãn $l$ trong đoạn $r$; ước lượng $\\tilde f_{l,r}=k/p$</td></tr>
   <tr><td>3. Chọn</td><td>Tính $\\tilde L(j)$ cho mọi $j$ là giá trị $x$ được lấy mẫu (bằng recurrence tiền tố $k_{u,[1,j_t]}=k_{u,[1,j_{t-1}]}+k_{u,[j_t,j_t]}$), trả về $j$ nhỏ nhất</td></tr></table>
   <p><b>Vì sao đúng:</b> theo bất đẳng thức Hoeffding, $\\Pr\\big(|k-pf|\\ge \\tfrac{\\varepsilon}{4}pm\\big)\\le 2e^{-\\varepsilon^2pm/8}$. Chọn hằng số $C$ đủ lớn thì mỗi ước lượng sai lệch không quá $\\varepsilon m/8$ với xác suất $\\ge 1-1/N^4$; lấy
   <b>hợp xác suất</b> trên $2$ nhãn $\\times$ $N$ khoảng thì mọi ước lượng cùng đúng với xác suất $\\ge1-1/N$. Khi đó $\\tilde L(j^\\star)\\le\\mathrm{OPT}+\\varepsilon/4$ và mọi $j$ có $\\tilde L(j)\\le\\mathrm{OPT}+\\varepsilon/4$ đều có $L(j)<\\mathrm{OPT}+\\varepsilon$.</p>
   <p><b>Ví dụ số (minh hoạ, giả định $C\\log N=100$):</b> $m=10^6$, $\\varepsilon=0{,}01$. Số mẫu kỳ vọng $pm=100/\\varepsilon=10\\,000$ (chỉ 1% dữ liệu); sai lệch mỗi số đếm $\\le\\varepsilon m/8=1\\,250$, tức $0{,}125\\%$ của $m$.</p>
   <div class="callout good"><div class="lbl">Ôn lại kiến thức đã học</div>Đây chính là &quot;Hoeffding + union bound&quot; của <a href="../05-hoeffding-union/index.html">module 05</a> và Chernoff của <a href="../04-chernoff/index.html">module 04</a>: Hoeffding cho từng số đếm, hợp xác suất cho mọi $N$ khoảng cùng lúc.</div>"""),
  dict(h="Gini impurity: vì sao khó hơn tỉ lệ phân loại sai", body="""
   <div class="pd-formula"><div class="pd-formula-label">Gini của một tập và của một ngưỡng chia</div>
   <div class="pd-formula-math">\\mathrm{Gini}(O)=1-\\sum_{l\\in\\{-1,+1\\}}\\Big(\\frac{\\#\\{y_i=l\\}}{|O|}\\Big)^2,\\qquad L_{\\mathrm{Gini}}(j)=\\frac{|L|}{m}\\mathrm{Gini}(L)+\\frac{|R|}{m}\\mathrm{Gini}(R)</div></div>
   <p>Khai triển ra, $L_{\\mathrm{Gini}}(j)=1-\\dfrac{f_{+1,[1,j]}^2}{m\\,f_{[1,j]}}-\\dfrac{f_{-1,[1,j]}^2}{m\\,f_{[1,j]}}-\\dfrac{f_{+1,(j,N]}^2}{m\\,f_{(j,N]}}-\\dfrac{f_{-1,(j,N]}^2}{m\\,f_{(j,N]}}$.
   Khác với tỉ lệ phân loại sai, mỗi số hạng là <b>tỉ số của hai số đếm</b> (một bình phương chia một tổng), nên chỉ đếm bằng lấy mẫu rồi nhân $1/p$ chưa đủ: sai số ở mẫu số khuếch đại.</p>
   <table><tr><th>Điểm trong bài</th><th>Ý</th></tr>
   <tr><td>Bổ đề 8</td><td>Nếu lấy mẫu $C\\log N/\\varepsilon$ quan sát thì mọi đoạn có từ $\\varepsilon m$ điểm trở lên đều chứa ít nhất $K/\\varepsilon\\cdot\\log N$ điểm mẫu: đoạn nào đủ lớn thì được đại diện đủ</td></tr>
   <tr><td>Hai mẫu độc lập</td><td>Bài lấy <b>hai</b> tập mẫu độc lập $S_1,S_2$ cỡ $C/\\varepsilon^2\\cdot\\log N$ rồi dùng thuật toán 5 để ước lượng các số hạng dạng $f^2/(mf)$</td></tr>
   <tr><td>Kết quả</td><td>1 lượt, bộ nhớ $\\tilde O(1/\\varepsilon^2)$, $L_{\\mathrm{Gini}}(j)\\le\\mathrm{OPT}+\\varepsilon$ (hàng C.2 của Figure 2)</td></tr></table>
   <div class="callout info"><div class="lbl">Suy luận của nhóm về vai trò hai mẫu</div>Bình phương một số đếm có thể ước lượng không chệch bằng tích hai ước lượng <i>độc lập</i> (vì kỳ vọng của tích độc lập bằng tích kỳ vọng); có lẽ đó là lý do cần hai mẫu độc lập. Bài báo không nêu câu này trong phần tóm tắt, cần đọc Algorithm 5 để kiểm chứng.</div>
   <p><b>Ví dụ số (giả định):</b> $m=6$; phía trái nhãn $(+1,+1,-1)$, phía phải nhãn $(-1,-1,+1)$. Mỗi phía có $\\mathrm{Gini}=1-(2/3)^2-(1/3)^2=4/9$, nên $L_{\\mathrm{Gini}}=\\tfrac36\\cdot\\tfrac49+\\tfrac36\\cdot\\tfrac49=4/9\\approx0{,}444$.
   Bài 3 sẽ dùng đúng ví dụ kiểu này để chứng minh $L_{\\mathrm{Gini}}=2L_{\\mathrm{MSE}}$ (phần 7).</p>"""),
  dict(h="Thuộc tính phân loại: bộ nhớ $\\tilde O(N/\\varepsilon)$ và cận dưới $\\Omega(N)$", body="""
   <p>🗣️ <b>Nói nôm na:</b> với số tuổi, ngưỡng chia chỉ là &quot;cắt một nhát&quot; trên trục số. Với <i>quốc gia</i> hay <i>màu sắc</i> không có thứ tự, bạn phải chia tập giá trị thành hai nhóm tuỳ ý, tức là có rất nhiều cách chia.</p>
   <table><tr><th></th><th>Thuộc tính có thứ tự (số)</th><th>Thuộc tính phân loại (không thứ tự)</th></tr>
   <tr><td>Cách chia</td><td>Ngưỡng $j$: chia $[1,j]$ và $(j,N]$</td><td>Phân hoạch $[N]=A\\sqcup B$ bất kỳ</td></tr>
   <tr><td>Số cách chia</td><td>Khoảng $N$</td><td>Cỡ $2^N$</td></tr>
   <tr><td>Sai số</td><td>$L(j)$</td><td>$L(A,B)=\\frac1m\\big(\\min\\{f_{-1,A},f_{+1,A}\\}+\\min\\{f_{-1,B},f_{+1,B}\\}\\big)$</td></tr>
   <tr><td>Kết quả của bài</td><td>Bộ nhớ $\\tilde O(1/\\varepsilon)$, 1 lượt</td><td>1 lượt, bộ nhớ $\\tilde O(N/\\varepsilon)$, cập nhật $O(1)$, hậu xử lý $O(2^N)$</td></tr>
   <tr><td>Cận dưới</td><td>Xem bài 3: $\\Omega(1/\\varepsilon)$</td><td>Mọi thuật toán <b>hằng số lượt</b> quyết định được liệu $\\mathrm{OPT}=0$ đều cần $\\Omega(N)$ bộ nhớ</td></tr></table>
   <p><b>Ví dụ số (minh hoạ):</b> $N=20$ nhóm giá trị $\\Rightarrow 2^{20}=1\\,048\\,576$ phân hoạch phải xét ở hậu xử lý; $N=40$ thì $2^{40}\\approx1{,}1\\times10^{12}$, không còn khả thi.
   Cận dưới $\\Omega(N)$ nói điều quan trọng hơn thời gian: <b>bộ nhớ tuyến tính theo số giá trị phân biệt là không tránh được</b> đối với thuộc tính phân loại.</p>
   <div class="callout warn"><div class="lbl">Bài học thực hành</div>Đặc trưng phân loại có hàng triệu giá trị (mã bưu chính, id người dùng) không thể xử lý chính xác trên luồng bằng bộ nhớ nhỏ; thực tế người ta gom nhóm hoặc băm trước. Điều này giải thích vì sao các bài báo tập trung vào thuộc tính số có thứ tự.</div>"""),
  dict(h="Nhiều thuộc tính và luồng có xoá: Count-Min sketch với phân rã dyadic", body="""
   <table><tr><th>Mở rộng</th><th>Cách làm trong bài</th><th>Cái giá</th></tr>
   <tr><td><b>$d$ thuộc tính</b></td><td>Chạy thuật toán riêng cho từng thuộc tính rồi chọn ngưỡng tốt nhất qua mọi thuộc tính: $\\arg\\min_{q\\in[d],j\\in[N]}L_q(j)$</td><td>Bộ nhớ nhân thêm hệ số $d$</td></tr>
   <tr><td><b>Luồng có xoá</b> (dynamic stream)</td><td>Thay lấy mẫu bằng <b>Count-Min sketch với phân rã dyadic</b> để ước lượng số đếm theo khoảng</td><td>Thêm hệ số $\\log N$ vào bộ nhớ và thời gian cập nhật</td></tr></table>
   <p><b>Vì sao dyadic?</b> Mọi khoảng $[l,r]\\subseteq[1,N]$ tách được thành tối đa cỡ $2\\log_2 N$ khoảng dyadic (độ dài $2^k$, bắt đầu tại bội của $2^k$); mỗi tầng $k$ có một Count-Min sketch riêng. Số đếm của khoảng bằng tổng số đếm các mảnh dyadic.</p>
   <table><tr><th>Ví dụ (minh hoạ)</th><th>Phân rã dyadic</th><th>Số mảnh</th></tr>
   <tr><td>$N=8$, khoảng $[3,7]$</td><td>$[3,3]\\cup[4,7]$</td><td>2</td></tr>
   <tr><td>$N=16$, khoảng $[2,13]$</td><td>$[2,3]\\cup[4,7]\\cup[8,11]\\cup[12,13]$</td><td>4 (tối đa cỡ $2\\log_2 16=8$)</td></tr></table>
   <div class="callout good"><div class="lbl">Ôn lại kiến thức đã học</div>Count-Min nằm ở <a href="../11-ham-bam/index.html">module 11</a>, cây dyadic và rank ở <a href="../12-cay-nhi-phan/index.html">module 12</a>. Bài báo tận dụng đúng cặp công cụ đó: Count-Min cho số đếm, dyadic cho <i>khoảng</i>, và hai thứ cùng chịu được phép xoá vì sketch là cấu trúc tuyến tính.</div>"""),
 ]))

# --------------------------------------------------------------------------------------------- PHẦN 6
PARTS_B.append(dict(
 title="Từ streaming sang MPC: thuật toán một vòng hằng số và cách dịch sang Hadoop",
 bullets=[
  "Sắp theo $x$ trong $O(1)$ vòng, lấy mẫu cục bộ, một máy trung tâm chọn ứng viên",
  "Gửi ứng viên tới mọi máy, mỗi máy tính tổng cục bộ, gộp lại: $O(1)$ vòng",
  "Mỗi bước dịch thành giai đoạn nào trong Hadoop (đối chiếu của nhóm)"],
 slides=[
  dict(h="Thuật toán MPC cho hồi quy: các bước (theo bài báo)", body="""
   <p>Cụm có $\\sqrt m$ máy, mỗi máy $\\tilde O(\\sqrt m)$ bộ nhớ, nhãn $M=O(1)$. Ý tưởng: lấy thuật toán 2 lượt (lấy mẫu chọn ứng viên, rồi đếm chính xác) và đặt hai &quot;lượt&quot; thành vài vòng.</p>
   <table><tr><th>Bước</th><th>Việc làm</th><th>Vòng (nhóm ước tính; bài chỉ nêu tổng $O(1)$)</th></tr>
   <tr><td>1</td><td><b>Sắp xếp</b> các cặp $(x_i,y_i)$ theo $x_i$ và lưu lên các máy $M_1,M_2,\\dots,M_{\\sqrt m}$ theo đúng thứ tự (kỹ thuật sắp xếp MPC có sẵn)</td><td>$O(1)$</td></tr>
   <tr><td>2</td><td>Mỗi máy độc lập lấy mẫu mỗi quan sát với xác suất $p=C\\log N/\\sqrt m$; mỗi máy giữ $\\tilde O(1)$ mẫu</td><td>(cục bộ)</td></tr>
   <tr><td>3</td><td>Mọi máy gửi mẫu tới <b>một máy trung tâm</b>; máy này nhận $\\tilde O(\\sqrt m)$ mẫu nên vừa bộ nhớ</td><td>1</td></tr>
   <tr><td>4</td><td>Máy trung tâm chọn tập ứng viên $S=\\{j_1,\\dots,j_k\\}$ với $k=O(\\sqrt m)$ như thuật toán 2 lượt</td><td>(cục bộ)</td></tr>
   <tr><td>5</td><td>Máy trung tâm <b>gửi $S$ tới mọi máy</b> (mỗi máy nhận thông điệp $\\tilde O(\\sqrt m)$)</td><td>1</td></tr>
   <tr><td>6</td><td>Máy $M_q$ tính phần tổng cục bộ $A_{t,q},B_{t,q},C_{t,q}$ trên các đoạn giữa các ứng viên mà nó giữ, rồi gửi về trung tâm</td><td>1</td></tr>
   <tr><td>7</td><td>Máy trung tâm cộng các phần để có $A_t,B_t,C_t$, tính $L(j_t)$, trả về ứng viên tốt nhất</td><td>(cục bộ)</td></tr></table>
   <div class="callout good"><div class="lbl">Vì sao thông điệp về trung tâm vẫn $\\tilde O(\\sqrt m)$</div>Nhờ bước 1, dữ liệu đã được sắp theo $x$ nên mỗi máy giữ một đoạn liên tiếp. Mỗi máy chỉ có <b>nhiều nhất 2 ứng viên &quot;biên&quot;</b> bị chia sẻ với máy khác; các ứng viên nằm hẳn trong một máy thì chỉ một máy phụ trách.
   Tổng số cặp (ứng viên, máy) là $\\le 2\\sqrt m+O(\\sqrt m)=O(\\sqrt m)$. Kết quả: $L(j)\\le\\mathrm{OPT}+O(1/\\sqrt m)$ trong $O(1)$ vòng.</div>"""),
  dict(h="Dịch sang Hadoop: mỗi bước là một giai đoạn nào (đối chiếu của nhóm)", body="""
   <p>Bài báo viết bằng ngôn ngữ MPC; bảng dưới là <b>cách nhóm đối chiếu</b> sang các thành phần đã học ở module hd-01 và hd-02. Đây là đối chiếu ý tưởng, không phải mã trong bài báo.</p>
   <table><tr><th>Bước MPC</th><th>Thành phần Hadoop tương ứng</th><th>Gợi ý đối chiếu</th></tr>
   <tr><td>Sắp theo $x$, dữ liệu liên tiếp trên các máy</td><td>Job sắp xếp toàn cục, như ví dụ <i>Distributed Sort</i> của bài MapReduce</td><td>Phân vùng theo khoảng giá trị $x$ để mỗi reducer giữ một đoạn liên tiếp; Hadoop có sẵn lớp lấy mẫu và phân vùng theo thứ tự toàn cục cho việc này (nhóm chưa thử, cần kiểm tra tài liệu Hadoop)</td></tr>
   <tr><td>Mỗi máy lấy mẫu với xác suất $p$</td><td>Mã trong hàm map: giữ mỗi bản ghi với xác suất $p$</td><td>Mẫu rất nhỏ so với dữ liệu</td></tr>
   <tr><td>Một máy trung tâm nhận mẫu và chọn ứng viên</td><td>Một reducer duy nhất, hoặc chương trình điều khiển (driver)</td><td>Chỉ $\\tilde O(\\sqrt m)$ mẫu nên một máy là đủ</td></tr>
   <tr><td>Gửi tập ứng viên tới mọi máy</td><td>Phát tới mọi task (ví dụ qua bộ nhớ đệm phân tán hoặc cấu hình job)</td><td>Kích thước $\\tilde O(\\sqrt m)$, vừa trong bộ nhớ mỗi task</td></tr>
   <tr><td>Mỗi máy tính $A,B,C$ cục bộ trên các đoạn</td><td>Giai đoạn map + <b>combiner</b>: cộng dồn theo đoạn trước khi shuffle</td><td>Đúng vai trò combiner trong bài MapReduce: giảm lưu lượng shuffle</td></tr>
   <tr><td>Máy trung tâm cộng các phần và chọn $j$ tốt nhất</td><td>Một reducer cộng các tổng riêng rồi tính $L(j_t)$</td><td>$O(\\sqrt m)$ cặp, rất nhỏ</td></tr></table>
   <div class="callout info"><div class="lbl">Số job và số vòng</div>Nếu gộp thật gọn, thuật toán cần cỡ <b>2 đến 3 job MapReduce nối tiếp</b> (một job sắp xếp và lấy mẫu, một job tính tổng theo ứng viên), tức $O(1)$ vòng.
   Con số này là ước lượng của nhóm khi đối chiếu, bài báo chỉ nói $O(1)$ vòng. Theo hd-02, mỗi job thêm là một lần shuffle qua đĩa và mạng: chính vì vậy việc giữ số vòng hằng số có giá trị thực tế.</div>"""),
  dict(h="Kết quả MPC (Theorem 13, 14) và đánh đổi theo $\\beta$", body=fig("ta_fig3_mpc.png",
   "Figure 3 (arXiv:2403.19867v4): kết quả MPC; R = hồi quy, C.1 = phân loại sai, C.2 = Gini.", 100) + """
   <table><tr><th>Bài toán</th><th>Số máy và bộ nhớ mỗi máy</th><th>Số vòng</th><th>Đảm bảo</th></tr>
   <tr><td>Hồi quy, $M=O(1)$</td><td>$\\sqrt m$ máy, $\\tilde O(\\sqrt m)$</td><td>$O(1)$</td><td>$L(j)\\le\\mathrm{OPT}+O(1/\\sqrt m)$</td></tr>
   <tr><td>Hồi quy và phân loại sai</td><td>$m^{1-\\beta}$ máy, $\\tilde O(m^{\\beta}/\\varepsilon^2)$</td><td>$O(1/\\beta)$</td><td>$L(j)\\le(1+\\varepsilon)\\mathrm{OPT}$</td></tr>
   <tr><td>Phân loại, tiêu chí misclassification</td><td>$\\sqrt m$ máy, $\\tilde O(\\sqrt m)$</td><td>1</td><td>$L(j)\\le\\mathrm{OPT}+1/\\sqrt m$</td></tr>
   <tr><td>Phân loại, tiêu chí Gini</td><td>$\\sqrt m$ máy, $\\tilde O(\\sqrt m)$</td><td>1</td><td>$L_{\\mathrm{Gini}}(j)\\le\\mathrm{OPT}+1/m^{0{,}25}$ (tương đương $\\varepsilon=1/m^{1/4}$)</td></tr></table>
   <p><b>Ví dụ số (minh hoạ), $m=10^6$:</b> $\\sqrt m=1\\,000$ máy, mỗi máy cỡ 1.000 phần tử; sai số cộng $1/\\sqrt m=0{,}001$ với hồi quy và phân loại sai, nhưng $1/m^{0{,}25}\\approx0{,}032$ với Gini: <b>Gini thô hơn khoảng 32 lần</b> ở cùng cấu hình.</p>
   <p><b>Mô phỏng nhiều bước nhị phân trong $O(1)$ vòng:</b> với $\\beta$ cố định, ta kiểm tra $2^{r+1}-1=O(m^{\\beta})$ ngưỡng ứng viên cùng lúc, mô phỏng $r=\\beta\\log N$ bước nhị phân trong $O(1)$ vòng (nhờ bổ đề 12: tính được sai số của $k=O(m^\\beta)$ ứng viên trong $O(1)$ vòng); do đó cần $O(1/\\beta)$ vòng tổng cộng.</p>"""),
 ]))

# --------------------------------------------------------------------------------------------- PHẦN 7
PARTS_B.append(dict(
 title="Bài báo 3 (arXiv 07/2026, ESA 2026): một lượt duyệt thật sự, và cận dưới khớp",
 bullets=[
  "Cải tiến: hồi quy 1 lượt thay 2 lượt; Gini $\\tilde O(1/\\varepsilon)$ thay $\\tilde O(1/\\varepsilon^2)$",
  "Thuật toán: reservoir sampling + ba Count-Min sketch cho ba 'moment' $n_R$, $s_R$, $q_R$",
  "Gini quy về hồi quy qua đồng nhất thức $L_{\\mathrm{Gini}}=2L_{\\mathrm{MSE}}$",
  "Cận dưới khớp bằng quy dẫn từ bài toán Index"],
 slides=[
  dict(h="Bài báo 3: Nearly Optimal Bounds, bảng cận trên và cận dưới", body=two(
   fig("ta3_title.png", "Trang đầu arXiv:2604.20394v2 [cs.DS], 07/07/2026, ESA 2026.", 120), fig("ta3_fig1.png",
   "Figure 1 (arXiv:2604.20394v2): ngưỡng tối ưu $j^\\star$, $\\mu(j^\\star)$ và $\\gamma(j^\\star)$ là giá trị dự đoán hai phía.", 130), "56%") + """
   <table><tr><th>Mục tiêu</th><th>Số lượt</th><th>Cận trên</th><th>Nguồn</th></tr>
   <tr><td>Hồi quy</td><td>2</td><td>$\\tilde O(M^2/\\varepsilon)$</td><td>Bài 2</td></tr>
   <tr><td><b>Hồi quy</b></td><td><b>1</b></td><td><b>$\\tilde O(M^2/\\varepsilon)$</b> ($\\tilde O(1/\\varepsilon)$ khi $M=O(1)$)</td><td>Bài 3</td></tr>
   <tr><td>Misclassification</td><td>1</td><td>$\\tilde O(1/\\varepsilon)$</td><td>Bài 2</td></tr>
   <tr><td>Gini</td><td>1</td><td>$\\tilde O(1/\\varepsilon^2)$</td><td>Bài 2</td></tr>
   <tr><td><b>Gini</b></td><td><b>1</b></td><td><b>$\\tilde O(1/\\varepsilon)$</b></td><td>Bài 3</td></tr></table>
   <table><tr><th>Cận dưới (1 lượt, xác suất thành công $\\ge2/3$)</th><th>Bộ nhớ</th></tr>
   <tr><td>Hồi quy</td><td>$\\Omega(M^2/\\varepsilon)$</td></tr><tr><td>Misclassification</td><td>$\\Omega(1/\\varepsilon)$</td></tr><tr><td>Gini</td><td>$\\Omega(1/\\varepsilon)$</td></tr></table>
   <p style="font-size:.92rem">Cận trên và cận dưới <b>khớp nhau</b> tới hệ số polylog: không thuật toán một lượt nào dùng ít bộ nhớ hơn nhiều. Thêm: thuật toán mới <b>không cần biết trước độ dài luồng $m$</b> (khác bài 2).
   Chỉ xét luồng chỉ-thêm (insertion-only); độ phức tạp của thuật toán <i>tất định</i> được bài báo nêu là câu hỏi mở.</p>"""),
  dict(h="Thuật toán một lượt: reservoir sampling và ba Count-Min sketch", body="""
   <p>🗣️ <b>Nói nôm na:</b> hai việc chia nhau. Một người bốc thăm vài giá trị $x$ làm <b>ứng viên</b> (reservoir sampling). Ba cuốn sổ Count-Min ghi sổ <b>mọi</b> điểm: sổ 1 đếm số điểm, sổ 2 cộng nhãn, sổ 3 cộng bình phương nhãn,
   để tra nhanh cho <i>bất kỳ khoảng</i> nào.</p>
   <table><tr><th>Bước</th><th>Nội dung (theo bài báo)</th></tr>
   <tr><td>1</td><td>Giữ một <b>reservoir sample</b> cỡ $K$ trong suốt luồng; sau luồng, ứng viên $S=\\{0,N\\}\\cup\\{x,x-1\\}$ với $x$ trong mẫu</td></tr>
   <tr><td>2</td><td>Đồng thời duy trì <b>3 sketch Count-Min hỗ trợ truy vấn khoảng</b> với $k=1/\\beta$ cho 3 luồng $(x_i,1)$, $(x_i,y_i)$, $(x_i,y_i^2)$</td></tr>
   <tr><td>3</td><td>Truy vấn ra ước lượng $\\hat n_R,\\hat s_R,\\hat q_R$ cho mọi khoảng $R$; đặt $\\widehat{\\mathrm{SSE}}(R)=\\hat q_R-\\hat s_R^2/(\\hat n_R+\\beta m)$ (mẫu số cộng $\\beta m$ để kiểm soát sai số do ước lượng dư; nếu $\\hat n_R=0$ thì đặt SSE bằng 0)</td></tr>
   <tr><td>4</td><td>Với mỗi ứng viên $j\\in S$: $\\hat L_{\\mathrm{MSE}}(j)=\\frac1m\\big(\\widehat{\\mathrm{SSE}}([1,j])+\\widehat{\\mathrm{SSE}}([j+1,N])\\big)$</td></tr>
   <tr><td>5</td><td>Trả về $\\hat j=\\arg\\min_{j\\in S}\\hat L_{\\mathrm{MSE}}(j)$</td></tr></table>
   <p><b>Ba moment và SSE:</b> với khoảng $R$ đặt $n_R=\\sum\\mathbf 1[x_i\\in R]$, $s_R=\\sum\\mathbf 1[x_i\\in R]y_i$, $q_R=\\sum\\mathbf 1[x_i\\in R]y_i^2$. Khi đó $\\sum_{x_i\\in R}(y_i-\\bar y_R)^2=q_R-s_R^2/n_R=\\mathrm{SSE}(R)$ và $m\\,L_{\\mathrm{MSE}}(j)=\\mathrm{SSE}([1,j])+\\mathrm{SSE}([j+1,N])$.
   <b>Kiểm tra bằng ví dụ 8 điểm:</b> $\\mathrm{SSE}([1,4])=198-28^2/4=2$, $\\mathrm{SSE}([5,8])=18-8^2/4=2$, nên $m\\,L=4$, $L=0{,}5$, khớp bảng tính tay.</p>
   <div class="callout good"><div class="lbl">Vì sao kết hợp hai công cụ</div>Lấy mẫu cho ta <b>tập ứng viên nhỏ chứa một điểm chia gần tối ưu</b> (nhờ tính Lipschitz của hàm mất mát); Count-Min cho số đếm theo khoảng của ba moment trong 1 lượt với bộ nhớ nhỏ.
   Định lý 1: bộ nhớ $\\tilde O(M^2/\\varepsilon)$, cập nhật $O(1)$, $L_{\\mathrm{MSE}}(\\hat j)\\le\\mathrm{OPT}+\\varepsilon$ với xác suất cao.</div>"""),
  dict(h="Gini quy về hồi quy: đồng nhất thức $L_{\\mathrm{Gini}}=2L_{\\mathrm{MSE}}$", body="""
   <p>Chỉ cần <b>mã hoá lại nhãn</b>: $z_i=(y_i+1)/2\\in\\{0,1\\}$. Bài báo chứng minh với mọi ngưỡng $j$: $L_{\\mathrm{Gini}}(j)=2\\,L_{\\mathrm{MSE}}(j)$ trên luồng $(x_i,z_i)$.
   Hệ quả: $\\mathrm{OPT}_{\\mathrm{Gini}}=2\\,\\mathrm{OPT}_{\\mathrm{MSE}}$ và hai tiêu chí có <b>cùng ngưỡng tối ưu</b>.</p>
   <p><b>Kiểm chứng bằng ví dụ ở phần trước</b> ($m=6$, trái nhãn $(+1,+1,-1)$, phải nhãn $(-1,-1,+1)$):</p>
   <table><tr><th>Đại lượng</th><th>Tính</th><th>Kết quả</th></tr>
   <tr><td>$L_{\\mathrm{Gini}}$</td><td>$\\tfrac36\\cdot\\tfrac49+\\tfrac36\\cdot\\tfrac49$</td><td>$4/9\\approx0{,}444$</td></tr>
   <tr><td>Mã hoá lại</td><td>Trái $z=(1,1,0)$ trung bình $2/3$; phải $z=(0,0,1)$ trung bình $1/3$</td><td></td></tr>
   <tr><td>SSE trái</td><td>$2\\cdot(1/3)^2+(2/3)^2$</td><td>$2/3$</td></tr>
   <tr><td>SSE phải</td><td>$2\\cdot(1/3)^2+(2/3)^2$</td><td>$2/3$</td></tr>
   <tr><td>$L_{\\mathrm{MSE}}$</td><td>$(2/3+2/3)/6$</td><td>$2/9\\approx0{,}222$</td></tr>
   <tr><td>$2L_{\\mathrm{MSE}}$</td><td>$2\\times 2/9$</td><td><b>$4/9$ = $L_{\\mathrm{Gini}}$</b></td></tr></table>
   <div class="callout info"><div class="lbl">Hệ quả thuật toán</div>Áp dụng thuật toán hồi quy với $M=1$ và sai số $\\varepsilon/2$: bộ nhớ $\\tilde O(M^2/(\\varepsilon/2))=\\tilde O(1/\\varepsilon)$, và nhân đôi trở lại cho $L_{\\mathrm{Gini}}(\\hat j)\\le\\mathrm{OPT}_{\\mathrm{Gini}}+\\varepsilon$.
   Nhờ vậy Gini giảm từ $\\tilde O(1/\\varepsilon^2)$ (bài 2) xuống $\\tilde O(1/\\varepsilon)$ chỉ bằng một phép mã hoá, một ví dụ đẹp về việc <b>đổi bài toán</b> thay vì đổi thuật toán.</div>"""),
  dict(h="Cận dưới: quy dẫn từ bài toán Index", body="""
   <p>🗣️ <b>Nói nôm na:</b> An cầm một dãy bit dài $n$ và chỉ được gửi cho Bình <b>một tin nhắn</b>; Bình chỉ muốn biết bit thứ $i$ (An không biết $i$). Dù An khôn khéo thế nào, tin nhắn vẫn phải dài cỡ $n$ bit: đó là bài toán <b>Index</b>.</p>
   <table><tr><th>Phần</th><th>Nội dung</th></tr>
   <tr><td>Bài toán Index</td><td>Alice giữ $z\\in\\{0,1\\}^n$, Bob giữ $i\\in[n]$, Bob phải xuất $z_i$. Mọi giao thức ngẫu nhiên một chiều thành công với xác suất $\\ge2/3$ cần $\\Omega(n)$ bit truyền</td></tr>
   <tr><td>Khuôn mẫu chung</td><td>Dựng một luồng có <b>hai ngưỡng chia liền kề cạnh tranh</b>, mà việc ngưỡng nào tốt hơn <b>tiết lộ bit ẩn</b></td></tr>
   <tr><td>Cách dùng bộ nhớ</td><td>Alice đưa dữ liệu mã hoá $z$ vào luồng và chạy thuật toán streaming; trạng thái bộ nhớ chính là &quot;tin nhắn&quot; gửi cho Bob. Bob thêm dữ liệu ứng với chỉ số $i$ rồi xem thuật toán chọn ngưỡng nào để suy ra $z_i$</td></tr>
   <tr><td>Kết luận</td><td>Bộ nhớ của thuật toán không thể nhỏ hơn số bit cần để giải Index: hồi quy cần $\\Omega(M^2/\\varepsilon)$ (nhờ co giãn nhãn: $L(y)=M^2L(y/M)$), misclassification và Gini cần $\\Omega(1/\\varepsilon)$</td></tr></table>
   <p><b>Ví dụ số (minh hoạ):</b> $\\varepsilon=0{,}001$, $M=1$: cần ít nhất cỡ $1/\\varepsilon=1\\,000$ bit. Nếu nhãn lớn $M=10$: $M^2/\\varepsilon=100\\,000$ bit, tức nhân $100$ lần chỉ vì khoảng nhãn rộng gấp 10.</p>
   <div class="callout warn"><div class="lbl">Điều bài báo nêu là còn mở</div>Các cận dưới áp dụng cho thuật toán <b>ngẫu nhiên</b> (thành công với xác suất tối thiểu $2/3$). Độ phức tạp của thuật toán <b>tất định</b> cho bài toán này vẫn là câu hỏi mở.</div>"""),
 ]))

# --------------------------------------------------------------------------------------------- PHẦN 8
PARTS_B.append(dict(
 title="Nối với Hadoop: số vòng, shuffle và combiner, và những điều các bài báo không nói",
 bullets=[
  "Bảng nối khái niệm bài báo ↔ khái niệm Hadoop (hd-01 đến hd-06)",
  "Đã chứng minh, còn mở, và nhóm suy luận: ba tầng mức chắc chắn",
  "Điểm cần nhớ khi trình bày: nói rõ phần nào là của bài báo, phần nào là của nhóm"],
 slides=[
  dict(h="Bảng nối: khái niệm trong bài báo và khái niệm trong Hadoop", body="""
   <table><tr><th>Bài báo (streaming và MPC)</th><th>Hadoop (module)</th><th>Mức chắc chắn</th></tr>
   <tr><td>$m$ quan sát chia cho $m^{1-\\beta}$ máy</td><td>Block của HDFS rải trên các DataNode (hd-01)</td><td>Đối chiếu của nhóm</td></tr>
   <tr><td>Bộ nhớ mỗi máy $\\tilde O(m^{\\beta})$</td><td>Bộ nhớ một container/task (hd-02)</td><td>Đối chiếu của nhóm</td></tr>
   <tr><td>MPC là trừu tượng hoá của MapReduce, Hadoop, Spark</td><td>Toàn bộ hd-02</td><td><b>Bài báo nêu</b></td></tr>
   <tr><td>Một vòng giao tiếp</td><td>Một job MapReduce có shuffle: map ghi đĩa cục bộ, reduce đọc từ xa (bài MapReduce, Figure 1)</td><td>Đối chiếu; chi tiết đĩa/mạng từ bài MapReduce</td></tr>
   <tr><td>Sắp theo $x$ trong $O(1)$ vòng</td><td>Ví dụ Distributed Sort trong bài MapReduce</td><td><b>Bài báo nêu</b> bước sắp; ví dụ Distributed Sort từ bài MapReduce</td></tr>
   <tr><td>Máy trung tâm chọn ứng viên</td><td>Một reducer hoặc driver</td><td>Đối chiếu của nhóm</td></tr>
   <tr><td>Tính tổng cục bộ rồi cộng lại</td><td>Combiner rồi reducer (hd-02, hd-03)</td><td>Đối chiếu của nhóm</td></tr>
   <tr><td>Count-Min cộng được từng ô</td><td>Mỗi mapper dựng sketch riêng, reducer cộng lại (như combiner)</td><td><b>Suy luận của nhóm</b> (bài báo chỉ dùng Count-Min cho luồng có xoá)</td></tr>
   <tr><td>Luồng sự kiện vào liên tục</td><td>Kafka là nguồn luồng (hd-05)</td><td>Đối chiếu của nhóm</td></tr></table>
   <div class="callout info"><div class="lbl">Cách dùng bảng này</div>Khi trình bày hay bị hỏi, nên nói rõ cột &quot;mức chắc chắn&quot;: chỉ những dòng in đậm là <i>câu chữ của bài báo</i>; các dòng còn lại là cách nhóm hiểu để nối với kiến thức Chương 2.</div>"""),
  dict(h="Đã chứng minh, còn mở, và nhóm suy luận", body="""
   <div class="callout good"><div class="lbl">Đã chứng minh (theo các bài đã đọc)</div><ul style="margin:6px 0 0;padding-left:20px;line-height:1.5">
   <li>Streaming, hồi quy: thuật toán 1 lượt $\\tilde O(M^2/\\varepsilon)$ và <b>cận dưới khớp $\\Omega(M^2/\\varepsilon)$</b> (bài 3).</li>
   <li>Streaming, Gini: thuật toán 1 lượt $\\tilde O(1/\\varepsilon)$ và cận dưới $\\Omega(1/\\varepsilon)$ (bài 3); misclassification $\\tilde O(1/\\varepsilon)$ khớp $\\Omega(1/\\varepsilon)$.</li>
   <li>Thuộc tính phân loại: $\\tilde O(N/\\varepsilon)$ và $\\Omega(N)$ cho mọi thuật toán hằng số lượt (bài 1, 2).</li>
   <li>MPC: các cận trên $O(1)$ vòng và $O(1/\\beta)$ vòng (bài 1, 2).</li></ul></div>
   <div class="callout warn"><div class="lbl">Còn mở (theo chính các bài hoặc theo việc các bài không nêu)</div><ul style="margin:6px 0 0;padding-left:20px;line-height:1.5">
   <li>Độ phức tạp của thuật toán <b>tất định</b> (bài 3 nêu).</li>
   <li>Bài 3 chỉ xét streaming; bảng MPC của bài 2 chỉ có <b>cận trên</b>. Các bài đã đọc không nêu cận dưới MPC, và không nói thuật toán 1 lượt của bài 3 có chuyển sang MPC với ít vòng hơn hay không.</li>
   <li>Dựng cả cây (không chỉ cây sâu 1): các bài chỉ nói áp dụng lặp lại, thêm lượt duyệt.</li></ul></div>
   <div class="callout info"><div class="lbl">Suy luận của nhóm (không phải khẳng định của bài báo)</div><ul style="margin:6px 0 0;padding-left:20px;line-height:1.5">
   <li>Count-Min cộng được từng ô nên có thể dựng sketch riêng ở từng mapper rồi cộng ở reducer.</li>
   <li>Tính chất &quot;giữa hai ứng viên có không quá $\\varepsilon m$ quan sát&quot; giống một xấp xỉ phân vị.</li>
   <li>Mỗi bước MPC dịch được thành giai đoạn MapReduce như bảng đối chiếu trước.</li></ul></div>"""),
 ]))

# --------------------------------------------------------------------------------------------- PHẦN 9
PARTS_B.append(dict(
 title="Tổng kết: ba bài báo, một câu chuyện nối tiếp",
 bullets=[
  "Từ thuật toán chính xác tới xấp xỉ, từ 2 lượt tới 1 lượt, từ cận trên tới cận khớp",
  "Danh mục trích dẫn và liên kết tới PDF"],
 slides=[
  dict(h="Ba bài báo nối tiếp nhau như thế nào", body="""
   <table><tr><th>Mốc</th><th>Bài</th><th>Đóng góp chính</th></tr>
   <tr><td>28/03/2024</td><td>arXiv:2403.19867v1<br/><i>Finding Decision Tree Splits in Streaming and Massively Parallel Models</i></td><td>Thuật toán chính xác 1 lượt $\\tilde O(D)$; xấp xỉ 2 lượt $\\tilde O(1/\\varepsilon)$; $O(\\log N)$ lượt cho $(1+\\varepsilon)$; phân loại; thuộc tính phân loại; MPC $O(1)$ vòng</td></tr>
   <tr><td>16/04/2025<br/>(ISIT 2025)</td><td>arXiv:2403.19867v4<br/><i>Constructing Decision Trees from Data Streams</i></td><td>Thêm Gini; tổng quát hoá lượt-bộ nhớ qua $\\beta$: $O(1/\\beta)$ lượt; viết lại phần MPC theo $\\beta$</td></tr>
   <tr><td>07/07/2026<br/>(ESA 2026)</td><td>arXiv:2604.20394v2<br/><i>Nearly Optimal Bounds for Computing Decision Tree Splits in Data Streams</i></td><td>1 lượt cho hồi quy và Gini; $\\tilde O(M^2/\\varepsilon)$ khớp $\\Omega(M^2/\\varepsilon)$; Gini quy về hồi quy; không cần biết $m$ trước</td></tr></table>
   <div class="callout good"><div class="lbl">Mạch phát triển</div>Mỗi bài trả lời câu hỏi mà bài trước để lại: bài 1 chứng minh làm được với bộ nhớ nhỏ; bài 2 làm rõ <i>đổi lượt lấy bộ nhớ</i> như thế nào và đưa Gini vào; bài 3 trả lời câu hỏi
   &quot;<b>còn làm tốt hơn nữa được không?</b>&quot; bằng cách vừa giảm xuống 1 lượt vừa chứng minh không thể nhỏ hơn.</div>
   <p>Các bài viết bởi Huy Phạm, <b>Tạ Duy Hoàng</b>, Hoa T. Vu (bài 1, 2) và <b>Tạ Duy Hoàng</b>, Hoa T. Vu (bài 3).</p>"""),
  dict(h="Danh mục trích dẫn và tài liệu đọc tiếp", body="""
   <table><tr><th>#</th><th>Trích dẫn</th><th>PDF</th></tr>
   <tr><td>[1]</td><td>H. Phạm, H. Ta, H. T. Vu. <i>Finding Decision Tree Splits in Streaming and Massively Parallel Models.</i> arXiv:2403.19867v1, 2024.</td><td><a href="../../../data/source/papers/Pham_Ta_Vu_2024_arXiv2403.19867v1.pdf" target="_blank">PDF</a></td></tr>
   <tr><td>[2]</td><td>H. Phạm, H. Ta, H. T. Vu. <i>Constructing Decision Trees from Data Streams.</i> ISIT 2025 (arXiv:2403.19867v4).</td><td><a href="../../../data/source/papers/Pham_Ta_Vu_2025_arXiv2403.19867v4.pdf" target="_blank">PDF</a></td></tr>
   <tr><td>[3]</td><td>H. Ta, H. T. Vu. <i>Nearly Optimal Bounds for Computing Decision Tree Splits in Data Streams.</i> ESA 2026 (arXiv:2604.20394v2).</td><td><a href="../../../data/source/papers/Ta_Vu_2026_arXiv2604.20394v2.pdf" target="_blank">PDF</a></td></tr>
   <tr><td>[4]</td><td>P. Domingos, G. Hulten. <i>Mining high-speed data streams.</i> KDD 2000.</td><td>trích trong [1] đến [3]</td></tr>
   <tr><td>[5]</td><td>G. Hulten, L. Spencer, P. Domingos. <i>Mining time-changing data streams.</i> KDD 2001.</td><td>trích trong [2], [3]</td></tr>
   <tr><td>[6]</td><td>G. Cormode, S. Muthukrishnan. <i>An improved data stream summary: the count-min sketch and its applications.</i> (Count-Min và truy vấn khoảng)</td><td>trích trong [2], [3]; xem module 11</td></tr>
   <tr><td>[7]</td><td>J. Dean, S. Ghemawat. <i>MapReduce: Simplified Data Processing on Large Clusters.</i> OSDI 2004 (ví dụ Distributed Sort, số vòng và shuffle)</td><td><a href="../../../data/source/papers/MapReduce_Dean2004.pdf" target="_blank">PDF</a></td></tr></table>
   <div class="callout info"><div class="lbl">Thứ tự đọc gợi ý</div>Đọc phần Introduction và Figure 1 của bài 1; rồi Algorithm 1 đến 3 của bài 2 (Mục 2); rồi Table 1 và Theorem 1 của bài 3; cuối cùng Mục 4 của bài 2 (MPC) để nối với MapReduce.
   Ôn trước các module 04, 05 (Chernoff, Hoeffding và hợp xác suất), 11 (Count-Min) và 12 (cây dyadic, rank) sẽ giúp đọc nhanh hơn nhiều.</div>"""),
 ]))


# =====================================================================================================
# Bổ sung đợt 2: bảng kết quả, Algorithm 4, 5, 6 (bài 2) và Table 1, Count-Min, Figure 2, 3 (bài 3)
# =====================================================================================================
from hd07_a import _after, _V4

_ESA = "Nguồn: Tạ, Vu, <i>Nearly Optimal Bounds for Computing Decision Tree Splits in Data Streams</i>, arXiv:2604.20394v2, "

_after(PARTS_B[0], "Bài báo 2: Constructing", dict(h="Bảng gốc kết quả streaming của bài 2 và Theorem 1: cách đọc từng hàng", body="""
   <div style="display:flex;gap:16px;align-items:flex-start;justify-content:center">""" + fig("ta_fig2_stream.png", _V4 + "Figure 2.", 200) + fig("ta_thm1.png", _V4 + "Theorem 1.", 200) + """</div>
   <p><b>Ký hiệu trong bảng:</b> R = hồi quy; C.1 = phân loại theo tỉ lệ phân loại sai; C.2 = phân loại theo Gini; CC.1 = phân loại với thuộc tính không có thứ tự. Ba cột còn lại là bộ nhớ, số lượt duyệt và mức đảm bảo.</p>
   <table><tr><th>Hàng</th><th>Đọc thành lời</th><th>Thuật toán trong bài</th></tr>
   <tr><td>R, $\\tilde O(D)$, 1 lượt, $L=\\mathrm{OPT}$</td><td>Muốn đáp án <b>đúng tuyệt đối</b> thì bộ nhớ tỉ lệ số giá trị $x$ khác nhau</td><td>Algorithm 1</td></tr>
   <tr><td>R với $M=O(1)$, $\\tilde O(1/\\varepsilon)$, 2 lượt</td><td>Chịu sai thêm $\\varepsilon$ thì bộ nhớ không còn phụ thuộc $N$ hay $m$</td><td>Algorithm 2</td></tr>
   <tr><td>R &amp; C.1, $\\tilde O(1/\\varepsilon^2\\cdot N^{\\beta})$, $O(1/\\beta)$ lượt, $(1+\\varepsilon)\\mathrm{OPT}$</td><td>Sai số <b>nhân</b> tốt hơn khi OPT nhỏ, đổi lại cần nhiều lượt; $\\beta$ là núm vặn giữa lượt và bộ nhớ</td><td>Algorithm 3 và 6</td></tr>
   <tr><td>C.2, $\\tilde O(1/\\varepsilon^2)$, 1 lượt</td><td>Gini tốn bộ nhớ gấp $1/\\varepsilon$ lần so với tỉ lệ phân loại sai</td><td>Algorithm 5</td></tr>
   <tr><td>CC.1, $\\tilde O(N/\\varepsilon)$ và $\\Omega(N)$</td><td>Thuộc tính không thứ tự thì bộ nhớ tuyến tính theo $N$ là không tránh được</td><td>Mục 3.2 của bài</td></tr></table>
   <div class="callout warn"><div class="lbl">Một chỗ cần đọc cẩn thận</div>Hàng thứ ba của bảng ghi &quot;R &amp; C.1, $\\tilde O(1/\\varepsilon)$, 1 lượt&quot;, trong khi Theorem 1 chỉ nêu thuật toán <b>2 lượt</b> cho hồi quy với sai số cộng, và bài 3 cũng ghi kết quả cũ của hồi quy là 2 lượt. Nhóm hiểu hàng này chắc chắn đúng cho C.1 (Algorithm 4); với hồi quy, kết quả 1 lượt chỉ có từ bài 3.</div>
   <p style="font-size:.9rem"><b>Sai số cộng và sai số nhân (minh hoạ):</b> nếu $\\mathrm{OPT}=0{,}001$ và $\\varepsilon=0{,}1$ thì đảm bảo cộng cho phép $L\\le0{,}101$ (lỏng), còn đảm bảo nhân buộc $L\\le0{,}0011$ (chặt). Nếu $\\mathrm{OPT}=5$ thì ngược lại: cộng cho $5{,}1$, nhân cho $5{,}5$.</p>"""))

_after(PARTS_B[0], "Phân loại bằng lấy mẫu", dict(h="Hình gốc Algorithm 4: ước lượng số đếm từ mẫu rồi chọn ngưỡng", body=two(fig("ta_alg4.png", _V4 + "Algorithm 4.", 250), """
   <p style="margin-top:0">🗣️ <b>Nói nôm na:</b> giống thăm dò trước bầu cử. Hỏi 1 trong 100 người, thấy 30 người chọn A thì đoán cả vùng có khoảng 3.000 người chọn A: lấy số đếm trong mẫu <b>chia cho tỉ lệ lấy mẫu</b>.</p>
   <p><b>Dòng 1:</b> giữ mỗi cặp với xác suất $p$.</p>
   <p><b>Dòng 2 đến 4:</b> với mỗi nhãn $l$ và mỗi khoảng $r$, đếm số điểm mẫu $k_{l,r}$ rồi đặt $\\tilde f_{l,r}=k_{l,r}/p$.</p>
   <p><b>Dòng 5:</b> thay các số đếm thật trong công thức $L(j)$ bằng số ước lượng, chọn $j$ nhỏ nhất trong các giá trị $x$ đã bốc.</p>""", "50%") + """
   <table><tr><th>Ví dụ (minh hoạ): $m=1000$, $p=0{,}1$, thử $j=40$</th><th>Đếm trong mẫu $k$</th><th>Ước lượng $k/p$</th></tr>
   <tr><td>Nhãn $+1$ bên trái</td><td>30</td><td>300</td></tr><tr><td>Nhãn $-1$ bên trái</td><td>8</td><td>80</td></tr>
   <tr><td>Nhãn $+1$ bên phải</td><td>5</td><td>50</td></tr><tr><td>Nhãn $-1$ bên phải</td><td>57</td><td>570</td></tr></table>
   <p>$\\tilde L(40)=\\frac{1}{1000}\\big(\\min\\{80,300\\}+\\min\\{50,570\\}\\big)=\\frac{130}{1000}=0{,}13$. Chỉ cần giữ 100 điểm mẫu thay vì 1000 điểm.</p>
   <div class="callout info"><div class="lbl">Khác Algorithm 2 ở đâu</div>Hồi quy cần tổng nhãn và tổng bình phương nhãn, nhạy với vài điểm có nhãn rất lớn, nên Algorithm 2 phải đếm chính xác ở lượt hai. Phân loại chỉ cần <b>đếm số điểm</b>, mà đếm thì ước lượng tốt bằng mẫu, nên một lượt là đủ.</div>"""),
  dict(h="Hình gốc Algorithm 6: cùng khung đoán và tìm nhị phân cho phân loại", body=two(fig("ta_alg6.png", _V4 + "Algorithm 6.", 420), """
   <p style="margin-top:0">Algorithm 6 có <b>cùng bộ khung</b> với Algorithm 3. Đặt hai hình cạnh nhau sẽ thấy ba chỗ khác:</p>
   <table><tr><th></th><th>Algorithm 3 (hồi quy)</th><th>Algorithm 6 (phân loại)</th></tr>
   <tr><td>Đại lượng được đoán</td><td>Tổng lỗi bình phương hai phía, tối đa $mM^2$</td><td>Số điểm phân loại sai hai phía, tối đa $m$</td></tr>
   <tr><td>Số lượt cho mỗi điểm thử</td><td>2 (tính trung bình, rồi tính lỗi)</td><td>1 (đếm bốn số $f$ là đủ)</td></tr>
   <tr><td>Điều kiện so sánh</td><td>Hai lỗi bình phương</td><td>$f_u=\\min\\{f_{-1,[1,j]},f_{+1,[1,j]}\\}$ và $f_v$ tương tự cho phía phải</td></tr></table>
   <p>Bốn nhánh if (dòng 8 đến 16) giống hệt: cả hai đạt thì ghi nhận, cả hai vượt thì đoán sai, một phía vượt thì bỏ nửa khoảng về phía đó.</p>""", "46%") + """
   <div class="callout good"><div class="lbl">Điều đáng học về cách làm nghiên cứu</div>Hai bài toán khác nhau dùng chung một khuôn vì cả hai hàm lỗi cùng có tính <b>đơn điệu</b>: thêm điểm vào một phía thì lỗi phía đó không giảm. Tìm được tính chất chung rồi thì thuật toán gần như viết lại được bằng cách thay tên đại lượng. Kết quả (Lemma 10): $O(\\log N)$ lượt, bộ nhớ $\\tilde O(1/\\varepsilon^2)$, $L(j)\\le(1+\\varepsilon)\\mathrm{OPT}$.</div>"""))

_after(PARTS_B[0], "Gini impurity", dict(h="Hình gốc Algorithm 5: hai mẫu độc lập để ước lượng một số hạng của Gini", body=two(fig("ta_alg5.png", _V4 + "Algorithm 5.", 300), """
   <p style="margin-top:0"><b>Mục tiêu:</b> ước lượng $\\dfrac{f_{+1,[1,j]}^2}{m\\,f_{[1,j]}}$ cho mọi $j$. Tách thành tích hai tỉ lệ:</p>
   <p>$\\dfrac{f_{+1,[1,j]}}{m}\\times\\dfrac{f_{+1,[1,j]}}{f_{[1,j]}}$</p>
   <p>Thừa số đầu: xác suất một điểm bất kỳ <b>vừa nằm bên trái vừa mang nhãn $+1$</b>. Thừa số sau: trong các điểm bên trái, tỉ lệ mang nhãn $+1$.</p>""", "50%") + """
   <table><tr><th>Dòng</th><th>Ý nghĩa</th></tr>
   <tr><td>2</td><td>Lấy hai mẫu $S_1,S_2$ bằng reservoir sampling, mỗi mẫu cỡ $C/\\varepsilon^2\\cdot\\log N$</td></tr>
   <tr><td>4 đến 6</td><td>$S_{2,j}$ là phần của $S_2$ nằm bên trái $j$. Nếu phần này quá ít điểm thì đặt ước lượng bằng 0 (khi đó số hạng thật cũng nhỏ hơn $\\varepsilon$)</td></tr>
   <tr><td>8</td><td>$a_i=1$ nếu điểm thứ $i$ của $S_{2,j}$ có nhãn $+1$: ước lượng thừa số sau</td></tr>
   <tr><td>9</td><td>$b_i=1$ nếu điểm thứ $i$ của $S_1$ có nhãn $+1$ và nằm bên trái: ước lượng thừa số đầu</td></tr>
   <tr><td>10, 11</td><td>$c_i=a_ib_i$, ước lượng là trung bình của $T$ giá trị $c_i$</td></tr></table>
   <p><b>Vì sao cần hai mẫu:</b> trong phần chứng minh Lemma 9, bài báo viết $\\mathbb E[c_i]=\\mathbb E[b_i]\\,\\mathbb E[a_i]$. Đẳng thức này chỉ đúng khi $a_i$ và $b_i$ <b>độc lập</b>, tức phải lấy từ hai mẫu khác nhau. Sau đó Hoeffding cho sai lệch không quá $\\varepsilon$ và hợp xác suất phủ mọi $j$.</p>
   <p><b>Ví dụ (minh hoạ):</b> $m=1000$, bên trái có 400 điểm, trong đó 300 nhãn $+1$. Giá trị thật: $300^2/(1000\\cdot400)=0{,}225$. Thừa số đầu $=0{,}3$, thừa số sau $=0{,}75$, tích $=0{,}225$, khớp.</p>"""))

# Điều nhóm từng ghi là "cần đọc Algorithm 5 để kiểm chứng" nay đã kiểm chứng
for _s in PARTS_B[0]["slides"]:
    if _s["h"].startswith("Gini impurity"):
        _old = "Bài báo không nêu câu này trong phần tóm tắt, cần đọc Algorithm 5 để kiểm chứng."
        assert _old in _s["body"]
        _s["body"] = _s["body"].replace(_old, "Nhóm đã đối chiếu với Algorithm 5 và phần chứng minh Lemma 9 (slide sau): bài báo dùng đúng đẳng thức kỳ vọng của tích hai biến độc lập.")

_after(PARTS_B[2], "Bài báo 3: Nearly Optimal", dict(h="Bảng gốc Table 1 của bài 3: cận trên và cận dưới đặt cạnh nhau", body=two(fig("ta3_table1.png", _ESA + "Table 1. [29] là bài 2.", 300), """
   <p style="margin-top:0">🗣️ <b>Nói nôm na:</b> <b>cận trên</b> là &quot;tôi làm được với chừng này bộ nhớ&quot;. <b>Cận dưới</b> là &quot;không ai làm được với ít hơn chừng này&quot;. Khi hai con số gặp nhau thì bài toán coi như đã giải xong về mặt bộ nhớ.</p>
   <p><b>Cách đọc:</b> nửa trên là thuật toán (Upper bounds), nửa dưới là giới hạn (Lower bounds). Cột Reference cho biết kết quả của bài nào: [29] là bài 2, &quot;This Paper&quot; là bài 3. Mọi dòng đều là sai số cộng $\\varepsilon$.</p>""", "46%") + """
   <table><tr><th>Mục tiêu</th><th>Trước bài 3</th><th>Bài 3</th><th>Cận dưới (bài 3)</th><th>Kết luận</th></tr>
   <tr><td>Hồi quy</td><td>2 lượt, $\\tilde O(M^2/\\varepsilon)$</td><td><b>1 lượt</b>, $\\tilde O(M^2/\\varepsilon)$</td><td>$\\Omega(M^2/\\varepsilon)$</td><td>Khớp</td></tr>
   <tr><td>Phân loại sai</td><td>1 lượt, $\\tilde O(1/\\varepsilon)$</td><td>(giữ nguyên)</td><td>$\\Omega(1/\\varepsilon)$</td><td>Khớp: thuật toán của bài 2 đã tối ưu</td></tr>
   <tr><td>Gini</td><td>1 lượt, $\\tilde O(1/\\varepsilon^2)$</td><td>1 lượt, <b>$\\tilde O(1/\\varepsilon)$</b></td><td>$\\Omega(1/\\varepsilon)$</td><td>Khớp</td></tr></table>
   <p><b>Ví dụ số (minh hoạ), $\\varepsilon=0{,}01$, $M=1$:</b> Gini trước đây cần cỡ $1/\\varepsilon^2=10\\,000$ đơn vị bộ nhớ, nay cỡ $1/\\varepsilon=100$, giảm 100 lần; và cận dưới nói không thể xuống dưới cỡ 100.</p>
   <div class="callout info"><div class="lbl">Vì sao $M^2$ xuất hiện</div>Nhãn nằm trong $[0,M]$ thì lỗi bình phương lớn cỡ $M^2$. Đổi đơn vị nhãn $y\\to y/M$ làm lỗi chia cho $M^2$, nên sai số $\\varepsilon$ trên nhãn gốc tương đương sai số $\\varepsilon/M^2$ trên nhãn đã chuẩn hoá. Bài báo dùng đúng phép co giãn này ở cả cận trên lẫn cận dưới.</div>"""))

_after(PARTS_B[2], "Thuật toán một lượt", dict(h="Định lý gốc về Count-Min với truy vấn khoảng: công cụ nền của bài 3", body=two(fig("ta3_cm.png", _ESA + "Theorem 2 (theo Cormode và Muthukrishnan).", 250), """
   <p style="margin-top:0">🗣️ <b>Nói nôm na:</b> một cuốn sổ nhỏ ghi nhanh. Hỏi &quot;tổng nhãn của các điểm có $x$ từ $l$ tới $r$ là bao nhiêu?&quot;, sổ trả lời con số <b>không bao giờ thấp hơn thật</b>, và cao hơn thật nhiều nhất $W/k$.</p>
   <p><b>Đọc định lý:</b> $f_R$ là tổng nhãn trong khoảng $R$; $W$ là tổng nhãn của cả luồng; $k$ là kích cỡ sổ. Đảm bảo: $f_R\\le\\hat f_R\\le f_R+W/k$ cho <b>mọi khoảng cùng lúc</b>, bộ nhớ $\\tilde O(k)$, cập nhật $\\tilde O(1)$.</p>""", "50%") + """
   <table><tr><th>Ví dụ (minh hoạ)</th><th>Tính</th></tr>
   <tr><td>$W=1000$, $k=100$</td><td>Mỗi câu trả lời dư tối đa $1000/100=10$</td></tr>
   <tr><td>Muốn dư tối đa 1</td><td>Cần $k=1000$: bộ nhớ tăng 10 lần</td></tr></table>
   <p><b>Bài 3 dùng ba cuốn sổ</b> cho ba luồng: $(x_i,1)$ để đếm số điểm $n_R$; $(x_i,y_i)$ để cộng nhãn $s_R$; $(x_i,y_i^2)$ để cộng bình phương nhãn $q_R$. Bài báo đặt các tham số:</p>
   <div class="pd-formula"><div class="pd-formula-math">\\tau=\\frac{\\varepsilon}{16M^2},\\qquad \\beta=\\frac{\\varepsilon}{32M^2},\\qquad K=\\Theta\\Big(\\frac{\\log N}{\\tau}\\Big)</div></div>
   <p><b>Thay số (minh hoạ), $\\varepsilon=0{,}1$, $M=1$:</b> $\\tau=1/160$, $\\beta=1/320$, cỡ sổ $k=1/\\beta=320$, cỡ mẫu reservoir $K$ cỡ $160\\log N$. Cả hai đều cỡ $M^2/\\varepsilon$ nhân hệ số log, đúng bằng cận bộ nhớ của Theorem 1.</p>
   <div class="callout warn"><div class="lbl">Vì sao mẫu số được cộng thêm $\\beta m$</div>Sổ chỉ <b>ước lượng dư</b>, không bao giờ thiếu. Trong $\\mathrm{SSE}=q-s^2/n$, một $\\hat n$ gần 0 có thể làm phép chia nhảy vọt; cộng $\\beta m$ vào mẫu số giữ cho phép chia ổn định với cái giá là một sai lệch nhỏ đã được tính trong $\\varepsilon$.</div>"""))

_after(PARTS_B[2], "Cận dưới: quy dẫn", dict(h="Hình gốc Figure 2 của bài 3: dựng luồng cho cận dưới hồi quy", body=fig("ta3_fig2.png", _ESA + "Figure 2.", 270) + """
   <p><b>Cách đọc hình</b> (trường hợp $n=4$, dãy bit của Alice $z=(0,1,1,0)$, Bob hỏi bit thứ $i=2$):</p>
   <ul style="margin:0 0 8px;padding-left:20px;line-height:1.5">
   <li><b>Ô xanh phía trên (Alice):</b> tại $x=2,4,6,8$ có $B$ điểm với nhãn lần lượt là $z_1,z_2,z_3,z_4=0,1,1,0$. Đây là cách Alice &quot;giấu&quot; dãy bit vào luồng.</li>
   <li><b>Ô đỏ phía dưới (Bob):</b> $T$ điểm nhãn 0 tại $x=2i-1=3$ và $T$ điểm nhãn 1 tại $x=2i+1=5$. Hai khối &quot;mỏ neo&quot; này rất nặng và kẹp hai bên khối $x=4$.</li>
   <li><b>Hai vạch đứt:</b> $j^-=3$ đẩy khối $x=4$ sang <b>phải</b>; $j^+=4$ giữ khối $x=4$ ở bên <b>trái</b>.</li></ul>
   <p><b>Ý tưởng:</b> bên trái vạch gần như toàn nhãn 0, bên phải gần như toàn nhãn 1. Khối $x=4$ mang nhãn $z_2$ nên xếp cùng phía với mỏ neo giống nhãn thì lỗi nhỏ hơn. Vậy <b>thuật toán chọn $j^-$ khi $z_i=1$, chọn $j^+$ khi $z_i=0$</b>: nhìn đáp án là đọc được bit.</p>
   <table><tr><th>Tham số trong bài</th><th>Với $n=4$</th><th>Nhóm tự tính (kiểm tra)</th></tr>
   <tr><td>$B=n$, $T=100n^2$, $N=2n+1$, $m=201n^2$</td><td>$B=4$, $T=1600$, $N=9$, $m=3216$</td><td>$L(j^-)=3{,}99/3216\\approx0{,}00124$; $L(j^+)=7{,}98/3216\\approx0{,}00248$</td></tr>
   <tr><td>Claim 14: mọi $j$ khác có $L\\ge50/201$</td><td>$\\approx0{,}249$</td><td>Vì hai mỏ neo rơi cùng một phía, mỗi mỏ neo lệch trung bình $1/2$</td></tr>
   <tr><td>Claim 15: $L(j^\\pm)\\le1/201$</td><td>$\\approx0{,}00498$</td><td>Hai giá trị ở trên đều nhỏ hơn, khớp</td></tr>
   <tr><td>Khoảng cách $|L(j^+)-L(j^-)|>1/(804n)$</td><td>$\\approx0{,}00031$</td><td>Thực tế $0{,}00124$, khớp; và $j^-$ tốt hơn vì $z_2=1$</td></tr></table>
   <div class="callout good"><div class="lbl">Từ hình tới cận dưới</div>Đặt $n=\\lfloor1/(1000\\varepsilon')\\rfloor$ thì khoảng cách giữa hai ngưỡng lớn hơn $\\varepsilon'$, nên thuật toán sai số $\\varepsilon'$ buộc phải chọn đúng. Bộ nhớ sau khi đọc phần của Alice chính là tin nhắn gửi Bob, mà Index cần $\\Omega(n)$ bit, tức $\\Omega(1/\\varepsilon')=\\Omega(M^2/\\varepsilon)$.</div>"""),
  dict(h="Hình gốc Figure 3 của bài 3: cùng khuôn mẫu cho phân loại", body=fig("ta3_fig3.png", _ESA + "Figure 3.", 240) + """
   <p><b>Cách đọc hình:</b> giống Figure 2 nhưng nhãn là $\\pm1$. Bob đặt $T$ điểm nhãn $-1$ tại $x=2i-1$ và $T$ điểm nhãn $+1$ tại $x=2i+1$. Alice đặt khối $G$ gồm $B$ điểm tại $x=2i$ với nhãn $s_i=+1$ nếu $z_i=1$, ngược lại $-1$. Hai ngưỡng cạnh tranh vẫn là $j^-=2i-1$ và $j^+=2i$.</p>
   <table><tr><th></th><th>Hồi quy (Figure 2)</th><th>Phân loại sai (Figure 3)</th></tr>
   <tr><td>Tham số</td><td>$n=\\lfloor1/(1000\\varepsilon')\\rfloor$, $T=100n^2$, $m=201n^2$</td><td>$n=\\lfloor1/(100\\varepsilon)\\rfloor$, $T=4n^2$, $m=9n^2$</td></tr>
   <tr><td>Ngưỡng khác $j^\\pm$</td><td>$L\\ge50/201$</td><td>$L\\ge4/9$ (Claim 17)</td></tr>
   <tr><td>Cách tính khoảng cách</td><td>Bậc hai: dùng công thức SSE khi thêm một khối</td><td>Đếm trực tiếp đa số và thiểu số</td></tr>
   <tr><td>Cận dưới</td><td>$\\Omega(M^2/\\varepsilon)$</td><td>$\\Omega(1/\\varepsilon)$ (Theorem 16)</td></tr></table>
   <p><b>Nhóm tự tính với $n=4$, $z=(0,1,1,0)$, $i=2$:</b> $B=4$, $T=64$, $m=144$. Với $j^-=3$: bên trái toàn nhãn $-1$ (sai 0), bên phải có 72 nhãn $+1$ và 4 nhãn $-1$ (sai 4), nên $L=4/144$. Với $j^+=4$: bên trái có 68 nhãn $-1$ và 4 nhãn $+1$ (sai 4), bên phải sai 4, nên $L=8/144$. Ngưỡng $j^-$ tốt hơn, đúng với $z_2=1$; khoảng cách là $B/m=1/(9n)$.</p>
   <div class="callout info"><div class="lbl">Một khuôn, ba kết quả</div>Bài báo nêu rõ các cận dưới cùng theo một khuôn: dựng luồng có hai ngưỡng liền kề cạnh tranh mà ngưỡng thắng tiết lộ bit ẩn. Chỗ khác nhau chỉ là phép tính khoảng cách cho từng hàm lỗi. Gini thì suy ra từ hồi quy nhờ $L_{\\mathrm{Gini}}=2L_{\\mathrm{MSE}}$.</div>"""))

QUIZ_EXTRA = [
 dict(q="Đếm lại trên Figure 1 (hình hồi quy) của bài báo, hai đường chấm ngang ứng với hai giá trị dự đoán nào ở hai phía ngưỡng j = 4?",
  opts=["Trung bình 7 bên trái, 2 bên phải", "Trung vị 8 bên trái, 1 bên phải", "Giá trị lớn nhất 8 và nhỏ nhất 1", "Tổng 49 bên trái, 14 bên phải"],
  correct=0, explain="Bên trái 7 điểm có tổng 49, trung bình 7; bên phải 7 điểm có tổng 14, trung bình 2. Trung bình là hằng số làm tổng bình phương sai lệch nhỏ nhất."),
 dict(q="Algorithm 2 trên ví dụ 8 điểm (N = 8): nếu lượt một bốc được hai giá trị 4 và 7 thì tập ứng viên S là gì?",
  opts=["{4, 7}", "{0, 4, 7, 8}", "{0, 3, 4, 6, 7, 8}", "{3, 4, 5, 6, 7, 8}"],
  correct=2, explain="S gồm giá trị được bốc, giá trị đứng ngay trước nó, cùng 0 và N: {0, 3, 4, 6, 7, 8}. Trong đó L(4) = 0,5 nhỏ nhất."),
 dict(q="Trong Algorithm 3, tại điểm thử j chỉ có lỗi phía trái vượt mức đoán. Thuật toán làm gì tiếp?",
  opts=["Ghi nhận j là khả thi", "Bỏ cặp đoán hiện tại", "Đặt cận trái thành j + 1", "Đặt cận phải thành j − 1"],
  correct=3, explain="Dời ngưỡng sang phải chỉ làm lỗi phía trái tăng thêm, nên mọi ngưỡng lớn hơn j cũng vượt: tìm tiếp bên trái, tức j_r = j − 1."),
 dict(q="Theo định lý Count-Min với truy vấn khoảng, nếu tổng nhãn cả luồng W = 1000 và cỡ sketch k = 100 thì ước lượng của một khoảng lệch thế nào?",
  opts=["Thấp hơn thật tối đa 10", "Cao hơn thật tối đa 10", "Lệch hai phía tối đa 100", "Luôn đúng tuyệt đối"],
  correct=1, explain="Đảm bảo là f_R ≤ ước lượng ≤ f_R + W/k: không bao giờ thiếu, dư tối đa 1000/100 = 10."),
 dict(q="Trong cách dựng cận dưới hồi quy (Figure 2 của bài 3) với n = 4, độ dài luồng m = 201n² bằng bao nhiêu, và thuật toán chọn ngưỡng nào khi bit được hỏi bằng 1?",
  opts=["m = 804; chọn j+ = 2i", "m = 3216; chọn j+ = 2i", "m = 3216; chọn j− = 2i − 1", "m = 804; chọn j− = 2i − 1"],
  correct=2, explain="m = 201 × 16 = 3216. Khi bit bằng 1, khối của Alice tại x = 2i cùng nhãn với mỏ neo bên phải, nên đẩy nó sang phải (j−) cho lỗi nhỏ hơn."),
 dict(q="Vì sao Algorithm 5 (ước lượng số hạng của Gini) cần hai tập mẫu độc lập S1 và S2?",
  opts=["Để tích hai chỉ báo có kỳ vọng bằng tích hai kỳ vọng", "Để giảm một nửa thời gian cập nhật", "Để một mẫu dùng cho hồi quy, một mẫu cho phân loại", "Để phòng khi một mẫu bị mất do lỗi máy"],
  correct=0, explain="Số hạng f²/(m·f) tách thành tích hai tỉ lệ; lấy a_i từ S2 và b_i từ S1 độc lập thì E[a_i·b_i] = E[a_i]·E[b_i], rồi áp dụng Hoeffding."),
]
