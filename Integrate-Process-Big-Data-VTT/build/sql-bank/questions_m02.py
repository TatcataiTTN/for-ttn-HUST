# -*- coding: utf-8 -*-
"""50 bài SQL chạy thật — Module 02 (Schema Alignment, GAV/LAV/GLAV/Certain Answers).
Mỗi câu chỉ có đề bài + referenceSql (lời giải mẫu) — KHÔNG chứa đáp án tại đây.
compute_expected.py sẽ chạy referenceSql thật trên schema_m02.sql (sqlite3) để lấy expected,
không ai gõ tay đáp án. Lược đồ bảng xem docstring đầu schema_m02.sql (đúng nguyên văn slide gốc).
difficulty: 1=dễ (1 bảng) 2=trung (join 2 bảng) 3=khó (union/subquery/multi-join, mô phỏng GAV/LAV).
"""

QUESTIONS = [
  # ---- Nhóm A: truy vấn cơ bản trên từng nguồn (warm-up, hiểu schema) ----
  dict(id="m02-001", difficulty=1, topic="Cơ bản",
    q="Lấy toàn bộ cột của bảng S1.Movie (title, director, year, genre).",
    referenceSql="SELECT title, director, year, genre FROM s1_movie;"),
  dict(id="m02-002", difficulty=1, topic="Cơ bản",
    q="Lấy title các phim do 'Christopher Nolan' đạo diễn, theo S1.Movie.",
    referenceSql="SELECT title FROM s1_movie WHERE director = 'Christopher Nolan';"),
  dict(id="m02-003", difficulty=1, topic="Cơ bản",
    q="Lấy title các phim thể loại 'SciFi' theo S5.MovieGenres, sắp xếp theo title tăng dần.",
    referenceSql="SELECT title FROM s5_moviegenres WHERE genre = 'SciFi' ORDER BY title;"),
  dict(id="m02-004", difficulty=1, topic="Cơ bản",
    q="Đếm số phim (COUNT) có trong bảng S6.MovieDirectors.",
    referenceSql="SELECT COUNT(*) AS so_phim FROM s6_moviedirectors;"),
  dict(id="m02-005", difficulty=1, topic="Cơ bản",
    q="Lấy title, year của các phim có year < 2010 theo S7.MovieYears.",
    referenceSql="SELECT title, year FROM s7_movieyears WHERE year < 2010;"),
  dict(id="m02-006", difficulty=1, topic="Cơ bản",
    q="Lấy place, movie, start từ S2.Cinemas nơi movie = 'Parasite'.",
    referenceSql="SELECT place, movie, start FROM s2_cinemas WHERE movie = 'Parasite';"),
  dict(id="m02-007", difficulty=1, topic="Cơ bản",
    q="Lấy title và grade từ S4.Reviews có grade >= 9, sắp theo grade giảm dần.",
    referenceSql="SELECT title, grade FROM s4_reviews WHERE grade >= 9 ORDER BY grade DESC;"),
  dict(id="m02-008", difficulty=1, topic="Cơ bản",
    q="Lấy danh sách DISTINCT các giá trị genre xuất hiện trong S5.MovieGenres.",
    referenceSql="SELECT DISTINCT genre FROM s5_moviegenres;"),

  # ---- Nhóm B: GAV unfolding — viết lại query mediated thành query trên nguồn ----
  dict(id="m02-009", difficulty=2, topic="GAV unfolding",
    q="GAV: Movie(title,director,year,genre) ⊇ S1.Movie. Viết query GAV-unfold trả về title,"
      " director của mediated Movie, lấy từ S1.Movie, lọc year > 2010.",
    referenceSql="SELECT title, director FROM s1_movie WHERE year > 2010;"),
  dict(id="m02-010", difficulty=2, topic="GAV unfolding",
    q="GAV: Movie(title,director,year,genre) ⊇ S1.MovieDetails JOIN S1.ActorPlays JOIN S1.Movie"
      " (join theo MID). Viết query lấy title + S1.MovieDetails.director cho các phim có"
      " MovieDetails.year >= 2010 (join s1_moviedetails với s1_movie qua title trùng + năm trùng"
      " để xác định đúng phim, giả định mỗi MID ứng với đúng 1 title trong s1_movie có cùng year).",
    referenceSql="SELECT m.title, d.director FROM s1_moviedetails d "
      "JOIN s1_movie m ON m.year = d.year AND m.director = d.director WHERE d.year >= 2010;"),
  dict(id="m02-011", difficulty=2, topic="GAV unfolding",
    q="GAV: Reviews(title,rating,description) ⊇ S4.Reviews (đổi tên date→bỏ, grade→rating,"
      " review→description). Viết query trả về title AS title, grade AS rating,"
      " review AS description từ S4.Reviews.",
    referenceSql="SELECT title, grade AS rating, review AS description FROM s4_reviews;"),
  dict(id="m02-012", difficulty=2, topic="GAV unfolding",
    q="GAV: Plays(movie,location,startTime) ⊇ S2.Cinemas (đổi tên place→location, start→startTime)."
      " Viết query trả về movie, place AS location, start AS startTime từ S2.Cinemas, chỉ lấy"
      " suất chiếu sau 19:00 (so sánh chuỗi giờ dạng 'HH:MM' vẫn đúng thứ tự).",
    referenceSql="SELECT movie, place AS location, start AS startTime FROM s2_cinemas WHERE start > '19:00';"),

  # ---- Nhóm C: Hợp nhất nhiều nguồn cùng phủ 1 quan hệ mediated (UNION) ----
  dict(id="m02-013", difficulty=2, topic="Hợp nhất nguồn (UNION)",
    q="Plays(movie,location,startTime) được phủ bởi CẢ S2.Cinemas VÀ S3.NYCCinemas (NYC là tập"
      " con các rạp của S2 nhưng có thể có suất riêng). Viết query UNION 2 nguồn để liệt kê toàn bộ"
      " (movie, location, startTime) không trùng lặp, map S3: name→location, title→movie,"
      " startTime→startTime.",
    referenceSql="SELECT movie, place AS location, start AS startTime FROM s2_cinemas "
      "UNION "
      "SELECT title AS movie, name AS location, startTime FROM s3_nyccinemas;"),
  dict(id="m02-014", difficulty=3, topic="Hợp nhất nguồn (UNION)",
    q="Mediated 'đạo diễn của mọi phim đã biết' có thể lấy từ S1.Movie HOẶC S6.MovieDirectors."
      " Viết query UNION title+director từ cả 2 nguồn (S6: dir AS director), rồi dùng DISTINCT để"
      " loại các dòng (title,director) trùng nhau giữa 2 nguồn.",
    referenceSql="SELECT DISTINCT title, director FROM ("
      "SELECT title, director FROM s1_movie "
      "UNION "
      "SELECT title, dir AS director FROM s6_moviedirectors);"),
  dict(id="m02-015", difficulty=3, topic="Certain Answers",
    q="Certain Answer ví dụ: 1 phim có director được CẢ S1.Movie và S6.MovieDirectors cùng xác"
      " nhận (giao của 2 nguồn) thì chắc chắn đúng hơn phim chỉ có ở 1 nguồn. Viết query lấy title"
      " các phim mà (title,director) xuất hiện ĐỒNG THỜI ở S1.Movie và ở S6.MovieDirectors"
      " (dir trùng director) — dùng INTERSECT hoặc EXISTS.",
    referenceSql="SELECT m.title FROM s1_movie m WHERE EXISTS ("
      "SELECT 1 FROM s6_moviedirectors d WHERE d.title = m.title AND d.dir = m.director);"),
  dict(id="m02-016", difficulty=3, topic="Certain Answers",
    q="Ngược lại câu trước: tìm các title có trong S1.Movie nhưng director ghi trong S1.Movie"
      " KHÔNG khớp với director ghi trong S6.MovieDirectors (xung đột giữa 2 nguồn — minh hoạ lý"
      " do Certain Answers phải xét TẤT CẢ instance khả dĩ, không chỉ 1 nguồn).",
    referenceSql="SELECT m.title, m.director AS director_S1, d.dir AS director_S6 "
      "FROM s1_movie m JOIN s6_moviedirectors d ON d.title = m.title "
      "WHERE m.director <> d.dir;"),

  # ---- Nhóm D: Join nhiều bảng trong 1 nguồn (S1 nội bộ) ----
  dict(id="m02-017", difficulty=2, topic="Join nội bộ 1 nguồn",
    q="Trong S1, lấy firstName, lastName của diễn viên cùng director của phim họ tham gia —"
      " join s1_actor JOIN s1_actorplays (qua AID) JOIN s1_moviedetails (qua MID).",
    referenceSql="SELECT a.firstName, a.lastName, d.director FROM s1_actor a "
      "JOIN s1_actorplays p ON p.AID = a.AID "
      "JOIN s1_moviedetails d ON d.MID = p.MID;"),
  dict(id="m02-018", difficulty=2, topic="Join nội bộ 1 nguồn",
    q="Lấy firstName, lastName các diễn viên quốc tịch 'South Korea' trong S1.Actor.",
    referenceSql="SELECT firstName, lastName FROM s1_actor WHERE nationality = 'South Korea';"),
  dict(id="m02-019", difficulty=2, topic="Join nội bộ 1 nguồn",
    q="Lấy title phim (từ s1_movie, join với s1_moviedetails qua director+year trùng) mà diễn"
      " viên sinh trước năm 1970 (yearofBirth < 1970) tham gia — join đủ 4 bảng S1.",
    referenceSql="SELECT DISTINCT m.title FROM s1_actor a "
      "JOIN s1_actorplays p ON p.AID = a.AID "
      "JOIN s1_moviedetails d ON d.MID = p.MID "
      "JOIN s1_movie m ON m.director = d.director AND m.year = d.year "
      "WHERE a.yearofBirth < 1970;"),

  # ---- Nhóm E: Data-level heterogeneity (chuẩn hoá định dạng/giá trị khác nhau giữa nguồn) ----
  dict(id="m02-020", difficulty=2, topic="Data-level heterogeneity",
    q="S4.Reviews chấm thang 1-10 ('grade'). Giả sử mediated Reviews.rating cần thang 1-5 (quy đổi"
      " rating = grade/2.0). Viết query trả title, grade/2.0 AS rating từ S4.Reviews.",
    referenceSql="SELECT title, grade / 2.0 AS rating FROM s4_reviews;"),
  dict(id="m02-021", difficulty=2, topic="Data-level heterogeneity",
    q="Tính rating trung bình (AVG) theo thang 1-5 (grade/2.0) cho từng title có nhiều review,"
      " nhóm theo title, chỉ giữ title có hơn 1 review (HAVING COUNT(*) > 1).",
    referenceSql="SELECT title, AVG(grade / 2.0) AS avg_rating, COUNT(*) AS n "
      "FROM s4_reviews GROUP BY title HAVING COUNT(*) > 1;"),

  # ---- Nhóm F: Aggregate / GROUP BY áp dụng cho mediated schema ----
  dict(id="m02-022", difficulty=2, topic="Aggregate",
    q="Đếm số phim theo từng genre trong S1.Movie, sắp giảm dần theo số lượng.",
    referenceSql="SELECT genre, COUNT(*) AS so_phim FROM s1_movie GROUP BY genre ORDER BY so_phim DESC;"),
  dict(id="m02-023", difficulty=2, topic="Aggregate",
    q="Đếm số phim theo từng director trong S1.Movie, chỉ giữ director có từ 2 phim trở lên.",
    referenceSql="SELECT director, COUNT(*) AS so_phim FROM s1_movie GROUP BY director HAVING COUNT(*) >= 2;"),
  dict(id="m02-024", difficulty=2, topic="Aggregate",
    q="Tính year trung bình (AVG) các phim trong S1.Movie theo từng genre.",
    referenceSql="SELECT genre, AVG(year) AS avg_year FROM s1_movie GROUP BY genre;"),
  dict(id="m02-025", difficulty=1, topic="Aggregate",
    q="Tìm year nhỏ nhất (MIN) và lớn nhất (MAX) trong S1.Movie.",
    referenceSql="SELECT MIN(year) AS year_min, MAX(year) AS year_max FROM s1_movie;"),

  # ---- Nhóm G: Schema Coverage — phát hiện "thiếu thông tin" giữa các nguồn ----
  dict(id="m02-026", difficulty=3, topic="Schema Coverage",
    q="Tìm các title có trong S1.Movie nhưng KHÔNG có trong S6.MovieDirectors (minh hoạ 'Different"
      " Coverage' của slide — S6 không biết hết mọi phim).",
    referenceSql="SELECT title FROM s1_movie WHERE title NOT IN (SELECT title FROM s6_moviedirectors);"),
  dict(id="m02-027", difficulty=3, topic="Schema Coverage",
    q="Tìm các title có trong S1.Movie nhưng KHÔNG có trong S7.MovieYears.",
    referenceSql="SELECT title FROM s1_movie WHERE title NOT IN (SELECT title FROM s7_movieyears);"),
  dict(id="m02-028", difficulty=3, topic="Schema Coverage",
    q="Liệt kê các title có mặt ở CẢ S5.MovieGenres, S6.MovieDirectors, S7.MovieYears (giao của 3"
      " nguồn — dùng INTERSECT hoặc 3 lần EXISTS).",
    referenceSql="SELECT title FROM s5_moviegenres "
      "INTERSECT SELECT title FROM s6_moviedirectors "
      "INTERSECT SELECT title FROM s7_movieyears;"),
  dict(id="m02-029", difficulty=3, topic="Schema Coverage",
    q="Dựng lại mediated Movie(title,director,year,genre) đầy đủ nhất có thể bằng JOIN 3 nguồn"
      " S5 (genre), S6 (director), S7 (year) theo title — đây chính là ví dụ LAV: mỗi nguồn là 1"
      " view chỉ biết 1 phần cột của mediated schema.",
    referenceSql="SELECT g.title, d.dir AS director, y.year, g.genre "
      "FROM s5_moviegenres g "
      "JOIN s6_moviedirectors d ON d.title = g.title "
      "JOIN s7_movieyears y ON y.title = g.title;"),

  # ---- Nhóm H: Subquery lồng nhau ----
  dict(id="m02-030", difficulty=2, topic="Subquery",
    q="Tìm title các phim trong S1.Movie có year lớn hơn year trung bình của toàn bộ S1.Movie.",
    referenceSql="SELECT title, year FROM s1_movie WHERE year > (SELECT AVG(year) FROM s1_movie);"),
  dict(id="m02-031", difficulty=2, topic="Subquery",
    q="Tìm title phim có grade (S4.Reviews) cao nhất trong toàn bộ bảng.",
    referenceSql="SELECT title, grade FROM s4_reviews WHERE grade = (SELECT MAX(grade) FROM s4_reviews);"),
  dict(id="m02-032", difficulty=2, topic="Subquery",
    q="Tìm các director (S1.Movie) có TẤT CẢ phim của họ thuộc genre 'SciFi' (dùng NOT EXISTS để"
      " loại director có ít nhất 1 phim khác genre SciFi).",
    referenceSql="SELECT DISTINCT director FROM s1_movie m1 WHERE NOT EXISTS ("
      "SELECT 1 FROM s1_movie m2 WHERE m2.director = m1.director AND m2.genre <> 'SciFi');"),

  # ---- Nhóm I: LEFT JOIN để lộ rõ dữ liệu thiếu (NULL) ----
  dict(id="m02-033", difficulty=2, topic="LEFT JOIN & NULL",
    q="LEFT JOIN S1.Movie với S4.Reviews (theo title) để thấy phim nào CHƯA có review nào"
      " (review columns sẽ là NULL) — trả về title, grade.",
    referenceSql="SELECT m.title, r.grade FROM s1_movie m LEFT JOIN s4_reviews r ON r.title = m.title;"),
  dict(id="m02-034", difficulty=2, topic="LEFT JOIN & NULL",
    q="Từ kết quả LEFT JOIN trên, lọc ra CHỈ các title chưa có review nào (grade IS NULL).",
    referenceSql="SELECT m.title FROM s1_movie m LEFT JOIN s4_reviews r ON r.title = m.title "
      "WHERE r.grade IS NULL;"),

  # ---- Nhóm J: ORDER BY + LIMIT ----
  dict(id="m02-035", difficulty=1, topic="ORDER BY/LIMIT",
    q="Lấy 3 phim có year lớn nhất trong S1.Movie (title, year), mới nhất trước.",
    referenceSql="SELECT title, year FROM s1_movie ORDER BY year DESC LIMIT 3;"),
  dict(id="m02-036", difficulty=1, topic="ORDER BY/LIMIT",
    q="Lấy phim có grade thấp nhất trong S4.Reviews (title, grade), chỉ 1 dòng.",
    referenceSql="SELECT title, grade FROM s4_reviews ORDER BY grade ASC LIMIT 1;"),

  # ---- Nhóm K: Query Reformulation nhiều bước (mô phỏng wrapper/reformulation pipeline) ----
  dict(id="m02-037", difficulty=3, topic="Query Reformulation",
    q="Mediated query gốc: 'Lấy title, director các phim SciFi, kèm điểm review trung bình nếu"
      " có'. Reformulate: join S1.Movie (lọc genre='SciFi') LEFT JOIN S4.Reviews (GROUP BY title"
      " lấy AVG grade).",
    referenceSql="SELECT m.title, m.director, "
      "(SELECT AVG(r.grade) FROM s4_reviews r WHERE r.title = m.title) AS avg_grade "
      "FROM s1_movie m WHERE m.genre = 'SciFi';"),
  dict(id="m02-038", difficulty=3, topic="Query Reformulation",
    q="Mediated query: 'phim nào có suất chiếu ở NYC VÀ có review >= 8'. Reformulate bằng JOIN"
      " S3.NYCCinemas với S4.Reviews qua title, lọc grade >= 8, DISTINCT title.",
    referenceSql="SELECT DISTINCT c.title FROM s3_nyccinemas c "
      "JOIN s4_reviews r ON r.title = c.title WHERE r.grade >= 8;"),
  dict(id="m02-039", difficulty=3, topic="Query Reformulation",
    q="Mediated query: 'phim có suất chiếu ở S2.Cinemas nhưng KHÔNG xuất hiện trong S3.NYCCinemas'"
      " (đang chiếu ở nơi khác ngoài NYC) — dùng NOT IN hoặc NOT EXISTS trên movie/title.",
    referenceSql="SELECT DISTINCT movie FROM s2_cinemas WHERE movie NOT IN "
      "(SELECT title FROM s3_nyccinemas);"),

  # ---- Nhóm L: Thêm ví dụ GLAV/TGD dạng kiểm tra tồn tại ----
  dict(id="m02-040", difficulty=3, topic="GLAV/TGD",
    q="TGD minh hoạ: nếu (title,genre) có ở S5 VÀ (title,dir) có ở S6 VÀ (title,year) có ở S7 THÌ"
      " suy ra tồn tại 1 dòng Movie(title,dir,year,genre) đầy đủ (đã làm ở m02-029) — ở đây hãy"
      " ĐẾM xem có bao nhiêu title thoả điều kiện tiền đề đó (đếm kết quả JOIN 3 nguồn).",
    referenceSql="SELECT COUNT(*) AS so_phim_day_du FROM ("
      "SELECT g.title FROM s5_moviegenres g "
      "JOIN s6_moviedirectors d ON d.title = g.title "
      "JOIN s7_movieyears y ON y.title = g.title);"),
  dict(id="m02-041", difficulty=3, topic="GLAV/TGD",
    q="Tìm title có trong S5 (MovieGenres) nhưng KHÔNG thoả được tiền đề TGD ở câu trước (thiếu"
      " ở S6 hoặc S7) — minh hoạ 1 instance mediated KHÔNG suy luận được đầy đủ từ GLAV.",
    referenceSql="SELECT title FROM s5_moviegenres WHERE title NOT IN ("
      "SELECT g.title FROM s5_moviegenres g "
      "JOIN s6_moviedirectors d ON d.title = g.title "
      "JOIN s7_movieyears y ON y.title = g.title);"),

  # ---- Nhóm M: Case/When mô phỏng phân loại ----
  dict(id="m02-042", difficulty=2, topic="CASE WHEN",
    q="Phân loại phim theo thập niên bằng CASE WHEN: year < 2000 → 'pre-2000', 2000-2009 →"
      " '2000s', >=2010 → '2010s'. Trả về title, year, decade.",
    referenceSql="SELECT title, year, CASE WHEN year < 2000 THEN 'pre-2000' "
      "WHEN year < 2010 THEN '2000s' ELSE '2010s' END AS decade FROM s1_movie;"),
  dict(id="m02-043", difficulty=2, topic="CASE WHEN",
    q="Đếm số phim theo từng decade (dùng lại logic CASE WHEN câu trước, GROUP BY decade).",
    referenceSql="SELECT decade, COUNT(*) AS so_phim FROM ("
      "SELECT CASE WHEN year < 2000 THEN 'pre-2000' WHEN year < 2010 THEN '2000s' "
      "ELSE '2010s' END AS decade FROM s1_movie) GROUP BY decade;"),

  # ---- Nhóm N: Self-join / so sánh trong cùng bảng ----
  dict(id="m02-044", difficulty=3, topic="Self-join",
    q="Tìm các cặp phim (title1, title2) cùng director trong S1.Movie, title1 < title2 (tránh"
      " trùng cặp và tránh so 1 phim với chính nó) — self-join s1_movie với chính nó.",
    referenceSql="SELECT a.title AS title1, b.title AS title2, a.director "
      "FROM s1_movie a JOIN s1_movie b ON a.director = b.director AND a.title < b.title;"),
  dict(id="m02-045", difficulty=3, topic="Self-join",
    q="Tìm các cặp phim cùng genre VÀ cùng năm phát hành (year) trong S1.Movie (self-join 2 điều"
      " kiện), title1 < title2.",
    referenceSql="SELECT a.title AS title1, b.title AS title2, a.genre, a.year "
      "FROM s1_movie a JOIN s1_movie b "
      "ON a.genre = b.genre AND a.year = b.year AND a.title < b.title;"),

  # ---- Nhóm O: Tổng hợp cuối — truy vấn phức hợp nhiều nguồn ----
  dict(id="m02-046", difficulty=3, topic="Tổng hợp nhiều nguồn",
    q="Danh sách đầy đủ nhất có thể: với mỗi title trong S1.Movie, lấy kèm review trung bình (S4,"
      " có thể NULL), và đánh dấu có chiếu ở NYC hay không (EXISTS trên S3) — trả về title,"
      " avg_grade, co_chieu_nyc (1/0).",
    referenceSql="SELECT m.title, "
      "(SELECT AVG(r.grade) FROM s4_reviews r WHERE r.title = m.title) AS avg_grade, "
      "(SELECT COUNT(*) > 0 FROM s3_nyccinemas c WHERE c.title = m.title) AS co_chieu_nyc "
      "FROM s1_movie m;"),
  dict(id="m02-047", difficulty=3, topic="Tổng hợp nhiều nguồn",
    q="Tìm title các phim có review trung bình (S4) >= 8.5 VÀ có chiếu ở S2.Cinemas (JOIN +"
      " subquery kết hợp HAVING).",
    referenceSql="SELECT r.title FROM s4_reviews r WHERE r.title IN (SELECT movie FROM s2_cinemas) "
      "GROUP BY r.title HAVING AVG(r.grade) >= 8.5;"),
  dict(id="m02-048", difficulty=3, topic="Tổng hợp nhiều nguồn",
    q="Director nào (S1.Movie) có phim xuất hiện ở S2.Cinemas NHIỀU rạp nhất? Trả về director,"
      " số lượt chiếu (JOIN S1.Movie với S2.Cinemas qua title, GROUP BY director, ORDER BY"
      " COUNT DESC LIMIT 1).",
    referenceSql="SELECT m.director, COUNT(*) AS so_luot_chieu FROM s1_movie m "
      "JOIN s2_cinemas c ON c.movie = m.title "
      "GROUP BY m.director ORDER BY so_luot_chieu DESC LIMIT 1;"),
  dict(id="m02-049", difficulty=2, topic="Tổng hợp nhiều nguồn",
    q="Liệt kê title, genre (S5) của các phim CÓ review (S4) nhưng KHÔNG có suất chiếu nào ở"
      " S2.Cinemas (phim được đánh giá nhưng hiện tại rạp không chiếu).",
    referenceSql="SELECT DISTINCT g.title, g.genre FROM s5_moviegenres g "
      "WHERE g.title IN (SELECT title FROM s4_reviews) "
      "AND g.title NOT IN (SELECT movie FROM s2_cinemas);"),
  dict(id="m02-050", difficulty=3, topic="Tổng hợp nhiều nguồn",
    q="Bài tổng hợp cuối: với mỗi genre (S5), tính số phim (COUNT DISTINCT title) và review trung"
      " bình của TOÀN BỘ phim thuộc genre đó (JOIN S5 với S4 qua title, GROUP BY genre).",
    referenceSql="SELECT g.genre, COUNT(DISTINCT g.title) AS so_phim, AVG(r.grade) AS avg_grade "
      "FROM s5_moviegenres g LEFT JOIN s4_reviews r ON r.title = g.title "
      "GROUP BY g.genre;"),
]

assert len(QUESTIONS) == 50, f"Expected 50 questions, got {len(QUESTIONS)}"
assert len({q['id'] for q in QUESTIONS}) == 50, "Duplicate ids found"
