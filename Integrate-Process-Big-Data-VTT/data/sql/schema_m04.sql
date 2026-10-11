-- Schema & dữ liệu SQL Sandbox — Module 04 (Record Linkage & Entity Resolution)
-- Mô phỏng đúng ví dụ "2 website rao vặt bất động sản cùng đăng 1 căn hộ, giá lệch ~5%" đã nêu
-- trong Quiz-Buoi4-RecordLinkage-ER.md câu D2 — dữ liệu MINH HOẠ tự soạn (gắn nhãn rõ), dùng để
-- luyện Blocking (lọc ứng viên) và Matching (so khớp gần đúng) bằng SQL thuần (không cần UDF).

DROP TABLE IF EXISTS nguon_a; DROP TABLE IF EXISTS nguon_b;

CREATE TABLE nguon_a (id INTEGER PRIMARY KEY, tieu_de TEXT, dia_chi TEXT, quan TEXT, dien_tich REAL, gia_trieu REAL, sdt TEXT);
CREATE TABLE nguon_b (id INTEGER PRIMARY KEY, ten_tin TEXT, khu_vuc TEXT, quan TEXT, dt_m2 REAL, gia_rao_trieu REAL, lien_he TEXT);

-- nguon_a: 10 tin đăng, mô phỏng batdongsan.com.vn
INSERT INTO nguon_a VALUES
 (1,'Cho thuê căn hộ 12 Láng Hạ, 35m2, đầy đủ nội thất','12 Láng Hạ','Đống Đa',35.0,8.0,'0901111111'),
 (2,'Căn hộ 45 Cầu Giấy view đẹp, 50m2','45 Cầu Giấy','Cầu Giấy',50.0,11.0,'0902222222'),
 (3,'Phòng trọ 78 Nguyễn Trãi giá rẻ','78 Nguyễn Trãi','Thanh Xuân',28.0,6.5,'0903333333'),
 (4,'Căn hộ cao cấp 9 Trần Duy Hưng, 60m2','9 Trần Duy Hưng','Cầu Giấy',60.0,14.0,'0904444444'),
 (5,'Chung cư mini 22 Hoàng Quốc Việt','22 Hoàng Quốc Việt','Cầu Giấy',40.0,9.0,'0905555555'),
 (6,'Nhà nguyên căn Linh Đàm, 80m2','Khu đô thị Linh Đàm','Hoàng Mai',80.0,18.0,'0906666666'),
 (7,'Căn hộ Mỹ Đình 2PN, 65m2','Mỹ Đình','Nam Từ Liêm',65.0,15.0,'0907777777'),
 (8,'Studio Hào Nam giá tốt','12 Hào Nam','Đống Đa',25.0,5.5,'0908888888'),
 (9,'Căn hộ Royal City','72A Nguyễn Trãi','Thanh Xuân',70.0,20.0,'0909999999'),
 (10,'Nhà trọ sinh viên Cầu Giấy','100 Cầu Giấy','Cầu Giấy',20.0,3.5,'0900000000');

-- nguon_b: 10 tin, mô phỏng nhatot.com — 7 tin trùng thực thể với nguon_a (giá lệch ~5-10%, địa
-- chỉ/tên viết khác chút), 3 tin độc lập không trùng (minh hoạ cả match lẫn non-match thật)
INSERT INTO nguon_b VALUES
 (201,'CC 12 Lang Ha full noi that','12 Lang Ha','Đống Đa',35.0,8.4,'0901111111'),       -- trùng id=1, giá lệch +5%
 (202,'Can ho Cau Giay 50m2 view dep','45 Cau Giay','Cầu Giấy',50.0,10.5,'0902222222'),   -- trùng id=2, giá lệch -4.5%
 (203,'Phong tro Nguyen Trai','78 Nguyen Trai','Thanh Xuân',28.0,6.8,'0903333333'),       -- trùng id=3, giá lệch +4.6%
 (204,'Can ho Tran Duy Hung cao cap','9 Tran Duy Hung','Cầu Giấy',60.0,14.5,'0904444444'), -- trùng id=4
 (205,'Chung cu mini Hoang Quoc Viet','22 Hoang Quoc Viet','Cầu Giấy',40.0,8.7,'0905555555'), -- trùng id=5
 (206,'Nha Linh Dam 80m2','KĐT Linh Đàm','Hoàng Mai',80.0,17.5,'0906666666'),             -- trùng id=6
 (207,'Studio Hao Nam','12 Hao Nam','Đống Đa',25.0,5.7,'0908888888'),                     -- trùng id=8 (khác thứ tự xuất hiện)
 (208,'Can ho Van Phu Ha Dong','Van Phu','Hà Đông',55.0,10.0,'0911111111'),               -- KHÔNG trùng (chỉ có ở nguon_b)
 (209,'Nha mat pho Kim Ma','Kim Ma','Ba Đình',45.0,25.0,'0912222222'),                    -- KHÔNG trùng
 (210,'Can ho Time City','458 Minh Khai','Hai Bà Trưng',68.0,19.0,'0913333333');          -- KHÔNG trùng
