# -*- coding: utf-8 -*-
"""Nội dung lý thuyết + quiz cho 14 module. Lý thuyết dựa trên kiến thức chuẩn xác suất/thuật toán
(Markov, Chebyshev, Chernoff, Hoeffding... là kết quả toán học kinh điển, không cần trích trang cụ thể).
Case study dựa trên các thuật toán đã đọc trực tiếp từ slide gốc (Morris, FM, KMV, q-digest, MRL, KLL,
CountMin, CountSketch, AGM, SupportFind, AMS) trong quá trình soạn bộ bài tập trước đó — không suy đoán."""

MODULES = [
# ---------------------------------------------------------------- 1
dict(n=1, slug="01-ky-vong", title="Biến ngẫu nhiên, kỳ vọng, tuyến tính kỳ vọng",
 tag="Xác suất cơ bản",
 intro="Nền tảng của mọi thuật toán streaming: mọi ước lượng đều bắt đầu từ một biến ngẫu nhiên và kỳ vọng của nó.",
 parts=[
  dict(title="Biến ngẫu nhiên & kỳ vọng", bullets=[
     "Không gian mẫu, biến ngẫu nhiên rời rạc", "Kỳ vọng là gì, tại sao cần nó",
     "Tuyến tính của kỳ vọng — công cụ mạnh nhất"],
   slides=[
    dict(h="Biến ngẫu nhiên là gì?", body="""
      <p>Một <b>biến ngẫu nhiên</b> $X$ là một hàm gán mỗi kết quả trong không gian mẫu $\\Omega$ với một số thực.
      Trong streaming, $X$ thường là một đại lượng ta <i>đo được sau khi xử lý</i> một luồng dữ liệu — ví dụ
      số phần tử phân biệt, hoặc giá trị của một bộ đếm ngẫu nhiên hoá.</p>
      <div class="pd-formula"><div class="pd-formula-label">Kỳ vọng (rời rạc)</div>
      <div class="pd-formula-math">$\\displaystyle \\mathbb E[X] = \\sum_{j} j \\cdot \\mathbb P(X=j)$</div></div>
      <ul class="pd-legend"><li><b>$\\mathbb E[X]$</b><span>giá trị trung bình "kỳ vọng" của $X$ qua vô số lần lặp</span></li>
      <li><b>$\\mathbb P(X=j)$</b><span>xác suất $X$ nhận đúng giá trị $j$</span></li></ul>"""),
    dict(h="Tuyến tính của kỳ vọng", body="""
      <p>Tính chất quan trọng nhất: <b>luôn đúng</b>, kể cả khi các biến ngẫu nhiên <i>không độc lập</i>.
      Đây là lý do vì sao hầu hết chứng minh streaming bắt đầu bằng cách viết đại lượng cần tính thành
      tổng các biến chỉ báo rồi áp linearity.</p>
      <div class="pd-formula"><div class="pd-formula-label">Tuyến tính của kỳ vọng</div>
      <div class="pd-formula-math">$\\mathbb E[X+Y] = \\mathbb E[X] + \\mathbb E[Y]$</div></div>
      <div class="callout good"><div class="lbl">Mẹo dùng thường xuyên</div>
      Muốn tính $\\mathbb E$ của "số phần tử thoả điều kiện gì đó" trong luồng? Viết nó thành
      $\\sum_i \\mathbf 1[\\text{điều kiện tại } i]$ rồi lấy $\\mathbb E$ từng số hạng — không cần độc lập.</div>""")]),
  dict(title="Case study: thuật toán Morris", bullets=[
    "Bài toán đếm xấp xỉ trong $O(\\log\\log n)$ bit",
    "Ý tưởng: tăng bộ đếm $X$ theo xác suất $1/2^X$",
    "$\\tilde n = 2^X - 1$ là ước lượng không chệch"],
   slides=[
    dict(h="Bài toán đếm xấp xỉ (Morris, 1978)", body="""
      <p>Đếm chính xác $n$ sự kiện cần $\\Theta(\\log n)$ bit (một bộ đếm nhị phân thường). Morris đưa ra
      thuật toán chỉ cần $O(\\log\\log n)$ bit bằng cách <b>không tăng bộ đếm mỗi lần</b>, mà tăng theo xác suất
      giảm dần.</p>
      <div class="pd-formula"><div class="pd-formula-label">Thuật toán Morris</div>
      <div class="pd-formula-math">Khởi tạo $X=0$. Mỗi <code>update()</code>: tăng $X$ thêm 1 với xác suất $1/2^X$.
      Truy vấn: trả về $\\tilde n = 2^X - 1$.</div></div>"""),
    dict(h="Vì sao không chệch?", body="""
      <p>Đây chính là case study cho <b>tuyến tính kỳ vọng + quy nạp</b> (sẽ gặp lại ở buổi 6): có thể chứng minh
      bằng quy nạp rằng $\\mathbb E[2^{X_n}] = n+1$ sau $n$ lần cập nhật, tức $\\tilde n = 2^{X_n}-1$ là một
      <b>ước lượng không chệch</b> của $n$ — nền tảng để mọi phân tích phương sai/xác suất lỗi phía sau dựa vào.</p>
      <div class="callout warn"><div class="lbl">Bẫy hay gặp</div>
      Không chệch (unbiased) KHÔNG có nghĩa là chính xác ở mỗi lần chạy — chỉ có nghĩa đúng <i>trung bình</i>
      qua nhiều lần chạy độc lập. Cần thêm Chebyshev (buổi 3) mới kiểm soát được độ lệch thực tế.</div>""")]),
 ],
 quiz=[
  dict(q="Tuyến tính của kỳ vọng $\\mathbb E[X+Y]=\\mathbb E[X]+\\mathbb E[Y]$ đòi hỏi điều kiện gì?",
   opts=["$X,Y$ phải độc lập","Không cần điều kiện gì, luôn đúng","$X,Y$ phải cùng phân phối","$X,Y$ phải rời rạc"],
   correct=1, explain="Đây chính là sức mạnh của linearity: đúng vô điều kiện, kể cả khi X,Y phụ thuộc nhau."),
  dict(q="Trong thuật toán Morris, bộ đếm $X$ tăng thêm 1 với xác suất nào?",
   opts=["$1/2$ cố định","$1/2^X$","$1/n$","$X/n$"], correct=1,
   explain="Xác suất tăng giảm dần theo hàm mũ khi X lớn, giúp bộ đếm chỉ cần lưu O(log log n) bit."),
  dict(q="Ước lượng $\\tilde n = 2^{X_n}-1$ của Morris có tính chất gì đã chứng minh được bằng quy nạp?",
   opts=["Luôn chính xác tuyệt đối","Không chệch: $\\mathbb E[\\tilde n]=n$","Luôn nhỏ hơn n","Không phụ thuộc n"],
   correct=1, explain="$\\mathbb E[2^{X_n}]=n+1 \\Rightarrow \\mathbb E[\\tilde n]=n$: không chệch, không phải chính xác từng lần."),
  dict(q="Công thức $\\mathbb E[X]=\\sum_j j\\cdot\\mathbb P(X=j)$ áp dụng cho loại biến ngẫu nhiên nào?",
   opts=["Chỉ liên tục","Chỉ nhị phân","Rời rạc","Chỉ không âm"], correct=2,
   explain="Đây là công thức kỳ vọng chuẩn cho biến ngẫu nhiên rời rạc."),
  dict(q="Viết 'số phần tử thoả điều kiện' thành tổng các biến chỉ báo rồi lấy kỳ vọng từng số hạng — kỹ thuật này tên là gì?",
   opts=["Phương pháp Monte Carlo","Áp dụng tuyến tính kỳ vọng","Quy nạp mạnh","Bất đẳng thức Markov"], correct=1,
   explain="Đây chính là kỹ thuật đếm bằng chỉ báo + linearity of expectation, dùng lặp lại xuyên suốt môn."),
 ]),

# ---------------------------------------------------------------- 2
dict(n=2, slug="02-markov", title="Phương sai, độc lập, bất đẳng thức Markov",
 tag="Bất đẳng thức tập trung",
 intro="Công cụ đầu tiên để biến 'không chệch' thành 'đáng tin cậy': chặn xác suất một biến ngẫu nhiên lệch quá xa.",
 parts=[
  dict(title="Phương sai & độc lập", bullets=["Phương sai đo độ phân tán", "Độc lập giữa 2 biến ngẫu nhiên",
    "Var cộng được khi độc lập"], slides=[
   dict(h="Phương sai", body="""
     <p>Phương sai đo mức độ $X$ "dao động" quanh kỳ vọng của nó — càng nhỏ, ước lượng càng đáng tin cậy.</p>
     <div class="pd-formula"><div class="pd-formula-label">Phương sai</div>
     <div class="pd-formula-math">$\\mathrm{Var}[X] = \\mathbb E[X^2] - (\\mathbb E[X])^2$</div></div>
     <div class="callout good"><div class="lbl">Vì sao Var cộng được khi độc lập</div>
     $\\mathrm{Var}[X+Y]=\\mathrm{Var}[X]+\\mathrm{Var}[Y]$ khi $X,Y$ độc lập — đây là lý do "chạy nhiều bản sao
     độc lập rồi lấy trung bình" luôn làm giảm phương sai (buổi 3 sẽ dùng liên tục).</div>"""),
   dict(h="Bất đẳng thức Markov", body="""
     <p>Công cụ đơn giản nhất nhưng là nền của mọi bất đẳng thức tập trung khác (Chebyshev, Chernoff đều
     suy ra từ Markov áp cho một biến biến đổi khéo léo).</p>
     <div class="pd-formula"><div class="pd-formula-label">Markov (X ≥ 0)</div>
     <div class="pd-formula-math">$\\displaystyle \\mathbb P(X > \\lambda) < \\frac{\\mathbb E[X]}{\\lambda}$</div></div>
     <div class="callout warn"><div class="lbl">Bẫy</div>Markov chỉ dùng được cho $X \\ge 0$, và thường cho chặn
     rất lỏng khi $X$ tập trung quanh kỳ vọng — cần Chebyshev để chặt hơn.</div>""")]),
  dict(title="Case study: phân tích Morris cơ bản", bullets=["Var[2^{X_n}] tính được bằng quy nạp",
    "Chebyshev áp cho Morris cho sai số $O(1/\\varepsilon^2)$", "Vì sao 1 bản sao Morris chưa đủ tin cậy"],
   slides=[dict(h="Markov không đủ mạnh cho Morris", body="""
     <p>Nếu chỉ dùng Markov trực tiếp trên $|\\tilde n - n|$, chặn thu được quá lỏng để hữu ích thực tế —
     đây chính là động lực lịch sử để chuyển sang Chebyshev (buổi 3), phân tích qua $\\mathrm{Var}[2^{X_n}]$
     thay vì Markov đơn thuần.</p>
     <div class="callout info"><div class="lbl">Liên hệ</div>Đây là mẫu hình lặp lại toàn môn: Markov cho biến
     bậc 1 → Chebyshev cho biến bậc 2 (cần biết Var) → Chernoff/Hoeffding cho hàm mũ (cần độc lập nhiều biến).</div>""")]),
 ],
 quiz=[
  dict(q="$\\mathrm{Var}[X]=\\mathbb E[X^2]-(\\mathbb E[X])^2$ — biểu thức này luôn có giá trị gì?",
   opts=["Có thể âm","Luôn không âm","Luôn bằng 0","Luôn bằng $\\mathbb E[X]$"], correct=1,
   explain="Phương sai là kỳ vọng của bình phương độ lệch, luôn ≥ 0."),
  dict(q="Bất đẳng thức Markov áp dụng được cho biến ngẫu nhiên nào?",
   opts=["Chỉ biến rời rạc","Chỉ biến có phân phối chuẩn","Biến $X\\ge 0$ bất kỳ","Chỉ biến có Var hữu hạn"],
   correct=2, explain="Markov chỉ cần X không âm và có kỳ vọng hữu hạn, không cần thêm điều kiện gì khác."),
  dict(q="$\\mathrm{Var}[X+Y]=\\mathrm{Var}[X]+\\mathrm{Var}[Y]$ đòi hỏi điều kiện gì?",
   opts=["X,Y độc lập","X,Y bằng nhau","Không cần điều kiện","X,Y đều dương"], correct=0,
   explain="Khác với kỳ vọng, cộng được phương sai CẦN tính độc lập (hoặc ít nhất pairwise independence)."),
  dict(q="Vì sao Markov thường cho chặn 'lỏng' trong thực tế?",
   opts=["Vì chỉ dùng thông tin kỳ vọng, bỏ qua độ phân tán","Vì công thức sai","Vì chỉ áp dụng được cho n nhỏ","Vì không tổng quát"],
   correct=0, explain="Markov chỉ dùng E[X], không biết gì về Var[X] nên không tận dụng được thông tin 'X tập trung' nếu có."),
  dict(q="Trong phân tích Morris, việc chuyển từ Markov sang Chebyshev nhằm mục đích gì?",
   opts=["Giảm bộ nhớ thuật toán","Có chặn xác suất chặt hơn nhờ dùng thêm thông tin Var","Làm thuật toán chạy nhanh hơn","Không có mục đích gì khác"],
   correct=1, explain="Chebyshev tận dụng thêm Var[2^{X_n}] đã tính được, cho chặn chặt hơn Markov đơn thuần."),
 ]),

# ---------------------------------------------------------------- 3
dict(n=3, slug="03-chebyshev", title="Bất đẳng thức Chebyshev",
 tag="Bất đẳng thức tập trung",
 intro="Nâng cấp Markov bằng cách áp dụng cho $(X-\\mathbb E X)^2$ — công cụ chuẩn để phân tích 'lấy trung bình nhiều mẫu'.",
 parts=[
  dict(title="Chebyshev & khuôn mẫu trung bình hoá", bullets=["Chebyshev suy ra từ Markov thế nào",
    "Lấy trung bình $s$ bản sao giảm phương sai $s$ lần", "Khuôn mẫu 'trung vị của trung bình'"],
   slides=[dict(h="Bất đẳng thức Chebyshev", body="""
     <div class="pd-formula"><div class="pd-formula-label">Chebyshev</div>
     <div class="pd-formula-math">$\\displaystyle \\mathbb P(|X-\\mathbb E X| > \\lambda) < \\frac{\\mathrm{Var}[X]}{\\lambda^2}$</div></div>
     <p>Chứng minh: áp Markov cho biến không âm $(X-\\mathbb E X)^2$ với ngưỡng $\\lambda^2$. Đây là ví dụ kinh điển
     của kỹ thuật "biến đổi biến rồi áp Markov" sẽ lặp lại ở Chernoff (buổi 4).</p>"""),
   dict(h="Lấy trung bình s bản sao", body="""
     <p>Nếu chạy $s$ bản sao độc lập của một ước lượng không chệch có phương sai $V$, và lấy trung bình:</p>
     <div class="pd-formula"><div class="pd-formula-label">Giảm phương sai qua trung bình</div>
     <div class="pd-formula-math">$\\mathrm{Var}\\Big[\\tfrac1s\\sum_{i=1}^s X_i\\Big] = \\dfrac{V}{s}$</div></div>
     <div class="callout good"><div class="lbl">Khuôn mẫu xuyên suốt môn</div>
     Thiết kế ước lượng không chệch → lấy trung bình $s=\\Theta(1/\\varepsilon^2\\delta)$ bản sao để Chebyshev
     cho sai số $\\varepsilon$ với xác suất $1-\\delta$. Vấn đề: $s$ tỉ lệ nghịch với $\\delta$ — rất tốn khi cần
     $\\delta$ nhỏ. Buổi 4-5 sẽ khắc phục bằng "trung vị của trung bình".</div>""")]),
  dict(title="Case study: KMV cho bài toán $F_0$", bullets=["Giữ k giá trị băm nhỏ nhất thay vì chỉ 1",
    "Phương sai giảm mạnh khi k tăng", "Chebyshev cho sai số $(1\\pm\\varepsilon)$ với $k=\\Theta(1/\\varepsilon^2)$"],
   slides=[dict(h="KMV — k Minimum Values", body="""
     <p>Bài toán đếm phần tử phân biệt ($F_0$): băm mỗi phần tử vào $[0,1]$, giữ lại $k$ giá trị băm nhỏ nhất
     đã gặp. Nếu $X$ là giá trị nhỏ thứ $k$, ước lượng $\\tilde t = kM/X$ (M là hệ số rời rạc hoá).</p>
     <div class="callout info"><div class="lbl">Vì sao giữ k giá trị thay vì 1</div>
     Thuật toán FM lý tưởng hoá (buổi 7) chỉ giữ giá trị nhỏ nhất — phương sai lớn, dễ bị 1 phần tử "may mắn"
     làm lệch. KMV dùng thống kê thứ tự thứ $k$ (trung vị hoá tự nhiên) → theo Chebyshev, chọn
     $k=\\Theta(1/\\varepsilon^2)$ đạt sai số $(1\\pm\\varepsilon)$ với xác suất hằng số.</div>""")]),
 ],
 quiz=[
  dict(q="Chebyshev được chứng minh bằng cách áp Markov cho biến nào?",
   opts=["$X$", "$(X-\\mathbb E X)^2$", "$e^{tX}$", "$1/X$"], correct=1,
   explain="Áp Markov cho bình phương độ lệch rồi khai căn ra dạng Chebyshev quen thuộc."),
  dict(q="Lấy trung bình $s$ bản sao độc lập của ước lượng có phương sai $V$ cho phương sai mới là bao nhiêu?",
   opts=["$V$", "$V/s$", "$V \\cdot s$", "$V/s^2$"], correct=1,
   explain="Var của trung bình s biến độc lập cùng phương sai V là V/s."),
  dict(q="Trong KMV, tại sao giữ $k$ giá trị băm nhỏ nhất thay vì chỉ 1?",
   opts=["Để tiết kiệm bộ nhớ hơn","Để giảm phương sai của ước lượng","Để tránh dùng hàm băm","Không có lý do đặc biệt"],
   correct=1, explain="Thống kê thứ tự thứ k ổn định hơn nhiều so với chỉ dùng giá trị nhỏ nhất (k=1)."),
  dict(q="Nhược điểm chính của việc chỉ dùng Chebyshev + lấy trung bình để đạt xác suất lỗi $\\delta$ rất nhỏ là gì?",
   opts=["Không đạt được độ chính xác nào","Số bản sao cần thiết tỉ lệ $1/\\delta$, rất tốn khi $\\delta$ nhỏ","Chebyshev không dùng được cho ước lượng không chệch","Phương sai sẽ tăng theo $s$"],
   correct=1, explain="Đây là động lực cho kỹ thuật median trick (Chernoff/Hoeffding, buổi 4-5) chỉ cần $s=\\Theta(\\log(1/\\delta))$."),
  dict(q="Với KMV, chọn $k=\\Theta(1/\\varepsilon^2)$ để đạt điều gì?",
   opts=["Sai số $(1\\pm\\varepsilon)$ với xác suất hằng số","Sai số bằng 0 tuyệt đối","Bộ nhớ $O(1)$","Không phụ thuộc $\\varepsilon$"],
   correct=0, explain="Đây chính là ứng dụng trực tiếp của Chebyshev: k càng lớn, phương sai càng nhỏ, càng gần đúng."),
 ]),

# ---------------------------------------------------------------- 4
dict(n=4, slug="04-chernoff", title="Bất đẳng thức Chernoff",
 tag="Bất đẳng thức tập trung",
 intro="Chặn dạng hàm mũ — mạnh hơn Chebyshev rất nhiều khi cần xác suất lỗi cực nhỏ.",
 parts=[
  dict(title="Chernoff bound", bullets=["Ý tưởng: áp Markov cho $e^{tX}$", "Chặn giảm theo hàm mũ theo $\\lambda^2$",
   "So sánh với Chebyshev ($1/\\lambda^2$)"], slides=[
   dict(h="Kỹ thuật MGF", body="""
     <p>Thay vì áp Markov trực tiếp cho $X$, áp cho $e^{tX}$ với $t>0$ tối ưu — chặn thu được giảm theo
     <b>hàm mũ</b> theo độ lệch, mạnh hơn hẳn Chebyshev (chỉ giảm theo $1/\\lambda^2$).</p>
     <div class="pd-formula"><div class="pd-formula-label">Chernoff (2 phía, $X=\\sum X_i$, $X_i\\in[0,1]$ độc lập)</div>
     <div class="pd-formula-math">$\\mathbb P(|X-\\mu|>\\lambda\\mu) < 2e^{-\\lambda^2\\mu/3}$</div></div>"""),
   dict(h="Median trick", body="""
     <p>Vì Chernoff/Hoeffding cho chặn hàm mũ theo <i>số bản sao</i> $t$, chỉ cần $t=\\Theta(\\log(1/\\delta))$
     bản sao (mỗi bản sao đúng với xác suất $\\ge 2/3$) rồi lấy <b>trung vị</b> để đạt xác suất lỗi $\\delta$
     tuỳ ý — rẻ hơn rất nhiều so với $\\Theta(1/\\delta)$ của Chebyshev thuần.</p>
     <div class="callout good"><div class="lbl">Khuôn mẫu hoàn chỉnh</div>
     Không chệch → Chebyshev (trung bình $s=O(1/\\varepsilon^2)$ bản sao, lỗi $\\le 1/3$) → Chernoff/Hoeffding
     (lặp $t=O(\\log 1/\\delta)$ lần, lấy trung vị) = "Morris++", "FM++"...</div>""")]),
  dict(title="Case study: Morris++ / FM++", bullets=["Morris+ = trung bình s bản sao Morris",
    "Morris++ = trung vị của t bản sao Morris+", "Không gian tổng: $O(\\varepsilon^{-2}\\log(1/\\delta))$"],
   slides=[dict(h="Từ Morris đến Morris++", body="""
     <p><b>Morris+</b>: chạy $s=\\Theta(1/\\varepsilon^2)$ bản sao Morris độc lập, lấy trung bình → Chebyshev
     cho xác suất lỗi $\\le 1/3$ với sai số $\\varepsilon$. <b>Morris++</b>: chạy $t=\\Theta(\\log(1/\\delta))$
     bản sao Morris+ độc lập, lấy <b>trung vị</b> → Hoeffding cho xác suất lỗi $\\delta$ tuỳ ý.</p>
     <div class="callout warn"><div class="lbl">Bẫy</div>Nhầm lẫn phổ biến: tưởng cần tăng $s$ (không phải $t$)
     để giảm $\\delta$ — sẽ tốn $\\Theta(1/\\delta)$ thay vì $\\Theta(\\log 1/\\delta)$. Luôn tách 2 tham số:
     $\\varepsilon$ (độ chính xác, do $s$ quyết định) và $\\delta$ (độ tin cậy, do $t$ quyết định).</div>""")]),
 ],
 quiz=[
  dict(q="Ý tưởng cốt lõi của chứng minh Chernoff là gì?",
   opts=["Áp Markov trực tiếp cho X","Áp Markov cho $e^{tX}$ với t tối ưu","Dùng Chebyshev hai lần","Tính chính xác phân phối của X"],
   correct=1, explain="Đây là kỹ thuật hàm sinh moment (MGF), nguồn gốc của chặn dạng hàm mũ."),
  dict(q="Chặn Chernoff giảm theo tốc độ nào khi độ lệch $\\lambda$ tăng?",
   opts=["Tuyến tính", "$1/\\lambda^2$ như Chebyshev", "Hàm mũ $e^{-\\Omega(\\lambda^2\\mu)}$", "Không đổi"],
   correct=2, explain="Đây chính là ưu điểm vượt trội của Chernoff so với Chebyshev khi cần xác suất lỗi rất nhỏ."),
  dict(q="Trong 'median trick', vai trò của tham số $t$ (số bản sao lặp lại) là gì?",
   opts=["Quyết định độ chính xác $\\varepsilon$","Quyết định xác suất tin cậy $1-\\delta$","Không có vai trò gì","Quyết định bộ nhớ mỗi bản sao"],
   correct=1, explain="t (số lần lặp lấy trung vị) điều khiển delta; s (số bản sao lấy trung bình) điều khiển epsilon — hai tham số tách biệt."),
  dict(q="Vì sao chỉ cần $t=\\Theta(\\log(1/\\delta))$ thay vì $\\Theta(1/\\delta)$ để đạt xác suất lỗi $\\delta$?",
   opts=["Vì median trick dùng Chernoff/Hoeffding (chặn hàm mũ) cho biến chỉ báo 'bản sao đúng/sai'","Vì Morris tự động chính xác","Vì không cần trung vị nữa","Đây là một sai lầm, thực ra vẫn cần 1/δ"],
   correct=0, explain="Chặn xác suất 'đa số t bản sao sai' giảm theo hàm mũ theo t nhờ Hoeffding, nên t chỉ cần log(1/δ)."),
  dict(q="Morris++ kết hợp đúng thứ tự nào?",
   opts=["Trung vị trước, trung bình sau","Trung bình s bản sao (Morris+), rồi trung vị t bản sao Morris+ (Morris++)","Chỉ cần trung bình, không cần trung vị","Chỉ cần trung vị, không cần trung bình"],
   correct=1, explain="Đúng thứ tự 2 tầng: trung bình để giảm phương sai (Chebyshev), trung vị để giảm xác suất lỗi (Chernoff/Hoeffding)."),
 ]),

# ---------------------------------------------------------------- 5
dict(n=5, slug="05-hoeffding-union", title="Bất đẳng thức Hoeffding & Union bound",
 tag="Bất đẳng thức tập trung",
 intro="Hoeffding tổng quát hoá Chernoff cho biến bị chặn bất kỳ; union bound gộp nhiều sự kiện lỗi lại thành một.",
 parts=[
  dict(title="Hoeffding & Union bound", bullets=["Hoeffding: không cần Bernoulli, chỉ cần bị chặn khoảng",
   "Union bound: $\\mathbb P(\\cup A_i)\\le\\sum\\mathbb P(A_i)$", "Chia đều ngân sách lỗi $\\delta/n$"],
   slides=[dict(h="Bất đẳng thức Hoeffding", body="""
     <div class="pd-formula"><div class="pd-formula-label">Hoeffding ($X_i$ i.i.d. Bernoulli(p))</div>
     <div class="pd-formula-math">$\\mathbb P\\Big(\\sum X_i > (p+\\varepsilon)n\\Big) < e^{-2\\varepsilon^2 n}$</div></div>
     <p>Tổng quát hơn Chernoff: không đòi hỏi phân phối Bernoulli cụ thể, chỉ cần mỗi $X_i$ bị chặn trong
     một khoảng $[a_i,b_i]$ — dùng được cho hầu hết mọi ước lượng streaming.</p>"""),
   dict(h="Union bound", body="""
     <div class="pd-formula"><div class="pd-formula-label">Union bound</div>
     <div class="pd-formula-math">$\\displaystyle \\mathbb P\\Big(\\bigcup_i A_i\\Big) \\le \\sum_i \\mathbb P(A_i)$</div></div>
     <div class="callout good"><div class="lbl">Kỹ thuật phổ biến nhất môn học</div>
     Có $n$ sự kiện xấu tiềm năng (vd n bộ đếm có thể sai)? Chia đều ngân sách lỗi: mỗi sự kiện được phép
     xác suất $\\delta/n$, tổng theo union bound vẫn $\\le \\delta$. Xuất hiện trong CountMin, q-digest, mọi
     cấu trúc có nhiều thành phần cần đồng thời đúng.</div>""")]),
  dict(title="Case study: CountMin & heavy hitters", bullets=["L hàng độc lập, mỗi hàng lỗi xác suất 1/2",
    "Union bound: xác suất TẤT CẢ hàng cùng sai $\\le 2^{-L}$", "Thủ thuật dyadic dùng union bound qua O(log n) tầng"],
   slides=[dict(h="CountMin: bao nhiêu hàng là đủ?", body="""
     <p>CountMin dùng $L$ hàm băm độc lập, mỗi hàng cho ước lượng lệch $\\le \\|x\\|_1/k$ với xác suất $\\ge 1/2$
     (Markov). Lấy <b>min</b> qua $L$ hàng: xác suất TẤT CẢ hàng đều sai $\\le 2^{-L}$ — chỉ cần
     $L=O(\\log(1/\\delta))$ hàng để đạt độ tin cậy $1-\\delta$.</p>
     <div class="callout info"><div class="lbl">Liên hệ dyadic trick</div>
     Thủ thuật cây dyadic tìm heavy hitters cần union bound qua $O(\\log n)$ tầng của cây nhị phân — mỗi tầng
     được cấp một phần ngân sách lỗi $\\delta/O(\\log n)$ để tổng lỗi vẫn $\\le \\delta$.</div>""")]),
 ],
 quiz=[
  dict(q="So với Chernoff, Hoeffding tổng quát hơn ở điểm nào?",
   opts=["Không cần các biến độc lập","Không đòi hỏi phân phối Bernoulli, chỉ cần biến bị chặn trong khoảng","Cho chặn chặt hơn luôn","Chỉ dùng được cho 1 biến"],
   correct=1, explain="Hoeffding áp dụng cho biến độc lập bị chặn bất kỳ [a_i,b_i], không riêng Bernoulli."),
  dict(q="Union bound $\\mathbb P(\\cup A_i)\\le\\sum\\mathbb P(A_i)$ đúng trong điều kiện nào?",
   opts=["Chỉ khi các $A_i$ độc lập","Chỉ khi các $A_i$ rời nhau","Luôn đúng, không cần điều kiện gì","Chỉ khi n=2"],
   correct=2, explain="Union bound là hệ quả của tiên đề cộng tính, đúng vô điều kiện cho mọi tập sự kiện."),
  dict(q="Trong CountMin, xác suất TẤT CẢ $L$ hàng cùng cho ước lượng sai là bao nhiêu (mỗi hàng lỗi độc lập xác suất 1/2)?",
   opts=["$1/2$", "$L/2$", "$2^{-L}$", "$1-2^{-L}$"], correct=2,
   explain="Các hàng độc lập, xác suất TẤT CẢ cùng sai = tích các xác suất lỗi = (1/2)^L = 2^{-L}."),
  dict(q="Kỹ thuật 'chia đều ngân sách lỗi $\\delta/n$ cho n sự kiện' dựa trên nguyên lý nào?",
   opts=["Chernoff bound","Union bound","Định lý giới hạn trung tâm","Bất đẳng thức Hölder"], correct=1,
   explain="Đây là ứng dụng trực tiếp và phổ biến nhất của union bound trong phân tích thuật toán streaming."),
  dict(q="Thủ thuật dyadic (cây nhị phân tìm heavy hitters) cần union bound qua bao nhiêu tầng?",
   opts=["$O(1)$", "$O(\\sqrt n)$", "$O(\\log n)$", "$O(n)$"], correct=2,
   explain="Cây nhị phân trên [n] có O(log n) tầng, mỗi tầng cần một phần ngân sách lỗi riêng."),
 ]),

# ---------------------------------------------------------------- 6
dict(n=6, slug="06-quy-nap", title="Quy nạp toán học & ước lượng không chệch",
 tag="Công cụ chứng minh",
 intro="Công cụ chứng minh các công thức 'sau n bước cập nhật' — và khái niệm trung tâm của mọi ước lượng streaming: không chệch.",
 parts=[
  dict(title="Quy nạp & ước lượng không chệch", bullets=["Cơ sở + bước quy nạp",
    "Định nghĩa $\\mathbb E[\\tilde X]=\\theta$", "Trung bình các ước lượng không chệch vẫn không chệch"],
   slides=[dict(h="Vì sao quy nạp xuất hiện khắp môn học", body="""
     <p>Streaming cập nhật <i>từng bước một</i> (mỗi phần tử tới, cập nhật trạng thái) — công thức kiểu
     "$\\mathbb E[f(X_n)]=g(n)$ sau $n$ bước" gần như luôn chứng minh bằng quy nạp theo $n$: giả sử đúng ở
     bước $n$, tính $\\mathbb E[f(X_{n+1})]$ bằng cách lấy kỳ vọng có điều kiện theo $X_n$.</p>"""),
   dict(h="Ước lượng không chệch", body="""
     <div class="pd-formula"><div class="pd-formula-label">Định nghĩa</div>
     <div class="pd-formula-math">$\\tilde X$ không chệch cho $\\theta$ $\\iff$ $\\mathbb E[\\tilde X] = \\theta$</div></div>
     <div class="callout good"><div class="lbl">Tính chất cộng được</div>
     Nếu $\\tilde X_1,\\dots,\\tilde X_k$ đều không chệch cho cùng $\\theta$, thì trung bình của chúng cũng
     không chệch (theo tuyến tính kỳ vọng, buổi 1) — đây là lý do "lấy trung bình nhiều bản sao" (buổi 3)
     không làm hỏng tính không chệch, chỉ giảm phương sai.</div>
     <div class="callout warn"><div class="lbl">Bẫy</div>Không chệch KHÔNG đồng nghĩa "tốt" — một ước lượng
     luôn trả về hằng số cố định có thể không chệch tình cờ ở 1 giá trị $\\theta$ cụ thể, nhưng vô dụng nói chung.</div>""")]),
  dict(title="Case study: quy nạp trong Morris", bullets=["$\\mathbb E[2^{X_{n+1}}\\mid X_n=j]$ tính được cụ thể",
    "Quy nạp: $\\mathbb E[2^{X_n}]=n+1$ với mọi n", "Đây là bằng chứng KMV/FM cũng dùng lại"],
   slides=[dict(h="Chứng minh quy nạp cho Morris", body="""
     <p>Bước quy nạp của Morris: với $X_n=j$, xác suất tăng là $1/2^j$, nên
     $\\mathbb E[2^{X_{n+1}}\\mid X_n{=}j] = 2^j(1-\\tfrac1{2^j}) + \\tfrac1{2^j}\\cdot 2^{j+1} = 2^j+1$.
     Lấy kỳ vọng theo phân phối của $X_n$: $\\mathbb E[2^{X_{n+1}}] = \\mathbb E[2^{X_n}]+1$. Cơ sở $n=0$:
     $\\mathbb E[2^{X_0}]=1$. Suy ra $\\mathbb E[2^{X_n}]=n+1$ — sơ đồ quy nạp này lặp lại ở FM (buổi 7) và
     nhiều thuật toán khác có cập nhật theo bước.</p>""")]),
 ],
 quiz=[
  dict(q="Một chứng minh quy nạp cần đủ 2 thành phần nào?",
   opts=["Bước cơ sở và bước quy nạp","Chỉ cần bước quy nạp","Chỉ cần bước cơ sở","Định lý Markov và Chebyshev"],
   correct=0, explain="Thiếu 1 trong 2 (đặc biệt là bước cơ sở) là lỗi chứng minh quy nạp phổ biến nhất."),
  dict(q="Ước lượng $\\tilde X$ được gọi là 'không chệch' cho $\\theta$ khi nào?",
   opts=["$\\tilde X = \\theta$ luôn đúng","$\\mathbb E[\\tilde X]=\\theta$","$\\mathrm{Var}[\\tilde X]=0$","$\\tilde X \\ge \\theta$"],
   correct=1, explain="Không chệch là tính chất về kỳ vọng, không phải về từng lần chạy cụ thể."),
  dict(q="Trung bình của $k$ ước lượng không chệch độc lập cho cùng $\\theta$ thì:",
   opts=["Vẫn không chệch cho $\\theta$","Trở thành chệch","Không xác định được","Chỉ không chệch khi k=1"],
   correct=0, explain="Theo tuyến tính kỳ vọng: E[trung bình] = trung bình các E[.] = θ."),
  dict(q="Trong chứng minh quy nạp của Morris, bước quy nạp dùng kỹ thuật nào từ buổi 1?",
   opts=["Bất đẳng thức Markov","Kỳ vọng có điều kiện + tuyến tính kỳ vọng","Bất đẳng thức Chebyshev","Union bound"],
   correct=1, explain="Tính E[2^{X_{n+1}}] bằng cách lấy kỳ vọng có điều kiện theo X_n rồi dùng linearity."),
  dict(q="Vì sao 'không chệch' một mình chưa đủ để đánh giá một ước lượng tốt?",
   opts=["Vì công thức có thể sai","Vì cần thêm kiểm soát phương sai (độ phân tán quanh θ)","Vì không chệch luôn kéo theo chính xác","Không có lý do gì, không chệch là đủ"],
   correct=1, explain="Một ước lượng không chệch nhưng phương sai cực lớn vẫn có thể vô dụng trong thực tế — cần Chebyshev/Chernoff kiểm soát thêm."),
 ]),

# ---------------------------------------------------------------- 7
dict(n=7, slug="07-tail-taylor", title="Tail integral & khai triển Taylor",
 tag="Công cụ giải tích",
 intro="Hai công cụ giải tích dùng để tính kỳ vọng của 'giá trị nhỏ nhất' và để xấp xỉ các hàm mũ/logarit xuất hiện trong chứng minh Chernoff.",
 parts=[
  dict(title="Tail integral", bullets=["$\\mathbb E[X]=\\int_0^\\infty \\mathbb P(X>\\lambda)d\\lambda$",
    "Dùng để tính kỳ vọng của min của các biến Uniform", "Nền tảng phân tích FM lý tưởng hoá"],
   slides=[dict(h="Công thức tail integral", body="""
     <div class="pd-formula"><div class="pd-formula-label">Tail integral (X ≥ 0)</div>
     <div class="pd-formula-math">$\\displaystyle \\mathbb E[X] = \\int_0^\\infty \\mathbb P(X>\\lambda)\\,d\\lambda$</div></div>
     <p>Hữu ích khi biết $\\mathbb P(X>\\lambda)$ dễ hơn biết phân phối đầy đủ của $X$ — điển hình khi
     $X=\\min(h_1,\\dots,h_t)$ với $h_i$ độc lập Uniform(0,1): $\\mathbb P(X>\\lambda)=(1-\\lambda)^t$, tích phân
     ra ngay $\\mathbb E[X]=1/(t+1)$.</p>"""),
   dict(h="Khai triển Taylor trong chứng minh Chernoff", body="""
     <div class="pd-formula"><div class="pd-formula-label">Bất đẳng thức nền</div>
     <div class="pd-formula-math">$1+a \\le e^a$ với mọi $a$ thực</div></div>
     <p>Bất đẳng thức này (suy từ Taylor của $e^a$ hoặc đạo hàm) là bước kỹ thuật quyết định trong mọi chứng
     minh Chernoff/Hoeffding — dùng để chặn từng nhân tử $\\mathbb E[e^{tX_i}]$ khi khai triển hàm sinh moment.</p>""")]),
  dict(title="Case study: FM lý tưởng hoá", bullets=["$X=\\min_i h(i)$, ước lượng $\\hat t = 1/X - 1$",
    "$\\mathbb E[X]=1/(t+1)$ tính bằng tail integral", "$\\mathrm{Var}[X]<(\\mathbb E X)^2$ — cần thêm lấy trung bình"],
   slides=[dict(h="FM: đếm phần tử phân biệt bằng min của hash", body="""
     <p>Chọn hàm băm ngẫu nhiên $h:[n]\\to[0,1]$, duy trì $X=\\min_{i\\in\\text{luồng}} h(i)$. Với $t$ phần tử
     phân biệt, $X$ chính là min của $t$ biến Uniform(0,1) độc lập → $\\mathbb E[X]=1/(t+1)$, nên
     $\\hat t = 1/X - 1$ là ước lượng "gần không chệch". Tính $\\mathbb E[X^2]=2/((t+1)(t+2))$ bằng cùng kỹ
     thuật tail integral cho thấy $\\mathrm{Var}[X]<(\\mathbb E X)^2$ — vẫn cần lấy trung bình nhiều bản sao
     (buổi 3) để giảm sai số.</p>""")]),
 ],
 quiz=[
  dict(q="Công thức tail integral $\\mathbb E[X]=\\int_0^\\infty \\mathbb P(X>\\lambda)d\\lambda$ áp dụng cho:",
   opts=["Mọi biến ngẫu nhiên","Chỉ biến X ≥ 0","Chỉ biến rời rạc","Chỉ biến có phân phối đều"], correct=1,
   explain="Công thức này chỉ đúng cho biến ngẫu nhiên không âm."),
  dict(q="Với $X=\\min$ của $t$ biến Uniform(0,1) độc lập, $\\mathbb P(X>\\lambda)$ bằng gì?",
   opts=["$\\lambda^t$", "$(1-\\lambda)^t$", "$t(1-\\lambda)$", "$1-\\lambda^t$"], correct=1,
   explain="Tất cả t biến đều phải > λ, mỗi biến độc lập có xác suất (1-λ), nhân lại."),
  dict(q="Bất đẳng thức $1+a\\le e^a$ được dùng ở bước nào trong chứng minh Chernoff?",
   opts=["Chặn từng nhân tử khi khai triển MGF $\\mathbb E[e^{tX_i}]$","Tính phương sai","Áp dụng Markov cuối cùng","Không liên quan tới Chernoff"],
   correct=0, explain="Đây là bước kỹ thuật cốt lõi biến tích các (1+p(e^t-1)) thành chặn hàm mũ gọn hơn."),
  dict(q="Trong FM lý tưởng hoá, ước lượng số phần tử phân biệt $\\hat t$ được tính từ $X=\\min h(i)$ như thế nào?",
   opts=["$\\hat t = X$","$\\hat t = 1/X - 1$","$\\hat t = 1-X$","$\\hat t = X^2$"], correct=1,
   explain="Từ E[X]=1/(t+1), nghịch đảo trừ 1 cho ước lượng của t."),
  dict(q="Vì sao chỉ 1 bản sao FM (1 hàm băm) chưa đủ dùng trong thực tế?",
   opts=["Vì tính toán quá chậm","Vì Var[X] vẫn cùng bậc với (E[X])², cần lấy trung bình nhiều bản sao để giảm sai số","Vì công thức sai","Vì không thể cài đặt được"],
   correct=1, explain="Giống mọi ước lượng không chệch khác trong môn, cần thêm bước Chebyshev/median trick để đủ tin cậy."),
 ]),

# ---------------------------------------------------------------- 8
dict(n=8, slug="08-vector-chuan", title="Vector, tích trong, chuẩn $\\ell_p$",
 tag="Đại số tuyến tính",
 intro="Ngôn ngữ hình học của streaming: một luồng dữ liệu chính là một vector, và $F_0, F_1, F_2$ chính là các chuẩn của nó.",
 parts=[
  dict(title="Chuẩn $\\ell_p$", bullets=["$\\ell_1,\\ell_2$ và tổng quát $\\ell_p$", "Cauchy–Schwarz",
   "Biểu đồ tần suất của luồng dữ liệu là 1 vector"], slides=[
   dict(h="Chuẩn của một vector", body="""
     <div class="pd-formula"><div class="pd-formula-label">Chuẩn $\\ell_p$</div>
     <div class="pd-formula-math">$\\displaystyle \\|x\\|_p = \\Big(\\sum_i |x_i|^p\\Big)^{1/p}$</div></div>
     <ul class="pd-legend"><li><b>$\\ell_0$</b><span>số toạ độ khác 0 (không phải chuẩn thật, hay gọi "giả chuẩn")</span></li>
     <li><b>$\\ell_1$</b><span>tổng trị tuyệt đối</span></li>
     <li><b>$\\ell_2$</b><span>độ dài Euclid, dùng nhiều nhất trong sketching</span></li></ul>"""),
   dict(h="Vector tần suất trong streaming", body="""
     <p>Với luồng dữ liệu trên miền $[n]$, định nghĩa $x\\in\\mathbb R^n$ với $x_i=$ số lần phần tử $i$ xuất
     hiện. Khi đó:</p>
     <div class="callout good"><div class="lbl">$F_0, F_1, F_2$ chính là các chuẩn</div>
     $F_0=\\|x\\|_0$ (số phần tử phân biệt) · $F_1=\\|x\\|_1$ (tổng số phần tử, luôn = độ dài luồng nếu không âm)
     · $F_2=\\|x\\|_2^2$ (bình phương chuẩn Euclid, đo "độ lệch" phân phối tần suất — AMS sketch buổi 10 ước
     lượng đại lượng này).</div>""")]),
  dict(title="Case study: heavy hitters & chuẩn tail", bullets=["$x_{\\text{tail}(k)}$: vector sau khi bỏ k toạ độ lớn nhất",
    "Đảm bảo $\\ell_2$ mạnh hơn $\\ell_1$ hẳn", "CountSketch dùng đảm bảo $\\ell_2$, CountMin chỉ $\\ell_1$"],
   slides=[dict(h="Vì sao bảo đảm $\\ell_2$ mạnh hơn $\\ell_1$", body="""
     <p>Với $x_{\\text{tail}(k)}$ là $x$ sau khi triệt tiêu $k$ toạ độ lớn nhất, luôn có
     $\\|x_{\\text{tail}(k)}\\|_2/\\sqrt k \\le \\|x_{\\text{tail}(k)}\\|_1/k$ (hệ quả Cauchy–Schwarz). Điều này
     giải thích tại sao CountSketch (đảm bảo kiểu $\\ell_2$, buổi 10) phát hiện được nhiều phần tử "trội" hơn
     CountMin (chỉ đảm bảo kiểu $\\ell_1$) trên cùng ngân sách bộ nhớ, đặc biệt khi phân phối tần suất có
     đuôi dài (nhiều phần tử nhỏ) như phân phối Zipf.</p>""")]),
 ],
 quiz=[
  dict(q="Chuẩn $\\ell_2$ của vector $x$ được định nghĩa là gì?",
   opts=["$\\sum|x_i|$", "$\\sqrt{\\sum x_i^2}$", "$\\max|x_i|$", "Số toạ độ khác 0"], correct=1,
   explain="ℓ2 là căn bậc hai của tổng bình phương các toạ độ — độ dài Euclid."),
  dict(q="Trong streaming, $F_0$ của một luồng dữ liệu chính là chuẩn nào của vector tần suất $x$?",
   opts=["$\\|x\\|_1$", "$\\|x\\|_2^2$", "$\\|x\\|_0$ (số toạ độ khác 0)", "$\\|x\\|_\\infty$"], correct=2,
   explain="F0 = số phần tử phân biệt = số toạ độ khác 0 của vector tần suất."),
  dict(q="$F_2$ của một luồng dữ liệu tương ứng với đại lượng nào?",
   opts=["$\\|x\\|_1$", "$\\|x\\|_2^2$", "$\\|x\\|_0$", "Trung bình của x"], correct=1,
   explain="F2 = tổng bình phương tần suất = bình phương chuẩn Euclid, được AMS sketch ước lượng."),
  dict(q="Vì sao đảm bảo kiểu $\\ell_2$ (như CountSketch) thường phát hiện heavy hitters tốt hơn kiểu $\\ell_1$ (CountMin)?",
   opts=["Vì $\\ell_2$ luôn nhỏ hơn $\\ell_1$ nên sai số tuyệt đối nhỏ hơn","Vì bất đẳng thức Cauchy–Schwarz cho $\\|x_{tail(k)}\\|_2/\\sqrt k \\le \\|x_{tail(k)}\\|_1/k$, ngưỡng phát hiện chặt hơn","Vì CountSketch dùng nhiều bộ nhớ hơn hẳn","Không có lý do toán học, chỉ là thực nghiệm"],
   correct=1, explain="Đây chính là hệ quả Cauchy-Schwarz làm ngưỡng heavy hitter kiểu ℓ2 chặt hơn kiểu ℓ1."),
  dict(q="'Giả chuẩn' $\\ell_0$ khác các chuẩn $\\ell_p$ ($p\\ge1$) thật sự ở điểm nào?",
   opts=["Không thoả bất đẳng thức tam giác như $\\ell_p$ thật","Luôn bằng $\\ell_1$","Chỉ định nghĩa được cho vector 2 chiều","Không có gì khác biệt"],
   correct=0, explain="ℓ0 (đếm số toạ độ khác 0) không thoả bất đẳng thức tam giác thông thường, nên gọi là 'giả chuẩn'."),
 ]),

# ---------------------------------------------------------------- 9
dict(n=9, slug="09-ma-tran-sketch", title="Ma trận, nhân ma trận-vector, phép chiếu",
 tag="Đại số tuyến tính",
 intro="Một sketch tuyến tính đơn giản là $\\Pi x$ — bộ nhớ $m\\ll n$ chiều, cập nhật được tức thời khi luồng thay đổi.",
 parts=[
  dict(title="Sketch tuyến tính $\\Pi x$", bullets=["Tính tuyến tính cho phép cập nhật tức thời",
   "Tính hợp nhất: $\\Pi x + \\Pi x' = \\Pi(x+x')$", "Cột thứ $i$ của $\\Pi$ là $\\Pi e_i$"],
   slides=[dict(h="Vì sao 'sketch tuyến tính' là chìa khoá của streaming", body="""
     <div class="pd-formula"><div class="pd-formula-label">Cập nhật turnstile</div>
     <div class="pd-formula-math">$x \\leftarrow x+\\Delta e_i \\implies \\Pi x \\leftarrow \\Pi x + \\Delta\\cdot\\Pi^{(i)}$</div></div>
     <p>Vì phép nhân ma trận-vector tuyến tính, một cập nhật đơn lẻ vào luồng ($x_i \\mathrel{+}= \\Delta$, kể
     cả $\\Delta$ âm — mô hình "turnstile") chỉ cần cộng $\\Delta$ lần cột $i$ của $\\Pi$ vào sketch hiện có —
     không cần đọc lại toàn bộ $x$.</p>"""),
   dict(h="Tính hợp nhất (mergeability)", body="""
     <div class="pd-formula"><div class="pd-formula-label">Hợp nhất 2 sketch</div>
     <div class="pd-formula-math">$\\Pi x + \\Pi x' = \\Pi(x+x')$</div></div>
     <div class="callout good"><div class="lbl">Ứng dụng</div>Cho phép tính phân tán: 2 máy chủ xử lý 2 phần
     luồng riêng, mỗi máy tính sketch riêng, rồi CỘNG 2 sketch lại = sketch của toàn bộ luồng gộp — không cần
     truyền dữ liệu gốc.</div>""")]),
  dict(title="Case study: CountMin là 1 sketch tuyến tính", bullets=["Mỗi hàng CountMin = ma trận 0/1 'chọn'",
    "Hàm băm quyết định vị trí giá trị 1 mỗi cột", "$(Ax)_i = x_{h(i)}$ khi A là ma trận chọn"],
   slides=[dict(h="CountMin nhìn dưới góc độ ma trận", body="""
     <p>Một hàng của CountMin là ma trận $A\\in\\{0,1\\}^{B\\times n}$: cột $i$ của $A$ có đúng 1 giá trị 1
     tại hàng $h(i)$ (còn lại 0). Khi đó $(Ax)_j = \\sum_{i: h(i)=j} x_i$ — chính xác là "bộ đếm gộp" của
     CountMin tại ô $j$. Đây là minh chứng cụ thể nhất cho khái niệm "sketch tuyến tính": CountMin, CountSketch,
     AMS, JL transform đều chỉ là các lựa chọn khác nhau của ma trận $\\Pi$.</p>""")]),
 ],
 quiz=[
  dict(q="Tính chất nào của phép nhân ma trận-vector cho phép cập nhật sketch tức thời khi 1 phần tử luồng thay đổi?",
   opts=["Tính đối xứng","Tính tuyến tính: $\\Pi(x+\\Delta e_i)=\\Pi x+\\Delta\\Pi^{(i)}$","Tính khả nghịch","Tính trực giao"],
   correct=1, explain="Nhờ tuyến tính, chỉ cần cộng thêm Δ lần cột i của Π, không cần tính lại từ đầu."),
  dict(q="Tính hợp nhất (mergeability) $\\Pi x+\\Pi x'=\\Pi(x+x')$ có ứng dụng thực tiễn nào?",
   opts=["Giảm độ dài luồng","Cho phép tính phân tán: cộng trực tiếp 2 sketch từ 2 máy khác nhau","Tăng độ chính xác tự động","Không có ứng dụng thực tế"],
   correct=1, explain="Đây là cơ sở để streaming/sketching mở rộng ra tính toán phân tán (distributed/parallel)."),
  dict(q="Cột thứ $i$ của ma trận $\\Pi$ bằng biểu thức nào?",
   opts=["$\\Pi \\mathbf 1$", "$\\Pi e_i$ (e_i là vector đơn vị thứ i)", "$\\Pi^\\top$", "$\\Pi^{-1}$"], correct=1,
   explain="Nhân ma trận với vector đơn vị e_i luôn trích ra đúng cột thứ i."),
  dict(q="Trong CountMin, một hàng có thể biểu diễn bằng ma trận 0/1 loại nào?",
   opts=["Ma trận đơn vị","Ma trận 'chọn': mỗi cột có đúng 1 giá trị 1 tại vị trí do hàm băm quyết định","Ma trận trực giao đầy đủ","Ma trận tam giác"],
   correct=1, explain="Mỗi phần tử i được 'chọn' vào đúng 1 ô đếm h(i) — đây là bản chất ma trận của CountMin."),
  dict(q="Vì sao mô hình 'turnstile' (cho phép cả cộng và trừ $\\Delta$) vẫn hoạt động được với sketch tuyến tính?",
   opts=["Vì tuyến tính đúng với mọi $\\Delta$, kể cả âm","Vì turnstile không dùng được với sketch tuyến tính","Vì cần thêm cấu trúc dữ liệu khác cho Δ âm","Vì Δ âm bị bỏ qua"],
   correct=0, explain="Công thức Πx+ΔΠ^{(i)} đúng với mọi Δ thực, không riêng Δ dương — đây là điểm mạnh của sketch tuyến tính so với các cấu trúc chỉ-chèn."),
 ]),

# ---------------------------------------------------------------- 10
dict(n=10, slug="10-rademacher-khintchine", title="Biến Rademacher & bất đẳng thức Khintchine",
 tag="Xác suất nâng cao",
 intro="Dấu ngẫu nhiên $\\pm1$ là 'chất liệu' của AMS sketch, CountSketch, và Johnson–Lindenstrauss transform.",
 parts=[
  dict(title="Rademacher & Khintchine", bullets=["$\\sigma_i=\\pm1$ độc lập, $\\mathbb E\\sigma_i=0$",
   "$\\mathbb E[(\\sum\\sigma_ix_i)^2]=\\|x\\|_2^2$", "Khintchine: chặn hàm mũ cho tổng có dấu"],
   slides=[dict(h="Biến Rademacher", body="""
     <div class="pd-formula"><div class="pd-formula-label">Tính chất cơ bản</div>
     <div class="pd-formula-math">$\\mathbb E[\\sigma_i]=0,\\quad \\mathbb E[\\sigma_i\\sigma_j]=0\\ (i\\ne j),\\quad
     \\mathbb E\\Big[\\big(\\textstyle\\sum_i\\sigma_ix_i\\big)^2\\Big]=\\|x\\|_2^2$</div></div>
     <p>Dấu ngẫu nhiên có tính chất đẹp: bình phương tổng có dấu cho ra đúng $\\|x\\|_2^2$ — đây là "không
     chệch" cho chuẩn Euclid, nền tảng của AMS sketch.</p>"""),
   dict(h="Bất đẳng thức Khintchine", body="""
     <div class="pd-formula"><div class="pd-formula-label">Khintchine</div>
     <div class="pd-formula-math">$\\mathbb P\\big(|\\langle\\sigma,x\\rangle|>\\lambda\\big) \\le 2e^{-\\lambda^2/(2\\|x\\|_2^2)}$</div></div>
     <div class="callout good"><div class="lbl">Ý nghĩa</div>Tổng có dấu ngẫu nhiên tập trung nhanh như một
     biến chuẩn (Gaussian) có cùng phương sai $\\|x\\|_2^2$ — gọi là "dưới-Gauss" (subgaussian). Dùng để phân
     tích sai số của KLL (quantile sketch, buổi 12) và CountSketch (buổi 11).</div>""")]),
  dict(title="Case study: AMS sketch cho $F_2$", bullets=["$Y=\\sum\\sigma_ix_i$, ước lượng $Y^2$",
    "Cần độc lập bậc 4 (không chỉ bậc 2 như CountMin)", "$\\mathrm{Var}[Y^2]\\le 2\\|x\\|_2^4$"],
   slides=[dict(h="AMS: ước lượng $F_2=\\|x\\|_2^2$", body="""
     <p>Chọn $\\sigma_1,\\dots,\\sigma_n$ độc lập bậc <b>bốn</b> (mạnh hơn 2-wise của CountMin), duy trì
     $Y=\\sum_i\\sigma_ix_i$ tuyến tính khi luồng cập nhật. $\\mathbb E[Y^2]=\\|x\\|_2^2$ (không chệch), và
     $\\mathrm{Var}[Y^2]\\le 2\\|x\\|_2^4$ (cần khai triển $\\mathbb E[Y^4]$, đòi hỏi độc lập bậc 4 — lý do
     2-wise independent như trong CountMin KHÔNG đủ ở đây).</p>""")]),
 ],
 quiz=[
  dict(q="Với $\\sigma_i$ Rademacher độc lập, $\\mathbb E[\\sigma_i\\sigma_j]$ với $i\\ne j$ bằng bao nhiêu?",
   opts=["1", "0", "-1", "1/2"], correct=1,
   explain="Do độc lập và mỗi σ có kỳ vọng 0: E[σ_iσ_j]=E[σ_i]E[σ_j]=0."),
  dict(q="$\\mathbb E[(\\sum_i\\sigma_ix_i)^2]$ bằng đại lượng nào?",
   opts=["$\\|x\\|_1$", "$\\|x\\|_2^2$", "$\\|x\\|_0$", "$n$"], correct=1,
   explain="Khai triển bình phương, các số hạng chéo triệt tiêu (E[σ_iσ_j]=0), chỉ còn Σx_i²=‖x‖₂²."),
  dict(q="Bất đẳng thức Khintchine cho biết tổng có dấu ngẫu nhiên tập trung giống loại phân phối nào?",
   opts=["Đều (Uniform)","Nhị thức","Dưới-Gauss (subgaussian), giống phân phối chuẩn","Không tập trung, phân tán đều"],
   correct=2, explain="Đây chính là ý nghĩa 'dưới-Gauss' của Khintchine — đuôi giảm nhanh như Gaussian."),
  dict(q="Vì sao AMS sketch (ước lượng $F_2$) cần hàm băm/dấu độc lập BẬC BỐN, không chỉ 2-wise như CountMin?",
   opts=["Vì cần tính $\\mathbb E[Y^4]$ để chặn $\\mathrm{Var}[Y^2]$, đòi hỏi độc lập bậc cao hơn","Vì AMS dùng nhiều bộ nhớ hơn","Vì đây chỉ là quy ước, không có lý do toán học","Vì 2-wise không tồn tại"],
   correct=0, explain="Phân tích phương sai của Y² cần khai triển E[Y⁴], các số hạng chéo chỉ triệt tiêu đúng cách khi có độc lập bậc 4."),
  dict(q="$Y=\\sum\\sigma_ix_i$ trong AMS sketch được duy trì như thế nào khi luồng cập nhật (turnstile)?",
   opts=["Phải tính lại từ đầu mỗi lần","Cập nhật tuyến tính: $Y \\mathrel{+}= \\Delta\\cdot\\sigma_i$ khi $x_i\\mathrel{+}=\\Delta$","Không thể cập nhật được trên turnstile","Cần lưu toàn bộ x"],
   correct=1, explain="Y là một sketch tuyến tính (giống buổi 9), nên cập nhật tức thời theo từng Δ."),
 ]),

# ---------------------------------------------------------------- 11
dict(n=11, slug="11-ham-bam", title="Hàm băm & k-wise independence",
 tag="Cấu trúc rời rạc",
 intro="Hàm băm k-wise independent: đủ 'giả ngẫu nhiên' cho các chứng minh, nhưng rẻ hơn ngẫu nhiên hoàn toàn rất nhiều lần.",
 parts=[
  dict(title="k-wise independent hashing", bullets=["Định nghĩa: xác suất đúng $1/b^k$ cho mọi k chỉ số",
   "Xây bằng đa thức bậc $\\le k-1$ trên $\\mathbb F_p$", "Chỉ cần $k\\log p$ bit thay vì $n\\log n$"],
   slides=[dict(h="Định nghĩa k-wise independence", body="""
     <div class="pd-formula"><div class="pd-formula-label">$k$-wise independent</div>
     <div class="pd-formula-math">$\\forall i_1,\\dots,i_k$ phân biệt, $\\forall j_1,\\dots,j_k\\in[b]$:
     $\\mathbb P_h(h(i_1){=}j_1\\wedge\\cdots\\wedge h(i_k){=}j_k) = 1/b^k$</div></div>
     <p>Yếu hơn "ngẫu nhiên hoàn toàn" (cần lưu $n\\log b$ bit) nhưng đủ mạnh cho hầu hết chứng minh chỉ dùng
     đến $\\mathbb E, \\mathrm{Var}$ (2-wise) hoặc moment bậc 4 (4-wise).</p>"""),
   dict(h="Xây dựng bằng đa thức", body="""
     <p>Họ $\\mathcal H_{\\text{poly}}$ gồm mọi đa thức bậc $\\le k-1$ trên trường hữu hạn $\\mathbb F_p$:
     theo nội suy Lagrange, với $k$ cặp $(i_r,j_r)$ cho trước tồn tại <b>đúng một</b> đa thức bậc $\\le k-1$
     đi qua tất cả — đây chính xác là điều kiện $k$-wise independent, và mỗi hàm chỉ cần $k\\log p$ bit để
     lưu (hệ số đa thức), thay vì $n\\log n$ bit của bảng tra cứu đầy đủ.</p>""")]),
  dict(title="Case study: CountMin/CountSketch chỉ cần 2-wise", bullets=["Phân tích phương sai CountMin chỉ dùng E, Var",
    "2-wise đủ để $\\mathrm{Cov}(\\mathbf1[h(i){=}v],\\mathbf1[h(j){=}v])=0$", "Tiết kiệm bộ nhớ hàm băm đáng kể"],
   slides=[dict(h="Vì sao CountMin chỉ cần 2-wise independent", body="""
     <p>Phân tích sai số CountMin (buổi 5, dùng Markov cho biến "nhiễu" $Z=\\sum_{j\\ne i}x_j\\mathbf1[h(j){=}h(i)]$)
     chỉ cần $\\mathbb E[Z]$ — mà $\\mathbb E[\\mathbf1[h(j){=}h(i)]]=1/B$ chỉ đòi hỏi hàm băm 2-wise independent
     (biết riêng từng cặp $(i,j)$ là đủ, không cần biết đồng thời hành vi của mọi phần tử). Đây là lý do
     CountMin/CountSketch chỉ cần hàm băm tuyến tính $h(x)=(ax+b)\\bmod p$ (2-wise), rẻ hơn nhiều so với
     4-wise cần cho AMS (buổi 10).</p>""")]),
 ],
 quiz=[
  dict(q="Họ hàm băm $k$-wise independent yêu cầu điều gì về xác suất đồng thời?",
   opts=["$\\mathbb P(h(i_1)=j_1\\wedge\\dots\\wedge h(i_k)=j_k)=1/b^k$ với mọi bộ $k$ chỉ số phân biệt","Chỉ cần đúng khi k=n","Xác suất luôn bằng 1","Không có yêu cầu cụ thể"],
   correct=0, explain="Đây là định nghĩa chuẩn: hành vi của k chỉ số bất kỳ giống hệt như k hàm hoàn toàn độc lập ngẫu nhiên."),
  dict(q="Họ đa thức bậc $\\le k-1$ trên $\\mathbb F_p$ đạt k-wise independent nhờ định lý nào?",
   opts=["Định lý Fermat nhỏ","Nội suy Lagrange: k điểm xác định duy nhất 1 đa thức bậc ≤k-1","Bất đẳng thức Cauchy-Schwarz","Định lý giới hạn trung tâm"],
   correct=1, explain="Đúng 1 đa thức bậc ≤k-1 đi qua k điểm cho trước — đây là cơ sở đếm để suy ra xác suất đúng 1/p^k."),
  dict(q="Một hàm trong $\\mathcal H_{\\text{poly}}$ bậc $k-1$ trên $\\mathbb F_p$ cần bao nhiêu bit để lưu?",
   opts=["$n\\log p$", "$k\\log p$", "$p\\log k$", "$\\log(np)$"], correct=1,
   explain="Chỉ cần lưu k hệ số của đa thức, mỗi hệ số trong F_p tốn log p bit."),
  dict(q="CountMin/CountSketch chỉ cần hàm băm mấy-wise independent để phân tích đúng?",
   opts=["1-wise", "2-wise", "4-wise", "n-wise"], correct=1,
   explain="Phân tích chỉ dùng E[Z] của biến nhiễu (buổi 5), chỉ cần biết xác suất va chạm từng cặp — đủ với 2-wise."),
  dict(q="Vì sao AMS sketch (buổi 10) cần độ độc lập cao hơn CountMin?",
   opts=["Vì AMS phân tích Var[Y²] cần E[Y⁴], đòi hỏi 4-wise independent","Vì AMS dùng ma trận lớn hơn","Vì AMS không dùng hàm băm","Không có sự khác biệt thực sự"],
   correct=0, explain="Đây chính là điểm khác biệt kỹ thuật giữa hai loại sketch — mức độ độc lập cần thiết phụ thuộc bậc moment cần phân tích."),
 ]),

# ---------------------------------------------------------------- 12
dict(n=12, slug="12-cay-nhi-phan", title="Cấu trúc cây nhị phân & rank/order statistics",
 tag="Cấu trúc dữ liệu",
 intro="Cây nhị phân là xương sống của q-digest, MRL, KLL (quantile sketches) và thủ thuật dyadic cho heavy hitters.",
 parts=[
  dict(title="Cây nhị phân & rank", bullets=["$\\mathrm{rank}(x)$: số phần tử $\\le x$",
   "Cây nhị phân hoàn chỉnh: $2^{L+1}-1$ nút", "Ý tưởng nén: gộp bớt để tiết kiệm bộ nhớ"],
   slides=[dict(h="Rank và quantile", body="""
     <div class="pd-formula"><div class="pd-formula-label">Rank</div>
     <div class="pd-formula-math">$\\mathrm{rank}(x) = |\\{i : y_i \\le x\\}|$</div></div>
     <p>Bài toán quantile: trả lời $\\mathrm{rank}(x)$ hoặc $\\mathrm{quantile}(\\phi)$ với sai số $\\pm\\varepsilon n$,
     dùng ít hơn hẳn $O(n)$ bộ nhớ. q-digest, MRL, KLL là 3 hướng giải khác nhau, đều dựa trên cây nhị phân.</p>"""),
   dict(h="Ý tưởng nén trên cây", body="""
     <p>q-digest: mỗi đỉnh cây có bộ đếm, gộp 2 đỉnh anh em vào đỉnh cha khi tổng đủ nhỏ (điều kiện nén
     $\\le \\varepsilon n/L$) — tiết kiệm bộ nhớ, đổi lấy sai số có kiểm soát (tổng sai số tích luỹ $\\le
     \\varepsilon n$ vì chỉ có $L$ tổ tiên cho mỗi truy vấn).</p>
     <div class="callout warn"><div class="lbl">Bẫy</div>MRL nén tất định (luôn giữ vị trí lẻ) có thể tích luỹ
     lỗi hệ thống; KLL sửa bằng cách <b>nén ngẫu nhiên</b> (chọn ngẫu nhiên vị trí lẻ/chẵn) — biến sai số
     thành tổng có dấu ngẫu nhiên, áp dụng được Khintchine (buổi 10) để chặn chặt hơn nhiều.</div>""")]),
  dict(title="Case study: thủ thuật dyadic cho heavy hitters", bullets=["Cây nhị phân trên [n], mỗi tầng 1 sketch riêng",
    "Cập nhật: mọi tổ tiên của lá phải cập nhật", "Truy vấn: chỉ đi vào nhánh có giá trị đủ lớn"],
   slides=[dict(h="Tăng tốc truy vấn heavy hitters", body="""
     <p>Xây cây nhị phân hoàn chỉnh trên $[n]$: mỗi tầng $j$ giữ 1 sketch CountMin cho vector đã "gộp đôi"
     $2^j$ lần. Cập nhật 1 phần tử phải cập nhật sketch ở MỌI tầng (mọi tổ tiên của lá tương ứng). Bù lại,
     truy vấn "chỉ đi tiếp vào nhánh có giá trị đủ lớn" giảm thời gian truy vấn từ $O(n\\log(n/\\delta))$
     xuống $O(k\\log(n/\\delta)\\log n)$ — minh chứng thực tế cho cây nhị phân + union bound (buổi 5) kết hợp.</p>""")]),
 ],
 quiz=[
  dict(q="Cây nhị phân hoàn chỉnh có $L+1$ mức (mức 0 là gốc) có tổng bao nhiêu nút?",
   opts=["$L+1$", "$2^{L+1}-1$", "$2^L$", "$L^2$"], correct=1,
   explain="Tổng số nút từ mức 0 đến L: 2^0+2^1+...+2^L = 2^{L+1}-1."),
  dict(q="Điều kiện nén trong q-digest ($c[p]+c[v]+c[\\text{sibling}]\\le\\varepsilon n/L$) đảm bảo điều gì?",
   opts=["Cây luôn cân bằng hoàn hảo","Tổng sai số tích luỹ tại mỗi truy vấn rank $\\le \\varepsilon n$","Không bao giờ có sai số","Bộ nhớ luôn bằng 0"],
   correct=1, explain="Mỗi tổ tiên góp tối đa εn/L sai số, có L tổ tiên nên tổng ≤ εn."),
  dict(q="Điểm khác biệt chính giữa MRL và KLL trong cách nén là gì?",
   opts=["KLL không dùng cây nhị phân","KLL chọn ngẫu nhiên vị trí lẻ/chẵn khi nén, MRL luôn cố định","MRL nhanh hơn KLL rất nhiều","Không có khác biệt đáng kể"],
   correct=1, explain="Đây là điểm mấu chốt: ngẫu nhiên hoá biến sai số MRL (tất định) thành tổng có dấu ngẫu nhiên kiểu Khintchine (buổi 10) cho KLL, cho chặn chặt hơn."),
  dict(q="Trong thủ thuật dyadic (heavy hitters), khi 1 phần tử được cập nhật, cần cập nhật những sketch nào?",
   opts=["Chỉ sketch ở lá tương ứng","Sketch tại MỌI tổ tiên của lá đó trên cây","Chỉ sketch tại gốc","Không cần cập nhật gì thêm"],
   correct=1, explain="Mỗi tầng của cây giữ 1 sketch riêng cho vector đã gộp ở mức đó, nên mọi tổ tiên đều cần cập nhật."),
  dict(q="Thủ thuật dyadic giảm thời gian truy vấn heavy hitters từ $O(n\\log(n/\\delta))$ xuống mức nào?",
   opts=["$O(1)$", "$O(k\\log(n/\\delta)\\log n)$", "$O(n^2)$", "Không giảm được"], correct=1,
   explain="Nhờ chỉ đi tiếp vào nhánh có giá trị đủ lớn (cắt tỉa cây), thay vì duyệt toàn bộ n phần tử."),
 ]),

# ---------------------------------------------------------------- 13
dict(n=13, slug="13-do-thi-boruvka", title="Đồ thị cơ bản, liên thông & Borůvka",
 tag="Cấu trúc rời rạc",
 intro="Bài toán liên thông trên luồng cạnh động (có xoá) cần một thuật toán khác hẳn union-find truyền thống: sketch AGM.",
 parts=[
  dict(title="Liên thông & thuật toán Borůvka", bullets=["Union-find sụp đổ khi luồng có XOÁ cạnh",
   "Borůvka: mỗi vòng số thành phần giảm ít nhất một nửa", "$O(\\log n)$ vòng để có cây khung"],
   slides=[dict(h="Vì sao union-find không đủ cho luồng động", body="""
     <p>Với luồng chỉ chèn cạnh, union-find (find/union) giải quyết liên thông trong $O(N\\log N)$ bit. Nhưng
     nếu luồng cho phép XOÁ cạnh, một cạnh đã dùng để hợp nhất 2 thành phần có thể bị xoá sau đó — union-find
     "sụp đổ", không có cách hoàn tác rẻ. Đây là động lực cho sketch tuyến tính (AGM, buổi sau) chịu được
     turnstile.</p>"""),
   dict(h="Thuật toán Borůvka", body="""
     <div class="pd-formula"><div class="pd-formula-label">Borůvka</div>
     <div class="pd-formula-math">Mỗi vòng: mỗi thành phần liên thông chọn 1 cạnh đi ra ngoài (nếu có), hợp nhất.</div></div>
     <div class="callout good"><div class="lbl">Vì sao chỉ cần $O(\\log n)$ vòng</div>
     Mỗi vòng, mỗi thành phần ghép với ít nhất 1 thành phần khác → số thành phần giảm ít nhất một nửa. Sau
     $O(\\log n)$ vòng, chỉ còn 1 thành phần (hoặc rừng cây khung hoàn chỉnh).</div>""")]),
  dict(title="Case study: sketch AGM cho đồ thị động", bullets=["Vector cạnh kề có dấu $a_i$ cho mỗi đỉnh",
    "$\\mathrm{supp}(\\sum_{i\\in S}a_i)$ = đúng tập cạnh cắt qua S", "Kết hợp SupportFind + Borůvka trong $O(N\\log^3 N)$ bit"],
   slides=[dict(h="Ý tưởng sketch AGM", body="""
     <p>Với mỗi đỉnh $i$, định nghĩa vector $a_i\\in\\mathbb R^{\\binom V2}$: $+1$ tại cạnh $\\{u,v\\}$ nếu
     $i=\\min(u,v)$, $-1$ nếu $i=\\max(u,v)$. Mệnh đề then chốt: với $S\\subseteq V$,
     $\\mathrm{supp}(\\sum_{i\\in S}a_i) = E(S,V\\setminus S)$ — cạnh có cả 2 đầu trong $S$ triệt tiêu, chỉ còn
     đúng các cạnh cắt. Kết hợp với <b>SupportFind</b> (khôi phục 1 phần tử khác 0 từ 1 sketch tuyến tính,
     buổi 14) và vòng lặp kiểu Borůvka, AGM giải liên thông trên luồng ĐỘNG (có xoá) chỉ trong
     $O(N\\log^3 N)$ bit — không cần lưu toàn bộ đồ thị.</p>""")]),
 ],
 quiz=[
  dict(q="Vì sao union-find truyền thống không giải quyết được liên thông trên luồng cạnh có XOÁ?",
   opts=["Vì union-find quá chậm","Vì 1 cạnh dùng để hợp nhất có thể bị xoá sau, không có cách hoàn tác rẻ","Vì union-find chỉ dùng được cho cây","Không có vấn đề gì, union-find vẫn dùng được"],
   correct=1, explain="Đây chính là hạn chế cốt lõi khiến cần đến sketch tuyến tính (AGM) cho luồng động."),
  dict(q="Sau mỗi vòng của thuật toán Borůvka, số thành phần liên thông giảm ít nhất bao nhiêu?",
   opts=["Giảm 1 đơn vị","Giảm một nửa","Không đổi","Giảm về 1 ngay lập tức"], correct=1,
   explain="Mỗi thành phần ghép với ít nhất 1 thành phần khác, nên số thành phần giảm ít nhất 2 lần."),
  dict(q="Từ tính chất giảm một nửa mỗi vòng, số vòng Borůvka cần trên đồ thị N đỉnh là bao nhiêu?",
   opts=["$O(N)$", "$O(\\log N)$", "$O(\\sqrt N)$", "$O(1)$"], correct=1,
   explain="Số thành phần giảm cấp số nhân theo cơ số 2, nên cần O(log N) vòng để về 1."),
  dict(q="Mệnh đề then chốt của sketch AGM là $\\mathrm{supp}(\\sum_{i\\in S}a_i)$ bằng gì?",
   opts=["Toàn bộ cạnh của đồ thị","Tập cạnh cắt $E(S,V\\setminus S)$","Số đỉnh trong S","Luôn bằng tập rỗng"],
   correct=1, explain="Cạnh có cả 2 đầu trong S triệt tiêu trong tổng, chỉ còn lại đúng các cạnh cắt qua S."),
  dict(q="Sketch AGM kết hợp Borůvka với công cụ nào để tìm 1 cạnh đi ra khỏi 1 siêu đỉnh?",
   opts=["CountMin sketch","SupportFind (khôi phục 1-thưa)","AMS sketch","q-digest"], correct=1,
   explain="SupportFind khôi phục đúng 1 phần tử khác 0 từ vector ẩn — chính là 1 cạnh cắt cần tìm mỗi vòng Borůvka."),
 ]),

# ---------------------------------------------------------------- 14
dict(n=14, slug="14-truong-huu-han", title="Số học $\\mathbb F_p$, đa thức & Schwartz–Zippel",
 tag="Cấu trúc rời rạc",
 intro="Bổ đề nhỏ nhưng cực kỳ mạnh: đa thức khác 0 hiếm khi 'tình cờ' bằng 0 — nền tảng của khôi phục 1-thưa và hàm băm.",
 parts=[
  dict(title="Trường hữu hạn & Schwartz–Zippel", bullets=["$\\mathbb F_p$: số học modulo p",
   "Đa thức bậc d có tối đa d nghiệm", "Schwartz–Zippel: $\\mathbb P(h(z)=0)\\le d/p$"],
   slides=[dict(h="Bổ đề Schwartz–Zippel", body="""
     <div class="pd-formula"><div class="pd-formula-label">Schwartz–Zippel (1 biến)</div>
     <div class="pd-formula-math">$h\\ne 0$ bậc $d$ trên $\\mathbb F_p$ $\\implies \\mathbb P_{z\\sim\\mathbb F_p}(h(z)=0)\\le d/p$</div></div>
     <p>Vì đa thức khác 0 bậc $d$ có tối đa $d$ nghiệm, chọn $z$ ngẫu nhiên trong $\\mathbb F_p$ hiếm khi
     "vô tình" trúng nghiệm — nếu $p\\gg d$, xác suất này gần như bằng 0. Đây là công cụ kiểm tra đẳng thức
     đa thức "giá rẻ" cực kỳ phổ biến trong khoa học máy tính lý thuyết.</p>"""),
   dict(h="Ba bộ đếm tuyến tính cho khôi phục 1-thưa", body="""
     <div class="pd-formula"><div class="pd-formula-label">SupportFind: $s_0,s_1,s_2$</div>
     <div class="pd-formula-math">$s_0=\\sum x_i,\\ \\ s_1=\\sum i\\cdot x_i,\\ \\ s_2=\\sum x_i z^i \\bmod p$</div></div>
     <p>Nếu $x=v\\cdot e_j$ (đúng 1 toạ độ khác 0): $j=s_1/s_0$, $v=s_0$. Kiểm tra $s_2\\overset?=s_0z^j$ xác
     nhận giả thuyết 1-thưa — nếu $x$ KHÔNG 1-thưa, xác suất kiểm tra vẫn "qua" (báo nhầm) bị chặn bởi
     Schwartz–Zippel, $\\le n/p$.</p>""")]),
  dict(title="Case study: k-wise hashing & SupportFind trong AGM", bullets=["Đa thức bậc k-1 = hàm băm k-wise (buổi 11)",
    "SupportFind là mảnh ghép cuối của sketch AGM (buổi 13)", "Cả môn học khép vòng tại đây"],
   slides=[dict(h="Điểm hội tụ của cả môn học", body="""
     <p>Buổi cuối này khép lại một vòng tròn: đa thức trên $\\mathbb F_p$ vừa là công cụ xây hàm băm $k$-wise
     independent (buổi 11), vừa là công cụ kiểm tra đẳng thức trong SupportFind — chính mảnh ghép giúp sketch
     AGM (buổi 13) tìm ra 1 cạnh cắt trong mỗi vòng Borůvka. Bốn thành phần hàm băm $k$-wise, cây nhị phân,
     Borůvka, và Schwartz–Zippel kết hợp với nhau tạo nên một thuật toán streaming hoàn chỉnh cho bài toán
     liên thông đồ thị động.</p>""")]),
 ],
 quiz=[
  dict(q="Một đa thức khác 0 bậc $d$ trên $\\mathbb F_p$ có tối đa bao nhiêu nghiệm?",
   opts=["$p$", "$d$", "$p/d$", "$d^2$"], correct=1,
   explain="Đây là tính chất đại số cơ bản: số nghiệm không vượt quá bậc đa thức."),
  dict(q="Bổ đề Schwartz–Zippel cho chặn nào về xác suất $z$ ngẫu nhiên là nghiệm của đa thức khác 0 bậc $d$?",
   opts=["$\\le d/p$", "$= 1$", "$\\ge d/p$", "$\\le p/d$"], correct=0,
   explain="Chọn z ngẫu nhiên đều trong F_p, xác suất trúng 1 trong tối đa d nghiệm là ≤ d/p."),
  dict(q="Trong SupportFind, nếu $x=v\\cdot e_j$, công thức nào cho $j$ từ $s_0,s_1$?",
   opts=["$j=s_0/s_1$", "$j=s_1/s_0$", "$j=s_0\\cdot s_1$", "$j=s_1-s_0$"], correct=1,
   explain="s0=v, s1=j·v, nên j = s1/s0 (chia được vì đang làm việc trên trường F_p)."),
  dict(q="Vai trò của phép kiểm tra $s_2\\overset?=s_0z^j$ trong SupportFind là gì?",
   opts=["Tính lại giá trị v","Xác nhận giả thuyết x thực sự 1-thưa, với xác suất báo nhầm bị chặn bởi Schwartz–Zippel","Tìm hàm băm mới","Không có vai trò gì đặc biệt"],
   correct=1, explain="Đây là bước kiểm chứng bắt buộc — nếu x không 1-thưa, xác suất s2 vẫn khớp (báo nhầm) là ≤ n/p."),
  dict(q="Đa thức trên $\\mathbb F_p$ xuất hiện ở những vai trò nào xuyên suốt môn học?",
   opts=["Chỉ dùng cho SupportFind","Xây hàm băm k-wise independent (buổi 11) VÀ kiểm tra đẳng thức trong SupportFind (buổi 14)","Chỉ dùng cho CountMin","Không liên quan gì đến các buổi khác"],
   correct=1, explain="Đây chính là điểm hội tụ khép vòng của môn học: cùng một công cụ toán học (đa thức trên F_p) phục vụ 2 mục đích khác nhau."),
 ]),
]
