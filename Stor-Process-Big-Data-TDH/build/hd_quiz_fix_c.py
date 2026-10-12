# -*- coding: utf-8 -*-
"""Vòng chỉnh thứ hai cho các câu quiz mà đáp án đúng vẫn dài hơn rõ rệt sau vòng 1 (ghi đè hd_quiz_fix_a/b)."""

QFIX_C = {
 "Vì sao GFS tách luồng dữ liệu khỏi luồng điều khiển khi ghi?": (None, [
   "Để client không cần biết vị trí các replica mà chỉ nói chuyện với một chunkserver trung tâm duy nhất cho mọi thao tác ghi",
   "Để tránh dùng TCP và thay bằng giao thức UDP nhanh hơn cho việc đẩy dữ liệu tới mọi bản sao",
   "Để master đọc và kiểm tra nội dung từng gói dữ liệu trước khi cho phép ghi vào chunk của chunkserver"]),
 "Vì sao partition theo 1 cột có hàng triệu giá trị khác nhau (vd user_id) là lựa chọn tồi?": (None, [
   "Vì partition chỉ dùng được với cột kiểu ngày tháng, còn các cột kiểu khác sẽ báo lỗi ngay khi tạo bảng trong Hive",
   "Vì partition tạo ra quá ít thư mục nên không giúp lọc bớt được dữ liệu khi chạy truy vấn có điều kiện",
   "Vì Hive không hỗ trợ cột kiểu số nguyên lớn, nên các cột như user_id không thể dùng để partition bảng"]),
 "Apache Tez khác MapReduce ở điểm cốt lõi nào, giúp Hive nhanh hơn?": (None, [
   "Tez không chạy trên YARN mà dùng bộ lập lịch riêng, nên không cần xin tài nguyên từ cụm Hadoop dùng chung",
   "Tez chỉ hỗ trợ truy vấn trên một bảng duy nhất, nhờ đó tránh được bước JOIN vốn rất tốn kém trong MapReduce",
   "Tez thay thế hoàn toàn HDFS bằng bộ nhớ trong, nên dữ liệu không còn được lưu lâu dài trên đĩa của cụm"]),
 "Kỹ thuật 'salting' trong thiết kế row key HBase làm gì?": (None, [
   "Nén dữ liệu của từng hàng trước khi ghi để giảm dung lượng lưu trữ trên đĩa của RegionServer xuống nhiều lần",
   "Xoá bớt các cột ít dùng khỏi row key để rút gọn kích thước khoá và tăng tốc độ tra cứu theo khoá",
   "Mã hoá dữ liệu trong từng ô bằng một khoá bí mật để bảo vệ các dữ liệu nhạy cảm của người dùng"]),
 "Trong ví dụ Sqoop chia 1.000.000 dòng với khoá phân bố LỆCH (70% dồn vào 10% khoảng khoá), điều gì xảy ra với thời gian hoàn thành job?": (None, [
   "Không ảnh hưởng gì, vì Sqoop luôn chia đều các dòng theo khoảng giá trị của khoá chính cho mọi Mapper",
   "Job chạy nhanh hơn, vì phần lớn Mapper xử lý một khoảng khoá nhỏ và xong rất sớm nên không ai phải chờ",
   "Sqoop tự phát hiện sự lệch trong lúc chạy và tự động chia lại các khoảng khoá sao cho đều nhau"]),
 "Vì sao 3 tầng (Chubby, root tablet, METADATA) đủ để địa chỉ 2^34 tablet?": (None, [
   "Vì Chubby lưu toàn bộ vị trí của mọi tablet trong một tệp nhỏ duy nhất mà master đọc mỗi lần tra cứu",
   "Vì mỗi tầng chỉ trỏ tới 2 tablet nên ba tầng chứa tối đa 8 tablet được địa chỉ, và 8 là đủ cho Bigtable",
   "Vì client luôn giữ đủ bộ đệm vị trí nên hệ thống không bao giờ thực sự cần tới tầng thứ ba để tra cứu"]),
 "Từ 1 lên 500 tablet server, thông lượng tổng của Bigtable trong bài tăng cỡ nào?": (
   "Hơn 100 lần, không phải 500 lần: mở rộng tốt nhưng không tuyến tính", [
   "Đúng 500 lần, tức mở rộng tuyến tính hoàn hảo theo số máy",
   "Chỉ khoảng 10 lần, tức gần như không mở rộng được",
   "Không đổi, thêm máy không giúp ích gì cho thông lượng"]),
 "Trong Ví dụ A (2 consumer group đọc cùng 1 partition), vì sao group 'backup' có lag tăng nhanh hơn group 'dashboard'?": (None, [
   "Vì 'backup' dùng một partition khác với 'dashboard' nên tốc độ ghi vào partition của nó cao hơn hẳn",
   "Vì 'backup' đọc sai thứ tự message nên phải đọc lại các message cũ nhiều lần ở mỗi batch xử lý",
   "Vì ZooKeeper ưu tiên cấp băng thông cho group 'dashboard' hơn group 'backup' mỗi khi hai group cùng đọc"]),
 "Vì sao 'exactly-once' được xem là mức cam kết tốn chi phí hơn, không nên chọn mặc định cho mọi hệ thống?": (None, [
   "Vì Kafka không hỗ trợ exactly-once trong thực tế, nên mọi hệ thống đều phải tự xử lý tin trùng ở phía ứng dụng",
   "Vì exactly-once làm mất khả năng replay dữ liệu, nên người dùng không thể đọc lại các tin cũ đã gửi trước đó",
   "Vì exactly-once chỉ hoạt động được với đúng một partition duy nhất cho mỗi topic, nên không mở rộng được"]),
 "Bài học lớn nhất rút ra từ việc nhìn lại lịch sử toàn Chương 2 là gì?": (None, [
   "Tất cả công nghệ trong hệ sinh thái đều do một nhóm kỹ sư ở Google thiết kế sẵn từ đầu thành một bộ thống nhất, rồi mới công bố ra ngoài",
   "Mọi công nghệ trong hệ sinh thái đều ra đời cùng một năm theo một kế hoạch chung của Apache Software Foundation đặt ra từ trước",
   "Hệ sinh thái Hadoop đã hoàn toàn lỗi thời và không còn công nghệ nào trong số đó được dùng tới ngày nay ở bất kỳ công ty nào"]),
 "Nhận định nào đúng về mức độ Bigtable phụ thuộc Chubby theo bài báo?": (None, [
   "Bigtable phụ thuộc hoàn toàn vào Chubby: cứ mỗi giờ Chubby gián đoạn là toàn bộ dữ liệu trong Bigtable bị mất vĩnh viễn",
   "Bigtable chỉ phụ thuộc Chubby một lần khi khởi động; sau đó cụm chạy độc lập hoàn toàn mà không cần Chubby nữa",
   "Bigtable không phụ thuộc Chubby vì mọi metadata và vị trí tablet đều được lưu ngay trong chính các tablet của nó"]),
 "Với cùng m = 10^6, sai số nào đúng cho thuật toán MPC một vòng?": (
   "Misclassification: OPT + 0,001; Gini: OPT + 0,032", [
   "Misclassification: OPT + 0,032; Gini: OPT + 0,001",
   "Misclassification và Gini: cùng OPT + 0,001",
   "Misclassification và Gini: cùng OPT + 0,032"]),
 "Số liệu chi phí thêm mỗi tin trong thực nghiệm của bài báo là bao nhiêu?": (
   "Kafka 9 byte mỗi tin, ActiveMQ 144 byte mỗi tin", [
   "Kafka 144 byte mỗi tin, ActiveMQ 9 byte mỗi tin",
   "Cả hai cùng 9 byte mỗi tin",
   "Cả hai cùng 144 byte mỗi tin"]),
}
