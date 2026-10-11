# -*- coding: utf-8 -*-
"""Chạy referenceSql của từng câu THẬT trên sqlite3 (dữ liệu thật trong schema_<mod>.sql),
lưu kết quả (columns + rows) vào data/sql/questions_<mod>.json. Không ai gõ tay đáp án.
Nếu referenceSql của bất kỳ câu nào lỗi -> dừng ngay (sys.exit(1)), không bỏ sót câu hỏng.
Dùng: python3 compute_expected.py m02   (hoặc m00, m04, m01, m03...)
"""
import importlib, json, pathlib, shutil, sqlite3, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))

def run_one(schema_sql, q):
    conn = sqlite3.connect(":memory:")
    conn.executescript(schema_sql)
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
    if len(sys.argv) < 2:
        print("Dung: python3 compute_expected.py <mod>  (vd m02)", file=sys.stderr)
        sys.exit(1)
    mod = sys.argv[1]
    schema_path = HERE / f"schema_{mod}.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")
    QUESTIONS = importlib.import_module(f"questions_{mod}").QUESTIONS
    data_sql_dir = HERE.parent.parent / "data" / "sql"
    out_path = data_sql_dir / f"questions_{mod}.json"
    data_sql_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(schema_path, data_sql_dir / schema_path.name)

    out = []
    for q in QUESTIONS:
        cols, rows = run_one(schema_sql, q)
        out.append({
            "id": q["id"], "q": q["q"], "difficulty": q["difficulty"], "topic": q["topic"],
            "referenceSql": q["referenceSql"],
            "expectedCols": cols,
            "expectedRows": [list(r) for r in rows],
        })
        print(f"OK {q['id']} -> {len(rows)} dong, {len(cols)} cot")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nDa ghi {len(out)} cau vao {out_path}")

if __name__ == "__main__":
    main()
