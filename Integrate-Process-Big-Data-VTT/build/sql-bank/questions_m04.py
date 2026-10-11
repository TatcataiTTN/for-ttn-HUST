# -*- coding: utf-8 -*-
"""50 bài SQL chạy thật — Module 04 (Record Linkage & Entity Resolution).
Lược đồ: nguon_a(id,tieu_de,dia_chi,quan,dien_tich,gia_trieu,sdt) · nguon_b(id,ten_tin,khu_vuc,
quan,dt_m2,gia_rao_trieu,lien_he) — 2 nguồn rao vặt BĐS độc lập, 7/10 tin trùng thực thể (giá
lệch 4-10%, tên/địa chỉ viết khác, nhưng SDT giống nhau — dùng SDT làm "oracle" kiểm tra kết quả
matching bằng các tín hiệu khác yếu hơn, đúng tinh thần slide: SDT hiếm khi có sẵn/đúng 100% thực
tế nên vẫn phải luyện matching bằng field khác)."""

QUESTIONS = [
  # ---- A: Data Preparation — chuẩn hoá/khám phá dữ liệu trước khi blocking ----
  dict(id="m04-001", difficulty=1, topic="Data Preparation",
    q="Lấy toàn bộ cột của nguon_a.",
    referenceSql="SELECT * FROM nguon_a;"),
  dict(id="m04-002", difficulty=1, topic="Data Preparation",
    q="Lấy tieu_de, gia_trieu từ nguon_a, sắp theo gia_trieu tăng dần.",
    referenceSql="SELECT tieu_de, gia_trieu FROM nguon_a ORDER BY gia_trieu ASC;"),
  dict(id="m04-003", difficulty=1, topic="Data Preparation",
    q="Đếm số tin đăng theo từng quan trong nguon_a.",
    referenceSql="SELECT quan, COUNT(*) AS so_tin FROM nguon_a GROUP BY quan;"),
  dict(id="m04-004", difficulty=1, topic="Data Preparation",
    q="Lấy danh sách DISTINCT các giá trị quan xuất hiện ở CẢ nguon_a và nguon_b (UNION).",
    referenceSql="SELECT DISTINCT quan FROM nguon_a UNION SELECT DISTINCT quan FROM nguon_b;"),
  dict(id="m04-005", difficulty=1, topic="Data Preparation",
    q="Chuẩn hoá: chuyển sdt về dạng chỉ giữ số (ở đây sdt đã toàn số) — đếm độ dài ký tự (LENGTH) của từng sdt trong nguon_a để kiểm tra đồng nhất định dạng.",
    referenceSql="SELECT DISTINCT LENGTH(sdt) AS do_dai_sdt FROM nguon_a;"),

  # ---- B: Blocking bằng khoá chính xác (exact blocking key) ----
  dict(id="m04-006", difficulty=2, topic="Blocking",
    q="Blocking đơn giản nhất: JOIN nguon_a với nguon_b CHỈ theo đúng quan trùng nhau (blocking key = quan) — đây là bước LỌC ỨNG VIÊN trước khi so khớp kỹ hơn.",
    referenceSql="SELECT a.id, a.tieu_de, b.id, b.ten_tin FROM nguon_a a JOIN nguon_b b ON a.quan = b.quan;"),
  dict(id="m04-007", difficulty=2, topic="Blocking",
    q="Đếm số CẶP ỨNG VIÊN sinh ra bởi blocking theo quan (so với Naive All-Pairs sẽ là 10x10=100 cặp).",
    referenceSql="SELECT COUNT(*) AS so_cap_ung_vien FROM nguon_a a JOIN nguon_b b ON a.quan = b.quan;"),
  dict(id="m04-008", difficulty=2, topic="Blocking",
    q="Blocking bằng diện tích: JOIN nguon_a với nguon_b khi dien_tich = dt_m2 (giả định diện tích ít khi bị ghi sai giữa 2 nguồn).",
    referenceSql="SELECT a.id, a.tieu_de, b.id, b.ten_tin, a.dien_tich FROM nguon_a a JOIN nguon_b b ON a.dien_tich = b.dt_m2;"),
  dict(id="m04-009", difficulty=2, topic="Blocking",
    q="Blocking kết hợp 2 điều kiện (quan VÀ dien_tich) để giảm số ứng viên hơn nữa so với chỉ dùng 1 điều kiện.",
    referenceSql="SELECT a.id, b.id FROM nguon_a a JOIN nguon_b b ON a.quan = b.quan AND a.dien_tich = b.dt_m2;"),
  dict(id="m04-010", difficulty=2, topic="Blocking",
    q="Sorted Neighborhood đơn giản hoá: sắp nguon_a theo dien_tich, lấy 3 tin có dien_tich gần giá trị 50 nhất (ORDER BY ABS(dien_tich-50) LIMIT 3) — mô phỏng 'cửa sổ trượt' quanh 1 giá trị.",
    referenceSql="SELECT tieu_de, dien_tich FROM nguon_a ORDER BY ABS(dien_tich - 50) LIMIT 3;"),

  # ---- C: Matching bằng ngưỡng similarity trên giá (price threshold) ----
  dict(id="m04-011", difficulty=2, topic="Matching theo giá",
    q="Matching theo giá với ngưỡng 10%: JOIN nguon_a với nguon_b (đã lọc theo quan+dien_tich ở"
      " câu trước) với điều kiện |gia_trieu - gia_rao_trieu| / gia_trieu <= 0.10.",
    referenceSql="SELECT a.id, a.tieu_de, b.id, b.ten_tin, a.gia_trieu, b.gia_rao_trieu "
      "FROM nguon_a a JOIN nguon_b b ON a.quan = b.quan AND a.dien_tich = b.dt_m2 "
      "WHERE ABS(a.gia_trieu - b.gia_rao_trieu) / a.gia_trieu <= 0.10;"),
  dict(id="m04-012", difficulty=3, topic="Matching theo giá",
    q="So sánh 2 ngưỡng: với ngưỡng 3% (quá chặt), bao nhiêu cặp match theo giá tìm được (trên"
      " tập đã blocking theo quan+dien_tich)?",
    referenceSql="SELECT COUNT(*) AS so_cap_match_3pct FROM nguon_a a JOIN nguon_b b "
      "ON a.quan = b.quan AND a.dien_tich = b.dt_m2 "
      "WHERE ABS(a.gia_trieu - b.gia_rao_trieu) / a.gia_trieu <= 0.03;"),
  dict(id="m04-013", difficulty=3, topic="Matching theo giá",
    q="Với ngưỡng 10% (hợp lý hơn), bao nhiêu cặp match theo giá tìm được? So sánh với câu trước"
      " để thấy ngưỡng quá chặt làm RECALL giảm (bỏ sót các cặp match thật).",
    referenceSql="SELECT COUNT(*) AS so_cap_match_10pct FROM nguon_a a JOIN nguon_b b "
      "ON a.quan = b.quan AND a.dien_tich = b.dt_m2 "
      "WHERE ABS(a.gia_trieu - b.gia_rao_trieu) / a.gia_trieu <= 0.10;"),

  # ---- D: Matching bằng substring địa chỉ (xấp xỉ Jaccard/so khớp chuỗi bằng SQL thuần) ----
  dict(id="m04-014", difficulty=2, topic="Matching theo địa chỉ",
    q="Tìm các cặp (nguon_a, nguon_b) có dia_chi của A xuất hiện là SUBSTRING của khu_vuc ở B"
      " hoặc ngược lại (dùng LIKE với '%'||...||'%') — minh hoạ so khớp chuỗi thô sơ không cần UDF.",
    referenceSql="SELECT a.id, a.dia_chi, b.id, b.khu_vuc FROM nguon_a a JOIN nguon_b b "
      "ON b.khu_vuc LIKE '%' || SUBSTR(a.dia_chi, 1, 6) || '%' OR a.dia_chi LIKE '%' || SUBSTR(b.khu_vuc,1,6) || '%';"),
  dict(id="m04-015", difficulty=2, topic="Matching theo địa chỉ",
    q="Chuẩn hoá đơn giản: SUBSTR 6 ký tự đầu của dia_chi (nguon_a) và khu_vuc (nguon_b), so sánh"
      " có BẰNG NHAU không sau khi chuẩn hoá (coi như đã bỏ dấu, viết thường — ở đây dữ liệu đã"
      " sẵn không dấu nên so trực tiếp được).",
    referenceSql="SELECT a.id, a.dia_chi, b.id, b.khu_vuc FROM nguon_a a JOIN nguon_b b "
      "WHERE SUBSTR(a.dia_chi,1,6) = SUBSTR(b.khu_vuc,1,6);"),

  # ---- E: Matching bằng SĐT — "oracle" để kiểm tra chất lượng blocking/matching khác ----
  dict(id="m04-016", difficulty=2, topic="Matching bằng SĐT",
    q="Tìm TOÀN BỘ cặp match THẬT (ground truth) bằng khoá chắc chắn nhất: sdt = lien_he.",
    referenceSql="SELECT a.id AS id_a, b.id AS id_b FROM nguon_a a JOIN nguon_b b ON a.sdt = b.lien_he;"),
  dict(id="m04-017", difficulty=3, topic="Matching bằng SĐT",
    q="So sánh với ground truth (câu trước): tìm các cặp match THEO GIÁ (ngưỡng 10%, đã blocking"
      " theo quan) nhưng KHÔNG nằm trong ground truth theo SĐT — đây là FALSE POSITIVE của"
      " phương pháp matching theo giá.",
    referenceSql="SELECT a.id, b.id FROM nguon_a a JOIN nguon_b b "
      "ON a.quan = b.quan AND ABS(a.gia_trieu - b.gia_rao_trieu) / a.gia_trieu <= 0.10 "
      "WHERE NOT EXISTS (SELECT 1 FROM nguon_a a2 JOIN nguon_b b2 ON a2.sdt = b2.lien_he WHERE a2.id = a.id AND b2.id = b.id);"),
  dict(id="m04-018", difficulty=3, topic="Matching bằng SĐT",
    q="Tìm các cặp match THẬT (ground truth SĐT) nhưng KHÔNG được blocking-theo-quan+dien_tich"
      " tìm ra (FALSE NEGATIVE — bị bỏ sót bởi bước blocking, nếu có).",
    referenceSql="SELECT a.id, b.id FROM nguon_a a JOIN nguon_b b ON a.sdt = b.lien_he "
      "WHERE NOT EXISTS (SELECT 1 FROM nguon_a a2 JOIN nguon_b b2 ON a2.quan=b2.quan AND a2.dien_tich=b2.dt_m2 WHERE a2.id=a.id AND b2.id=b.id);"),

  # ---- F: Entity Resolution — phát hiện non-match (chỉ có ở 1 nguồn) ----
  dict(id="m04-019", difficulty=2, topic="Non-match",
    q="Tìm các tin trong nguon_a KHÔNG có cặp match nào trong nguon_b (theo SĐT) — đây là các tin"
      " chỉ đăng ở 1 nguồn (non-match thật).",
    referenceSql="SELECT id, tieu_de FROM nguon_a WHERE sdt NOT IN (SELECT lien_he FROM nguon_b);"),
  dict(id="m04-020", difficulty=2, topic="Non-match",
    q="Tìm các tin trong nguon_b KHÔNG có cặp match nào trong nguon_a (theo SĐT).",
    referenceSql="SELECT id, ten_tin FROM nguon_b WHERE lien_he NOT IN (SELECT sdt FROM nguon_a);"),
  dict(id="m04-021", difficulty=1, topic="Non-match",
    q="Đếm tổng số tin ĐÃ match (theo SĐT) so với tổng số tin ở nguon_a — tính tỷ lệ match (%).",
    referenceSql="SELECT 100.0 * (SELECT COUNT(*) FROM nguon_a a WHERE a.sdt IN (SELECT lien_he FROM nguon_b)) / (SELECT COUNT(*) FROM nguon_a) AS ty_le_match_pct;"),

  # ---- G: Clustering đơn giản — hợp nhất 2 nguồn thành 1 danh sách thực thể duy nhất ----
  dict(id="m04-022", difficulty=3, topic="Clustering/Hợp nhất",
    q="Dựng danh sách thực thể HỢP NHẤT: với mỗi cặp match (theo SĐT), lấy tieu_de từ nguon_a,"
      " gia trung bình của 2 nguồn (Data Fusion đơn giản = trung bình 2 giá).",
    referenceSql="SELECT a.tieu_de, (a.gia_trieu + b.gia_rao_trieu) / 2.0 AS gia_hop_nhat "
      "FROM nguon_a a JOIN nguon_b b ON a.sdt = b.lien_he;"),
  dict(id="m04-023", difficulty=3, topic="Clustering/Hợp nhất",
    q="Danh sách thực thể ĐẦY ĐỦ sau khi hợp nhất: UNION các tin match (lấy 1 đại diện từ nguon_a)"
      " với các tin non-match riêng của cả 2 nguồn — tổng số thực thể duy nhất phải là 13"
      " (7 match + 3 non-match A + 3 non-match B).",
    referenceSql="SELECT tieu_de AS ten FROM nguon_a "
      "UNION SELECT ten_tin FROM nguon_b WHERE lien_he NOT IN (SELECT sdt FROM nguon_a);"),
  dict(id="m04-024", difficulty=2, topic="Clustering/Hợp nhất",
    q="Đếm số thực thể duy nhất sau hợp nhất (kết quả của câu trước) để xác nhận đúng 13.",
    referenceSql="SELECT COUNT(*) AS so_thuc_the_duy_nhat FROM (SELECT tieu_de AS ten FROM nguon_a "
      "UNION SELECT ten_tin FROM nguon_b WHERE lien_he NOT IN (SELECT sdt FROM nguon_a));"),

  # ---- H: Aggregate/so sánh phân phối giá giữa 2 nguồn ----
  dict(id="m04-025", difficulty=2, topic="Aggregate",
    q="Tính giá trung bình (gia_trieu) theo quan trong nguon_a.",
    referenceSql="SELECT quan, AVG(gia_trieu) AS gia_tb FROM nguon_a GROUP BY quan;"),
  dict(id="m04-026", difficulty=2, topic="Aggregate",
    q="Tính giá trung bình (gia_rao_trieu) theo quan trong nguon_b.",
    referenceSql="SELECT quan, AVG(gia_rao_trieu) AS gia_tb FROM nguon_b GROUP BY quan;"),
  dict(id="m04-027", difficulty=3, topic="Aggregate",
    q="So sánh giá trung bình theo quan giữa 2 nguồn (JOIN 2 bảng kết quả GROUP BY theo quan).",
    referenceSql="SELECT x.quan, x.gia_tb_a, y.gia_tb_b FROM "
      "(SELECT quan, AVG(gia_trieu) AS gia_tb_a FROM nguon_a GROUP BY quan) x "
      "JOIN (SELECT quan, AVG(gia_rao_trieu) AS gia_tb_b FROM nguon_b GROUP BY quan) y ON x.quan = y.quan;"),
  dict(id="m04-028", difficulty=1, topic="Aggregate",
    q="Tìm giá cao nhất (gia_trieu) trong nguon_a.",
    referenceSql="SELECT tieu_de, gia_trieu FROM nguon_a WHERE gia_trieu = (SELECT MAX(gia_trieu) FROM nguon_a);"),

  # ---- I: LEFT JOIN để liệt kê đầy đủ kèm trạng thái match ----
  dict(id="m04-029", difficulty=2, topic="LEFT JOIN & trạng thái match",
    q="LEFT JOIN nguon_a với nguon_b (theo SĐT) để gắn nhãn từng tin ở nguon_a là 'co_match' hay"
      " 'khong_match'.",
    referenceSql="SELECT a.id, a.tieu_de, CASE WHEN b.id IS NULL THEN 'khong_match' ELSE 'co_match' END AS trang_thai "
      "FROM nguon_a a LEFT JOIN nguon_b b ON a.sdt = b.lien_he;"),
  dict(id="m04-030", difficulty=2, topic="LEFT JOIN & trạng thái match",
    q="Từ kết quả LEFT JOIN trên, đếm số tin 'co_match' và 'khong_match'.",
    referenceSql="SELECT trang_thai, COUNT(*) AS so_tin FROM (SELECT CASE WHEN b.id IS NULL THEN 'khong_match' ELSE 'co_match' END AS trang_thai "
      "FROM nguon_a a LEFT JOIN nguon_b b ON a.sdt = b.lien_he) GROUP BY trang_thai;"),

  # ---- J: Subquery nâng cao ----
  dict(id="m04-031", difficulty=3, topic="Subquery",
    q="Tìm tin ở nguon_a có gia_trieu CAO HƠN giá trung bình của TOÀN BỘ nguon_a VÀ cũng có 1 cặp"
      " match ở nguon_b (theo SĐT).",
    referenceSql="SELECT a.id, a.tieu_de, a.gia_trieu FROM nguon_a a "
      "WHERE a.gia_trieu > (SELECT AVG(gia_trieu) FROM nguon_a) "
      "AND a.sdt IN (SELECT lien_he FROM nguon_b);"),
  dict(id="m04-032", difficulty=2, topic="Subquery",
    q="Tìm quan có số tin đăng (nguon_a) NHIỀU NHẤT.",
    referenceSql="SELECT quan, COUNT(*) AS so_tin FROM nguon_a GROUP BY quan ORDER BY so_tin DESC LIMIT 1;"),

  # ---- K: ORDER BY/LIMIT và phân tích chênh lệch giá ----
  dict(id="m04-033", difficulty=2, topic="Chênh lệch giá",
    q="Với các cặp match (theo SĐT), tính % chênh lệch giá tuyệt đối (|gia_trieu-gia_rao_trieu|/"
      "gia_trieu*100), sắp giảm dần — xem cặp nào lệch giá nhiều nhất.",
    referenceSql="SELECT a.tieu_de, a.gia_trieu, b.gia_rao_trieu, "
      "ROUND(ABS(a.gia_trieu - b.gia_rao_trieu) / a.gia_trieu * 100, 1) AS pct_lech "
      "FROM nguon_a a JOIN nguon_b b ON a.sdt = b.lien_he ORDER BY pct_lech DESC;"),
  dict(id="m04-034", difficulty=2, topic="Chênh lệch giá",
    q="Tính % chênh lệch giá TRUNG BÌNH qua toàn bộ 7 cặp match — đây chính là con số thực tế"
      " đứng sau ví dụ '~5%' nêu trong câu hỏi D2 của Quiz buổi 4.",
    referenceSql="SELECT AVG(ABS(a.gia_trieu - b.gia_rao_trieu) / a.gia_trieu * 100) AS pct_lech_tb "
      "FROM nguon_a a JOIN nguon_b b ON a.sdt = b.lien_he;"),

  # ---- L: So sánh hiệu quả Blocking (giảm số cặp cần xét) ----
  dict(id="m04-035", difficulty=2, topic="Hiệu quả Blocking",
    q="Tính số cặp Naive All-Pairs (không blocking) = số dòng nguon_a × số dòng nguon_b.",
    referenceSql="SELECT (SELECT COUNT(*) FROM nguon_a) * (SELECT COUNT(*) FROM nguon_b) AS so_cap_naive;"),
  dict(id="m04-036", difficulty=2, topic="Hiệu quả Blocking",
    q="Tính tỷ lệ GIẢM số cặp cần xét khi dùng blocking theo quan+dien_tich so với Naive All-Pairs"
      " (%).",
    referenceSql="SELECT 100.0 * (1.0 - CAST((SELECT COUNT(*) FROM nguon_a a JOIN nguon_b b ON a.quan=b.quan AND a.dien_tich=b.dt_m2) AS REAL) "
      "/ ((SELECT COUNT(*) FROM nguon_a) * (SELECT COUNT(*) FROM nguon_b))) AS pct_giam;"),

  # ---- M: CASE WHEN phân loại khoảng giá ----
  dict(id="m04-037", difficulty=2, topic="CASE WHEN",
    q="Phân loại tin nguon_a theo khoảng giá: <7 'rẻ', 7-13 'vừa', >13 'cao'.",
    referenceSql="SELECT tieu_de, gia_trieu, CASE WHEN gia_trieu < 7 THEN 'rẻ' WHEN gia_trieu <= 13 THEN 'vừa' ELSE 'cao' END AS phan_loai FROM nguon_a;"),
  dict(id="m04-038", difficulty=2, topic="CASE WHEN",
    q="Đếm số tin theo từng phân loại giá (rẻ/vừa/cao) ở nguon_a.",
    referenceSql="SELECT phan_loai, COUNT(*) AS so_tin FROM (SELECT CASE WHEN gia_trieu < 7 THEN 'rẻ' WHEN gia_trieu <= 13 THEN 'vừa' ELSE 'cao' END AS phan_loai FROM nguon_a) GROUP BY phan_loai;"),

  # ---- N: Self-join tìm trùng lặp NỘI BỘ 1 nguồn (deduplication) ----
  dict(id="m04-039", difficulty=3, topic="Deduplication nội bộ",
    q="Giả sử cần Naive Deduplication NGAY TRONG nguon_a (tìm tin trùng lặp do đăng nhầm 2 lần) —"
      " self-join theo sdt trùng nhau, id khác nhau (nếu có). Kết quả rỗng nghĩa là nguon_a"
      " không có trùng lặp nội bộ.",
    referenceSql="SELECT a1.id, a2.id, a1.sdt FROM nguon_a a1 JOIN nguon_a a2 ON a1.sdt = a2.sdt AND a1.id < a2.id;"),
  dict(id="m04-040", difficulty=2, topic="Deduplication nội bộ",
    q="Tương tự, kiểm tra nguon_b có trùng lặp nội bộ theo lien_he không.",
    referenceSql="SELECT b1.id, b2.id, b1.lien_he FROM nguon_b b1 JOIN nguon_b b2 ON b1.lien_he = b2.lien_he AND b1.id < b2.id;"),

  # ---- O: Tổng hợp cuối ----
  dict(id="m04-041", difficulty=3, topic="Tổng hợp",
    q="Pipeline đầy đủ 1 câu: Blocking (quan) → Matching (giá ngưỡng 10%) → liệt kê kèm % lệch giá,"
      " sắp theo % lệch giá tăng dần (cặp khớp tốt nhất lên đầu).",
    referenceSql="SELECT a.tieu_de, b.ten_tin, ROUND(ABS(a.gia_trieu-b.gia_rao_trieu)/a.gia_trieu*100,1) AS pct_lech "
      "FROM nguon_a a JOIN nguon_b b ON a.quan = b.quan "
      "WHERE ABS(a.gia_trieu - b.gia_rao_trieu) / a.gia_trieu <= 0.10 ORDER BY pct_lech ASC;"),
  dict(id="m04-042", difficulty=2, topic="Tổng hợp",
    q="Liệt kê HoTen... (ở đây là tieu_de) các tin nguon_a thuộc quan 'Cầu Giấy' CÓ match ở nguon_b.",
    referenceSql="SELECT a.tieu_de FROM nguon_a a WHERE a.quan = 'Cầu Giấy' AND a.sdt IN (SELECT lien_he FROM nguon_b);"),
  dict(id="m04-043", difficulty=2, topic="Tổng hợp",
    q="Liệt kê các tin nguon_a thuộc quan 'Cầu Giấy' KHÔNG có match ở nguon_b.",
    referenceSql="SELECT a.tieu_de FROM nguon_a a WHERE a.quan = 'Cầu Giấy' AND a.sdt NOT IN (SELECT lien_he FROM nguon_b);"),
  dict(id="m04-044", difficulty=2, topic="Tổng hợp",
    q="Tính dien_tich trung bình CHỈ của các tin ĐÃ match (theo SĐT) ở nguon_a.",
    referenceSql="SELECT AVG(dien_tich) AS dt_tb_matched FROM nguon_a WHERE sdt IN (SELECT lien_he FROM nguon_b);"),
  dict(id="m04-045", difficulty=2, topic="Tổng hợp",
    q="Tính dien_tich trung bình CHỈ của các tin KHÔNG match ở nguon_a — so với câu trước để xem"
      " tin không-match có xu hướng diện tích khác biệt không.",
    referenceSql="SELECT AVG(dien_tich) AS dt_tb_non_matched FROM nguon_a WHERE sdt NOT IN (SELECT lien_he FROM nguon_b);"),
  dict(id="m04-046", difficulty=3, topic="Tổng hợp",
    q="Tìm quan xuất hiện ở nguon_a nhưng KHÔNG xuất hiện ở nguon_b (nếu có) — minh hoạ Schema"
      " Coverage khác nhau giữa 2 nguồn tương tự Module 02.",
    referenceSql="SELECT DISTINCT quan FROM nguon_a WHERE quan NOT IN (SELECT quan FROM nguon_b);"),
  dict(id="m04-047", difficulty=3, topic="Tổng hợp",
    q="Tìm quan xuất hiện ở nguon_b nhưng KHÔNG xuất hiện ở nguon_a.",
    referenceSql="SELECT DISTINCT quan FROM nguon_b WHERE quan NOT IN (SELECT quan FROM nguon_a);"),
  dict(id="m04-048", difficulty=1, topic="Tổng hợp",
    q="Đếm tổng số tin đăng của CẢ 2 nguồn gộp lại (không loại trùng, dùng UNION ALL).",
    referenceSql="SELECT (SELECT COUNT(*) FROM nguon_a) + (SELECT COUNT(*) FROM nguon_b) AS tong_tin_tho;"),
  dict(id="m04-049", difficulty=3, topic="Tổng hợp",
    q="Tính tỷ lệ phần trăm số thực thể TRÙNG LẶP (7 cặp match) trên tổng số tin thô (20) — minh"
      " hoạ mức độ trùng lặp dữ liệu thực tế giữa 2 nguồn rao vặt độc lập.",
    referenceSql="SELECT 100.0 * 7 / ((SELECT COUNT(*) FROM nguon_a) + (SELECT COUNT(*) FROM nguon_b)) AS pct_trung_lap;"),
  dict(id="m04-050", difficulty=3, topic="Tổng hợp",
    q="Bài tổng hợp cuối: với mỗi quan có ít nhất 1 cặp match, tính số cặp match và % lệch giá"
      " trung bình của các cặp đó.",
    referenceSql="SELECT a.quan, COUNT(*) AS so_cap, AVG(ABS(a.gia_trieu-b.gia_rao_trieu)/a.gia_trieu*100) AS pct_lech_tb "
      "FROM nguon_a a JOIN nguon_b b ON a.sdt = b.lien_he GROUP BY a.quan;"),
]

assert len(QUESTIONS) == 50, f"Expected 50 questions, got {len(QUESTIONS)}"
assert len({q['id'] for q in QUESTIONS}) == 50, "Duplicate ids found"
