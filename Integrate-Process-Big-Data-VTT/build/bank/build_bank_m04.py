# -*- coding: utf-8 -*-
"""Sinh ngân hàng trắc nghiệm Module 04 (Record Linkage & ER) — dùng bank_common.py chung."""
import pathlib, random, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from facts_m04 import FACTS
from bank_common import BankBuilder, audit

SEED = 20260211
OUT = HERE.parent.parent / "data" / "bank" / "bank_m04.json"

# Chuyển câu GỐC (có đáp số) từ Quiz-Buoi4-RecordLinkage-ER.md thành trắc nghiệm — đúng nguyên tắc
# PTIT: "câu gốc tự luận có đáp số → chuyển thành trắc nghiệm, giữ nhãn nguồn + '(chuyển thành trắc nghiệm)'"
QUIZ_CONVERTED = [
  dict(q="(Quiz buổi 4, câu B1) Edit Distance giữa 'color' và 'colour' là bao nhiêu?",
       correct="1 (chỉ cần chèn ký tự 'u')", topic="Similarity Measures",
       wrong=["0 (2 chuỗi giống nhau)", "2 (cần 2 phép biến đổi)", "6 (bằng độ dài chuỗi dài hơn)"]),
  dict(q="(Quiz buổi 4, câu B2) Similarity score s(x,y)=1-d(x,y)/max(|x|,|y|) giữa 'color' và 'colour' (d=1) là bao nhiêu?",
       correct="5/6 ≈ 0.833", topic="Similarity Measures",
       wrong=["1/6 ≈ 0.167", "1.0 (hoàn toàn giống nhau)", "0.5"]),
  dict(q="(Quiz buổi 4, câu B3) Cho Bx={a,b,c,d}, By={b,c,d,e}. Overlap measure O(x,y) là bao nhiêu?",
       correct="3 (|{b,c,d}|)", topic="Similarity Measures",
       wrong=["4 (|Bx|)", "5 (|Bx∪By|)", "1"]),
  dict(q="(Quiz buổi 4, câu B3) Cùng Bx,By trên, Jaccard measure J(x,y) là bao nhiêu?",
       correct="3/5 = 0.6", topic="Similarity Measures",
       wrong=["3/4 = 0.75", "3/8 = 0.375", "4/5 = 0.8"]),
  dict(q="(Quiz buổi 4, câu B5) Áp dụng đúng 4 bước Soundex, mã của tên 'Williams' là gì?",
       correct="W452", topic="Similarity Measures",
       wrong=["W450", "W4520", "L452"]),
  dict(q="(Quiz buổi 4, câu A4) Theo Fellegi & Sunter (1969), 'possible-link' nghĩa là gì?",
       correct="Chưa đủ bằng chứng để kết luận chắc chắn là match hay non-match",
       topic="Khái niệm nền",
       wrong=["Chắc chắn là match, chỉ chưa xác nhận bằng tay", "Chắc chắn là non-match",
              "Một lỗi hệ thống cần sửa ngay"]),
  dict(q="(Quiz buổi 4, câu A6) Vì sao áp dụng similarity measure cho TẤT CẢ các cặp bị coi là không khả thi ở quy mô lớn?",
       correct="Độ phức tạp bậc hai O(n²) (hay O(|X|×|Y|)) — bùng nổ số cặp cần xét khi n lớn",
       topic="ER Pipeline",
       wrong=["Vì similarity measure luôn cho kết quả sai với n lớn", "Vì SQL không hỗ trợ tính similarity",
              "Độ phức tạp O(log n), nhanh nhưng tốn nhiều RAM"]),
  dict(q="(Quiz buổi 4, câu C1) Thứ tự ĐÚNG của 4 bước Entity Resolution Pipeline là gì?",
       correct="Prepare Data → Blocking/Sorting → Matching → Clustering",
       topic="ER Pipeline",
       wrong=["Blocking → Prepare Data → Clustering → Matching",
              "Matching → Blocking → Prepare Data → Clustering",
              "Clustering → Matching → Blocking → Prepare Data"]),
  dict(q="(Quiz buổi 4, câu C3) Sorted Neighborhood và LSH khác nhau cơ bản ở điểm nào?",
       correct="Sorted Neighborhood cần định nghĩa thủ công 1 sorting key; LSH hash embedding, không cần định nghĩa key thủ công",
       topic="ER Pipeline",
       wrong=["2 kỹ thuật này hoàn toàn giống nhau, chỉ khác tên gọi",
              "LSH cần sorting key thủ công, Sorted Neighborhood dùng hash (bị đảo ngược)",
              "Sorted Neighborhood chỉ dùng được cho số, LSH chỉ dùng được cho chuỗi"]),
  dict(q="(Quiz buổi 4, câu C4) 2 hướng giải pháp khi Learned Matchers thiếu dữ liệu gán nhãn là gì?",
       correct="Transfer Learning (học từ kịch bản nhiều dữ liệu, fine-tune ít nhãn) và Active Learning (chủ động chọn cặp cần gán nhãn)",
       topic="ER Pipeline",
       wrong=["Tăng số lượng cột dữ liệu và giảm số dòng dữ liệu",
              "Chỉ cần dùng Naïve Deduplication thay thế hoàn toàn",
              "Blocking chặt hơn và bỏ qua bước Matching"]),
  dict(q="(Quiz buổi 4, câu D1) Trong project tích hợp khí tượng (trạm điểm vs ô lưới ERA5), vì sao bước 'gán trạm vào ô lưới gần nhất' KHÔNG thể dùng Jaccard/Edit Distance trực tiếp?",
       correct="Vì đây là bài toán khoảng cách KHÔNG GIAN ĐỊA LÝ giữa toạ độ điểm và ô lưới, cần kỹ thuật Spatial Interpolation (Kriging/Bilinear), không phải so khớp chuỗi ký tự",
       topic="Khái niệm nền",
       wrong=["Vì Jaccard/Edit Distance chỉ chạy được trên hệ điều hành Linux",
              "Vì trạm quan trắc không có toạ độ, chỉ có tên",
              "Thực ra vẫn dùng được Jaccard/Edit Distance trực tiếp, không cần kỹ thuật gì thêm"]),
]

def main():
    b = BankBuilder(SEED)
    for f in FACTS:
        b.add(f"'{f['term']}' được định nghĩa như thế nào (theo đúng nội dung slide buổi 4)?", f["definition"], f["wrong"], f["topic"], f["src"], f"m04-t1-{f['id']}")
    all_terms = [f["term"] for f in FACTS]
    for f in FACTS:
        others = [t for t in all_terms if t != f["term"]]
        distract = random.Random(SEED + hash(f["id"])).sample(others, 3)
        b.add(f"Định nghĩa sau mô tả đúng khái niệm nào? — \"{f['definition']}\"", f["term"], distract, f["topic"], f["src"], f"m04-t2-{f['id']}")
    for f in FACTS:
        b.add(f"Phát biểu nào sau đây về {f['term']} là ĐÚNG?", f["definition"], f["wrong"], f["topic"], f["src"], f"m04-t3-{f['id']}")
    for i, c in enumerate(QUIZ_CONVERTED):
        b.add(c["q"], c["correct"], c["wrong"], c["topic"], "gốc-slide (chuyển thành trắc nghiệm)", f"m04-t7-{i:02d}")
    b.write(OUT)
    audit(b.items, "Module 04")

if __name__ == "__main__":
    main()
