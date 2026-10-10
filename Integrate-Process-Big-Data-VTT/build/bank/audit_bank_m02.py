# -*- coding: utf-8 -*-
"""Audit thiên lệch ngân hàng Module 02 — vị trí đáp án đúng (chi-square) + tỉ lệ đáp án đúng
dài nhất tuyệt đối. Theo 04-quiz-bias-audit.md của skill build-complete-self-study-system."""
import json, pathlib, collections

OUT = pathlib.Path(__file__).parent.parent.parent / "data" / "bank" / "bank_m02.json"
items = json.loads(OUT.read_text(encoding="utf-8"))

n = len(items)
pos_count = collections.Counter(it["correct"] for it in items)
print(f"Tổng số câu: {n}")
print("Phân bố vị trí đáp án đúng (0=A,1=B,2=C,3=D):", dict(pos_count))
expected = n / 4
chi2 = sum((pos_count.get(i, 0) - expected) ** 2 / expected for i in range(4))
print(f"Chi-square (kỳ vọng mỗi vị trí {expected:.1f} câu): {chi2:.2f}  (an toàn nếu < ~7.8 ở mức 95%, df=3)")

longest_is_correct = 0
for it in items:
    lens = [len(o) for o in it["opts"]]
    if lens[it["correct"]] == max(lens) and lens.count(max(lens)) == 1:
        longest_is_correct += 1
print(f"Số câu đáp án đúng là đáp án DÀI NHẤT tuyệt đối: {longest_is_correct}/{n} ({100*longest_is_correct/n:.1f}%)"
      "  (an toàn nếu < ~30%)")

dupes = collections.Counter(it["id"] for it in items)
bad = [k for k, v in dupes.items() if v > 1]
print("ID trùng lặp:", bad if bad else "không có")

print("\nPhân bố theo nguồn (src):", dict(collections.Counter(it["src"] for it in items)))
print("Phân bố theo chủ đề (topic):", dict(collections.Counter(it["topic"] for it in items)))
