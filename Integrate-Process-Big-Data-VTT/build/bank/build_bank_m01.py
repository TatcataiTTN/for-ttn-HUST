# -*- coding: utf-8 -*-
"""Sinh ngân hàng trắc nghiệm Module 01 (Data Integration overview)."""
import pathlib, random, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from facts_m01 import FACTS
from bank_common import BankBuilder, audit

SEED = 20260212
OUT = HERE.parent.parent / "data" / "bank" / "bank_m01.json"

COMPARE_QS = [
  dict(q="Virtual Integration và Data Warehousing khác nhau cơ bản ở điểm nào?",
       correct="Virtual: dữ liệu ở nguyên nguồn, truy cập query-time qua wrapper; Warehousing: copy định kỳ về kho tập trung (ETL)",
       topic="Kiến trúc",
       wrong=["2 kiến trúc này hoàn toàn giống nhau, chỉ khác tên gọi",
              "Virtual Integration luôn chạy chậm hơn Data Warehousing trong mọi trường hợp",
              "Data Warehousing không cần ETL, chỉ Virtual Integration mới cần"]),
  dict(q="Vì sao Data Warehousing cho phép chạy data mining/ML dễ hơn Virtual Integration?",
       correct="Vì dữ liệu đã copy về kho, có thể chạy tính toán nặng tuỳ ý trên bản copy mà không làm phiền nguồn gốc",
       topic="Kiến trúc",
       wrong=["Vì Data Warehousing luôn có phần cứng mạnh hơn Virtual Integration",
              "Vì Virtual Integration không hỗ trợ bất kỳ loại truy vấn nào",
              "Vì ML chỉ chạy được trên dữ liệu đã ETL, không chạy được trên dữ liệu thô"]),
  dict(q="DBMS và Data Integration khác nhau ở tầng trừu tượng nào?",
       correct="DBMS = trừu tượng logical vs physical (trong 1 CSDL); Data Integration = trừu tượng bậc cao hơn, che giấu sự khác biệt GIỮA NHIỀU nguồn độc lập",
       topic="Khái niệm nền",
       wrong=["2 khái niệm này hoàn toàn giống nhau, Data Integration chỉ là tên gọi khác của DBMS",
              "DBMS luôn ở tầng cao hơn Data Integration (bị đảo ngược)",
              "Data Integration chỉ hoạt động được khi không có DBMS nào cả"]),
  dict(q="Structural Heterogeneity và Semantic Heterogeneity khác nhau ở điểm nào?",
       correct="Structural: khác cách TỔ CHỨC bảng/khoá/độ chi tiết; Semantic: khác Ý NGHĨA thuật ngữ (đồng nghĩa/đa nghĩa)",
       topic="Heterogeneity",
       wrong=["2 loại dị biệt này hoàn toàn giống nhau, chỉ khác tên gọi",
              "Semantic Heterogeneity chỉ xảy ra ở cấp độ vật lý (ổ đĩa), không liên quan ngữ nghĩa",
              "Structural Heterogeneity chỉ giải quyết được bằng Entity Resolution"]),
  dict(q="Instance/Identity Heterogeneity khác với 6 mức dị biệt còn lại ở điểm nào, và giải quyết bằng kỹ thuật học ở buổi nào?",
       correct="Nó xảy ra ở mức DỮ LIỆU THỰC THỂ (không phải schema) — giải quyết bằng Entity Resolution/Record Linkage, học ở buổi 4",
       topic="Heterogeneity",
       wrong=["Nó giống hoàn toàn Structural Heterogeneity, học ở buổi 3",
              "Nó chỉ là vấn đề định dạng file, giải quyết bằng đổi tên cột",
              "Nó không cần giải quyết, có thể bỏ qua an toàn"]),
]

def main():
    b = BankBuilder(SEED)
    for f in FACTS:
        b.add(f"'{f['term']}' được định nghĩa như thế nào (theo đúng nội dung slide buổi 2)?", f["definition"], f["wrong"], f["topic"], f["src"], f"m01-t1-{f['id']}")
    all_terms = [f["term"] for f in FACTS]
    for f in FACTS:
        others = [t for t in all_terms if t != f["term"]]
        distract = random.Random(SEED + hash(f["id"])).sample(others, 3)
        b.add(f"Định nghĩa sau mô tả đúng khái niệm nào? — \"{f['definition']}\"", f["term"], distract, f["topic"], f["src"], f"m01-t2-{f['id']}")
    for f in FACTS:
        b.add(f"Phát biểu nào sau đây về {f['term']} là ĐÚNG?", f["definition"], f["wrong"], f["topic"], f["src"], f"m01-t3-{f['id']}")
    for i, c in enumerate(COMPARE_QS):
        b.add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m01-t4-{i:02d}")
    b.write(OUT)
    audit(b.items, "Module 01")

if __name__ == "__main__":
    main()
