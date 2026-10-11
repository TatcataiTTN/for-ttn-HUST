-- Schema & dữ liệu SQL Sandbox — Module 00 (Nền tảng CSDL quan hệ & ER)
-- Ví dụ "Người thuê — Thuê — Căn hộ" đúng như bài m02 Bổ sung trong exercises.json Module 00:
-- 3 bảng: NguoiThue (thực thể), CanHo (thực thể), Thue (bảng trung gian cho liên kết N-N có
-- thuộc tính riêng NgayBatDau/NgayKetThuc/GiaThueThucTe — đúng lời giải bài tập làm giấy đã có).
-- Dữ liệu là dữ liệu MINH HOẠ tự soạn (ghi rõ), dùng để luyện JOIN/khoá chính-khoá ngoại/N-N.

DROP TABLE IF EXISTS thue; DROP TABLE IF EXISTS canho; DROP TABLE IF EXISTS nguoithue;

CREATE TABLE nguoithue (MaNguoiThue INTEGER PRIMARY KEY, HoTen TEXT, SDT TEXT, NamSinh INTEGER);
CREATE TABLE canho (MaCanHo INTEGER PRIMARY KEY, DiaChi TEXT, Quan TEXT, DienTich REAL, GiaThueNiemYet REAL);
CREATE TABLE thue (MaNguoiThue INTEGER, MaCanHo INTEGER, NgayBatDau TEXT, NgayKetThuc TEXT, GiaThueThucTe REAL,
  PRIMARY KEY (MaNguoiThue, MaCanHo, NgayBatDau),
  FOREIGN KEY (MaNguoiThue) REFERENCES nguoithue(MaNguoiThue),
  FOREIGN KEY (MaCanHo) REFERENCES canho(MaCanHo));

INSERT INTO nguoithue VALUES
 (1,'Nguyễn Văn An','0901111111',1995),
 (2,'Trần Thị Bình','0902222222',1998),
 (3,'Lê Minh Châu','0903333333',1990),
 (4,'Phạm Thu Dung','0904444444',2000),
 (5,'Hoàng Văn Em','0905555555',1993),
 (6,'Vũ Thị Phượng','0906666666',1997);  -- chưa từng thuê căn hộ nào (minh hoạ LEFT JOIN tìm "chưa có liên kết")

INSERT INTO canho VALUES
 (101,'12 Láng Hạ','Đống Đa',35.0,8000000),
 (102,'45 Cầu Giấy','Cầu Giấy',50.0,11000000),
 (103,'78 Nguyễn Trãi','Thanh Xuân',28.0,6500000),
 (104,'9 Trần Duy Hưng','Cầu Giấy',60.0,14000000),
 (105,'22 Hoàng Quốc Việt','Cầu Giấy',40.0,9000000),
 (106,'5 Dương Đình Nghệ','Cầu Giấy',45.0,10000000);  -- chưa từng được thuê (minh hoạ LEFT JOIN tìm "chưa có liên kết")

-- 1 người có thể thuê nhiều căn hộ theo thời gian (N-N có thuộc tính NgayBatDau/GiaThueThucTe)
INSERT INTO thue VALUES
 (1,101,'2023-01-01','2023-12-31',7800000),
 (1,103,'2024-01-01','2024-12-31',6300000),
 (2,102,'2023-06-01','2024-05-31',9800000),  -- chủ động giảm giá nhiều (1.2 triệu) để minh hoạ bài m00-017
 (3,104,'2022-01-01','2023-12-31',13500000),
 (3,105,'2024-01-01',NULL,8800000),   -- đang thuê, chưa kết thúc (NULL = chưa biết ngày kết thúc)
 (4,101,'2024-01-01','2024-12-31',8000000),
 (5,103,'2023-01-01','2023-06-30',6500000);
