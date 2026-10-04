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

document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('.sim[data-sim]').forEach(function(root){
    var f = W[root.getAttribute('data-sim')];
    if (f) f(root);
  });
});
})();
