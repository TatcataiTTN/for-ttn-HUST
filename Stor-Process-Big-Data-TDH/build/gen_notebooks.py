# -*- coding: utf-8 -*-
import json, pathlib, sys, uuid
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from modules_content import MODULES

ROOT = pathlib.Path(__file__).parent.parent
EX = json.loads((pathlib.Path(__file__).parent / "exercises.json").read_text(encoding="utf-8"))

def _id():
    return uuid.uuid4().hex[:8]

def md_cell(src):
    return {"cell_type": "markdown", "id": _id(), "metadata": {}, "source": src.splitlines(keepends=True)}

def code_cell(src):
    return {"cell_type": "code", "id": _id(), "execution_count": None, "metadata": {}, "outputs": [], "source": src.splitlines(keepends=True)}

def build_notebook(mod):
    n = mod["n"]
    items = EX["phan2"].get(str(n), [])
    cells = [md_cell(
        f"# Buổi {n}: {mod['title']}\n\n"
        f"Notebook thực hành Python đi kèm module **{mod['title']}** — hệ thống tự học "
        f"*Lưu trữ & xử lý dữ liệu lớn*.\n\n"
        f"10 bài dưới đây trích nguyên văn từ bộ bài tập nền tảng Phần 2 (thuật toán/mã giả Python). "
        f"Mỗi bài có 1 ô markdown đề bài + 1 ô code trống để bạn tự làm.\n\n"
        f"> Chạy được trên Jupyter local hoặc mở thẳng trên [Google Colab](https://colab.research.google.com/) "
        f"(tải file này lên rồi mở)."
    ), code_cell("import math, random, time\n")]
    for i, it in enumerate(items, 1):
        cells.append(md_cell(f"## Bài {i}\n\n{it}"))
        cells.append(code_cell("# TODO: làm bài tại đây\n"))
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10"}
        },
        "nbformat": 4, "nbformat_minor": 5
    }
    out = ROOT / "data" / "notebooks" / "modules" / f"{n:02d}_{mod['slug']}.ipynb"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return out

if __name__ == "__main__":
    for m in MODULES:
        p = build_notebook(m)
        print("wrote", p.name)
