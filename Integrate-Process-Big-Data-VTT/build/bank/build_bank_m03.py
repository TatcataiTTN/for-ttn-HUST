# -*- coding: utf-8 -*-
"""Sinh ngân hàng trắc nghiệm Module 03 (Mediation Query & Big Data Challenges)."""
import pathlib, random, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from facts_m03 import FACTS
from bank_common import BankBuilder, audit

SEED = 20260213
OUT = HERE.parent.parent / "data" / "bank" / "bank_m03.json"

COMPARE_QS = [
  dict(q="Join Graph và Partial Mapping đóng vai trò khác nhau thế nào trong quy trình sinh Mediation Query?",
       correct="Partial Mapping xác định TỪNG sub-tree tương ứng nguồn nào; Join Graph xác định CÁCH NỐI các nguồn đó lại với nhau qua key/reference key",
       topic="Mediation Query bán cấu trúc",
       wrong=["2 khái niệm này hoàn toàn giống nhau, chỉ khác tên gọi",
              "Join Graph xác định sub-tree, Partial Mapping xác định cách nối (bị đảo ngược vai trò)",
              "Chỉ cần Join Graph là đủ, không cần Partial Mapping"]),
  dict(q="FeatureRank và SchemaRank trong WebTables khác nhau ở điểm nào?",
       correct="SchemaRank = FeatureRank + đo độ nhất quán schema qua Pointwise Mutual Information giữa các thuộc tính",
       topic="WebTables Ranking",
       wrong=["2 thuật toán này hoàn toàn độc lập, không cái nào kế thừa cái nào",
              "FeatureRank dùng PMI, SchemaRank chỉ dùng đặc trưng bảng (bị đảo ngược)",
              "SchemaRank chỉ áp dụng được cho bảng tiếng Việt"]),
  dict(q="4 lý do Data Integration truyền thống không đủ ở quy mô Big Data gồm những gì?",
       correct="Deep Web at Scale, Schema Explosion, Modeling Everything, Keyword Queries",
       topic="Vì sao DI truyền thống không đủ ở Big Data",
       wrong=["Chỉ 2 lý do: thiếu phần cứng và thiếu băng thông mạng",
              "Schema Explosion, Data Fusion, Record Linkage, Blocking (nhầm với khái niệm buổi 4)",
              "Chỉ liên quan tới chi phí lưu trữ (storage cost), không liên quan tới schema/truy vấn"]),
  dict(q="Probabilistic Mapping (buổi 3b) khác Probabilistic Mediated Schema (đã học ở phần PAYGO buổi 3a) ở điểm nào?",
       correct="Probabilistic Mediated Schema gắn xác suất cho CẤU TRÚC mediated schema (nhiều phiên bản schema); Probabilistic Mapping gắn xác suất cho ÁNH XẠ (nhiều mapping khả dĩ giữa 1 schema cố định và nguồn)",
       topic="PAYGO & Big Data (mở rộng)",
       wrong=["2 khái niệm này hoàn toàn giống nhau, chỉ khác tên gọi",
              "Probabilistic Mapping chỉ áp dụng được khi KHÔNG dùng PAYGO",
              "Chỉ Probabilistic Mediated Schema mới có xác suất, Probabilistic Mapping là mapping chắc chắn 100%"]),
]

def main():
    b = BankBuilder(SEED)
    for f in FACTS:
        b.add(f"'{f['term']}' được định nghĩa như thế nào (theo đúng nội dung slide buổi 3)?", f["definition"], f["wrong"], f["topic"], f["src"], f"m03-t1-{f['id']}")
    all_terms = [f["term"] for f in FACTS]
    for f in FACTS:
        others = [t for t in all_terms if t != f["term"]]
        distract = random.Random(SEED + hash(f["id"])).sample(others, 3)
        b.add(f"Định nghĩa sau mô tả đúng khái niệm nào? — \"{f['definition']}\"", f["term"], distract, f["topic"], f["src"], f"m03-t2-{f['id']}")
    for f in FACTS:
        b.add(f"Phát biểu nào sau đây về {f['term']} là ĐÚNG?", f["definition"], f["wrong"], f["topic"], f["src"], f"m03-t3-{f['id']}")
    for i, c in enumerate(COMPARE_QS):
        b.add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m03-t4-{i:02d}")
    b.write(OUT)
    audit(b.items, "Module 03")

if __name__ == "__main__":
    main()
