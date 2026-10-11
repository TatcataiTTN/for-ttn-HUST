# -*- coding: utf-8 -*-
"""Sinh ngân hàng trắc nghiệm Module 00 (Nền tảng CSDL) — dùng bank_common.py chung."""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from facts_m00 import FACTS
from bank_common import BankBuilder, audit

SEED = 20260207
OUT = HERE.parent.parent / "data" / "bank" / "bank_m00.json"

COMPARE_QS = [
  dict(q="Khoá chính và khoá ngoại khác nhau ở điểm nào?",
       correct="Khoá chính định danh duy nhất dòng TRONG CHÍNH bảng đó; khoá ngoại trỏ TỚI khoá chính của BẢNG KHÁC",
       topic="So sánh Khoá",
       wrong=["Khoá chính và khoá ngoại là 2 tên gọi khác nhau của cùng 1 khái niệm",
              "Khoá ngoại luôn định danh duy nhất dòng, khoá chính thì không",
              "Chỉ bảng trung gian mới có khoá ngoại, bảng thực thể không bao giờ có"]),
  dict(q="Liên kết 1-N và liên kết N-N khác nhau ở cách hiện thực thành bảng quan hệ như thế nào?",
       correct="1-N: chỉ cần thêm 1 khoá ngoại vào bảng ở phía 'N'; N-N: phải tạo 1 bảng trung gian riêng",
       topic="So sánh Khoá",
       wrong=["Cả 2 loại liên kết đều hiện thực giống nhau, chỉ thêm 1 khoá ngoại",
              "1-N cần bảng trung gian, N-N chỉ cần thêm khoá ngoại (bị đảo ngược)",
              "N-N không thể hiện thực được bằng CSDL quan hệ"]),
  dict(q="Vì sao bảng trung gian (junction table) của liên kết N-N thường có khoá chính là TỔ HỢP 2 khoá ngoại?",
       correct="Vì 1 cặp (thực thể A, thực thể B) cụ thể chỉ nên xuất hiện 1 lần trong bảng trung gian — tổ hợp 2 khoá ngoại định danh duy nhất 1 dòng liên kết",
       topic="So sánh Khoá",
       wrong=["Vì SQL yêu cầu bảng trung gian phải có ít nhất 2 cột",
              "Vì tổ hợp khoá giúp bảng chạy nhanh hơn, không liên quan tới tính duy nhất",
              "Vì nếu không tổ hợp khoá thì không thể JOIN được"]),
  dict(q="Dư thừa dữ liệu (Data Redundancy) và Dị thường cập nhật (Update Anomaly) liên hệ với nhau thế nào?",
       correct="Dư thừa dữ liệu (lưu lặp cùng 1 thông tin) là NGUYÊN NHÂN trực tiếp dẫn tới dị thường cập nhật khi sửa không đồng bộ hết các bản lặp",
       topic="So sánh Khoá",
       wrong=["2 khái niệm hoàn toàn không liên quan tới nhau",
              "Dị thường cập nhật là nguyên nhân gây ra dư thừa dữ liệu (bị đảo ngược nhân-quả)",
              "Chỉ xảy ra khi dùng khoá ngoại sai kiểu dữ liệu"]),
  dict(q="Vì sao 2 đội thiết kế CSDL độc lập, cùng chuẩn hoá đúng kỹ thuật, vẫn có thể ra 2 lược đồ (bảng) khác nhau cho cùng 1 miền dữ liệu?",
       correct="Vì chuẩn hoá chỉ đảm bảo không dư thừa/dị thường — không ép buộc duy nhất 1 cách tách bảng cụ thể",
       topic="So sánh Khoá",
       wrong=["Vì 1 trong 2 đội chắc chắn đã làm sai kỹ thuật chuẩn hoá",
              "Vì 2 đội dùng 2 hệ quản trị CSDL khác nhau (MySQL vs PostgreSQL)",
              "Chuẩn hoá đúng kỹ thuật luôn cho ra đúng 1 lược đồ duy nhất, tình huống này không xảy ra"]),
  dict(q="Record Linkage (buổi 4) liên hệ thế nào với khái niệm khoá chính/khoá ngoại đã học ở Module 00?",
       correct="Record Linkage đi tìm lại 'khoá chính ngầm' giữa 2 nguồn không chia sẻ cùng khoá ngoại thật, vì 2 nguồn được thiết kế độc lập",
       topic="Cầu nối sang Data Integration",
       wrong=["Record Linkage không liên quan gì tới khoá chính/khoá ngoại",
              "Record Linkage chỉ cần join trực tiếp bằng khoá ngoại có sẵn giữa 2 nguồn",
              "Khoá chính/khoá ngoại chỉ tồn tại trong 1 CSDL duy nhất, không áp dụng khi có nhiều nguồn"]),
]

SCHEMA_QS = [
  dict(q="Trong ví dụ SQL Sandbox Module 00, vì sao bảng 'thue' cần khoá chính là TỔ HỢP (MaNguoiThue, MaCanHo, NgayBatDau) thay vì chỉ 1 cột?",
       correct="Vì 1 người có thể thuê nhiều căn hộ qua nhiều lần (nhiều NgayBatDau khác nhau) — chỉ (MaNguoiThue,MaCanHo) không đủ phân biệt nếu thuê lại cùng căn hộ ở 2 giai đoạn khác nhau",
       topic="Ví dụ nguoithue-canho-thue",
       wrong=["Vì SQLite bắt buộc mọi bảng phải có khoá chính gồm 3 cột",
              "Vì MaNguoiThue và MaCanHo có thể trùng giá trị với nhau",
              "Chỉ để tăng tốc độ truy vấn, không liên quan tới tính duy nhất của dòng"]),
  dict(q="Trong ví dụ Module 00, cột nào của bảng 'thue' là khoá ngoại trỏ tới bảng 'canho'?",
       correct="MaCanHo", topic="Ví dụ nguoithue-canho-thue",
       wrong=["MaNguoiThue", "NgayBatDau", "GiaThueThucTe"]),
  dict(q="Vì sao KHÔNG nên thêm trực tiếp cột 'HoTen' vào bảng 'thue' (dù sẽ giúp truy vấn đỡ phải JOIN)?",
       correct="Vì HoTen sẽ bị lặp lại ở mọi hợp đồng của cùng 1 người — gây dư thừa dữ liệu và dị thường cập nhật nếu người đó đổi tên",
       topic="Ví dụ nguoithue-canho-thue",
       wrong=["Vì SQL không cho phép 1 bảng có cột kiểu TEXT",
              "Vì HoTen phải luôn là khoá chính của bảng chứa nó",
              "Vì JOIN luôn chạy nhanh hơn so với không JOIN, nên không có lý do gì để thêm cột"]),
  dict(q="Cột GiaThueNiemYet (ở bảng canho) và GiaThueThucTe (ở bảng thue) khác nhau ở điểm gì, theo đúng thiết kế ví dụ Module 00?",
       correct="GiaThueNiemYet là giá rao ban đầu của căn hộ (thuộc tính của thực thể CanHo); GiaThueThucTe là giá đã thương lượng cho 1 hợp đồng cụ thể (thuộc tính của liên kết Thue)",
       topic="Ví dụ nguoithue-canho-thue",
       wrong=["2 cột này thực chất là 1, chỉ đặt tên khác nhau cho dễ nhớ",
              "GiaThueThucTe luôn phải lớn hơn GiaThueNiemYet",
              "GiaThueNiemYet chỉ tồn tại ở bảng thue, không tồn tại ở bảng canho"]),
]

CLOZE_QS = [
  dict(q="Mỗi thực thể trong ER, khi chuyển sang lược đồ quan hệ, thành 1 bảng với 1 ___ định danh duy nhất mỗi dòng.",
       correct="khoá chính (primary key)", topic="ER Model",
       wrong=["khoá ngoại (foreign key)", "chỉ mục phụ (secondary index)", "ràng buộc CHECK"]),
  dict(q="Một liên kết (relationship) được hiện thực bằng ___ — cột ở bảng này trỏ tới khoá chính bảng kia.",
       correct="khoá ngoại (foreign key)", topic="ER Model",
       wrong=["khoá chính (primary key)", "view ảo (virtual view)", "trigger"]),
  dict(q="Toàn bộ kỹ thuật Record Linkage thực chất là đi tìm lại '___' giữa 2 nguồn không hề chia sẻ cùng 1 khoá ngoại thật.",
       correct="khoá chính ngầm", topic="Cầu nối sang Data Integration",
       wrong=["mật khẩu quản trị", "chỉ mục B-tree", "view vật lý"]),
  dict(q="Chuẩn hoá (1NF → 2NF → 3NF...) nhằm giảm ___ dữ liệu và dị thường cập nhật.",
       correct="dư thừa (redundancy)", topic="Chuẩn hoá",
       wrong=["tốc độ truy vấn", "kích thước font chữ hiển thị", "số lượng người dùng truy cập"]),
  dict(q="'Chuẩn hoá đúng kỹ thuật ở từng nguồn' không có nghĩa là '___' giữa các nguồn.",
       correct="dễ tích hợp", topic="Chuẩn hoá",
       wrong=["sẽ chạy chậm hơn", "không cần khoá chính", "sẽ tự động có cùng tên cột"]),
]

def main():
    b = BankBuilder(SEED)
    for f in FACTS:
        b.add(f"'{f['term']}' được định nghĩa như thế nào?", f["definition"], f["wrong"], f["topic"], f["src"], f"m00-t1-{f['id']}")
    all_terms = [f["term"] for f in FACTS]
    import random
    for f in FACTS:
        others = [t for t in all_terms if t != f["term"]]
        distract = random.Random(SEED + hash(f["id"])).sample(others, 3)
        b.add(f"Định nghĩa sau mô tả đúng khái niệm nào? — \"{f['definition']}\"", f["term"], distract, f["topic"], f["src"], f"m00-t2-{f['id']}")
    for f in FACTS:
        b.add(f"Phát biểu nào sau đây về {f['term']} là ĐÚNG?", f["definition"], f["wrong"], f["topic"], f["src"], f"m00-t3-{f['id']}")
    for i, c in enumerate(CLOZE_QS):
        b.add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m00-t5-{i:02d}")
    for i, c in enumerate(COMPARE_QS):
        b.add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m00-t4-{i:02d}")
    for i, c in enumerate(SCHEMA_QS):
        b.add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m00-t6-{i:02d}")
    b.write(OUT)
    audit(b.items, "Module 00")

if __name__ == "__main__":
    main()
