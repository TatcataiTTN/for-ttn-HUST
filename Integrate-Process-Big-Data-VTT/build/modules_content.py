# -*- coding: utf-8 -*-
"""Nội dung lý thuyết + quiz cho 5 module của môn IT5427 - Tích hợp và xử lý dữ liệu lớn
(HUST, giảng viên Vũ Tuyết Trinh). Nội dung viết lại từ:
  - 4 file slide bài giảng gốc (1. Introduction.pdf, 2_SchemaAlignment.pdf, 2_mediationquery.pdf,
    3_RecordLinkage_ER.pdf) đã đọc trực tiếp và tóm tắt trong các phiên trước.
  - Giáo trình CHÍNH THỨC của môn (theo đề cương IT5427.pdf, mục "Text and Reading") là Dong &
    Srivastava "Big Data Integration" (Morgan & Claypool 2015) và Doan-Halevy-Ives "Principles of
    Data Integration" (Morgan Kaufmann 2012) - cả 2 đều trả phí, không có bản đầy đủ hợp pháp. Bản
    thay thế hợp pháp duy nhất tìm được: bài báo mở "Big Data Integration" (Dong & Srivastava,
    PVLDB 2013, vol.6) - cùng tác giả/tiêu đề, nội dung cô đọng từ chính cuốn sách - đã lưu tại
    Literature-Review-Papers/23_DongSrivastava2013_BigDataIntegration_PVLDB.pdf.
  - Module 00 (nền tảng) KHÔNG thuộc giáo trình chính thức môn này - viết lại bằng lời riêng từ
    kiến thức CSDL quan hệ/ER phổ thông (tương tự nội dung sách Fundamentals of Database Systems,
    Elmasri & Navathe, mà người học sẵn có) để làm tiền đề, không trích dẫn nguyên văn bất kỳ sách
    nào, không khẳng định đây là tài liệu bắt buộc của IT5427.
Mọi công thức GAV/LAV/Certain-Answers, similarity measures, Soundex... đều đúng với slide gốc,
không suy đoán thêm."""

MODULES = [
# ---------------------------------------------------------------- 0
dict(n=0, slug="00-nen-tang-csdl", title="Nền tảng: Mô hình quan hệ & Thực thể-Liên kết",
 tag="Kiến thức nền tự bổ sung — không thuộc giáo trình chính thức IT5427",
 intro="Trước khi học Tích hợp dữ liệu, cần nắm vững CSDL được mô hình hoá thế nào ở từng nguồn — "
       "đây là nền tảng để hiểu vì sao 2 nguồn 'cùng dữ liệu' lại có schema khác nhau.",
 parts=[
  dict(title="Mô hình thực thể - liên kết (ER) & mô hình quan hệ", bullets=[
    "Thực thể (entity), thuộc tính (attribute), liên kết (relationship)",
    "Khoá chính (primary key) & khoá ngoại (foreign key)",
    "Chuyển ER sang lược đồ quan hệ (bảng)"],
   slides=[
    dict(h="Vì sao cần mô hình hoá dữ liệu trước khi tích hợp?", body="""
      <p>Mỗi tổ chức thiết kế CSDL riêng để phục vụ đúng nhu cầu của họ — cùng biểu diễn "một căn hộ cho thuê"
      nhưng hệ thống A có thể gộp 1 bảng, hệ thống B tách thành 3 bảng liên kết nhau. <b>Mô hình Thực thể -
      Liên kết (Entity-Relationship, ER)</b> là ngôn ngữ chung để mô tả ý định thiết kế đó trước khi hiện
      thực hoá thành bảng quan hệ (relational schema).</p>
      <ul class="pd-legend">
      <li><b>Thực thể (Entity)</b><span>một đối tượng thế giới thực cần lưu trữ, VD "Căn hộ", "Người thuê"</span></li>
      <li><b>Thuộc tính (Attribute)</b><span>đặc điểm mô tả thực thể, VD diện tích, giá thuê</span></li>
      <li><b>Liên kết (Relationship)</b><span>quan hệ giữa 2+ thực thể, VD "Người thuê — Thuê — Căn hộ"</span></li>
      </ul>"""),
    dict(h="Khoá chính & khoá ngoại — nền tảng của mọi phép Join", body="""
      <p>Khi chuyển ER sang bảng quan hệ, mỗi thực thể thành 1 bảng với 1 <b>khoá chính</b> (primary key)
      định danh duy nhất mỗi dòng. Một liên kết được hiện thực bằng <b>khoá ngoại</b> (foreign key) — cột
      ở bảng này trỏ tới khoá chính bảng kia.</p>
      <div class="callout good"><div class="lbl">Vì sao quan trọng cho môn Tích hợp dữ liệu</div>
      Toàn bộ kỹ thuật <b>Record Linkage</b> (buổi 4) thực chất là đi tìm lại "khoá chính ngầm" giữa 2 nguồn
      không hề chia sẻ cùng 1 khoá ngoại thật — vì chúng được thiết kế độc lập với nhau.</div>""")]),
  dict(title="Chuẩn hoá & dị biệt thiết kế", bullets=[
    "Chuẩn hoá (normalization) giảm dư thừa dữ liệu",
    "Cùng 1 miền dữ liệu, nhiều cách thiết kế hợp lệ khác nhau",
    "Đây chính là nguồn gốc của Schema Heterogeneity (buổi 2)"],
   slides=[
    dict(h="Chuẩn hoá tạo ra sự đa dạng thiết kế hợp lệ", body="""
      <p>Chuẩn hoá (1NF → 2NF → 3NF...) nhằm giảm dị thường cập nhật/dư thừa dữ liệu — nhưng đồng thời khiến
      2 đội thiết kế độc lập, cùng chuẩn hoá đúng kỹ thuật, vẫn ra <b>2 lược đồ khác nhau</b> cho cùng 1 miền
      dữ liệu: 1 bên tách bảng Địa chỉ riêng, bên kia gộp vào bảng chính.</p>
      <div class="callout warn"><div class="lbl">Cầu nối sang buổi 2</div>
      "Chuẩn hoá đúng kỹ thuật ở từng nguồn" không có nghĩa "dễ tích hợp giữa các nguồn" — đây chính là lý do
      Data Integration là một bài toán riêng, không tự động giải quyết chỉ bằng thiết kế CSDL tốt.</div>""")]),
 ],
 quiz=[
  dict(q="Trong mô hình ER, 'Người thuê — Thuê — Căn hộ' thuộc loại thành phần nào?",
   opts=["Thực thể (Entity)","Thuộc tính (Attribute)","Liên kết (Relationship)","Khoá ngoại"], correct=2,
   explain="Đây là quan hệ nối 2 thực thể (Người thuê, Căn hộ) — đúng định nghĩa Relationship trong ER."),
  dict(q="Khoá ngoại (foreign key) dùng để làm gì?",
   opts=["Định danh duy nhất 1 dòng trong chính bảng đó","Trỏ tới khoá chính của bảng khác để hiện thực liên kết",
         "Tăng tốc độ truy vấn","Mã hoá dữ liệu nhạy cảm"], correct=1,
   explain="Khoá ngoại là cột tham chiếu khoá chính ở bảng khác — cơ chế hiện thực Relationship bằng bảng quan hệ."),
  dict(q="Vì sao 2 hệ thống cùng chuẩn hoá đúng kỹ thuật vẫn có thể ra lược đồ khác nhau?",
   opts=["Vì 1 trong 2 bên làm sai","Chuẩn hoá không duy nhất — nhiều cách tách bảng hợp lệ cho cùng miền dữ liệu",
         "Vì dùng hệ quản trị CSDL khác nhau","Vì dữ liệu khác nhau"], correct=1,
   explain="Chuẩn hoá đảm bảo không dư thừa/dị thường, nhưng không ép buộc duy nhất 1 cách tách bảng — đây là gốc rễ của Structural Heterogeneity."),
 ]),

# ---------------------------------------------------------------- 1
dict(n=1, slug="01-data-integration-overview", title="Data Integration — Tổng quan & Dị biệt dữ liệu",
 tag="Buổi 2 — Nền tảng",
 intro="Data Integration là lớp trừu tượng bậc cao hơn DBMS: cho người dùng 1 giao diện truy vấn thống nhất "
       "tới nhiều nguồn dữ liệu độc lập, dù chúng khác nhau ở mọi tầng — từ hệ thống tới ngữ nghĩa.",
 parts=[
  dict(title="Data Integration là gì", bullets=[
    "DBMS = trừu tượng hoá logic/vật lý; Data Integration = trừu tượng hoá bậc cao hơn",
    "Mediated Schema — giao diện thống nhất duy nhất người dùng nhìn thấy",
    "Wrapper — cầu nối giữa truy vấn và dữ liệu nguồn thật"],
   slides=[
    dict(h="Data Integration: một tầng trừu tượng mới", body="""
      <p>DBMS cho ta trừu tượng <i>logical vs physical</i> — người dùng viết SQL mà không cần biết dữ liệu lưu
      trên đĩa ra sao. <b>Data Integration</b> đi xa hơn: cho người dùng 1 giao diện truy vấn duy nhất
      (<b>Mediated Schema</b>) mà không cần biết dữ liệu thật nằm ở nguồn nào, mô hình gì, viết bằng ngôn ngữ gì.</p>
      <div class="callout good"><div class="lbl">3 thứ Mediated Schema giúp "độc lập"</div>
      Vị trí &amp; nơi lưu trữ nguồn · Mô hình dữ liệu &amp; cú pháp (SQL/XML/JSON...) · Biến thể ngữ nghĩa
      giữa các nguồn.</div>"""),
    dict(h="Wrapper — nơi 'dịch' truy vấn thành thao tác thật", body="""
      <p>Khi truy vấn trên Mediated Schema được viết lại (reformulate) thành truy vấn con cho từng nguồn,
      <b>Wrapper</b> là thành phần thực sự gửi thao tác đó tới nguồn (gọi API, chạy SQL cục bộ, parse HTML...),
      rồi chuyển kết quả trả về đúng mô hình dữ liệu nội bộ của hệ thống tích hợp.</p>
      <div class="pd-formula"><div class="pd-formula-label">Pipeline Query Processing</div>
      <div class="pd-formula-math">Query &rarr; Query Reformulation &rarr; Query Optimizer &rarr; Execution Engine &rarr; Wrapper(s) &rarr; Sources</div></div>""")]),
  dict(title="7 mức độ Heterogeneity", bullets=[
    "System/Platform · Syntactic/Format · Structural/Schema",
    "Semantic/Conceptual · Instance/Identity",
    "Temporal/Process · Quality/Provenance/Governance"],
   slides=[
    dict(h="Dị biệt không chỉ là 'khác định dạng file'", body="""
      <p>Slide gốc chia dị biệt giữa các nguồn thành <b>7 tầng</b>, từ thấp tới cao:</p>
      <ul class="pd-legend">
      <li><b>1. System/Platform</b><span>dữ liệu lưu ở đâu, truy cập bằng cách nào (SQL JDBC, Document API, Kafka topic...)</span></li>
      <li><b>2. Syntactic/Format</b><span>định dạng file, encoding, cú pháp ngày/số (vd "2026-09-15" vs "15/09/26")</span></li>
      <li><b>3. Structural/Schema</b><span>bảng, thuộc tính, khoá, độ chi tiết (granularity) khác nhau</span></li>
      <li><b>4. Semantic/Conceptual</b><span>đồng nghĩa (synonym), đa nghĩa (homonym) — cần ontology để giải quyết</span></li>
      </ul>"""),
    dict(h="3 tầng còn lại — thường bị bỏ sót", body="""
      <ul class="pd-legend">
      <li><b>5. Instance/Identity</b><span>cùng 1 thực thể thật xuất hiện khác nhau ở 2 nguồn — giải quyết bằng
      <b>Entity Resolution/Record Linkage</b> (buổi 4)</span></li>
      <li><b>6. Temporal/Process</b><span>tần suất cập nhật khác nhau, dữ liệu "mới nhất" ở nguồn này có thể cũ hơn nguồn kia</span></li>
      <li><b>7. Quality/Provenance/Governance</b><span>độ tin cậy, nguồn gốc, quyền truy cập dữ liệu khác nhau giữa các nguồn</span></li>
      </ul>
      <div class="callout warn"><div class="lbl">Khung quan trọng nhất môn học</div>
      3 buổi tiếp theo lần lượt giải quyết đúng các tầng này: buổi 3 giải quyết tầng 3-4 (Schema Alignment),
      buổi 4 giải quyết tầng 5 (Record Linkage) — rồi tới Data Fusion xử lý xung đột giá trị khi đã gộp.</div>""")]),
  dict(title="Kiến trúc: Virtual vs. Warehouse", bullets=[
    "Virtual Integration — truy vấn thời gian thực qua wrapper, dữ liệu ở nguyên nguồn",
    "Data Warehousing — copy định kỳ (ETL) về kho tập trung",
    "5V của Big Data & pipeline 3 bước tổng thể"],
   slides=[
    dict(h="Virtual Integration vs. Data Warehousing", body="""
      <table class="pd-table"><tr><th></th><th>Virtual</th><th>Warehouse</th></tr>
      <tr><td>Dữ liệu ở đâu</td><td>Vẫn ở nguồn gốc</td><td>Copy về kho tập trung (ETL)</td></tr>
      <tr><td>Độ mới</td><td>Luôn mới nhất (query-time)</td><td>Có độ trễ theo chu kỳ ETL</td></tr>
      <tr><td>Ảnh hưởng nguồn</td><td>Mỗi truy vấn làm phiền nguồn gốc</td><td>Không làm phiền sau khi đã copy</td></tr>
      <tr><td>Tính toán nặng</td><td>Khó (giới hạn bởi nguồn)</td><td>Dễ (data mining, ML trên kho)</td></tr></table>"""),
    dict(h="5V & pipeline tổng thể của môn học", body="""
      <p><b>Volume · Velocity · Variety · Veracity · Value</b> — 5 tiêu chí định nghĩa Big Data. Toàn bộ nội
      dung môn học đi theo đúng 1 pipeline 3 bước xử lý Big Data Integration:</p>
      <div class="pd-formula"><div class="pd-formula-label">Pipeline tổng thể</div>
      <div class="pd-formula-math">Schema Alignment &rarr; Entity Resolution &rarr; Data Fusion</div></div>
      <div class="callout good"><div class="lbl">Đây chính là 3 buổi học tiếp theo</div>
      Buổi 3: Schema Alignment (GAV/LAV/GLAV). Buổi 4: Entity Resolution (Record Linkage). Data Fusion
      (Survivorship Rule) là bước ứng dụng cụ thể khi làm project.</div>""")]),
 ],
 quiz=[
  dict(q="Mediated Schema giúp người dùng độc lập với điều gì?",
   opts=["Chỉ vị trí lưu trữ nguồn","Vị trí, mô hình/cú pháp dữ liệu, và biến thể ngữ nghĩa giữa các nguồn",
         "Chỉ tốc độ mạng","Chỉ giá dịch vụ cloud"], correct=1,
   explain="Slide liệt kê rõ 3 thứ: source & location, data model & syntax, semantic variations."),
  dict(q="Wrapper nằm ở vị trí nào trong pipeline Query Processing?",
   opts=["Trước Query Reformulation","Giữa Query Optimizer và Execution Engine",
         "Sau Execution Engine, kết nối trực tiếp tới từng nguồn","Không thuộc pipeline này"], correct=2,
   explain="Pipeline: Query → Reformulation → Optimizer → Execution Engine → Wrapper(s) → Sources."),
  dict(q="Hai nguồn cùng lưu 'căn hộ cho thuê' nhưng 1 bên tách riêng bảng Địa chỉ, bên kia gộp chung — đây là dị biệt tầng nào?",
   opts=["Syntactic/Format","Structural/Schema","Semantic/Conceptual","Temporal/Process"], correct=1,
   explain="Khác biệt về tổ chức bảng/độ chi tiết = Structural/Schema Heterogeneity (tầng 3)."),
  dict(q="'Apartment' và 'Flat' cùng nghĩa nhưng viết khác nhau ở 2 nguồn — đây là dị biệt tầng nào?",
   opts=["Structural/Schema","Instance/Identity","Semantic/Conceptual (đồng nghĩa)","System/Platform"], correct=2,
   explain="Đồng nghĩa (synonym) giữa các thuật ngữ là ví dụ kinh điển của Semantic/Conceptual Heterogeneity."),
  dict(q="Cùng 1 căn hộ thật bị đăng tin ở 2 website khác nhau, không có ID chung — đây là dị biệt tầng nào, và buổi học nào giải quyết?",
   opts=["Structural, buổi 3","Instance/Identity, buổi 4","Temporal, không buổi nào giải quyết","Quality, buổi 2"], correct=1,
   explain="Đây đúng định nghĩa Instance/Identity Heterogeneity — giải quyết bằng Record Linkage/Entity Resolution ở buổi 4."),
  dict(q="Ưu điểm chính của Data Warehousing so với Virtual Integration là gì?",
   opts=["Dữ liệu luôn mới nhất","Không cần thiết kế lược đồ vật lý",
         "Có thể chạy tính toán nặng (data mining/ML) mà không làm phiền nguồn gốc mỗi lần",
         "Không cần ETL"], correct=2,
   explain="Vì dữ liệu đã copy về kho, có thể chạy tính toán nặng tuỳ ý trên bản copy, không đụng tới nguồn gốc."),
 ]),

# ---------------------------------------------------------------- 2
dict(n=2, slug="02-schema-alignment", title="Schema Alignment — GAV, LAV, GLAV & Certain Answers",
 tag="Buổi 3a — Lý thuyết Schema Mapping",
 intro="Làm sao viết truy vấn trên Mediated Schema rồi 'dịch' đúng thành truy vấn thật trên các nguồn? "
       "3 ngôn ngữ mapping GAV/LAV/GLAV trả lời câu hỏi này theo 3 cách khác nhau.",
 parts=[
  dict(title="Certain Answers — định nghĩa 'câu trả lời đúng'", bullets=[
    "Possible Instances — các instance mediated schema khả dĩ với dữ liệu nguồn hiện có",
    "Certain Answer = đúng trong MỌI possible instance",
    "Open-world vs Closed-world assumption"],
   slides=[
    dict(h="Vì sao cần khái niệm Certain Answers?", body="""
      <p>Khi nhiều nguồn khác nhau map vào cùng Mediated Schema, có thể tồn tại <b>nhiều instance khả dĩ</b>
      (possible instances) của Mediated Schema đều nhất quán với dữ liệu nguồn + mapping đã cho. Câu hỏi đặt
      ra: trả lời truy vấn dựa trên instance nào?</p>
      <div class="pd-formula"><div class="pd-formula-label">Certain Answer</div>
      <div class="pd-formula-math">$t \\in Q(s_1,...,s_n)$ iff $t \\in Q(g)$ với $\\forall g$ sao cho $(g,s_1,...,s_n) \\in M_R$</div></div>
      <div class="callout good"><div class="lbl">Nói đơn giản</div>
      Chỉ coi 1 dòng kết quả là "chắc chắn đúng" nếu nó đúng trong <b>MỌI</b> instance mediated schema khả dĩ —
      không phải chỉ 1 instance cụ thể nào.</div>"""),
    dict(h="Ví dụ: Director có là Certain Answer không?", body="""
      <p>Nguồn chỉ có (Title, Year), Mediated Schema cần (Director, Title, Year). Có 2 instance khả dĩ:
      {(Allen, Manhattan, 1979), (Coppola, GodFather, 1972)} và {(Halevy, Manhattan, 1979), (Stonebraker,
      GodFather, 1972)}.</p>
      <div class="callout warn"><div class="lbl">Kết quả</div>
      Truy vấn "trả về mọi năm phim" → (1979, 1972) là <b>certain answer</b> (đúng ở cả 2 instance). Truy vấn
      "trả về mọi đạo diễn" → <b>không có certain answer</b> nào, vì không đạo diễn nào xuất hiện ở cả 2
      instance.</div>""")]),
  dict(title="GAV — Global-as-View", bullets=[
    "Mediated schema = 1 view trên các nguồn: $G \\supseteq Q(sources)$",
    "Reformulation = Query Unfolding (thay subgoal bằng rule, lặp tới hết)",
    "Nhanh, đơn giản — nhưng cứng nhắc, không biểu diễn được thông tin thiếu"],
   slides=[
    dict(h="GAV: định nghĩa & công thức", body="""
      <p>Trong GAV, mỗi quan hệ của Mediated Schema được định nghĩa <b>là 1 view</b> (truy vấn) trên các
      nguồn — giống hệt cách bạn viết 1 SQL VIEW gộp nhiều bảng nguồn lại.</p>
      <div class="pd-formula"><div class="pd-formula-label">GAV — dạng tổng quát</div>
      <div class="pd-formula-math">$G_i(\\bar X) \\supseteq Q(\\bar S)$ &nbsp; (open-world) &nbsp;hoặc&nbsp; $G_i(\\bar X) = Q(\\bar S)$ &nbsp;(closed-world)</div></div>
      <p>Ví dụ: <code>Movie(title,director,year,genre) ⊇ S1.Movie(MID,title), S1.MovieDetail(MID,director,genre,year)</code></p>"""),
    dict(h="Reformulation trong GAV = Query Unfolding", body="""
      <p>Vì mediated schema đã được định nghĩa thẳng bằng truy vấn trên nguồn, reformulate 1 truy vấn Q trên
      mediated schema chỉ đơn giản là <b>thay từng subgoal bằng định nghĩa GAV tương ứng</b>, lặp tới khi hết.</p>
      <div class="callout warn"><div class="lbl">Nhược điểm cốt lõi của GAV</div>
      Cứng nhắc — ép mọi nguồn vào đúng 1 "góc nhìn" của mediated schema, không biểu diễn được trường hợp
      nguồn chỉ biết 1 phần thông tin (incomplete information). Thêm nguồn mới = phải viết lại định nghĩa
      mediated schema.</div>""")]),
  dict(title="LAV — Local-as-View & GLAV", bullets=[
    "LAV: mỗi nguồn = 1 view trên mediated schema: $S_i \\subseteq Q_i(G)$",
    "Reformulation LAV = 'Answering Queries Using Views' (khó hơn GAV)",
    "GLAV kết hợp cả 2, biểu diễn bằng Tuple Generating Dependency (TGD)"],
   slides=[
    dict(h="LAV: linh hoạt hơn nhưng khó reformulate hơn", body="""
      <p>Ngược lại GAV: mỗi <b>nguồn</b> được định nghĩa là 1 view trên mediated schema.</p>
      <div class="pd-formula"><div class="pd-formula-label">LAV — dạng tổng quát</div>
      <div class="pd-formula-math">$S_i(\\bar X) \\subseteq Q_i(G)$</div></div>
      <div class="callout good"><div class="lbl">Ưu điểm</div>
      Thêm/bớt nguồn chỉ cần thêm/bớt 1 định nghĩa LAV, không đụng tới mediated schema — và LAV biểu diễn
      được thông tin không đầy đủ (GAV thì không).</div>
      <div class="callout warn"><div class="lbl">Đánh đổi</div>
      Reformulate trở thành bài toán <b>Answering Queries Using Views</b> — khó hơn unfolding nhiều, dùng kỹ
      thuật Inverse Rules (suy ngược định nghĩa view ra rule rồi mới unfold được).</div>"""),
    dict(h="GLAV — kết hợp cả hai bằng Tuple Generating Dependency", body="""
      <div class="pd-formula"><div class="pd-formula-label">GLAV</div>
      <div class="pd-formula-math">$Q^S(\\bar X) \\subseteq Q^G(\\bar X)$ &nbsp;—&nbsp; tương đương TGD:
      $(\\forall \\bar X)\\, s_1(\\bar X_1),...,s_m(\\bar X_m) \\to (\\exists \\bar Y)\\, t_1(\\bar Y_1),...,t_k(\\bar Y_k)$</div></div>
      <table class="pd-table"><tr><th>Tiêu chí</th><th>GAV</th><th>LAV</th><th>GLAV</th></tr>
      <tr><td>Reformulation</td><td>Dễ (unfolding)</td><td>Khó (views)</td><td>Khó (views)</td></tr>
      <tr><td>Biểu diễn incomplete info</td><td>Không</td><td>Có</td><td>Có</td></tr>
      <tr><td>Thêm nguồn mới</td><td>Sửa mediated schema</td><td>Chỉ thêm định nghĩa</td><td>Chỉ thêm định nghĩa</td></tr></table>""")]),
 ],
 quiz=[
  dict(q="Certain Answer được định nghĩa thế nào?",
   opts=["Đúng ở ít nhất 1 instance khả dĩ của mediated schema","Đúng ở MỌI instance khả dĩ của mediated schema",
         "Đúng ở instance được chọn ngẫu nhiên","Đúng khi không có nguồn nào mâu thuẫn"], correct=1,
   explain="Certain = chắc chắn đúng trong tất cả các khả năng, không chỉ 1 trường hợp cụ thể."),
  dict(q="Trong GAV, mediated schema được định nghĩa như thế nào?",
   opts=["Là 1 view trên các nguồn","Các nguồn là view trên mediated schema",
         "Cả 2 chiều đều là truy vấn (TGD)","Không có định nghĩa hình thức"], correct=0,
   explain="GAV = Global-as-View: global/mediated schema ĐƯỢC ĐỊNH NGHĨA LÀ view trên nguồn."),
  dict(q="Reformulation trong GAV dùng thuật toán nào?",
   opts=["Inverse Rules","Query Unfolding — thay subgoal bằng rule, lặp tới hết",
         "Correlation Clustering","Locality-Sensitive Hashing"], correct=1,
   explain="GAV reformulate bằng Unfolding: đơn giản vì mediated schema đã định nghĩa thẳng bằng nguồn."),
  dict(q="Nhược điểm cốt lõi của GAV so với LAV là gì?",
   opts=["GAV luôn chậm hơn khi thực thi","GAV không biểu diễn được thông tin nguồn không đầy đủ (incomplete information)",
         "GAV không dùng được SQL","GAV chỉ hoạt động với 1 nguồn duy nhất"], correct=1,
   explain="GAV ép mọi nguồn vào đúng 1 view cố định — không biểu diễn được trường hợp nguồn chỉ biết 1 phần."),
  dict(q="Reformulation trong LAV tương đương với bài toán kinh điển nào?",
   opts=["Query Unfolding","Answering Queries Using Views","Correlation Clustering","Entity Resolution"], correct=1,
   explain="Vì nguồn là view trên mediated schema, trả lời truy vấn trên mediated schema = trả lời bằng các view đã có — đúng định nghĩa bài toán này."),
  dict(q="GLAV biểu diễn hình thức bằng công cụ nào?",
   opts=["Chỉ dùng SQL thuần","Tuple Generating Dependency (TGD)","Hash function","Decision Tree"], correct=1,
   explain="GLAV tương đương 1 TGD: vế trái (nguồn) kéo theo sự tồn tại dữ liệu thoả vế phải (mediated schema)."),
 ]),

# ---------------------------------------------------------------- 3
dict(n=3, slug="03-mediation-query-bigdata", title="Mediation Query bán cấu trúc & Big Data Integration Challenges",
 tag="Buổi 3b — Mở rộng",
 intro="Khi dữ liệu là XML/semi-structured, không thể chỉ viết 1 câu GAV đơn giản — cần decompose schema "
       "thành sub-trees. Và khi số nguồn lên tới hàng triệu, cả GAV lẫn LAV truyền thống đều vỡ trận.",
 parts=[
  dict(title="Sinh Mediation Query cho dữ liệu bán cấu trúc", bullets=[
    "Decompose mediation schema thành sub-trees",
    "Partial Mapping — ánh xạ 1 sub-tree với 1 nguồn cụ thể",
    "Join Graph & kết hợp các partial mapping thành mediation query hoàn chỉnh"],
   slides=[
    dict(h="Vì sao XML/semi-structured khó hơn quan hệ?", body="""
      <p>Với dữ liệu quan hệ, 1 câu GAV map thẳng 1 bảng mediated vào biểu thức trên bảng nguồn. Với cây XML
      lồng nhau nhiều cấp, không có "1 bảng" để map — phải <b>decompose mediation schema thành các sub-tree</b>
      (root là node đa trị hoặc gốc cây, lá phải có ít nhất 1 text node), rồi xử lý từng sub-tree riêng.</p>"""),
    dict(h="Partial Mapping → Join Graph → Mediation Query", body="""
      <p>Quy trình 3 bước: (1) Với mỗi sub-tree, tìm phần tương ứng ở từng nguồn (<b>partial mapping</b>).
      (2) Tìm các phép join khả dĩ giữa các nguồn dựa trên key/reference-key, tạo thành <b>join graph</b>
      (node = nguồn, cạnh = điều kiện join). (3) Kết hợp các partial mapping (mỗi sub-tree 1 cái) thành 1
      <b>mediation query</b> hoàn chỉnh — hợp hai mediation query cũng tạo ra 1 mediation query mới.</p>
      <div class="callout good"><div class="lbl">Kết quả</div>
      Output cuối là 1 truy vấn XQuery thực thi được, sinh ra cây XML đúng cấu trúc mediation schema từ
      nhiều nguồn XML rời rạc.</div>""")]),
  dict(title="Vì sao tích hợp truyền thống 'vỡ trận' ở quy mô Big Data", bullets=[
    "Deep Web at Scale, Schema Explosion, Keyword Queries không có schema cố định",
    "GAV/LAV đòi hỏi mapping chính xác — không khả thi với hàng triệu nguồn",
    "PAYGO: bắt đầu lỏng lẻo, cải thiện dần theo thời gian"],
   slides=[
    dict(h="4 lý do Data Integration truyền thống không đủ", body="""
      <ul class="pd-legend">
      <li><b>Deep Web at Scale</b><span>hàng chục triệu nguồn ẩn sau form web — không thể thiết kế mapping thủ công cho từng nguồn</span></li>
      <li><b>Schema Explosion</b><span>hàng trăm nghìn schema khác nhau cùng miền dữ liệu ("database design by the masses")</span></li>
      <li><b>Modeling Everything</b><span>dữ liệu trải khắp mọi lĩnh vực tri thức loài người — 1 mediated schema duy nhất là bất khả thi</span></li>
      <li><b>Keyword Queries</b><span>người dùng web gõ từ khoá, không viết SQL theo đúng mediated schema nào cả</span></li>
      </ul>"""),
    dict(h="PAYGO — Pay-As-You-Go Integration", body="""
      <p>Thay vì thiết kế mediated schema + mapping hoàn chỉnh trước (như GAV/LAV truyền thống), PAYGO bắt
      đầu với rất ít ràng buộc ngữ nghĩa, trả lời truy vấn "tốt nhất có thể" với những gì đã biết, rồi
      <b>cải thiện dần</b> theo thời gian/phản hồi người dùng.</p>
      <table class="pd-table"><tr><th>Traditional DI</th><th>PAYGO</th></tr>
      <tr><td>Single Mediated Schema (thiết kế thủ công)</td><td>Schema Clusters (tự động theo chủ đề)</td></tr>
      <tr><td>Exact Schema Mappings</td><td>Approximate/Probabilistic Mappings</td></tr>
      <tr><td>Structured Queries (SQL)</td><td>Keyword Queries + Routing</td></tr>
      <tr><td>Deterministic Answers</td><td>Heterogeneous Ranking (best-effort)</td></tr></table>""")]),
  dict(title="Dataspace, Probabilistic Schema & WebTables", bullets=[
    "Dataspace/DSSP — mô hình thay thế khi không đủ thời gian thiết kế mediated schema",
    "Probabilistic Mediated Schema — tạo tự động bằng clustering, kèm xác suất",
    "WebTables — tích hợp không cần mediated schema tường minh, dùng keyword search + ranking"],
   slides=[
    dict(h="Probabilistic Mediated Schema & Mapping", body="""
      <p>Thay vì 1 mediated schema "đúng duy nhất", hệ thống tạo <b>nhiều phiên bản khả dĩ</b> bằng clustering
      thuộc tính các nguồn, mỗi phiên bản kèm 1 trọng số xác suất. Tương tự, mỗi mapping cũng có nhiều khả
      năng kèm xác suất tin cậy — mô hình hoá đúng sự không chắc chắn (uncertainty) ở cả 2 tầng.</p>"""),
    dict(h="WebTables — khai thác 154 triệu bảng chất lượng cao trên Web", body="""
      <p>Không xây mediated schema, WebTables trích xuất hàng tỷ bảng HTML, lọc ra các bảng quan hệ chất
      lượng cao bằng phân loại thống kê, rồi <b>xếp hạng theo từ khoá người dùng gõ</b> (FeatureRank dùng đặc
      trưng bảng; SchemaRank cộng thêm độ nhất quán schema qua Pointwise Mutual Information).</p>
      <div class="callout good"><div class="lbl">Ý nghĩa</div>
      Đây là minh chứng PAYGO hoạt động thực tế ở quy mô Web — "tích hợp" bằng tìm-kiếm-và-xếp-hạng thay vì
      mapping tường minh.</div>""")]),
 ],
 quiz=[
  dict(q="Khi decompose mediation schema XML thành sub-tree, điều kiện bắt buộc của mỗi sub-tree là gì?",
   opts=["Phải có đúng 1 node","Root là node đa trị hoặc gốc cây, và có ít nhất 1 text node trong sub-tree",
         "Không được chứa thuộc tính nào","Phải trùng khớp hoàn toàn 1 nguồn"], correct=1,
   explain="Slide định nghĩa rõ: root = multi-value node hoặc root của mediation schema; node mono-value; có ít nhất 1 text node."),
  dict(q="Join Graph trong sinh mediation query dùng để làm gì?",
   opts=["Biểu diễn các phép join khả dĩ giữa các nguồn dựa trên key/reference-key",
         "Tối ưu hoá tốc độ mạng","Mã hoá dữ liệu","Chuẩn hoá bảng"], correct=0,
   explain="Node = nguồn, cạnh = điều kiện join (VD authorId=id) — dùng để kết hợp các partial mapping."),
  dict(q="'Schema Explosion' trong Big Data Integration nghĩa là gì?",
   opts=["Dữ liệu bị mất do lỗi hệ thống","Hàng trăm nghìn schema khác nhau cùng tồn tại cho cùng 1 miền dữ liệu",
         "Mediated schema tự động xoá","Tốc độ truy vấn giảm"], correct=1,
   explain="'Database design by the masses' tạo ra vô số schema khác nhau cho cùng ý tưởng — không thể gộp thủ công."),
  dict(q="Nguyên lý cốt lõi của PAYGO là gì?",
   opts=["Thiết kế mediated schema hoàn chỉnh trước khi dùng","Bắt đầu với ít ràng buộc ngữ nghĩa, cải thiện dần theo thời gian/phản hồi",
         "Chỉ dùng được với dữ liệu quan hệ","Yêu cầu toàn bộ nguồn phải có cùng schema"], correct=1,
   explain="Pay-As-You-Go: trả lời tốt nhất có thể ngay từ đầu, tự động cải thiện mapping dần, không chờ thiết kế hoàn chỉnh."),
  dict(q="Probabilistic Mediated Schema được tạo ra bằng cách nào?",
   opts=["Chuyên gia thiết kế thủ công","Clustering tự động các thuộc tính nguồn, kèm xác suất cho mỗi phiên bản",
         "Dịch máy","Random ngẫu nhiên hoàn toàn"], correct=1,
   explain="Tạo tự động bằng clustering thuộc tính — do Volume/Variety quá lớn để thiết kế thủ công."),
  dict(q="SchemaRank trong WebTables khác FeatureRank ở điểm nào?",
   opts=["SchemaRank không dùng máy học","SchemaRank cộng thêm đo độ nhất quán schema qua Pointwise Mutual Information",
         "SchemaRank chỉ dùng cho bảng tiếng Anh","SchemaRank chậm hơn nhưng không chính xác hơn"], correct=1,
   explain="SchemaRank = FeatureRank + đo coherence giữa các thuộc tính bằng pmi(a,b), cải thiện chất lượng xếp hạng đo được trong slide."),
 ]),

# ---------------------------------------------------------------- 4
dict(n=4, slug="04-record-linkage-entity-resolution", title="Record Linkage & Entity Resolution",
 tag="Buổi 4 — Thực hành nhiều nhất",
 intro="Cùng 1 thực thể thật xuất hiện khác nhau ở nhiều nguồn — làm sao máy tính nhận ra 'David Smith' và "
       "'Davod Smith' là cùng 1 người, ở quy mô hàng triệu bản ghi, không thể so từng cặp thủ công? "
       "Slide gốc buổi này trích dẫn <i>Dong &amp; Srivastava, Big Data Integration, Chapter 3</i> làm "
       "nguồn chính — xem bản mở tương đương (PVLDB 2013) trong mục Tài liệu tham khảo cuối trang.",
 parts=[
  dict(title="Đặt vấn đề & Similarity Measures", bullets=[
    "Record Linkage, Entity Resolution, Entity Linking — phân biệt 3 khái niệm",
    "Similarity measure s(x,y) ∈ [0,1] — càng cao càng giống",
    "Edit Distance, Jaccard, TF/IDF, Soundex"],
   slides=[
    dict(h="Record Linkage vs. Entity Resolution vs. Entity Linking", body="""
      <ul class="pd-legend">
      <li><b>Record Linkage</b><span>tìm cặp bản ghi ở 2 file khác nhau đại diện cùng 1 thực thể</span></li>
      <li><b>Entity Resolution (ER)</b><span>trường hợp đặc biệt của Entity Linking — khử trùng lặp (có thể trong cùng 1 file)</span></li>
      <li><b>Entity Linking</b><span>khái niệm rộng hơn — tạo liên kết giữa các bản ghi có liên quan (không nhất thiết "là 1")</span></li>
      </ul>
      <div class="callout warn"><div class="lbl">Fellegi &amp; Sunter (1969)</div>
      3 kết luận khi so 1 cặp bản ghi: <b>match</b>, <b>non-match</b>, hoặc <b>possible-match</b> (chưa đủ bằng chứng).</div>"""),
    dict(h="Edit Distance (Levenshtein) — tính bằng Dynamic Programming", body="""
      <div class="pd-formula"><div class="pd-formula-label">Edit Distance</div>
      <div class="pd-formula-math">$d(i,j) = \\min\\{d(i-1,j-1)+c(x_i,y_j),\\; d(i-1,j)+1,\\; d(i,j-1)+1\\}$</div></div>
      <p>Ví dụ: <code>color</code> → <code>colour</code> chỉ cần <b>1 phép chèn</b> (thêm 'u') ⟹ $d=1$.
      Similarity: $s(x,y) = 1 - d(x,y)/\\max(|x|,|y|) = 1 - 1/6 \\approx 0.833$.</p>"""),
    dict(h="Jaccard & TF/IDF — similarity dạng tập hợp", body="""
      <div class="pd-formula"><div class="pd-formula-label">Jaccard Measure</div>
      <div class="pd-formula-math">$J(x,y) = \\dfrac{|B_x \\cap B_y|}{|B_x \\cup B_y|}$</div></div>
      <p>$B_x=\\{a,b,c,d\\}$, $B_y=\\{b,c,d,e\\}$ ⟹ $J=3/5=0.6$.</p>
      <div class="callout good"><div class="lbl">Vì sao cần TF/IDF thay vì Jaccard thuần</div>
      "Apple Corporation, CA" vs "IBM Corporation, CA" vs "Apple Corp" — Jaccard thuần dễ khớp nhầm x↔y (cùng
      "Corporation, CA" phổ biến). TF/IDF cho trọng số cao hơn cho từ hiếm ("Apple") ⟹ khớp đúng x↔z.</div>"""),
    dict(h="Soundex — so khớp theo âm đọc", body="""
      <p>4 bước: (1) giữ chữ cái đầu (2) loại W/H, mã hoá chữ còn lại thành số theo nhóm âm
      (B,F,P,V=1; C,G,J,K,Q,S,X,Z=2; D,T=3; L=4; M,N=5; R=6) (3) gộp số liên tiếp trùng nhau
      (4) bỏ ký tự không phải số, lấy 4 ký tự đầu.</p>
      <div class="callout warn"><div class="lbl">Điểm yếu</div>
      Thiết kế cho tên gốc Caucasian — Soundex bỏ qua nguyên âm nên hoạt động kém với tên gốc Á Đông (vốn
      phân biệt nhau chủ yếu qua nguyên âm).</div>""")]),
  dict(title="Entity Resolution Pipeline: Prepare → Block → Match → Cluster", bullets=[
    "Blocking/Sorting — giảm O(n²) xuống khả thi",
    "Matching — threshold hoặc Learned Matchers (ML/Deep Learning)",
    "Clustering — Connected Components, Correlation Clustering, Markov Clustering"],
   slides=[
    dict(h="Blocking/Sorting: Naïve All-Pairs quá chậm", body="""
      <p>So mọi cặp có thể là $O(n^2)$ — không khả thi ở quy mô lớn. 2 kỹ thuật chính:</p>
      <ul class="pd-legend">
      <li><b>Sorted Neighborhood</b><span>sắp xếp theo sorting key, chỉ so trong 1 cửa sổ trượt kích thước cố định</span></li>
      <li><b>LSH (Locality-Sensitive Hashing)</b><span>hash embedding bản ghi — bản ghi gần nhau rơi vào cùng bucket với xác suất cao</span></li>
      </ul>"""),
    dict(h="Matching: từ threshold tới Deep Learning", body="""
      <p>Cách đơn giản: $\\mathrm{sim}(r,r') > \\theta_h \\Rightarrow$ match. Hiện đại hơn: <b>Learned
      Matchers</b> — ML truyền thống (SVM/Random Forest/XGBoost, 2 pha: học similarity rồi học quyết định)
      hoặc Deep Learning (DeepER, Magellan) tự học biểu diễn từ dữ liệu thô, tránh phải thiết kế feature thủ công.</p>
      <div class="callout warn"><div class="lbl">Vấn đề dữ liệu gán nhãn</div>
      Nhãn khan hiếm + class skew (match ít hơn non-match rất nhiều) → cần Transfer Learning (học từ kịch bản
      nhiều dữ liệu, fine-tune ít nhãn) hoặc Active Learning (chủ động chọn cặp cần gán nhãn).</div>"""),
    dict(h="Clustering: gộp các cặp match thành 1 thực thể", body="""
      <ul class="pd-legend">
      <li><b>Connected Components</b><span>đơn giản nhất, nhưng dễ tạo cụm quá lớn do tính bắc cầu (A~B, B~C ⟹ gộp cả A,C dù không thực sự giống)</span></li>
      <li><b>Correlation Clustering</b><span>dùng cả cạnh dương lẫn âm, tối ưu toàn cục — NP-hard</span></li>
      <li><b>Markov Clustering</b><span>mô phỏng luồng ngẫu nhiên (stochastic flow) trên đồ thị</span></li>
      </ul>
      <div class="callout good"><div class="lbl">Incremental Data Deduplication</div>
      Khi có dữ liệu mới, dùng greedy update (connect/merge/split/move) trên similarity graph đã có — nhanh
      hơn nhiều so với tính lại correlation clustering từ đầu.</div>""")]),
 ],
 quiz=[
  dict(q="Theo Fellegi & Sunter (1969), khi so 1 cặp bản ghi có 3 kết luận. 'Possible-match' nghĩa là gì?",
   opts=["Chắc chắn là cùng 1 thực thể","Chắc chắn khác thực thể","Chưa đủ bằng chứng kết luận chắc chắn","Lỗi dữ liệu"], correct=2,
   explain="Possible-match = chưa đủ tin cậy để khẳng định match hay non-match, cần thêm thông tin/con người xác nhận."),
  dict(q="Edit Distance giữa 'color' và 'colour' là bao nhiêu, và vì sao?",
   opts=["0, vì giống hệt","1, chỉ cần 1 phép chèn ký tự 'u'","2, cần 2 phép biến đổi","5, bằng độ dài chuỗi ngắn hơn"], correct=1,
   explain="color → colou+r: chỉ 1 phép insert 'u'. d=1."),
  dict(q="Vì sao TF/IDF khớp đúng 'Apple Corporation, CA' với 'Apple Corp' thay vì 'IBM Corporation, CA'?",
   opts=["Vì TF/IDF luôn ưu tiên chuỗi ngắn hơn","Vì TF/IDF cho trọng số cao hơn cho từ hiếm ('Apple'), thấp hơn cho từ phổ biến ('Corporation, CA')",
         "Vì TF/IDF không quan tâm nội dung","Vì TF/IDF dùng edit distance"], correct=1,
   explain="IDF (inverse document frequency) làm từ hiếm có trọng số cao — đúng là tín hiệu phân biệt thật sự."),
  dict(q="Soundex hoạt động kém với tên gốc Á Đông vì lý do gì?",
   opts=["Tên Á Đông quá ngắn","Soundex bỏ qua nguyên âm, trong khi tên Á Đông phân biệt nhau chủ yếu qua nguyên âm",
         "Soundex chỉ hỗ trợ bảng chữ cái Latin hoa","Soundex yêu cầu tên có dấu"], correct=1,
   explain="Thiết kế gốc cho tên Caucasian, bỏ nguyên âm — không phù hợp ngôn ngữ phân biệt nhiều qua nguyên âm."),
  dict(q="Sorted Neighborhood giảm độ phức tạp blocking bằng cách nào?",
   opts=["So mọi cặp nhưng song song hoá","Sắp xếp theo sorting key rồi chỉ so trong 1 cửa sổ trượt kích thước cố định",
         "Xoá bớt dữ liệu ngẫu nhiên","Dùng GPU"], correct=1,
   explain="Giả định các bản ghi trùng nhau nằm gần nhau sau khi sort — chỉ cần so trong window, không phải toàn bộ n²."),
  dict(q="Vấn đề 'class skew' khi huấn luyện Learned Matchers là gì?",
   opts=["Dữ liệu quá nhiều","Số cặp match ít hơn rất nhiều so với số cặp non-match","Mô hình quá đơn giản","Không liên quan tới ER"], correct=1,
   explain="Hầu hết các cặp bản ghi KHÔNG match — mất cân bằng lớp nghiêm trọng, cần xử lý riêng khi huấn luyện."),
  dict(q="Nhược điểm chính của Connected Components khi dùng làm thuật toán Clustering trong ER là gì?",
   opts=["Chạy quá chậm","Không chạy được trên đồ thị lớn","Tính bắc cầu dễ tạo cụm quá lớn, gộp nhầm các bản ghi không thực sự giống nhau",
         "Không thể implement"], correct=2,
   explain="A~B và B~C (qua cầu nối B) không đảm bảo A~C thực sự — nhưng Connected Components vẫn gộp cả 3 vào 1 cụm."),
  dict(q="Incremental Data Deduplication dùng kỹ thuật gì để tránh tính lại Correlation Clustering từ đầu?",
   opts=["Xoá hết dữ liệu cũ, chạy lại toàn bộ","Greedy update: connect/merge/split/move trên similarity graph đã có",
         "Chỉ xử lý dữ liệu mới, bỏ qua dữ liệu cũ hoàn toàn","Dùng Soundex thay cho toàn bộ pipeline"], correct=1,
   explain="Giữ lại kết quả clustering cũ, cập nhật tăng dần bằng các thao tác đồ thị nhẹ — nhanh hơn nhiều so với tính lại từ đầu."),
 ]),
]
