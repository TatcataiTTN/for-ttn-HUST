# -*- coding: utf-8 -*-
"""Sinh ngân hàng trắc nghiệm Module 06 (Sources Profiling & Selection)."""
import pathlib, random, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from facts_m06 import FACTS
from bank_common import BankBuilder, audit

SEED = 20260214
OUT = HERE.parent.parent / "data" / "bank" / "bank_m06.json"

# Ví dụ số đã verify thủ công trong Explain-05-SourcesSelection.md (trang 20, 23-24)
WORKED_QS = [
  dict(q="Cho A={1,2,3,4}, B={2,3,4,5}. Min-hash resemblance ρ(A,B) = |A∩B|/|A∪B| là bao nhiêu?",
       correct="3/5 = 0.60 (|A∩B|={2,3,4} có 3 phần tử, |A∪B|={1,2,3,4,5} có 5 phần tử)",
       topic="Source Profiling & Selection",
       wrong=["4/5 = 0.80", "3/4 = 0.75", "2/5 = 0.40"]),
  dict(q="Với HLRT, cần trích n=2 thuộc tính (vd tên nước + mã điện thoại). Theo công thức 2n+2, cần bao nhiêu chuỗi mốc (delimiter)?",
       correct="6 chuỗi mốc (h, t, l1, r1, l2, r2)", topic="HLRT & Stalker",
       wrong=["4 chuỗi mốc (chỉ l1,r1,l2,r2, bỏ h/t)", "2 chuỗi mốc (chỉ h,t)", "8 chuỗi mốc (2n+4)"]),
  dict(q="Bảng ví dụ: A(benefit=100,cost=40), B(80,30), C(60,20), A+C(150,60). Với ngân sách $70, tập con nào cho profit (benefit−cost) cao nhất trong số các tập hợp lệ (cost≤70)?",
       correct="A+C, profit = 150−60 = 90", topic="Chọn nguồn (Selection)",
       wrong=["A+B+C, profit = 160−90 = 70 nhưng cost=90 VƯỢT ngân sách 70 nên không hợp lệ", "B+C, profit = 120−50 = 70", "A đơn lẻ, profit = 100−40 = 60"]),
  dict(q="Theo bảng suy luận bắc cầu: đã biết L1 (R2=R3, match) và L2 (R1=R2, match). Có thể suy ra ngay nhãn của cặp (R1,R3) là gì mà KHÔNG cần hỏi người?",
       correct="Match (A=B và B=C ⟹ A=C, suy luận bắc cầu hợp lệ)", topic="Crowdsourcing",
       wrong=["Non-match", "Không suy luận được, luôn phải hỏi người với mọi cặp mới", "Possible-match, cần thêm bằng chứng"]),
]

def main():
    b = BankBuilder(SEED)
    for f in FACTS:
        b.add(f"'{f['term']}' được định nghĩa như thế nào (theo đúng nội dung slide Sources Profiling & Selection)?", f["definition"], f["wrong"], f["topic"], f["src"], f"m06-t1-{f['id']}")
    all_terms = [f["term"] for f in FACTS]
    for f in FACTS:
        others = [t for t in all_terms if t != f["term"]]
        distract = random.Random(SEED + hash(f["id"])).sample(others, 3)
        b.add(f"Định nghĩa sau mô tả đúng khái niệm nào? — \"{f['definition']}\"", f["term"], distract, f["topic"], f["src"], f"m06-t2-{f['id']}")
    for f in FACTS:
        b.add(f"Phát biểu nào sau đây về {f['term']} là ĐÚNG?", f["definition"], f["wrong"], f["topic"], f["src"], f"m06-t3-{f['id']}")
    for i, c in enumerate(WORKED_QS):
        b.add(c["q"], c["correct"], c["wrong"], c["topic"], "gốc-slide (ví dụ số, đã verify thủ công)", f"m06-t8-{i:02d}")
    b.write(OUT)
    audit(b.items, "Module 06")

if __name__ == "__main__":
    main()
