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

// ---------- Lập lịch (lap_lich_50_slides.pdf) ----------

// List Scheduling theo đúng THỨ TỰ cho sẵn trong labels/pj. LPT = gọi hàm này sau khi tự sắp giảm dần.
ALG.listSchedule = function(labels, pj, m){
  var load = new Array(m).fill(0);
  var rows = labels.map(function(lab, idx){
    var best = 0;
    for (var i=1;i<m;i++) if (load[i] < load[best]) best = i;
    var S = load[best], C = S + pj[idx];
    load[best] += pj[idx];
    return { label: lab, p: pj[idx], machine: best, S: S, C: C };
  });
  var Cmax = Math.max.apply(null, load);
  var W = pj.reduce(function(a,b){return a+b;}, 0);
  var lb = Math.max(W/m, Math.max.apply(null, pj));
  return { rows: rows, load: load, Cmax: Cmax, W: W, lowerBound: lb };
};
ALG.lpt = function(labels, pj, m){
  var idx = labels.map(function(_,i){return i;}).sort(function(a,b){ return pj[b]-pj[a]; });
  return ALG.listSchedule(idx.map(function(i){return labels[i];}), idx.map(function(i){return pj[i];}), m);
};

// Lập lịch DAG bằng List Scheduling event-driven. edges: [[u,v],...] nghĩa là v phụ thuộc u.
ALG.dagSchedule = function(labels, pj, edges, m){
  var n = labels.length;
  var idxOf = {}; labels.forEach(function(l,i){ idxOf[l]=i; });
  var preds = labels.map(function(){return [];}), succs = labels.map(function(){return [];});
  edges.forEach(function(e){ var u=idxOf[e[0]], v=idxOf[e[1]]; preds[v].push(u); succs[u].push(v); });
  var done = new Array(n).fill(false), doneAt = new Array(n).fill(null);
  var machineFree = new Array(m).fill(0);
  var started = new Array(n).fill(false);
  var events = [];
  var remaining = n;
  var t = 0;
  // mô phỏng rời rạc đơn giản: tại mỗi bước, gán tác vụ sẵn sàng cho máy rảnh sớm nhất
  var queue = [];
  function readyNow(j){ return !started[j] && preds[j].every(function(u){ return done[u]; }); }
  var assigned = new Array(n).fill(null); // {machine,S,C}
  var remainingTasks = n, iter = 0;
  while (remainingTasks > 0 && iter < 10000){
    iter++;
    // tìm máy rảnh sớm nhất và tác vụ sẵn sàng tại thời điểm đó
    var earliestMachine = 0;
    for (var i=1;i<m;i++) if (machineFree[i] < machineFree[earliestMachine]) earliestMachine = i;
    var tNow = machineFree[earliestMachine];
    var cand = null;
    for (var j=0;j<n;j++){
      if (!started[j] && readyNow(j)){ if (cand===null) cand = j; }
    }
    if (cand === null){
      // không có tác vụ sẵn sàng — nhảy thời gian tới sự kiện hoàn thành gần nhất
      var nextDone = Infinity;
      assigned.forEach(function(a){ if (a && a.C > tNow && a.C < nextDone) nextDone = a.C; });
      if (!isFinite(nextDone)) break;
      machineFree[earliestMachine] = nextDone;
      continue;
    }
    started[cand] = true;
    var S = tNow, C = tNow + pj[cand];
    assigned[cand] = { machine: earliestMachine, S: S, C: C };
    machineFree[earliestMachine] = C;
    done[cand] = true; // đánh dấu ngay để tính sẵn sàng cho vòng sau (đã bắt đầu = coi như theo thứ tự tô pô ở mô hình đơn giản này)
    remainingTasks--;
  }
  var rows = labels.map(function(l,i){ return { label:l, p: pj[i], machine: assigned[i].machine, S: assigned[i].S, C: assigned[i].C }; });
  var Cmax = Math.max.apply(null, rows.map(function(r){return r.C;}));
  return { rows: rows, Cmax: Cmax };
};

// FIFO / SPT / Smith trên 1 máy — thứ tự cho trước, trả về Cj và tổng (có trọng số)
ALG.oneMachineOrder = function(labels, pj, wj){
  var t = 0; var rows = labels.map(function(l,i){ var C = t + pj[i]; t = C; return { label:l, p:pj[i], w:(wj?wj[i]:1), C:C }; });
  var sum = rows.reduce(function(a,r){return a+r.C;},0);
  var wsum = rows.reduce(function(a,r){return a+r.w*r.C;},0);
  return { rows: rows, sumC: sum, sumWC: wsum };
};
ALG.sptOrder = function(labels, pj){
  var idx = labels.map(function(_,i){return i;}).sort(function(a,b){ return pj[a]-pj[b]; });
  return { labels: idx.map(function(i){return labels[i];}), pj: idx.map(function(i){return pj[i];}) };
};
ALG.smithOrder = function(labels, pj, wj){
  var idx = labels.map(function(_,i){return i;}).sort(function(a,b){ return (pj[a]/wj[a]) - (pj[b]/wj[b]); });
  return { labels: idx.map(function(i){return labels[i];}), pj: idx.map(function(i){return pj[i];}), wj: idx.map(function(i){return wj[i];}) };
};

// SRPT (ngắt được) vs FIFO (không ngắt) — tasks: [{label,r,p}], mô phỏng rời rạc theo đơn vị thời gian nhỏ nhất.
ALG.srptRun = function(tasks){
  var jobs = tasks.map(function(t){ return { label:t.label, r:t.r, p:t.p, rem:t.p, C:null }; });
  var t = Math.min.apply(null, jobs.map(function(j){return j.r;}));
  var timeline = [];
  var remainingCount = jobs.length;
  while (remainingCount > 0){
    var avail = jobs.filter(function(j){ return j.r<=t && j.rem>0; });
    if (avail.length===0){ var nextR = Math.min.apply(null, jobs.filter(function(j){return j.rem>0;}).map(function(j){return j.r;})); t = nextR; continue; }
    avail.sort(function(a,b){ return a.rem-b.rem; });
    var run = avail[0];
    var nextArrival = Math.min.apply(null, jobs.filter(function(j){return j.r>t;}).map(function(j){return j.r;}).concat([Infinity]));
    var step = Math.min(run.rem, nextArrival-t);
    step = step>0?step:run.rem;
    timeline.push({label:run.label, from:t, to:t+step});
    t += step; run.rem -= step;
    if (run.rem<=0){ run.C = t; remainingCount--; }
  }
  var sum = jobs.reduce(function(a,j){ return a+(j.C-j.r); },0);
  return { jobs: jobs, timeline: timeline, sumFlow: sum };
};
ALG.fifoRun = function(tasks){
  var jobs = tasks.slice().sort(function(a,b){ return a.r-b.r; });
  var t = 0; var out = [];
  jobs.forEach(function(j){ var S=Math.max(t,j.r), C=S+j.p; out.push({label:j.label,r:j.r,p:j.p,S:S,C:C}); t=C; });
  var sum = out.reduce(function(a,j){return a+(j.C-j.r);},0);
  return { jobs: out, sumFlow: sum };
};

// Progressive filling: B tổng, demands[]
ALG.progressiveFilling = function(B, demands){
  var n = demands.length;
  var sorted = demands.map(function(d,i){return {d:d,i:i};}).sort(function(a,b){return a.d-b.d;});
  var alloc = new Array(n).fill(0);
  var steps = [];
  var remaining = B, active = n;
  for (var k=0;k<sorted.length;k++){
    var cur = sorted[k].d;
    var prevLevel = k>0?sorted[k-1].d:0;
    var delta = cur - prevLevel;
    var give = Math.min(delta, remaining/active);
    for (var j=k;j<n;j++) alloc[sorted[j].i] += give;
    remaining -= give*active;
    steps.push({ upTo: prevLevel+give, alloc: alloc.slice() });
    if (give < delta){ break; } // hết tài nguyên giữa chừng
    active--;
    if (remaining<=1e-9) break;
  }
  return { alloc: alloc, steps: steps, lambda: Math.max.apply(null, alloc) };
};

// DRF: 2 người dùng, mỗi người (cpu,ram) trên 1 task, tổng (Rc,Rr)
ALG.drfTwoUsers = function(a, b, Rc, Rr){
  // xA = (Rc/ (a[0]+ (a[0]/b[0])*b[0]))... giải trực tiếp theo tỉ lệ dominant share chung s:
  // xA = s*Rc/a[0] theo chuẩn hoá của dominant resource của A; tổng quát hoá bằng dò nhị phân cho chắc.
  function used(s){
    // với mỗi người, dominant resource là loại có a[r]/R[r] lớn hơn
    var domA = (a[0]/Rc >= a[1]/Rr) ? 0 : 1;
    var domB = (b[0]/Rc >= b[1]/Rr) ? 0 : 1;
    var R = [Rc, Rr];
    var xA = s * R[domA] / a[domA];
    var xB = s * R[domB] / b[domB];
    return { xA: xA, xB: xB, cpu: xA*a[0]+xB*b[0], ram: xA*a[1]+xB*b[1] };
  }
  var lo=0, hi=1;
  for (var it=0; it<60; it++){
    var mid=(lo+hi)/2, u=used(mid);
    if (u.cpu<=Rc && u.ram<=Rr) lo=mid; else hi=mid;
  }
  var r = used(lo);
  return { s: lo, xA: r.xA, xB: r.xB, cpuUsed: r.cpu, ramUsed: r.ram };
};
// DRF theo từng task (rời rạc) — chọn người có dominant share nhỏ nhất, hoà thì A trước
ALG.drfStepwise = function(a, b, Rc, Rr, maxSteps){
  var xA=0, xB=0, rows=[];
  for (var k=0;k<(maxSteps||20);k++){
    var cpu = xA*a[0]+xB*b[0], ram = xA*a[1]+xB*b[1];
    var canA = (cpu+a[0]<=Rc) && (ram+a[1]<=Rr);
    var canB = (cpu+b[0]<=Rc) && (ram+b[1]<=Rr);
    if (!canA && !canB) break;
    var sA = Math.max(xA*a[0]/Rc, xA*a[1]/Rr), sB = Math.max(xB*b[0]/Rc, xB*b[1]/Rr);
    var giveA = canA && (!canB || sA<=sB);
    if (giveA) xA++; else xB++;
    cpu = xA*a[0]+xB*b[0]; ram = xA*a[1]+xB*b[1];
    sA = Math.max(xA*a[0]/Rc, xA*a[1]/Rr); sB = Math.max(xB*b[0]/Rc, xB*b[1]/Rr);
    rows.push({ step:k+1, givenTo: giveA?'A':'B', xA:xA, xB:xB, sA:sA, sB:sB, cpu:cpu, ram:ram });
  }
  return { rows: rows, xA: xA, xB: xB };
};

// Kafka: gán partition cho consumer. loads: [{id,load}] đã hoặc chưa sort.
ALG.kafkaRoundRobin = function(parts, mC){
  var assign = parts.map(function(p,i){ return { id:p.id, load:p.load, consumer: i % mC }; });
  return ALG.kafkaSummarize(assign, mC);
};
ALG.kafkaRange = function(parts, mC){
  var n = parts.length, q = Math.floor(n/mC), r = n%mC;
  var assign = [], idx = 0;
  for (var c=0;c<mC;c++){
    var cnt = q + (c<r?1:0);
    for (var k=0;k<cnt;k++){ assign.push({ id:parts[idx].id, load:parts[idx].load, consumer:c }); idx++; }
  }
  return ALG.kafkaSummarize(assign, mC);
};
ALG.kafkaLPT = function(parts, mC){
  var sorted = parts.slice().sort(function(a,b){ return b.load-a.load; });
  var load = new Array(mC).fill(0);
  var assign = sorted.map(function(p){
    var best=0; for (var i=1;i<mC;i++) if (load[i]<load[best]) best=i;
    load[best]+=p.load;
    return { id:p.id, load:p.load, consumer: best };
  });
  return ALG.kafkaSummarize(assign, mC);
};
ALG.kafkaSummarize = function(assign, mC){
  var byC = {};
  assign.forEach(function(a){ (byC[a.consumer]=byC[a.consumer]||[]).push(a); });
  var rows = [];
  for (var c=0;c<mC;c++){
    var items = byC[c]||[];
    rows.push({ consumer:'C'+(c+1), parts: items.map(function(x){return x.id;}).join(', '), count: items.length,
                load: items.reduce(function(s,x){return s+x.load;},0) });
  }
  var maxLoad = Math.max.apply(null, rows.map(function(r){return r.load;}));
  return { rows: rows, maxLoad: maxLoad, assign: assign };
};

// Tái cân bằng khi 1 consumer rời nhóm — so "round robin lại toàn bộ" vs "sticky (giữ phân công còn hợp lệ)"
ALG.kafkaRebalanceCompare = function(parts, assignBefore, leavingConsumer, remainingConsumers){
  // assignBefore: [{id,load,consumer}]
  var lost = assignBefore.filter(function(a){ return a.consumer===leavingConsumer; });
  var kept = assignBefore.filter(function(a){ return a.consumer!==leavingConsumer; });
  // Round robin lại toàn bộ trên remainingConsumers
  var rrAssign = parts.map(function(p,i){ return { id:p.id, load:p.load, consumer: remainingConsumers[i % remainingConsumers.length] }; });
  var rrMoves = rrAssign.filter(function(a){
    var before = assignBefore.filter(function(b){return b.id===a.id;})[0];
    return before.consumer !== a.consumer;
  }).length;
  // Sticky: giữ kept nguyên, gán lost cho consumer có tải nhỏ nhất hiện tại (hoà -> consumer nhỏ hơn)
  var stickyAssign = kept.map(function(a){ return {id:a.id, load:a.load, consumer:a.consumer}; });
  lost.forEach(function(p){
    var loadByC = {}; remainingConsumers.forEach(function(c){ loadByC[c]=0; });
    stickyAssign.forEach(function(a){ loadByC[a.consumer]=(loadByC[a.consumer]||0)+a.load; });
    var best = remainingConsumers[0];
    remainingConsumers.forEach(function(c){ if (loadByC[c]<loadByC[best]) best=c; });
    stickyAssign.push({ id:p.id, load:p.load, consumer: best });
  });
  var stickyMoves = lost.length; // chỉ các partition mất chủ phải chuyển, phần kept giữ nguyên tuyệt đối
  return {
    roundRobin: ALG.kafkaSummarize(rrAssign, Math.max.apply(null,remainingConsumers)+1), rrMoves: rrMoves,
    sticky: ALG.kafkaSummarize(stickyAssign, Math.max.apply(null,remainingConsumers)+1), stickyMoves: stickyMoves
  };
};

global.ALG = ALG;
if (typeof module !== 'undefined' && module.exports) module.exports = ALG;
})(typeof window !== 'undefined' ? window : globalThis);
