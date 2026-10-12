# -*- coding: utf-8 -*-
"""Cân bằng độ dài đáp án quiz hd-03 đến hd-07 (xem hd_quiz_fix_a.py). Mỗi mục: câu hỏi -> (đáp án đúng mới hoặc None, [3 đáp án nhiễu])."""

QFIX_B = {
 # ------------------------------------------------------------------ hd-03
 "Apache Pig ra đời ở đâu, với mục tiêu gì?": (None, [
   "Facebook, để thay thế hoàn toàn SQL bằng một ngôn ngữ dataflow mới cho nhà phân tích",
   "Google, để thay thế GFS bằng một hệ file phân tán nhanh hơn trên nhiều máy",
   "LinkedIn, để xử lý luồng hoạt động người dùng theo thời gian thực cho nhiều ứng dụng"]),
 "PigLatin được thiết kế nằm ở đâu trên phổ 'khai báo (SQL) - thủ tục (MapReduce)'?": (None, [
   "Hoàn toàn khai báo như SQL: người dùng chỉ mô tả kết quả, không mô tả thứ tự các bước",
   "Hoàn toàn thủ tục như MapReduce Java thuần: người dùng tự viết từng hàm map và reduce",
   "Không nằm trên phổ này vì PigLatin là ngôn ngữ truy vấn đồ thị chứ không phải dataflow"]),
 "Trong PigLatin, vì sao đổi thứ tự FILTER và GROUP BY có thể cho kết quả khác nhau?": (None, [
   "Vì PigLatin không hỗ trợ lệnh GROUP BY nên thứ tự các lệnh không có ý nghĩa gì",
   "Vì FILTER chỉ dùng được ngay sau JOIN, nên đổi thứ tự sẽ gây lỗi cú pháp",
   "Không có khác biệt gì, hai thứ tự luôn cho kết quả giống hệt nhau trong mọi trường hợp"]),
 "Động lực chính khiến Facebook xây Hive là gì?": (None, [
   "Muốn thay thế hoàn toàn MapReduce bằng một công nghệ xử lý mới nhanh hơn cho toàn bộ kho dữ liệu",
   "Google yêu cầu Facebook dùng ngôn ngữ truy vấn tương thích chuẩn nội bộ để trao đổi dữ liệu",
   "Muốn giảm chi phí phần cứng bằng cách chuyển toàn bộ kho dữ liệu sang cơ sở dữ liệu quan hệ"]),
 "Theo nguồn lịch sử, tỉ lệ nhân sự Facebook dùng hạ tầng phân tích dữ liệu mỗi tháng đã thay đổi ra sao?": (None, [
   "Giữ nguyên ở mức 6 người dùng vì chỉ đội hạ tầng mới được phép truy cập dữ liệu",
   "Giảm dần theo thời gian vì dữ liệu quá lớn khiến truy vấn ngày càng chậm hơn",
   "Tăng lên 100% nhân sự ngay trong năm đầu nhờ Hive tự động hoá mọi phân tích"]),
 "Sự khác biệt cốt lõi giữa PigLatin và HiveQL là gì?": (None, [
   "Không có khác biệt thực chất, đây là cùng một ngôn ngữ do hai công ty đặt tên khác nhau",
   "PigLatin chỉ chạy được trên Spark còn HiveQL chạy trên MapReduce, ngoài ra giống hệt nhau",
   "HiveQL không hỗ trợ GROUP BY và JOIN nên chỉ dùng được cho truy vấn một bảng đơn giản"]),
 "Trong ví dụ JOIN giữa bảng orders và employees, nếu dùng inner join mặc định, nhân viên E3 (chưa có đơn hàng nào) có xuất hiện trong kết quả không?": (None, [
   "Có, E3 luôn xuất hiện với các cột của bảng orders mang giá trị NULL",
   "Có, nhưng chỉ xuất hiện đúng một lần dù E3 có thể có nhiều đơn hàng",
   "Tuỳ vào việc dùng PigLatin hay HiveQL: Pig giữ lại, Hive loại bỏ"]),
 "Cả script PigLatin và HiveQL cho bài toán tổng doanh số theo nhân viên, sau khi biên dịch, đều chuyển thành gì bên dưới?": (None, [
   "Một truy vấn SQL gửi trực tiếp tới cơ sở dữ liệu quan hệ rồi trả kết quả về cho Hive",
   "Mã máy được biên dịch trực tiếp và chạy ngoài YARN, không còn liên quan tới MapReduce",
   "Không cần biên dịch, script được NameNode thông dịch và chạy trực tiếp trên các DataNode"]),
 "UDF (User-Defined Function) được dùng khi nào?": (None, [
   "Khi muốn thay thế hoàn toàn HiveQL hoặc PigLatin bằng chương trình Java viết tay cho mọi việc",
   "Chỉ khi dùng trong Pig; Hive không cho người dùng tự định nghĩa hàm bất kỳ nào",
   "Khi dữ liệu quá nhỏ để chạy MapReduce, UDF cho phép xử lý trên một máy duy nhất"]),
 "Partition trong Hive chia dữ liệu theo cơ chế nào?": (None, [
   "Theo hash(cột) mod số-phần, chia đều dữ liệu bất kể giá trị thật của cột",
   "Theo thứ tự ghi dữ liệu vào bảng: mỗi lô ghi tạo thành một thư mục con riêng",
   "Không chia gì cả: Hive luôn quét toàn bảng và chỉ lọc kết quả ở bước cuối"]),
 "Vì sao partition theo 1 cột có hàng triệu giá trị khác nhau (vd user_id) là lựa chọn tồi?": (None, [
   "Vì Hive không hỗ trợ cột kiểu số nguyên lớn, nên các cột như user_id không partition được",
   "Vì partition chỉ dùng được với cột kiểu ngày tháng, còn cột khác sẽ báo lỗi khi tạo bảng",
   "Vì partition tạo ra quá ít thư mục nên không giúp lọc được dữ liệu khi truy vấn"]),
 "Bucket khác Partition ở điểm cốt lõi nào?": (None, [
   "Bucket chỉ dùng được trong Pig, còn Partition mới là cơ chế dùng trong Hive",
   "Bucket và Partition là cùng một cơ chế, chỉ khác tên gọi giữa các phiên bản Hive",
   "Bucket chia theo giá trị thật của cột như Partition, nhưng không tạo thư mục con trên HDFS"]),
 "Stinger Initiative (Hortonworks) có mục tiêu gì, và gồm mấy 'wave'?": (None, [
   "Thay HiveQL bằng một ngôn ngữ truy vấn mới hoàn toàn, chỉ qua 1 wave duy nhất",
   "Xây một hệ quản trị cơ sở dữ liệu hoàn toàn mới, không liên quan tới Hive",
   "Giảm chi phí lưu trữ HDFS xuống còn một phần ba, không liên quan tới tốc độ truy vấn"]),
 "Apache Tez khác MapReduce ở điểm cốt lõi nào, giúp Hive nhanh hơn?": (None, [
   "Tez không chạy trên YARN mà có bộ lập lịch riêng, nên không cần xin tài nguyên từ cụm",
   "Tez chỉ hỗ trợ truy vấn trên một bảng duy nhất nên tránh được bước JOIN tốn kém",
   "Tez thay thế hoàn toàn HDFS bằng bộ nhớ trong, nên dữ liệu không còn lưu lâu dài trên đĩa"]),
 "Thành phần nào của Hive có ảnh hưởng lâu dài nhất, được cả Presto/Trino/Spark SQL tương thích ngày nay?": (None, [
   "Cú pháp HiveQL với các câu lệnh SELECT, JOIN, GROUP BY quen thuộc",
   "Giao diện web của Hive dùng để gửi truy vấn và xem kết quả",
   "Thuật toán tối ưu truy vấn riêng của Hive, được Presto sao chép nguyên"]),
 "Vì sao Hive thế hệ đầu (chạy trên MapReduce) không phù hợp cho truy vấn tương tác nhanh?": (None, [
   "Vì HiveQL không hỗ trợ lệnh SELECT nên không thể truy vấn dữ liệu một cách trực tiếp",
   "Vì Hive thế hệ đầu không đọc được dữ liệu từ HDFS mà chỉ đọc từ cơ sở dữ liệu quan hệ",
   "Vì Hive thế hệ đầu chỉ chạy được trên một node duy nhất nên không xử lý được dữ liệu lớn"]),
 "Theo bài học kiến trúc rút ra từ cả Hive Metastore và việc chuyển MapReduce→Tez, điều gì giúp Hive 'sống' qua nhiều thế hệ công nghệ xử lý khác nhau?": (None, [
   "Vì HiveQL không bao giờ thay đổi cú pháp, nên mọi thế hệ công nghệ đều chạy được cùng một lớp mã",
   "Vì Hive chỉ chạy trên phần cứng của Facebook nên không bị ảnh hưởng bởi thay đổi công nghệ bên ngoài",
   "Vì Hive không phụ thuộc vào Hadoop nên có thể chuyển sang bất kỳ nền tảng tính toán nào ngay lập tức"]),
 "Điểm khác nhau chính giữa bài đếm URL và bài đồ thị liên kết ngược ở bước reduce là gì?": (None, [
   "Đếm URL không cần shuffle, còn đồ thị liên kết ngược bắt buộc phải shuffle dữ liệu",
   "Đồ thị liên kết ngược không cần hàm map, chỉ cần một hàm reduce duy nhất",
   "Hai bài hoàn toàn giống nhau, chỉ khác tên các cột trong dữ liệu đầu vào"]),
 "Pig và Hive liên hệ thế nào với MapReduce theo cách nhìn của module này?": (None, [
   "Thay thế hoàn toàn MapReduce nên không còn dịch ra job và không còn chi phí shuffle nào",
   "Chỉ dùng cho dữ liệu nhỏ nên không bao giờ sinh ra job MapReduce trên cụm lớn",
   "Không liên quan tới Hadoop vì chạy trên một máy riêng rồi mới đẩy kết quả lên HDFS"]),

 # ------------------------------------------------------------------ hd-04
 "Công ty nào ban đầu xây dựng HBase, và để giải quyết bài toán gì?": (None, [
   "Facebook, cho hệ thống nhắn tin Messages quy mô lớn",
   "Cloudera, cho các tác vụ ETL của khách hàng doanh nghiệp",
   "LinkedIn, cho luồng hoạt động người dùng thời gian thực"]),
 "Khác biệt chính giữa HBase và RDBMS truyền thống là gì?": (None, [
   "HBase nhanh hơn RDBMS ở mọi tác vụ, kể cả truy vấn phân tích phức tạp nhiều bảng",
   "HBase không lưu được bảng lớn, chỉ phù hợp với dữ liệu dưới vài chục gigabyte",
   "HBase chỉ chạy được trên một máy duy nhất nên phải dùng RDBMS cho dữ liệu phân tán"]),
 "Trong mô hình Bigtable/HBase, điều gì KHÔNG cần khai báo trước schema, khác với RDBMS?": (None, [
   "Row key (khoá dùng để định danh từng hàng trong bảng)",
   "Column family (nhóm cột được lưu cùng nhau trên đĩa)",
   "Tên bảng (định danh bảng trong không gian tên của HBase)"]),
 "Region trong HBase được chia theo tiêu chí gì?": (None, [
   "Theo column family: mỗi family là một Region riêng",
   "Theo số lượng cột: mỗi Region chứa số cột bằng nhau",
   "Theo thời gian tạo dữ liệu: mỗi Region là một ngày"]),
 "Vì sao 1 bảng có mọi row key mới đều tăng dần (vd timestamp làm tiền tố) dễ gây hotspot?": (None, [
   "Vì row key quá dài nên NameNode không lưu hết được metadata của các hàng mới",
   "Vì HBase không hỗ trợ lưu các số tăng dần nên các hàng mới bị ghi đè lên nhau",
   "Vì column family của các hàng mới bị trùng nên các RegionServer phải gộp lại liên tục"]),
 "Kỹ thuật 'salting' trong thiết kế row key HBase làm gì?": (None, [
   "Mã hoá dữ liệu trong từng ô bằng một khoá bí mật để bảo vệ dữ liệu nhạy cảm",
   "Nén dữ liệu của từng hàng để giảm dung lượng lưu trữ trên đĩa của RegionServer",
   "Xoá bớt các cột ít dùng khỏi row key để rút gọn kích thước và tăng tốc độ tra cứu"]),
 "Đánh đổi của kỹ thuật salting là gì?": (None, [
   "Không có đánh đổi nào, salting chỉ có lợi cho cả ghi lẫn đọc theo khoảng thời gian",
   "Làm HBase ghi chậm hơn vì mọi lần ghi phải khoá toàn bộ bảng để thêm tiền tố",
   "Làm tăng kích thước row key tới mức vượt giới hạn và khiến bảng không dùng được"]),
 "get(rowkey) trong HBase gần tương đương với câu SQL nào, và khác biệt quan trọng gì?": (None, [
   "SELECT * FROM t — lấy toàn bộ bảng, hoàn toàn không có khác biệt gì khác",
   "DELETE FROM t WHERE pk = ? — nhưng chỉ xoá được một phiên bản của ô",
   "CREATE INDEX ON t(pk) — nhưng chỉ tạo được chỉ mục trên khoá chính"]),
 "Điều gì xảy ra với hệ thống Messages của Facebook sau đó (2018)?": (None, [
   "Vẫn dùng HBase nguyên vẹn tới nay, không thay đổi gì về kiến trúc lưu trữ",
   "Facebook đóng dịch vụ Messages và chuyển người dùng sang một ứng dụng khác",
   "Facebook quay lại dùng cơ sở dữ liệu quan hệ truyền thống cho toàn bộ tin nhắn"]),
 "Sqoop giải quyết bài toán thực tế gì cho doanh nghiệp?": (None, [
   "Thay thế hoàn toàn RDBMS của doanh nghiệp bằng một kho dữ liệu phân tán mới",
   "Tăng tốc các truy vấn SQL phức tạp ngay trên chính cơ sở dữ liệu quan hệ",
   "Mã hoá dữ liệu nhạy cảm trước khi lưu trên HDFS để tuân thủ quy định bảo mật"]),
 "Vì sao Sqoop import KHÔNG cần bước Reduce?": (None, [
   "Vì Sqoop không dùng MapReduce mà chỉ chạy một tiến trình duy nhất trên máy client",
   "Vì bảng RDBMS nguồn luôn đủ nhỏ để một Mapper đọc xong trong vài giây",
   "Vì bước Reduce chỉ được dùng cho Pig và Hive, không áp dụng cho các công cụ khác"]),
 "Apache Sqoop hiện ở trạng thái nào (tính tới thời điểm viết bài)?": (None, [
   "Vẫn đang được phát triển tích cực với các bản phát hành đều đặn hằng quý",
   "Chưa từng chính thức công bố bản phát hành nào, chỉ là mã nguồn thử nghiệm",
   "Vừa được tách thành hai dự án mới độc lập vào năm 2021"]),
 "So với Sqoop, CDC streaming (vd Debezium+Kafka) lấy dữ liệu thay đổi từ RDBMS theo cách nào?": (None, [
   "Quét lại toàn bộ bảng theo lịch định kỳ rồi so sánh với lần quét trước",
   "Yêu cầu RDBMS tạm ngừng hoạt động để xuất bản sao đầy đủ ra HDFS",
   "Không thể lấy dữ liệu thay đổi, chỉ lấy được ảnh chụp tại một thời điểm cố định"]),
 "Trong ví dụ Sqoop chia 1.000.000 dòng với khoá phân bố LỆCH (70% dồn vào 10% khoảng khoá), điều gì xảy ra với thời gian hoàn thành job?": (None, [
   "Không ảnh hưởng gì vì Sqoop chia đều các dòng theo khoảng giá trị của khoá chính",
   "Job sẽ chạy nhanh hơn vì phần lớn Mapper đều xử lý một khoảng khoá nhỏ rất nhanh",
   "Sqoop tự phát hiện sự lệch và tự động chia lại các khoảng khoá sao cho đều nhau"]),
 "Vì sao câu hỏi 'HBase hay Sqoop mạnh hơn' là sai ngay từ gốc?": (None, [
   "Vì cả hai công cụ đều đã bị ngừng phát triển nên không còn đáng để so sánh với nhau nữa",
   "Vì HBase và Sqoop thực chất là hai tên gọi khác nhau của cùng một công cụ trong hệ sinh thái",
   "Vì Sqoop thay thế hoàn toàn HBase trong mọi hệ thống, nên không còn lý do dùng HBase"]),
 "HBase được gọi là gì trong hệ sinh thái Hadoop?": (None, [
   "Công cụ ETL nạp dữ liệu từ nhiều nguồn vào HDFS",
   "Hệ thống lập lịch workflow cho các job Hadoop",
   "Công cụ điều phối và đồng bộ phân tán giữa các node"]),
 "Tại sao bảng 'lịch sử xét nghiệm bệnh nhân' (số lần xét nghiệm mỗi người rất khác nhau) hợp với mô hình wide-column hơn RDBMS cố định cột?": (None, [
   "Vì RDBMS không lưu được số liệu y tế nên bắt buộc phải dùng mô hình wide-column",
   "Vì wide-column nhanh hơn RDBMS ở mọi trường hợp bất kể mẫu truy cập dữ liệu",
   "Vì RDBMS không hỗ trợ lưu tiếng Việt có dấu trong các cột văn bản của bảng"]),
 "Vì sao 3 tầng (Chubby, root tablet, METADATA) đủ để địa chỉ 2^34 tablet?": (None, [
   "Vì mỗi tầng chỉ trỏ tới 2 tablet nên 3 tầng chứa tối đa 8 tablet được địa chỉ",
   "Vì Chubby lưu toàn bộ vị trí của mọi tablet trong một tệp nhỏ duy nhất",
   "Vì client luôn giữ đủ bộ đệm vị trí nên không bao giờ cần tới tầng thứ ba"]),
 "Major compaction khác minor compaction ở điểm nào?": (None, [
   "Major chỉ ghi memtable ra đĩa thành một SSTable mới và không động tới SSTable cũ",
   "Major chỉ chạy một lần khi master khởi động để dọn các tablet bị bỏ lại",
   "Major xoá commit log của tablet sau khi mọi dữ liệu đã được ghi ra SSTable"]),
 "Từ 1 lên 500 tablet server, thông lượng tổng của Bigtable trong bài tăng cỡ nào?": (
   "Hơn 100 lần, không phải 500 lần (mở rộng không tuyến tính)", [
   "Đúng 500 lần (mở rộng tuyến tính hoàn hảo)",
   "Chỉ khoảng 10 lần (gần như không mở rộng)",
   "Không đổi (thêm máy không giúp ích gì)"]),
 "Vì sao Bigtable dùng một commit log duy nhất cho mỗi tablet server thay vì mỗi tablet một log?": (None, [
   "Để dễ xoá log: chỉ cần xoá một tệp duy nhất khi tablet server ngừng hoạt động",
   "Vì mỗi tablet quá nhỏ nên một log riêng không đủ dung lượng để ghi mutation",
   "Vì Chubby yêu cầu mỗi tablet server chỉ được mở đúng một tệp log trên GFS"]),

 # ------------------------------------------------------------------ hd-05
 "Khác biệt cốt lõi giữa Kafka ('log phân tán') và message queue truyền thống là gì?": (None, [
   "Kafka luôn nhanh hơn message queue ở mọi trường hợp vì nó ghi dữ liệu thẳng vào bộ nhớ RAM",
   "Kafka chỉ cho phép một consumer đọc mỗi message, còn queue truyền thống cho nhiều consumer đọc lại",
   "Không có khác biệt thực sự về kiến trúc: Kafka chỉ là tên khác của một message queue thông thường"]),
 "Trong Kafka, 'offset' đại diện cho điều gì?": (None, [
   "Độ trễ mạng đo được giữa producer và broker trong lần gửi tin gần nhất",
   "Số lượng broker đang tham gia trong cluster tại thời điểm consumer kết nối",
   "Kích thước tối đa mà một message có thể có trước khi bị broker từ chối"]),
 "Bài toán gán partition cho consumer (RoundRobin/Range/Sticky) đã được học chi tiết ở đâu trong site này?": (None, [
   "Chính module này, ở phần kiến trúc Kafka với bốn khối nền tảng",
   "Module HBase & Sqoop, ở phần thiết kế row key và region",
   "Không được học ở đâu trong site này; đây là kiến thức hoàn toàn mới"]),
 "Confluent được thành lập năm nào, với khoản đầu tư ban đầu từ đâu?": (None, [
   "2010, tự vốn hoàn toàn bởi ba kỹ sư sáng lập",
   "2018, từ một quỹ đầu tư của chính phủ",
   "2021, thông qua đợt chào bán cổ phiếu lần đầu (IPO)"]),
 "Mô hình kinh doanh của Confluent là gì?": (None, [
   "Đóng toàn bộ mã nguồn Kafka và bán giấy phép độc quyền cho từng khách hàng",
   "Chỉ bán phần cứng chuyên dụng đã cài sẵn Kafka cho các trung tâm dữ liệu",
   "Không có mô hình kinh doanh rõ ràng, hoạt động chủ yếu bằng quỹ tài trợ"]),
 "Triết lý kiến trúc mà Kafka khai sinh, coi log sự kiện là 'nguồn sự thật duy nhất', được gọi là gì?": (None, [
   "Kiến trúc hướng đối tượng (object-oriented architecture)",
   "Chuẩn hoá quan hệ (relational normalization) của dữ liệu",
   "Nhân bản chủ-tớ (master-slave replication) giữa các cơ sở dữ liệu"]),
 "Jun Rao có kinh nghiệm nền tảng gì trước khi tham gia phát triển Kafka?": (None, [
   "Kỹ sư phần cứng tại Intel, chuyên thiết kế vi xử lý và bộ nhớ đệm",
   "Giảng viên đại học về mạng máy tính, chưa từng làm hệ thống phân tán",
   "Không có kinh nghiệm liên quan tới cơ sở dữ liệu hay hệ thống phân tán"]),
 "Kafka liên hệ trực tiếp tới lý thuyết lập lịch hàng đợi nào đã học trước đó?": (None, [
   "List Scheduling và LPT (Lập lịch 02) cho các máy giống nhau",
   "DRF, công bằng tài nguyên chiếm ưu thế (Lập lịch 07)",
   "Không liên hệ tới lý thuyết lập lịch nào trong các buổi đã học"]),
 "Paper/tài liệu nào trong materials.zip được dùng làm nguồn chính cho kiến trúc Kafka trong module này?": (None, [
   "Dean & Ghemawat (2004), MapReduce: Simplified Data Processing",
   "Decandia et al. (2007), Dynamo: kho key-value sẵn sàng cao của Amazon",
   "Ghodsi et al. (2011), Dominant Resource Fairness"]),
 "Trong Ví dụ A (2 consumer group đọc cùng 1 partition), vì sao group 'backup' có lag tăng nhanh hơn group 'dashboard'?": (None, [
   "Vì 'backup' đọc sai thứ tự message nên phải đọc lại các message cũ nhiều lần mỗi batch",
   "Vì 'backup' dùng một partition khác với 'dashboard' nên tốc độ ghi vào partition của nó cao hơn",
   "Vì ZooKeeper ưu tiên cấp băng thông cho group 'dashboard' hơn group 'backup' khi đọc"]),
 "Replication factor của 1 Partition trong Kafka thể hiện điều gì?": (None, [
   "Số lượng Topic khác nhau cùng được lưu trên một Broker duy nhất trong cluster",
   "Số lượng Consumer Group đang đọc Partition đó cùng một lúc trong cluster",
   "Thời gian retention tính bằng ngày mà Partition đó giữ lại các message"]),
 "Trong ví dụ mô phỏng mất broker giữ leader (replication factor = 3), điều gì xảy ra để hệ thống không mất dữ liệu?": (None, [
   "Dữ liệu buộc phải mất vì Kafka không có cơ chế nào để khôi phục sau khi leader hỏng",
   "Toàn bộ Partition bị xoá và được tạo lại từ đầu bằng dữ liệu mới của Producer",
   "ZooKeeper hoặc KRaft tự tạo lại phần dữ liệu đã mất dựa trên các thông điệp Producer gửi lại"]),
 "KRaft (KIP-500 + KIP-595) thay đổi điều gì trong kiến trúc Kafka?": (None, [
   "Thay đổi hoàn toàn khái niệm Topic, Partition và Offset mà producer và consumer nhìn thấy",
   "Thêm một lớp message queue truyền thống chạy song song với log phân tán để xử lý tin khẩn",
   "Chỉ áp dụng cho Kafka chạy trên Windows, còn Linux vẫn bắt buộc dùng ZooKeeper"]),
 "Theo mốc thời gian đã verify, phiên bản Kafka nào gỡ bỏ HOÀN TOÀN hỗ trợ ZooKeeper?": (None, [
   "Kafka 2.8.0 (KRaft ra mắt bản thử nghiệm)",
   "Kafka 3.3.1 (KRaft sẵn sàng cho production)",
   "Kafka 1.0 (bản ổn định đầu tiên mang số 1)"]),
 "Vì sao 'exactly-once' được xem là mức cam kết tốn chi phí hơn, không nên chọn mặc định cho mọi hệ thống?": (None, [
   "Vì Kafka không hỗ trợ exactly-once trong thực tế nên mọi hệ thống phải tự xử lý trùng",
   "Vì exactly-once chỉ hoạt động được với đúng một partition duy nhất cho mỗi topic",
   "Vì exactly-once làm mất khả năng replay dữ liệu, nên người dùng không thể đọc lại tin cũ"]),
 "Retention trong Kafka khác gì so với việc 'xoá message ngay sau khi 1 consumer đọc xong' của message queue truyền thống?": (None, [
   "Không khác gì: retention chỉ là tên gọi khác của việc xoá message ngay sau khi consumer đọc xong",
   "Retention chỉ áp dụng khi không còn consumer nào đang kết nối tới broker trong thời gian cấu hình",
   "Retention khiến Kafka không bao giờ xoá dữ liệu, mọi message được giữ vĩnh viễn trên đĩa"]),
 "Theo bài báo Kafka, vì sao dùng mô hình pull thay vì push?": (None, [
   "Vì pull luôn nhanh hơn push trong mọi tình huống và không bao giờ làm nghẽn broker",
   "Vì push không dùng được với Hadoop nên bắt buộc phải chuyển sang mô hình pull",
   "Vì pull bắt buộc phải có ZooKeeper để theo dõi xem consumer đã kéo tin hay chưa"]),
 "Tại sao tin trong Kafka được gọi bằng offset logic thay vì message id riêng?": (None, [
   "Để dễ mã hoá bằng Avro hơn, vì Avro chỉ chấp nhận định danh dạng số nguyên liên tiếp",
   "Vì Kafka thực chất không lưu tin lâu dài nên không cần đến message id riêng",
   "Vì offset được sinh ngẫu nhiên nên khó đoán hơn và an toàn hơn message id tuần tự"]),
 "Với sendfile, bài báo nói tiết kiệm được bao nhiêu so với cách gửi thông thường (4 lần sao chép, 2 lời gọi hệ thống)?": (None, [
   "Bỏ toàn bộ các lần sao chép và mọi lời gọi hệ thống",
   "Bỏ 1 lần sao chép nhưng vẫn giữ cả 2 lời gọi hệ thống",
   "Chỉ giảm lời gọi hệ thống, số lần sao chép giữ nguyên"]),
 "Bài báo Kafka 2011 nói gì về replication?": (None, [
   "Đã có sẵn replication 3 bản như HDFS, mọi tin đều được lưu ở ba broker khác nhau",
   "Không cần replication vì ZooKeeper đã lưu một bản sao của mọi tin ở cụm riêng",
   "Replication chỉ áp dụng cho consumer để đồng bộ vị trí đọc giữa các nhóm"]),
 "Vì sao Kafka chỉ đảm bảo at-least-once trong bài báo?": (None, [
   "Vì Kafka không có khái niệm offset nên không thể biết tin nào đã được giao cho consumer",
   "Vì consumer không có cách nào xác nhận (ack) việc đã nhận tin nên không thể đảm bảo hơn",
   "Vì ZooKeeper không đủ nhanh để ghi nhận offset của từng tin nên chỉ ghi nhận định kỳ"]),

 # ------------------------------------------------------------------ hd-06
 "Oozie biểu diễn thứ tự phụ thuộc giữa các bước bằng cấu trúc gì?": (None, [
   "Danh sách tuyến tính đơn giản các action chạy lần lượt",
   "Bảng băm ánh xạ tên action tới thời điểm chạy của nó",
   "Cây nhị phân tìm kiếm sắp xếp các action theo tên"]),
 "Trong workflow có fork/join, 2 nhánh chạy song song để giảm tổng thời gian pipeline. Điều kiện bắt buộc để làm vậy AN TOÀN là gì?": (None, [
   "2 nhánh phải cùng loại action, ví dụ cả hai đều là MapReduce hoặc cả hai đều là Hive",
   "2 nhánh phải chạy trên cùng 1 máy để chia sẻ bộ nhớ đệm giữa các job",
   "Không có điều kiện gì, fork/join luôn an toàn bất kể hai nhánh có phụ thuộc nhau hay không"]),
 "Trong workflow Oozie 4 bước (Sqoop → Hive clean → MapReduce → Email), nếu bước Hive clean thất bại, điều gì xảy ra?": (None, [
   "Oozie vẫn chạy tiếp các bước sau (MapReduce, Email) với dữ liệu cũ của lần chạy trước",
   "Toàn bộ cluster Hadoop dừng hoạt động cho tới khi quản trị viên khởi động lại",
   "Email báo cáo vẫn được gửi đi nhưng kèm ghi chú rằng bước Hive đã thất bại"]),
 "ZooKeeper được mô phỏng theo hệ thống nào của Google?": (None, [
   "Bigtable (cơ sở dữ liệu NoSQL phân tán)",
   "GFS (hệ file phân tán của Google)",
   "Spanner (cơ sở dữ liệu phân tán toàn cầu)"]),
 "ZooKeeper ra đời ở đâu, khoảng năm nào?": (None, [
   "Facebook, khoảng năm 2010",
   "LinkedIn, khoảng năm 2011",
   "Powerset, khoảng năm 2008"]),
 "Znode loại 'ephemeral' tự biến mất khi nào?": (None, [
   "Không bao giờ tự biến mất, phải được quản trị viên hoặc client xoá thủ công",
   "Sau đúng 24 giờ kể từ lúc được tạo, không phụ thuộc vào trạng thái của client",
   "Khi dịch vụ ZooKeeper được khởi động lại, mọi znode ephemeral đều bị xoá sạch"]),
 "Đặc tính 'sequential' của znode nghĩa là gì?": (None, [
   "Znode tự động bị xoá sau một khoảng thời gian cấu hình sẵn kể từ lúc tạo",
   "Znode chỉ cho phép đúng một client truy cập tại một thời điểm, các client khác bị khoá",
   "Znode luôn là bản sao chỉ-đọc của một znode khác nằm trên server dự phòng"]),
 "Vì sao ZAB/Paxos yêu cầu ĐA SỐ (majority) follower xác nhận, không phải TẤT CẢ?": (None, [
   "Vì đa số xác nhận nhanh hơn nên toàn hệ thống đạt độ trễ thấp hơn mức cần thiết",
   "Vì ZooKeeper không hỗ trợ cơ chế chờ xác nhận từ 100% các follower của ensemble",
   "Không có lý do kỹ thuật cụ thể, đây chỉ là quy ước đặt ra cho thuận tiện khi cài đặt"]),
 "Tình trạng 'split-brain' trong hệ phân tán là gì?": (None, [
   "Hệ thống chạy quá chậm vì một node nắm giữ toàn bộ tải của cụm trong thời gian dài",
   "Hệ thống hết dung lượng lưu trữ trên đĩa nên không ghi thêm được dữ liệu mới",
   "Lỗi cú pháp trong mã nguồn khiến các node không biên dịch và khởi động được"]),
 "4 chức năng cốt lõi ZooKeeper cung cấp gồm những gì?": (None, [
   "Lưu trữ tệp lớn, nén dữ liệu, mã hoá dữ liệu và sao lưu dữ liệu định kỳ",
   "Chạy các job MapReduce, các script Pig, truy vấn Hive và import dữ liệu bằng Sqoop",
   "Tạo báo cáo định kỳ, gửi email cảnh báo và lập lịch các tác vụ theo kiểu cron"]),
 "Trong HBase, ZooKeeper được dùng để bầu cử thành phần nào?": (None, [
   "DataNode (nút lưu trữ block dữ liệu của HDFS)",
   "NameNode (nút quản lý metadata của HDFS)",
   "JobTracker (bộ theo dõi job của Hadoop 1.0)"]),
 "Theo dòng thời gian tổng kết, công nghệ nào ra đời SỚM NHẤT làm nền tảng cho cả hệ sinh thái?": (None, [
   "Kafka (LinkedIn), ra đời sau khi các công cụ lưu trữ và xử lý đã có",
   "YARN (2012), tách quản lý tài nguyên khỏi MapReduce trong Hadoop 2.0",
   "Hive (Facebook), ra đời để dân phân tích dùng SQL trên Hadoop"]),
 "Bài học lớn nhất rút ra từ việc nhìn lại lịch sử toàn Chương 2 là gì?": (None, [
   "Tất cả công nghệ trong hệ sinh thái đều do một nhóm kỹ sư ở Google thiết kế sẵn từ đầu thành một bộ thống nhất",
   "Mọi công nghệ trong hệ sinh thái đều ra đời cùng một năm theo kế hoạch của Apache Software Foundation",
   "Hệ sinh thái Hadoop đã hoàn toàn lỗi thời, không còn công nghệ nào trong số đó được dùng tới ngày nay"]),
 "Mặc định lease Chubby kéo dài thêm bao lâu mỗi lần gia hạn, và master quá tải có thể kéo tới đâu?": (None, [
   "1 giây, tới khoảng 5 giây",
   "60 giây, tới khoảng 10 phút",
   "5 phút, tới khoảng 1 giờ"]),
 "Grace period của Chubby phục vụ mục đích gì?": (None, [
   "Tăng tốc đọc dữ liệu từ bộ đệm bằng cách tạm ngừng mọi yêu cầu ghi trong vài giây",
   "Xoá ngay tất cả khoá mà client đang giữ để nhường cho master mới bắt đầu",
   "Chuyển client sang một Chubby cell khác ngay lập tức mà không chờ master cũ"]),
 "Vì sao Chubby dùng vô hiệu bộ đệm (invalidation) thay vì TTL như DNS?": (None, [
   "Vì TTL không được Chubby hỗ trợ nên bắt buộc phải dùng cơ chế vô hiệu bộ đệm",
   "Vì vô hiệu bộ đệm luôn rẻ hơn TTL trong mọi trường hợp, kể cả khi dữ liệu đổi liên tục",
   "Vì client của Chubby không có bộ đệm nên mọi lần đọc đều phải hỏi lại master"]),
 "Điểm khác chính giữa khoá của Chubby và cách làm khoá trên ZooKeeper là gì?": (None, [
   "Chubby không có khoá; ZooKeeper cung cấp khoá phân tán như một tính năng gốc",
   "ZooKeeper có API khoá riêng với lệnh lock/unlock, còn Chubby thì không có khoá nào",
   "Hai hệ thống giống hệt nhau về API, chỉ khác ở ngôn ngữ cài đặt (C++ so với Java)"]),
 "Nhận định nào đúng về mức độ Bigtable phụ thuộc Chubby theo bài báo?": (None, [
   "Bigtable không phụ thuộc Chubby vì mọi metadata đều lưu trong chính các tablet của nó",
   "Bigtable chỉ phụ thuộc Chubby một lần khi khởi động, sau đó chạy độc lập hoàn toàn",
   "Bigtable phụ thuộc hoàn toàn vào Chubby: cứ mỗi giờ Chubby gián đoạn là mất dữ liệu"]),
 "Bài học chung nào của bài báo Chubby áp dụng cho ZooKeeper?": (None, [
   "Nên ghi cả các tệp dữ liệu lớn vào dịch vụ điều phối để mọi client cùng thấy một bản",
   "Nên cho mọi client nối thẳng tới leader để có dữ liệu mới nhất ở mọi lần đọc",
   "Nên bỏ khái niệm session để giảm số lượt giữ phiên giữa client và server"]),

 # ------------------------------------------------------------------ hd-07
 "Vì sao chỉ cần 3 số (đếm, tổng nhãn, tổng bình phương nhãn) cho mỗi đoạn là đủ tính sai số hồi quy?": (None, [
   "Vì nhãn của mọi quan sát trong cùng một đoạn luôn bằng nhau, nên chỉ cần ba số là đủ",
   "Vì chỉ có đúng ba giá trị x phân biệt trong luồng, mỗi giá trị cần một số đếm",
   "Vì Count-Min sketch chỉ có khả năng lưu đúng ba số cho mỗi khoảng truy vấn"]),
 "Thuật toán 1 lượt chính xác trong bài 1 dùng bộ nhớ bao nhiêu?": (None, [
   "Õ(1/ε²), với ε là sai số cộng cho phép của thuật toán",
   "O(1) bộ nhớ, vì chỉ cần giữ một biến đếm duy nhất",
   "Õ(m), tức tỉ lệ thuận với số quan sát của luồng"]),
 "Mục đích của lượt 1 trong thuật toán 2 lượt xấp xỉ cộng ε là gì?": (None, [
   "Tính đúng toàn bộ sai số của mọi ngưỡng ngay trong lượt đầu, lượt hai chỉ để kiểm tra lại",
   "Loại bỏ các nhãn lớn để nhãn còn lại nằm trong giới hạn M = O(1) của thuật toán",
   "Sắp xếp toàn bộ dữ liệu theo x để lượt hai duyệt tuần tự từng đoạn một cách chính xác"]),
 "Nhận định nào đúng về giả định i.i.d. trong các bài của thầy?": (None, [
   "Bài 1 có giả định i.i.d. nhưng bài 2 đã bỏ giả định đó và mở rộng sang phân loại",
   "Chỉ riêng bài 3 bỏ giả định i.i.d., còn bài 1 và bài 2 vẫn giả định dữ liệu độc lập",
   "Cả ba bài đều giả định dữ liệu độc lập cùng phân phối như công trình Domingos-Hulten"]),
 "Công trình Domingos-Hulten (KDD 2000) khác các bài của thầy ở điểm nào sau đây?": (None, [
   "Chỉ xét luồng hữu hạn và không đưa ra đảm bảo nào về bộ nhớ",
   "Xét cả bài toán hồi quy và có thêm phần MPC cho MapReduce",
   "Có cận dưới khớp bằng quy dẫn từ bài toán Index cho mọi tiêu chí"]),
 "Với thuộc tính phân loại có N = 20 giá trị, số phân hoạch [N] = A ⊔ B phải xét ở hậu xử lý cỡ bao nhiêu?": (None, [
   "Khoảng 20 phân hoạch, mỗi giá trị một lần",
   "Khoảng 400 phân hoạch (20 × 20)",
   "Khoảng 1 tỉ phân hoạch (2^30)"]),
 "Vì sao bước sắp theo x ở đầu thuật toán MPC giúp thông điệp gửi về máy trung tâm vẫn nhỏ cỡ √m?": (None, [
   "Vì dữ liệu được nén lại ở bước sắp xếp nên thông điệp luôn nhỏ hơn dữ liệu gốc rất nhiều",
   "Vì chỉ máy đầu tiên trong thứ tự sắp xếp phải gửi kết quả về máy trung tâm",
   "Vì các ứng viên biên bị xoá bớt trước khi gửi nên tổng số cặp luôn nhỏ hơn √m"]),
 "Trong module này, một vòng MPC tương ứng với thành phần nào của Hadoop?": (None, [
   "Một lần gọi đọc HDFS từ client tới DataNode",
   "Một lần gửi heartbeat từ DataNode tới NameNode",
   "Một znode được tạo trong cây của ZooKeeper"]),
 "Kỹ thuật nào giúp bài 3 giảm bộ nhớ cho Gini từ Õ(1/ε²) xuống Õ(1/ε)?": (None, [
   "Lấy mẫu nhiều hơn gấp đôi để các ước lượng đạt sai số nhỏ hơn với cùng bộ nhớ",
   "Dùng nhiều lượt duyệt hơn để đếm chính xác thay cho việc ước lượng bằng sketch",
   "Bỏ qua các ngưỡng nằm ở biên của miền giá trị nhằm giảm số ứng viên cần xét"]),
 "Cận dưới trong bài 3 được chứng minh bằng cách quy dẫn từ bài toán nào?": (None, [
   "Sắp xếp so sánh (cận dưới Ω(n log n))",
   "Tìm đường đi ngắn nhất trong đồ thị có trọng số",
   "Bao phủ tập (set cover) với số tập tối thiểu"]),
 "Nhận định nào là suy luận của nhóm, không phải khẳng định của bài báo?": (None, [
   "MPC là phép trừu tượng hoá của MapReduce, Hadoop và Spark, như bài báo nêu ở phần mở đầu",
   "Cận dưới khớp cho hồi quy một lượt là Ω(M²/ε), được chứng minh bằng quy dẫn từ Index",
   "Thuật toán một lượt dùng reservoir sampling để chọn tập ứng viên chứa ngưỡng gần tối ưu"]),
 "Luồng có xoá (dynamic stream) cần thay lấy mẫu bằng công cụ nào, và trả thêm cái giá gì?": (None, [
   "Quicksort trên toàn bộ luồng đã lưu, thêm thời gian sắp xếp nhưng không tăng bộ nhớ",
   "Bloom filter để kiểm tra phần tử đã bị xoá, thêm bộ nhớ lên gấp đôi so với trước",
   "Reservoir sampling với thêm một lượt duyệt để loại các phần tử đã xoá khỏi mẫu"]),
 "Vì sao các bài báo chọn tìm ngưỡng chia tối ưu cho từng nút thay vì cây quyết định tối ưu toàn cục?": (None, [
   "Vì cây quyết định chỉ có đúng một nút nên không có cây toàn cục nào để tối ưu cả",
   "Vì dữ liệu của các bài toán này quá nhỏ nên việc tối ưu toàn cục không đem lại lợi ích",
   "Vì các thuật toán CART và ID3 bị cấm sử dụng trong mô hình luồng dữ liệu và MPC"]),
 "Với bài 3, bộ nhớ của thuật toán 1 lượt cho hồi quy so với bài 2 (2 lượt) khác nhau thế nào về lượt và bộ nhớ?": (None, [
   "Bài 3 dùng nhiều bộ nhớ hơn bài 2 nhưng đổi lại giảm được số lượt duyệt xuống còn một",
   "Bài 3 cần 3 lượt duyệt và dùng bộ nhớ nhỏ hơn bài 2 một hệ số bằng đúng M",
   "Hai bài hoàn toàn giống nhau về lượt, bộ nhớ và điều kiện cần biết trước độ dài luồng"]),
}
