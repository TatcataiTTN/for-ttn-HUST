# -*- coding: utf-8 -*-
"""Helper dùng chung cho các phần bổ sung (hd_add_*.py) của 6 module Hadoop và module hd-07.
Ảnh/hình: crop nguyên trạng từ bài báo gốc trong thư mục References, có ghi nguồn dưới từng hình
(dùng cho bài tập môn học phi thương mại)."""

P = "../../../assets/images/papers/"
L = "../../../assets/images/logos/"


def fig(f, cap, h=300):
    return (f'<figure style="margin:0 0 10px;text-align:center"><img src="{P}{f}" alt="{cap}" '
            f'style="max-height:{h}px;max-width:100%;width:auto;height:auto;border:1px solid var(--border);'
            f'border-radius:8px;background:#fff"><figcaption style="font-size:.78rem;color:var(--muted);'
            f'margin-top:4px">{cap}</figcaption></figure>')


def logo(f, h=34):
    return (f'<img src="{L}{f}" alt="" style="height:{h}px;max-width:150px;width:auto;object-fit:contain;'
            f'vertical-align:middle;background:#fff;padding:3px 6px;border:1px solid var(--border);'
            f'border-radius:6px;margin-right:6px">')


def logos(*fs, h=34):
    return '<p style="margin:0 0 8px">' + "".join(logo(x, h) for x in fs) + "</p>"


def two(left, right, w="50%"):
    """Hai cột: ảnh/bảng bên trái, văn bản bên phải."""
    return (f'<div style="display:flex;gap:22px;align-items:flex-start"><div style="flex:0 0 {w}">{left}</div>'
            f'<div style="flex:1">{right}</div></div>')
