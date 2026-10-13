# -*- coding: utf-8 -*-
"""Sinh ngân hàng trắc nghiệm Module 05 (Bài tập lớn) — dùng bank_common.py chung."""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from facts_m05 import FACTS
from bank_common import BankBuilder, audit

SEED = 20260413
OUT = HERE.parent.parent / "data" / "bank" / "bank_m05.json"

b = BankBuilder(SEED)
for f in FACTS:
    b.add(q=f"{f['term']} — chọn mô tả ĐÚNG:", correct=f["definition"], wrongs=f["wrong"],
          topic=f["topic"], src=f["src"], qid=f["id"])

b.write(OUT)
audit(b.items, label="Module 05")
