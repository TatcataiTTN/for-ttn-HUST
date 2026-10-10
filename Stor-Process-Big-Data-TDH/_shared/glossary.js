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
  {id:'zookeeper', page:'vi/group-1-slides.html', term:'Apache ZooKeeper', short:'Dịch vụ điều phối phân tán: quản lý cấu hình, đặt tên, đồng bộ hoá, bầu leader — dùng thuật toán ZAB.'}
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
