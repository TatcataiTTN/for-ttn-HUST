/* Thư viện thuật toán thuần JS (không đụng DOM) — dùng cho các demo tương tác.
   Theo đúng hợp đồng của mẫu PTIT: mỗi hàm nhận tham số, trả cấu trúc dữ liệu đủ để hiển thị. */
(function(global){
'use strict';
var ALG = {};

// ---------- Buổi 1: Morris ----------
ALG.morrisRun = function(n){
  var X = 0;
  for (var i = 0; i < n; i++) if (Math.random() < 1/Math.pow(2, X)) X++;
  return { X: X, estimate: Math.pow(2, X) - 1 };
};
ALG.morrisTrials = function(n, trials){
  var ests = [];
  for (var t = 0; t < trials; t++) ests.push(ALG.morrisRun(n).estimate);
  var mean = ests.reduce(function(a,b){return a+b;}, 0) / trials;
  var variance = ests.reduce(function(a,b){return a+(b-mean)*(b-mean);}, 0) / trials;
  return { n: n, trials: trials, estimates: ests, mean: mean, variance: variance };
};

// ---------- Buổi 2: Markov bound ----------
ALG.markovCheck = function(samples, lambda){
  var EX = samples.reduce(function(a,b){return a+b;}, 0) / samples.length;
  var bound = EX / lambda;
  var empirical = samples.filter(function(x){ return x > lambda; }).length / samples.length;
  return { EX: EX, lambda: lambda, bound: bound, empirical: empirical, valid: empirical <= bound + 1e-9 };
};

// ---------- Buổi 3: Chebyshev + KMV (F0) ----------
ALG.chebyshevCheck = function(samples, lambda){
  var n = samples.length;
  var EX = samples.reduce(function(a,b){return a+b;},0)/n;
  var Var = samples.reduce(function(a,b){return a+(b-EX)*(b-EX);},0)/n;
  var bound = Var / (lambda*lambda);
  var empirical = samples.filter(function(x){ return Math.abs(x-EX) > lambda; }).length / n;
  return { EX: EX, Var: Var, lambda: lambda, bound: bound, empirical: empirical };
};
ALG.kmvEstimate = function(stream, k){
  var seen = {};
  stream.forEach(function(x){ seen[x] = true; });
  var distinctTrue = Object.keys(seen).length;
  // băm bằng hàm giả (deterministic nhưng tán xạ tốt) cho từng phần tử phân biệt
  function hash(x){
    var s = String(x), h = 2166136261;
    for (var i=0;i<s.length;i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return ((h >>> 0) % 1000003) / 1000003;
  }
  var hashes = Object.keys(seen).map(hash).sort(function(a,b){return a-b;});
  var kk = Math.min(k, hashes.length);
  var estimate = kk < hashes.length ? kk / hashes[kk-1] : distinctTrue;
  return { distinctTrue: distinctTrue, k: kk, kthHash: hashes[kk-1], estimate: Math.round(estimate) };
};

// ---------- Buổi 4: Chernoff vs chặn chính xác ----------
function logC(n,k){ // log(n choose k) ổn định số học
  function lf(x){ var r=0; for(var i=2;i<=x;i++) r+=Math.log(i); return r; }
  return lf(n)-lf(k)-lf(n-k);
}
ALG.binomialTailExact = function(n, p, k){
  var sum = 0;
  for (var i = k; i <= n; i++) sum += Math.exp(logC(n,i) + i*Math.log(p) + (n-i)*Math.log(1-p));
  return sum;
};
ALG.chernoffBound = function(n, p, lambda){
  var mu = n*p;
  return 2*Math.exp(-lambda*lambda*mu/3);
};

// ---------- Buổi 5: CountMin số hàng cần thiết ----------
ALG.countMinRowsNeeded = function(delta){
  return Math.ceil(Math.log2(1/delta));
};
ALG.unionBoundCheck = function(probs){
  var bound = probs.reduce(function(a,b){return a+b;},0);
  var exact = 1 - probs.reduce(function(a,b){return a*(1-b);}, 1);
  return { bound: bound, exact: exact };
};

// ---------- Buổi 6: kiểm chứng quy nạp Morris ----------
ALG.morrisInductionCheck = function(nMax, trialsPerN){
  var rows = [];
  for (var n = 0; n <= nMax; n++){
    var sum2X = 0;
    for (var t = 0; t < trialsPerN; t++){
      var X = 0;
      for (var i = 0; i < n; i++) if (Math.random() < 1/Math.pow(2,X)) X++;
      sum2X += Math.pow(2, X);
    }
    rows.push({ n: n, empiricalE2X: sum2X/trialsPerN, theoryE2X: n+1 });
  }
  return rows;
};

// ---------- Buổi 7: FM lý tưởng hoá (tail integral) ----------
ALG.fmRun = function(t, trials){
  var ests = [];
  for (var tr = 0; tr < trials; tr++){
    var X = 1;
    for (var i = 0; i < t; i++) X = Math.min(X, Math.random());
    ests.push(1/X - 1);
  }
  var sorted = ests.slice().sort(function(a,b){return a-b;});
  var median = sorted[Math.floor(sorted.length/2)];
  var mean = ests.reduce(function(a,b){return a+b;},0)/trials;
  return { t: t, trials: trials, mean: mean, median: median, min: sorted[0], max: sorted[sorted.length-1] };
};

// ---------- Buổi 8: chuẩn vector ----------
ALG.vectorNorms = function(freqMap){
  var vals = Object.keys(freqMap).map(function(k){ return freqMap[k]; });
  var F0 = vals.filter(function(v){ return v !== 0; }).length;
  var F1 = vals.reduce(function(a,b){ return a+Math.abs(b); }, 0);
  var F2 = vals.reduce(function(a,b){ return a+b*b; }, 0);
  return { F0: F0, F1: F1, F2: F2, norm2: Math.sqrt(F2) };
};
ALG.freqMapFromTokens = function(tokens){
  var m = {};
  tokens.forEach(function(t){ m[t] = (m[t]||0)+1; });
  return m;
};

// ---------- Buổi 9: ma trận-vector (sketch tuyến tính) ----------
ALG.matvec = function(A, x){
  return A.map(function(row){
    var s = 0; for (var j=0;j<x.length;j++) s += row[j]*x[j];
    return s;
  });
};
ALG.streamingUpdateCheck = function(A, x, updates){
  // updates: [[i, delta], ...]; so sánh cập nhật tức thời vs tính lại từ đầu
  var y = ALG.matvec(A, x.map(function(){return 0;}));
  var xFinal = x.map(function(){return 0;});
  updates.forEach(function(u){
    var i = u[0], delta = u[1];
    for (var r=0;r<A.length;r++) y[r] += delta*A[r][i];
    xFinal[i] += delta;
  });
  var direct = ALG.matvec(A, xFinal);
  var match = y.every(function(v,idx){ return Math.abs(v-direct[idx]) < 1e-9; });
  return { y: y, direct: direct, match: match };
};

// ---------- Buổi 10: AMS (Rademacher, F2) ----------
ALG.amsEstimate = function(x, trials){
  var trueF2 = x.reduce(function(a,b){ return a+b*b; }, 0);
  var ests = [];
  for (var t=0;t<trials;t++){
    var Y = 0;
    for (var i=0;i<x.length;i++) Y += (Math.random()<0.5?1:-1)*x[i];
    ests.push(Y*Y);
  }
  var mean = ests.reduce(function(a,b){return a+b;},0)/trials;
  return { trueF2: trueF2, meanEstimate: mean, trials: trials };
};

// ---------- Buổi 11: CountMin thật ----------
function hashFn(seed){
  return function(x){
    var s = seed+'|'+String(x), h = 2166136261;
    for (var i=0;i<s.length;i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return (h>>>0);
  };
}
ALG.countMinBuild = function(stream, L, B){
  var hashes = []; for (var r=0;r<L;r++) hashes.push(hashFn('row'+r));
  var table = []; for (var r2=0;r2<L;r2++) table.push(new Array(B).fill(0));
  stream.forEach(function(x){
    for (var r3=0;r3<L;r3++) table[r3][hashes[r3](x) % B]++;
  });
  return { table: table, hashes: hashes, L: L, B: B };
};
ALG.countMinQuery = function(cm, x){
  var vals = cm.hashes.map(function(h, r){ return cm.table[r][h(x) % cm.B]; });
  return Math.min.apply(null, vals);
};

// ---------- Buổi 12: rank/quantile ----------
ALG.rank = function(sortedArr, x){
  return sortedArr.filter(function(v){ return v <= x; }).length;
};
ALG.quantile = function(sortedArr, phi){
  var idx = Math.max(0, Math.min(sortedArr.length-1, Math.floor(phi*sortedArr.length)));
  return sortedArr[idx];
};

// ---------- Buổi 13: Borůvka ----------
ALG.boruvkaRun = function(n, edges){
  var parent = []; for (var i=0;i<n;i++) parent.push(i);
  function find(x){ while (parent[x]!==x){ parent[x]=parent[parent[x]]; x=parent[x]; } return x; }
  function union(a,b){ var ra=find(a), rb=find(b); if (ra!==rb) parent[ra]=rb; }
  var rounds = [];
  var active = edges.slice();
  var comps = n;
  var guard = 0;
  while (comps > 1 && guard < 50){
    guard++;
    var cheapest = {}; // comp -> edge index
    for (var e=0;e<active.length;e++){
      var u = active[e][0], v = active[e][1];
      var ru = find(u), rv = find(v);
      if (ru === rv) continue;
      if (cheapest[ru] === undefined) cheapest[ru] = e;
      if (cheapest[rv] === undefined) cheapest[rv] = e;
    }
    var merged = 0;
    Object.keys(cheapest).forEach(function(c){
      var e2 = active[cheapest[c]];
      if (find(e2[0]) !== find(e2[1])) { union(e2[0], e2[1]); merged++; }
    });
    var newComps = {}; for (var i2=0;i2<n;i2++) newComps[find(i2)] = true;
    comps = Object.keys(newComps).length;
    rounds.push({ round: rounds.length+1, componentsAfter: comps, mergedEdges: merged });
    if (merged === 0) break;
  }
  return { rounds: rounds, finalComponents: comps };
};

// ---------- Buổi 14: Schwartz-Zippel ----------
ALG.evalPolyMod = function(coeffs, x, p){
  var result = 0;
  for (var i = coeffs.length-1; i>=0; i--) result = (result*x + coeffs[i]) % p;
  return ((result % p) + p) % p;
};
ALG.schwartzZippelTest = function(coeffs, p, trials){
  var zeroCount = 0;
  for (var t=0;t<trials;t++){
    var z = Math.floor(Math.random()*p);
    if (ALG.evalPolyMod(coeffs, z, p) === 0) zeroCount++;
  }
  var degree = coeffs.length - 1;
  return { zeroCount: zeroCount, trials: trials, empirical: zeroCount/trials, theoryBound: degree/p, degree: degree, p: p };
};

global.ALG = ALG;
if (typeof module !== 'undefined' && module.exports) module.exports = ALG;
})(typeof window !== 'undefined' ? window : globalThis);
