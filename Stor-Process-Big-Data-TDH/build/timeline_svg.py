# -*- coding: utf-8 -*-
"""Sơ đồ timeline nhiều lane dùng chung cho deck Nhóm 1 và module hd-06 (SVG tự vẽ, không sao chép nguồn nào)."""
import math

def tech_timeline_svg():
    """Timeline nhiều lane tự vẽ bằng SVG gốc. Đường nét đứt = ý tưởng/ảnh hưởng (bài báo → công nghệ);
    đường liền = phụ thuộc lúc chạy (chạy trên Hadoop, dùng ZooKeeper, nạp dữ liệu vào Hadoop)."""
    y0, y1 = 2002, 2013
    ml, step = 150, 64
    def X(year): return ml + (year - y0) * step
    W = X(y1) + 150
    H = 470
    lanes = [
        {"label": "Nghiên cứu<br/>nền tảng (Google)", "y": 72, "color": "#2b5ce6"},
        {"label": "Lõi Hadoop", "y": 168, "color": "#0f9d58"},
        {"label": "Streaming", "y": 264, "color": "#c2255c"},
        {"label": "Công cụ<br/>hệ sinh thái", "y": 360, "color": "#d98e00"},
    ]
    # (lane, năm, tên, mô tả, key, dx, hướng nhãn, căn nhãn, lệch nhãn)
    nodes = {
        "GFS": (0, 2003, "GFS", "SOSP 2003", True, 0, "u", "r", 0),
        "MR": (0, 2004, "MapReduce", "OSDI 2004", True, 0, "u", "c", 0),
        "BT": (0, 2006, "Bigtable", "OSDI 2006", True, -8, "u", "r", 0),
        "CH": (0, 2006, "Chubby", "OSDI 2006", False, 8, "u", "l", 0),
        "HD": (1, 2006, "Hadoop", "Tách từ Nutch<br/>(Cutting, Yahoo!)", True, 0, "d", "r", 0),
        "YARN": (1, 2012, "YARN", "Hadoop 2.0: tách<br/>quản lý tài nguyên", True, 0, "u", "c", 0),
        "KF": (2, 2011.1, "Kafka", "Mã nguồn mở (LinkedIn)", True, 0, "u", "l", 14),
        "KR": (2, 2013.2, "KRaft", "2022: Kafka bỏ<br/>ZooKeeper", False, 0, "d", "c", 0),
        "ZK": (3, 2007, "ZooKeeper", "Yahoo Research", False, 0, "d", "c", 0),
        "HB": (3, 2008.25, "HBase", "28/3/2008<br/>(Powerset)", True, 0, "d", "c", 0),
        "PIG": (3, 2008.75, "Pig", "9/2008 (Yahoo)", False, 0, "u", "l", 8),
        "HIVE": (3, 2010.8, "Hive", "10/2010 (Facebook)", True, 0, "u", "l", 8),
        "OZ": (3, 2012.3, "Oozie", "Top-level 2012", False, 0, "d", "c", 0),
    }
    def pos(k):
        n = nodes[k]; return X(n[1]) + n[5], lanes[n[0]]["y"]
    # (từ, đến, kiểu, màu, chú thích ngắn)
    GR = "#7a8499"
    links = [
        ("GFS", "HD", "dash", GR), ("MR", "HD", "dash", GR), ("BT", "HB", "dash", GR), ("CH", "ZK", "dash", GR),
        ("HD", "YARN", "solid", "#0f9d58"),
        ("HD", "HB", "solid", "#0f9d58"), ("HD", "PIG", "solid", "#0f9d58"),
        ("HD", "HIVE", "solid", "#0f9d58"), ("HD", "OZ", "solid", "#0f9d58"),
        ("ZK", "KF", "solid", "#c2255c"), ("ZK", "HB", "solid", "#d98e00"),
    ]
    svg = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Timeline phát triển hệ sinh thái Hadoop">']
    cols = sorted({c for _, _, _, c in links} | {"#c2255c"})
    svg.append("<defs>" + "".join(
        f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in cols) + "</defs>")
    yr = y0
    while yr < y1:
        x = X(yr)
        svg.append(f'<line x1="{x}" y1="36" x2="{x}" y2="410" stroke="var(--border)" stroke-width="1"/>')
        svg.append(f'<text x="{x}" y="440" font-size="13" fill="var(--muted)" text-anchor="middle">{yr}</text>')
        yr += 1
    xb = X(2013.2)
    svg.append(f'<text x="{xb}" y="440" font-size="13" fill="var(--muted)" text-anchor="middle">⋯ 2022</text>')
    for ln in lanes:
        svg.append(f'<line x1="{ml-20}" y1="{ln["y"]}" x2="{xb+30}" y2="{ln["y"]}" stroke="{ln["color"]}" stroke-width="2.5" opacity=".5"/>')
        svg.append(f'<foreignObject x="0" y="{ln["y"]-24}" width="{ml-30}" height="48">'
                   f'<div xmlns="http://www.w3.org/1999/xhtml" style="font:700 14px sans-serif;color:{ln["color"]};'
                   f'text-align:right;line-height:1.25;height:48px;display:flex;align-items:center;justify-content:flex-end">'
                   f'<span>{ln["label"]}</span></div></foreignObject>')
    import math
    def shorten(a, b, r=11):
        dx, dy = b[0]-a[0], b[1]-a[1]; d = math.hypot(dx, dy) or 1
        return (a[0]+dx/d*r, a[1]+dy/d*r), (b[0]-dx/d*(r+2), b[1]-dy/d*(r+2))
    for a, b, kind, col in links:
        pa, pb = shorten(pos(a), pos(b))
        dash = ' stroke-dasharray="5,4"' if kind == "dash" else ""
        svg.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="{col}" '
                   f'stroke-width="{1.4 if kind=="dash" else 1.8}"{dash} opacity=".85" marker-end="url(#ah{col[1:]})"/>')
    # Kafka nạp dữ liệu vào HDFS: mũi tên lên tới lane Hadoop
    kx, ky = pos("KF"); hy = lanes[1]["y"]
    svg.append(f'<line x1="{kx}" y1="{ky-11}" x2="{kx}" y2="{hy+10}" stroke="#c2255c" stroke-width="1.8" marker-end="url(#ah{"c2255c"})"/>')
    svg.append(f'<rect x="{kx-5}" y="{hy-5}" width="10" height="10" transform="rotate(45 {kx} {hy})" fill="var(--panel)" stroke="#0f9d58" stroke-width="2"/>')
    svg.append(f'<foreignObject x="{kx-150}" y="{hy+18}" width="144" height="40"><div xmlns="http://www.w3.org/1999/xhtml" '
               f'style="font:600 11.5px sans-serif;color:#c2255c;text-align:right;line-height:1.2">nạp dữ liệu<br/>vào HDFS</div></foreignObject>')
    for k, (lane_i, year, name, sub, key, dx, side, al, lx) in nodes.items():
        ln = lanes[lane_i]; x = X(year) + dx; y = ln["y"]
        svg.append(f'<circle cx="{x}" cy="{y}" r="{8 if key else 6}" fill="{ln["color"]}" stroke="var(--panel)" stroke-width="2"/>')
        bw = 150
        bx = {"c": x - bw/2, "l": x - 6 + lx, "r": x - bw + 6}[al]
        ta = {"c": "center", "l": "left", "r": "right"}[al]
        ai = {"c": "center", "l": "flex-start", "r": "flex-end"}[al]
        by, just = (y - 12 - 52, "flex-end") if side == "u" else (y + 12, "flex-start")
        svg.append(f'<foreignObject x="{bx}" y="{by}" width="{bw}" height="52">'
                   f'<div xmlns="http://www.w3.org/1999/xhtml" style="height:52px;display:flex;flex-direction:column;'
                   f'justify-content:{just};align-items:{ai};text-align:{ta};font-family:sans-serif">'
                   f'<div style="background:color-mix(in srgb,var(--panel) 90%,transparent);padding:0 3px;border-radius:3px">'
                   f'<div style="font-weight:{"800" if key else "700"};font-size:{"15" if key else "13.5"}px;color:var(--text);line-height:1.15">{name}</div>'
                   f'<div style="font-size:11.5px;color:var(--muted);line-height:1.2">{sub}</div></div></div></foreignObject>')
    svg.append('</svg>')
    return "".join(svg)
