# -*- coding: utf-8 -*-
"""50 bài SQL chạy thật — Module 00 (Nền tảng CSDL: ER, khoá chính/khoá ngoại, liên kết N-N).
Lược đồ: nguoithue(MaNguoiThue PK,...) · canho(MaCanHo PK,...) ·
thue(MaNguoiThue FK, MaCanHo FK, NgayBatDau, NgayKetThuc, GiaThueThucTe) — bảng trung gian N-N
có thuộc tính riêng, đúng bài tập làm giấy đã có trong exercises.json Module 00.
"""

QUESTIONS = [
  # ---- A: SELECT cơ bản ----
  dict(id="m00-001", difficulty=1, topic="Cơ bản",
    q="Lấy toàn bộ cột của bảng nguoithue.",
    referenceSql="SELECT * FROM nguoithue;"),
  dict(id="m00-002", difficulty=1, topic="Cơ bản",
    q="Lấy HoTen, SDT của người thuê sinh sau năm 1995.",
    referenceSql="SELECT HoTen, SDT FROM nguoithue WHERE NamSinh > 1995;"),
  dict(id="m00-003", difficulty=1, topic="Cơ bản",
    q="Lấy DiaChi các căn hộ ở quận 'Cầu Giấy'.",
    referenceSql="SELECT DiaChi FROM canho WHERE Quan = 'Cầu Giấy';"),
  dict(id="m00-004", difficulty=1, topic="Cơ bản",
    q="Lấy DiaChi, GiaThueNiemYet các căn hộ có giá niêm yết trên 9000000, sắp giảm dần theo giá.",
    referenceSql="SELECT DiaChi, GiaThueNiemYet FROM canho WHERE GiaThueNiemYet > 9000000 ORDER BY GiaThueNiemYet DESC;"),
  dict(id="m00-005", difficulty=1, topic="Cơ bản",
    q="Đếm số căn hộ có diện tích (DienTich) lớn hơn 40.",
    referenceSql="SELECT COUNT(*) AS so_can FROM canho WHERE DienTich > 40;"),
  dict(id="m00-006", difficulty=1, topic="Cơ bản",
    q="Lấy danh sách DISTINCT các quận (Quan) xuất hiện trong bảng canho.",
    referenceSql="SELECT DISTINCT Quan FROM canho;"),
  dict(id="m00-007", difficulty=1, topic="Cơ bản",
    q="Tìm hợp đồng thuê (thue) đang còn hiệu lực (NgayKetThuc IS NULL).",
    referenceSql="SELECT * FROM thue WHERE NgayKetThuc IS NULL;"),
  dict(id="m00-008", difficulty=1, topic="Cơ bản",
    q="Lấy GiaThueThucTe nhỏ nhất và lớn nhất trong bảng thue.",
    referenceSql="SELECT MIN(GiaThueThucTe) AS gia_min, MAX(GiaThueThucTe) AS gia_max FROM thue;"),

  # ---- B: JOIN khoá chính-khoá ngoại ----
  dict(id="m00-009", difficulty=2, topic="Join khoá chính-ngoại",
    q="JOIN thue với nguoithue (qua MaNguoiThue) để lấy HoTen cùng GiaThueThucTe của từng hợp đồng.",
    referenceSql="SELECT n.HoTen, t.GiaThueThucTe FROM thue t JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue;"),
  dict(id="m00-010", difficulty=2, topic="Join khoá chính-ngoại",
    q="JOIN thue với canho (qua MaCanHo) để lấy DiaChi cùng NgayBatDau của từng hợp đồng.",
    referenceSql="SELECT c.DiaChi, t.NgayBatDau FROM thue t JOIN canho c ON c.MaCanHo = t.MaCanHo;"),
  dict(id="m00-011", difficulty=3, topic="Join khoá chính-ngoại",
    q="JOIN đủ 3 bảng (nguoithue-thue-canho) để lấy HoTen, DiaChi, GiaThueThucTe của mọi hợp đồng.",
    referenceSql="SELECT n.HoTen, c.DiaChi, t.GiaThueThucTe FROM thue t "
      "JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue "
      "JOIN canho c ON c.MaCanHo = t.MaCanHo;"),
  dict(id="m00-012", difficulty=2, topic="Join khoá chính-ngoại",
    q="Tìm HoTen người thuê căn hộ ở quận 'Thanh Xuân' (join thue-nguoithue-canho, lọc Quan).",
    referenceSql="SELECT DISTINCT n.HoTen FROM thue t "
      "JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue "
      "JOIN canho c ON c.MaCanHo = t.MaCanHo WHERE c.Quan = 'Thanh Xuân';"),

  # ---- C: Liên kết N-N — 1 người thuê nhiều căn hộ / 1 căn hộ nhiều người thuê ----
  dict(id="m00-013", difficulty=2, topic="Liên kết N-N",
    q="Tìm những người thuê (MaNguoiThue) đã thuê NHIỀU HƠN 1 căn hộ (GROUP BY + HAVING).",
    referenceSql="SELECT MaNguoiThue, COUNT(*) AS so_can_da_thue FROM thue GROUP BY MaNguoiThue HAVING COUNT(*) > 1;"),
  dict(id="m00-014", difficulty=2, topic="Liên kết N-N",
    q="Tìm những căn hộ (MaCanHo) đã được CHO THUÊ CHO NHIỀU HƠN 1 người khác nhau theo thời gian.",
    referenceSql="SELECT MaCanHo, COUNT(DISTINCT MaNguoiThue) AS so_nguoi_da_thue FROM thue GROUP BY MaCanHo HAVING COUNT(DISTINCT MaNguoiThue) > 1;"),
  dict(id="m00-015", difficulty=3, topic="Liên kết N-N",
    q="Lấy HoTen và danh sách DiaChi (dùng GROUP_CONCAT) của mọi căn hộ mà người đó đã từng thuê.",
    referenceSql="SELECT n.HoTen, GROUP_CONCAT(c.DiaChi, '; ') AS cac_can_ho FROM thue t "
      "JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue "
      "JOIN canho c ON c.MaCanHo = t.MaCanHo GROUP BY n.HoTen;"),

  # ---- D: Chênh lệch giá niêm yết vs giá thực tế (data-level) ----
  dict(id="m00-016", difficulty=2, topic="So sánh giá",
    q="So sánh GiaThueNiemYet (canho) với GiaThueThucTe (thue) cho từng hợp đồng — trả về DiaChi,"
      " GiaThueNiemYet, GiaThueThucTe, và chênh lệch (niêm yết - thực tế).",
    referenceSql="SELECT c.DiaChi, c.GiaThueNiemYet, t.GiaThueThucTe, "
      "c.GiaThueNiemYet - t.GiaThueThucTe AS chenh_lech "
      "FROM thue t JOIN canho c ON c.MaCanHo = t.MaCanHo;"),
  dict(id="m00-017", difficulty=2, topic="So sánh giá",
    q="Tìm các hợp đồng có GiaThueThucTe thấp hơn GiaThueNiemYet hơn 1.000.000 VNĐ (khách thuê được giảm giá đáng kể).",
    referenceSql="SELECT n.HoTen, c.DiaChi, c.GiaThueNiemYet, t.GiaThueThucTe FROM thue t "
      "JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue "
      "JOIN canho c ON c.MaCanHo = t.MaCanHo "
      "WHERE c.GiaThueNiemYet - t.GiaThueThucTe > 1000000;"),

  # ---- E: Aggregate theo nhóm ----
  dict(id="m00-018", difficulty=2, topic="Aggregate",
    q="Tính GiaThueNiemYet trung bình theo từng Quan trong bảng canho.",
    referenceSql="SELECT Quan, AVG(GiaThueNiemYet) AS gia_tb FROM canho GROUP BY Quan;"),
  dict(id="m00-019", difficulty=2, topic="Aggregate",
    q="Đếm số căn hộ theo từng Quan, sắp giảm dần theo số lượng.",
    referenceSql="SELECT Quan, COUNT(*) AS so_can FROM canho GROUP BY Quan ORDER BY so_can DESC;"),
  dict(id="m00-020", difficulty=2, topic="Aggregate",
    q="Tính tổng doanh thu thực tế (SUM GiaThueThucTe) theo từng người thuê (MaNguoiThue).",
    referenceSql="SELECT MaNguoiThue, SUM(GiaThueThucTe) AS tong_tien FROM thue GROUP BY MaNguoiThue;"),
  dict(id="m00-021", difficulty=2, topic="Aggregate",
    q="Tính diện tích trung bình (AVG DienTich) của các căn hộ theo từng Quan, chỉ giữ Quan có từ 2 căn hộ trở lên.",
    referenceSql="SELECT Quan, AVG(DienTich) AS dt_tb FROM canho GROUP BY Quan HAVING COUNT(*) >= 2;"),

  # ---- F: LEFT JOIN để lộ căn hộ chưa từng được thuê ----
  dict(id="m00-022", difficulty=2, topic="LEFT JOIN & NULL",
    q="LEFT JOIN canho với thue (qua MaCanHo) để tìm các căn hộ CHƯA TỪNG được thuê (không xuất hiện trong thue).",
    referenceSql="SELECT c.MaCanHo, c.DiaChi FROM canho c LEFT JOIN thue t ON t.MaCanHo = c.MaCanHo WHERE t.MaCanHo IS NULL;"),
  dict(id="m00-023", difficulty=2, topic="LEFT JOIN & NULL",
    q="LEFT JOIN nguoithue với thue để tìm người chưa từng thuê căn hộ nào.",
    referenceSql="SELECT n.MaNguoiThue, n.HoTen FROM nguoithue n LEFT JOIN thue t ON t.MaNguoiThue = n.MaNguoiThue WHERE t.MaNguoiThue IS NULL;"),

  # ---- G: Subquery ----
  dict(id="m00-024", difficulty=2, topic="Subquery",
    q="Tìm căn hộ có GiaThueNiemYet CAO HƠN giá trung bình của toàn bộ bảng canho.",
    referenceSql="SELECT DiaChi, GiaThueNiemYet FROM canho WHERE GiaThueNiemYet > (SELECT AVG(GiaThueNiemYet) FROM canho);"),
  dict(id="m00-025", difficulty=2, topic="Subquery",
    q="Tìm người thuê (HoTen) đã trả GiaThueThucTe cao nhất trong toàn bộ bảng thue.",
    referenceSql="SELECT n.HoTen, t.GiaThueThucTe FROM thue t JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue "
      "WHERE t.GiaThueThucTe = (SELECT MAX(GiaThueThucTe) FROM thue);"),
  dict(id="m00-026", difficulty=3, topic="Subquery",
    q="Tìm những người thuê (HoTen) CHỈ thuê căn hộ ở quận 'Cầu Giấy' (không có hợp đồng nào ở quận khác).",
    referenceSql="SELECT n.HoTen FROM nguoithue n WHERE n.MaNguoiThue IN (SELECT MaNguoiThue FROM thue) "
      "AND NOT EXISTS (SELECT 1 FROM thue t JOIN canho c ON c.MaCanHo = t.MaCanHo "
      "WHERE t.MaNguoiThue = n.MaNguoiThue AND c.Quan <> 'Cầu Giấy');"),

  # ---- H: ORDER BY / LIMIT ----
  dict(id="m00-027", difficulty=1, topic="ORDER BY/LIMIT",
    q="Lấy 2 căn hộ có diện tích lớn nhất (DiaChi, DienTich).",
    referenceSql="SELECT DiaChi, DienTich FROM canho ORDER BY DienTich DESC LIMIT 2;"),
  dict(id="m00-028", difficulty=1, topic="ORDER BY/LIMIT",
    q="Lấy người thuê trẻ tuổi nhất (NamSinh lớn nhất) — HoTen, NamSinh, chỉ 1 dòng.",
    referenceSql="SELECT HoTen, NamSinh FROM nguoithue ORDER BY NamSinh DESC LIMIT 1;"),

  # ---- I: CASE WHEN phân loại ----
  dict(id="m00-029", difficulty=2, topic="CASE WHEN",
    q="Phân loại căn hộ theo diện tích bằng CASE WHEN: <30 → 'nhỏ', 30-49 → 'vừa', >=50 → 'lớn'.",
    referenceSql="SELECT DiaChi, DienTich, CASE WHEN DienTich < 30 THEN 'nhỏ' WHEN DienTich < 50 THEN 'vừa' ELSE 'lớn' END AS loai FROM canho;"),
  dict(id="m00-030", difficulty=2, topic="CASE WHEN",
    q="Đếm số căn hộ theo từng loại (nhỏ/vừa/lớn) dùng lại logic CASE WHEN ở trên.",
    referenceSql="SELECT loai, COUNT(*) AS so_can FROM (SELECT CASE WHEN DienTich < 30 THEN 'nhỏ' "
      "WHEN DienTich < 50 THEN 'vừa' ELSE 'lớn' END AS loai FROM canho) GROUP BY loai;"),

  # ---- J: Chuẩn hoá & self-join minh hoạ cấu trúc bảng ----
  dict(id="m00-031", difficulty=3, topic="Self-join",
    q="Tìm các cặp người thuê (ten1,ten2) đã từng thuê CÙNG 1 căn hộ (không nhất thiết cùng lúc) —"
      " self-join bảng thue qua MaCanHo, MaNguoiThue1 < MaNguoiThue2 để tránh trùng cặp.",
    referenceSql="SELECT n1.HoTen AS ten1, n2.HoTen AS ten2, t1.MaCanHo FROM thue t1 "
      "JOIN thue t2 ON t1.MaCanHo = t2.MaCanHo AND t1.MaNguoiThue < t2.MaNguoiThue "
      "JOIN nguoithue n1 ON n1.MaNguoiThue = t1.MaNguoiThue "
      "JOIN nguoithue n2 ON n2.MaNguoiThue = t2.MaNguoiThue;"),
  dict(id="m00-032", difficulty=2, topic="Chuẩn hoá",
    q="Minh hoạ vì sao KHÔNG nên gộp cột HoTen vào bảng thue (tránh dư thừa): đếm xem HoTen"
      " 'Nguyễn Văn An' sẽ bị lặp lại bao nhiêu dòng nếu join thue với nguoithue.",
    referenceSql="SELECT n.HoTen, COUNT(*) AS so_dong_se_lap_lai FROM thue t "
      "JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue "
      "WHERE n.HoTen = 'Nguyễn Văn An' GROUP BY n.HoTen;"),

  # ---- K: Tổng hợp cuối ----
  dict(id="m00-033", difficulty=3, topic="Tổng hợp",
    q="Với mỗi quận (Quan), tính số hợp đồng thuê đã ký (join canho-thue qua MaCanHo, GROUP BY Quan).",
    referenceSql="SELECT c.Quan, COUNT(*) AS so_hop_dong FROM thue t JOIN canho c ON c.MaCanHo = t.MaCanHo GROUP BY c.Quan;"),
  dict(id="m00-034", difficulty=3, topic="Tổng hợp",
    q="Tìm quận (Quan) có tổng doanh thu thực tế (SUM GiaThueThucTe) cao nhất.",
    referenceSql="SELECT c.Quan, SUM(t.GiaThueThucTe) AS tong_doanh_thu FROM thue t JOIN canho c ON c.MaCanHo = t.MaCanHo "
      "GROUP BY c.Quan ORDER BY tong_doanh_thu DESC LIMIT 1;"),
  dict(id="m00-035", difficulty=2, topic="Tổng hợp",
    q="Liệt kê HoTen, DiaChi, NgayBatDau, NgayKetThuc của các hợp đồng ĐÃ KẾT THÚC (NgayKetThuc"
      " khác NULL), sắp theo NgayBatDau tăng dần.",
    referenceSql="SELECT n.HoTen, c.DiaChi, t.NgayBatDau, t.NgayKetThuc FROM thue t "
      "JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue "
      "JOIN canho c ON c.MaCanHo = t.MaCanHo "
      "WHERE t.NgayKetThuc IS NOT NULL ORDER BY t.NgayBatDau;"),
  dict(id="m00-036", difficulty=2, topic="Tổng hợp",
    q="Tính độ tuổi gần đúng của từng người thuê tại năm 2026 (2026 - NamSinh), trả về HoTen, tuoi.",
    referenceSql="SELECT HoTen, 2026 - NamSinh AS tuoi FROM nguoithue;"),
  dict(id="m00-037", difficulty=2, topic="Tổng hợp",
    q="Tìm các căn hộ có GiaThueNiemYet trong khoảng [7000000, 10000000] (BETWEEN).",
    referenceSql="SELECT DiaChi, GiaThueNiemYet FROM canho WHERE GiaThueNiemYet BETWEEN 7000000 AND 10000000;"),
  dict(id="m00-038", difficulty=2, topic="Tổng hợp",
    q="Tìm các căn hộ có DiaChi chứa chữ 'Cầu' (LIKE '%Cầu%').",
    referenceSql="SELECT DiaChi FROM canho WHERE DiaChi LIKE '%Cầu%';"),
  dict(id="m00-039", difficulty=3, topic="Tổng hợp",
    q="Với mỗi người thuê, tính số ngày đã thuê CĂN HỘ ĐẦU TIÊN của họ (NgayKetThuc - NgayBatDau,"
      " dùng julianday; chỉ tính các hợp đồng đã có NgayKetThuc).",
    referenceSql="SELECT MaNguoiThue, MaCanHo, "
      "CAST(julianday(NgayKetThuc) - julianday(NgayBatDau) AS INTEGER) AS so_ngay "
      "FROM thue WHERE NgayKetThuc IS NOT NULL;"),
  dict(id="m00-040", difficulty=2, topic="Tổng hợp",
    q="Tìm người thuê có SDT bắt đầu bằng '090' và sinh trước năm 1996.",
    referenceSql="SELECT HoTen, SDT, NamSinh FROM nguoithue WHERE SDT LIKE '090%' AND NamSinh < 1996;"),

  # ---- L: 10 bài bổ sung để đủ đa dạng dạng bài ----
  dict(id="m00-041", difficulty=1, topic="Cơ bản",
    q="Tìm căn hộ có MaCanHo = 102 (SELECT * duy nhất 1 dòng).",
    referenceSql="SELECT * FROM canho WHERE MaCanHo = 102;"),
  dict(id="m00-042", difficulty=2, topic="Join khoá chính-ngoại",
    q="Tìm DiaChi các căn hộ mà người tên 'Lê Minh Châu' đã từng thuê.",
    referenceSql="SELECT c.DiaChi FROM thue t JOIN canho c ON c.MaCanHo = t.MaCanHo "
      "JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue WHERE n.HoTen = 'Lê Minh Châu';"),
  dict(id="m00-043", difficulty=2, topic="Aggregate",
    q="Tính số lượng hợp đồng (COUNT) đã ký theo từng năm bắt đầu (lấy 4 ký tự đầu NgayBatDau).",
    referenceSql="SELECT SUBSTR(NgayBatDau,1,4) AS nam, COUNT(*) AS so_hop_dong FROM thue GROUP BY nam;"),
  dict(id="m00-044", difficulty=2, topic="Subquery",
    q="Tìm căn hộ có diện tích nhỏ hơn diện tích TRUNG BÌNH của các căn hộ ở quận 'Cầu Giấy'.",
    referenceSql="SELECT DiaChi, DienTich FROM canho WHERE DienTich < "
      "(SELECT AVG(DienTich) FROM canho WHERE Quan = 'Cầu Giấy');"),
  dict(id="m00-045", difficulty=2, topic="LEFT JOIN & NULL",
    q="LEFT JOIN để liệt kê MỌI người thuê kèm tổng số hợp đồng họ đã ký (0 nếu chưa từng thuê).",
    referenceSql="SELECT n.HoTen, COUNT(t.MaCanHo) AS so_hop_dong FROM nguoithue n "
      "LEFT JOIN thue t ON t.MaNguoiThue = n.MaNguoiThue GROUP BY n.HoTen;"),
  dict(id="m00-046", difficulty=3, topic="Tổng hợp",
    q="Tìm người thuê đã ký hợp đồng ở ÍT NHẤT 2 quận khác nhau.",
    referenceSql="SELECT n.HoTen FROM nguoithue n JOIN thue t ON t.MaNguoiThue = n.MaNguoiThue "
      "JOIN canho c ON c.MaCanHo = t.MaCanHo GROUP BY n.HoTen HAVING COUNT(DISTINCT c.Quan) >= 2;"),
  dict(id="m00-047", difficulty=2, topic="CASE WHEN",
    q="Gắn nhãn hợp đồng 'đang thuê' (NgayKetThuc IS NULL) hay 'đã kết thúc' cho từng dòng thue.",
    referenceSql="SELECT MaNguoiThue, MaCanHo, CASE WHEN NgayKetThuc IS NULL THEN 'đang thuê' ELSE 'đã kết thúc' END AS trang_thai FROM thue;"),
  dict(id="m00-048", difficulty=2, topic="Tổng hợp",
    q="Tính GiaThueThucTe trung bình CHỈ của các hợp đồng đã kết thúc (NgayKetThuc IS NOT NULL).",
    referenceSql="SELECT AVG(GiaThueThucTe) AS gia_tb_da_ket_thuc FROM thue WHERE NgayKetThuc IS NOT NULL;"),
  dict(id="m00-049", difficulty=3, topic="Tổng hợp",
    q="Xếp hạng (ORDER BY) các người thuê theo tổng tiền đã trả (SUM GiaThueThucTe) giảm dần, lấy top 3.",
    referenceSql="SELECT n.HoTen, SUM(t.GiaThueThucTe) AS tong_tien FROM thue t "
      "JOIN nguoithue n ON n.MaNguoiThue = t.MaNguoiThue "
      "GROUP BY n.HoTen ORDER BY tong_tien DESC LIMIT 3;"),
  dict(id="m00-050", difficulty=3, topic="Tổng hợp",
    q="Bài tổng hợp cuối: với mỗi quận, tính số căn hộ, số hợp đồng, và doanh thu trung bình mỗi"
      " hợp đồng (SUM/COUNT), chỉ giữ quận có ít nhất 1 hợp đồng.",
    referenceSql="SELECT c.Quan, COUNT(DISTINCT c.MaCanHo) AS so_can, COUNT(t.MaCanHo) AS so_hop_dong, "
      "AVG(t.GiaThueThucTe) AS doanh_thu_tb FROM canho c JOIN thue t ON t.MaCanHo = c.MaCanHo "
      "GROUP BY c.Quan;"),
]

assert len(QUESTIONS) == 50, f"Expected 50 questions, got {len(QUESTIONS)}"
assert len({q['id'] for q in QUESTIONS}) == 50, "Duplicate ids found"
