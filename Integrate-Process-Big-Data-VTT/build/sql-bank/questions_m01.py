# -*- coding: utf-8 -*-
"""16 bài SQL chạy thật — Module 01 (Data Integration overview). Module này chủ yếu lý thuyết
kiến trúc (Mediated Schema/Wrapper/Heterogeneity) nên số bài SQL ít hơn các module 00/02/04 có
nhiều phép toán quan hệ cụ thể hơn. Dùng lại dataset Movie S1-S7 (xem schema_m02.sql/schema_m01.sql).
"""

QUESTIONS = [
  dict(id="m01-001", difficulty=1, topic="Wrapper (mô phỏng)",
    q="Mô phỏng Wrapper cho nguồn S1: SELECT đúng 4 cột (title,director,year,genre) từ s1_movie —"
      " đây chính là việc Wrapper phải làm để trả dữ liệu về đúng mô hình mediated schema.",
    referenceSql="SELECT title, director, year, genre FROM s1_movie;"),
  dict(id="m01-002", difficulty=2, topic="Wrapper (mô phỏng)",
    q="Mô phỏng Wrapper cho nguồn S2 (Cinemas): đổi tên cột place→location, start→startTime để"
      " khớp mediated schema Plays(movie,location,startTime).",
    referenceSql="SELECT movie, place AS location, start AS startTime FROM s2_cinemas;"),
  dict(id="m01-003", difficulty=2, topic="Wrapper (mô phỏng)",
    q="Mô phỏng Wrapper cho nguồn S4 (Reviews): đổi tên grade→rating, review→description để khớp"
      " mediated schema Reviews(title,rating,description).",
    referenceSql="SELECT title, grade AS rating, review AS description FROM s4_reviews;"),
  dict(id="m01-004", difficulty=1, topic="System/Platform Heterogeneity",
    q="S1 lưu đạo diễn trong 4 bảng tách (Movie/Actor/ActorPlays/MovieDetails) trong khi mediated"
      " schema chỉ có 1 bảng Movie — đếm số bảng khác nhau mà Wrapper của S1 phải JOIN để trả về"
      " đủ thông tin 1 phim (Movie+MovieDetails).",
    referenceSql="SELECT COUNT(DISTINCT m.title) AS so_phim_can_join FROM s1_movie m "
      "JOIN s1_moviedetails d ON d.director = m.director AND d.year = m.year;"),
  dict(id="m01-005", difficulty=1, topic="Virtual vs Warehouse (mô phỏng)",
    q="Mô phỏng truy vấn 'query-time' kiểu Virtual Integration: lấy trực tiếp từ S5 (không cache)"
      " các phim thể loại 'Animation'.",
    referenceSql="SELECT title FROM s5_moviegenres WHERE genre = 'Animation';"),
  dict(id="m01-006", difficulty=2, topic="Virtual vs Warehouse (mô phỏng)",
    q="Mô phỏng 'bản copy đã ETL' kiểu Data Warehousing: tạo 1 bảng tạm gộp sẵn title+genre+year"
      " từ S5+S7 (JOIN), coi như đã chạy ETL 1 lần — SELECT kết quả JOIN đó.",
    referenceSql="SELECT g.title, g.genre, y.year FROM s5_moviegenres g JOIN s7_movieyears y ON y.title = g.title;"),
  dict(id="m01-007", difficulty=2, topic="Query Reformulation",
    q="Mediated query: 'Lấy mọi phim SciFi có năm > 2010'. Reformulate thành truy vấn trên S1"
      " (nguồn duy nhất có đủ cả genre và year trong 1 bảng).",
    referenceSql="SELECT title FROM s1_movie WHERE genre = 'SciFi' AND year > 2010;"),
  dict(id="m01-008", difficulty=3, topic="Query Reformulation",
    q="Cùng mediated query trên nhưng giả sử CHỈ CÓ S5 (genre) và S7 (year), không có S1 — viết"
      " lại reformulation bằng JOIN 2 nguồn rồi lọc.",
    referenceSql="SELECT g.title FROM s5_moviegenres g JOIN s7_movieyears y ON y.title = g.title "
      "WHERE g.genre = 'SciFi' AND y.year > 2010;"),
  dict(id="m01-009", difficulty=1, topic="5V (mô phỏng Volume)",
    q="Mô phỏng đo 'Volume': đếm tổng số dòng dữ liệu đang có trên TOÀN BỘ các nguồn S1.Movie,"
      " S5, S6, S7 gộp lại (UNION ALL các COUNT).",
    referenceSql="SELECT (SELECT COUNT(*) FROM s1_movie) + (SELECT COUNT(*) FROM s5_moviegenres) "
      "+ (SELECT COUNT(*) FROM s6_moviedirectors) + (SELECT COUNT(*) FROM s7_movieyears) AS tong_volume;"),
  dict(id="m01-010", difficulty=2, topic="5V (mô phỏng Variety)",
    q="Mô phỏng đo 'Variety': đếm số LƯỢC ĐỒ BẢNG khác nhau (ở đây đơn giản hoá = số bảng nguồn"
      " khác nhau) đang tồn tại cho miền dữ liệu Movie.",
    referenceSql="SELECT COUNT(*) AS so_nguon_khac_nhau FROM (SELECT 's1' UNION SELECT 's2' "
      "UNION SELECT 's3' UNION SELECT 's4' UNION SELECT 's5' UNION SELECT 's6' UNION SELECT 's7');"),
  dict(id="m01-011", difficulty=2, topic="Pipeline Schema Alignment→ER→Fusion (mô phỏng)",
    q="Bước 1 (Schema Alignment, mô phỏng): hợp nhất title+genre+director+year từ 3 nguồn S5/S6/S7"
      " thành 1 'mediated view' tạm (đã làm ở Module 02 bài m02-029) — lặp lại ở đây cho đủ pipeline.",
    referenceSql="SELECT g.title, d.dir AS director, y.year, g.genre FROM s5_moviegenres g "
      "JOIN s6_moviedirectors d ON d.title = g.title JOIN s7_movieyears y ON y.title = g.title;"),
  dict(id="m01-012", difficulty=2, topic="Pipeline Schema Alignment→ER→Fusion (mô phỏng)",
    q="Bước 2 (Entity Resolution, mô phỏng): kiểm tra xem có title nào ở S1 bị TRÙNG LẶP nội bộ"
      " (xuất hiện quá 1 lần) — nếu có, đây là bước ER cần xử lý trước khi Fusion.",
    referenceSql="SELECT title, COUNT(*) AS so_lan FROM s1_movie GROUP BY title HAVING COUNT(*) > 1;"),
  dict(id="m01-013", difficulty=3, topic="Pipeline Schema Alignment→ER→Fusion (mô phỏng)",
    q="Bước 3 (Data Fusion, mô phỏng): với các title có director khác nhau giữa S1 và S6 (xung"
      " đột, xem lại bài m02-016), chọn GIÁ TRỊ THẮNG theo luật đơn giản 'ưu tiên S1' (Survivorship Rule).",
    referenceSql="SELECT m.title, m.director AS director_thang_theo_S1 FROM s1_movie m "
      "JOIN s6_moviedirectors d ON d.title = m.title WHERE m.director <> d.dir;"),
  dict(id="m01-014", difficulty=1, topic="Query Processing pipeline",
    q="Mô phỏng bước cuối 'Execution Engine gọi Wrapper' bằng 1 UNION gộp kết quả từ 2 wrapper"
      " (S2 và S3) cho cùng mediated Plays.",
    referenceSql="SELECT movie, place AS location, start AS startTime FROM s2_cinemas "
      "UNION SELECT title AS movie, name AS location, startTime FROM s3_nyccinemas;"),
  dict(id="m01-015", difficulty=2, topic="Data-level Heterogeneity",
    q="Mô phỏng Data-level Heterogeneity (đổi đơn vị): giả sử cần quy đổi grade (thang 1-10, S4)"
      " sang thang 1-5 bằng phép tính /2.0 — đây chính là ví dụ 'Celsius↔Fahrenheit' nhưng cho"
      " điểm đánh giá phim.",
    referenceSql="SELECT title, grade / 2.0 AS rating_thang_5 FROM s4_reviews;"),
  dict(id="m01-016", difficulty=2, topic="Temporal Heterogeneity (mô phỏng)",
    q="Mô phỏng Temporal Heterogeneity: tìm các review (S4) cũ nhất và mới nhất theo cột date, để"
      " minh hoạ các nguồn có thể cập nhật ở tần suất khác nhau.",
    referenceSql="SELECT MIN(date) AS review_cu_nhat, MAX(date) AS review_moi_nhat FROM s4_reviews;"),
]

assert len(QUESTIONS) == 16, f"Expected 16 questions, got {len(QUESTIONS)}"
assert len({q['id'] for q in QUESTIONS}) == 16, "Duplicate ids found"
