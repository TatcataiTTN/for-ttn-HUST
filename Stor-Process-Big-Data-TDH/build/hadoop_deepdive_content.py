# -*- coding: utf-8 -*-
"""Module tự học SÂU "Hệ sinh thái Hadoop" (Chương 2): 7 module hd-01..hd-07, n = 25..31.

Nguồn sự thật (sửa ở đây, KHÔNG sửa tay file này):
  - hd01_expanded.py .. hd06_expanded.py : nội dung gốc 6 module (đã mở rộng sâu theo chuẩn 02-module-content-standard.md)
  - hd_add_a.py, hd_add_b.py             : phần bổ sung đọc trực tiếp bài báo GFS, MapReduce, Bigtable, Kafka, Chubby, logo, bản đồ tổng hợp
  - hd07_expanded.py (hd07_a/b.py)       : module mới hd-07, ba bài báo của thầy Tạ Duy Hoàng (Phần 8)
File này chỉ lắp ráp: chèn phần bổ sung vào đúng vị trí, gắn logo, thêm câu hỏi quiz, và bọc công thức TeX trong
khối .pd-formula-math bằng $$...$$ (trước đây các công thức này hiển thị thành mã TeX thô vì thiếu dấu phân cách)."""
import copy
import random
import re

from hd01_expanded import HD01_EXPANDED
from hd02_expanded import HD02_EXPANDED
from hd03_expanded import HD03_EXPANDED
from hd04_expanded import HD04_EXPANDED
from hd05_expanded import HD05_EXPANDED
from hd06_expanded import HD06_EXPANDED
from hd07_expanded import HD07_EXPANDED
from hd_add_a import HD01, HD02, HD03
from hd_add_b import HD04, HD05, HD06
from hd_add_common import logos

ADDITIONS = {
    "hd-01-hadoop-hdfs": HD01, "hd-02-mapreduce-yarn": HD02, "hd-03-pig-hive": HD03,
    "hd-04-hbase-sqoop": HD04, "hd-05-kafka": HD05, "hd-06-oozie-zookeeper": HD06,
}

_FORMULA = re.compile(r'(<div class="pd-formula-math">)(.*?)(</div>)', re.S)


def _wrap_formula(m):
    inner = m.group(2).strip()
    if inner.startswith("$"):
        return m.group(0)
    return f'{m.group(1)}$${inner}$${m.group(3)}'


def _balance_quiz(mod):
    """Audit thiên lệch vị trí (build-complete-self-study-system, giai đoạn 4): đáp án đúng trong dữ liệu gốc dồn vào cùng
    một vị trí. Xáo lại thứ tự lựa chọn theo hạt giống cố định (cùng kết quả mỗi lần build) để vị trí đúng phân bố đều A-D."""
    rng = random.Random(mod["n"] * 7919)
    n = len(mod["quiz"])
    slots = []
    while len(slots) < n:
        block = [0, 1, 2, 3]
        rng.shuffle(block)
        slots += block
    for q, target in zip(mod["quiz"], slots[:n]):
        opts = q["opts"]
        right = opts[q["correct"]]
        others = [o for i, o in enumerate(opts) if i != q["correct"]]
        rng.shuffle(others)
        new = others[:target] + [right] + others[target:]
        q["opts"], q["correct"] = new, target
    return mod


def _build(mod):
    mod = copy.deepcopy(mod)
    add = ADDITIONS.get(mod["slug"])
    if add:
        for after, part in sorted(add["inserts"], key=lambda t: -t[0]):
            mod["parts"].insert(after, copy.deepcopy(part))
        mod["quiz"] = mod["quiz"] + copy.deepcopy(add["quiz"])
        heads = add.get("logo_heads", {})
        for p in mod["parts"]:
            for s in p["slides"]:
                if s["h"] in heads:
                    s["body"] = logos(*heads[s["h"]]) + s["body"]
    for p in mod["parts"]:
        for s in p["slides"]:
            s["body"] = _FORMULA.sub(_wrap_formula, s["body"])
    return _balance_quiz(mod)


HADOOP_MODULES = [_build(m) for m in (HD01_EXPANDED, HD02_EXPANDED, HD03_EXPANDED, HD04_EXPANDED,
                                       HD05_EXPANDED, HD06_EXPANDED, HD07_EXPANDED)]
