# -*- coding: utf-8 -*-
"""Thư viện chung để sinh ngân hàng trắc nghiệm cho MỌI module — tách ra từ build_bank_m02.py
để build_bank_m00/01/03/04.py không phải chép lại logic cân bằng vị trí + chống length-bias.
"""
import json, pathlib, random

FILLERS = [
    " — một cách diễn giải hay gặp nhưng không khớp với định nghĩa đã học trong môn này",
    " — nhầm lẫn phổ biến giữa 2 khái niệm có tên gần giống nhau",
    " — đúng trong 1 ngữ cảnh khác, không đúng với ngữ cảnh đang xét ở đây",
    " — chỉ đúng một phần, còn thiếu điều kiện quan trọng để kết luận chắc chắn",
    " — cách hiểu sai thường gặp ở người mới bắt đầu học khái niệm này",
    " — mô tả gần đúng nhưng đảo ngược vai trò giữa 2 thành phần liên quan",
]

def debias_length(correct, wrongs, qid):
    """Nếu đáp án đúng là đáp án DÀI NHẤT tuyệt đối (unique max), kéo dài đáp án nhiễu ngắn nhất
    bằng 1 câu đệm trung lập (chọn theo hash để không có 1 câu đệm cố định trở thành dấu hiệu)."""
    opts = [correct] + list(wrongs)
    for _round in range(3):
        lens = [len(o) for o in opts]
        if not (lens[0] == max(lens) and lens.count(max(lens)) == 1):
            break
        shortest_i = min(range(1, 4), key=lambda i: lens[i])
        filler = FILLERS[hash((qid, shortest_i, _round)) % len(FILLERS)]
        opts[shortest_i] = opts[shortest_i] + filler
    return opts[0], opts[1:]

def balanced_options(correct, wrongs, slot, rng_local):
    opts = [correct] + list(wrongs)
    rng_local.shuffle(opts)
    cur = opts.index(correct)
    opts[cur], opts[slot] = opts[slot], opts[cur]
    return opts, slot

class BankBuilder:
    """Gom add() + cân bằng vị trí round-robin + chống length-bias, dùng chung cho mọi module."""
    def __init__(self, seed):
        self.seed = seed
        self.slot_cycle = [0, 1, 2, 3]
        self.si = 0
        self.items = []

    def add(self, q, correct, wrongs, topic, src, qid):
        assert len(wrongs) == 3, f"{qid} can dung 3 phuong an nhieu, co {len(wrongs)}"
        correct, wrongs = debias_length(correct, wrongs, qid)
        local_rng = random.Random(self.seed + hash(qid) % 100000)
        opts, correct_idx = balanced_options(correct, wrongs, self.slot_cycle[self.si % 4], local_rng)
        self.si += 1
        self.items.append(dict(id=qid, q=q, opts=opts, correct=correct_idx, topic=topic, src=src,
                                explain=f"Đáp án đúng: {correct}"))

    def write(self, out_path: pathlib.Path):
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(self.items, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Da sinh {len(self.items)} cau -> {out_path}")

def audit(items, label=""):
    import collections
    n = len(items)
    pos_count = collections.Counter(it["correct"] for it in items)
    expected = n / 4
    chi2 = sum((pos_count.get(i, 0) - expected) ** 2 / expected for i in range(4))
    longest_is_correct = 0
    for it in items:
        lens = [len(o) for o in it["opts"]]
        if lens[it["correct"]] == max(lens) and lens.count(max(lens)) == 1:
            longest_is_correct += 1
    dupes = collections.Counter(it["id"] for it in items)
    bad = [k for k, v in dupes.items() if v > 1]
    print(f"\n=== Audit {label} ===")
    print(f"Tổng số câu: {n}")
    print("Phân bố vị trí đáp án đúng:", dict(pos_count), f"  chi2={chi2:.2f} (an toàn <~7.8)")
    pct = 100 * longest_is_correct / n
    print(f"Đáp án đúng = dài nhất tuyệt đối: {longest_is_correct}/{n} ({pct:.1f}%, an toàn <~30%)")
    print("ID trùng lặp:", bad if bad else "không có")
    print("Theo nguồn:", dict(collections.Counter(it["src"] for it in items)))
    print("Theo chủ đề:", dict(collections.Counter(it["topic"] for it in items)))
    assert chi2 < 7.8, f"FAIL: chi2 qua cao ({chi2:.2f})"
    assert pct < 30, f"FAIL: length-bias qua cao ({pct:.1f}%)"
    assert not bad, f"FAIL: id trung lap {bad}"
    print("=> PASS audit\n")
