# -*- coding: utf-8 -*-
"""Chạy referenceSql của từng câu THẬT trên sqlite3 (dữ liệu thật trong schema_m02.sql),
lưu kết quả (columns + rows) vào data/questions_m02.json. Không ai gõ tay đáp án.
Nếu referenceSql của bất kỳ câu nào lỗi -> dừng ngay (sys.exit(1)), không bỏ sót câu hỏng.
"""
import json, pathlib, sqlite3, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from questions_m02 import QUESTIONS

SCHEMA_SQL = (HERE / "schema_m02.sql").read_text(encoding="utf-8")
OUT = HERE.parent.parent / "data" / "sql" / "questions_m02.json"

def run_one(q):
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA_SQL)
    cur = conn.cursor()
    try:
        cur.execute(q["referenceSql"])
    except sqlite3.Error as e:
        print(f"LOI referenceSql cau {q['id']}: {e}\nSQL: {q['referenceSql']}", file=sys.stderr)
        sys.exit(1)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchall()
    conn.close()
    return cols, rows

def main():
    out = []
    for q in QUESTIONS:
        cols, rows = run_one(q)
        out.append({
            "id": q["id"], "q": q["q"], "difficulty": q["difficulty"], "topic": q["topic"],
            "referenceSql": q["referenceSql"],
            "expectedCols": cols,
            "expectedRows": [list(r) for r in rows],
        })
        print(f"OK {q['id']} -> {len(rows)} dong, {len(cols)} cot")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nDa ghi {len(out)} cau vao {OUT}")

if __name__ == "__main__":
    main()
