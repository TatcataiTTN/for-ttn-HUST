/* Từ điển thuật ngữ + tìm kiếm toàn site (đơn giản hoá từ pattern SPSS — chỉ 1 ngôn ngữ, bỏ xuyên-ngôn-ngữ).
   Kiến trúc: 1 mảng G, mỗi mục {id, page, term, short, full}. searchTerms() 5 bậc điểm số fuzzy (bỏ dấu). */
(function(){
'use strict';

var G = [
  // ---- 14 buổi streaming/sketching ----
  {id:'morris', page:'vi/modules/01-ky-vong/index.html', term:'Thuật toán Morris', short:'Đếm xấp xỉ chỉ dùng O(log log n) bit.', full:'Tăng bộ đếm X với xác suất 1/2^X thay vì mỗi lần +1; ước lượng n bằng 2^X−1, không chệch.'},
  {id:'ky-vong', page:'vi/modules/01-ky-vong/index.html', term:'Tuyến tính của kỳ vọng', short:'E[X+Y]=E[X]+E[Y], luôn đúng kể cả khi không độc lập.'},
  {id:'markov', page:'vi/modules/02-markov/index.html', term:'Bất đẳng thức Markov', short:'P(X>λ) < E[X]/λ cho biến không âm.'},
  {id:'chebyshev', page:'vi/modules/03-chebyshev/index.html', term:'Bất đẳng thức Chebyshev', short:'P(|X−EX|>λ) < Var(X)/λ², chặn đuôi dùng phương sai.'},
  {id:'kmv', page:'vi/modules/03-chebyshev/index.html', term:'KMV (k-minimum values)', short:'Ước lượng F0 (số phần tử phân biệt) bằng k giá trị băm nhỏ nhất.'},
  {id:'chernoff', page:'vi/modules/04-chernoff/index.html', term:'Chặn Chernoff', short:'Chặn đuôi theo hàm mũ, chặt hơn Chebyshev khi tổng nhiều biến độc lập.'},
  {id:'unionbound', page:'vi/modules/05-hoeffding-union/index.html', term:'Union bound', short:'P(hợp các sự kiện) ≤ tổng xác suất từng sự kiện, luôn đúng dù không độc lập.'},
  {id:'quynap', page:'vi/modules/06-quy-nap/index.html', term:'Chứng minh quy nạp', short:'Kỹ thuật chứng minh nền tảng, dùng lại trong bảo đảm xấp xỉ List Scheduling/LPT.'},
  {id:'fm', page:'vi/modules/07-tail-taylor/index.html', term:'Flajolet-Martin (FM)', short:'Ước lượng F0 bằng giá trị nhỏ nhất của t số Uniform(0,1); trung bình cộng bị lệch mạnh, nên dùng trung vị.'},
  {id:'f0f1f2', page:'vi/modules/08-vector-chuan/index.html', term:'F0, F1, F2', short:'Số phần tử phân biệt, độ dài luồng, và bình phương chuẩn L2 của vector tần suất.'},
  {id:'sketch-tuyen-tinh', page:'vi/modules/09-ma-tran-sketch/index.html', term:'Sketch tuyến tính (Πx)', short:'Phép chiếu tuyến tính cho phép cập nhật tức thời khi dữ liệu đổi, không cần tính lại từ đầu.'},
  {id:'ams', page:'vi/modules/10-rademacher-khintchine/index.html', term:'AMS sketch', short:'Ước lượng F2 bằng tổng có dấu ngẫu nhiên Rademacher, không chệch.'},
  {id:'countmin', page:'vi/modules/11-ham-bam/index.html', term:'CountMin sketch', short:'Bảng đếm xấp xỉ bằng L hàm băm độc lập, ước lượng luôn ≥ đếm thật.'},
  {id:'qdigest', page:'vi/modules/12-cay-nhi-phan/index.html', term:'q-digest / MRL / KLL', short:'Các sketch ước lượng phân vị (quantile) của một luồng dữ liệu với sai số kiểm soát được.'},
  {id:'boruvka', page:'vi/modules/13-do-thi-boruvka/index.html', term:"Thuật toán Borůvka", short:'Xây cây khung nhỏ nhất theo từng vòng, O(log n) vòng — phù hợp mô hình streaming trên đồ thị.'},
  {id:'schwartzzippel', page:'vi/modules/14-truong-huu-han/index.html', term:'Bổ đề Schwartz-Zippel', short:'Đa thức khác 0 bậc d trên trường hữu hạn có tối đa d nghiệm — nền tảng kiểm tra đẳng thức đa thức ngẫu nhiên.'},

  // ---- 10 buổi lập lịch ----
  {id:'cmax', page:'vi/modules/ll-02-list-scheduling-lpt/index.html', term:'Makespan (Cmax)', short:'Thời điểm hoàn thành tác vụ cuối cùng — mục tiêu min Cmax của bài toán lập lịch cơ bản.'},
  {id:'listsched', page:'vi/modules/ll-02-list-scheduling-lpt/index.html', term:'List Scheduling', short:'Giao tác vụ tiếp theo cho máy đang tải nhỏ nhất; bảo đảm Cmax ≤ (2−1/m)·OPT.'},
  {id:'lpt', page:'vi/modules/ll-02-list-scheduling-lpt/index.html', term:'LPT (Longest Processing Time)', short:'Sắp tác vụ dài trước rồi chạy List Scheduling; bảo đảm (4/3−1/3m)·OPT, chặt hơn List Scheduling thường.'},
  {id:'dagsched', page:'vi/modules/ll-03-dag-mapreduce/index.html', term:'Lập lịch DAG & đường găng', short:'Chỉ chọn tác vụ có mọi tiền nhiệm đã xong; đường găng (critical path) quyết định cận dưới OPT.'},
  {id:'datalocality', page:'vi/modules/ll-03-dag-mapreduce/index.html', term:'Vị trí dữ liệu (data locality)', short:'Chọn máy chạy task theo tổng thời gian chờ+lấy dữ liệu+xử lý nhỏ nhất, không mặc định ưu tiên máy có dữ liệu.'},
  {id:'fifo-sched', page:'vi/modules/ll-04-fifo-spt-smith/index.html', term:'FIFO (lập lịch)', short:'Chạy theo đúng thứ tự vào hàng đợi — đơn giản nhưng không tối ưu tổng thời gian hoàn thành.'},
  {id:'spt', page:'vi/modules/ll-04-fifo-spt-smith/index.html', term:'SPT (Shortest Processing Time)', short:'Chạy tác vụ ngắn trước; tối ưu ΣCj trên 1 máy, chứng minh bằng lập luận đổi chỗ.'},
  {id:'smith', page:'vi/modules/ll-04-fifo-spt-smith/index.html', term:'Quy tắc Smith', short:'Sắp theo pj/wj tăng dần; tối ưu Σ wⱼCⱼ — SPT là trường hợp riêng khi mọi wj bằng nhau.'},
  {id:'srpt', page:'vi/modules/ll-05-srpt/index.html', term:'SRPT (Shortest Remaining Processing Time)', short:'Luôn chạy công việc còn lại ít nhất, cho phép ngắt; tối ưu tổng thời gian trong hệ thống.'},
  {id:'progfill', page:'vi/modules/ll-06-cong-bang-tai-nguyen/index.html', term:'Progressive filling', short:'Tăng đều phần cấp tài nguyên tới khi đạt nhu cầu hoặc hết tài nguyên — hiện thực hoá max-min fairness.'},
  {id:'maxmin', page:'vi/modules/ll-06-cong-bang-tai-nguyen/index.html', term:'Max-min fairness', short:'Không thể tăng phần cấp một người mà không giảm phần của người đang nhận ít hơn hoặc bằng.'},
  {id:'drf', page:'vi/modules/ll-07-drf/index.html', term:'DRF (Dominant Resource Fairness)', short:'Max-min fairness áp dụng trên dominant share khi có nhiều loại tài nguyên (Ghodsi và cộng sự, NSDI 2011).'},
  {id:'dominant-share', page:'vi/modules/ll-07-drf/index.html', term:'Dominant share', short:'Tỉ lệ lớn nhất của một người dùng trên các loại tài nguyên — xác định tài nguyên "trội" của người đó.'},
  {id:'roundrobin-kafka', page:'vi/modules/ll-08-kafka-roundrobin-range/index.html', term:'RoundRobinAssignor (Kafka)', short:'Gán partition lần lượt theo vòng — cân bằng số lượng nhưng không cân bằng tải.'},
  {id:'range-kafka', page:'vi/modules/ll-08-kafka-roundrobin-range/index.html', term:'RangeAssignor (Kafka)', short:'Chia đoạn partition liên tiếp theo từng topic — dễ lệch tải nếu partition tải cao đứng cạnh nhau.'},
  {id:'sticky-kafka', page:'vi/modules/ll-09-kafka-sticky-rebalance/index.html', term:'StickyAssignor (Kafka)', short:'Giữ tối đa phân công cũ khi tái cân bằng, chỉ gán lại phần partition mất chủ — giảm di chuyển.'},

  // ---- Hadoop / hệ sinh thái (slide Nhóm 1) ----
  {id:'hdfs', page:'vi/group-1-slides.html', term:'HDFS', short:'Hệ file phân tán của Hadoop — chia tệp thành block, nhân bản 3 lần mặc định để chịu lỗi.'},
  {id:'namenode', page:'vi/group-1-slides.html', term:'NameNode / DataNode', short:'NameNode quản lý metadata; DataNode lưu block dữ liệu thật — mô hình master/slave của HDFS.'},
  {id:'mapreduce', page:'vi/group-1-slides.html', term:'MapReduce', short:'Mô hình lập trình song song gồm hàm Map và Reduce — engine thực thi chung của Hive/Pig/Sqoop.'},
  {id:'yarn', page:'vi/group-1-slides.html', term:'YARN', short:'Quản lý tài nguyên & lập lịch của Hadoop 2.x, tách biệt khỏi MapReduce — gồm ResourceManager, ApplicationMaster, NodeManager.'},
  {id:'hive', page:'vi/group-1-slides.html', term:'Apache Hive', short:'Data warehouse trên Hadoop, truy vấn bằng HiveQL (giống SQL), dịch thành job MapReduce/Tez/Spark.'},
  {id:'pig', page:'vi/group-1-slides.html', term:'Apache Pig', short:'Ngôn ngữ kịch bản Pig Latin cho data flow, biên dịch thành chuỗi job MapReduce.'},
  {id:'hbase', page:'vi/group-1-slides.html', term:'Apache HBase', short:'NoSQL wide-column trên Hadoop (mô hình Bigtable) — đọc/ghi ngẫu nhiên độ trễ thấp, không hỗ trợ SQL/join.'},
  {id:'sqoop', page:'vi/group-1-slides.html', term:'Apache Sqoop', short:'Nhập/xuất dữ liệu hàng loạt giữa Hadoop và RDBMS, dùng MapReduce chỉ gồm Map task.'},
  {id:'kafka', page:'vi/group-1-slides.html', term:'Apache Kafka', short:'Nền tảng publish-subscribe phân tán, chia topic thành partition để song song hoá.'},
  {id:'oozie', page:'vi/group-1-slides.html', term:'Apache Oozie', short:'Lập lịch workflow dạng đồ thị có hướng không chu trình (DAG) cho chuỗi job Hadoop.'},
  {id:'zookeeper', page:'vi/group-1-slides.html', term:'Apache ZooKeeper', short:'Dịch vụ điều phối phân tán: quản lý cấu hình, đặt tên, đồng bộ hoá, bầu leader — dùng thuật toán ZAB.'},

  // ---- Hadoop deep-dive: lịch sử, động lực, ảnh hưởng (6 module tự học sâu hd-01..hd-06) ----
  {id:'hd-nutch', page:'vi/modules/hd-01-hadoop-hdfs/index.html', term:'Apache Nutch', short:'Công cụ tìm kiếm mở (2002, Cutting & Cafarella) không scale được — tiền thân trực tiếp của Hadoop.'},
  {id:'hd-gfs-mr-paper', page:'vi/modules/hd-01-hadoop-hdfs/index.html', term:'GFS & MapReduce (paper Google)', short:'2 bài báo Google (2003, 2004) truyền cảm hứng trực tiếp cho kiến trúc HDFS + MapReduce của Hadoop.'},
  {id:'hd-hadoop-name', page:'vi/modules/hd-01-hadoop-hdfs/index.html', term:'Vì sao tên "Hadoop"', short:'Tên con voi nhồi bông của con trai Doug Cutting — không phải viết tắt kỹ thuật.'},
  {id:'hd-fsimage', page:'vi/modules/hd-01-hadoop-hdfs/index.html', term:'fsimage / edit log', short:'fsimage là ảnh chụp namespace; edit log là nhật ký thay đổi — NameNode phát lại log khi khởi động.'},
  {id:'hd-secondary-nn', page:'vi/modules/hd-01-hadoop-hdfs/index.html', term:'Secondary NameNode vs Standby NameNode', short:'Secondary NN chỉ gộp log định kỳ, KHÔNG phải cơ chế failover — Standby NN (HA, Hadoop 2.0) mới thay thế được NameNode chính.'},
  {id:'hd-blocksize', page:'vi/modules/hd-01-hadoop-hdfs/index.html', term:'Block size HDFS (64MB/128MB)', short:'Block lớn giảm số entry metadata trên NameNode — đánh đổi: HDFS kém hiệu quả với rất nhiều tệp nhỏ.'},
  {id:'hd-jobtracker', page:'vi/modules/hd-02-mapreduce-yarn/index.html', term:'JobTracker (Hadoop 1.0)', short:'Vừa quản lý tài nguyên vừa theo dõi mọi job — điểm nghẽn & SPOF, giới hạn cụm ~4.000 node.'},
  {id:'hd-combiner', page:'vi/modules/hd-02-mapreduce-yarn/index.html', term:'Combiner (MapReduce)', short:'"Mini-Reducer" gộp trước tại Mapper, giảm lưu lượng shuffle — chỉ đúng khi hàm reduce kết hợp/giao hoán.'},
  {id:'hd-yarn-arch', page:'vi/modules/hd-02-mapreduce-yarn/index.html', term:'ResourceManager / NodeManager / ApplicationMaster', short:'3 vai trò YARN tách biệt (Hadoop 2.0, 2012) thay cho 1 JobTracker duy nhất — mỗi job có ApplicationMaster riêng.'},
  {id:'hd-yarn-k8s', page:'vi/modules/hd-02-mapreduce-yarn/index.html', term:'YARN → Kubernetes', short:'Ý tưởng tách resource management khỏi logic ứng dụng của YARN lặp lại ở quy mô lớn hơn với Kubernetes (2014).'},
  {id:'hd-piglatin', page:'vi/modules/hd-03-pig-hive/index.html', term:'PigLatin', short:'Ngôn ngữ thủ tục (procedural dataflow) của Apache Pig — nằm giữa SQL khai báo và MapReduce cấp thấp.'},
  {id:'hd-hiveql', page:'vi/modules/hd-03-pig-hive/index.html', term:'HiveQL', short:'Ngôn ngữ khai báo giống SQL của Hive (Facebook, phát hành 10/2010) — dịch thành job MapReduce.'},
  {id:'hd-hive-metastore', page:'vi/modules/hd-03-pig-hive/index.html', term:'Hive Metastore', short:'Catalog lưu schema bảng — di sản bền lâu nhất của Hive, được Presto/Trino/Spark SQL ngày nay tương thích.'},
  {id:'hd-bigtable', page:'vi/modules/hd-04-hbase-sqoop/index.html', term:'Google Bigtable (paper)', short:'Paper 2006 của Google — HBase là bản mã nguồn mở theo mô hình này, do Powerset xây (phát hành 28/3/2008).'},
  {id:'hd-hotspotting', page:'vi/modules/hd-04-hbase-sqoop/index.html', term:'Hotspotting (thiết kế row key HBase)', short:'Dùng timestamp làm tiền tố row key khiến mọi row mới dồn vào 1 region — lỗi thiết kế schema HBase phổ biến nhất.'},
  {id:'hd-sqoop-attic', page:'vi/modules/hd-04-hbase-sqoop/index.html', term:'Sqoop & Apache Attic', short:'Sqoop (Cloudera, 2009) bị retired vào Apache Attic tháng 6/2021 khi CDC streaming thay vai trò ETL batch của nó.'},
  {id:'hd-kafka-linkedin', page:'vi/modules/hd-05-kafka/index.html', term:'Kafka @ LinkedIn', short:'Jay Kreps, Neha Narkhede, Jun Rao phát triển Kafka tại LinkedIn (2010), mã nguồn mở hoá đầu 2011.'},
  {id:'hd-offset-lag', page:'vi/modules/hd-05-kafka/index.html', term:'Offset & Lag (Kafka)', short:'Offset là vị trí đọc của 1 consumer group trong 1 partition; lag = log-end-offset − offset đã commit.'},
  {id:'hd-log-centric', page:'vi/modules/hd-05-kafka/index.html', term:'Event sourcing / log-centric architecture', short:'Triết lý Kafka khai sinh: log bất biến là nguồn sự thật duy nhất, mọi hệ thống khác là "view" xây lại từ đó.'},
  {id:'hd-confluent', page:'vi/modules/hd-05-kafka/index.html', term:'Confluent', short:'Công ty do 3 người tạo Kafka thành lập năm 2014 (500.000 USD từ LinkedIn), IPO năm 2021.'},
  {id:'hd-oozie-dag', page:'vi/modules/hd-06-oozie-zookeeper/index.html', term:'Oozie workflow (DAG)', short:'Oozie (Yahoo!, 2008) điều phối chuỗi job Hadoop phụ thuộc nhau theo đồ thị có hướng không chu trình.'},
  {id:'hd-chubby', page:'vi/modules/hd-06-oozie-zookeeper/index.html', term:'Google Chubby', short:'Dịch vụ lock phân tán nội bộ của Google (paper Mike Burrows) — ZooKeeper mô phỏng theo kiến trúc này.'},
  {id:'hd-zab', page:'vi/modules/hd-06-oozie-zookeeper/index.html', term:'ZAB (ZooKeeper Atomic Broadcast)', short:'Biến thể của Paxos dùng để đạt đồng thuận phân tán trong ZooKeeper.'},
  {id:'hd-znode-election', page:'vi/modules/hd-06-oozie-zookeeper/index.html', term:'Bầu leader bằng znode tuần tự', short:'Mỗi ứng viên tạo 1 znode tuần tự (ephemeral); znode có số thứ tự (zxid) nhỏ nhất đang tồn tại là leader.'},
  {id:'hd-timeline', page:'vi/hadoop-deep-dive-slides.html', term:'Dòng thời gian hệ sinh thái Hadoop', short:'2003-04 (Google) → 2006-2008 (Hadoop/Pig/ZooKeeper/HBase/Oozie) → 2009-2012 (Sqoop/Kafka/YARN) — nhiều công ty, không phải 1 bản thiết kế.'}
];

function norm(s){
  return String(s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/đ/gi,'d').toLowerCase().trim();
}

function searchTerms(q, limit){
  limit = limit || 8;
  var nq = norm(q);
  if (!nq) return [];
  var tokens = nq.split(/\s+/).filter(Boolean);
  var scored = [];
  G.forEach(function(item){
    var termHay = norm(item.term);
    var fullHay = norm([item.term, item.short, item.full||''].join(' '));
    var score = null;
    if (termHay.indexOf(nq) === 0) score = 0;
    else if (termHay.indexOf(nq) >= 0) score = 1;
    else if (fullHay.indexOf(nq) >= 0) score = 2;
    else if (tokens.length > 1 && tokens.every(function(t){ return fullHay.indexOf(t) >= 0; })) score = 3;
    else if (tokens.some(function(t){ return t.length >= 3 && fullHay.indexOf(t) >= 0; })) score = 4;
    if (score !== null) scored.push({ item: item, score: score });
  });
  scored.sort(function(a,b){ return a.score - b.score; });
  return scored.slice(0, limit).map(function(s){ return s.item; });
}

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

document.addEventListener('DOMContentLoaded', function(){
  var box = document.getElementById('site-search');
  if (!box) return;
  var relRoot = box.getAttribute('data-rel-root') || '';
  var input = document.getElementById('site-search-input');
  var results = document.getElementById('site-search-results');

  function render(items, q){
    if (!items.length){
      results.innerHTML = '<div class="gs-empty">Không tìm thấy thuật ngữ khớp với "'+esc(q)+'".</div>';
      results.hidden = false; return;
    }
    results.innerHTML = items.map(function(it){
      return '<a class="gs-item" href="'+relRoot+it.page+'">'+
        '<span class="gs-term">'+esc(it.term)+'</span>'+
        '<div class="gs-short">'+esc(it.short)+'</div></a>';
    }).join('');
    results.hidden = false;
  }

  input.addEventListener('input', function(){
    var q = input.value;
    if (!q.trim()){ results.hidden = true; return; }
    render(searchTerms(q), q);
  });
  input.addEventListener('focus', function(){
    if (input.value.trim()) render(searchTerms(input.value), input.value);
  });
  document.addEventListener('click', function(e){
    if (!box.contains(e.target)) results.hidden = true;
  });
  input.addEventListener('keydown', function(e){
    if (e.key === 'Escape'){ results.hidden = true; input.blur(); }
  });
});
})();
