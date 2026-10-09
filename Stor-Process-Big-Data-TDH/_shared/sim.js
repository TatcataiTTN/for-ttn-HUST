/* Widget mô phỏng tương tác — 1 demo cho mỗi buổi, dùng thư viện thuần ALG (algo.js).
   Theo đúng hợp đồng: <div class="sim" data-sim="ten"></div>, chạy 1 lần khi tải, nút "Chạy lại". */
(function(){
'use strict';
var A = window.ALG;
function el(tag,attrs,html){var e=document.createElement(tag);if(attrs)for(var k in attrs)e.setAttribute(k,attrs[k]);if(html!==undefined)e.innerHTML=html;return e}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function frame(root,title,body){root.innerHTML='<div class="simh">🧪 '+title+'</div>'+body}
function $(root,sel){return root.querySelector(sel)}
function nums(s){return s.split(/[\s,;]+/).filter(Boolean).map(Number)}
function toks(s){return s.split(/[\s,;]+/).filter(Boolean)}
function fnum(x){ if (!isFinite(x)) return '∞'; if (Number.isInteger(x)) return String(x); return (Math.round(x*1000)/1000).toString(); }
function tbl(head,rows){return '<table class="t"><tr>'+head.map(function(h){return '<th>'+h+'</th>'}).join('')+'</tr>'+rows.map(function(r){var c='';if(r&&r.cls){c=' class="'+r.cls+'"';r=r.cells}return '<tr'+c+'>'+r.map(function(x){return '<td>'+x+'</td>'}).join('')+'</tr>'}).join('')+'</table>'}
function renderMath(root){
  if (window.renderMathInElement) {
    try { renderMathInElement(root, {delimiters: window.KATEX_DELIMS||[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}], macros: window.KATEX_MACROS||{}, throwOnError:false}); } catch(e){}
  }
}
var W = {};

W.morris = function(root){
  frame(root,'Chạy thử thuật toán Morris', '<div class="row"><label>Số sự kiện n = <input id="n" type="number" value="1000" style="width:90px"></label><label>Số lần chạy độc lập = <input id="t" type="number" value="30" style="width:70px"></label><button class="btn" id="go">Chạy</button></div><div class="out"></div>');
  function run(){
    var n=+$(root,'#n').value, t=+$(root,'#t').value;
    var r = A.morrisTrials(n, t);
    var rows = r.estimates.slice(0,10).map(function(e,i){ return [i+1, fnum(e), fnum(e-n)]; });
    $(root,'.out').innerHTML = '<p>Giá trị thật: <b>'+n+'</b>. Trung bình '+t+' lần chạy: <b>'+fnum(r.mean)+'</b> (kỳ vọng lý thuyết = n = '+n+') — sai số trung bình '+fnum(r.mean-n)+'.</p>'+
      '<p>Phương sai thực nghiệm của ước lượng: '+fnum(r.variance)+' — Morris dùng bộ nhớ $O(\\log\\log n)$ bit thay vì $O(\\log n)$ của bộ đếm chính xác.</p>'+
      tbl(['Lần chạy','Ước lượng $\\tilde n$','Sai số'], rows)+'<p><small>Chỉ hiện 10/'+t+' lần đầu.</small></p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.markov = function(root){
  frame(root,'Kiểm chứng bất đẳng thức Markov trên dữ liệu ngẫu nhiên', '<div class="row"><label>Số mẫu = <input id="n" type="number" value="5000" style="width:90px"></label><label>Ngưỡng λ = <input id="lam" type="number" value="7" style="width:70px"></label><button class="btn" id="go">Sinh mẫu Uniform(0,10) &amp; kiểm tra</button></div><div class="out"></div>');
  function run(){
    var n=+$(root,'#n').value, lam=+$(root,'#lam').value;
    var samples = Array.from({length:n}, function(){ return Math.random()*10; });
    var r = A.markovCheck(samples, lam);
    $(root,'.out').innerHTML = '<p>$\\mathbb EX\\approx$'+fnum(r.EX)+'</p>'+
      '<p>Chặn Markov: $\\mathbb P(X>\\lambda)<\\mathbb EX/\\lambda=$ <b>'+fnum(r.bound)+'</b></p>'+
      '<p>Tần suất thực nghiệm $X>\\lambda$: <b>'+fnum(r.empirical)+'</b></p>'+
      '<p class="'+(r.valid?'ok':'no')+'">'+(r.valid?'✓ thực nghiệm ≤ chặn Markov, đúng như lý thuyết':'✗ vi phạm — kiểm tra lại tham số')+'</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.chebyshev = function(root){
  frame(root,'Chebyshev &amp; thuật toán KMV (đếm phần tử phân biệt)',
    '<div class="row"><b>1. Chebyshev trên mẫu ngẫu nhiên</b></div>'+
    '<div class="row"><label>Số mẫu = <input id="n" type="number" value="5000" style="width:90px"></label><label>Ngưỡng λ = <input id="lam" type="number" value="3" style="width:60px"></label><button class="btn" id="go1">Kiểm tra</button></div><div class="out1"></div>'+
    '<div class="row" style="margin-top:14px"><b>2. KMV ước lượng F₀ từ 1 luồng</b></div>'+
    '<div class="row"><label>Luồng (số, cách nhau dấu phẩy/khoảng trắng): <input id="stream" size="40" value="1 2 3 1 4 2 5 1 6 3 7 8 2 9 4"></label><label>k = <input id="k" type="number" value="4" style="width:60px"></label><button class="btn" id="go2">Ước lượng</button></div><div class="out2"></div>');
  function run1(){
    var n=+$(root,'#n').value, lam=+$(root,'#lam').value;
    var samples = Array.from({length:n}, function(){ return Math.random()*10; });
    var r = A.chebyshevCheck(samples, lam);
    $(root,'.out1').innerHTML = '$\\mathbb EX\\approx$'+fnum(r.EX)+', $\\mathrm{Var}[X]\\approx$'+fnum(r.Var)+
      '<p>Chặn Chebyshev: $\\mathbb P(|X-\\mathbb EX|>\\lambda)<\\mathrm{Var}/\\lambda^2=$<b>'+fnum(r.bound)+'</b> — thực nghiệm: <b>'+fnum(r.empirical)+'</b></p>';
    renderMath(root);
  }
  function run2(){
    var stream = nums($(root,'#stream').value), k=+$(root,'#k').value;
    var r = A.kmvEstimate(stream, k);
    $(root,'.out2').innerHTML = '<p>Số phần tử phân biệt THẬT (đếm trực tiếp): <b>'+r.distinctTrue+'</b></p>'+
      '<p>Ước lượng KMV (giữ k='+r.k+' giá trị băm nhỏ nhất): <b>'+r.estimate+'</b></p>'+
      '<p><small>Luồng ngắn nên sai số có thể lớn — KMV chỉ chính xác khi luồng đủ dài so với k (buổi 3: cần $k=\\Theta(1/\\varepsilon^2)$).</small></p>';
    renderMath(root);
  }
  $(root,'#go1').onclick=run1; $(root,'#go2').onclick=run2; run1(); run2();
};

W.chernoff = function(root){
  frame(root,'So sánh xác suất nhị thức CHÍNH XÁC với chặn Chernoff',
    '<div class="row"><label>n = <input id="n" type="number" value="1000" style="width:80px"></label><label>p = <input id="p" type="number" value="0.5" step="0.1" style="width:70px"></label><label>λ = <input id="lam" type="number" value="0.1" step="0.05" style="width:70px"></label><button class="btn" id="go">Tính</button></div><div class="out"></div>');
  function run(){
    var n=+$(root,'#n').value, p=+$(root,'#p').value, lam=+$(root,'#lam').value;
    var mu = n*p, k = Math.ceil(mu*(1+lam));
    var exact = A.binomialTailExact(n,p,k);
    var bound = A.chernoffBound(n,p,lam);
    $(root,'.out').innerHTML = '<p>$\\mu=np=$'+fnum(mu)+', ngưỡng $k=\\lceil(1+\\lambda)\\mu\\rceil=$'+k+'</p>'+
      tbl(['Đại lượng','Giá trị'], [['$\\mathbb P(X\\ge k)$ chính xác', fnum(exact)], ['Chặn Chernoff $2e^{-\\lambda^2\\mu/3}$', fnum(bound)]])+
      '<p class="'+(exact<=bound?'ok':'no')+'">'+(exact<=bound?'✓ chặn Chernoff ≥ xác suất thật, đúng chiều bất đẳng thức':'✗ có gì đó sai')+
      ' — λ càng nhỏ, chặn Chernoff càng lỏng so với giá trị thật.</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.unionbound = function(root){
  frame(root,'Union bound: CountMin cần bao nhiêu hàng?',
    '<div class="row"><label>Xác suất lỗi mong muốn δ = <input id="d" type="number" value="0.01" step="0.01" style="width:90px"></label><button class="btn" id="go">Tính số hàng L</button></div><div class="out"></div>'+
    '<div class="row" style="margin-top:10px"><label>So sánh union bound với xác suất đúng (độc lập): xác suất mỗi sự kiện p = <input id="p" type="number" value="0.05" step="0.01" style="width:80px"></label><label>số sự kiện n = <input id="nn" type="number" value="20" style="width:70px"></label><button class="btn" id="go2">So sánh</button></div><div class="out2"></div>');
  function run(){
    var d=+$(root,'#d').value, L=A.countMinRowsNeeded(d);
    $(root,'.out').innerHTML='<p>Cần $L=\\lceil\\log_2(1/\\delta)\\rceil=$<b>'+L+'</b> hàng độc lập để xác suất lỗi $\\le\\delta=$'+d+' (vì $2^{-L}\\le\\delta$).</p>';
    renderMath(root);
  }
  function run2(){
    var p=+$(root,'#p').value, nn=+$(root,'#nn').value;
    var probs = Array.from({length:nn},function(){return p;});
    var r = A.unionBoundCheck(probs);
    $(root,'.out2').innerHTML = tbl(['Union bound ($\\sum p_i$)','Xác suất đúng khi độc lập ($1-\\prod(1-p_i)$)'],[[fnum(r.bound), fnum(r.exact)]])+
      '<p><small>Union bound luôn ≥ xác suất đúng (chặn trên hợp lệ dù không độc lập); khi p nhỏ và n vừa phải, 2 giá trị gần nhau.</small></p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; $(root,'#go2').onclick=run2; run(); run2();
};

W.induction = function(root){
  frame(root,'Kiểm chứng bằng thực nghiệm: $\\mathbb E[2^{X_n}]=n+1$ (Morris)',
    '<div class="row"><label>n tối đa = <input id="nmax" type="number" value="12" style="width:70px"></label><label>số lần lặp mỗi n = <input id="tr" type="number" value="400" style="width:80px"></label><button class="btn" id="go">Chạy thực nghiệm</button></div><div class="out"></div>');
  function run(){
    var nmax=+$(root,'#nmax').value, tr=+$(root,'#tr').value;
    var rows = A.morrisInductionCheck(nmax, tr);
    $(root,'.out').innerHTML = tbl(['n','$\\mathbb E[2^{X_n}]$ thực nghiệm','Lý thuyết $n+1$'],
      rows.map(function(r){ return [r.n, fnum(r.empiricalE2X), r.theoryE2X]; }))+
      '<p><small>Thực nghiệm càng gần lý thuyết khi số lần lặp càng lớn (luật số lớn).</small></p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.fm = function(root){
  frame(root,'FM lý tưởng hoá: $\\hat t=1/X-1$ với $X=\\min$ của $t$ giá trị Uniform(0,1)',
    '<div class="row"><label>t (số phần tử phân biệt thật) = <input id="t" type="number" value="50" style="width:80px"></label><label>số lần chạy độc lập = <input id="tr" type="number" value="300" style="width:80px"></label><button class="btn" id="go">Chạy</button></div><div class="out"></div>');
  function run(){
    var t=+$(root,'#t').value, tr=+$(root,'#tr').value;
    var r = A.fmRun(t, tr);
    $(root,'.out').innerHTML = '<p>Giá trị thật $t=$'+t+'</p>'+
      tbl(['Thống kê trên '+tr+' lần chạy','Giá trị'],[
        ['Trung bình cộng', fnum(r.mean)], ['Trung vị', fnum(r.median)], ['Nhỏ nhất', fnum(r.min)], ['Lớn nhất', fnum(r.max)]
      ])+
      '<div class="callout warn"><div class="lbl">Quan sát thật từ demo này</div>Trung bình cộng bị kéo lệch rất mạnh bởi vài lần chạy ngoại lai ($X$ rất gần 0 ⟹ $1/X$ bùng nổ — hệ quả bất đẳng thức Jensen vì $1/x$ là hàm lồi). Trung vị ổn định hơn nhiều nhưng vẫn hơi lệch cao so với t thật. Đây chính là lý do thực tế: FM thô gần như không dùng được 1 mình, cần KMV (buổi 3, giữ nhiều giá trị băm) hoặc kỹ thuật trung vị hoá (buổi 4).</div>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.vectornorm = function(root){
  frame(root,'Tính $F_0,F_1,F_2$ của một luồng dữ liệu',
    '<div class="row"><label>Luồng (token cách nhau bởi khoảng trắng): <input id="s" size="50" value="a b a c a b d a e b c c f"></label><button class="btn" id="go">Tính</button></div><div class="out"></div>');
  function run(){
    var tokens = toks($(root,'#s').value);
    var fm = A.freqMapFromTokens(tokens);
    var r = A.vectorNorms(fm);
    $(root,'.out').innerHTML = '<p>Biểu đồ tần suất: '+Object.keys(fm).map(function(k){return k+':'+fm[k];}).join(', ')+'</p>'+
      tbl(['Đại lượng','Công thức','Giá trị'],[
        ['$F_0$ (phần tử phân biệt)','$\\|x\\|_0$', r.F0],
        ['$F_1$ (độ dài luồng)','$\\|x\\|_1$', r.F1],
        ['$F_2$','$\\|x\\|_2^2$', r.F2],
        ['$\\|x\\|_2$', '$\\sqrt{F_2}$', fnum(r.norm2)]
      ]);
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.sketchmatrix = function(root){
  frame(root,'Sketch tuyến tính $\\Pi x$: cập nhật tức thời so với tính lại từ đầu',
    '<div class="row"><label>Ma trận $\\Pi$ (mỗi hàng 1 dòng, số cách nhau khoảng trắng):</label></div>'+
    '<textarea id="A" rows="2" style="width:100%">1 0 1\n0 1 1</textarea>'+
    '<div class="row"><label>Danh sách cập nhật (i,Δ) cách nhau dấu chấm phẩy: <input id="u" size="30" value="0,2; 1,3; 2,1; 0,-1"></label><button class="btn" id="go">Chạy streaming</button></div><div class="out"></div>');
  function run(){
    var A2 = $(root,'#A').value.trim().split('\n').map(function(l){ return nums(l); });
    var n = A2[0].length;
    var updates = $(root,'#u').value.trim().split(';').map(function(s){ var p=nums(s); return [p[0], p[1]]; });
    var r = A.streamingUpdateCheck(A2, new Array(n).fill(0), updates);
    $(root,'.out').innerHTML = '<p>Sketch sau khi cập nhật TỪNG BƯỚC (cộng dồn $\\Delta\\cdot\\Pi^{(i)}$): ['+r.y.map(fnum).join(', ')+']</p>'+
      '<p>Tính TRỰC TIẾP $\\Pi x_{\\text{final}}$ từ đầu: ['+r.direct.map(fnum).join(', ')+']</p>'+
      '<p class="'+(r.match?'ok':'no')+'">'+(r.match?'✓ khớp hoàn toàn — minh chứng tính tuyến tính cho phép cập nhật tức thời':'✗ không khớp')+'</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.ams = function(root){
  frame(root,'AMS sketch: ước lượng $F_2=\\|x\\|_2^2$ bằng tổng có dấu ngẫu nhiên',
    '<div class="row"><label>Vector x: <input id="x" size="30" value="3 -2 5 1 -4 2 6"></label><label>Số lần lặp = <input id="tr" type="number" value="500" style="width:80px"></label><button class="btn" id="go">Ước lượng</button></div><div class="out"></div>');
  function run(){
    var x = nums($(root,'#x').value), tr=+$(root,'#tr').value;
    var r = A.amsEstimate(x, tr);
    $(root,'.out').innerHTML = tbl(['Đại lượng','Giá trị'],[
      ['$F_2$ thật ($\\sum x_i^2$)', r.trueF2],
      ['Trung bình $Y^2$ qua '+tr+' lần (mỗi lần 1 bộ dấu σ mới)', fnum(r.meanEstimate)]
    ])+'<p><small>Mỗi lần lặp dùng 1 bộ dấu Rademacher độc lập mới — trung bình nhiều lần tiến gần $F_2$ thật (không chệch).</small></p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.countmin = function(root){
  frame(root,'CountMin sketch thật: xây bảng đếm từ luồng dữ liệu',
    '<div class="row"><label>Luồng: <input id="s" size="50" value="x x y x z y x w x y x v x y"></label></div>'+
    '<div class="row"><label>L (số hàng) = <input id="L" type="number" value="3" style="width:60px"></label><label>B (số ô/hàng) = <input id="B" type="number" value="8" style="width:60px"></label><button class="btn" id="go">Xây CountMin &amp; truy vấn</button></div><div class="out"></div>');
  function run(){
    var tokens = toks($(root,'#s').value), L=+$(root,'#L').value, B=+$(root,'#B').value;
    var cm = A.countMinBuild(tokens, L, B);
    var trueCount = {}; tokens.forEach(function(t){ trueCount[t]=(trueCount[t]||0)+1; });
    var rows = Object.keys(trueCount).map(function(k){ return [k, trueCount[k], A.countMinQuery(cm,k)]; });
    $(root,'.out').innerHTML = tbl(['Phần tử','Đếm THẬT','Ước lượng CountMin (min qua '+L+' hàng)'], rows)+
      '<p><small>Ước lượng CountMin luôn $\\ge$ đếm thật (chỉ lệch 1 chiều do va chạm hàm băm) — đây là đặc điểm riêng của mô hình chỉ-chèn.</small></p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.rank = function(root){
  frame(root,'Rank &amp; Quantile trên mảng đã sắp xếp',
    '<div class="row"><label>Mảng (số cách nhau khoảng trắng): <input id="arr" size="40" value="2 4 7 7 9 12 15 18 20 23"></label></div>'+
    '<div class="row"><label>Truy vấn rank(x), x = <input id="x" type="number" value="9" style="width:70px"></label><label>Truy vấn quantile(φ), φ = <input id="phi" type="number" value="0.5" step="0.1" style="width:70px"></label><button class="btn" id="go">Tính</button></div><div class="out"></div>');
  function run(){
    var arr = nums($(root,'#arr').value).sort(function(a,b){return a-b;});
    var x=+$(root,'#x').value, phi=+$(root,'#phi').value;
    var rk = A.rank(arr, x), q = A.quantile(arr, phi);
    $(root,'.out').innerHTML = '<p>Mảng đã sắp xếp: ['+arr.join(', ')+'] (n='+arr.length+')</p>'+
      tbl(['Truy vấn','Kết quả'],[['rank('+x+')', rk],['quantile('+phi+')', q]]);
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.boruvka = function(root){
  frame(root,'Chạy Borůvka từng vòng trên đồ thị nhỏ',
    '<div class="row"><label>Số đỉnh n = <input id="n" type="number" value="8" style="width:70px"></label><label>Cạnh (u,v cách nhau dấu chấm phẩy): <input id="e" size="50" value="0,1; 1,2; 2,3; 3,0; 4,5; 5,6; 6,7; 7,4; 1,5; 3,7"></label><button class="btn" id="go">Chạy Borůvka</button></div><div class="out"></div>');
  function run(){
    var n=+$(root,'#n').value;
    var edges = $(root,'#e').value.trim().split(';').map(function(s){ return nums(s); });
    var r = A.boruvkaRun(n, edges);
    $(root,'.out').innerHTML = tbl(['Vòng','Số thành phần còn lại','Số cạnh hợp nhất vòng này'],
      r.rounds.map(function(rd){ return [rd.round, rd.componentsAfter, rd.mergedEdges]; }))+
      '<p>Kết quả: còn <b>'+r.finalComponents+'</b> thành phần liên thông sau <b>'+r.rounds.length+'</b> vòng (dự đoán lý thuyết $O(\\log n)$ vòng, $n='+n+'\\Rightarrow\\log_2 n\\approx'+fnum(Math.log2(n))+'$).</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.schwartzzippel = function(root){
  frame(root,'Kiểm chứng bổ đề Schwartz–Zippel',
    '<div class="row"><label>Hệ số đa thức $a_0,a_1,\\dots$ (hằng số trước, cách nhau khoảng trắng): <input id="c" size="30" value="6 -5 1"></label><label>p (nguyên tố) = <input id="p" type="number" value="101" style="width:80px"></label><label>Số lần thử z ngẫu nhiên = <input id="tr" type="number" value="5000" style="width:90px"></label><button class="btn" id="go">Kiểm tra</button></div><div class="out"></div>');
  function run(){
    var coeffs = nums($(root,'#c').value), p=+$(root,'#p').value, tr=+$(root,'#tr').value;
    var r = A.schwartzZippelTest(coeffs, p, tr);
    $(root,'.out').innerHTML = '<p>Đa thức bậc $d='+r.degree+'$ trên $\\mathbb F_{'+p+'}$.</p>'+
      tbl(['Đại lượng','Giá trị'],[
        ['Tần suất thực nghiệm $h(z)=0$', fnum(r.empirical)],
        ['Chặn lý thuyết $d/p$', fnum(r.theoryBound)]
      ])+'<p class="'+(r.empirical<=r.theoryBound*1.5?'ok':'no')+'">Tần suất thực nghiệm nên xấp xỉ hoặc nhỏ hơn chặn $d/p$ (số nghiệm thực tế của đa thức này $\\le d$).</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

/* ---------- 10 demo "Lập lịch trong hệ thống phân tán" ---------- */

W.ll01_scenario = function(root){
  frame(root,'Chọn giả thiết → hiện đúng mục tiêu lập lịch phù hợp',
    '<div class="row"><label>Thời điểm biết tin: <select id="t1"><option value="offline">Offline (biết trước)</option><option value="online">Online (biết khi đến)</option></select></label>'+
    '<label>Ngắt được: <select id="t2"><option value="no">Không ngắt</option><option value="yes">Ngắt được</option></select></label>'+
    '<label>Phụ thuộc: <select id="t3"><option value="indep">Độc lập</option><option value="dag">DAG</option></select></label>'+
    '<label>Trọng số: <select id="t4"><option value="no">Không có</option><option value="yes">Có w_j</option></select></label>'+
    '<button class="btn" id="go">Xem gợi ý</button></div><div class="out"></div>');
  function run(){
    var offline=$(root,'#t1').value==='offline', preempt=$(root,'#t2').value==='yes', dag=$(root,'#t3').value==='dag', wgt=$(root,'#t4').value==='yes';
    var sug;
    if (dag) sug = 'List Scheduling trên DAG (buổi ll-03) — mục tiêu $\\min C_{max}$, chỉ chọn tác vụ đã sẵn sàng.';
    else if (preempt && !offline) sug = 'SRPT (buổi ll-05) — công việc đến động, ngắt được, tối ưu tổng thời gian trong hệ thống.';
    else if (wgt) sug = 'Quy tắc Smith (buổi ll-04) — một máy, có trọng số, tối thiểu $\\sum w_jC_j$.';
    else if (!wgt && offline && !preempt && !dag) sug = 'List Scheduling/LPT (buổi ll-02) nếu nhiều máy giảm $C_{max}$, hoặc SPT (buổi ll-04) nếu 1 máy giảm $\\sum C_j$.';
    else sug = 'Xem bảng tra cứu tổng hợp ở buổi ll-10 để chọn chính xác hơn theo đúng ràng buộc của bạn.';
    $(root,'.out').innerHTML = '<div class="callout info"><div class="lbl">Gợi ý thuật toán</div>'+sug+'</div>'+
      '<p><small>Đây là gợi ý sơ bộ dựa trên giả thiết chọn — không thay thế việc đọc kỹ điều kiện áp dụng ở từng buổi.</small></p>';
    renderMath(root);
  }
  ['t1','t2','t3','t4'].forEach(function(id){ $(root,'#'+id).onchange = run; });
  $(root,'#go').onclick=run; run();
};

W.listscheduling = function(root){
  frame(root,'List Scheduling vs LPT — Gantt chart và so với cận dưới OPT',
    '<div class="row"><label>Tên tác vụ (cách nhau khoảng trắng): <input id="labs" size="30" value="A B C D E F"></label></div>'+
    '<div class="row"><label>Thời gian xử lý $p_j$: <input id="pj" size="30" value="2 3 4 6 7 8"></label><label>Số máy m = <input id="m" type="number" value="3" style="width:60px"></label><button class="btn" id="go">Chạy List Scheduling &amp; LPT</button></div><div class="out"></div>');
  function ganttRow(name, rows, m){
    var html = '<p><b>'+name+'</b></p><div class="t" style="font-family:monospace;font-size:.82rem;line-height:1.9">';
    for (var i=0;i<m;i++){
      var segs = rows.filter(function(r){return r.machine===i;}).sort(function(a,b){return a.S-b.S;});
      html += 'M'+(i+1)+': '+segs.map(function(s){return s.label+'['+fnum(s.S)+'-'+fnum(s.C)+']';}).join(' ')+'<br>';
    }
    return html+'</div>';
  }
  function run(){
    var labs = toks($(root,'#labs').value), pj = nums($(root,'#pj').value), m = +$(root,'#m').value;
    var ls = A.listSchedule(labs, pj, m);
    var lpt = A.lpt(labs, pj, m);
    $(root,'.out').innerHTML = '<p>Cận dưới OPT $\\ge\\max(W/m,\\max p_j)=$ <b>'+fnum(ls.lowerBound)+'</b> (W='+ls.W+')</p>'+
      ganttRow('List Scheduling (theo thứ tự nhập)', ls.rows, m) + '<p>$C_{max}=$<b>'+fnum(ls.Cmax)+'</b>, tỉ lệ $C_{max}/$OPT$\\approx$'+fnum(ls.Cmax/ls.lowerBound)+'</p>'+
      ganttRow('LPT (sắp giảm dần trước khi chạy)', lpt.rows, m) + '<p>$C_{max}=$<b>'+fnum(lpt.Cmax)+'</b>, tỉ lệ $C_{max}/$OPT$\\approx$'+fnum(lpt.Cmax/ls.lowerBound)+'</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.dagschedule = function(root){
  frame(root,'List Scheduling trên DAG — ví dụ 6 tác vụ (A..F)',
    '<div class="row"><label>$p_j$ (A B C D E F): <input id="pj" size="30" value="3 2 4 2 3 2"></label><label>Số máy m = <input id="m" type="number" value="2" style="width:60px"></label></div>'+
    '<div class="row"><small>Cạnh phụ thuộc mặc định (đúng ví dụ slide tr.16-20): A→C, A→D, B→D, C→E, D→F, F→E.</small></div>'+
    '<button class="btn" id="go">Chạy mô phỏng</button><div class="out"></div>');
  function run(){
    var labs = ['A','B','C','D','E','F'], pj = nums($(root,'#pj').value), m = +$(root,'#m').value;
    var edges = [['A','C'],['A','D'],['B','D'],['C','E'],['D','F'],['F','E']];
    var r = A.dagSchedule(labs, pj, edges, m);
    var rows = r.rows.map(function(x){ return [x.label, x.p, 'M'+(x.machine+1), fnum(x.S), fnum(x.C)]; });
    $(root,'.out').innerHTML = tbl(['Tác vụ','p_j','Máy','Bắt đầu S','Kết thúc C'], rows)+
      '<p>$C_{max}=$<b>'+fnum(r.Cmax)+'</b> (ví dụ gốc: đường găng A→C→E dài 10, OPT≥10).</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.spt_smith = function(root){
  frame(root,'FIFO vs SPT vs Smith trên 1 máy',
    '<div class="row"><label>Tên (cách nhau khoảng trắng): <input id="labs" size="20" value="A B C"></label>'+
    '<label>$p_j$: <input id="pj" size="20" value="6 3 2"></label><label>$w_j$ (để trống = đều bằng 1): <input id="wj" size="20" value="1 3 2"></label></div>'+
    '<button class="btn" id="go">So sánh 3 thứ tự</button><div class="out"></div>');
  function run(){
    var labs = toks($(root,'#labs').value), pj = nums($(root,'#pj').value);
    var wjRaw = $(root,'#wj').value.trim(); var wj = wjRaw ? nums(wjRaw) : labs.map(function(){return 1;});
    var fifo = A.oneMachineOrder(labs, pj, wj);
    var spt = A.sptOrder(labs, pj); var sptRes = A.oneMachineOrder(spt.labels, spt.pj, spt.labels.map(function(l){return wj[labs.indexOf(l)];}));
    var smith = A.smithOrder(labs, pj, wj); var smithRes = A.oneMachineOrder(smith.labels, smith.pj, smith.wj);
    $(root,'.out').innerHTML =
      tbl(['Thứ tự','Trình tự','$\\sum C_j$','$\\sum w_jC_j$'],[
        ['FIFO (nhập ban đầu)', labs.join('→'), fnum(fifo.sumC), fnum(fifo.sumWC)],
        ['SPT ($p_j$ tăng dần)', spt.labels.join('→'), fnum(sptRes.sumC), fnum(sptRes.sumWC)],
        ['Smith ($p_j/w_j$ tăng dần)', smith.labels.join('→'), fnum(smithRes.sumC), fnum(smithRes.sumWC)]
      ])+'<p><small>SPT tối ưu $\\sum C_j$ (không trọng số); Smith tối ưu $\\sum w_jC_j$ khi có trọng số — SPT là trường hợp riêng của Smith khi mọi $w_j$ bằng nhau.</small></p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.srpt = function(root){
  frame(root,'SRPT (ngắt được) vs FIFO (không ngắt) với công việc đến động',
    '<div class="row"><label>Task dạng label,r,p cách nhau dấu chấm phẩy: <input id="jobs" size="40" value="A,0,8; B,1,2"></label></div>'+
    '<button class="btn" id="go">Chạy SRPT &amp; FIFO</button><div class="out"></div>');
  function parseJobs(s){
    return s.trim().split(';').map(function(part){
      var f = part.split(',').map(function(x){return x.trim();});
      return { label: f[0], r: +f[1], p: +f[2] };
    });
  }
  function run(){
    var jobs = parseJobs($(root,'#jobs').value);
    var srpt = A.srptRun(jobs);
    var fifo = A.fifoRun(jobs);
    $(root,'.out').innerHTML =
      '<p><b>SRPT</b>: '+srpt.timeline.map(function(s){return s.label+'['+fnum(s.from)+'-'+fnum(s.to)+']';}).join(' → ')+
      '</p><p>Tổng $\\sum(C_j-r_j)=$ <b>'+fnum(srpt.sumFlow)+'</b></p>'+
      '<p><b>FIFO không ngắt</b>: '+fifo.jobs.map(function(j){return j.label+'['+fnum(j.S)+'-'+fnum(j.C)+']';}).join(' → ')+
      '</p><p>Tổng $\\sum(C_j-r_j)=$ <b>'+fnum(fifo.sumFlow)+'</b></p>'+
      '<p class="'+(srpt.sumFlow<=fifo.sumFlow?'ok':'no')+'">'+(srpt.sumFlow<=fifo.sumFlow?'✓ SRPT ≤ FIFO, đúng tính tối ưu lý thuyết':'✗ kiểm tra lại dữ liệu nhập')+'</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.progressive_filling = function(root){
  frame(root,'Progressive filling: chia công bằng 1 loại tài nguyên',
    '<div class="row"><label>Tổng tài nguyên B = <input id="B" type="number" value="12" style="width:80px"></label><label>Nhu cầu $d_i$ (cách nhau khoảng trắng): <input id="d" size="30" value="2 8 8"></label></div>'+
    '<button class="btn" id="go">Chạy progressive filling</button><div class="out"></div>');
  function run(){
    var B = +$(root,'#B').value, d = nums($(root,'#d').value);
    var r = A.progressiveFilling(B, d);
    var rows = r.steps.map(function(s,i){ return ['Tới mức '+fnum(s.upTo)].concat(s.alloc.map(fnum)); });
    var head = ['Giai đoạn'].concat(d.map(function(_,i){return 'x'+(i+1);}));
    $(root,'.out').innerHTML = tbl(head, rows)+
      '<p>Phần cấp cuối cùng: ['+r.alloc.map(fnum).join(', ')+'], $\\lambda=$'+fnum(r.lambda)+'</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.drf = function(root){
  frame(root,'DRF — Dominant Resource Fairness (2 người dùng)',
    '<div class="row"><label>Tổng CPU = <input id="Rc" type="number" value="9" style="width:70px"></label><label>Tổng RAM(GB) = <input id="Rr" type="number" value="18" style="width:70px"></label></div>'+
    '<div class="row"><label>A: CPU/task,RAM/task = <input id="a" size="10" value="1,4"></label><label>B: CPU/task,RAM/task = <input id="b" size="10" value="3,1"></label></div>'+
    '<button class="btn" id="go">Tính DRF (liên tục &amp; theo từng task)</button><div class="out"></div>');
  function run(){
    var Rc=+$(root,'#Rc').value, Rr=+$(root,'#Rr').value;
    var a = nums($(root,'#a').value), b = nums($(root,'#b').value);
    var cont = A.drfTwoUsers(a,b,Rc,Rr);
    var step = A.drfStepwise(a,b,Rc,Rr,30);
    $(root,'.out').innerHTML = '<p><b>Nghiệm liên tục:</b> $s=$'+fnum(cont.s)+', $x_A=$'+fnum(cont.xA)+', $x_B=$'+fnum(cont.xB)+
      ' — dùng '+fnum(cont.cpuUsed)+' CPU, '+fnum(cont.ramUsed)+' GB RAM.</p>'+
      '<p><b>Cấp phát theo từng task:</b></p>'+
      tbl(['Bước','Cấp cho','xA','xB','sA','sB','CPU dùng','RAM dùng'],
        step.rows.map(function(r){ return [r.step, r.givenTo, r.xA, r.xB, fnum(r.sA), fnum(r.sB), fnum(r.cpu), fnum(r.ram)]; }))+
      '<p>Kết quả rời rạc cuối: $(x_A,x_B)=($'+step.xA+', '+step.xB+'$)$</p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.kafka_assign = function(root){
  frame(root,'So sánh Round Robin, Range, LPT-theo-tải khi gán partition',
    '<div class="row"><label>Tải từng partition P1..Pn (cách nhau khoảng trắng): <input id="loads" size="30" value="8 7 6 3 2 1"></label><label>Số consumer = <input id="mc" type="number" value="3" style="width:60px"></label></div>'+
    '<button class="btn" id="go">So sánh 3 phương án</button><div class="out"></div>');
  function showAssign(title, res){
    return '<p><b>'+title+'</b> — tải lớn nhất: <b>'+fnum(res.maxLoad)+'</b></p>'+
      tbl(['Consumer','Partition nhận','Số lượng','Tổng tải'], res.rows.map(function(r){return [r.consumer, r.parts, r.count, fnum(r.load)];}));
  }
  function run(){
    var loads = nums($(root,'#loads').value), mc = +$(root,'#mc').value;
    var parts = loads.map(function(l,i){ return { id:'P'+(i+1), load:l }; });
    var rr = A.kafkaRoundRobin(parts, mc), rg = A.kafkaRange(parts, mc), lpt = A.kafkaLPT(parts, mc);
    $(root,'.out').innerHTML = showAssign('Round Robin', rr) + showAssign('Range', rg) + showAssign('LPT theo tải', lpt)+
      '<p><small>Cận dưới lý thuyết = tổng tải / số consumer = '+fnum(loads.reduce(function(a,b){return a+b;},0)/mc)+'.</small></p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.kafka_rebalance = function(root){
  frame(root,'Tái cân bằng khi 1 consumer rời nhóm — Round Robin lại vs Sticky',
    '<div class="row"><small>Mặc định dùng đúng ví dụ slide: Round Robin ban đầu C1={P1,P4}, C2={P2,P5}, C3={P3,P6}, tải (8,7,6,3,2,1); C2 rời nhóm.</small></div>'+
    '<button class="btn" id="go">So sánh phân công lại toàn bộ vs Sticky</button><div class="out"></div>');
  function run(){
    var parts = [{id:'P1',load:8},{id:'P2',load:7},{id:'P3',load:6},{id:'P4',load:3},{id:'P5',load:2},{id:'P6',load:1}];
    var before = [{id:'P1',load:8,consumer:0},{id:'P4',load:3,consumer:0},{id:'P2',load:7,consumer:1},{id:'P5',load:2,consumer:1},{id:'P3',load:6,consumer:2},{id:'P6',load:1,consumer:2}];
    var r = A.kafkaRebalanceCompare(parts, before, 1, [0,2]);
    $(root,'.out').innerHTML =
      '<p><b>Round Robin lại toàn bộ</b> — số partition chuyển: <b>'+r.rrMoves+'</b>, tải lớn nhất: '+fnum(r.roundRobin.maxLoad)+'</p>'+
      tbl(['Consumer','Partition nhận','Tải'], r.roundRobin.rows.map(function(x){return [x.consumer,x.parts,fnum(x.load)];}))+
      '<p><b>Sticky (giữ phân công cũ, chỉ gán lại phần mất chủ)</b> — số partition chuyển: <b>'+r.stickyMoves+'</b>, tải lớn nhất: '+fnum(r.sticky.maxLoad)+'</p>'+
      tbl(['Consumer','Partition nhận','Tải'], r.sticky.rows.map(function(x){return [x.consumer,x.parts,fnum(x.load)];}))+
      '<p><small>Sticky luôn chuyển ít partition hơn hoặc bằng — đúng vì chỉ các partition mất chủ mới bắt buộc đổi.</small></p>';
    renderMath(root);
  }
  $(root,'#go').onclick=run; run();
};

W.algo_picker = function(root){
  var table = [
    { cond:'Tác vụ độc lập, nhiều máy, giảm Cmax', algo:'List Scheduling / LPT', note:'Máy giống nhau' },
    { cond:'Tác vụ có phụ thuộc (DAG)', algo:'List Scheduling trên DAG', note:'Chỉ chọn tác vụ đã sẵn sàng' },
    { cond:'1 máy, giảm ΣCj', algo:'SPT', note:'Tất cả có sẵn từ đầu' },
    { cond:'1 máy, giảm Σ wⱼCⱼ', algo:'Smith', note:'Biết pj, wj, có sẵn từ đầu' },
    { cond:'1 máy, tác vụ đến động, ngắt được', algo:'SRPT', note:'Biết độ dài, ngắt không mất phí' },
    { cond:'Chia 1 loại tài nguyên công bằng', algo:'Tăng đều (progressive filling)', note:'Định nghĩa rõ nhu cầu' },
    { cond:'Chia nhiều loại tài nguyên công bằng', algo:'DRF', note:'Xét dominant share' },
    { cond:'Gán partition Kafka theo số lượng', algo:'Round Robin / Range', note:'Phụ thuộc subscription' },
    { cond:'Giảm di chuyển khi tái cân bằng Kafka', algo:'Nguyên tắc sticky', note:'Ưu tiên giữ phân công hợp lệ' }
  ];
  frame(root,'Tra bảng chọn thuật toán theo đặc điểm bài toán',
    '<div class="row"><label>Lọc theo từ khoá (vd "DAG", "Kafka", "1 máy"): <input id="q" size="30" value=""></label></div><div class="out"></div>');
  function run(){
    var q = $(root,'#q').value.trim().toLowerCase();
    var rows = table.filter(function(r){ return !q || (r.cond+r.algo+r.note).toLowerCase().indexOf(q)>=0; })
      .map(function(r){ return [r.cond, r.algo, r.note]; });
    $(root,'.out').innerHTML = tbl(['Bài toán','Thuật toán cơ bản','Điều kiện cần nhớ'], rows);
  }
  $(root,'#q').addEventListener('input', run); run();
};

document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('.sim[data-sim]').forEach(function(root){
    var f = W[root.getAttribute('data-sim')];
    if (f) f(root);
  });
});
})();
