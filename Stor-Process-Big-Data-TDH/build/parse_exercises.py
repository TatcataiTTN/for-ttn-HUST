#!/usr/bin/env python3
"""Bóc tách các file .md bài tập gốc thành JSON theo buổi, dùng để build trang HTML.
Nguồn: thư mục Hoc/ (không sửa file gốc, chỉ đọc)."""
import re, json, pathlib

HOC = pathlib.Path("/Users/tuannghiat/Downloads/HUST - Lưu trữ và xử lý dữ liệu lớn - Tạ Duy Hoàng/Hoc")
OUT = pathlib.Path(__file__).parent / "exercises.json"

def split_by_buoi(text, heading_re):
    """Trả về dict {so_buoi: [dòng nội dung phần đó]} dựa theo heading '## Buổi N ...'"""
    parts = {}
    current = None
    buf = []
    for line in text.splitlines():
        m = heading_re.match(line)
        if m:
            if current is not None:
                parts[current] = buf
            current = int(m.group(1))
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        parts[current] = buf
    return parts

def extract_items(lines):
    """Trích các dòng '1. ...' '2. ...' liên tiếp thành list string, gộp các dòng con (code block, indent)."""
    items = []
    cur = None
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            if cur is not None:
                cur += ("\n" + line)
            continue
        m = re.match(r"^(\d+)\.\s+(.*)", line)
        if m and not in_code:
            if cur is not None:
                items.append(cur.strip())
            cur = m.group(2)
        elif cur is not None:
            cur += ("\n" + line)
    if cur is not None:
        items.append(cur.strip())
    return items

heading_buoi = re.compile(r"^##\s+Buổi\s+(\d+)")

# ---- Bai-tap-nen-tang.md : Phần 1 (20/buổi) + Phần 2 (10/buổi) ----
nentang = (HOC / "Bai-tap-nen-tang.md").read_text(encoding="utf-8")
p1_marker = "# Phần 1"
p2_marker = "# Phần 2"
i1 = nentang.index(p1_marker)
i2 = nentang.index(p2_marker)
phan1_text = nentang[i1:i2]
phan2_text = nentang[i2:]

phan1_by_buoi = split_by_buoi(phan1_text, heading_buoi)
phan2_by_buoi = split_by_buoi(phan2_text, heading_buoi)

phan1 = {k: extract_items(v) for k, v in phan1_by_buoi.items()}
phan2 = {k: extract_items(v) for k, v in phan2_by_buoi.items()}

# ---- Bai-tap-tu-luan.md : 10 bài "vừa" / buổi ----
tuluan_text = (HOC / "Bai-tap-tu-luan.md").read_text(encoding="utf-8")
tuluan_by_buoi = split_by_buoi(tuluan_text, heading_buoi)
tuluan = {k: extract_items(v) for k, v in tuluan_by_buoi.items()}

# ---- Bai-tap-slide.md : 20 bài áp dụng slide (không chia buổi, để riêng) ----
slide_text = (HOC / "Bai-tap-slide.md").read_text(encoding="utf-8")
slide_lines = slide_text.splitlines()
slide_items = extract_items(slide_lines)

# ---- Lấy tiêu đề buổi (từ Ke-hoach-2-tuan.md nếu có, không thì lấy heading trong Bai-tap-nen-tang) ----
titles = {}
for k, v in phan1_by_buoi.items():
    pass
# lấy title từ chính heading line gốc
title_re = re.compile(r"^##\s+Buổi\s+(\d+)\s+—\s+(.*)")
for line in phan1_text.splitlines():
    m = title_re.match(line)
    if m:
        titles[int(m.group(1))] = m.group(2).strip()

data = {
    "titles": titles,
    "phan1": phan1,
    "phan2": phan2,
    "tuluan": tuluan,
    "slide": slide_items,
}

OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
for b in range(1, 15):
    print(b, titles.get(b), len(phan1.get(b, [])), len(phan2.get(b, [])), len(tuluan.get(b, [])))
print("slide items:", len(slide_items))
