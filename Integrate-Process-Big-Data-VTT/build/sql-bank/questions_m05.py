# -*- coding: utf-8 -*-
"""32 bài SQL chạy thật — Module 05 (Bài tập lớn: Tích hợp dữ liệu khí tượng đa nguồn).
Toàn bộ dữ liệu trong schema_m05.sql là SỐ THẬT trích trực tiếp từ
IT5427-Nhom16-TichHopKhiTuong/data_samples/batch_week2/ (không tổng hợp). 3 bảng:
nasa_power_ngay(thanh_pho,ngay,vi_do,kinh_do,nhiet_do_tb_c,luong_mua_mm,buc_xa_mj_m2) — 60 dòng,
openmeteo_ngay(thanh_pho,ngay,vi_do,kinh_do,nhiet_do_max_c,nhiet_do_min_c,luong_mua_mm) — 60 dòng,
ghcn_tram(ma_tram,ngay,element,gia_tri) — 30 dòng, dạng EAV thật của GHCN-Daily (TMAX/TMIN/TAVG/PRCP
mỗi biến 1 dòng, đơn vị 0.1°C / 0.1mm, trạm TH000048565 khu vực Bangkok).
Bài toán cốt lõi: 3 nguồn mô tả CÙNG hiện tượng (nhiệt độ/mưa, cùng 6 thành phố Đông Nam Á, cùng
01-10/01/2024) nhưng khác cấu trúc bảng (wide vs EAV), khác định nghĩa biến (nhiệt độ trung bình vs
max/min), khác đơn vị (độ C thường vs phần mười độ C) — đúng Schema/Semantic/Syntactic Heterogeneity
mà đề tài nhóm giải quyết thật."""

QUESTIONS = [
  # ---- A: Khám phá dữ liệu — nhận diện heterogeneity trước khi tích hợp ----
  dict(id="m05-001", difficulty=1, topic="Khám phá dữ liệu",
    q="Liệt kê toàn bộ bản ghi nasa_power_ngay của thanh_pho='hanoi', sắp theo ngay.",
    referenceSql="SELECT * FROM nasa_power_ngay WHERE thanh_pho='hanoi' ORDER BY ngay;"),
  dict(id="m05-002", difficulty=1, topic="Khám phá dữ liệu",
    q="Đếm số thành_pho DISTINCT xuất hiện trong nasa_power_ngay.",
    referenceSql="SELECT COUNT(DISTINCT thanh_pho) AS so_thanh_pho FROM nasa_power_ngay;"),
  dict(id="m05-003", difficulty=1, topic="Khám phá dữ liệu",
    q="Liệt kê các element DISTINCT có trong ghcn_tram — minh hoạ cấu trúc EAV (mỗi biến 1 dòng"
      " riêng thay vì 1 cột).",
    referenceSql="SELECT DISTINCT element FROM ghcn_tram;"),
  dict(id="m05-004", difficulty=1, topic="Khám phá dữ liệu",
    q="Đếm số dòng ghcn_tram theo từng element — cho thấy không phải ngày nào cũng có đủ cả 4"
      " biến (dữ liệu trạm thật có thiếu, không đều như dữ liệu mô hình).",
    referenceSql="SELECT element, COUNT(*) AS so_dong FROM ghcn_tram GROUP BY element;"),
  dict(id="m05-005", difficulty=2, topic="Khám phá dữ liệu",
    q="So sánh vi_do, kinh_do của cùng thanh_pho='bangkok' giữa nasa_power_ngay và openmeteo_ngay"
      " (SELECT DISTINCT từ cả 2 bảng, UNION) — toạ độ có hoàn toàn trùng khớp không?",
    referenceSql="SELECT 'nasa' AS nguon, vi_do, kinh_do FROM nasa_power_ngay WHERE thanh_pho='bangkok' "
      "UNION SELECT 'openmeteo', vi_do, kinh_do FROM openmeteo_ngay WHERE thanh_pho='bangkok';"),

  # ---- B: Chuẩn hoá dữ liệu EAV (GHCN) — Schema Alignment thật ----
  dict(id="m05-006", difficulty=2, topic="Chuẩn hoá EAV",
    q="Lấy riêng các dòng element='TMAX' từ ghcn_tram, quy đổi gia_tri (đơn vị 0.1°C) sang độ C"
      " thường (chia 10).",
    referenceSql="SELECT ngay, gia_tri/10.0 AS tmax_c FROM ghcn_tram WHERE element='TMAX' ORDER BY ngay;"),
  dict(id="m05-007", difficulty=3, topic="Chuẩn hoá EAV",
    q="PIVOT thủ công: với mỗi ngay, lấy TMAX và TMIN (đã quy đổi độ C) trên CÙNG 1 dòng bằng"
      " self-join ghcn_tram với chính nó (a.element='TMAX', b.element='TMIN', a.ngay=b.ngay) —"
      " đây chính là bước 'unpivot EAV sang wide table' cần làm trước khi JOIN với 2 bảng kia.",
    referenceSql="SELECT a.ngay, a.gia_tri/10.0 AS tmax_c, b.gia_tri/10.0 AS tmin_c "
      "FROM ghcn_tram a JOIN ghcn_tram b ON a.ngay=b.ngay AND a.element='TMAX' AND b.element='TMIN' "
      "ORDER BY a.ngay;"),
  dict(id="m05-008", difficulty=3, topic="Chuẩn hoá EAV",
    q="Từ bước PIVOT trên, chỉ lấy các ngày có CẢ TMAX lẫn TMIN (INNER JOIN tự nhiên đã loại ngày"
      " thiếu) — đếm có bao nhiêu ngày trong 10 ngày đầu tháng 1/2024 có đủ dữ liệu.",
    referenceSql="SELECT COUNT(*) AS so_ngay_du_lieu FROM ghcn_tram a JOIN ghcn_tram b "
      "ON a.ngay=b.ngay AND a.element='TMAX' AND b.element='TMIN';"),
  dict(id="m05-009", difficulty=2, topic="Chuẩn hoá EAV",
    q="Quy đổi PRCP (đơn vị 0.1mm theo chuẩn GHCN) sang mm thường, liệt kê theo ngay.",
    referenceSql="SELECT ngay, gia_tri/10.0 AS mua_mm FROM ghcn_tram WHERE element='PRCP' ORDER BY ngay;"),
  dict(id="m05-010", difficulty=2, topic="Chuẩn hoá EAV",
    q="Tính nhiệt độ trung bình (TAVG, quy đổi độ C) của trạm TH000048565 trong 10 ngày có dữ liệu.",
    referenceSql="SELECT AVG(gia_tri/10.0) AS tavg_tb_c FROM ghcn_tram WHERE element='TAVG';"),

  # ---- C: Data Fusion / Veracity — đối chiếu 2 nguồn cho CÙNG thành phố+ngày ----
  dict(id="m05-011", difficulty=2, topic="Data Fusion",
    q="JOIN nasa_power_ngay với openmeteo_ngay theo CÙNG thanh_pho + ngay, lấy nhiet_do_tb_c (NASA)"
      " và nhiet_do_max_c/nhiet_do_min_c (Open-Meteo) trên cùng 1 dòng, cho thanh_pho='hanoi'.",
    referenceSql="SELECT n.ngay, n.nhiet_do_tb_c, o.nhiet_do_max_c, o.nhiet_do_min_c "
      "FROM nasa_power_ngay n JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "WHERE n.thanh_pho='hanoi' ORDER BY n.ngay;"),
  dict(id="m05-012", difficulty=3, topic="Data Fusion",
    q="Kiểm tra TÍNH HỢP LÝ (sanity check veracity): với mọi thành phố/ngày, nhiet_do_tb_c (NASA)"
      " có luôn nằm trong khoảng [nhiet_do_min_c, nhiet_do_max_c] (Open-Meteo) không? Liệt kê các"
      " trường hợp VI PHẠM (nếu có) — đây là tín hiệu 2 nguồn đo/mô hình hoá khác nhau thật sự.",
    referenceSql="SELECT n.thanh_pho, n.ngay, n.nhiet_do_tb_c, o.nhiet_do_min_c, o.nhiet_do_max_c "
      "FROM nasa_power_ngay n JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "WHERE n.nhiet_do_tb_c < o.nhiet_do_min_c OR n.nhiet_do_tb_c > o.nhiet_do_max_c;"),
  dict(id="m05-013", difficulty=3, topic="Data Fusion",
    q="Tính độ lệch tuyệt đối lượng mưa (mm) giữa nasa_power_ngay.luong_mua_mm và"
      " openmeteo_ngay.luong_mua_mm cho CÙNG thanh_pho+ngay — sắp giảm dần để thấy ngày/thành phố"
      " lệch nhiều nhất (mưa đối lưu nhiệt đới rất khó mô hình hoá, 2 nguồn hay lệch nhau ở biến này).",
    referenceSql="SELECT n.thanh_pho, n.ngay, n.luong_mua_mm AS mua_nasa, o.luong_mua_mm AS mua_openmeteo, "
      "ABS(n.luong_mua_mm - o.luong_mua_mm) AS lech_mm "
      "FROM nasa_power_ngay n JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "ORDER BY lech_mm DESC LIMIT 10;"),
  dict(id="m05-014", difficulty=2, topic="Data Fusion",
    q="Tính độ lệch tuyệt đối mưa trung bình (mm) theo TỪNG thành_pho (GROUP BY), xem thành phố nào"
      " có 2 nguồn lệch nhau nhiều nhất trung bình.",
    referenceSql="SELECT n.thanh_pho, AVG(ABS(n.luong_mua_mm - o.luong_mua_mm)) AS lech_mm_tb "
      "FROM nasa_power_ngay n JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "GROUP BY n.thanh_pho ORDER BY lech_mm_tb DESC;"),
  dict(id="m05-015", difficulty=3, topic="Data Fusion",
    q="Đối chiếu nguồn THỨ 3 (trạm mặt đất thật): JOIN bảng TMAX đã PIVOT từ ghcn_tram (trạm"
      " TH000048565, khu vực Bangkok) với openmeteo_ngay.thanh_pho='bangkok' theo ngay, so lệch"
      " nhiet_do_max_c giữa trạm thật và mô hình Open-Meteo.",
    referenceSql="SELECT g.ngay, g.gia_tri/10.0 AS tmax_tram_that, o.nhiet_do_max_c AS tmax_openmeteo, "
      "ABS(g.gia_tri/10.0 - o.nhiet_do_max_c) AS lech_c "
      "FROM ghcn_tram g JOIN openmeteo_ngay o ON g.ngay=o.ngay AND o.thanh_pho='bangkok' "
      "WHERE g.element='TMAX' ORDER BY g.ngay;"),
  dict(id="m05-016", difficulty=3, topic="Data Fusion",
    q="Từ câu trước, tính độ lệch trung bình (°C) giữa trạm GHCN thật và mô hình Open-Meteo cho"
      " TMAX tại Bangkok — số càng nhỏ càng cho thấy Open-Meteo mô phỏng tốt khu vực này.",
    referenceSql="SELECT AVG(ABS(g.gia_tri/10.0 - o.nhiet_do_max_c)) AS lech_tb_c "
      "FROM ghcn_tram g JOIN openmeteo_ngay o ON g.ngay=o.ngay AND o.thanh_pho='bangkok' "
      "WHERE g.element='TMAX';"),
  dict(id="m05-017", difficulty=2, topic="Data Fusion",
    q="Tìm các ngày Open-Meteo báo CÓ mưa (luong_mua_mm > 0) nhưng NASA POWER báo KHÔNG mưa"
      " (luong_mua_mm = 0) cho cùng thành phố — mâu thuẫn nhị phân giữa 2 nguồn, cần quy tắc"
      " survivorship khi tích hợp (nguồn nào đáng tin hơn cho biến nào).",
    referenceSql="SELECT n.thanh_pho, n.ngay, n.luong_mua_mm AS mua_nasa, o.luong_mua_mm AS mua_openmeteo "
      "FROM nasa_power_ngay n JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "WHERE n.luong_mua_mm = 0 AND o.luong_mua_mm > 0;"),
  dict(id="m05-018", difficulty=2, topic="Data Fusion",
    q="Đếm tổng số ngày (trên toàn bộ 6 thành phố) rơi vào tình huống mâu thuẫn ở câu trước.",
    referenceSql="SELECT COUNT(*) AS so_ngay_mau_thuan FROM nasa_power_ngay n "
      "JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "WHERE n.luong_mua_mm = 0 AND o.luong_mua_mm > 0;"),

  # ---- D: Tích hợp đa nguồn — truy vấn liên nguồn theo đúng kiến trúc mediated schema ----
  dict(id="m05-019", difficulty=2, topic="Tích hợp đa nguồn",
    q="Viết 1 'view tích hợp' đơn giản bằng SELECT: với mỗi thành_pho+ngay, lấy nhiet_do_tb_c"
      " (NASA) LÀM GIÁ TRỊ CHÍNH, kèm buc_xa_mj_m2 (chỉ NASA có) và luong_mua_mm của CẢ 2 nguồn"
      " đặt cạnh nhau để người dùng tự đối chiếu — mô phỏng đúng ý tưởng mediated schema của đề tài.",
    referenceSql="SELECT n.thanh_pho, n.ngay, n.nhiet_do_tb_c, n.buc_xa_mj_m2, "
      "n.luong_mua_mm AS mua_nasa, o.luong_mua_mm AS mua_openmeteo "
      "FROM nasa_power_ngay n JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay;"),
  dict(id="m05-020", difficulty=3, topic="Tích hợp đa nguồn",
    q="Tính biên độ nhiệt ngày (nhiet_do_max_c - nhiet_do_min_c) từ openmeteo_ngay cho mọi thành"
      " phố, trung bình theo thanh_pho — thành phố ven biển/xích đạo (Jakarta, KL) có biên độ nhỏ"
      " hơn thành phố có mùa đông rõ (Hà Nội) hay không?",
    referenceSql="SELECT thanh_pho, AVG(nhiet_do_max_c - nhiet_do_min_c) AS bien_do_nhiet_tb "
      "FROM openmeteo_ngay GROUP BY thanh_pho ORDER BY bien_do_nhiet_tb DESC;"),
  dict(id="m05-021", difficulty=2, topic="Tích hợp đa nguồn",
    q="Xếp hạng 6 thành phố theo buc_xa_mj_m2 (bức xạ mặt trời) trung bình 10 ngày đầu năm 2024 —"
      " dữ liệu CHỈ có ở NASA POWER (openmeteo_ngay không có cột này), minh hoạ Variety thật giữa"
      " 2 nguồn (không chỉ khác giá trị mà khác cả BIẾN có sẵn).",
    referenceSql="SELECT thanh_pho, AVG(buc_xa_mj_m2) AS buc_xa_tb FROM nasa_power_ngay "
      "GROUP BY thanh_pho ORDER BY buc_xa_tb DESC;"),
  dict(id="m05-022", difficulty=3, topic="Tích hợp đa nguồn",
    q="Phát hiện dị thường đơn giản: tìm các (thanh_pho, ngay) có luong_mua_mm (Open-Meteo) lớn"
      " hơn 2 LẦN trung bình luong_mua_mm của CHÍNH thành phố đó trong 10 ngày — ứng dụng trực"
      " tiếp bài toán 'phát hiện dị thường khí hậu' của đề tài nhóm, viết bằng subquery tương quan.",
    referenceSql="SELECT o.thanh_pho, o.ngay, o.luong_mua_mm FROM openmeteo_ngay o "
      "WHERE o.luong_mua_mm > 2 * (SELECT AVG(o2.luong_mua_mm) FROM openmeteo_ngay o2 "
      "WHERE o2.thanh_pho = o.thanh_pho);"),
  dict(id="m05-023", difficulty=2, topic="Tích hợp đa nguồn",
    q="Thành phố nào có nhiet_do_tb_c (NASA) trung bình CAO NHẤT trong 10 ngày — gợi ý cho ứng"
      " dụng 'khuyến nghị khung giờ bay UAV' (nhiệt độ cao thường đi kèm nhiễu động khí quyển"
      " mạnh hơn vào buổi trưa).",
    referenceSql="SELECT thanh_pho, AVG(nhiet_do_tb_c) AS nhiet_tb FROM nasa_power_ngay "
      "GROUP BY thanh_pho ORDER BY nhiet_tb DESC LIMIT 1;"),
  dict(id="m05-024", difficulty=3, topic="Tích hợp đa nguồn",
    q="Với mỗi thành phố, tính số ngày 'mưa lớn' (luong_mua_mm Open-Meteo > 10mm) trong 10 ngày —"
      " ứng dụng cho khuyến nghị nông nghiệp (ngày nào nên hoãn tưới tiêu/thu hoạch).",
    referenceSql="SELECT thanh_pho, COUNT(*) AS so_ngay_mua_lon FROM openmeteo_ngay "
      "WHERE luong_mua_mm > 10 GROUP BY thanh_pho ORDER BY so_ngay_mua_lon DESC;"),

  # ---- E: Tổng hợp cuối — câu hỏi lớn kết hợp nhiều kỹ thuật ----
  dict(id="m05-025", difficulty=3, topic="Tổng hợp",
    q="Xếp hạng các cặp (thanh_pho, ngay) theo ĐỘ TIN CẬY ước lượng: 'tin cậy cao' nếu độ lệch"
      " mưa giữa NASA/Open-Meteo <= 5mm VÀ nhiet_do_tb_c nằm trong khoảng [min,max] của Open-Meteo"
      " — đếm số cặp tin cậy cao theo từng thành phố (kết hợp điều kiện mục C).",
    referenceSql="SELECT n.thanh_pho, COUNT(*) AS so_cap_tin_cay FROM nasa_power_ngay n "
      "JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "WHERE ABS(n.luong_mua_mm - o.luong_mua_mm) <= 5 "
      "AND n.nhiet_do_tb_c BETWEEN o.nhiet_do_min_c AND o.nhiet_do_max_c "
      "GROUP BY n.thanh_pho ORDER BY so_cap_tin_cay DESC;"),
  dict(id="m05-026", difficulty=2, topic="Tổng hợp",
    q="Tính tổng lượng mưa 10 ngày (Open-Meteo) của từng thành phố, sắp giảm dần — thành phố nào"
      " 'ướt' nhất đầu tháng 1/2024 trong 6 thành phố Đông Nam Á này?",
    referenceSql="SELECT thanh_pho, SUM(luong_mua_mm) AS tong_mua FROM openmeteo_ngay "
      "GROUP BY thanh_pho ORDER BY tong_mua DESC;"),
  dict(id="m05-027", difficulty=1, topic="Tổng hợp",
    q="Vĩ độ (vi_do) của thành phố nào trong nasa_power_ngay gần xích đạo nhất (|vi_do| nhỏ nhất)?",
    referenceSql="SELECT DISTINCT thanh_pho, vi_do FROM nasa_power_ngay ORDER BY ABS(vi_do) ASC LIMIT 1;"),
  dict(id="m05-028", difficulty=2, topic="Tổng hợp",
    q="So sánh nhiệt độ trung bình (TAVG, GHCN, quy đổi độ C) của trạm TH000048565 với"
      " nhiet_do_tb_c (NASA, thanh_pho='bangkok') — chênh lệch trung bình bao nhiêu độ C?",
    referenceSql="SELECT AVG(ABS(g.gia_tri/10.0 - n.nhiet_do_tb_c)) AS lech_tb_c "
      "FROM ghcn_tram g JOIN nasa_power_ngay n ON g.ngay=n.ngay AND n.thanh_pho='bangkok' "
      "WHERE g.element='TAVG';"),
  dict(id="m05-029", difficulty=3, topic="Tổng hợp",
    q="Liệt kê 5 cặp (thanh_pho, ngay) có nhiet_do_tb_c (NASA) CAO NHẤT toàn bộ dữ liệu, kèm giá"
      " trị tương ứng ở Open-Meteo (max/min) để đối chiếu nhanh.",
    referenceSql="SELECT n.thanh_pho, n.ngay, n.nhiet_do_tb_c, o.nhiet_do_max_c, o.nhiet_do_min_c "
      "FROM nasa_power_ngay n JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "ORDER BY n.nhiet_do_tb_c DESC LIMIT 5;"),
  dict(id="m05-030", difficulty=2, topic="Tổng hợp",
    q="Đếm số thành phố có ÍT NHẤT 1 ngày 'không mưa cả 2 nguồn' (cả nasa và openmeteo đều"
      " luong_mua_mm = 0) trong 10 ngày.",
    referenceSql="SELECT COUNT(DISTINCT n.thanh_pho) AS so_thanh_pho FROM nasa_power_ngay n "
      "JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "WHERE n.luong_mua_mm = 0 AND o.luong_mua_mm = 0;"),
  dict(id="m05-031", difficulty=3, topic="Tổng hợp",
    q="Bài tổng hợp cuối: với mỗi thành_pho, tính (a) nhiệt độ TB (NASA), (b) tổng mưa (Open-Meteo),"
      " (c) độ lệch mưa TB giữa 2 nguồn — trong 1 câu SELECT duy nhất dùng nhiều JOIN + GROUP BY,"
      " đúng dạng báo cáo tổng hợp cuối module các buổi trước.",
    referenceSql="SELECT n.thanh_pho, AVG(n.nhiet_do_tb_c) AS nhiet_tb, SUM(o.luong_mua_mm) AS tong_mua, "
      "AVG(ABS(n.luong_mua_mm - o.luong_mua_mm)) AS lech_mua_tb "
      "FROM nasa_power_ngay n JOIN openmeteo_ngay o ON n.thanh_pho=o.thanh_pho AND n.ngay=o.ngay "
      "GROUP BY n.thanh_pho ORDER BY nhiet_tb DESC;"),
  dict(id="m05-032", difficulty=1, topic="Tổng hợp",
    q="Đếm tổng số bản ghi (dòng) trên CẢ 3 bảng gộp lại — quy mô dữ liệu mẫu thật dùng trong"
      " module này.",
    referenceSql="SELECT (SELECT COUNT(*) FROM nasa_power_ngay) + (SELECT COUNT(*) FROM openmeteo_ngay) "
      "+ (SELECT COUNT(*) FROM ghcn_tram) AS tong_so_dong;"),
]

assert len(QUESTIONS) == 32, f"Expected 32 questions, got {len(QUESTIONS)}"
assert len({q['id'] for q in QUESTIONS}) == 32, "Duplicate ids found"
