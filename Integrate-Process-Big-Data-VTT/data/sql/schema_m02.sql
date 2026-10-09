-- Schema & dữ liệu SQL Sandbox — Module 02 (Schema Alignment)
-- Lược đồ các bảng S1..S7 lấy ĐÚNG NGUYÊN VĂN từ slide "2_SchemaAlignment.pdf" (trang 6-9,
-- "Schema Heterogeneity by Example" / "Table and Attribute Naming" / "Tabular Organization" /
-- "Schema Coverage") — xác minh bằng pdftotext trực tiếp từ file slide gốc:
--   Mediated Schema: Movie(title,director,year,genre) · Actors(title,name) ·
--                     Plays(movie,location,startTime) · Reviews(title,rating,description)
--   S1: Movie(title,director,year,genre); Actor(AID,firstName,lastName,nationality,yearofBirth);
--       ActorPlays(AID,MID); MovieDetails(MID,director,genre,year)
--   S2: Cinemas(place,movie,start)
--   S3: NYCCinemas(name,title,startTime)
--   S4: Reviews(title,date,grade,review)
--   S5: MovieGenres(title,genre)
--   S6: MovieDirectors(title,dir)
--   S7: MovieYears(title,year)
--
-- DỮ LIỆU (các dòng INSERT) là dữ liệu MINH HOẠ do người soạn tự tạo (gắn nhãn rõ trong trang web
-- là "dữ liệu minh hoạ"), dùng 10 phim thật quen thuộc để bài tập có ngữ cảnh dễ hiểu — slide gốc
-- không có dữ liệu mẫu cụ thể, chỉ có lược đồ bảng.

DROP TABLE IF EXISTS s1_movie; DROP TABLE IF EXISTS s1_actor; DROP TABLE IF EXISTS s1_actorplays; DROP TABLE IF EXISTS s1_moviedetails;
DROP TABLE IF EXISTS s2_cinemas; DROP TABLE IF EXISTS s3_nyccinemas; DROP TABLE IF EXISTS s4_reviews;
DROP TABLE IF EXISTS s5_moviegenres; DROP TABLE IF EXISTS s6_moviedirectors; DROP TABLE IF EXISTS s7_movieyears;

CREATE TABLE s1_movie (title TEXT, director TEXT, year INTEGER, genre TEXT);
CREATE TABLE s1_actor (AID INTEGER PRIMARY KEY, firstName TEXT, lastName TEXT, nationality TEXT, yearofBirth INTEGER);
CREATE TABLE s1_actorplays (AID INTEGER, MID INTEGER);
CREATE TABLE s1_moviedetails (MID INTEGER PRIMARY KEY, director TEXT, genre TEXT, year INTEGER);

CREATE TABLE s2_cinemas (place TEXT, movie TEXT, start TEXT);
CREATE TABLE s3_nyccinemas (name TEXT, title TEXT, startTime TEXT);
CREATE TABLE s4_reviews (title TEXT, date TEXT, grade INTEGER, review TEXT);
CREATE TABLE s5_moviegenres (title TEXT, genre TEXT);
CREATE TABLE s6_moviedirectors (title TEXT, dir TEXT);
CREATE TABLE s7_movieyears (title TEXT, year INTEGER);

-- S1.Movie — 10 phim (title, director, year, genre)
INSERT INTO s1_movie VALUES
 ('Parasite','Bong Joon-ho',2019,'Drama'),
 ('Inception','Christopher Nolan',2010,'SciFi'),
 ('The Godfather','Francis Ford Coppola',1972,'Crime'),
 ('Spirited Away','Hayao Miyazaki',2001,'Animation'),
 ('Oldboy','Park Chan-wook',2003,'Thriller'),
 ('Interstellar','Christopher Nolan',2014,'SciFi'),
 ('Memento','Christopher Nolan',2000,'Thriller'),
 ('Your Name','Makoto Shinkai',2016,'Animation'),
 ('Train to Busan','Yeon Sang-ho',2016,'Horror'),
 ('The Dark Knight','Christopher Nolan',2008,'Action');

-- S1.Actor — diễn viên (độc lập, dùng AID riêng của nguồn này)
INSERT INTO s1_actor VALUES
 (1,'Song','Kang-ho','South Korea',1967),
 (2,'Leonardo','DiCaprio','USA',1974),
 (3,'Marlon','Brando','USA',1924),
 (4,'Choi','Min-sik','South Korea',1962),
 (5,'Christian','Bale','UK',1974);

-- S1.MovieDetails — MID độc lập của nguồn S1 (không trùng AID), map 1-1 với 1 phim trong s1_movie
INSERT INTO s1_moviedetails VALUES
 (101,'Bong Joon-ho','Drama',2019),
 (102,'Christopher Nolan','SciFi',2010),
 (103,'Francis Ford Coppola','Crime',1972),
 (104,'Park Chan-wook','Thriller',2003),
 (105,'Christopher Nolan','Action',2008);

-- S1.ActorPlays — nối Actor.AID với MovieDetails.MID
INSERT INTO s1_actorplays VALUES (1,101),(2,102),(3,103),(4,104),(5,105);

-- S2.Cinemas — rạp (place, movie, start) - giờ dạng chuỗi 'HH:MM'
INSERT INTO s2_cinemas VALUES
 ('BHD Thanh Xuan','Parasite','19:30'),
 ('CGV Vincom','Inception','20:00'),
 ('Lotte Lieu Giai','The Dark Knight','18:45'),
 ('BHD Thanh Xuan','Interstellar','21:00'),
 ('CGV Vincom','Your Name','17:15');

-- S3.NYCCinemas — (name, title, startTime) — chỉ phim chiếu ở NYC (tập con khác của S2)
INSERT INTO s3_nyccinemas VALUES
 ('AMC Lincoln Square','Parasite','19:00'),
 ('Film Forum','Oldboy','21:30'),
 ('IFC Center','Memento','18:00');

-- S4.Reviews — (title, date, grade 1-10, review text)
INSERT INTO s4_reviews VALUES
 ('Parasite','2019-05-30',9,'Dark social satire, flawless pacing'),
 ('Parasite','2019-06-02',8,'Brilliant class commentary'),
 ('Inception','2010-07-16',8,'Mind-bending but a bit cold'),
 ('The Godfather','1972-03-24',10,'Genre-defining masterpiece'),
 ('Oldboy','2003-11-21',9,'Brutal and unforgettable'),
 ('Interstellar','2014-11-07',7,'Visually stunning, plot stretches logic'),
 ('Memento','2000-09-05',8,'Clever reverse structure'),
 ('The Dark Knight','2008-07-18',9,'Heath Ledger steals the film');

-- S5.MovieGenres — (title, genre), nguồn chỉ biết thể loại, không biết đạo diễn/năm
INSERT INTO s5_moviegenres VALUES
 ('Parasite','Drama'),('Inception','SciFi'),('The Godfather','Crime'),
 ('Spirited Away','Animation'),('Oldboy','Thriller'),('Interstellar','SciFi'),
 ('Memento','Thriller'),('Your Name','Animation'),('Train to Busan','Horror'),
 ('The Dark Knight','Action');

-- S6.MovieDirectors — (title, dir), nguồn chỉ biết đạo diễn — CHÚ Ý: thiếu 'Train to Busan'
-- (minh hoạ đúng ý "Different coverage" của slide — không phải nguồn nào cũng biết hết mọi phim).
-- CHÚ Ý 2: dòng 'The Godfather' CỐ TÌNH ghi sai director ('Martin Scorsese' thay vì đúng
-- 'Francis Ford Coppola') — đây là xung đột dữ liệu GIỮA 2 NGUỒN được cài có chủ đích, dùng cho
-- bài m02-015/m02-016 minh hoạ đúng vấn đề Certain Answers khi 2 nguồn không đồng thuận.
INSERT INTO s6_moviedirectors VALUES
 ('Parasite','Bong Joon-ho'),('Inception','Christopher Nolan'),('The Godfather','Martin Scorsese'),
 ('Spirited Away','Hayao Miyazaki'),('Oldboy','Park Chan-wook'),('Interstellar','Christopher Nolan'),
 ('Memento','Christopher Nolan'),('Your Name','Makoto Shinkai'),('The Dark Knight','Christopher Nolan');

-- S7.MovieYears — (title, year), nguồn chỉ biết năm — cũng thiếu 'Train to Busan'
INSERT INTO s7_movieyears VALUES
 ('Parasite',2019),('Inception',2010),('The Godfather',1972),('Spirited Away',2001),
 ('Oldboy',2003),('Interstellar',2014),('Memento',2000),('Your Name',2016),('The Dark Knight',2008);
