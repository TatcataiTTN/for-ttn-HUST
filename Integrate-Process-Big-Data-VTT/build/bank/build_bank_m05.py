# -*- coding: utf-8 -*-
"""Sinh ngân hàng trắc nghiệm Module 05 (Bài tập lớn) — dùng bank_common.py chung."""
import pathlib, random, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from facts_m05 import FACTS
from bank_common import BankBuilder, audit

SEED = 20260413
OUT = HERE.parent.parent / "data" / "bank" / "bank_m05.json"

# Áp dụng dữ liệu thật của SQL sandbox module 05 (3 bảng nasa_power_ngay/openmeteo_ngay/ghcn_tram,
# trích thật từ data_samples/batch_week2/ đồ án Nhóm 16 — xem build/sql-bank/schema_m05.sql) thành
# câu hỏi khái niệm bổ sung, KHÔNG bịa số liệu.
WORKED_QS = [
  dict(q="Trong SQL sandbox module 05, vì sao không thể JOIN trực tiếp nasa_power_ngay và openmeteo_ngay theo (vi_do, kinh_do) bằng dấu '=' để so sánh nhiệt độ cùng 1 thành phố?",
       correct="Vì mỗi nguồn tự ghi toạ độ tâm lưới/trạm độc lập (số thực nhiều chữ số thập phân), gần như không bao giờ trùng tuyệt đối — cần so khớp theo thành_phố hoặc ngưỡng khoảng cách, không so bằng dấu '='",
       topic="Kiến trúc đồ án",
       wrong=["Vì 2 bảng không có cột toạ độ nào, phải tự thêm trước khi JOIN",
              "Vì SQLite (sql.js) không hỗ trợ JOIN giữa 2 bảng khác tên",
              "Vì toạ độ ở nasa_power_ngay luôn là số nguyên còn ở openmeteo_ngay luôn là chuỗi, không so sánh được"]),
  dict(q="Bảng ghcn_tram trong SQL sandbox module 05 lưu dữ liệu theo cấu trúc Entity-Attribute-Value (mỗi dòng 1 element như TMAX/TMIN/PRCP), khác hẳn 2 bảng nasa_power_ngay/openmeteo_ngay (mỗi biến 1 cột). Để so sánh nhiệt độ TMAX của 1 trạm GHCN với nhiet_do_max_c của Open-Meteo cùng ngày, bước xử lý nào là BẮT BUỘC trước khi so sánh?",
       correct="Lọc/PIVOT bảng ghcn_tram theo element='TMAX' trước, rồi mới JOIN theo ngày — không thể so trực tiếp vì ghcn_tram gộp nhiều loại biến trong cùng 1 cột gia_tri",
       topic="Kiến trúc đồ án",
       wrong=["Không cần xử lý gì thêm, JOIN trực tiếp 2 bảng theo ngay là so sánh đúng ngay",
              "Phải xoá bảng ghcn_tram vì SQLite không hỗ trợ cấu trúc EAV",
              "Chỉ cần đổi tên cột gia_tri thành nhiet_do_max_c là so sánh được"]),
]

b = BankBuilder(SEED)
for f in FACTS:
    b.add(q=f"{f['term']} — chọn mô tả ĐÚNG:", correct=f["definition"], wrongs=f["wrong"],
          topic=f["topic"], src=f["src"], qid=f["id"])

# T2: định nghĩa -> thuật ngữ (framing ngược, cùng pattern các module khác)
all_terms = [f["term"] for f in FACTS]
for f in FACTS:
    others = [t for t in all_terms if t != f["term"]]
    distract = random.Random(SEED + hash(f["id"]) % 100000).sample(others, 3)
    b.add(q=f"Mô tả sau nói về thuật ngữ/mốc nào? — \"{f['definition']}\"", correct=f["term"],
          wrongs=distract, topic=f["topic"], src=f["src"], qid=f"{f['id']}-t2")

for i, c in enumerate(WORKED_QS):
    b.add(q=c["q"], correct=c["correct"], wrongs=c["wrong"], topic=c["topic"],
          src="data thật module (áp dụng SQL sandbox)", qid=f"m05-worked-{i:02d}")

b.write(OUT)
audit(b.items, label="Module 05")
