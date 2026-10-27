# -*- coding: utf-8 -*-
"""Sinh ngân hàng trắc nghiệm Module 01 (Data Integration overview)."""
import pathlib, random, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from facts_m01 import FACTS
from bank_common import BankBuilder, audit

SEED = 20260212
OUT = HERE.parent.parent / "data" / "bank" / "bank_m01.json"

COMPARE_QS = [
  dict(q="Virtual Integration và Data Warehousing khác nhau cơ bản ở điểm nào?",
       correct="Virtual: dữ liệu ở nguyên nguồn, truy cập query-time qua wrapper; Warehousing: copy định kỳ về kho tập trung (ETL)",
       topic="Kiến trúc",
       wrong=["2 kiến trúc này hoàn toàn giống nhau, chỉ khác tên gọi",
              "Virtual Integration luôn chạy chậm hơn Data Warehousing trong mọi trường hợp",
              "Data Warehousing không cần ETL, chỉ Virtual Integration mới cần"]),
  dict(q="Vì sao Data Warehousing cho phép chạy data mining/ML dễ hơn Virtual Integration?",
       correct="Vì dữ liệu đã copy về kho, có thể chạy tính toán nặng tuỳ ý trên bản copy mà không làm phiền nguồn gốc",
       topic="Kiến trúc",
       wrong=["Vì Data Warehousing luôn có phần cứng mạnh hơn Virtual Integration",
              "Vì Virtual Integration không hỗ trợ bất kỳ loại truy vấn nào",
              "Vì ML chỉ chạy được trên dữ liệu đã ETL, không chạy được trên dữ liệu thô"]),
  dict(q="DBMS và Data Integration khác nhau ở tầng trừu tượng nào?",
       correct="DBMS = trừu tượng logical vs physical (trong 1 CSDL); Data Integration = trừu tượng bậc cao hơn, che giấu sự khác biệt GIỮA NHIỀU nguồn độc lập",
       topic="Khái niệm nền",
       wrong=["2 khái niệm này hoàn toàn giống nhau, Data Integration chỉ là tên gọi khác của DBMS",
              "DBMS luôn ở tầng cao hơn Data Integration (bị đảo ngược)",
              "Data Integration chỉ hoạt động được khi không có DBMS nào cả"]),
  dict(q="Structural Heterogeneity và Semantic Heterogeneity khác nhau ở điểm nào?",
       correct="Structural: khác cách TỔ CHỨC bảng/khoá/độ chi tiết; Semantic: khác Ý NGHĨA thuật ngữ (đồng nghĩa/đa nghĩa)",
       topic="Heterogeneity",
       wrong=["2 loại dị biệt này hoàn toàn giống nhau, chỉ khác tên gọi",
              "Semantic Heterogeneity chỉ xảy ra ở cấp độ vật lý (ổ đĩa), không liên quan ngữ nghĩa",
              "Structural Heterogeneity chỉ giải quyết được bằng Entity Resolution"]),
  dict(q="Instance/Identity Heterogeneity khác với 6 mức dị biệt còn lại ở điểm nào, và giải quyết bằng kỹ thuật học ở buổi nào?",
       correct="Nó xảy ra ở mức DỮ LIỆU THỰC THỂ (không phải schema) — giải quyết bằng Entity Resolution/Record Linkage, học ở buổi 4",
       topic="Heterogeneity",
       wrong=["Nó giống hoàn toàn Structural Heterogeneity, học ở buổi 3",
              "Nó chỉ là vấn đề định dạng file, giải quyết bằng đổi tên cột",
              "Nó không cần giải quyết, có thể bỏ qua an toàn"]),
]

# Chuyển 13 câu trắc nghiệm ĐƠN-CHỌN (không phải "chọn nhiều") từ Quiz DI.pdf (Phần A: khái niệm
# nền/heterogeneity; Phần D: kiến trúc/wrapper) thành câu bank — giữ đúng 4 phương án gốc của đề,
# đáp án theo suy luận của tôi đối chiếu lý thuyết đã học (đề gốc KHÔNG có đáp án chính thức giảng
# viên cho phần Quiz DI này — xem slides/Quiz-DI-DataIntegration-GAV-LAV-GLAV.md). 4 câu "chọn nhiều"
# của Phần A/D (câu 1, 21, 26) KHÔNG đưa vào đây vì bank này chỉ hỗ trợ chọn 1 đáp án (radio).
QUIZ_DI_CONVERTED = [
  dict(q="(Quiz DI, câu 2) Điều nào sau đây KHÔNG phải là vấn đề chính trong tích hợp dữ liệu?",
       correct="Trực quan hóa dữ liệu tự động", topic="Khái niệm nền",
       wrong=["Đồng nhất lược đồ", "Xử lý truy vấn phân tán", "Vấn đề về bảo mật và quyền riêng tư"]),
  dict(q="(Quiz DI, câu 4) Trường hợp nào sau đây là ví dụ về sự không đồng nhất ngữ nghĩa (semantic heterogeneity) giữa hai nguồn dữ liệu?",
       correct="Sử dụng 2 giá trị khác nhau để biểu diễn cùng 1 trạng thái của cùng 1 đối tượng (VD mã giới tính 'M/F' vs '1/2')",
       topic="Heterogeneity",
       wrong=["Sử dụng tên bảng và thuộc tính khác nhau để biểu diễn cùng một đối tượng (đây là Structural/Schema heterogeneity)",
              "Có lược đồ giống nhau nhưng dữ liệu khác nhau", "Hai nguồn chứa cùng dữ liệu và cùng lược đồ"]),
  dict(q="(Quiz DI, câu 22) Trong kiến trúc kho dữ liệu (data warehouse), dữ liệu được tích hợp bằng cách nào?",
       correct="Đưa dữ liệu vào một kho dữ liệu vật lý chung (ETL)", topic="Kiến trúc",
       wrong=["Chỉ dùng dữ liệu XML", "Biểu diễn bởi cùng 1 lược đồ (chưa đủ, bản chất là vật lý hoá)", "Không cần ánh xạ dữ liệu"]),
  dict(q="(Quiz DI, câu 23) Kiến trúc tích hợp dữ liệu ảo (virtual data integration) hoạt động như thế nào?",
       correct="Để dữ liệu tại nguồn và truy cập qua wrapper tại thời điểm có truy vấn (query-time)", topic="Kiến trúc",
       wrong=["Luôn sao chép toàn bộ dữ liệu về một nơi (đây là data warehouse)", "Không sử dụng truy vấn", "Chỉ hoạt động với một nguồn dữ liệu duy nhất"]),
  dict(q="(Quiz DI, câu 24) Điểm chung của kho dữ liệu (warehouse) và tích hợp ảo dữ liệu (virtual) là gì?",
       correct="Cả hai đều có thể gặp vấn đề tính không đồng nhất ngữ nghĩa giữa các nguồn",
       topic="Kiến trúc",
       wrong=["Cả hai đều không cần lược đồ", "Cả hai đều không cần nguồn dữ liệu",
              "Chỉ virtual integration mới gặp vấn đề dị biệt ngữ nghĩa, warehouse thì không"]),
  dict(q="(Quiz DI, câu 15) Mediated Query (câu truy vấn trung gian) là gì?",
       correct="Câu truy vấn biểu diễn ánh xạ giữa lược đồ tích hợp (mediated schema) và lược đồ nguồn",
       topic="Kiến trúc",
       wrong=["Câu truy vấn của người dùng hệ tích hợp", "Câu truy vấn chạy trực tiếp trên các nguồn dữ liệu", "Câu truy vấn phân tán trên các nguồn"]),
  dict(q="(Quiz DI, câu 17) Trong kiến trúc tích hợp dữ liệu, lược đồ tích hợp (mediated schema) có vai trò gì?",
       correct="Là giao diện/lược đồ chung để người dùng truy vấn nhiều nguồn dữ liệu khác nhau",
       topic="Khái niệm nền",
       wrong=["Là nơi lưu duy nhất toàn bộ dữ liệu vật lý (đây là warehouse)", "Là ánh xạ giữa các nguồn dữ liệu (ánh xạ là thứ KẾT NỐI mediated schema với nguồn, không phải chính nó)", "Là khóa chính của tất cả bảng"]),
  dict(q="(Quiz DI, câu 18) Ánh xạ ngữ nghĩa giữa các lược đồ (Semantic mappings) dùng để làm gì?",
       correct="Mô tả quan hệ ngữ nghĩa giữa lược đồ chung (mediated schema) và các nguồn dữ liệu",
       topic="Kiến trúc",
       wrong=["Nén dữ liệu", "Xóa các bảng trùng nhau", "Tạo định dạng chung biểu diễn yêu cầu truy vấn"]),
  dict(q="(Quiz DI, câu 20) Mục tiêu của tích hợp dữ liệu là cung cấp gì?",
       correct="Một truy vấn thống nhất đến nhiều nguồn dữ liệu khác nhau", topic="Khái niệm nền",
       wrong=["Một hệ thống phần mềm mới", "Một ngôn ngữ lập trình mới", "Một tổ chức lưu trữ mới"]),
  dict(q="(Quiz DI, câu 25) Bộ trích lọc/trình bao bọc (Wrapper/Extractor) trong kiến trúc tích hợp dữ liệu có nhiệm vụ gì?",
       correct="Gửi truy vấn đến nguồn dữ liệu và chuyển kết quả về mô hình dữ liệu chung",
       topic="Khái niệm nền",
       wrong=["Thay thế cho nguồn dữ liệu", "Xóa dữ liệu lỗi", "Chỉ biểu diễn dữ liệu đã trích chọn bằng ngôn ngữ chung (thiếu phần GỬI truy vấn xuống nguồn)"]),
  dict(q="(Quiz DI, câu 16) Mục tiêu chính của tích hợp dữ liệu là gì?",
       correct="Kết nối nhiều nguồn dữ liệu khác nhau dưới một lược đồ chung", topic="Khái niệm nền",
       wrong=["Xóa bỏ tất cả các cơ sở dữ liệu cũ", "Tăng khả năng xử lý truy vấn", "Chuyển toàn bộ dữ liệu sang định dạng văn bản"]),
  dict(q="(Quiz DI, câu 3) Trong tích hợp dữ liệu, 'lược đồ trung gian' (mediated schema) đề cập đến gì?",
       correct="Một lược đồ tiêu chuẩn ánh xạ đến nhiều lược đồ nguồn khác nhau", topic="Khái niệm nền",
       wrong=["Lược đồ của nguồn dữ liệu lớn nhất", "Bản sao lưu của tất cả các cơ sở dữ liệu vật lý", "Bản sao của kho dữ liệu mới nhất"]),
  dict(q="(Quiz DI, câu 19) Tính không đồng nhất về lược đồ (Schema heterogeneity) thể hiện điều gì?",
       correct="Các nguồn dữ liệu khác nhau về lược đồ (tên bảng/thuộc tính/cấu trúc)", topic="Heterogeneity",
       wrong=["Các hệ thống có thể cùng tên bảng và cùng thuộc tính (đây là trường hợp KHÔNG có dị biệt)",
              "Giá trị dữ liệu trong các nguồn khác nhau có thể biểu diễn theo các cách khác nhau (đây là Instance/Semantic heterogeneity)",
              "Các nguồn sử dụng các công cụ lưu trữ khác nhau (đây là System/Platform heterogeneity)"]),
]

def main():
    b = BankBuilder(SEED)
    for f in FACTS:
        b.add(f"'{f['term']}' được định nghĩa như thế nào (theo đúng nội dung slide buổi 2)?", f["definition"], f["wrong"], f["topic"], f["src"], f"m01-t1-{f['id']}")
    all_terms = [f["term"] for f in FACTS]
    for f in FACTS:
        others = [t for t in all_terms if t != f["term"]]
        distract = random.Random(SEED + hash(f["id"])).sample(others, 3)
        b.add(f"Định nghĩa sau mô tả đúng khái niệm nào? — \"{f['definition']}\"", f["term"], distract, f["topic"], f["src"], f"m01-t2-{f['id']}")
    for f in FACTS:
        b.add(f"Phát biểu nào sau đây về {f['term']} là ĐÚNG?", f["definition"], f["wrong"], f["topic"], f["src"], f"m01-t3-{f['id']}")
    for i, c in enumerate(COMPARE_QS):
        b.add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m01-t4-{i:02d}")
    for i, c in enumerate(QUIZ_DI_CONVERTED):
        b.add(c["q"], c["correct"], c["wrong"], c["topic"], "Quiz DI.pdf (tự suy luận, chưa có đáp án chính thức giảng viên, chuyển thành trắc nghiệm)", f"m01-t9-{i:02d}")
    b.write(OUT)
    audit(b.items, "Module 01")

if __name__ == "__main__":
    main()
