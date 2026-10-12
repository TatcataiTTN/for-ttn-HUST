# -*- coding: utf-8 -*-
"""Cân bằng độ dài đáp án quiz hd-01, hd-02 (giai đoạn 4 'audit thiên lệch quiz'): bản gốc có đáp án đúng dài gấp khoảng 2 lần
các đáp án nhiễu, và nhiều đáp án nhiễu quá lộ liễu. Mỗi mục: câu hỏi -> (đáp án đúng mới hoặc None, [3 đáp án nhiễu mới]).
Đáp án nhiễu viết lại phải sai rõ ràng theo nội dung module nhưng đủ hợp lý và độ dài tương đương đáp án đúng."""

QFIX_A = {
 # ------------------------------------------------------------------ hd-01
 "Hadoop ra đời trực tiếp từ dự án nào, và vì vấn đề gì?": (None, [
   "Dự án Apache Lucene, vì Lucene không đánh chỉ mục được văn bản tiếng Anh",
   "Một dự án nội bộ của Google, được công bố mã nguồn vào năm 2006",
   "Một dự án của Yahoo viết cho quảng cáo, vì cơ sở dữ liệu quan hệ quá chậm"]),
 "Google có cho Hadoop dùng chung mã nguồn GFS/MapReduce không?": (None, [
   "Có, Google tặng mã nguồn GFS và MapReduce cho Apache Software Foundation năm 2006",
   "Có một phần: chỉ mã MapReduce được chuyển giao, còn GFS thì được viết lại",
   "Không, Hadoop được viết xong hoàn toàn trước khi Google công bố bất kỳ bài báo nào"]),
 "Trong kiến trúc HDFS, NameNode chịu trách nhiệm chính về điều gì?": (None, [
   "Lưu dữ liệu thật của mọi block và phục vụ đọc ghi trực tiếp cho client",
   "Điều phối CPU và bộ nhớ cho các ứng dụng đang chạy trên toàn cụm",
   "Thực hiện nhân bản vật lý từng block giữa các DataNode với nhau"]),
 "fsimage và edit log phối hợp ra sao khi NameNode khởi động lại?": (None, [
   "Chỉ cần đọc fsimage gần nhất, vì fsimage luôn chứa trạng thái mới nhất",
   "Chỉ cần phát lại toàn bộ edit log từ đầu, fsimage chỉ dùng để sao lưu",
   "Hỏi từng DataNode xem chúng giữ block nào rồi tự suy ra toàn bộ namespace"]),
 "Vì sao Hadoop 1.0 coi NameNode là một Single Point of Failure?": (None, [
   "Vì NameNode lưu toàn bộ dữ liệu thật nên đĩa của nó hỏng là mất sạch dữ liệu",
   "Vì NameNode không dùng heartbeat nên không biết DataNode nào còn sống",
   "Vì NameNode chạy trên phần cứng đắt tiền nên không thể thay thế bằng máy khác"]),
 "Secondary NameNode và Standby NameNode khác nhau cốt lõi ở điểm nào?": (None, [
   "Secondary NameNode là bản sao nóng tiếp quản ngay khi NameNode chính hỏng; Standby NameNode chỉ gộp log định kỳ",
   "Hai thành phần giống nhau về chức năng, chỉ khác tên gọi giữa Hadoop 1.0 và 2.0; cả hai đều failover được",
   "Secondary NameNode lưu dữ liệu thật của các block nên khôi phục được tệp; Standby NameNode chỉ lưu metadata"]),
 "Block size lớn (64MB/128MB) trong HDFS giúp giải quyết vấn đề gì?": (None, [
   "Tăng khả năng lưu hiệu quả hàng triệu tệp nhỏ trong cùng một cụm",
   "Giảm hệ số nhân bản cần thiết để chịu lỗi cho mỗi block dữ liệu",
   "Giảm thời gian truy cập ngẫu nhiên từng byte trong các tệp lớn"]),
 "'Small-files problem' của HDFS là gì?": (None, [
   "HDFS từ chối lưu tệp nhỏ hơn một block, nên người dùng phải gộp tệp thủ công trước",
   "Tệp nhỏ bị nhân bản nhiều hơn tệp lớn nên tốn nhiều dung lượng đĩa vật lý hơn hẳn",
   "Tệp nhỏ làm DataNode quá tải vì mỗi tệp nhỏ cần một kết nối mạng riêng tới client"]),
 "Một tệp 300MB với block size 128MB được chia thành mấy block?": (None, [
   "2 block (128 MB + 172 MB, block cuối lớn hơn)",
   "4 block (mỗi block cỡ 75 MB, chia đều)",
   "300 block (mỗi block 1 MB)"]),
 "Nếu xác suất 1 DataNode hỏng trong năm là 2% (độc lập), xác suất mất HẲN 1 block có 3 bản sao là bao nhiêu (giả định đơn giản)?": (
   "0,0008% (tức 0,02 × 0,02 × 0,02)", [
   "0,04% (tức 0,02 × 0,02, như chỉ có 2 bản sao)",
   "2% (như không nhân bản, chỉ có một bản)",
   "6% (cộng ba lần 2% cho ba DataNode)"]),
 "Rack awareness trong HDFS giải quyết vấn đề gì mà nhân bản đơn thuần (không quan tâm vị trí) không giải quyết được?": (None, [
   "Đặt cả 3 bản sao trong cùng một rack để ghi nhanh nhất và tiết kiệm băng thông liên rack",
   "Giảm số bản sao cần thiết xuống còn 2 vì các rack khác nhau đã đủ độ tin cậy cao",
   "Cho client ghi song song lên nhiều rack cùng lúc để tăng thông lượng ghi gấp ba lần"]),
 "Khi một DataNode giữ bản sao của 1 block bị lỗi, hệ thống phản ứng ra sao?": (None, [
   "Client phát hiện lỗi khi đọc rồi tự sao chép block sang một DataNode khác",
   "DataNode lỗi tự khởi động lại và phục hồi block từ đĩa dự phòng cục bộ của nó",
   "NameNode xoá toàn bộ tệp chứa block đó và yêu cầu client ghi lại từ đầu"]),
 "HDFS theo mô hình truy cập nào, khác gì so với hệ file UNIX thông thường?": (None, [
   "Đọc-ghi ngẫu nhiên đầy đủ như hệ file UNIX, cho phép sửa bất kỳ byte nào trong tệp",
   "Chỉ đọc (read-only) sau khi tạo; không cho ghi hay append dưới mọi hình thức",
   "Ghi ngẫu nhiên giữa tệp được hỗ trợ nhưng chỉ khi tệp nhỏ hơn đúng một block"]),
 "Triết lý 'scale-out, lưu trước xử lý sau' của Hadoop ảnh hưởng trực tiếp tới kiến trúc nào phổ biến hiện nay?": (None, [
   "Hệ thống mainframe tập trung với một kho dữ liệu quan hệ duy nhất cho cả công ty",
   "Cơ sở dữ liệu quan hệ scale-up chạy trên một máy chủ rất mạnh duy nhất",
   "Kiến trúc tính toán biên (edge) không còn dùng kho dữ liệu trung tâm nào"]),
 "Lease mà GFS master cấp cho replica primary có timeout ban đầu bao lâu, và để làm gì?": (None, [
   "60 phút; cho phép chunkserver tự bầu primary mà không cần hỏi master",
   "5 giây; dùng để kiểm tra checksum các chunk trước khi cho phép ghi",
   "Không có timeout, lease cấp vĩnh viễn cho replica được chọn đầu tiên"]),
 "Vì sao GFS tách luồng dữ liệu khỏi luồng điều khiển khi ghi?": (None, [
   "Để master đọc và kiểm tra nội dung từng gói dữ liệu trước khi cho phép ghi vào chunk",
   "Để client không cần biết vị trí các replica mà chỉ nói chuyện với một chunkserver trung tâm",
   "Để tránh dùng TCP và thay bằng giao thức UDP nhanh hơn cho mọi bản sao"]),
 "Sự cố hot spot đầu tiên của GFS xảy ra trong tình huống nào và được sửa ra sao?": (None, [
   "Master hết RAM vì quá nhiều tệp nhỏ; sửa bằng cách thêm master thứ hai chạy song song",
   "Chunkserver hỏng đĩa hàng loạt cùng lúc; sửa bằng cách giảm kích thước chunk xuống 4 MB",
   "Client cache sai vị trí chunk sau khi chunkserver khởi động lại; sửa bằng bỏ cache metadata"]),

 # ------------------------------------------------------------------ hd-02
 "MapReduce tách biệt điều gì khỏi logic nghiệp vụ của người lập trình?": (None, [
   "Logic bảo mật: xác thực người dùng, phân quyền truy cập và mã hoá dữ liệu",
   "Logic giao diện: hiển thị kết quả, vẽ biểu đồ và tương tác với người dùng",
   "Logic cơ sở dữ liệu: lập chỉ mục, giao dịch ACID và khoá bản ghi"]),
 "Trong ví dụ 'đếm phiếu bầu' minh hoạ MapReduce, bước nào tương ứng với Shuffle?": (None, [
   "Mỗi phòng bỏ phiếu tự đếm xong số phiếu của riêng phòng mình trước khi gửi đi",
   "Cộng tổng phiếu của toàn quốc để ra người thắng cuộc sau cùng của cuộc bầu cử",
   "Kiểm tra từng phiếu bầu xem có hợp lệ hay không rồi loại bỏ phiếu không hợp lệ"]),
 "Combiner trong MapReduce chỉ dùng đúng khi hàm reduce có tính chất gì?": (None, [
   "Không có điều kiện gì, combiner dùng được với mọi hàm reduce bất kỳ",
   "Chỉ dùng khi dữ liệu đầu vào đã được sắp xếp sẵn theo khoá",
   "Chỉ dùng khi chạy đúng một Reducer duy nhất trên toàn cụm"]),
 "Combiner giúp ÍT nhất trong trường hợp nào?": (None, [
   "Dữ liệu có rất nhiều từ lặp lại như văn bản ngôn ngữ tự nhiên cần đếm tần suất",
   "Số Mapper rất nhỏ nên mỗi Mapper phải xử lý một lượng dữ liệu rất lớn mỗi lần",
   "Reducer chạy rất nhanh nên không còn điểm nghẽn ở giai đoạn gộp kết quả"]),
 "Trong Hadoop 1.0, JobTracker đồng thời đảm nhiệm bao nhiêu vai trò khác nhau?": (None, [
   "1 vai trò duy nhất: chỉ theo dõi tiến trình của các job đang chạy trên cụm",
   "3 vai trò, gồm cả việc lưu trữ dữ liệu thật của các block trong HDFS",
   "Không có vai trò điều phối nào, chỉ chuyển tiếp thông điệp giữa client và NameNode"]),
 "YARN viết tắt của gì, và ý nghĩa cái tên đó?": (None, [
   "Yarn Architecture for Resource Networks, viết tắt chính thức do Apache đặt ra",
   "Young Allocation Resource Node, tên dựa theo node cấp phát tài nguyên đầu tiên",
   "Không viết tắt gì cả, chỉ là tên thương hiệu lấy từ sợi len trong logo dự án"]),
 "ApplicationMaster trong YARN khác JobTracker cũ ở điểm cốt lõi nào?": (None, [
   "ApplicationMaster chạy trên máy có CPU mạnh hơn nên theo dõi job nhanh hơn JobTracker",
   "ApplicationMaster không cần xin tài nguyên vì được ResourceManager cấp mặc định sẵn",
   "Hai thành phần giống hệt nhau về chức năng, chỉ đổi tên khi chuyển sang Hadoop 2.0"]),
 "Container trong YARN là gì?": (None, [
   "Một Docker container thật chứa toàn bộ hệ điều hành và ứng dụng chạy bên trong",
   "Một ổ đĩa vật lý gắn vào NodeManager để lưu các block dữ liệu của tệp HDFS",
   "Một loại máy chủ vật lý riêng chỉ dùng để chạy ApplicationMaster của từng job"]),
 "Khác biệt chính giữa Capacity Scheduler và Fair Scheduler là gì?": (None, [
   "Capacity Scheduler chia công bằng động theo thời gian thực; Fair Scheduler chia theo phần trăm cố định cho từng hàng đợi",
   "Hai bộ lập lịch giống hệt nhau về thuật toán, chỉ khác tên gọi giữa các bản phân phối Hadoop",
   "Fair Scheduler chỉ chạy được khi cụm có đúng một job; Capacity Scheduler mới hỗ trợ nhiều job và nhiều team"]),
 "Nhờ YARN, điều gì trở nên khả thi mà Hadoop 1.0 không làm được?": (None, [
   "Lưu trữ dữ liệu lớn hơn nhiều so với trước nhờ nhân bản HDFS thông minh hơn",
   "Giảm số lần nhân bản HDFS xuống còn 1 bản mà vẫn chịu lỗi như cũ",
   "Thay thế hoàn toàn HDFS bằng một hệ file phân tán mới nhanh hơn nhiều"]),
 "Vì sao Job Z (yêu cầu nhiều nhất, 20 Container) không được ưu tiên cấp nhiều hơn Job Y trong ví dụ trên?": (None, [
   "Vì Z nộp yêu cầu sau cùng nên ResourceManager xếp Z vào cuối hàng đợi chờ cấp phát",
   "Vì Z bị lỗi ở lần chạy trước nên bị hạ mức ưu tiên cho tới khi chạy thành công",
   "Vì ResourceManager luôn ưu tiên job nhỏ và đẩy job lớn xuống sau để giảm thời gian chờ"]),
 "Trong ví dụ 2 job xin 12 và 10 Container trên cụm chỉ có 20 Container trống, Fair Scheduler làm gì?": (None, [
   "Chỉ cấp đủ cho job nộp trước, job nộp sau phải chờ tới khi job đầu hoàn thành",
   "Từ chối cả hai yêu cầu vì tổng 22 Container vượt quá 20 Container đang trống",
   "Tạo thêm Container mới ngay lập tức để đáp ứng đủ 100% cả hai yêu cầu"]),
 "Ý tưởng kiến trúc nào của YARN lặp lại ở quy mô lớn hơn trong Kubernetes?": (None, [
   "Lưu trữ phân tán có nhân bản 3 lần để chịu lỗi ở cấp độ từng tệp dữ liệu",
   "Dùng ngôn ngữ lập trình Java làm nền tảng chung cho mọi thành phần hệ thống",
   "Mô hình key-value phân tán để lưu trạng thái của từng ứng dụng trong cụm"]),
 "Vì sao Spark có thể dần thay thế MapReduce làm engine xử lý chính mà không cần xây lại cụm?": (None, [
   "Vì Spark tự quản lý toàn bộ cụm riêng và không cần YARN, nên phải xây một cụm mới",
   "Vì Spark dùng hệ file khác HDFS hoàn toàn, nên dữ liệu phải được chuyển đổi trước khi chạy",
   "Vì Spark không chạy được trên cụm Hadoop, nên chỉ thay thế được ở một cụm tách biệt"]),
 "Theo Figure 1 của bài MapReduce, reduce worker lấy dữ liệu của map worker bằng cách nào?": (None, [
   "Map worker chủ động đẩy dữ liệu trực tiếp vào bộ nhớ của reduce worker khi map xong",
   "Qua hệ file toàn cục: map ghi ra HDFS, reduce đọc lại như tệp đầu vào thông thường",
   "Qua master: master nhận từng cặp trung gian rồi chuyển tiếp tới reduce worker tương ứng"]),
 "Vì sao map task đã hoàn thành trên máy chết phải chạy lại, còn reduce task đã hoàn thành thì không?": (None, [
   "Vì hàm map chậm hơn hàm reduce nên master ưu tiên chạy lại các task chậm nhất",
   "Vì reduce chạy trên các máy mạnh hơn nên hiếm khi hỏng và không cần dự phòng",
   "Vì master chỉ ghi nhớ trạng thái của các reduce task, không ghi nhớ trạng thái map"]),
 "Ví dụ Distributed Sort trong bài báo, hàm reduce làm gì?": (None, [
   "Tự thực hiện thuật toán quicksort trên toàn bộ các cặp mà reducer nhận được",
   "Gộp các bản ghi có cùng khoá thành một bản ghi duy nhất trước khi ghi ra",
   "Đếm số bản ghi của mỗi khoá rồi phát ra cặp (khoá, số lượng)"]),
 "Vì sao chạy lại hay chạy song song hai bản của cùng một task (backup) không làm sai kết quả?": (None, [
   "Vì master chọn ngẫu nhiên một trong hai kết quả và bỏ kết quả còn lại",
   "Vì dữ liệu đầu vào chỉ được đọc đúng một lần nên bản thứ hai không có gì để ghi",
   "Vì mỗi bản chạy trên một máy riêng nên kết quả của chúng không bao giờ trộn lẫn"]),
}
