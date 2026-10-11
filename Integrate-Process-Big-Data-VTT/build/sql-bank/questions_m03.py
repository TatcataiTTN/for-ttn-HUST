# -*- coding: utf-8 -*-
"""16 bài SQL chạy thật — Module 03 (Mediation Query bán cấu trúc & Big Data Challenges). Module
này chủ yếu lý thuyết (decompose sub-tree, PAYGO, WebTables) nên SQL chỉ dùng để minh hoạ Join
Graph/hợp nhất nguồn — ít bài hơn Module 00/02/04. Dùng lại dataset Movie S1-S7 (schema_m03.sql)."""

QUESTIONS = [
  dict(id="m03-001", difficulty=1, topic="Join Graph (mô phỏng)",
    q="Join Graph node=nguồn, cạnh=điều kiện join theo key. Viết truy vấn minh hoạ 1 cạnh của Join"
      " Graph: nối S5 (MovieGenres) với S6 (MovieDirectors) qua key 'title'.",
    referenceSql="SELECT g.title, g.genre, d.dir FROM s5_moviegenres g JOIN s6_moviedirectors d ON d.title = g.title;"),
  dict(id="m03-002", difficulty=2, topic="Join Graph (mô phỏng)",
    q="Mở rộng Join Graph thêm 1 cạnh nữa: nối tiếp kết quả trên với S7 (MovieYears) qua title —"
      " mô phỏng việc sinh mediation query phải đi qua NHIỀU cạnh join liên tiếp.",
    referenceSql="SELECT g.title, g.genre, d.dir, y.year FROM s5_moviegenres g "
      "JOIN s6_moviedirectors d ON d.title = g.title JOIN s7_movieyears y ON y.title = g.title;"),
  dict(id="m03-003", difficulty=2, topic="Partial Mapping (mô phỏng)",
    q="Partial Mapping sub-tree 'genre': chỉ map đúng phần genre từ S5 (không đụng tới các cột"
      " khác) — SELECT title, genre từ S5.",
    referenceSql="SELECT title, genre FROM s5_moviegenres;"),
  dict(id="m03-004", difficulty=2, topic="Partial Mapping (mô phỏng)",
    q="Partial Mapping sub-tree 'director': chỉ map đúng phần director từ S6.",
    referenceSql="SELECT title, dir AS director FROM s6_moviedirectors;"),
  dict(id="m03-005", difficulty=3, topic="Kết hợp Partial Mappings",
    q="Kết hợp 2 partial mapping ở trên (genre từ S5, director từ S6) thành 1 mediation query"
      " hoàn chỉnh hơn (JOIN theo title) — đúng bước 'combine' cuối cùng của quy trình sinh"
      " mediation query bán cấu trúc.",
    referenceSql="SELECT g.title, g.genre, d.dir AS director FROM s5_moviegenres g JOIN s6_moviedirectors d ON d.title = g.title;"),
  dict(id="m03-006", difficulty=1, topic="Schema Explosion (mô phỏng)",
    q="Mô phỏng 'Schema Explosion': đếm số CÁCH ĐẶT TÊN khác nhau cho cùng khái niệm 'đạo diễn'"
      " giữa các nguồn (S1.director, S1.MovieDetails.director, S6.dir) — minh hoạ cùng 1 khái"
      " niệm có nhiều tên cột khác nhau.",
    referenceSql="SELECT COUNT(*) AS so_cach_dat_ten FROM (SELECT 'S1.director' UNION SELECT 'S1.MovieDetails.director' UNION SELECT 'S6.dir');"),
  dict(id="m03-007", difficulty=2, topic="Deep Web at Scale (mô phỏng)",
    q="Mô phỏng 'Deep Web at Scale': giả sử mỗi nguồn S1-S7 là 1 'deep web source' ẩn sau form —"
      " đếm tổng số nguồn (bảng) đang tồn tại cho miền dữ liệu Movie.",
    referenceSql="SELECT 7 AS so_nguon_deep_web;"),
  dict(id="m03-008", difficulty=2, topic="Keyword Queries (mô phỏng)",
    q="Mô phỏng Keyword Query 'Nolan SciFi' (không viết SQL đúng mediated schema) bằng cách LIKE"
      " trên cả 2 cột director và genre của S1, OR 2 điều kiện lại.",
    referenceSql="SELECT title FROM s1_movie WHERE director LIKE '%Nolan%' OR genre LIKE '%SciFi%';"),
  dict(id="m03-009", difficulty=2, topic="FeatureRank/SchemaRank (mô phỏng)",
    q="Mô phỏng FeatureRank đơn giản: xếp hạng các nguồn (bảng) theo SỐ DÒNG dữ liệu (coi bảng"
      " nhiều dữ liệu hơn là 'đặc trưng' tốt hơn) — đếm số dòng của S1.Movie và S5.MovieGenres.",
    referenceSql="SELECT 'S1' AS nguon, COUNT(*) AS so_dong FROM s1_movie "
      "UNION SELECT 'S5', COUNT(*) FROM s5_moviegenres;"),
  dict(id="m03-010", difficulty=3, topic="FeatureRank/SchemaRank (mô phỏng)",
    q="Mô phỏng SchemaRank đơn giản: đo độ 'nhất quán' giữa S5 và S6 bằng số title XUẤT HIỆN Ở"
      " CẢ 2 nguồn (càng nhiều title chung, 2 nguồn càng nhất quán với nhau) — đúng tinh thần PMI"
      " cộng thêm trong SchemaRank.",
    referenceSql="SELECT COUNT(*) AS so_title_chung FROM (SELECT title FROM s5_moviegenres INTERSECT SELECT title FROM s6_moviedirectors);"),
  dict(id="m03-011", difficulty=2, topic="Probabilistic Mapping (mô phỏng)",
    q="Mô phỏng Probabilistic Mapping: giả sử director của 'The Godfather' có 2 mapping khả dĩ"
      " (S1 nói Coppola, S6 nói Scorsese) — liệt kê cả 2 khả năng kèm 'nguồn' làm cột xác suất"
      " giả định bằng UNION.",
    referenceSql="SELECT 'S1' AS nguon_tin_cay, director AS director_khavi FROM s1_movie WHERE title = 'The Godfather' "
      "UNION SELECT 'S6', dir FROM s6_moviedirectors WHERE title = 'The Godfather';"),
  dict(id="m03-012", difficulty=2, topic="Modeling Everything (mô phỏng)",
    q="Mô phỏng 'Modeling Everything': đếm số LĨNH VỰC (ở đây đơn giản hoá = số genre khác nhau)"
      " mà 1 mediated schema Movie phải mô hình hoá — minh hoạ sự đa dạng không thể quản được bằng"
      " 1 schema cứng ở quy mô lớn.",
    referenceSql="SELECT COUNT(DISTINCT genre) AS so_genre_can_mo_hinh FROM s5_moviegenres;"),
  dict(id="m03-013", difficulty=1, topic="XQuery output (mô phỏng)",
    q="Mô phỏng 'output XQuery' bằng cách lồng kết quả theo dạng cây (title là gốc, kèm genre là"
      " con) — SQLite không có XML thật nhưng có thể mô phỏng bằng chuỗi nối.",
    referenceSql="SELECT title || ' -> genre: ' || genre AS cay_mo_phong FROM s5_moviegenres LIMIT 5;"),
  dict(id="m03-014", difficulty=2, topic="Join Graph (mô phỏng)",
    q="Tìm các title CHỈ xuất hiện ở ĐÚNG 1 trong 3 nguồn S5/S6/S7 (không đủ để dựng mediated Movie"
      " đầy đủ) — minh hoạ hạn chế của Join Graph khi dữ liệu nguồn không phủ đều nhau.",
    referenceSql="SELECT title FROM (SELECT title FROM s5_moviegenres UNION ALL SELECT title FROM s6_moviedirectors UNION ALL SELECT title FROM s7_movieyears) "
      "GROUP BY title HAVING COUNT(*) = 1;"),
  dict(id="m03-015", difficulty=2, topic="Join Graph (mô phỏng)",
    q="Ngược lại, tìm các title xuất hiện ở ĐỦ CẢ 3 nguồn S5/S6/S7 (đủ dữ liệu dựng mediated Movie"
      " hoàn chỉnh qua Join Graph) — xác nhận lại đúng bằng m02-029 trước đó.",
    referenceSql="SELECT title FROM (SELECT title FROM s5_moviegenres UNION ALL SELECT title FROM s6_moviedirectors UNION ALL SELECT title FROM s7_movieyears) "
      "GROUP BY title HAVING COUNT(*) = 3;"),
  dict(id="m03-016", difficulty=1, topic="PAYGO (mô phỏng)",
    q="Mô phỏng PAYGO 'trả lời tốt nhất có thể ngay': dù S6 thiếu 'Train to Busan', vẫn trả về"
      " TOÀN BỘ title từ S1 kèm director nếu có (LEFT JOIN, chấp nhận NULL) thay vì chờ đủ dữ liệu.",
    referenceSql="SELECT m.title, d.dir AS director_neu_co FROM s1_movie m LEFT JOIN s6_moviedirectors d ON d.title = m.title;"),
]

assert len(QUESTIONS) == 16, f"Expected 16 questions, got {len(QUESTIONS)}"
assert len({q['id'] for q in QUESTIONS}) == 16, "Duplicate ids found"
