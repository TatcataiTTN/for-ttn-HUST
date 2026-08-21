#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ngan hang 200 cau hoi on tap cho mon "Cac cong nghe truyen thong cho IoT"
(HUST, 20251196M). Noi dung duoc chuyen the tu vat ly/thuat toan da kiem chung
cua du an ve tinh FSO SIKD (Tu hoc/SIKD_Satellite_QKD/Study_Materials/
SIKD_Formula_Guide_v3_Expanded.tex), tong quat hoa cho cac khai niem truyen
thong ve tinh phu hop mon hoc (khong nhac ten file/thu muc ma nguon cu the,
theo yeu cau).

Ky luat xay dung: dap an dung duoc dat DAU TIEN trong danh sach lua chon, sau
do xao tron xac dinh (seed = ma cau hoi) va danh lai nhan A-D -- giong co che
da dung o trang for-ttn-USTH/Thesis-M1 -- de khong ton tai mot "dap an go tay"
tach roi khoi noi dung lua chon.
"""
import json
import random
import sys

OUT = "/Users/tuannghiat/for-ttn-HUST/Communication-tech-for-IoT/data/questions.json"

PERSPECTIVES = []


def P(num, title):
    PERSPECTIVES.append({"num": num, "title": title, "items": []})
    return PERSPECTIVES[-1]


def Q(persp, group, question, options, framework):
    assert len(options) == 4, question
    persp["items"].append({"group": group, "question": question, "options": options, "framework": framework})


# ============================================================================
# P0 -- Khai niem nen: an toan luong tu, ghep kenh khoa/du lieu, kien truc pipeline
# ============================================================================
p0 = P(0, "Khai niệm nền tảng: bảo mật lượng tử & kiến trúc kênh vũ trụ")

g = "An toàn thông tin lượng tử"
Q(p0, g,
  "\"Bảo mật theo lý thuyết thông tin\" (information-theoretic security) của phân phối khóa lượng tử (QKD) nghĩa là gì?",
  ["Tính bí mật của khóa suy ra từ định luật vật lý (không nhân bản được trạng thái lượng tử, đo là làm nhiễu loạn), không phụ thuộc năng lực tính toán của kẻ nghe lén",
   "Khóa được mã hóa bằng AES-256 trước khi truyền",
   "Khóa chỉ an toàn trước kẻ tấn công có máy tính cổ điển",
   "Khóa khó bị tính ra bởi máy tính hiện tại, nhưng sẽ yếu đi khi có máy tính lượng tử"],
  "QKD dựa trên định luật vật lý (no-cloning, đo là làm nhiễu), không phải độ khó tính toán -- nên an toàn cả trước máy tính lượng tử, khác RSA/ECC.")

Q(p0, g,
  "Chỉ số sức khỏe chính của một phiên QKD là gì, và vì sao?",
  ["QBER (tỷ lệ lỗi bit lượng tử): kẻ nghe lén làm nhiễu loạn trạng thái lượng tử nên làm tăng QBER, từ đó bị phát hiện",
   "Công suất phát quang, vì phát mạnh hơn luôn an toàn hơn",
   "Số lượng vệ tinh nhìn thấy trạm mặt đất cùng lúc",
   "Tần số sóng mang phụ dùng cho kênh dữ liệu cổ điển"],
  "Độ làm nhiễu do QKD gây ra biểu hiện trực tiếp qua QBER tăng -- đây là cơ chế phát hiện nghe lén nổi tiếng của BB84/BBM92.")

Q(p0, g,
  "Nếu QBER đo được vượt qua ngưỡng BB84 (~11%), điều gì xảy ra với tốc độ khóa bí mật (SKR)?",
  ["SKR về 0 -- không thể chưng cất được khóa bí mật từ dữ liệu đã sifted, dù vẫn còn bit đã trao đổi",
   "SKR không đổi vì QBER chỉ ảnh hưởng tốc độ, không ảnh hưởng bảo mật",
   "SKR tăng vì nhiều bit hơn được giữ lại",
   "Chỉ kênh dữ liệu cổ điển bị ảnh hưởng, kênh khóa vẫn hoạt động bình thường"],
  "Trên ngưỡng QBER, phần thông tin rò rỉ cho kẻ nghe lén (qua reconciliation công khai) vượt qua thông tin hợp lệ còn lại -- SKR âm về mặt toán học nên quy ước bằng 0.")

g = "SIKD: ghép đồng thời khóa và dữ liệu"
Q(p0, g,
  "Trong một hệ thống ghép đồng thời thông tin và khóa (SIKD) trên một chùm tia quang duy nhất, hai kênh (khóa và dữ liệu) được tách biệt bằng kỹ thuật nào?",
  ["Ghép kênh sóng mang phụ (subcarrier multiplexing/SCM): mỗi kênh điều chế một tần số sóng mang phụ riêng trên cùng một sóng mang quang",
   "Ghép kênh phân chia thời gian (TDM) đơn thuần giữa hai khe thời gian riêng biệt",
   "Dùng hai bước sóng laser khác nhau hoàn toàn (WDM cổ điển)",
   "Dùng hai anten thu vật lý tách rời cho từng kênh"],
  "SCM cho phép cả hai kênh chia sẻ chung một chùm tia và một photodetector, nhưng đây chính là nguồn gốc của nhiễu xuyên kênh (crosstalk) giữa chúng.")

Q(p0, g,
  "Vì sao điều chế của kênh dữ liệu cổ điển lại trở thành một nguồn nhiễu đối với kênh khóa lượng tử trong kiến trúc SIKD?",
  ["Vì cả hai kênh cùng đi qua MỘT photodetector chung, nên tín hiệu điều chế của kênh dữ liệu rò sang thành nhiễu xuyên âm (crosstalk) khi máy thu khóa tách sóng",
   "Vì kênh dữ liệu dùng bước sóng khác nên bị tán sắc trong sợi quang",
   "Vì kênh khóa luôn phát trước kênh dữ liệu vài micro-giây",
   "Vì cả hai kênh dùng chung một nguồn đồng hồ nhưng lệch pha"],
  "Tách kênh xảy ra SAU tách sóng quang (bộ lọc RF), không phải trước -- nên biên độ điều chế của kênh kia luôn còn lại trong dòng quang điện chung, tạo crosstalk.")

Q(p0, g,
  "Căng thẳng thiết kế trung tâm của một hệ thống SIKD là gì?",
  ["Tăng độ sâu điều chế kênh dữ liệu để tăng thông lượng lại làm tăng nhiễu xuyên âm lên kênh khóa (tỷ lệ bình phương), nên hai kênh KHÔNG độc lập về hiệu năng",
   "Tăng công suất phát luôn cải thiện cả hai kênh mà không đánh đổi gì",
   "Kênh khóa và kênh dữ liệu hoàn toàn độc lập vì dùng tần số khác nhau",
   "Vấn đề duy nhất là băng thông máy thu, không liên quan đến điều chế"],
  "Nhiễu xuyên âm tỷ lệ với bình phương độ sâu điều chế dữ liệu, trong khi tín hiệu khóa chỉ tỷ lệ bậc 1 -- đây là lý do power-split là một bài toán tối ưu thật, không phải hai liên kết độc lập.")

g = "Kiến trúc pipeline mô hình hóa"
Q(p0, g,
  "Trong một pipeline mô phỏng hiệu năng liên kết vệ tinh quang điện hoàn chỉnh, thứ tự hợp lý của các bước tính toán là gì?",
  ["Quỹ đạo/hình học (góc ngưỡng, slant range) -> mô hình kênh (suy hao hình học, khí quyển, nhiễu loạn) -> thời tiết thực -> hiệu năng máy thu (QBER/SKR/thông lượng)",
   "Hiệu năng máy thu trước, rồi mới tính hình học quỹ đạo sau",
   "Thời tiết là bước đầu tiên, không liên quan gì đến hình học quỹ đạo",
   "Tất cả các bước độc lập, thứ tự không quan trọng"],
  "Slant range/góc ngưỡng là đầu vào cho suy hao hình học và độ dài đường truyền khí quyển; thời tiết điều chỉnh hệ số khí quyển; tất cả gộp lại mới ra được nhiễu/tín hiệu cho tầng hiệu năng máy thu.")

Q(p0, g,
  "Nhánh 'hình học vùng phủ và lập lịch' trong kiến trúc mô phỏng kết nối với nhánh 'kênh vật lý' ở điểm nào?",
  ["Cả hai đều xuất phát từ cùng dữ liệu quỹ đạo (elevation, slant range theo thời gian) -- hình học quyết định KHI NÀO có liên kết khả thi, kênh vật lý quyết định CHẤT LƯỢNG liên kết đó",
   "Hai nhánh hoàn toàn tách biệt, không dùng chung dữ liệu nào",
   "Nhánh lập lịch chỉ dùng dữ liệu thời tiết, không cần quỹ đạo",
   "Nhánh kênh vật lý chỉ áp dụng cho trạm mặt đất cố định, không áp dụng cho vệ tinh chuyển động"],
  "Cả giá trị trọng số cho bài toán ghép cặp (SKR hiệu dụng) lẫn tính khả thi cặp trạm (DUAL/SF) đều bắt nguồn từ cùng một chuỗi vị trí quỹ đạo theo thời gian.")

Q(p0, g,
  "Vì sao một dự án mô phỏng nghiêm túc cần tách riêng 'mô hình kênh vật lý' (channel) và 'mô hình hiệu năng máy thu' (performance) thành hai lớp khác nhau?",
  ["Để có thể thay đổi giả định máy thu (ví dụ ngưỡng quyết định, cấu trúc nhiễu) mà không phải viết lại vật lý lan truyền sóng, giúp kiểm tra lỗi riêng từng lớp",
   "Vì hai lớp này không bao giờ dùng chung tham số nào",
   "Chỉ để code chạy nhanh hơn, không liên quan đến tính đúng",
   "Vì quy định của ITU yêu cầu tách lớp như vậy"],
  "Phân lớp giúp kiểm tra vật lý (h_g, h_l, sigma_R^2) độc lập với giả định máy thu (ngưỡng kép, Gauss-Hermite) -- đây là lý do các lỗi vật lý và lỗi máy thu được phát hiện/sửa riêng biệt trong quá trình review dự án này.")

Q(p0, g,
  "Trong quá trình phát triển một mô hình liên kết quang phức tạp (nhiều hệ số, nhiều bước tích phân), điều gì là dấu hiệu cảnh báo cần 'kiểm tra vật lý bậc độ lớn' trước khi tin kết quả?",
  ["Một đại lượng trung gian (ví dụ phương sai nhiễu loạn) ra giá trị lớn bất thường vài bậc độ lớn so với kỳ vọng vật lý, dấu hiệu rõ ràng của lỗi số mũ/hệ số",
   "Kết quả cuối cùng khớp với một bài báo tham khảo, nên không cần kiểm tra thêm",
   "Chương trình chạy không báo lỗi cú pháp, nên kết quả chắc chắn đúng",
   "Giá trị luôn nằm trong khoảng [0,1] nên không cần kiểm tra thêm"],
  "Một lỗi thực tế trong dự án này: dùng nhầm số mũ 1 thay vì 10 trong một hàm mũ làm sai lệch kết quả tới 10 bậc độ lớn, chỉ phát hiện được qua kiểm tra 'liệu con số này có hợp lý vật lý không' trước khi tin dùng.")

Q(p0, g,
  "Khi một dự án công bố bảng số 'trước' và 'sau' sửa lỗi công thức, tại sao việc ghi lại LÝ DO sửa (không chỉ con số mới) lại quan trọng?",
  ["Để người đọc/hội đồng đánh giá có thể tự kiểm chứng logic sửa lỗi, phân biệt lỗi tính toán thực sự với thay đổi giả định thiết kế, và tránh lặp lại lỗi tương tự trong tương lai",
   "Vì quy định trình bày bắt buộc phải có bảng số liệu",
   "Để tạo ấn tượng với người đọc rằng dự án rất kỹ lưỡng",
   "Lý do không quan trọng, chỉ cần con số cuối cùng đúng là đủ"],
  "Một bảng đối chiếu 'trước/sau kèm lý do' (ví dụ fix hệ số Rytov 0.56->2.25, fix crosstalk /2->/8) là công cụ minh bạch hóa khoa học, cho phép người khác kiểm tra độc lập từng bước suy luận.")

g = "Tín hiệu quang mang thông tin cổ điển và lượng tử"
Q(p0, g,
  "Vì sao một hệ thống ghép khóa lượng tử và dữ liệu cổ điển trên vệ tinh phải dùng ĐÚNG MỘT đường truyền quang vật lý (thay vì hai đường tách biệt hoàn toàn, ví dụ hai laser/hai kính viễn vọng riêng)?",
  ["Vì mỗi kính viễn vọng/hệ thống trỏ hướng chính xác trên vệ tinh có chi phí SWaP (khối lượng, năng lượng, không gian) rất lớn -- dùng chung một đường truyền vật lý cho cả hai kênh tiết kiệm đáng kể tài nguyên vệ tinh, đổi lại phải chấp nhận crosstalk giữa hai kênh",
   "Vì luật viễn thông quốc tế cấm dùng hai kính viễn vọng riêng biệt trên cùng một vệ tinh",
   "Vì tín hiệu lượng tử không thể tồn tại độc lập với tín hiệu cổ điển trong bất kỳ trường hợp nào",
   "Không có lý do kỹ thuật, đây chỉ là lựa chọn ngẫu nhiên của nhóm thiết kế"],
  "Đây là động lực thiết kế cốt lõi của kiến trúc SIKD: chia sẻ hạ tầng quang đắt đỏ (kính viễn vọng, hệ trỏ hướng) giữa hai kênh, chấp nhận đánh đổi kỹ thuật (crosstalk) để tiết kiệm tài nguyên vệ tinh khan hiếm.")

Q(p0, g,
  "Trong một hệ thống QKD dựa trên vệ tinh, tại sao kênh khóa lượng tử thường chỉ chiếm một PHẦN NHỎ công suất/băng thông so với kênh dữ liệu cổ điển trên cùng liên kết, thay vì chia đều 50/50?",
  ["Vì mục đích của kênh khóa không phải là truyền TẢI LƯỢNG dữ liệu lớn mà là phân phối một lượng khóa bí mật vừa đủ để mã hóa dữ liệu (dùng thuật toán mã hóa đối xứng tốc độ cao ở lớp ứng dụng) -- nhu cầu về TỐC ĐỘ khóa thấp hơn nhiều so với tốc độ dữ liệu thô cần truyền",
   "Kênh khóa luôn cần công suất lớn hơn kênh dữ liệu vì độ nhạy vật lý",
   "Không có lý do kỹ thuật, tỷ lệ 50/50 luôn tối ưu trong mọi hệ thống QKD",
   "Kênh dữ liệu và kênh khóa luôn có công suất bằng nhau theo định nghĩa"],
  "Đây là lý do thực tế đằng sau việc chọn m_K << m_D trong thiết kế: một khóa vài chục/hàng trăm Mbps đã đủ để mã hóa (one-time-pad hoặc AES với rekey thường xuyên) một luồng dữ liệu tốc độ cao hơn nhiều, nên không cần 'chia đều' tài nguyên điều chế.")

Q(p0, g,
  "Nếu một vệ tinh QKD chỉ có MỘT lần bay qua (pass) rất ngắn (ví dụ dưới 5 phút) trên một trạm mặt đất mỗi ngày, điều này đặt ra yêu cầu gì cho tốc độ SKR (Mbps) so với một hệ thống có kết nối liên tục 24/7?",
  ["Cần SKR CAO trong khoảng thời gian ngắn ngủi của pass để tích lũy đủ lượng khóa cần thiết cho cả ngày -- đây là lý do các con số SKR hàng chục Mbps (thay vì Kbps) có ý nghĩa thực tế quan trọng cho ứng dụng vệ tinh, khác với các hệ thống QKD mặt đất có thể duy trì kết nối liên tục với SKR thấp hơn nhưng bù bằng thời gian",
   "Tốc độ SKR không quan trọng nếu pass ngắn, chỉ cần pass xảy ra là đủ",
   "SKR càng thấp càng tốt để tránh quá tải hệ thống trong thời gian ngắn",
   "Thời lượng pass không có bất kỳ liên hệ nào với yêu cầu SKR"],
  "Đây là lý do kiến trúc vệ tinh QKD khác biệt căn bản so với QKD sợi quang mặt đất: ràng buộc THỜI GIAN CỬA SỔ (pass ngắn, không liên tục) đòi hỏi tối ưu hóa để đạt SKR cao trong khoảng thời gian hạn hẹp, thúc đẩy các cải tiến như tăng m_K, tối ưu khẩu độ, và chọn đúng elevation.")

# ============================================================================
# P1 -- Kenh vat ly FSO: hinh hoc chum tia, khi quyen, nhieu loan
# ============================================================================
p1 = P(1, "Kênh vật lý quang (FSO): chùm tia, khí quyển, nhiễu loạn")

g = "Bán kính chùm tia Gaussian"
Q(p1, g,
  "Công thức bán kính thắt chùm (beam waist) w0 = lambda / (2*theta_C) cho biết điều gì?",
  ["Bán kính nhỏ nhất của chùm tia laser ngay tại điểm phát, tỷ lệ thuận với bước sóng và tỷ lệ nghịch với góc phân kỳ theta_C",
   "Bán kính chùm tia tại máy thu, không phụ thuộc khoảng cách",
   "Đường kính khẩu độ thu của kính viễn vọng mặt đất",
   "Công suất trung bình của chùm tia laser"],
  "w0 là kích thước 'thắt' của chùm ngay tại nguồn phát; chùm hẹp hơn (theta_C nhỏ) cần công nghệ trỏ hướng chính xác hơn (PAT) nhưng tập trung năng lượng tốt hơn.")

Q(p1, g,
  "Khi khoảng cách lan truyền L rất lớn (far-field, L*lambda/(pi*w0^2) >> 1), bán kính chùm tia tại máy thu w_L quan hệ với L như thế nào?",
  ["w_L tăng gần như TUYẾN TÍNH theo L (w_L ~ L*lambda/(pi*w0))",
   "w_L không đổi theo L sau khi vượt far-field",
   "w_L giảm dần theo L do hội tụ tự nhiên",
   "w_L tỷ lệ với căn bậc hai của L"],
  "Ở far-field, chùm tia đã phân kỳ hết cỡ 'thắt' ban đầu và lan rộng gần tuyến tính -- đây là lý do đốm sáng trên mặt đất có đường kính vài mét dù chùm chỉ vài cm ở nguồn.")

Q(p1, g,
  "Vì sao hệ số suy hao hình học h_g của một liên kết quang không gian-mặt đất có giá trị rất nhỏ (cỡ 10^-4, tức khoảng -34 đến -39 dB) dù chưa tính suy hao khí quyển?",
  ["Vì bán kính chùm tia tại máy thu w_L (cỡ vài mét) lớn hơn khẩu độ thu a_R (vài cm) hàng trăm lần, nên chỉ một phần rất nhỏ năng lượng 'đốm sáng' rơi vào được khẩu độ thu",
   "Vì khí quyển đã hấp thụ gần hết năng lượng trước khi h_g được tính",
   "Vì máy thu luôn đặt sai vị trí so với tâm chùm tia",
   "Vì bước sóng 1550nm bị Trái Đất che khuất một phần"],
  "Đây là bản chất giới hạn nhiễu xạ (diffraction-limited) của liên kết FSO ở khoảng cách quỹ đạo thấp: diện tích thu chỉ bắt được tỷ lệ (a_R/w_L)^2 ~ 10^-4 năng lượng chùm.")

Q(p1, g,
  "Theo hệ số hình học h_g = [erf(nu_R)]^2 với nu_R = căn(pi/2)*a_R/w_L, khi khẩu độ thu a_R tăng gấp đôi (giữ nguyên w_L), h_g thay đổi thế nào (ở chế độ nu_R nhỏ)?",
  ["Tăng khoảng 4 lần (~+6 dB), vì h_g tỷ lệ xấp xỉ với a_R^2 khi nu_R << 1",
   "Tăng gấp đôi (+3dB) vì h_g tỷ lệ tuyến tính với a_R",
   "Không đổi vì h_g chỉ phụ thuộc w_L",
   "Giảm đi vì khẩu độ lớn hơn thu cả nhiễu nền"],
  "Với nu_R nhỏ, erf(nu_R) ~ (2/căn(pi))*nu_R nên h_g tỷ lệ với nu_R^2 tỷ lệ với a_R^2 -- gấp đôi khẩu độ thu là một đòn bẩy thiết kế mạnh nhưng đắt về SWaP (kích thước/khối lượng/năng lượng).")

Q(p1, g,
  "Slant range (khoảng cách nghiêng) giữa trạm mặt đất và vệ tinh quỹ đạo thấp thay đổi như thế nào khi góc ngưỡng (elevation) giảm từ 90 độ xuống gần 0 độ?",
  ["Tăng dần một cách đáng kể: từ bằng độ cao vệ tinh (elevation 90 độ, vệ tinh đỉnh đầu) lên đến gấp vài lần độ cao khi elevation thấp (gần chân trời)",
   "Không đổi, vì slant range chỉ phụ thuộc độ cao quỹ đạo",
   "Giảm dần khi elevation giảm",
   "Chỉ thay đổi nếu vệ tinh ở quỹ đạo địa tĩnh, không áp dụng cho quỹ đạo thấp"],
  "Ví dụ thực: ở độ cao vệ tinh 550km, slant range là 550km lúc elevation 90 độ nhưng tăng lên gần 1000km lúc elevation 30 độ -- làm h_g và suy hao khí quyển đều xấu đi rõ rệt khi vệ tinh ở gần chân trời.")

Q(p1, g,
  "Vì sao dùng công thức hình học CẦU (spherical) cho slant range chính xác hơn xấp xỉ PHẲNG (flat, L=H/cos(zenith)) ở góc nghiêng lớn?",
  ["Vì hình học phẳng bỏ qua độ cong của Trái Đất, gây sai số đáng kể (có thể >10%) khi góc thiên đỉnh lớn (elevation nhỏ), do vị trí trạm mặt đất không còn là 'điểm dưới vệ tinh' theo nghĩa phẳng",
   "Vì hình học cầu luôn cho kết quả nhỏ hơn hình học phẳng ở mọi góc",
   "Hai công thức luôn cho cùng kết quả, chỉ khác cách viết",
   "Hình học phẳng chỉ sai ở góc thiên đỉnh = 0"],
  "Tại elevation thấp (~30 độ), hai công thức cho kết quả lệch nhau khoảng 11% -- sai số này lan truyền tiếp vào w_L rồi h_g, ảnh hưởng toàn bộ ngân sách liên kết.")

g = "Suy hao khí quyển"
Q(p1, g,
  "Công thức Kruse/Kim cho hệ số suy hao trời quang (không mây/mưa) phụ thuộc chủ yếu vào đại lượng nào?",
  ["Tầm nhìn ngang V (visibility): hệ số suy hao tỷ lệ nghịch với V, cộng với một hàm mũ phụ thuộc bước sóng",
   "Áp suất khí quyển tại mặt đất",
   "Tốc độ gió ở tầng cao (jet-stream)",
   "Độ cao vệ tinh so với mặt đất"],
  "V càng lớn (trời càng trong) thì hệ số suy hao sigma_clear càng nhỏ -- đây là lý do dự báo tầm nhìn là dữ liệu đầu vào quan trọng cho dự toán ngân sách liên kết quang.")

Q(p1, g,
  "Hệ số suy hao do mưa được mô hình hóa theo dạng beta_rain = alpha * R^rho với rho < 1 (rho=0.63 trong một mô hình nhiệt đới thực tế). Ý nghĩa của rho < 1 là gì?",
  ["Suy hao do mưa tăng DƯỚI tuyến tính theo cường độ mưa: mưa mạnh gấp 5 lần chỉ làm suy hao tăng khoảng 5^0.63 ~ 2.76 lần, không phải gấp 5 lần",
   "Suy hao do mưa tăng tuyến tính đúng bằng cường độ mưa",
   "Suy hao do mưa không phụ thuộc cường độ mưa khi rho<1",
   "Công thức chỉ đúng khi trời không mưa"],
  "Số mũ phân tuyến tính (rho=0.63) là đặc trưng thực nghiệm của mô hình mưa nhiệt đới -- quan trọng để không đánh giá quá cao mức độ tệ đi khi mưa rất to.")

Q(p1, g,
  "Theo định luật Beer-Lambert h_l = exp(-sigma_total * L_atm), nếu sigma_total tăng gấp đôi (ví dụ do mưa to thêm), hệ số truyền qua khí quyển h_l thay đổi thế nào?",
  ["h_l giảm theo hàm mũ (bình phương giá trị cũ, vì exp(-2x) = [exp(-x)]^2) -- suy hao tính theo dB tăng gấp đôi",
   "h_l giảm một nửa một cách tuyến tính",
   "h_l không đổi vì Beer-Lambert chỉ áp dụng cho ánh sáng khả kiến",
   "h_l tăng vì nhiều hạt mưa tán xạ ánh sáng về phía máy thu"],
  "Vì dB(suy hao) tỷ lệ tuyến tính với sigma_total*L_atm, tăng gấp đôi sigma_total tương đương tăng gấp đôi số dB suy hao -- trong thực tế mưa to có thể thêm ~100dB suy hao, gần như cắt đứt liên kết.")

Q(p1, g,
  "Khi đổi lượng mưa tháng (mm/tháng) từ dữ liệu khí hậu thành cường độ mưa theo giờ (mm/h) để đưa vào mô hình suy hao, tham số nào KHÔNG thể bỏ qua nếu muốn chính xác?",
  ["Tỷ lệ số giờ thực sự có mưa trong tháng (f_rain) -- vì mưa không rơi đều 24/7 cả tháng mà chỉ tập trung trong một phần nhỏ số giờ",
   "Nhiệt độ trung bình tháng, vì nhiệt độ quyết định cường độ mưa",
   "Áp suất khí quyển trung bình tháng",
   "Chỉ cần chia đều tổng lượng mưa cho tổng số giờ trong tháng (30*24), không cần tham số nào khác"],
  "Nếu chia đều cho toàn bộ giờ trong tháng sẽ đánh giá THẤP cường độ mưa thực tế (vì mưa chỉ rơi trong f_rain phần giờ) -- cần dữ liệu thực theo (thành phố, tháng) thay vì giả định một tỷ lệ cố định.")

g = "Nhiễu loạn khí quyển (scintillation)"
Q(p1, g,
  "Hồ sơ Hufnagel-Valley 5/7 mô tả đại lượng nào theo độ cao h?",
  ["Cấu trúc chiết suất khúc xạ của khí quyển Cn2(h), phản ánh cường độ xoáy chuyển loạn của không khí tại mỗi độ cao",
   "Áp suất khí quyển theo độ cao",
   "Nhiệt độ khí quyển theo độ cao",
   "Độ ẩm tương đối theo độ cao"],
  "Cn2(h) là đầu vào trực tiếp cho tích phân tính phương sai Rytov -- càng loạn mạch mạnh (Cn2 lớn) ở các lớp khí quyển mà tia sáng đi qua, nhiễu loạn (scintillation) càng mạnh.")

Q(p1, g,
  "Trong hồ sơ H-V 5/7, số mũ 10 trong số hạng (10^-5 * h)^10 có ý nghĩa gì nếu tính sai thành số mũ 1?",
  ["Đây là đặc trưng bắt buộc của mô hình H-V 5/7; dùng nhầm số mũ 1 sẽ làm sai lệch Cn2(h) tới khoảng 10 bậc độ lớn, gây kết quả phương sai Rytov vô lý",
   "Không quan trọng, cả hai số mũ cho kết quả tương đương",
   "Số mũ 10 chỉ ảnh hưởng ở độ cao rất thấp gần mặt đất",
   "Số mũ này chỉ là hệ số làm tròn, có thể bỏ qua"],
  "Đây là một lỗi thực tế từng xảy ra trong quá trình phát triển mô hình: nhầm số mũ gây sai lệch ~10 bậc độ lớn, phát hiện được nhờ kiểm tra 'phương sai Rytov vô lý ~10^8'.")

Q(p1, g,
  "Hệ số nhân trong công thức phương sai Rytov cho đường truyền nghiêng (slant-path, plane-wave) là 2.25 theo tài liệu chuẩn (Andrews & Phillips). Nếu một phiên bản trước đó dùng hệ số 0.56 (= 2.25/4), đây có thể là lỗi gì?",
  ["Nhầm lẫn giữa sigma_R^2 (phương sai Rytov) và sigma_X^2 (= sigma_R^2/4, phương sai log-biên độ) -- tính nhầm một đại lượng rồi lại chia 4 lần nữa, gây hụt nhiễu loạn ~4 lần thêm",
   "Chỉ là sai số làm tròn không đáng kể",
   "Hệ số 0.56 dành cho bước sóng khác 1550nm",
   "Hệ số 0.56 dùng cho đường truyền thẳng đứng (zenith), 2.25 cho đường nghiêng"],
  "Đây là một fix quan trọng được phát hiện qua đối chiếu kỹ với công thức gốc: tính nhầm hệ số làm hụt cả sigma_R^2 thật sự đi 4 lần, rồi bước chia sigma_X^2=sigma_R^2/4 lại hụt thêm một lần nữa.")

Q(p1, g,
  "Vì sao Cn2(0) (độ loạn không khí tại mặt đất) hầu như KHÔNG ảnh hưởng đáng kể đến phương sai Rytov trên một đường truyền nghiêng từ vệ tinh quỹ đạo thấp (~550km) xuống mặt đất?",
  ["Vì số hạng chứa Cn2(0) trong hồ sơ H-V tắt rất nhanh theo độ cao (chỉ còn đáng kể trong khoảng vài trăm mét), trong khi tích phân Rytov chạy trên toàn bộ đường truyền hàng trăm km",
   "Vì Cn2(0) luôn bằng 0 trong thực tế",
   "Vì máy thu được đặt cao hơn mặt đất nên không chịu ảnh hưởng lớp này",
   "Vì công thức Rytov không sử dụng Cn2(0) làm đầu vào"],
  "Kiểm chứng thực tế: thay đổi Cn2(0) tới 17 lần chỉ làm phương sai Rytov thay đổi ~2.8% -- biến số thực sự chi phối là tốc độ gió tầng cao (qua số hạng jet-stream), không phải độ loạn mặt đất.")

Q(p1, g,
  "Sau khi áp dụng hệ số Rytov đã sửa (2.25), giá trị phương sai Rytov thu được trên một liên kết LEO-mặt đất thực tế (góc ngưỡng đến 30 độ) vẫn nhỏ hơn 0.3. Ý nghĩa thực hành của điều này là gì?",
  ["Mô hình log-normal (nhiễu loạn yếu) vẫn còn hợp lệ, chưa cần chuyển sang mô hình Gamma-Gamma phức tạp hơn (dành cho nhiễu loạn mạnh)",
   "Kết quả này chứng tỏ fix hệ số là sai vì không làm thay đổi kết luận",
   "Phải luôn dùng Gamma-Gamma bất kể giá trị phương sai Rytov",
   "Giá trị dưới 0.3 có nghĩa liên kết hoàn toàn không bị nhiễu loạn"],
  "Các mô hình fading quang chia theo chế độ 'yếu' (log-normal, sigma_R^2<0.3) và 'mạnh' (Gamma-Gamma); kể cả sau khi sửa hệ số, các liên kết LEO nhiệt đới trong dải góc này vẫn thuộc chế độ yếu.")

Q(p1, g,
  "Mô hình fading log-normal h_a = exp(2X) với X ~ N(-sigma_X^2, sigma_X^2) chọn trung bình của X là -sigma_X^2 (không phải 0) nhằm mục đích gì?",
  ["Đảm bảo kỳ vọng của h_a (E[h_a]) bằng 1 -- tức fading trung bình không làm mất hay thêm năng lượng tổng thể, chỉ làm biến động quanh mức chuẩn",
   "Để h_a luôn nhỏ hơn 1 trong mọi trường hợp",
   "Để đơn giản hóa tính toán, không có ý nghĩa vật lý",
   "Để phù hợp với đơn vị decibel"],
  "Đây là điều kiện chuẩn hóa bắt buộc cho mọi mô hình fading nhân tính: nếu không có số hạng bù -sigma_X^2, trung bình của kênh fading sẽ lệch khỏi 1, gây sai lệch hệ thống trong tính công suất trung bình thu được.")

g = "Chuỗi suy hao tổng hợp"
Q(p1, g,
  "Hệ số truyền đạt tổng thể của kênh quang không gian h = h_g * h_l * h_a được ghép bởi cách nào?",
  ["Nhân các hệ số độc lập với nhau: hình học (h_g), khí quyển hấp thụ/tán xạ (h_l), và nhiễu loạn (h_a, ngẫu nhiên) -- mỗi thành phần mô tả một cơ chế vật lý riêng biệt",
   "Cộng các hệ số lại với nhau theo dB trực tiếp mà không đổi đơn vị",
   "Chỉ một trong ba hệ số quyết định, hai hệ số còn lại luôn xấp xỉ 1",
   "Nhân hai hệ số đầu, bỏ qua nhiễu loạn vì luôn rất nhỏ"],
  "Cấu trúc nhân (tương đương cộng theo dB) là mô hình chuẩn cho ngân sách liên kết quang: h_g thường chiếm ưu thế (>30dB một mình) do bản chất giới hạn nhiễu xạ của liên kết không gian.")

Q(p1, g,
  "Trong ba thành phần h_g, h_l, h_a, thành phần nào thường DAO ĐỘNG NGẪU NHIÊN theo thời gian thực (trong khung thời gian mili-giây đến giây), còn hai thành phần kia thì tương đối 'chậm' hoặc tất định?",
  ["h_a (nhiễu loạn khí quyển) là ngẫu nhiên nhanh; h_g (hình học) tất định theo quỹ đạo; h_l (khí quyển hấp thụ) thay đổi chậm theo thời tiết",
   "Cả ba thành phần đều tất định hoàn toàn",
   "Cả ba thành phần đều ngẫu nhiên với cùng tốc độ biến đổi",
   "h_g là ngẫu nhiên nhanh nhất vì phụ thuộc rung động vệ tinh"],
  "Phân biệt tốc độ biến đổi của từng thành phần giúp thiết kế hệ thống bù trừ phù hợp: bù nhiễu loạn cần điều khiển nhanh (adaptive optics), còn h_g/h_l chỉ cần cập nhật theo lịch quỹ đạo/thời tiết.")

Q(p1, g,
  "Nếu một kỹ sư thiết kế hệ thống muốn giảm suy hao chủ đạo nhất của liên kết FSO không gian-mặt đất (thường là h_g), đòn bẩy thiết kế nào HIỆU QUẢ nhất theo phân tích chuỗi công thức trên?",
  ["Tăng đường kính khẩu độ thu (a_R) hoặc giảm góc phân kỳ chùm (theta_C) -- cả hai đều làm tăng h_g nhưng đều đắt về khối lượng/năng lượng/độ phức tạp hệ thống trỏ hướng (SWaP/PAT)",
   "Tăng công suất phát lên rất cao là cách duy nhất và rẻ nhất",
   "Đổi bước sóng sang vùng sóng vô tuyến sẽ loại bỏ hoàn toàn vấn đề này",
   "Không thể cải thiện h_g bằng bất kỳ cách nào, chỉ có thể bù bằng tăng công suất"],
  "Vì h_g tỷ lệ với (a_R/w_L)^2 (ở chế độ yếu), tăng khẩu độ hoặc giảm góc phân kỳ là đòn bẩy vật lý trực tiếp -- đây là lý do thiết kế khẩu độ thu và hệ thống trỏ hướng chính xác (PAT) là trọng tâm kỹ thuật của liên kết FSO không gian.")

Q(p1, g,
  "Vì sao một liên kết liên-vệ-tinh (ISL, cả hai đầu đều trong không gian) thường có ngân sách liên kết 'dễ thở' hơn nhiều so với liên kết xuống mặt đất, dù cùng dùng công nghệ laser tương tự?",
  ["Vì ISL không phải đi qua khí quyển (h_l ~ 1, không hấp thụ/tán xạ/nhiễu loạn bởi không khí), chỉ còn suy hao hình học (nhiễu xạ theo khoảng cách) cần tính đến",
   "Vì vệ tinh luôn gần nhau hơn trạm mặt đất",
   "Vì công suất phát của ISL luôn lớn hơn nhiều lần",
   "Vì ISL dùng bước sóng khác hoàn toàn không bị suy hao"],
  "Bay trong chân không loại bỏ cả ba nguồn suy hao khí quyển (hấp thụ trời quang, hấp thụ mưa, nhiễu loạn) -- đây là lý do kiến trúc 'mesh trên trời' có dư địa liên kết lớn hơn nhiều so với downlink RF/quang xuống mặt đất.")

Q(p1, g,
  "Một hệ thống FSO hoạt động tốt vào ban đêm (P_bg=0, không nền sáng) nhưng cửa sổ thời tiết tốt nhất lại rơi vào ban ngày (ít mây). Đây là loại mâu thuẫn gì trong thiết kế hệ thống?",
  ["Mâu thuẫn giữa yêu cầu vật lý của máy thu (tránh nền sáng ban ngày làm tăng nhiễu) và lịch trình thực tế tối ưu về mặt khí tượng (ít mây nhất vào một khung giờ ban ngày cụ thể)",
   "Không có mâu thuẫn gì, hai yếu tố này hoàn toàn độc lập",
   "Vấn đề chỉ xảy ra ở vĩ độ cao, không liên quan vùng nhiệt đới",
   "Máy thu quang không bao giờ bị ảnh hưởng bởi ánh sáng nền"],
  "Đây là một giới hạn thiết kế còn mở trong nghiên cứu hệ thống SIKD: khung giờ thời tiết tốt nhất (sáng sớm) chồng lấn với ban ngày, trong khi các ước tính SKR ở đây đều giả định điều kiện đêm tối ưu -- cần ước lượng riêng ảnh hưởng nền sáng ban ngày lên máy thu.")

Q(p1, g,
  "Trong chuỗi tính toán ngân sách liên kết, tại sao cần tính h_g trước rồi mới tính h_l và h_a, thay vì tính độc lập không theo thứ tự?",
  ["Vì h_g phụ thuộc slant range L (từ hình học quỹ đạo), và L cũng là đầu vào trực tiếp để tính độ dài đường truyền khí quyển L_atm cho h_l -- các đại lượng hình học là nền tảng cho cả hai bước sau",
   "Thứ tự không quan trọng vì cả ba đều là hằng số cố định",
   "Vì quy định lập trình yêu cầu tính theo thứ tự bảng chữ cái",
   "Vì h_a phải tính trước h_g để chuẩn hóa đơn vị"],
  "L (từ hình học) quyết định cả w_L (cho h_g) lẫn L_atm = (H_atm - H_U)/cos(zenith) (cho h_l) -- đây là lý do mọi sai số trong bước hình học (ví dụ dùng xấp xỉ phẳng thay vì cầu) sẽ lan truyền sang cả các bước tiếp theo.")

Q(p1, g,
  "Nếu góc ngưỡng (elevation) giảm từ 90 độ xuống 30 độ, hai hiệu ứng nào CÙNG LÚC làm xấu ngân sách liên kết quang?",
  ["Slant range L tăng (làm h_g giảm) VÀ độ dài đường truyền khí quyển L_atm tăng theo 1/cos(zenith) (làm h_l giảm) -- cả hai cùng tác động theo hướng bất lợi",
   "Chỉ h_g bị ảnh hưởng, h_l không đổi theo góc ngưỡng",
   "Chỉ h_l bị ảnh hưởng, h_g không đổi theo góc ngưỡng",
   "Cả hai đều được cải thiện khi góc ngưỡng giảm"],
  "Đây là lý do các trạm mặt đất thường đặt ngưỡng góc ngưỡng tối thiểu (mask elevation, ví dụ 30-40 độ) để tránh vùng góc thấp mà cả hai cơ chế suy hao đều xấu đi đồng thời.")

Q(p1, g,
  "Giả sử một kỹ sư chỉ đổi khẩu độ thu từ 5cm lên 10cm nhưng KHÔNG đổi bất kỳ tham số nào khác. Điều gì xảy ra với hệ số hình học h_g ở chế độ nu_R nhỏ?",
  ["h_g tăng khoảng 4 lần (xấp xỉ +6dB), vì h_g tỷ lệ với bình phương khẩu độ thu trong chế độ erf(nu_R) tuyến tính",
   "h_g không đổi vì h_g chỉ phụ thuộc góc phân kỳ chùm, không phụ thuộc khẩu độ thu",
   "h_g giảm vì khẩu độ lớn hơn thu thêm cả nhiễu nền",
   "h_g tăng đúng 2 lần (tỷ lệ thuận với đường kính)"],
  "Đây là mối quan hệ bậc hai then chốt (h_g ~ a_R^2) giúp kỹ sư đánh giá nhanh lợi ích của việc tăng khẩu độ viễn vọng kính thu, đổi lại với chi phí SWaP.")

Q(p1, g,
  "Trong bảng tra cứu nhanh của mô hình, h_g thực tế nằm trong khoảng -34 đến -39 dB và h_l (trời quang) trong khoảng -9 đến -18 dB. So sánh hai con số này cho thấy điều gì về đóng góp của từng yếu tố vào TỔNG suy hao?",
  ["Suy hao hình học (h_g) là thành phần chi phối ngân sách liên kết, lớn hơn nhiều so với suy hao khí quyển trời quang (h_l) trong điều kiện bình thường",
   "Hai thành phần luôn đóng góp bằng nhau vào tổng suy hao",
   "Suy hao khí quyển luôn lớn hơn suy hao hình học",
   "Cả hai đều không đáng kể so với nhiễu máy thu"],
  "Đây là một kết luận thiết kế quan trọng: dù tối ưu hóa khí quyển (chọn thời tiết tốt) tối đa cũng chỉ cải thiện vài chục dB, trong khi h_g một mình đã chiếm hơn 30dB -- muốn cải thiện tổng thể phải tập trung vào hình học/khẩu độ.")

g = "Ứng dụng số liệu cụ thể"
Q(p1, g,
  "Với theta_C = 10 microrad và lambda = 1550nm, bán kính thắt chùm w0 = lambda/(2*theta_C) xấp xỉ bao nhiêu?",
  ["Khoảng 7.75cm (w0 = 1550e-9 / (2*10e-6) = 0.0775m)",
   "Khoảng 77.5cm, lớn hơn 10 lần",
   "Khoảng 0.775mm, nhỏ hơn 100 lần",
   "Khoảng 7.75m, lớn hơn 100 lần"],
  "Đây là phép tính trực tiếp minh họa quy mô thực tế: chùm tia laser vệ tinh xuất phát với bán kính cỡ vài cm tại nguồn, nhưng lan rộng đến vài mét khi tới mặt đất do khoảng cách hàng trăm km.")

Q(p1, g,
  "Ở góc thiên đỉnh zeta=0 (elevation 90 độ, vệ tinh đúng đỉnh đầu) với độ cao quỹ đạo H_S=550km, slant range L (cả hai công thức phẳng và cầu) bằng bao nhiêu, và tại sao hai công thức trùng nhau đúng ở điểm này?",
  ["L = 550km trong cả hai công thức, vì tại thiên đỉnh vệ tinh nằm thẳng trên đầu trạm nên độ cong Trái Đất không tạo ra sai khác giữa mô hình phẳng và mô hình cầu",
   "L = 550km chỉ trong công thức cầu, công thức phẳng cho kết quả khác",
   "Hai công thức luôn khác nhau ở mọi góc, kể cả zeta=0",
   "L phụ thuộc vào vĩ độ trạm mặt đất, không chỉ độ cao quỹ đạo"],
  "Đây là một điểm kiểm tra chéo (cross-check) hữu ích: hai mô hình hình học khác nhau PHẢI hội tụ về cùng kết quả ở trường hợp biên (thẳng đứng) -- nếu không khớp, một trong hai công thức chắc chắn có lỗi.")

Q(p1, g,
  "So sánh h_g tại elevation 90 độ (-33.90dB) và tại elevation 30 độ (-39.03dB), chênh lệch khoảng 5dB. Nguyên nhân trực tiếp của chênh lệch này là gì?",
  ["Slant range tăng từ 550km lên 992.8km khi elevation giảm, làm w_L (bán kính chùm tại máy thu) tăng theo, khiến tỷ lệ năng lượng lọt vào khẩu độ thu (a_R/w_L)^2 giảm mạnh",
   "Công suất phát của vệ tinh tự động giảm khi elevation thấp",
   "Bước sóng laser thay đổi theo góc quan sát",
   "Chênh lệch này hoàn toàn do suy hao khí quyển, không liên quan hình học"],
  "Chuỗi nhân quả rõ ràng: elevation thấp -> slant range dài hơn -> chùm tia lan rộng hơn tại máy thu -> hệ số hình học xấu đi -- đây là lý do các trạm ưu tiên bắt liên kết khi vệ tinh ở elevation cao.")

Q(p1, g,
  "Nếu tầm nhìn V = 10km và bước sóng lambda = 1550nm, số mũ q(V) trong công thức Kruse/Kim (dải 6 < V <= 50) là q=1.3. Việc số mũ q phụ thuộc vào chính giá trị V (không phải hằng số cố định) phản ánh điều gì về bản chất vật lý của suy hao trời quang?",
  ["Cơ chế tán xạ ánh sáng bởi các hạt trong khí quyển thay đổi tính chất (kích thước hạt sương/bụi chi phối) tùy mức độ trong suốt của không khí, nên không thể dùng một công thức suy hao duy nhất cho mọi điều kiện tầm nhìn",
   "q(V) chỉ là một hệ số hiệu chỉnh tùy ý không có cơ sở vật lý",
   "V không thực sự ảnh hưởng đến suy hao, chỉ ảnh hưởng đến q",
   "Công thức này chỉ đúng khi V luôn lớn hơn 50km"],
  "Việc chia theo dải V (khác hệ số mũ cho sương mù dày, sương mù vừa, trời trong) phản ánh các chế độ tán xạ Mie khác nhau tùy kích thước hạt tương đối so với bước sóng -- một chi tiết thực nghiệm quan trọng của mô hình Kruse/Kim.")

Q(p1, g,
  "Trong ví dụ minh họa mưa to R=30mm/h ở góc zeta=30 độ, suy hao khí quyển tổng cộng đạt khoảng -110.4dB, so với chỉ -10.2dB lúc trời quang cùng góc. Từ góc độ thiết kế hệ thống, con số 100dB chênh lệch này có ý nghĩa gì?",
  ["Một hệ thống FSO thực tế KHÔNG thể duy trì liên kết qua mưa to bằng cách tăng công suất phát bù trừ (100dB là mức không khả thi về công suất) -- giải pháp thực tế là chuyển sang trạm dự phòng ở địa điểm khác không mưa, hoặc chờ thời tiết cải thiện",
   "Chỉ cần tăng công suất phát lên 100dB (10^10 lần) là bù được hoàn toàn",
   "100dB không đáng kể so với ngân sách liên kết tổng thể",
   "Mưa to thực ra cải thiện liên kết bằng cách làm sạch bụi trong không khí"],
  "Đây là lý do các hệ thống FSO thực tế luôn cần chiến lược dự phòng đa trạm (site diversity) thay vì chỉ dựa vào một trạm duy nhất -- vật lý không cho phép 'vượt qua' suy hao mưa to bằng công suất.")

Q(p1, g,
  "Nếu một hệ thống đo được phương sai Rytov sigma_R^2 = 0.25 (gần ngưỡng 0.3 phân chia chế độ yếu/mạnh), quyết định thiết kế thận trọng nên là gì?",
  ["Vẫn tạm dùng mô hình log-normal nhưng theo dõi sát điều kiện thực tế (gió tầng cao, mùa) vì giá trị gần ngưỡng có thể vượt sang chế độ nhiễu loạn mạnh trong điều kiện xấu hơn, khi đó cần chuyển sang mô hình Gamma-Gamma",
   "Luôn an toàn vì 0.25 nhỏ hơn 0.3 nên không cần quan tâm thêm",
   "Ngay lập tức chuyển sang mô hình Gamma-Gamma bất kể giá trị chưa vượt ngưỡng",
   "Giá trị 0.25 không có ý nghĩa thực tế nào, chỉ là một con số trung gian"],
  "Đây là tư duy kỹ thuật thận trọng khi giá trị đo/tính nằm gần ranh giới giữa hai chế độ mô hình khác nhau -- không nên áp dụng mô hình một cách máy móc mà cần xét biên độ an toàn.")

Q(p1, g,
  "Vì sao bước sóng 1550nm được ưu tiên chọn cho các liên kết FSO không gian thay vì các bước sóng khả kiến (ví dụ 550nm)?",
  ["1550nm nằm trong cửa sổ truyền dẫn tốt của khí quyển và tương thích với công nghệ laser/sợi quang viễn thông trưởng thành (đã phát triển cho ngành viễn thông sợi quang mặt đất), đồng thời an toàn hơn cho mắt người ở cùng mức công suất",
   "1550nm bị khí quyển hấp thụ mạnh nhất nên an toàn hơn",
   "1550nm không thể xuyên qua khí quyển nên chỉ dùng được cho ISL",
   "Không có lý do kỹ thuật, chỉ là quy ước lịch sử ngẫu nhiên"],
  "Việc chọn bước sóng viễn thông chuẩn 1550nm cho phép tận dụng toàn bộ hệ sinh thái linh kiện quang (laser, bộ khuếch đại, bộ điều chế) đã được phát triển và thương mại hóa rộng rãi cho ngành viễn thông sợi quang.")

Q(p1, g,
  "Đối với một liên kết ISL (vệ tinh-vệ tinh) và một liên kết downlink (vệ tinh-mặt đất) có cùng khoảng cách L, tại sao ISL có suy hao TỔNG THỂ thấp hơn hẳn dù hệ số hình học h_g có thể tương tự?",
  ["Vì ISL có h_l ~ 1 (không suy hao khí quyển) trong khi downlink phải nhân thêm hệ số h_l (thường -9 đến -18dB hoặc tệ hơn nhiều khi mưa) -- đây là khác biệt chính giữa hai loại liên kết chứ không phải ở hình học",
   "Vì ISL luôn có khoảng cách ngắn hơn downlink",
   "Vì ISL dùng công suất phát cao hơn downlink",
   "Vì ISL không cần khẩu độ thu lớn như downlink"],
  "Đây là lý do kiến trúc mạng vệ tinh hiện đại ưu tiên chuyển tiếp dữ liệu qua ISL nhiều nhất có thể trước khi hạ xuống mặt đất -- giảm thiểu số lần phải 'trả giá' suy hao khí quyển.")

Q(p1, g,
  "Một hệ thống tăng khẩu độ thu a_R từ 5cm lên 15cm (gấp 3 lần). Ước lượng mức cải thiện h_g theo dB (ở chế độ nu_R nhỏ, h_g ~ a_R^2)?",
  ["Khoảng +9.5dB (10*log10(3^2) = 10*log10(9) ~ 9.54dB)",
   "Khoảng +3dB, tương ứng tăng tuyến tính",
   "Khoảng +30dB, tăng theo lũy thừa bậc 4",
   "Không thay đổi vì h_g không phụ thuộc khẩu độ"],
  "Đây là bài tập áp dụng trực tiếp quan hệ bậc hai h_g ~ a_R^2: gấp 3 lần đường kính khẩu độ mang lại gần 10dB cải thiện, một mức đáng kể trong ngân sách liên kết, nhưng đổi lại kích thước/khối lượng viễn vọng kính tăng đáng kể.")

Q(p1, g,
  "Xét chuỗi h = h_g * h_l * h_a với h_g cỡ -35dB, h_l cỡ -12dB (trời quang), và h_a dao động ngẫu nhiên quanh 0dB (do chuẩn hóa E[h_a]=1). Suy hao TRUNG BÌNH tổng cộng của kênh gần bằng bao nhiêu?",
  ["Khoảng -47dB (cộng trực tiếp các giá trị dB: -35 + -12 + 0)",
   "Khoảng -35dB, chỉ tính thành phần lớn nhất",
   "Khoảng -12dB, chỉ tính thành phần khí quyển",
   "Khoảng -420dB, nhân các giá trị dB với nhau"],
  "Vì cấu trúc h = h_g*h_l*h_a là NHÂN các hệ số tuyến tính, cộng các giá trị dB tương ứng là phép tính đúng -- đây là kỹ năng chuyển đổi domain (tuyến tính vs logarit) cơ bản trong phân tích ngân sách liên kết.")

g = "So sánh FSO với RF & công nghệ bù trừ"
Q(p1, g,
  "So với liên kết RF (vô tuyến), lợi thế cơ bản của liên kết FSO (quang) về mặt PHỔ TẦN là gì?",
  ["FSO không cần đăng ký phổ tần với cơ quan quản lý viễn thông (như ITU) vì hoạt động ở dải bước sóng quang, tránh được vấn đề khan hiếm/xung đột phổ tần vốn ngày càng nghiêm trọng ở băng RF",
   "FSO luôn có băng thông thấp hơn RF nên ít bị nhiễu hơn",
   "FSO không bị ảnh hưởng bởi bất kỳ điều kiện thời tiết nào, khác RF",
   "FSO không cần bất kỳ hệ thống trỏ hướng chính xác nào, khác RF"],
  "Đây là một lợi thế kinh tế/quy định quan trọng của FSO: trong khi băng RF (đặc biệt các băng phổ biến như Ku/Ka) đòi hỏi cấp phép và ngày càng đông đúc, chùm tia laser hẹp hoạt động ở bước sóng quang không thuộc phạm vi quản lý phổ vô tuyến truyền thống.")

Q(p1, g,
  "Ngược lại, nhược điểm chính của FSO so với RF khi xét về ĐỘ NHẠY với điều kiện khí quyển là gì?",
  ["FSO nhạy cảm hơn NHIỀU với mây/mưa/sương mù (có thể mất liên kết hoàn toàn khi mây dày), trong khi RF ở các băng tần thấp hơn (ví dụ L/S-band) ít bị ảnh hưởng bởi các hiện tượng khí tượng này hơn",
   "FSO hoàn toàn không bị ảnh hưởng bởi thời tiết, chỉ RF mới bị ảnh hưởng",
   "Cả FSO và RF đều bị ảnh hưởng như nhau bởi mọi điều kiện thời tiết",
   "RF nhạy cảm hơn FSO đối với mây và sương mù"],
  "Đây là lý do các hệ thống thực tế cân nhắc kiến trúc LAI (hybrid RF/FSO): dùng FSO cho thông lượng cao khi thời tiết cho phép, chuyển sang RF dự phòng khi mây/mưa cản trở liên kết quang -- tận dụng ưu điểm bổ sung của cả hai công nghệ.")

Q(p1, g,
  "Hệ thống trỏ hướng, thu nhận, bám mục tiêu (Pointing, Acquisition, Tracking - PAT) đóng vai trò gì trong một liên kết FSO không gian, và tại sao nó ít quan trọng hơn nhiều đối với liên kết RF cùng cự ly?",
  ["FSO dùng chùm tia rất hẹp (góc phân kỳ vài microrad) nên cần trỏ hướng cực kỳ chính xác để đảm bảo chùm tia thực sự chiếu trúng khẩu độ thu nhỏ ở xa hàng trăm km; RF dùng búp sóng anten rộng hơn nhiều nên yêu cầu độ chính xác trỏ hướng thấp hơn đáng kể",
   "PAT chỉ cần thiết cho RF, không cần thiết cho FSO",
   "PAT không có vai trò gì trong cả hai loại liên kết",
   "Độ chính xác trỏ hướng yêu cầu như nhau cho cả FSO và RF"],
  "Đây là lý do hệ thống FSO không gian phức tạp và đắt đỏ hơn về mặt cơ khí/quang học so với RF cùng chức năng -- góc phân kỳ chùm hẹp (đem lại lợi ích tập trung năng lượng, xem Công thức 1) đòi hỏi đánh đổi bằng độ chính xác trỏ hướng cực cao.")

Q(p1, g,
  "Công nghệ quang thích ứng (adaptive optics, dùng cảm biến mặt sóng và gương biến dạng để bù méo mặt sóng theo thời gian thực) có thể giúp giảm ảnh hưởng của thành phần nào trong ba thành phần h_g, h_l, h_a?",
  ["h_a (nhiễu loạn khí quyển): adaptive optics đo và bù trừ trực tiếp sự méo mặt sóng do nhiễu loạn gây ra theo thời gian thực, cải thiện chất lượng hội tụ chùm tia tại máy thu",
   "h_g (suy hao hình học): adaptive optics chỉ ảnh hưởng đến khẩu độ thu, không liên quan nhiễu loạn",
   "h_l (suy hao khí quyển hấp thụ): adaptive optics loại bỏ hoàn toàn ảnh hưởng của mây và mưa",
   "Adaptive optics không có tác dụng gì đối với bất kỳ thành phần suy hao nào"],
  "Đây là công nghệ bù trừ tiên tiến chuyên biệt cho nhiễu loạn (thành phần ngẫu nhiên nhanh h_a) -- một hướng cải thiện bổ sung khác với các đòn bẩy hình học (khẩu độ, góc phân kỳ) đã thảo luận, cho các hệ thống yêu cầu hiệu năng cao hơn.")

Q(p1, g,
  "Trong bối cảnh môn học 'Các công nghệ truyền thông cho IoT', vì sao hiểu cả hai công nghệ RF VÀ FSO lại quan trọng, thay vì chỉ học một trong hai?",
  ["Vì các hệ thống vệ tinh IoT hiện đại (ví dụ Starlink) thường kết hợp cả hai: RF cho downlink/uplink người dùng (dễ triển khai đại trà, ít nhạy thời tiết) và FSO/laser cho liên kết liên-vệ-tinh mật độ cao (không qua khí quyển nên tận dụng được ưu điểm thông lượng lớn của quang) -- hiểu cả hai giúp phân tích đúng kiến trúc hệ thống thực tế",
   "Chỉ cần học RF là đủ vì FSO không được sử dụng trong thực tế",
   "Chỉ cần học FSO là đủ vì RF là công nghệ đã lỗi thời",
   "Hai công nghệ này hoàn toàn không liên quan đến nhau trong bất kỳ hệ thống thực tế nào"],
  "Đây là lý do kiến trúc 'mesh trên trời, phễu xuống đất' (đã thảo luận ở phần link budget Starlink) kết hợp cả RF (downlink) và FSO/laser (ISL) -- mỗi công nghệ được dùng đúng chỗ phát huy ưu thế của nó.")

Q(p1, g,
  "Nếu một kỹ sư đề xuất dùng FSO thay thế HOÀN TOÀN cho RF trong downlink vệ tinh-người dùng ở vùng nhiệt đới (mây nhiều quanh năm), rủi ro kỹ thuật chính của đề xuất này là gì?",
  ["Độ khả dụng liên kết downlink sẽ rất thấp trong các tháng nhiều mây (có thể chỉ 10-15% như đã phân tích ở phần thời tiết), khiến dịch vụ không đủ tin cậy cho người dùng cuối cần kết nối liên tục -- FSO downlink phù hợp hơn cho các ứng dụng chấp nhận gián đoạn (ví dụ tích lũy dữ liệu theo cơ hội), không phù hợp thay thế hoàn toàn RF cho dịch vụ liên tục",
   "Không có rủi ro nào, FSO luôn hoạt động tốt hơn RF trong mọi điều kiện thời tiết",
   "Rủi ro chỉ tồn tại ở vùng ôn đới, không áp dụng cho vùng nhiệt đới",
   "FSO downlink không bao giờ bị ảnh hưởng bởi mây, chỉ ISL mới bị ảnh hưởng"],
  "Đây là ứng dụng tổng hợp giữa kiến thức vật lý kênh (Bậc 1) và thống kê thời tiết (Bậc 3): quyết định công nghệ nào phù hợp cho downlink phải cân nhắc độ khả dụng thực tế theo khí hậu địa phương, không chỉ dựa vào ưu điểm lý thuyết về băng thông.")

Q(p1, g,
  "Vì sao khẩu độ thu của một trạm mặt đất FSO (thường vài chục cm đường kính) nhỏ hơn nhiều so với ăng-ten chảo RF cho cùng cự ly liên kết vệ tinh (có thể vài mét)?",
  ["Vì bước sóng quang (1550nm) ngắn hơn bước sóng RF (cm) nhiều bậc độ lớn, và độ lợi/độ hội tụ của một khẩu độ thu tỷ lệ nghịch với bình phương bước sóng ở cùng kích thước vật lý -- khẩu độ quang nhỏ đã đủ hội tụ năng lượng hiệu quả nhờ bước sóng ngắn",
   "Khẩu độ FSO nhỏ hơn vì công suất phát FSO luôn thấp hơn RF nhiều lần",
   "Không có sự khác biệt thực sự về kích thước khẩu độ giữa hai công nghệ",
   "Khẩu độ RF nhỏ hơn FSO trong hầu hết các hệ thống thực tế"],
  "Đây là một hệ quả trực tiếp của vật lý sóng điện từ: bước sóng ngắn hơn (quang so với RF) cho phép đạt độ định hướng/độ lợi tương đương với khẩu độ vật lý nhỏ hơn nhiều -- một lý do khác khiến thiết bị đầu cuối FSO có thể nhỏ gọn hơn ăng-ten RF chảo lớn.")

Q(p1, g,
  "Trong thiết kế một hệ thống liên kết vệ tinh lai RF/FSO, tiêu chí CHUYỂN ĐỔI (switchover) giữa hai chế độ có thể dựa trên đại lượng nào đã học trong phần kênh vật lý?",
  ["Ước lượng thời gian thực của suy hao khí quyển h_l (ví dụ dựa vào cảm biến mây/mưa cục bộ hoặc dự báo ngắn hạn) -- khi h_l dự kiến xấu đi quá một ngưỡng (ví dụ do mây dày sắp tới), hệ thống chủ động chuyển từ FSO sang RF trước khi liên kết quang bị gián đoạn hoàn toàn",
   "Chuyển đổi luôn dựa vào thời gian trong ngày cố định, không cần đo đạc thực tế",
   "Không có tiêu chí kỹ thuật nào hợp lý để quyết định chuyển đổi",
   "Chuyển đổi chỉ nên thực hiện thủ công bởi người vận hành, không thể tự động hóa"],
  "Đây là một ứng dụng thiết kế hệ thống thực tế tổng hợp kiến thức về mô hình suy hao khí quyển: một hệ thống lai thông minh cần giám sát liên tục điều kiện kênh và chuyển đổi chủ động trước khi chất lượng dịch vụ suy giảm nghiêm trọng.")

# ============================================================================
# P2 -- May thu: nhieu, nguong quyet dinh, QBER, SKR, BER
# ============================================================================
p2 = P(2, "Máy thu quang điện: mô hình nhiễu, QBER, tốc độ khóa & dữ liệu")

g = "Mô hình nhiễu 4 thành phần"
Q(p2, g,
  "Nhiễu shot (shot noise) tại máy thu quang điện phát sinh từ đâu, và nó tỷ lệ với đại lượng nào?",
  ["Từ bản chất rời rạc (hạt) của dòng quang điện; tỷ lệ với TỔNG dòng quang điện một chiều (DC) tại photodetector, không phải chỉ riêng một kênh điều chế",
   "Chỉ phát sinh từ nhiệt độ của điện trở tải (resistor)",
   "Chỉ tỷ lệ với độ sâu điều chế của kênh khóa",
   "Không liên quan gì đến công suất quang thu được"],
  "Một lỗi từng gặp: nhân nhầm shot noise với độ sâu điều chế kênh khóa (m_K) làm hụt nhiễu ~20 lần -- shot noise phải tính trên TỔNG dòng DC chung của cả hai kênh vì chúng dùng chung một photodetector.")

Q(p2, g,
  "Nhiễu nhiệt (thermal noise) sigma_thermal^2 = 4*k_B*T/R_L * delta_f phụ thuộc vào những yếu tố nào, và KHÔNG phụ thuộc vào yếu tố nào?",
  ["Phụ thuộc nhiệt độ T và điện trở tải R_L; KHÔNG phụ thuộc công suất quang thu được (độc lập với cường độ tín hiệu)",
   "Phụ thuộc trực tiếp vào công suất quang phát P_T",
   "Chỉ phụ thuộc bước sóng của laser",
   "Chỉ xuất hiện khi trời có mây, biến mất khi trời quang"],
  "Đây là nhiễu 'nền' cố định của mạch điện tử, độc lập với tín hiệu quang -- khác hẳn shot noise và crosstalk noise đều phụ thuộc công suất quang thu được.")

Q(p2, g,
  "Nhiễu xuyên âm (crosstalk noise) từ kênh dữ liệu sang kênh khóa tỷ lệ với BÌNH PHƯƠNG của tích (công suất phát * độ sâu điều chế dữ liệu * hệ số kênh). Điều này dẫn đến nghịch lý gì khi liên kết càng MẠNH (elevation cao, h_g*h_l lớn)?",
  ["Khi liên kết mạnh nhất, crosstalk (tỷ lệ bình phương theo h_g*h_l) tăng nhanh hơn tín hiệu khóa (chỉ tỷ lệ bậc 1) -- nên crosstalk có thể CHI PHỐI nhiễu chính xác lúc liên kết mạnh nhất, phản trực giác thông thường",
   "Crosstalk luôn không đáng kể bất kể độ mạnh của liên kết",
   "Crosstalk chỉ xuất hiện khi liên kết yếu",
   "Crosstalk không liên quan gì đến độ mạnh của liên kết, chỉ phụ thuộc khoảng cách vệ tinh"],
  "Đây là một kết luận phản trực giác quan trọng của thiết kế SIKD: sau khi sửa hệ số, crosstalk có thể dao động từ 0.5 đến hàng trăm lần nhiễu nhiệt tùy elevation -- 'nhiễu nhiệt chi phối' chỉ đúng ở một vùng góc ngưỡng hẹp.")

Q(p2, g,
  "Nếu hệ số cách ly (isolation, tính theo dB) giữa hai kênh điều chế được CẢI THIỆN (isolation lớn hơn), phương sai crosstalk thay đổi thế nào?",
  ["Giảm, vì phương sai crosstalk tỷ lệ với 10^(-Isolation/10) -- isolation càng lớn (cách ly tốt hơn) thì crosstalk càng nhỏ",
   "Tăng, vì isolation lớn hơn nghĩa là hai kênh gần nhau hơn",
   "Không đổi vì isolation chỉ ảnh hưởng kênh dữ liệu",
   "Crosstalk trở thành số âm"],
  "Đây là đòn bẩy thiết kế phần cứng (bộ lọc RF, tách tần số sóng mang phụ xa nhau hơn) để giảm trực tiếp nhiễu xuyên âm mà không cần đổi công suất phát hay độ sâu điều chế.")

g = "Ngưỡng quyết định & xác suất sift"
Q(p2, g,
  "Trong luật quyết định ngưỡng kép (dual-threshold), mẫu tín hiệu thu rơi vào 'vùng bảo vệ' giữa hai ngưỡng d0 và d1 sẽ được xử lý như thế nào?",
  ["Bị LOẠI BỎ (không tính vào bit sift) -- chỉ mẫu vượt hẳn một trong hai ngưỡng mới được giữ lại để xác định bit 0 hay 1",
   "Được gán ngẫu nhiên thành bit 0 hoặc 1",
   "Được coi mặc định là bit 1",
   "Gây lỗi hệ thống và dừng toàn bộ phiên truyền"],
  "Vùng bảo vệ giữa d0 và d1 loại bỏ các mẫu mơ hồ (gần mức 0 vi phân) -- đây là cơ chế giảm lỗi (QBER) chính của luật quyết định ngưỡng kép, đánh đổi bằng giảm tỷ lệ bit được giữ lại (P_sift).")

Q(p2, g,
  "Nếu hệ số mở rộng ngưỡng (zeta_scale) được tăng lên, điều gì xảy ra đồng thời với QBER và xác suất sift (P_sift)?",
  ["QBER giảm (ít lỗi hơn vì vùng bảo vệ rộng hơn loại bỏ nhiều mẫu mơ hồ) NHƯNG P_sift cũng giảm (nhiều mẫu bị loại bỏ hơn) -- đây là đánh đổi kinh điển giữa tốc độ và độ chính xác (yield-vs-error)",
   "Cả hai đều tăng cùng lúc",
   "Cả hai đều giảm cùng lúc",
   "QBER tăng nhưng P_sift không đổi"],
  "Đây là nguyên tắc thiết kế trung tâm của luật ngưỡng kép: không thể giảm QBER mà không trả giá bằng giảm lượng bit hữu ích (P_sift), cần chọn zeta_scale cân bằng phù hợp.")

Q(p2, g,
  "Biên độ tín hiệu khóa danh định (không fading) i_mean = 0.5*R_e*G_k*P_T*m_K*h_g*h_l tỷ lệ TUYẾN TÍNH với độ sâu điều chế khóa m_K. Nếu tăng m_K lên 3 lần (ví dụ 0.05 -> 0.15), điều gì xảy ra với tỷ lệ tín-trên-nhiễu của kênh khóa (giữ nguyên công suất nhiễu)?",
  ["Tỷ lệ tín-trên-nhiễu tăng gần 3 lần, giúp QBER giảm mạnh vì tín hiệu khóa mạnh hơn hẳn so với mức nhiễu nền",
   "Tỷ lệ tín-trên-nhiễu không đổi vì nhiễu cũng tăng theo cùng tỷ lệ",
   "Tỷ lệ tín-trên-nhiễu giảm vì tăng m_K làm tăng crosstalk nhiều hơn tín hiệu",
   "Không có ảnh hưởng gì đến QBER, chỉ ảnh hưởng tốc độ dữ liệu"],
  "Đây là một trong hai lý do chính khiến một phiên bản thiết kế với m_K=0.15 (thay vì 0.05) đạt QBER dưới 0.02% thay vì trên 10% -- tăng độ sâu điều chế khóa là đòn bẩy mạnh để cải thiện độ tin cậy kênh khóa.")

Q(p2, g,
  "Vì sao việc tính xác suất tách sóng (P00, P11, P10, P01) qua fading log-normal cần dùng phép cầu phương Gauss-Hermite thay vì tính tích phân trực tiếp?",
  ["Vì biến fading trong không gian log là Gaussian, và phép thế h_a=exp(2X) biến tích phân trung bình thành dạng chuẩn của Gauss-Hermite -- phương pháp này tính CHÍNH XÁC (không xấp xỉ) cho đa thức bậc thấp, sai số rất nhỏ với số điểm vừa đủ",
   "Vì tích phân trực tiếp luôn cho kết quả sai",
   "Vì Gauss-Hermite là phương pháp duy nhất máy tính hỗ trợ",
   "Vì fading không phải là một biến ngẫu nhiên nên không thể tích phân thông thường"],
  "Đây là một lựa chọn toán học có chủ đích: với số điểm cầu phương vừa đủ (ví dụ 20 điểm), sai số thực tế có thể dưới 10^-6 trong chế độ nhiễu loạn yếu -- đủ chính xác cho tính QBER đáng tin cậy.")

g = "Tốc độ khóa bí mật (SKR)"
Q(p2, g,
  "Công thức SKR (dạng cơ bản, Shor-Preskill/GLLP) trừ đi hai số hạng H2(QBER) và chi_E. Ý nghĩa vật lý của hai số hạng này là gì?",
  ["H2(QBER) (điều chỉnh bởi hệ số hiệu chỉnh lỗi f_EC) là thông tin bị rò rỉ qua quá trình đồng bộ/sửa lỗi công khai (reconciliation); chi_E là thông tin tối đa kẻ nghe lén có thể biết được (thường bằng 0 ở điều kiện cơ sở, không nghe lén)",
   "Cả hai số hạng đều là nhiễu vật lý của kênh quang",
   "H2(QBER) là công suất phát, chi_E là công suất thu",
   "Hai số hạng này chỉ mang tính trang trí, không ảnh hưởng kết quả"],
  "SKR = P_sift*[1 - (1+f_EC)*H2(QBER) - chi_E]: đây là công thức bảo mật theo lý thuyết thông tin, trừ đi TOÀN BỘ thông tin rò rỉ (cả do quá trình sửa lỗi lẫn do kẻ nghe lén tiềm năng) trước khi còn lại là khóa bí mật thực sự.")

Q(p2, g,
  "Vì sao công thức SKR PHẢI bao gồm số hạng rò rỉ do hiệu chỉnh lỗi (error-correction leak, f_EC*H2(QBER)), kể cả khi không có kẻ nghe lén (chi_E=0)?",
  ["Vì Alice và Bob vẫn phải chạy quá trình đồng bộ (reconciliation) trên kênh công khai để thống nhất chuỗi bit, và quá trình này tự nó đã làm lộ một lượng thông tin nhất định cho bất kỳ ai nghe được kênh công khai đó (giới hạn Slepian-Wolf)",
   "Vì nếu không có số hạng này, SKR sẽ luôn bằng 0",
   "Vì đây chỉ là một hệ số an toàn thêm vào cho chắc, không có ý nghĩa vật lý cụ thể",
   "Vì f_EC chỉ cần thiết khi QBER bằng 0"],
  "Thiếu số hạng này, công thức chỉ đạt SKR=0 tại QBER=50% -- mâu thuẫn với kết luận vật lý chuẩn là SKR phải về 0 ngay tại ngưỡng BB84 (~11%). Thêm đúng số hạng này khôi phục đúng kết luận vật lý.")

Q(p2, g,
  "Với f_EC=1 (giả định hiệu chỉnh lỗi hoàn hảo, 100%) và chi_E=0, công thức SKR rút gọn thành SKR_norm = P_sift*[1 - 2*H2(QBER)]. Tại QBER = 11% (ngưỡng BB84), hàm entropy nhị phân H2(0.11) xấp xỉ 0.4999. SKR_norm lúc này xấp xỉ bao nhiêu?",
  ["Xấp xỉ 0 (vì 1 - 2*0.4999 = 0.0002 ~ 0), đúng như kỳ vọng lý thuyết: SKR phải triệt tiêu đúng tại ngưỡng lỗi BB84",
   "Xấp xỉ 0.5, vì entropy tối đa là 0.5",
   "Xấp xỉ 1, vì P_sift luôn gần 1",
   "Âm vô cùng, hệ thống bị lỗi toán học"],
  "Đây là một phép kiểm tra hợp lý (sanity check) quan trọng: công thức đúng phải cho SKR về 0 chính xác tại ngưỡng QBER 11% mà lý thuyết BB84 đã biết trước -- nếu không khớp, công thức đang sai ở đâu đó.")

Q(p2, g,
  "Nếu QBER thực tế của một liên kết rất thấp (ví dụ dưới 0.02%, gần như không lỗi), SKR_norm sẽ gần với giá trị tối đa nào, và tại sao?",
  ["Gần bằng 1 (hầu như toàn bộ bit sifted đều trở thành khóa bí mật), vì H2(QBER) gần 0 khi QBER gần 0, nên 1 - 2*H2(QBER) gần 1",
   "Vẫn bằng 0 bất kể QBER thấp đến đâu",
   "Bằng 0.5, giá trị cố định cho mọi trường hợp",
   "Âm, vì công thức không ổn định ở QBER thấp"],
  "Đây là lý do một liên kết được thiết kế tốt (elevation cao, khẩu độ đủ lớn, m_K đủ sâu) có thể đạt SKR tới hàng chục Mbps: gần như toàn bộ dòng bit sift được chuyển thành khóa bí mật khi QBER cực thấp.")

Q(p2, g,
  "SKR tuyệt đối tính bằng bit-trên-giây (SKR_bps) được suy ra từ SKR chuẩn hóa (SKR_norm, không đơn vị, trong khoảng 0-1) bằng cách nào?",
  ["Nhân SKR_norm với tốc độ bit thô của kênh (R_b): SKR_bps = SKR_norm * R_b",
   "Chia SKR_norm cho R_b",
   "SKR_bps luôn bằng SKR_norm nhân với 10^9 cố định",
   "Không có liên hệ toán học, phải đo trực tiếp"],
  "SKR_norm là 'tỷ lệ hiệu quả' (bao nhiêu phần trăm bit thô trở thành khóa), còn SKR_bps là thông lượng khóa thực tế -- phải nhân với tốc độ bit R_b để ra đơn vị vật lý (Mbps).")

g = "Kênh dữ liệu cổ điển (BER)"
Q(p2, g,
  "Tỷ lệ lỗi bit (BER) của kênh dữ liệu cổ điển được tính qua hàm Q (hàm lỗi bổ sung) áp dụng lên tỷ số biên độ tín hiệu trên nhiễu A0/sigma_N,D. Nếu nhiễu tại máy thu dữ liệu sigma_N,D tăng lên (ví dụ do crosstalk NGƯỢC từ kênh khóa), BER thay đổi thế nào?",
  ["BER tăng, vì tỷ số tín hiệu-trên-nhiễu giảm khi mẫu số (sigma_N,D) tăng, làm giá trị hàm Q tăng theo",
   "BER giảm vì nhiễu giúp 'làm mịn' tín hiệu",
   "BER không đổi vì BER chỉ phụ thuộc biên độ tín hiệu, không phụ thuộc nhiễu",
   "BER luôn bằng 0 nếu tín hiệu đủ mạnh, bất kể nhiễu"],
  "Đây là ví dụ cụ thể của tương tác hai chiều trong SIKD: nhiễu xuyên âm 'ngược' (key->data, thường nhỏ vì m_K << m_D) vẫn đóng góp vào nhiễu tổng của máy thu dữ liệu, ảnh hưởng trực tiếp BER của kênh cổ điển.")

Q(p2, g,
  "Vì sao nhiễu của máy thu dữ liệu (sigma_N,D) cần tính CẢ crosstalk ngược từ kênh khóa (tỷ lệ m_K^2), dù m_K thường nhỏ hơn nhiều so với m_D?",
  ["Vì trong một hệ thống SIKD, cả hai kênh đều chia sẻ chung một photodetector nên luôn có crosstalk hai chiều -- bỏ qua chiều nhỏ hơn vẫn có thể gây sai lệch hệ thống nếu độ sâu điều chế khóa (m_K) được tăng lên để cải thiện QBER (như đã thảo luận ở các mục trước)",
   "Vì crosstalk ngược luôn lớn hơn crosstalk thuận",
   "Vì kênh dữ liệu không bao giờ bị ảnh hưởng bởi kênh khóa trong thực tế",
   "Chỉ để cho công thức đối xứng về mặt toán học, không có ý nghĩa thực tế"],
  "Đây là minh chứng rõ nhất cho 'căng thẳng thiết kế trung tâm' của SIKD: tăng m_K (để cải thiện kênh khóa) không miễn phí, nó làm tăng nhiễu lên chính kênh dữ liệu -- cả hai kênh phải được tối ưu CÙNG LÚC, không tách rời.")

Q(p2, g,
  "Trong thiết kế tổng thể máy thu SIKD, nếu kỹ sư chỉ tối ưu riêng kênh khóa (giảm QBER bằng cách tăng m_K tối đa) mà không xét đến ảnh hưởng lên kênh dữ liệu, hậu quả có thể là gì?",
  ["Thông lượng/BER của kênh dữ liệu cổ điển có thể xấu đi đáng kể do crosstalk ngược tăng theo m_K^2, dù kênh khóa đạt hiệu năng rất tốt",
   "Không có hậu quả gì vì hai kênh hoàn toàn độc lập",
   "Kênh dữ liệu sẽ tự động được cải thiện theo",
   "Chỉ ảnh hưởng đến độ trễ (latency), không ảnh hưởng BER"],
  "Đây chính là lý do bài toán power-split (phân bổ m_K và m_D) phải được giải như MỘT bài toán tối ưu đa mục tiêu (Pareto), không thể tối ưu từng kênh riêng lẻ rồi ghép lại.")

Q(p2, g,
  "Giả sử một liên kết có P_sift = 0.9 và QBER = 0.001 (0.1%). Ước lượng thô: SKR_norm áp dụng f_EC=1, chi_E=0 sẽ gần giá trị nào nhất (H2(0.001) rất nhỏ, xấp xỉ 0.011)?",
  ["Xấp xỉ P_sift * (1 - 2*0.011) = 0.9 * 0.978 ~ 0.88 -- gần 88% bit sifted trở thành khóa bí mật",
   "Xấp xỉ 0, vì QBER khác 0 luôn làm SKR về 0",
   "Xấp xỉ 1.0 đúng tuyệt đối, không có hao hụt nào",
   "Xấp xỉ 0.5, giá trị trung bình mặc định"],
  "Ví dụ minh họa cách áp dụng đầy đủ công thức SKR: P_sift đạt trần hiệu quả tối đa, còn số hạng H2(QBER) trừ đi một lượng nhỏ phản ánh chi phí hiệu chỉnh lỗi -- kết quả vẫn gần như toàn bộ P_sift khi QBER rất thấp.")

Q(p2, g,
  "Nếu một liên kết có P_sift rất cao (gần 1, hầu hết mẫu đều vượt ngưỡng) NHƯNG QBER cũng cao (gần 11%), SKR_norm sẽ thế nào?",
  ["SKR_norm vẫn gần 0, vì số hạng H2(QBER) gần 0.5 làm triệt tiêu gần hết thông tin dôi dư bất kể P_sift lớn -- P_sift cao không cứu được SKR nếu QBER quá gần ngưỡng",
   "SKR_norm sẽ luôn cao vì P_sift quyết định hoàn toàn, QBER không quan trọng",
   "SKR_norm bằng trung bình cộng của P_sift và (1-QBER)",
   "Không thể xảy ra đồng thời P_sift cao và QBER cao trong thực tế"],
  "Đây là điểm quan trọng để tránh nhầm lẫn: P_sift (lượng bit qua được ngưỡng) và chất lượng bit (QBER) là hai trục ĐỘC LẬP -- một hệ thống có thể sift nhiều bit nhưng vẫn không an toàn nếu chất lượng bit kém.")

Q(p2, g,
  "So sánh hai biện pháp cải thiện SKR: (a) tăng zeta_scale (ngưỡng rộng hơn) và (b) tăng m_K (điều chế khóa sâu hơn). Điểm khác biệt cơ bản giữa hai biện pháp này về mặt đánh đổi là gì?",
  ["(a) đánh đổi P_sift lấy QBER thấp hơn (giảm lượng bit nhưng sạch hơn); (b) tăng trực tiếp tỷ lệ tín-nhiễu của tín hiệu khóa (cải thiện cả hai) nhưng làm tăng crosstalk lên kênh dữ liệu -- hai cơ chế đánh đổi khác hẳn nhau",
   "Cả hai đều hoàn toàn giống nhau về tác động",
   "(a) không có bất kỳ đánh đổi nào",
   "(b) chỉ ảnh hưởng tốc độ, không ảnh hưởng QBER"],
  "Hiểu rõ cơ chế đánh đổi của từng tham số giúp kỹ sư chọn đúng 'đòn bẩy' phù hợp với mục tiêu thiết kế cụ thể (ưu tiên độ tin cậy khóa, hay ưu tiên thông lượng dữ liệu, hay cân bằng cả hai).")

g = "Băng thông, tốc độ bit và ứng dụng số"
Q(p2, g,
  "Băng thông nhiễu delta_f trong công thức shot noise và thermal noise thường được đặt bằng một nửa tốc độ bit R_b (delta_f = R_b/2). Cơ sở kỹ thuật của lựa chọn này là gì?",
  ["Theo tiêu chí Nyquist, băng thông tối thiểu cần thiết để truyền tín hiệu số ở tốc độ R_b mà không gây nhiễu liên ký tự (ISI) là R_b/2 (băng gốc) -- đây là băng thông 'vừa đủ' cho máy thu, không lãng phí thu thêm nhiễu ngoài băng cần thiết",
   "R_b/2 là một quy ước tùy ý không có cơ sở kỹ thuật",
   "Băng thông luôn phải bằng chính xác R_b, không có phép chia đôi",
   "Đây là yêu cầu bắt buộc của luật viễn thông quốc tế"],
  "Chọn đúng băng thông máy thu (khớp Nyquist) là nguyên tắc thiết kế cơ bản: băng thông rộng hơn cần thiết chỉ thu thêm nhiễu (mọi loại nhiễu đều tỷ lệ với delta_f) mà không cải thiện khả năng giải mã tín hiệu.")

Q(p2, g,
  "Nếu tốc độ bit R_b tăng gấp đôi (giữ nguyên mọi tham số khác), băng thông nhiễu delta_f tăng gấp đôi theo. Điều này ảnh hưởng đồng thời đến tín hiệu và nhiễu như thế nào, dẫn đến hệ quả gì cho QBER?",
  ["Nhiễu (shot, thermal, crosstalk) đều tỷ lệ với delta_f nên tăng theo R_b, trong khi biên độ tín hiệu i_mean không đổi -- tỷ số tín hiệu/nhiễu giảm khi tăng tốc độ bit, nên QBER có xu hướng XẤU ĐI khi chạy hệ thống nhanh hơn",
   "Tín hiệu và nhiễu đều không đổi khi tăng R_b",
   "Chỉ tín hiệu tăng theo R_b, nhiễu không đổi, nên QBER luôn cải thiện khi tăng tốc độ",
   "R_b không có bất kỳ ảnh hưởng nào đến QBER"],
  "Đây là một đánh đổi cơ bản trong thiết kế hệ thống truyền thông: tăng tốc độ bit không miễn phí -- nó đòi hỏi băng thông nhiễu rộng hơn, làm giảm tỷ số tín hiệu/nhiễu và có thể làm xấu QBER nếu không bù bằng công suất/khẩu độ lớn hơn.")

Q(p2, g,
  "Độ nhạy quang điện (responsivity) R_e (đơn vị A/W, ví dụ 0.9 A/W cho InGaAs PIN) xuất hiện trong hầu hết công thức nhiễu và tín hiệu. Vai trò vật lý của R_e là gì?",
  ["Hệ số chuyển đổi từ công suất quang (W) sang dòng điện (A) tại photodetector -- một photodiode có R_e cao chuyển đổi hiệu quả hơn cùng một lượng ánh sáng thành tín hiệu điện lớn hơn",
   "Hệ số suy hao của sợi quang trước máy thu",
   "Hệ số khuếch đại của bộ khuếch đại điện sau photodetector",
   "Nhiệt độ hoạt động tối ưu của photodetector"],
  "R_e là thông số phần cứng cơ bản của cảm biến quang: chọn loại photodetector có R_e cao (ví dụ InGaAs PIN cho vùng 1550nm) trực tiếp cải thiện biên độ tín hiệu thu được mà không cần thay đổi công suất phát.")

Q(p2, g,
  "Vì sao dùng photodiode InGaAs PIN (thay vì Silicon PIN thông thường) là lựa chọn phù hợp cho máy thu hoạt động ở bước sóng 1550nm?",
  ["Vì độ nhạy quang điện của Silicon giảm mạnh (gần như bằng 0) ở bước sóng trên khoảng 1100nm, trong khi InGaAs có độ nhạy tốt trong dải 1000-1700nm bao gồm 1550nm -- lựa chọn vật liệu bán dẫn phải khớp với bước sóng hoạt động",
   "InGaAs luôn rẻ hơn Silicon nên được ưu tiên vì lý do chi phí",
   "Không có sự khác biệt nào giữa hai loại vật liệu ở bất kỳ bước sóng nào",
   "Silicon PIN hoạt động tốt hơn ở 1550nm nhưng InGaAs được chọn vì lý do khác"],
  "Đây là kiến thức nền tảng về vật lý bán dẫn quang điện: độ rộng vùng cấm (bandgap) của vật liệu quyết định dải bước sóng mà nó có thể hấp thụ hiệu quả -- một lựa chọn phần cứng phải khớp với bước sóng hệ thống.")

Q(p2, g,
  "Hệ số khuếch đại G_k (cho kênh khóa) và G_d (cho kênh dữ liệu) trong công thức biên độ tín hiệu đóng vai trò gì, và tại sao chúng thường được đặt riêng biệt (không nhất thiết bằng nhau)?",
  ["Đại diện cho độ khuếch đại điện tử SAU tách sóng quang của từng nhánh thu (mạch khóa và mạch dữ liệu là hai đường xử lý riêng biệt sau khi tách sóng), có thể tối ưu độc lập tùy yêu cầu từng kênh",
   "G_k và G_d luôn phải bằng nhau theo định nghĩa toán học",
   "Chúng đại diện cho công suất phát của laser, không liên quan đến máy thu",
   "Chỉ một trong hai hệ số này thực sự tồn tại trong hệ thống thực"],
  "Tách riêng độ khuếch đại cho từng nhánh xử lý (sau khi đã tách kênh bằng bộ lọc RF) là một bậc tự do thiết kế bổ sung, cho phép tối ưu độc lập độ nhạy của từng máy thu con.")

Q(p2, g,
  "Giả sử một hệ thống có QBER = 5% (giữa mức cực thấp và ngưỡng 11%). Nhìn vào xu hướng hàm entropy nhị phân H2(Q), SKR_norm tại QBER=5% (với f_EC=1) nằm trong khoảng nào so với hai trường hợp cực trị (QBER~0 cho SKR gần 1, QBER=11% cho SKR gần 0)?",
  ["Nằm giữa hai cực trị nhưng lệch gần về phía cao hơn (SKR_norm dương đáng kể, không phải chính giữa 0.5) vì H2(Q) là hàm lồi tăng nhanh dần theo QBER, nên ở QBER thấp-trung bình, SKR vẫn còn khá tốt",
   "Luôn đúng bằng 0.5 do QBER nằm giữa khoảng 0-11%",
   "Bằng 0 vì QBER khác 0",
   "Bằng 1 vì QBER dưới ngưỡng 11%"],
  "Hiểu tính chất phi tuyến (lồi) của hàm entropy nhị phân giúp tránh suy diễn tuyến tính sai lầm: SKR không giảm đều đặn theo QBER mà giảm nhanh dần khi QBER tiến gần ngưỡng 11%.")

Q(p2, g,
  "Nếu hệ số hiệu chỉnh lỗi thực tế f_EC < 1 (hiệu chỉnh lỗi hiệu quả hơn giả định 100%, ví dụ f_EC=0.9), SKR_norm thay đổi thế nào so với giả định f_EC=1?",
  ["SKR_norm CAO HƠN, vì số hạng rò rỉ (1+f_EC)*H2(QBER) nhỏ hơn khi f_EC nhỏ hơn -- một thuật toán hiệu chỉnh lỗi hiệu quả hơn (rò rỉ ít thông tin hơn) trực tiếp làm tăng khóa bí mật thu được",
   "SKR_norm không đổi vì f_EC không xuất hiện trong công thức SKR",
   "SKR_norm thấp hơn vì f_EC nhỏ hơn luôn bất lợi",
   "SKR_norm bằng 0 bất kể giá trị f_EC"],
  "Đây là lý do nghiên cứu và cải tiến thuật toán hiệu chỉnh lỗi (error-correction code) hiệu quả hơn là một hướng cải thiện SKR hoàn toàn độc lập với việc cải thiện phần cứng quang học -- một đòn bẩy ở tầng xử lý tín hiệu số.")

Q(p2, g,
  "Trong bảng tra cứu, QBER thực tế của hệ thống ở điều kiện tốt nằm dưới 0.02% trong khi ngưỡng lý thuyết BB84 là 11%. Khoảng cách rất lớn này (QBER thực tế thấp hơn ngưỡng khoảng 500 lần) có ý nghĩa gì về 'dư địa an toàn' (margin) của hệ thống?",
  ["Hệ thống có dư địa an toàn rất lớn trước ngưỡng sụp đổ bảo mật -- ngay cả khi điều kiện thực tế (nhiễu, suy hao) xấu đi đáng kể so với kịch bản tính toán, hệ thống vẫn khó chạm ngưỡng 11% để mất khả năng tạo khóa",
   "Khoảng cách này không có ý nghĩa thực tế nào, chỉ là một con số toán học",
   "Hệ thống đang hoạt động quá an toàn nên nên giảm QBER thấp hơn nữa bằng mọi giá",
   "QBER thấp hơn ngưỡng nghĩa là hệ thống chưa đạt hiệu năng tối đa và cần điều chỉnh ngay"],
  "Đánh giá dư địa an toàn (margin) là một phần quan trọng của phân tích thiết kế: một hệ thống có QBER gần sát ngưỡng rất dễ bị 'sập' bảo mật khi điều kiện thực tế xấu đi nhẹ, trong khi dư địa lớn cho phép hệ thống chịu được biến động thực tế.")

Q(p2, g,
  "So sánh QBER v3 tại elevation 90 độ (<0.001%) và tại elevation 30 độ (0.019%) cho thấy QBER tăng theo cấp số nhân khi elevation giảm dù vẫn ở mức rất thấp tuyệt đối. Nguyên nhân gốc rễ của xu hướng này là gì (liên kết ngược lại chuỗi nhân quả hình học đã học)?",
  ["Elevation thấp làm slant range dài hơn, khiến h_g và h_l đều xấu đi, làm giảm biên độ tín hiệu khóa i_mean (tỷ lệ với h_g*h_l), từ đó giảm tỷ số tín hiệu/nhiễu và tăng QBER -- toàn bộ chuỗi nhân quả bắt nguồn từ hình học",
   "QBER tăng do nhiệt độ máy thu thay đổi theo elevation",
   "QBER không thực sự phụ thuộc elevation, đây chỉ là nhiễu thống kê",
   "Elevation chỉ ảnh hưởng đến kênh dữ liệu, không ảnh hưởng kênh khóa"],
  "Đây là minh chứng cho việc các lớp mô hình (hình học -> kênh vật lý -> hiệu năng máy thu) liên kết chặt chẽ với nhau: một thay đổi ở lớp hình học (elevation) lan truyền qua toàn bộ chuỗi tính toán để ảnh hưởng chỉ số cuối cùng (QBER).")

Q(p2, g,
  "Nếu công suất phát P_T tăng gấp đôi (giữ nguyên mọi tham số khác), tín hiệu khóa i_mean (tỷ lệ tuyến tính với P_T) tăng gấp đôi, nhưng nhiễu crosstalk sigma_CT^2 (tỷ lệ với P_T^2) tăng gấp 4 lần. Ảnh hưởng ròng lên tỷ số tín hiệu/nhiễu do riêng crosstalk là gì?",
  ["Tỷ số tín hiệu/nhiễu-crosstalk XẤU ĐI (giảm) khi tăng công suất phát, vì nhiễu tăng nhanh hơn tín hiệu (bậc 2 so với bậc 1) -- tăng công suất không phải lúc nào cũng có lợi nếu crosstalk chi phối",
   "Tỷ số tín hiệu/nhiễu cải thiện vì cả hai đều tăng",
   "Tỷ số tín hiệu/nhiễu không đổi vì cả tín hiệu và nhiễu đều tăng theo P_T",
   "Công suất phát không ảnh hưởng đến crosstalk trong bất kỳ trường hợp nào"],
  "Đây là một kết luận thiết kế tinh tế: trong chế độ mà crosstalk chi phối (elevation cao), đơn giản tăng công suất phát KHÔNG cải thiện hiệu năng mà có thể làm XẤU ĐI -- cần giải pháp khác (cải thiện isolation, giảm m_D) thay vì chỉ tăng công suất.")

g = "Ứng dụng thiết kế máy thu tổng hợp"
Q(p2, g,
  "Một kỹ sư đề xuất giảm nhiệt độ hoạt động của máy thu (làm mát chủ động) để cải thiện hiệu năng. Thành phần nhiễu nào trong bốn thành phần đã học sẽ được cải thiện trực tiếp bởi biện pháp này?",
  ["Nhiễu nhiệt (sigma_thermal^2 = 4*k_B*T/R_L*delta_f) giảm trực tiếp khi nhiệt độ T giảm -- đây là biện pháp phần cứng kinh điển để cải thiện độ nhạy máy thu trong các ứng dụng đòi hỏi hiệu năng cao (ví dụ máy thu thiên văn/viễn thông chuyên dụng)",
   "Nhiễu shot sẽ giảm vì nó cũng phụ thuộc nhiệt độ",
   "Nhiễu xuyên âm (crosstalk) sẽ biến mất hoàn toàn khi làm mát",
   "Không có thành phần nhiễu nào bị ảnh hưởng bởi nhiệt độ máy thu"],
  "Đây là ứng dụng trực tiếp công thức nhiễu nhiệt: làm mát máy thu (ví dụ dùng phần tử Peltier hoặc làm mát criogenic) là một biện pháp thực tế phổ biến để giảm sàn nhiễu, dù đánh đổi bằng độ phức tạp/năng lượng hệ thống.")

Q(p2, g,
  "So sánh hai biện pháp cải thiện QBER: (a) làm mát máy thu để giảm nhiễu nhiệt, và (b) tăng m_K để tăng biên độ tín hiệu khóa. Trong chế độ mà crosstalk (không phải nhiệt) đang chi phối nhiễu tổng, biện pháp nào có khả năng hiệu quả hơn?",
  ["Biện pháp (b) hiệu quả hơn trong chế độ crosstalk chi phối, vì làm mát máy thu chỉ giảm nhiễu nhiệt (một thành phần không chi phối trong trường hợp này), trong khi tăng m_K trực tiếp cải thiện tỷ số tín hiệu/nhiễu tổng thể bất kể nguồn nhiễu nào đang chi phối",
   "Biện pháp (a) luôn hiệu quả hơn trong mọi trường hợp bất kể nguồn nhiễu chi phối",
   "Cả hai biện pháp đều không có tác dụng gì trong chế độ crosstalk chi phối",
   "Hai biện pháp có hiệu quả như nhau trong mọi trường hợp"],
  "Đây là một ví dụ áp dụng kiến thức đã học (crosstalk có thể chi phối nhiễu ở elevation cao) vào quyết định kỹ thuật: biết ĐÚNG nguồn nhiễu nào đang chi phối giúp chọn đúng biện pháp cải thiện, tránh đầu tư vào giải pháp không hiệu quả (làm mát tốn kém nhưng không giải quyết đúng vấn đề).")

Q(p2, g,
  "Nếu một hệ thống SIKD được thiết kế lại để dùng HAI photodetector RIÊNG BIỆT (một cho kênh khóa, một cho kênh dữ liệu, tách bằng bộ chia chùm quang trước khi tách sóng) thay vì một photodetector chung, crosstalk sẽ thay đổi thế nào?",
  ["Crosstalk điện tử (do chia sẻ chung photodetector) sẽ giảm đáng kể hoặc biến mất, NHƯNG đổi lại phải chia đôi năng lượng quang thu được (mỗi photodetector chỉ nhận một phần), làm giảm tín hiệu của cả hai kênh, và tăng độ phức tạp/chi phí phần cứng (hai photodetector, bộ chia chùm)",
   "Crosstalk sẽ tăng lên nếu dùng hai photodetector riêng biệt",
   "Không có sự khác biệt nào giữa dùng một hay hai photodetector",
   "Dùng hai photodetector sẽ tự động tăng gấp đôi cả tín hiệu và giảm nhiễu"],
  "Đây là một đánh đổi kiến trúc thay thế đáng để cân nhắc: loại bỏ crosstalk bằng phần cứng có cái giá của nó (chia sẻ năng lượng, phức tạp hệ thống) -- không có giải pháp 'miễn phí', mọi lựa chọn thiết kế đều có đánh đổi.")

Q(p2, g,
  "Trong công thức tính QBER và SKR đã học, giả định 'không nghe lén' (chi_E=0) được dùng làm ĐƯỜNG CƠ SỞ (baseline). Nếu một kịch bản thực tế có ke nghe lén thực sự tồn tại và trích được một phần thông tin (chi_E > 0), SKR thực tế sẽ so với đường cơ sở như thế nào?",
  ["SKR thực tế sẽ THẤP HƠN đường cơ sở (chi_E=0), vì số hạng chi_E được trừ trực tiếp trong công thức SKR -- đường cơ sở luôn là giá trị TỐI ĐA có thể đạt được, mọi tình huống có nghe lén thực sự đều cho SKR thấp hơn hoặc bằng",
   "SKR thực tế sẽ luôn cao hơn đường cơ sở khi có nghe lén",
   "SKR không bị ảnh hưởng bởi sự hiện diện của kẻ nghe lén",
   "Đường cơ sở (chi_E=0) không có ý nghĩa thực tế nào"],
  "Đây là ý nghĩa của việc trình bày kết quả 'đường cơ sở, không nghe lén': các con số SKR công bố (44-65 Mbps ở các elevation khác nhau) là GIỚI HẠN TRÊN lý tưởng -- một đánh giá bảo mật hoàn chỉnh cần phân tích thêm các kịch bản tấn công cụ thể (chi_E > 0) để biết SKR thực tế đảm bảo trong điều kiện bị đe dọa.")

Q(p2, g,
  "Nếu hai hệ thống có cùng QBER nhưng khác P_sift (một hệ thống P_sift=0.5, hệ thống kia P_sift=0.9), hệ thống nào cho SKR_bps (tốc độ khóa tuyệt đối) cao hơn, giả sử cùng R_b?",
  ["Hệ thống có P_sift=0.9 cho SKR_bps cao hơn, vì SKR = P_sift*[1-(1+f_EC)*H2(QBER)-chi_E]*R_b -- P_sift là hệ số nhân trực tiếp, P_sift cao hơn (giữ nguyên QBER) luôn cho kết quả cao hơn tương ứng",
   "Cả hai hệ thống cho SKR_bps bằng nhau vì QBER giống nhau",
   "Hệ thống có P_sift=0.5 cho SKR_bps cao hơn",
   "Không thể so sánh nếu không biết thêm thông tin về công suất phát"],
  "Đây là một bài tập áp dụng trực tiếp công thức SKR: P_sift và (1 - hàm của QBER) là hai hệ số NHÂN độc lập, cả hai đều cần cao để đạt SKR tối đa -- cải thiện riêng một trong hai (ví dụ chỉ giảm QBER mà không tăng P_sift) chỉ mang lại lợi ích một phần.")

Q(p2, g,
  "Vì sao thiết kế máy thu SIKD cho vệ tinh (SWaP hạn chế) thường phải chấp nhận đánh đổi (ví dụ QBER hơi cao hơn lý tưởng) thay vì luôn chọn cấu hình cho QBER thấp nhất tuyệt đối có thể?",
  ["Vì các biện pháp giảm QBER tối đa (khẩu độ lớn hơn, làm mát sâu, hai photodetector riêng biệt) đều tốn thêm khối lượng/năng lượng/không gian trên vệ tinh -- tài nguyên SWaP luôn giới hạn nên thiết kế thực tế phải tìm điểm cân bằng 'đủ tốt' thay vì tối ưu tuyệt đối một chỉ số duy nhất",
   "QBER thấp nhất luôn là lựa chọn miễn phí không có đánh đổi nào",
   "Vệ tinh không có bất kỳ giới hạn tài nguyên nào so với hệ thống mặt đất",
   "Không có mối liên hệ nào giữa QBER và tài nguyên vệ tinh"],
  "Đây là một chủ đề xuyên suốt của kỹ thuật không gian: mọi cải tiến hiệu năng (dù là quang học, điện tử, hay thuật toán) đều cạnh tranh với ngân sách SWaP (Size, Weight, and Power) hữu hạn của vệ tinh -- thiết kế tốt là tìm điểm tối ưu tổng thể, không phải tối ưu một chỉ số đơn lẻ bằng mọi giá.")

Q(p2, g,
  "Nếu một máy thu được thiết kế với biên an toàn QBER rất lớn (QBER thiết kế mục tiêu chỉ 1% so với ngưỡng sập 11%), nhưng thực tế vận hành luôn đo được QBER dưới 0.02% (thấp hơn nhiều so với mục tiêu thiết kế), điều này gợi ý gì về khả năng TỐI ƯU HÓA THÊM của hệ thống?",
  ["Hệ thống có thể đang 'quá thiết kế' (over-engineered) cho kênh khóa -- có thể tái phân bổ một phần tài nguyên (ví dụ giảm nhẹ m_K, dùng công suất dư ra tăng m_D) để cải thiện thông lượng dữ liệu mà vẫn giữ QBER trong biên an toàn hợp lý",
   "Không thể tối ưu hóa thêm gì, cấu hình hiện tại là duy nhất khả thi",
   "Cần ngay lập tức tăng thêm QBER mục tiêu lên gần ngưỡng 11% để tận dụng tối đa",
   "QBER thấp hơn mục tiêu luôn là dấu hiệu của lỗi đo đạc"],
  "Đây là một ứng dụng thực tế của tư duy tối ưu đa mục tiêu (đã học ở phần power-split): một hệ số an toàn (margin) quá lớn ở một chỉ số có thể là cơ hội để tái cân bằng tài nguyên sang chỉ số khác đang cần cải thiện hơn.")

Q(p2, g,
  "Trong một buổi bảo vệ đồ án, nếu hội đồng hỏi 'Tại sao không đơn giản dùng ngưỡng đơn (single threshold) thay vì ngưỡng kép, cho đơn giản hơn?', câu trả lời hợp lý nhất dựa trên kiến thức đã học là gì?",
  ["Ngưỡng đơn không có 'vùng bảo vệ' để loại bỏ các mẫu mơ hồ gần điểm quyết định, nên sẽ có QBER cao hơn đáng kể ở cùng điều kiện nhiễu -- ngưỡng kép đánh đổi một phần P_sift (loại bỏ một số mẫu) để đổi lấy QBER thấp hơn nhiều, một đánh đổi hợp lý khi bảo mật (QBER thấp) quan trọng hơn tốc độ tuyệt đối",
   "Ngưỡng đơn và ngưỡng kép luôn cho kết quả giống hệt nhau về QBER",
   "Ngưỡng kép chỉ là một lựa chọn thẩm mỹ, không có lý do kỹ thuật",
   "Ngưỡng đơn luôn tốt hơn ngưỡng kép trong mọi trường hợp không có ngoại lệ"],
  "Đây là câu hỏi tổng hợp kiểm tra khả năng giải thích LÝ DO thiết kế (không chỉ nhớ công thức) -- một kỹ năng quan trọng khi trình bày và bảo vệ các lựa chọn kỹ thuật trước hội đồng chuyên môn.")

# ============================================================================
# P3 -- Thoi tiet thuc & kha dung
# ============================================================================
p3 = P(3, "Thống kê thời tiết thực & độ khả dụng liên kết")

g = "Mô hình ba trạng thái"
Q(p3, g,
  "Mô hình thời tiết ba trạng thái (clear/rain/cloud) cho một cặp (thành phố, tháng) được xây dựng từ hai xác suất cơ bản nào?",
  ["Xác suất có mây dày đặc (P_cloud, từ dữ liệu quan trắc mây) và tỷ lệ giờ có mưa (f_rain, từ dữ liệu quan trắc mưa) -- từ hai con số này suy ra ba xác suất trạng thái còn lại",
   "Chỉ từ nhiệt độ trung bình và độ ẩm",
   "Chỉ từ dữ liệu dự báo thời tiết 24 giờ tới",
   "Từ áp suất khí quyển và tốc độ gió bề mặt"],
  "p_rain = min(f_rain, 1-P_cloud); p_clear = max(0, 1-P_cloud-p_rain); p_cloud = P_cloud -- cả ba xác suất cộng lại đúng bằng 1, đảm bảo tính nhất quán.")

Q(p3, g,
  "Trong mô hình ba trạng thái, trạng thái 'mây' (cloud) đóng góp bao nhiêu vào SKR hiệu dụng (SKR_eff)?",
  ["Đóng góp bằng 0 -- khi mây dày đặc, liên kết quang được coi là TẮT hoàn toàn (không truyền được khóa)",
   "Đóng góp bằng đúng một nửa SKR trạng thái trời quang",
   "Đóng góp phụ thuộc độ dày của mây, tính theo một hàm suy giảm liên tục",
   "Đóng góp bằng SKR trạng thái mưa"],
  "SKR_eff = p_clear*SKR_clear + p_rain*SKR_rain (không có số hạng cho p_cloud) -- đây là đơn giản hóa hợp lý vì mây dày đặc thường chặn hoàn toàn liên kết quang ở bước sóng 1550nm.")

g = "Độ khả dụng"
Q(p3, g,
  "Độ khả dụng A (metric chính thức của hệ thống) được định nghĩa là A = p_clear + p_rain = 1 - P_cloud. Tại sao A KHÔNG phụ thuộc vào f_rain (tỷ lệ giờ có mưa)?",
  ["Vì p_clear và p_rain cùng nhau chiếm toàn bộ phần 'không mây' (1-P_cloud); dù f_rain dịch chuyển tỷ trọng giữa clear và rain, TỔNG của chúng luôn cố định bằng 1-P_cloud",
   "Vì f_rain luôn bằng 0 trong thực tế nên không ảnh hưởng",
   "Vì mưa không bao giờ ảnh hưởng đến liên kết quang",
   "Đó là một xấp xỉ gần đúng, thực ra A có phụ thuộc yếu vào f_rain"],
  "Đây là một kết luận bất ngờ nhưng quan trọng: khả dụng của liên kết quang chỉ phụ thuộc MÂY, không phụ thuộc MƯA -- và nó khiến metric chính vững chãi trước sai số đo đạc f_rain (một tham số khó đo chính xác hơn P_cloud).")

Q(p3, g,
  "Kết luận khí tượng cốt lõi 'mây quyết định khả dụng, không phải mưa' có ý nghĩa thực hành gì khi thiết kế hệ thống FSO cho một khu vực mới?",
  ["Ưu tiên thu thập/dự báo dữ liệu MÂY (cloud cover) chính xác hơn là dữ liệu mưa khi đánh giá địa điểm triển khai trạm mặt đất, vì đây là yếu tố quyết định khả dụng thực sự",
   "Dữ liệu mưa quan trọng hơn dữ liệu mây trong mọi trường hợp",
   "Cả hai loại dữ liệu đều không cần thiết, chỉ cần độ cao vệ tinh",
   "Khả dụng không thể dự đoán trước, chỉ có thể đo thực tế sau khi triển khai"],
  "Đây là một phát hiện có thể hướng dẫn quyết định thực tế: đầu tư vào chất lượng dữ liệu mây (ví dụ trạm quan trắc vệ tinh) mang lại giá trị dự báo cao hơn nhiều so với đầu tư tương đương vào dữ liệu mưa chi tiết.")

Q(p3, g,
  "Nếu một thành phố có P_cloud = 0.893 (tháng có nhiều mây nhất trong năm) và một thành phố khác có P_cloud = 0.035 (tháng ít mây nhất), chênh lệch độ khả dụng A giữa hai trường hợp này lớn cỡ nào?",
  ["Chênh lệch rất lớn, khoảng 9 lần (A ~ 10.7% so với A ~ 96.5%) -- cho thấy biên độ dao động theo mùa/địa điểm có thể cực lớn ngay trong cùng một vùng khí hậu nhiệt đới",
   "Chênh lệch không đáng kể, dưới 10%",
   "Cả hai trường hợp đều cho A xấp xỉ nhau vì cùng vùng nhiệt đới",
   "Không thể tính được A từ P_cloud đơn thuần"],
  "Đây là minh họa rõ ràng mức độ quan trọng của việc chọn ĐÚNG mùa và ĐÚNG địa điểm khi lập kế hoạch liên kết FSO -- cùng một công nghệ có thể có khả dụng từ dưới 11% đến trên 96% tùy thời điểm/vị trí.")

g = "Nguồn dữ liệu và chu kỳ ngày"
Q(p3, g,
  "Vì sao dữ liệu khí hậu tái phân tích (reanalysis, ví dụ ERA5) được ưu tiên hơn dữ liệu dự báo thời tiết ngắn hạn khi xây dựng mô hình xác suất mây/mưa dài hạn cho một hệ thống vệ tinh?",
  ["Vì mô hình xác suất cần dữ liệu LỊCH SỬ nhiều năm (ví dụ 10 năm) để ước lượng đúng phân bố thống kê theo mùa/giờ, thu được từ dữ liệu quá khứ đã được kiểm chứng, không phải dự báo tương lai có độ bất định",
   "Vì dự báo thời tiết ngắn hạn luôn chính xác hơn reanalysis",
   "Vì reanalysis chỉ có sẵn cho một khu vực rất nhỏ",
   "Không có lý do đặc biệt, cả hai loại dữ liệu tương đương nhau"],
  "Bộ dữ liệu khí hậu nhiều năm (climatology) cho phép tính xác suất theo (thành phố, tháng, giờ) ổn định thống kê, phục vụ bài toán lập lịch dài hạn khác hẳn với bài toán dự báo tức thời.")

Q(p3, g,
  "Trong nghiên cứu thực tế, đỉnh mưa thường rơi vào chiều (khoảng 13-17h, do đối lưu nhiệt) trong khi tổng lượng mây lại cao nhất vào bình minh/đêm và thấp nhất vào khoảng 9-12h sáng. Sự LỆCH PHA này dẫn đến kết luận gì về cửa sổ hoạt động tốt nhất cho liên kết FSO?",
  ["Cửa sổ tốt nhất là SÁNG SỚM (khoảng 5-10h, ban ngày), khi mây vừa giảm mà còn chưa đến giờ đỉnh mưa chiều",
   "Cửa sổ tốt nhất luôn là giữa trưa (12h) vì mặt trời lên cao nhất",
   "Không có sự khác biệt về thời điểm trong ngày, mọi giờ đều như nhau",
   "Cửa sổ tốt nhất là ban đêm muộn (sau 22h), khi không còn ảnh hưởng của cả hai yếu tố"],
  "Phát hiện này minh họa giá trị của việc phân tích chu kỳ theo GIỜ (không chỉ theo tháng/mùa) -- nếu chỉ nhìn trung bình ngày sẽ bỏ lỡ cơ hội khai thác cửa sổ 'sáng sớm' có xác suất thời tiết tốt cao hơn hẳn.")

Q(p3, g,
  "Một hệ thống giả định máy thu hoạt động ở điều kiện P_bg=0 (không nền sáng, tức ban đêm) để tính SKR, nhưng kết luận về chu kỳ ngày lại cho thấy cửa sổ thời tiết tốt nhất là ban ngày (sáng sớm). Đây là ví dụ về loại vấn đề gì trong nghiên cứu hệ thống?",
  ["Một giới hạn/mâu thuẫn thiết kế còn mở (open limitation): cần ước lượng lại ảnh hưởng của nền sáng ban ngày lên máy thu trước khi kết luận chắc chắn về tính khả thi của cửa sổ sáng sớm",
   "Không phải vấn đề gì cả vì cả hai giả định luôn đúng đồng thời trong thực tế",
   "Chứng tỏ mô hình thời tiết bị sai và cần làm lại từ đầu",
   "Chỉ ảnh hưởng tới các hệ thống ở vĩ độ cao, không liên quan vùng nhiệt đới"],
  "Đây là một ví dụ tốt về tính trung thực khoa học: một nghiên cứu nghiêm túc PHẢI nêu rõ các giới hạn/mâu thuẫn còn tồn tại (chưa chứng minh được), thay vì ngầm ẩn giả định mọi thứ đều khớp nhau hoàn hảo.")

g = "Thống kê liên thành phố"
Q(p3, g,
  "Khi tính xác suất 'ít nhất một trong N thành phố có trời quang' (joint clear probability) cho mạng lưới đa trạm, tại sao KHÔNG nên giả định các thành phố là độc lập thống kê với nhau?",
  ["Vì trường mây có tương quan không gian thật (các thành phố gần nhau/cùng hệ thời tiết lớn có xu hướng cùng mây hoặc cùng quang một lúc) -- giả định độc lập sẽ PHÓNG ĐẠI quá mức lợi ích của đa dạng hóa vị trí (site-diversity)",
   "Vì số lượng thành phố luôn quá ít để áp dụng lý thuyết xác suất",
   "Vì xác suất độc lập luôn cho kết quả thấp hơn thực tế, không ảnh hưởng gì",
   "Không có sự khác biệt nào giữa giả định độc lập và tính trực tiếp từ dữ liệu"],
  "Đây là một nguyên tắc data-quality quan trọng: trước khi coi các đơn vị quan sát (ngày, thành phố, trạm) là độc lập, phải kiểm tra tương quan/autocorrelation thực tế -- nếu bỏ qua sẽ đánh giá sai (thường là lạc quan quá mức) lợi ích của mạng lưới đa điểm.")

Q(p3, g,
  "Hệ số tương quan Pearson giữa các chuỗi mây trung bình ngày của hai thành phố được dùng để đánh giá điều gì trong thiết kế mạng lưới trạm mặt đất đa điểm?",
  ["Mức độ 'dự phòng lẫn nhau' thực sự giữa hai trạm: tương quan cao nghĩa là khi một trạm có mây thì trạm kia cũng thường có mây, làm giảm lợi ích của việc đặt cả hai trạm (vì chúng không bù trừ cho nhau tốt)",
   "Khoảng cách địa lý chính xác giữa hai thành phố",
   "Tốc độ truyền dữ liệu giữa hai trạm mặt đất",
   "Số lượng vệ tinh nhìn thấy cả hai trạm cùng lúc"],
  "Chọn vị trí trạm có tương quan mây THẤP với nhau (ví dụ khác hệ thời tiết lớn) mang lại lợi ích đa dạng hóa (diversity) thực sự lớn hơn nhiều so với chọn các trạm gần nhau về mặt địa lý nhưng cùng một hệ thời tiết.")

Q(p3, g,
  "Nếu một nghiên cứu báo cáo 'xác suất ít nhất 1/8/28 thành phố có trời quang đồng thời là X%/Y%/Z%' bằng cách tính TRỰC TIẾP từ bản ghi ngày chung (không giả định độc lập), đây là thực hành tốt theo nguyên tắc nào?",
  ["Ưu tiên tính toán từ dữ liệu thực nghiệm trực tiếp hơn là dựa vào giả định lý thuyết đơn giản hóa (như độc lập thống kê) khi hai cách có thể cho kết quả khác biệt đáng kể",
   "Luôn ưu tiên công thức lý thuyết vì dễ tính toán hơn",
   "Không quan trọng, hai cách luôn cho kết quả giống hệt nhau",
   "Chỉ cần tính cho trường hợp 2 thành phố, các trường hợp khác suy diễn tuyến tính"],
  "Đây là ví dụ về kiểm chứng dữ liệu (data-quality auditing): so sánh với các nghiên cứu khác (ví dụ công bố bởi nhóm khác) dùng giả định độc lập giúp phát hiện và giải thích sự khác biệt về phương pháp luận.")

Q(p3, g,
  "Trong bối cảnh một hệ thống liên kết vệ tinh IoT phải chọn giữa hai chiến lược: (a) đặt nhiều trạm mặt đất GẦN nhau để dễ bảo trì, hoặc (b) đặt trạm XA nhau (khác hệ thời tiết) để tăng độ khả dụng tổng thể, phân tích tương quan mây ở trên ủng hộ chiến lược nào về mặt kỹ thuật thuần túy?",
  ["Chiến lược (b): đặt trạm ở các vị trí có tương quan mây thấp giúp tăng thực sự độ khả dụng tổng thể của mạng lưới (giảm khả năng tất cả trạm cùng bị mây cùng lúc)",
   "Chiến lược (a) luôn tốt hơn về mọi mặt vì dễ quản lý",
   "Cả hai chiến lược cho kết quả khả dụng giống hệt nhau",
   "Khoảng cách giữa các trạm không ảnh hưởng đến độ khả dụng tổng thể"],
  "Đây là ứng dụng trực tiếp của phân tích tương quan không gian vào quyết định quy hoạch mạng lưới -- minh họa cách một kết quả thống kê thuần túy dẫn đến khuyến nghị kỹ thuật cụ thể.")

Q(p3, g,
  "Giả sử A(thành phố X, tháng 11) = 10.7% và A(thành phố Y, tháng 2) = 96.5%. Nếu một ứng dụng IoT cần độ khả dụng tối thiểu 50% để đảm bảo hoạt động ổn định, kết luận nào đúng cho cả hai trường hợp này?",
  ["Thành phố Y tháng 2 đạt yêu cầu (96.5% > 50%), nhưng thành phố X tháng 11 KHÔNG đạt yêu cầu (10.7% < 50%) -- cần lịch trình dự phòng hoặc trạm thay thế cho trường hợp này",
   "Cả hai trường hợp đều đạt yêu cầu vì trung bình năm luôn trên 50%",
   "Cả hai trường hợp đều không đạt yêu cầu",
   "Không thể kết luận gì nếu không biết thêm thông tin về mưa"],
  "Đây là ứng dụng thực tế trực tiếp của độ khả dụng theo (thành phố, tháng): các ứng dụng có yêu cầu độ tin cậy cao cần lập lịch theo THÁNG cụ thể, không thể dùng một con số trung bình năm duy nhất cho mọi tháng.")

g = "Ứng dụng dữ liệu khí hậu thực"
Q(p3, g,
  "Nếu một thành phố có độ khả dụng trung bình năm A=60% nhưng dao động từ 15% (tháng mưa nhiều nhất) đến 92% (tháng khô nhất), một kỹ sư lập kế hoạch dịch vụ dựa CHỈ vào con số trung bình năm sẽ mắc sai lầm gì?",
  ["Đánh giá sai khả năng phục vụ liên tục trong các tháng mưa (thực tế chỉ 15%, thấp hơn nhiều so với kỳ vọng dựa trên 60%) -- cần lập kế hoạch theo THÁNG cụ thể (worst-case theo mùa) thay vì chỉ dùng trung bình năm, đặc biệt cho ứng dụng cần độ tin cậy quanh năm",
   "Không có sai lầm nào, trung bình năm luôn đủ thông tin cho mọi mục đích lập kế hoạch",
   "Sai lầm duy nhất là tính toán trung bình năm không chính xác về mặt số học",
   "Trung bình năm luôn đánh giá thấp hơn thực tế, nên an toàn khi dùng"],
  "Đây là một cạm bẫy thống kê phổ biến: chỉ số trung bình che giấu biến động theo mùa, có thể dẫn đến cam kết dịch vụ (SLA) không thực tế nếu không xét kịch bản xấu nhất theo mùa.")

Q(p3, g,
  "Trong hai thành phố có cùng P_cloud trung bình năm nhưng một thành phố có biên độ dao động THEO MÙA lớn (chênh lệch nhiều giữa mùa khô/mưa) còn thành phố kia ổn định quanh năm, thành phố nào dễ lập lịch dịch vụ liên tục hơn?",
  ["Thành phố ổn định quanh năm dễ lập lịch hơn, vì độ khả dụng có thể dự đoán nhất quán mà không cần thiết kế riêng cho từng mùa hay chấp nhận rủi ro cao trong mùa xấu",
   "Thành phố có biên độ dao động lớn luôn dễ lập lịch hơn vì có tháng rất tốt",
   "Không có sự khác biệt nào giữa hai trường hợp nếu trung bình năm bằng nhau",
   "Biên độ dao động theo mùa không liên quan đến việc lập lịch dịch vụ"],
  "Đây là một tiêu chí bổ sung khi so sánh địa điểm triển khai: không chỉ trung bình mà cả ĐỘ ỔN ĐỊNH theo mùa cũng là yếu tố quan trọng cho các ứng dụng cần độ tin cậy dịch vụ nhất quán.")

Q(p3, g,
  "Ngưỡng '85% cloud cover' được dùng làm mốc phân loại 'có mây dày đặc' (chặn liên kết quang). Nếu ngưỡng này được hạ xuống 70% (nghiêm ngặt hơn), độ khả dụng A tính được sẽ thay đổi theo hướng nào?",
  ["A sẽ GIẢM (thấp hơn so với ngưỡng 85%), vì nhiều giờ có mây vừa phải (70-85%) trước đây được tính là 'khả dụng' (trời quang/mưa) nay bị phân loại lại thành 'mây, không khả dụng'",
   "A sẽ TĂNG vì ngưỡng nghiêm ngặt hơn luôn cho kết quả tốt hơn",
   "A không thay đổi vì ngưỡng phân loại không ảnh hưởng đến kết quả cuối cùng",
   "Không thể xác định được hướng thay đổi nếu không có thêm dữ liệu"],
  "Đây là minh họa tầm quan trọng của việc chọn ngưỡng phân loại: cùng một tập dữ liệu mây thô có thể cho ra độ khả dụng khác nhau tùy tiêu chí 'thế nào là mây đủ dày để chặn liên kết' -- ngưỡng này cần được xác định bằng thực nghiệm (đo suy hao thực tế qua các mức độ mây khác nhau), không chọn tùy ý.")

Q(p3, g,
  "Nếu dữ liệu khí hậu chỉ có độ phân giải theo NGÀY (không có độ phân giải theo giờ), phát hiện quan trọng về 'cửa sổ sáng sớm tốt nhất' (do lệch pha giữa đỉnh mây và đỉnh mưa) có còn phát hiện được không?",
  ["Không, phát hiện này CHỈ có thể thấy được với dữ liệu độ phân giải GIỜ -- dữ liệu ngày chỉ cho biết tổng thể một ngày ra sao, che giấu hoàn toàn cấu trúc biến động trong ngày",
   "Có, vì dữ liệu ngày và giờ luôn cho cùng kết quả sau khi tính trung bình",
   "Có, nhưng cần nhân đôi số ngày quan sát để bù độ phân giải",
   "Độ phân giải dữ liệu không ảnh hưởng đến khả năng phát hiện chu kỳ trong ngày"],
  "Đây là một bài học về lựa chọn độ phân giải dữ liệu phù hợp với câu hỏi nghiên cứu: nếu câu hỏi liên quan đến cấu trúc TRONG NGÀY, bắt buộc phải có dữ liệu độ phân giải giờ, dữ liệu ngày sẽ đánh mất hoàn toàn thông tin này.")

Q(p3, g,
  "Một kỹ sư đề xuất bỏ qua hoàn toàn dữ liệu mưa (f_rain) trong mô hình vì 'độ khả dụng A không phụ thuộc f_rain'. Đề xuất này có hợp lý không, xét rằng SKR_eff (không chỉ A) cũng là một chỉ số quan trọng?",
  ["Không hợp lý: dù A không phụ thuộc f_rain, SKR_eff = p_clear*SKR_clear + p_rain*SKR_rain VẪN phụ thuộc f_rain (vì f_rain quyết định tỷ trọng giữa hai trạng thái có SKR khác nhau) -- bỏ dữ liệu mưa sẽ làm mất khả năng ước lượng SKR_eff chính xác dù A vẫn đúng",
   "Hợp lý hoàn toàn, vì mọi chỉ số quan trọng của hệ thống đều không phụ thuộc f_rain",
   "Hợp lý một phần, chỉ cần bỏ dữ liệu mưa cho các tháng mùa khô",
   "Không liên quan, vì SKR_eff không sử dụng bất kỳ dữ liệu thời tiết nào"],
  "Đây là một điểm dễ nhầm lẫn quan trọng: tính BẤT BIẾN của MỘT chỉ số (A) đối với một tham số không có nghĩa là MỌI chỉ số khác cũng bất biến -- cần xét riêng từng chỉ số trước khi quyết định bỏ qua một nguồn dữ liệu.")

Q(p3, g,
  "So sánh hai chiến lược thu thập dữ liệu khí hậu cho một địa điểm mới: (a) 10 năm dữ liệu vệ tinh/tái phân tích độ phân giải giờ, (b) 1 năm dữ liệu trạm mặt đất độ phân giải phút. Ưu điểm chính của từng chiến lược cho bài toán lập lịch dài hạn là gì?",
  ["(a) cho ước lượng xác suất theo mùa/giờ ỔN ĐỊNH THỐNG KÊ hơn (nhiều năm giảm ảnh hưởng của biến động năm-này-năm-khác), trong khi (b) cho độ chi tiết cao hơn trong PHẠM VI THỜI GIAN NGẮN nhưng dễ bị chi phối bởi đặc thù riêng của năm đó (ví dụ El Nino/La Nina)",
   "(b) luôn tốt hơn (a) trong mọi trường hợp vì độ phân giải cao hơn",
   "(a) luôn tốt hơn (b) trong mọi trường hợp vì thời gian dài hơn",
   "Không có sự khác biệt thực sự giữa hai chiến lược"],
  "Đây là một đánh đổi kinh điển giữa ĐỘ DÀI CHUỖI THỜI GIAN (statistical robustness) và ĐỘ PHÂN GIẢI (chi tiết trong ngày) -- lựa chọn phù hợp tùy câu hỏi nghiên cứu cụ thể đang cần trả lời.")

Q(p3, g,
  "Nếu hai tháng liên tiếp (ví dụ tháng 6 và tháng 7) của cùng một thành phố có P_cloud gần như nhau, nhưng dữ liệu chỉ có sẵn đầy đủ cho tháng 6, việc NGOẠI SUY (extrapolate) độ khả dụng của tháng 7 từ tháng 6 có rủi ro gì?",
  ["Rủi ro là giả định 'tháng liền kề luôn giống nhau' có thể sai nếu có sự chuyển đổi mùa/gió mùa xảy ra ngay giữa hai tháng đó -- cần kiểm tra dữ liệu lịch sử của CHÍNH tháng 7 (nếu có) thay vì luôn giả định liên tục trơn tru giữa các tháng",
   "Không có rủi ro nào, các tháng liền kề luôn có thời tiết giống hệt nhau",
   "Rủi ro chỉ tồn tại ở vùng ôn đới, không áp dụng cho vùng nhiệt đới",
   "Ngoại suy giữa hai tháng liền kề luôn chính xác hơn dữ liệu thực đo"],
  "Đây là một cảnh báo phương pháp luận quan trọng khi làm việc với dữ liệu khí hậu thiếu: nội suy/ngoại suy theo thời gian cần thận trọng, đặc biệt quanh các điểm chuyển mùa nơi thời tiết có thể thay đổi nhanh.")

Q(p3, g,
  "Xét về bản chất vật lý, tại sao mây (cloud) có khả năng CHẶN HOÀN TOÀN liên kết quang 1550nm trong khi mưa (rain) chỉ gây suy hao MỘT PHẦN (dù có thể rất lớn, ví dụ ~100dB)?",
  ["Mây bao gồm các giọt nước/tinh thể băng cực nhỏ (kích thước micromet) dày đặc trong một lớp liên tục dày, tán xạ/hấp thụ gần như toàn bộ ánh sáng đi qua; mưa là các giọt lớn hơn rơi thưa hơn trong không gian, chỉ chắn một phần đường đi của tia sáng dù mỗi giọt gây suy hao đáng kể",
   "Mây và mưa có cùng cơ chế vật lý, chỉ khác nhau về tên gọi",
   "Mưa luôn gây suy hao lớn hơn mây trong mọi trường hợp",
   "Mây chỉ ảnh hưởng ban ngày, mưa chỉ ảnh hưởng ban đêm"],
  "Hiểu sự khác biệt cơ chế vật lý (tán xạ Mie dày đặc liên tục vs suy hao do mật độ giọt mưa) giải thích tại sao mô hình toán học xử lý hai hiện tượng này khác nhau (mây: nhị phân bật/tắt; mưa: hệ số suy hao liên tục theo cường độ).")

Q(p3, g,
  "Một nhóm nghiên cứu khác công bố xác suất 'ít nhất 2/8 thành phố quang đãng đồng thời' cao hơn đáng kể so với kết quả tính trực tiếp từ dữ liệu thực trong dự án này. Giải thích khả dĩ nhất cho sự khác biệt là gì?",
  ["Nhóm khác có thể đã giả định các thành phố ĐỘC LẬP thống kê (bỏ qua tương quan mây không gian thực tế), dẫn đến ước lượng lạc quan hơn (phóng đại) xác suất 'ít nhất N thành phố cùng quang đãng' so với tính trực tiếp từ dữ liệu tương quan thực",
   "Nhóm khác chắc chắn dùng dữ liệu chính xác hơn nên kết quả của họ đáng tin hơn",
   "Sự khác biệt chỉ có thể do lỗi tính toán, không có nguyên nhân phương pháp luận nào",
   "Cả hai kết quả đều sai như nhau nên không có gì đáng bàn"],
  "Đây là ví dụ thực hành của nguyên tắc đã học (không giả định độc lập khi có tương quan không gian thật) -- khi so sánh với nghiên cứu khác cho kết quả khác biệt, cần xem xét GIẢ ĐỊNH PHƯƠNG PHÁP LUẬN của từng bên trước khi kết luận bên nào đúng.")

# ============================================================================
# P4 -- Hinh hoc vung phu, kha thi cap tram, pass ve tinh
# ============================================================================
p4 = P(4, "Hình học vùng phủ, khả thi kết nối cặp trạm & pass vệ tinh")

g = "Vùng phủ và slant range"
Q(p4, g,
  "Bán kính vùng phủ mặt đất R_cov = R_E * psi (với psi = arccos[(R_E/(R_E+h))*cos(elevation)] - elevation) phụ thuộc vào hai yếu tố nào?",
  ["Độ cao quỹ đạo h và góc ngưỡng tối thiểu chấp nhận được (elevation mask) -- góc mask càng lớn (yêu cầu vệ tinh càng cao trên đầu) thì vùng phủ càng nhỏ",
   "Chỉ phụ thuộc độ cao quỹ đạo, không liên quan góc ngưỡng",
   "Chỉ phụ thuộc vĩ độ địa lý của trạm mặt đất",
   "Phụ thuộc thời tiết tại thời điểm quan sát"],
  "Đây là công thức hình học thuần túy (không phụ thuộc thời tiết/kênh) xác định 'dấu vết' trên mặt đất mà một vệ tinh có thể phục vụ tại một thời điểm, với ràng buộc góc ngưỡng tối thiểu.")

Q(p4, g,
  "Một báo cáo kỹ thuật ghi nhầm '950km là bán kính vùng phủ mặt đất' ở góc mask 30 độ, trong khi con số này thực ra là SLANT RANGE (khoảng cách nghiêng), còn bán kính vùng phủ thực sự nhỏ hơn nhiều (khoảng 793km). Đây là loại lỗi gì, và vì sao nó quan trọng?",
  ["Nhầm lẫn hai đại lượng hình học khác nhau (khoảng cách dọc theo tia nhìn vs. bán kính hình tròn chiếu xuống mặt đất) -- quan trọng vì bán kính vùng phủ quyết định ngưỡng DUAL/SF (2*R_cov), nếu dùng nhầm số lớn hơn sẽ tính sai rất nhiều cặp thành phố là 'khả thi đồng thời'",
   "Chỉ là lỗi làm tròn số, không ảnh hưởng kết quả đáng kể",
   "Hai đại lượng này luôn bằng nhau trong mọi trường hợp",
   "Đây là lỗi chính tả, không phải lỗi số liệu"],
  "Sửa lỗi này là ví dụ về tầm quan trọng của kiểm tra chu kỳ (cross-check) định nghĩa đại lượng trước khi dùng vào các bước tính toán tiếp theo -- một nhầm lẫn đơn vị/định nghĩa có thể làm sai lệch cả chuỗi kết luận sau đó.")

Q(p4, g,
  "Ngưỡng phân loại DUAL (hai thành phố có thể kết nối ĐỒNG THỜI qua cùng một vệ tinh) là 2*R_cov. Nếu khoảng cách thực tế giữa hai thành phố LỚN HƠN ngưỡng này, kết nối được phân loại là gì và cần cơ chế gì để truyền dữ liệu?",
  ["Phân loại SF (store-and-forward): cần một cơ chế chuyển tiếp qua trung gian (ví dụ vệ tinh mang dữ liệu từ thành phố này sang thành phố kia trong các lần bay khác nhau, hoặc qua nút tin cậy trung gian)",
   "Vẫn là DUAL nhưng với độ trễ lớn hơn",
   "Không thể kết nối được trong bất kỳ trường hợp nào",
   "Tự động chuyển sang kết nối qua cáp quang mặt đất"],
  "Đây là ranh giới hình học cứng (không thuật toán lập lịch nào phá vỡ được): một cặp quá xa sẽ luôn cần cơ chế lưu-và-chuyển-tiếp (SF), dù thuật toán điều phối có thông minh đến đâu.")

Q(p4, g,
  "Công thức Haversine dùng để tính khoảng cách vòng cung lớn (great-circle distance) giữa hai điểm trên bề mặt cầu (ví dụ hai trạm mặt đất) dựa vào những đầu vào nào?",
  ["Vĩ độ và kinh độ của hai điểm -- tính khoảng cách ngắn nhất theo bề mặt cong của Trái Đất, không phải đường thẳng xuyên qua lòng đất",
   "Độ cao của cả hai điểm so với mặt nước biển",
   "Vận tốc quay của Trái Đất",
   "Áp suất khí quyển tại hai điểm"],
  "Đây là công cụ hình học cơ bản để xác định khoảng cách thực tế giữa cặp trạm mặt đất, đầu vào trực tiếp cho bước phân loại DUAL/SF (so sánh với ngưỡng 2*R_cov).")

Q(p4, g,
  "Góc lệch thiên đỉnh (off-nadir angle) eta, xác định bởi sin(eta) = R_E*cos(elevation)/(R_E+h), mô tả điều gì từ góc nhìn của VỆ TINH (không phải trạm mặt đất)?",
  ["Góc lệch của hướng nhìn từ vệ tinh xuống trạm mặt đất so với phương thẳng đứng (nadir, hướng thẳng xuống tâm Trái Đất) -- quan trọng cho thiết kế hệ thống trỏ hướng anten/quang trên vệ tinh",
   "Góc ngưỡng mà trạm mặt đất nhìn lên vệ tinh",
   "Góc nghiêng của mặt phẳng quỹ đạo so với xích đạo",
   "Góc phân kỳ của chùm tia laser"],
  "Trong khi elevation là góc quan sát TỪ MẶT ĐẤT, off-nadir là góc tương ứng nhìn TỪ VỆ TINH -- cả hai mô tả cùng hình học nhưng từ hai góc nhìn khác nhau, cần cho thiết kế hệ thống trỏ hướng ở cả hai đầu.")

g = "Độ trễ chuyển tiếp và tần suất pass"
Q(p4, g,
  "Độ trễ lưu-và-chuyển-tiếp (SF latency) từ thành phố i đến thành phố j được định nghĩa là trung vị (median) của khoảng thời gian giữa lần RISE của cùng một vệ tinh tại j sau lần rise tại i. Vì sao độ trễ này CÓ HƯỚNG (từ i đến j khác từ j đến i)?",
  ["Vì hướng bay của vệ tinh (đang lên/đang xuống) so với vĩ độ của từng thành phố khác nhau tùy thứ tự bay qua, nên thời gian chờ đợi không đối xứng giữa hai chiều",
   "Vì vệ tinh chỉ bay theo một chiều cố định trong toàn bộ sứ mệnh",
   "Vì hai thành phố luôn có cùng một độ trễ theo định nghĩa toán học, không thể khác nhau",
   "Độ trễ này không liên quan gì đến quỹ đạo vệ tinh, chỉ phụ thuộc tốc độ xử lý dữ liệu trên mặt đất"],
  "Đã có trường hợp đo được mức độ bất đối xứng tới ~100 lần cho một cặp thành phố thực tế -- đây là một phát hiện quan trọng: giả định 'đối xứng' (như với phân loại DUAL/SF) không áp dụng được cho độ trễ chuyển tiếp thực tế.")

Q(p4, g,
  "Khi trích xuất 'pass' (một lần vệ tinh bay qua trong tầm nhìn của một trạm, tức elevation >= mask) từ chuỗi dữ liệu quỹ đạo rời rạc theo thời gian (ví dụ bước 30 giây), tại sao cần NỘI SUY (interpolate) thời điểm rise/set thay vì lấy đúng mẫu dữ liệu gần nhất?",
  ["Để tránh sai lệch hệ thống do bước rời rạc của lưới thời gian -- nếu chỉ lấy mẫu gần nhất, thời điểm bắt đầu/kết thúc pass có thể bị lệch tới nửa bước thời gian, tích lũy sai số đáng kể qua nhiều pass",
   "Nội suy không cần thiết, lấy mẫu gần nhất luôn đủ chính xác",
   "Chỉ để làm mượt đồ thị trực quan, không ảnh hưởng kết quả tính toán",
   "Vì dữ liệu quỹ đạo gốc luôn bị thiếu mẫu ngẫu nhiên"],
  "Nội suy tuyến tính giữa hai mẫu kề nhau cho thời điểm rise/set chính xác hơn, quan trọng khi tính các đại lượng phụ thuộc thời lượng pass (ví dụ lượng khóa tích lũy được trong một lần bay qua).")

Q(p4, g,
  "Với 8 trạm mặt đất, tổng số cặp trạm có thể có là C(8,2)=28. Nếu hình học (ở một góc mask cụ thể) phân loại được 14 cặp là DUAL và 14 cặp là SF, kết luận gì rút ra về 'trần' hiệu năng của hệ thống?",
  ["Đây là một RANH GIỚI HÌNH HỌC CỨNG: không có thuật toán lập lịch nào (dù thông minh đến đâu) có thể biến một cặp SF thành DUAL -- muốn cải thiện tỷ lệ này phải thay đổi HẠ TẦNG (thêm trạm, thay đổi quỹ đạo/độ cao vệ tinh), không phải thuật toán",
   "Tỷ lệ này sẽ tự động cải thiện theo thời gian khi vệ tinh di chuyển",
   "Tỷ lệ 50/50 là một sự trùng hợp không có ý nghĩa gì",
   "Thuật toán lập lịch tối ưu có thể chuyển đổi các cặp SF thành DUAL nếu đủ thông minh"],
  "Đây là một kết luận quan trọng về giới hạn cấu trúc của bài toán: nó đặt bối cảnh cho 'tình trạng thiếu khóa' (pair-starvation) ở các phần sau, và nhắc nhở rằng tối ưu thuật toán chỉ cải thiện được trong phạm vi cho phép bởi hình học, không vượt qua được.")

Q(p4, g,
  "Tần suất pass mỗi ngày của một vệ tinh cụ thể qua một trạm mặt đất ở vĩ độ thấp (gần xích đạo) thường NGẮN hơn (thời lượng mỗi pass) so với một trạm ở vĩ độ cao hơn cùng quỹ đạo nghiêng. Giải thích hợp lý nhất cho hiện tượng này là gì?",
  ["Tại vĩ độ gần 'bụng' của quỹ đạo nghiêng (gần góc nghiêng tối đa của quỹ đạo), tốc độ góc chiếu của vệ tinh lên bầu trời tại vị trí quan sát là cao nhất, khiến thời gian vệ tinh nằm trong tầm nhìn ngắn lại",
   "Vì vệ tinh bay chậm hơn khi ở gần xích đạo",
   "Vì bầu khí quyển dày hơn ở xích đạo làm vệ tinh bị che khuất nhanh hơn",
   "Không có sự khác biệt thực sự, chỉ là sai số đo đạc"],
  "Ví dụ thực tế: một pass qua khu vực Đông Nam Á (vĩ độ thấp) có thể chỉ kéo dài khoảng 200 giây, ngắn hơn đáng kể so với các trạm ở vĩ độ cao hơn cùng một quỹ đạo -- ảnh hưởng trực tiếp đến lượng dữ liệu/khóa có thể trao đổi trong một lần bay qua.")

Q(p4, g,
  "Nếu một trạm mặt đất giảm ngưỡng góc mask từ 40 độ xuống 30 độ, điều gì xảy ra đồng thời với vùng phủ (R_cov) và thời gian trung bình mỗi pass, còn đổi lại là gì về mặt chất lượng liên kết?",
  ["Vùng phủ R_cov tăng và thời gian pass tăng (nhiều cơ hội kết nối hơn), nhưng chất lượng liên kết trung bình giảm do có nhiều thời gian hơn ở góc ngưỡng thấp (suy hao lớn hơn, QBER cao hơn) -- đánh đổi giữa SỐ LƯỢNG và CHẤT LƯỢNG cơ hội kết nối",
   "Cả vùng phủ, thời gian pass và chất lượng đều cải thiện đồng thời không đánh đổi",
   "Không có ảnh hưởng gì đến vùng phủ, chỉ ảnh hưởng chất lượng",
   "Giảm mask luôn là lựa chọn tối ưu tuyệt đối trong mọi trường hợp"],
  "Đây là ví dụ cụ thể về đánh đổi coverage-vs-security đã đề cập: mask 40 độ mất khoảng 28% vùng phủ so với mask 30 độ nhưng giữ QBER an toàn hơn -- lựa chọn mask phụ thuộc ưu tiên của ứng dụng cụ thể.")

g = "Ứng dụng thiết kế mạng lưới"
Q(p4, g,
  "Một hệ thống IoT vệ tinh muốn đảm bảo MỌI cặp trong số 8 trạm đều có thể trao đổi dữ liệu (khả thi, dù là DUAL hay SF), điều này có luôn đạt được với bất kỳ số lượng trạm nào không?",
  ["Có, vì ngay cả cặp SF (quá xa để DUAL) vẫn có thể trao đổi qua cơ chế chuyển tiếp lưu-và-chuyển-tiếp, chỉ là độ trễ cao hơn nhiều so với cặp DUAL",
   "Không, các cặp SF hoàn toàn không thể trao đổi dữ liệu dưới bất kỳ hình thức nào",
   "Chỉ các trạm ở cùng một châu lục mới có thể trao đổi dữ liệu",
   "Cần tối thiểu 20 trạm mới đảm bảo mọi cặp đều khả thi"],
  "Điểm quan trọng: 'không DUAL' không có nghĩa là 'không thể kết nối' -- nó chỉ có nghĩa cần có cơ chế thay thế (SF hoặc relay đa chặng qua các vệ tinh khác) với chi phí độ trễ lớn hơn nhiều.")

Q(p4, g,
  "Nếu một nhà thiết kế hệ thống muốn giảm số cặp SF (tăng số cặp DUAL) trong mạng lưới 8 trạm, giải pháp nào PHÙ HỢP nhất dựa trên phân tích hình học ở trên?",
  ["Tăng độ cao quỹ đạo vệ tinh (h lớn hơn) và/hoặc giảm ngưỡng góc mask -- cả hai đều làm tăng R_cov, do đó tăng ngưỡng DUAL (2*R_cov) và biến nhiều cặp SF thành DUAL",
   "Viết lại thuật toán lập lịch thông minh hơn, không cần thay đổi hạ tầng",
   "Tăng công suất phát của từng trạm mặt đất",
   "Giảm số lượng trạm xuống còn 4 trạm"],
  "Đây là ứng dụng trực tiếp của công thức R_cov = R_E*[arccos(...)-elevation]: các tham số hình học (h, elevation mask) là đòn bẩy THẬT sự để thay đổi tỷ lệ DUAL/SF, khác với lớp thuật toán lập lịch chỉ hoạt động TRONG ràng buộc hình học đã có sẵn.")

Q(p4, g,
  "Vì sao các kết quả hình học (R_cov, ngưỡng DUAL, off-nadir) ở đây được gọi là 'tĩnh' (static) trong khi kết quả lập lịch ở các phần sau lại 'động' (thay đổi theo từng bước thời gian)?",
  ["Vì các công thức hình học chỉ phụ thuộc độ cao quỹ đạo và góc mask (thông số THIẾT KẾ cố định của hệ thống), không phụ thuộc trạng thái tức thời (vị trí vệ tinh, thời tiết) tại mỗi thời điểm -- trong khi lập lịch phải quyết định lại liên tục theo từng bước thời gian dựa trên trạng thái đó",
   "Vì các công thức hình học không thể tính bằng máy tính, phải tính tay",
   "Vì lập lịch không liên quan gì đến hình học quỹ đạo",
   "Không có sự khác biệt thực sự giữa 'tĩnh' và 'động' trong ngữ cảnh này"],
  "Phân biệt rõ hai lớp này giúp hiểu tại sao thay đổi hạ tầng (thông số hình học) và thay đổi thuật toán (lớp điều phối động) là hai loại can thiệp hoàn toàn khác nhau, với hiệu quả và chi phí khác nhau.")

g = "Ứng dụng số liệu hình học"
Q(p4, g,
  "Với độ cao quỹ đạo h=550km và góc mask 30 độ, bán kính vùng phủ tính được là khoảng 793km. Nếu độ cao quỹ đạo tăng lên h=1200km (giữ nguyên góc mask 30 độ), R_cov sẽ thay đổi theo hướng nào, và tại sao?",
  ["R_cov TĂNG đáng kể, vì độ cao lớn hơn làm góc psi (bán kính góc nhìn từ tâm Trái Đất) lớn hơn ở cùng một góc ngưỡng tối thiểu -- vệ tinh cao hơn 'nhìn thấy' được một vùng mặt đất rộng hơn",
   "R_cov giảm khi độ cao tăng vì vệ tinh xa hơn nên tín hiệu yếu hơn",
   "R_cov không đổi vì chỉ phụ thuộc góc mask, không phụ thuộc độ cao",
   "R_cov chỉ phụ thuộc vĩ độ trạm mặt đất, không phụ thuộc độ cao quỹ đạo hay góc mask"],
  "Đây là lý do các chòm sao ở quỹ đạo cao hơn (dù cùng loại LEO) có thể phục vụ vùng phủ rộng hơn với ít vệ tinh hơn -- nhưng đổi lại thường có suy hao hình học h_g tệ hơn (slant range dài hơn) như đã học ở phần kênh vật lý.")

Q(p4, g,
  "Nếu ngưỡng DUAL (2*R_cov) tại mask 30 độ là 1587km nhưng khoảng cách thực tế giữa hai thành phố là 1600km (chỉ lớn hơn ngưỡng 13km), thực tế vận hành có luôn phân loại chắc chắn là SF hay có thể còn 'lằn ranh xám'?",
  ["Về mặt hình học tĩnh, đây vẫn là SF (vượt ngưỡng), nhưng gần ranh giới nghĩa là trong một số khoảnh khắc đặc biệt (elevation vừa đủ cao ở cả hai đầu cùng lúc) DUAL có thể xảy ra không thường xuyên -- ranh giới cứng theo lý thuyết trung bình không loại trừ hoàn toàn khả năng biên",
   "Luôn chắc chắn 100% là DUAL vì gần ngưỡng nghĩa là gần đạt được",
   "Không thể xác định được phân loại nếu khoảng cách gần ngưỡng",
   "Ngưỡng DUAL không có ý nghĩa thực tế khi khoảng cách gần biên"],
  "Đây là một điểm tinh tế trong áp dụng ngưỡng lý thuyết vào thực tế vận hành: ngưỡng hình học dựa trên góc mask cố định là một xấp xỉ hợp lý, nhưng biên giới thực tế có thể mờ hơn khi xét chi tiết theo từng thời điểm cụ thể.")

Q(p4, g,
  "Cùng một cặp thành phố có thể được phục vụ bởi NHIỀU vệ tinh khác nhau trong chòm sao (không chỉ một). Điều này ảnh hưởng thế nào đến xác suất tổng thể của việc có ít nhất MỘT lần DUAL trong một ngày, so với chỉ xét MỘT vệ tinh đơn lẻ?",
  ["Xác suất có ít nhất một lần DUAL trong ngày cao hơn nhiều so với xét một vệ tinh đơn lẻ, vì nhiều vệ tinh trong chòm sao tạo ra nhiều 'cơ hội' pass qua cả hai thành phố cùng lúc trong suốt cả ngày",
   "Xác suất không đổi vì chỉ một vệ tinh mới có thể tạo DUAL tại một thời điểm",
   "Có nhiều vệ tinh làm giảm xác suất DUAL vì chúng cạnh tranh lẫn nhau",
   "Số lượng vệ tinh trong chòm sao không liên quan đến tần suất DUAL"],
  "Đây là lý do tại sao phân tích 'khả thi cặp' (DUAL/SF) trong thực tế phải xét TOÀN BỘ chòm sao (nhiều vệ tinh, nhiều mặt phẳng quỹ đạo) chứ không chỉ một vệ tinh đơn lẻ -- càng nhiều vệ tinh, cơ hội DUAL trong ngày càng dày đặc.")

Q(p4, g,
  "So sánh hai kịch bản mask elevation: (a) mask thấp (10 độ, vùng phủ rộng nhưng chất lượng liên kết biến động lớn) và (b) mask cao (50 độ, vùng phủ hẹp nhưng chất lượng liên kết ổn định cao). Ứng dụng nào phù hợp với (a) hơn: giám sát IoT gửi dữ liệu ít nhạy cảm thời gian, hay liên kết cần độ tin cậy tức thời cao?",
  ["Mask thấp (a) phù hợp hơn cho giám sát IoT ít nhạy cảm thời gian: chấp nhận chất lượng biến động (đôi khi kém) để đổi lấy TẦN SUẤT liên lạc cao hơn (nhiều cơ hội pass hơn) -- phù hợp mô hình 'gửi khi có cơ hội, không cần ngay lập tức'",
   "Mask cao (b) luôn phù hợp hơn cho mọi loại ứng dụng IoT không có ngoại lệ",
   "Loại mask không liên quan gì đến loại ứng dụng IoT",
   "Mask thấp chỉ phù hợp cho liên kết cần độ tin cậy tức thời cao nhất"],
  "Đây là một ứng dụng thực hành của đánh đổi coverage-vs-quality vào lựa chọn thiết kế hệ thống cụ thể: hiểu rõ mẫu hình lưu lượng của ứng dụng (real-time vs store-and-forward chấp nhận độ trễ) giúp chọn đúng ngưỡng mask.")

Q(p4, g,
  "Một hệ thống dùng CHUNG một ngưỡng mask cố định cho TẤT CẢ các trạm mặt đất trong mạng lưới, bất kể địa hình xung quanh từng trạm (núi, tòa nhà cao tầng che khuất một phần chân trời). Đây có phải là giả định luôn hợp lý trong triển khai thực tế không?",
  ["Không hoàn toàn hợp lý: mỗi trạm có thể có chướng ngại vật địa phương khác nhau (núi, công trình) làm giới hạn góc nhìn thực tế thấp hơn mask lý thuyết ở một số hướng cụ thể -- triển khai thực tế cần khảo sát địa hình từng trạm, không chỉ áp dụng một con số chung",
   "Hoàn toàn hợp lý vì mọi trạm mặt đất đều có địa hình giống hệt nhau",
   "Chướng ngại vật địa phương không bao giờ ảnh hưởng đến góc nhìn thực tế của trạm",
   "Mask lý thuyết luôn thấp hơn giới hạn thực tế nên luôn an toàn"],
  "Đây là một khoảng cách giữa mô hình lý thuyết (mask đồng nhất) và thực tế triển khai (địa hình riêng từng trạm) -- một dự án nghiêm túc cần bổ sung khảo sát địa hình thực địa (site survey) trước khi tin tưởng hoàn toàn vào con số mask lý thuyết.")

Q(p4, g,
  "Nếu độ trễ SF (store-and-forward) từ thành phố A đến B là 45 phút nhưng từ B đến A là 4500 phút (bất đối xứng ~100 lần như đã đề cập), một ứng dụng cần dữ liệu 2 chiều cân bằng sẽ bị ảnh hưởng thế nào nếu chỉ thiết kế dựa trên độ trễ trung bình 1 chiều?",
  ["Ứng dụng sẽ bị đánh giá SAI nghiêm trọng về độ trễ thực tế của chiều B->A, có thể gây thất bại cho các giao thức yêu cầu phản hồi hai chiều trong khung thời gian hợp lý nếu không thiết kế riêng cho từng hướng",
   "Không có ảnh hưởng gì vì độ trễ trung bình luôn đại diện tốt cho cả hai chiều",
   "Ứng dụng luôn hoạt động tốt hơn dự kiến vì độ trễ trung bình thường được đánh giá cao",
   "Bất đối xứng độ trễ chỉ là vấn đề lý thuyết, không xảy ra trong triển khai thực tế"],
  "Đây là ứng dụng thực tế trực tiếp của việc phát hiện 'độ trễ SF có hướng': thiết kế giao thức truyền thông (đặc biệt các giao thức cần xác nhận/bắt tay hai chiều) phải xét RIÊNG độ trễ từng hướng, không dùng một con số trung bình gộp.")

Q(p4, g,
  "Trong bối cảnh một mạng lưới IoT vệ tinh cho Việt Nam (một quốc gia trải dài theo chiều Bắc-Nam), việc các trạm mặt đất đặt xa nhau theo VĨ ĐỘ (thay vì theo KINH ĐỘ) ảnh hưởng thế nào đến tỷ lệ DUAL/SF so với đặt các trạm gần nhau về vĩ độ nhưng xa về kinh độ?",
  ["Với các quỹ đạo nghiêng thông thường, khoảng cách vĩ độ lớn (Bắc-Nam) thường tương ứng khoảng cách địa lý thực tế lớn hơn thường xuyên chạm ngưỡng SF hơn -- việc lựa chọn hướng trải trạm (Bắc-Nam vs Đông-Tây) ảnh hưởng trực tiếp đến cấu trúc mạng lưới DUAL/SF, cần tính bằng Haversine thực tế chứ không suy diễn từ một chiều đơn lẻ",
   "Hướng trải trạm hoàn toàn không ảnh hưởng gì đến khoảng cách Haversine",
   "Khoảng cách vĩ độ luôn bằng khoảng cách kinh độ ở mọi vị trí trên Trái Đất",
   "DUAL/SF chỉ phụ thuộc số lượng trạm, không phụ thuộc cách bố trí địa lý"],
  "Đây là một ứng dụng thực hành quan trọng cho bối cảnh Việt Nam cụ thể: hình dạng địa lý trải dài Bắc-Nam của đất nước là một yếu tố THIẾT KẾ thực sự cần đưa vào bài toán quy hoạch mạng lưới trạm mặt đất, không phải chi tiết phụ.")

Q(p4, g,
  "So sánh: (a) tăng số lượng vệ tinh trong CÙNG một mặt phẳng quỹ đạo (cùng độ nghiêng, cùng độ cao) và (b) tăng số lượng MẶT PHẲNG quỹ đạo (giữ tổng số vệ tinh không đổi bằng cách phân bố lại). Chiến lược nào có khả năng tăng TẦN SUẤT pass qua một cặp trạm cụ thể tốt hơn?",
  ["(a) tăng số vệ tinh trong cùng mặt phẳng chủ yếu tăng tần suất pass DỌC THEO đúng quỹ đạo đó (lặp lại nhanh hơn cho các trạm nằm gần vệt quỹ đạo), trong khi (b) tăng đa dạng góc tiếp cận (nhiều hướng bay khác nhau) giúp phủ đều hơn cho nhiều cặp trạm ở các vị trí địa lý khác nhau",
   "Cả hai chiến lược luôn cho kết quả giống hệt nhau về tần suất pass",
   "(b) không bao giờ ảnh hưởng đến tần suất pass, chỉ ảnh hưởng đến vùng phủ",
   "Chỉ số lượng vệ tinh TỔNG mới quan trọng, cách phân bố không ảnh hưởng gì"],
  "Đây là kiến thức thiết kế chòm sao cơ bản (constellation design): số mặt phẳng và số vệ tinh/mặt phẳng là hai bậc tự do riêng biệt, mỗi lựa chọn tối ưu cho một mục tiêu vùng phủ khác nhau (tần suất lặp lại vs độ đa dạng góc nhìn).")

Q(p4, g,
  "Vì sao dữ liệu quỹ đạo dùng cho phân tích hình học (elevation, slant range theo thời gian) cần được cập nhật định kỳ (ví dụ TLE mới mỗi vài ngày) thay vì dùng một bộ dữ liệu quỹ đạo cố định mãi mãi?",
  ["Vì quỹ đạo vệ tinh thực tế bị nhiễu loạn dần theo thời gian (do lực cản khí quyển, nhiễu hấp dẫn không đều của Trái Đất, áp suất bức xạ mặt trời) nên tham số quỹ đạo cũ dần trở nên kém chính xác, cần cập nhật để dự đoán vị trí vệ tinh đúng",
   "Quỹ đạo vệ tinh không bao giờ thay đổi sau khi phóng lên, dữ liệu cũ luôn chính xác",
   "Chỉ cần cập nhật một lần duy nhất khi vệ tinh mới được phóng",
   "Việc cập nhật chỉ cần thiết cho vệ tinh địa tĩnh, không cần cho quỹ đạo thấp"],
  "Đây là kiến thức cơ bản về quỹ đạo học thực tế: mọi phân tích dựa trên vị trí vệ tinh (kể cả các công thức hình học tưởng chừng 'tĩnh' như R_cov) cuối cùng vẫn phụ thuộc vào độ chính xác của dữ liệu quỹ đạo đầu vào, cần làm mới định kỳ.")

Q(p4, g,
  "Một cặp trạm được phân loại DUAL theo tiêu chí hình học tĩnh, nhưng trong thực tế lập lịch động, cả hai trạm CÙNG được ghép với MỘT vệ tinh trong CÙNG một pass chỉ xảy ra nếu thuật toán matching (tầng 1) thực sự chọn như vậy. Điều này cho thấy mối quan hệ gì giữa lớp hình học và lớp thuật toán?",
  ["Hình học chỉ xác định TÍNH KHẢ THI (điều kiện cần), còn thuật toán lập lịch quyết định liệu khả năng đó có THỰC SỰ được TẬN DỤNG hay không (điều kiện đủ) -- một cặp DUAL khả thi vẫn có thể không được ghép nếu thuật toán ưu tiên cặp khác cạnh tranh cùng vệ tinh",
   "Hình học và thuật toán hoàn toàn độc lập, không có mối quan hệ điều kiện cần-đủ nào",
   "Một khi đã phân loại DUAL, thuật toán luôn tự động ghép cặp đó thành công",
   "Thuật toán lập lịch có thể thay đổi phân loại DUAL/SF của một cặp trạm"],
  "Đây là một phân biệt khái niệm quan trọng đã xuất hiện xuyên suốt: hình học đặt RANH GIỚI CỨNG (cái gì có thể), thuật toán quyết định TRONG ranh giới đó cái gì THỰC SỰ xảy ra -- hai lớp bổ sung chứ không thay thế nhau.")

g = "Ứng dụng thiết kế mạng lưới (tiếp)"
Q(p4, g,
  "Một mạng lưới IoT vệ tinh dùng chòm sao quỹ đạo cực (polar, độ nghiêng gần 90 độ) thay vì chòm sao nghiêng vừa phải (ví dụ 53 độ như Starlink). Điều này ảnh hưởng thế nào đến vùng phủ ở các vĩ độ CAO (gần cực) so với vùng nhiệt đới?",
  ["Chòm sao quỹ đạo cực cho vùng phủ TỐT HƠN ở vĩ độ cao (gần cực, nơi các quỹ đạo hội tụ và mật độ pass dày hơn), trong khi chòm sao nghiêng vừa phải (như 53 độ) tập trung vùng phủ tốt hơn ở các vĩ độ trung bình-thấp gần đường xích đạo và ôn đới",
   "Cả hai loại quỹ đạo luôn cho vùng phủ giống hệt nhau ở mọi vĩ độ",
   "Quỹ đạo cực chỉ phù hợp cho liên lạc ở vùng xích đạo",
   "Độ nghiêng quỹ đạo không ảnh hưởng gì đến phân bố vùng phủ theo vĩ độ"],
  "Đây là kiến thức thiết kế chòm sao quan trọng khi lựa chọn hạ tầng cho một ứng dụng IoT cụ thể: một mạng lưới phục vụ chủ yếu khu vực nhiệt đới (như Việt Nam) nên ưu tiên độ nghiêng quỹ đạo phù hợp với dải vĩ độ mục tiêu, không nhất thiết chọn quỹ đạo cực.")

Q(p4, g,
  "Nếu một trạm mặt đất mới được đề xuất đặt tại một vị trí có độ cao lớn (ví dụ trên núi, cao hơn mực nước biển đáng kể), điều này có thể ảnh hưởng tích cực đến những yếu tố nào đã học trong phần hình học và khí quyển?",
  ["Có thể cải thiện cả góc mask hiệu dụng (ít bị núi/địa hình xung quanh che khuất chân trời hơn ở một số hướng) VÀ giảm độ dài đường truyền khí quyển L_atm (do một phần khí quyển dày đặc nhất đã ở dưới độ cao trạm), giảm suy hao h_l",
   "Độ cao trạm mặt đất không có bất kỳ ảnh hưởng nào đến hiệu năng liên kết",
   "Độ cao trạm chỉ ảnh hưởng đến chi phí xây dựng, không ảnh hưởng vật lý liên kết",
   "Đặt trạm ở độ cao lớn luôn làm xấu đi mọi chỉ số hiệu năng"],
  "Đây là một ứng dụng tổng hợp kiến thức từ cả phần hình học (Bậc 4) và khí quyển (Bậc 1): các đài quan trắc thiên văn/viễn thông quang học thực tế thường được đặt ở địa điểm cao (núi) chính vì lý do giảm bớt đường truyền qua lớp khí quyển dày đặc gần mặt đất.")

Q(p4, g,
  "Xét một chòm sao có quỹ đạo rất thấp (VLEO, ví dụ dưới 400km) so với LEO điển hình (~550km). Ngoài suy hao khí quyển do lực cản (đã học ở phần khác), độ cao thấp hơn này ảnh hưởng thế nào đến R_cov và tần suất pass?",
  ["R_cov giảm (vùng phủ hẹp hơn ở cùng góc mask) nhưng cần NHIỀU vệ tinh hơn để duy trì vùng phủ liên tục toàn cầu, đồng thời tần suất pass qua một điểm cụ thể có thể thay đổi do chu kỳ quỹ đạo ngắn hơn",
   "R_cov luôn tăng khi độ cao quỹ đạo giảm",
   "Độ cao quỹ đạo không ảnh hưởng gì đến R_cov, chỉ ảnh hưởng suy hao khí quyển RF/FSO",
   "VLEO luôn cho tần suất pass thấp hơn LEO cao hơn trong mọi trường hợp"],
  "Đây là một đánh đổi hạ tầng bổ sung khi cân nhắc VLEO (đã thảo luận độ cao/nhiên liệu ở phần khác của môn học): vùng phủ hẹp hơn đòi hỏi mật độ chòm sao dày hơn, một yếu tố cần cân nhắc cùng với chi phí nhiên liệu duy trì quỹ đạo khi thiết kế hệ thống VLEO.")

Q(p4, g,
  "Nếu hai trạm mặt đất cách nhau đúng bằng ngưỡng DUAL (d = 2*R_cov, biên giới lý thuyết), theo định nghĩa toán học của bài toán, cặp trạm này thuộc phân loại nào?",
  ["DUAL (theo quy tắc d <= 2*R_cov đã nêu, trường hợp bằng vẫn được tính là DUAL) -- đây là quy ước biên (boundary convention) cần thống nhất rõ ràng khi triển khai thuật toán phân loại để tránh mơ hồ ở các trường hợp biên",
   "SF, vì bằng ngưỡng nghĩa là đã vượt quá giới hạn",
   "Không xác định được, cần thêm thông tin",
   "Cả DUAL và SF cùng lúc"],
  "Đây là một chi tiết triển khai thực tế quan trọng: mọi quy tắc phân loại dựa trên ngưỡng cần định nghĩa rõ ràng xử lý trường hợp BẰNG (đẳng thức), để đảm bảo tính nhất quán và có thể tái lập khi cài đặt thuật toán trong hệ thống thực.")

Q(p4, g,
  "Một sinh viên nhầm lẫn cho rằng 'off-nadir angle' và 'elevation angle' là CÙNG MỘT giá trị chỉ khác tên gọi. Cách giải thích rõ ràng nhất để sửa nhầm lẫn này là gì?",
  ["Hai góc này bù nhau theo một quan hệ hình học cụ thể (không phải bằng nhau): elevation đo từ mặt đất lên (90 độ khi vệ tinh ở đỉnh đầu, 0 độ khi ở chân trời), còn off-nadir đo từ vệ tinh xuống theo hướng ngược lại (0 độ khi trạm ở ngay dưới vệ tinh/thiên đỉnh của vệ tinh, tăng dần khi trạm lệch ra xa) -- hai góc liên hệ qua công thức sin(off-nadir) = R_E*cos(elevation)/(R_E+h) chứ không đơn giản là trừ nhau từ 90 độ như trên mặt phẳng",
   "Hai góc này thực sự bằng nhau trong mọi trường hợp, không cần phân biệt",
   "Elevation chỉ dùng cho FSO, off-nadir chỉ dùng cho RF",
   "Off-nadir luôn lớn hơn elevation đúng 90 độ trong mọi tình huống"],
  "Làm rõ sự khác biệt giữa hai góc nhìn từ hai đầu liên kết (mặt đất vs vệ tinh) là một điểm dễ nhầm lẫn quan trọng cần nắm chắc, đặc biệt khi thiết kế hệ thống trỏ hướng cho CẢ HAI đầu của liên kết.")

# ============================================================================
# P5 -- Lap lich hai tang & thuat toan toi uu ghep cap
# ============================================================================
p5 = P(5, "Lập lịch mạng lưới: ghép cặp trạm-vệ tinh & phân bổ khóa hai chiều")

g = "Phát biểu bài toán"
Q(p5, g,
  "Trong bài toán lập lịch hai tầng, tầng 1 (matching, ghép cặp trạm-vệ tinh) có những ràng buộc cơ bản nào?",
  ["Mỗi trạm chỉ được ghép với tối đa MỘT vệ tinh tại một thời điểm, mỗi vệ tinh chỉ được ghép với tối đa MỘT trạm, và chỉ được ghép nếu vệ tinh đó THỰC SỰ nằm trong tầm nhìn của trạm (thỏa mãn điều kiện hình học)",
   "Mỗi trạm có thể ghép với nhiều vệ tinh cùng lúc không giới hạn",
   "Chỉ cần ràng buộc vệ tinh phải nằm trong tầm nhìn, không cần ràng buộc số lượng ghép cặp",
   "Ràng buộc duy nhất là tổng số ghép cặp không vượt quá 100 mỗi ngày"],
  "Đây là một bài toán ghép cặp song phương có điều kiện (bipartite matching) kinh điển: các biến nhị phân x_{g,s}(t) biểu diễn 'trạm g có đang kết nối vệ tinh s tại thời điểm t hay không', với các ràng buộc đảm bảo tính vật lý khả thi.")

Q(p5, g,
  "Hàm mục tiêu của bài toán matching ở mỗi bước thời gian bao gồm trọng số w_{g,s} (thường là SKR hiệu dụng) TRỪ ĐI một chi phí phát sinh khi có handover (chuyển đổi vệ tinh đang phục vụ). Vì sao cần trừ chi phí handover thay vì chỉ tối đa hóa trọng số đơn thuần?",
  ["Vì mỗi lần chuyển sang một vệ tinh mới đòi hỏi thời gian để hệ thống trỏ hướng bắt/khóa lại mục tiêu (acquisition), trong khoảng thời gian đó liên kết không hoạt động hiệu quả -- nếu không tính chi phí này, thuật toán sẽ chuyển đổi liên tục một cách không thực tế",
   "Chi phí handover chỉ là một yếu tố trang trí, không ảnh hưởng kết quả thực tế",
   "Handover luôn có lợi, nên cần KHUYẾN KHÍCH thay vì trừ chi phí",
   "Chi phí handover chỉ áp dụng cho vệ tinh ở quỹ đạo địa tĩnh"],
  "Đây là một bài học thiết kế quan trọng: nếu bỏ qua chi phí handover, thuật toán 'tối ưu' có thể đề xuất chuyển đổi vệ tinh liên tục để lấy trọng số cao nhất tức thời, gây ra tần suất handover phi thực tế (đã có trường hợp tăng tần suất handover lên +678% khi mô hình chi phí bị thiếu).")

Q(p5, g,
  "Tầng 2 (phân bổ khóa cặp trạm, trusted-relay) tính khóa khả dụng cho một cặp trạm (A, B) bằng K_q = min(tổng khóa tích lũy từ phía A, tổng khóa tích lũy từ phía B). Ý nghĩa vật lý của hàm min() này là gì?",
  ["Trong mô hình chuyển tiếp tin cậy (trusted-relay), khóa chỉ dùng được khi CẢ HAI phía đều có đủ khóa -- phía nào ít hơn sẽ là 'nút cổ chai' giới hạn toàn bộ cặp, giống nguyên tắc 'mắt xích yếu nhất'",
   "Hàm min() chỉ là một bước làm tròn số liệu, không có ý nghĩa đặc biệt",
   "Khóa khả dụng luôn bằng tổng của cả hai phía cộng lại",
   "Hàm min() đảm bảo khóa luôn bằng 0"],
  "Đây là một ràng buộc cấu trúc quan trọng: 'trần gain' của bất kỳ cải thiện nào ở một phía sẽ bị giới hạn bởi phía còn lại nếu phía đó không được cải thiện tương ứng -- đây cũng là lý do 'thêm trạm mặt đất' được xác định là đòn bẩy mạnh hơn 'lập lịch khôn hơn'.")

g = "Ba chiến lược lập lịch"
Q(p5, g,
  "Chiến lược lập lịch cơ bản nhất ('sticky', mù thời tiết): mỗi trạm giữ nguyên vệ tinh đang phục vụ cho tới khi nó set (khuất khỏi tầm nhìn), sau đó mới chọn vệ tinh có elevation cao nhất. Nhược điểm chính của chiến lược này là gì?",
  ["Không có sự PHỐI HỢP giữa các trạm: hai trạm có thể độc lập chọn TRÙNG một vệ tinh cùng lúc, dẫn đến xung đột (cả hai đều 'muốn' cùng một vệ tinh nhưng chỉ một trạm được phục vụ thực sự)",
   "Chiến lược này luôn cho kết quả tối ưu tuyệt đối, không có nhược điểm",
   "Chiến lược này không thể triển khai được trong thực tế",
   "Nhược điểm duy nhất là tốc độ tính toán chậm"],
  "Đây là lý do cần thêm một phiên bản 'feasible' của chiến lược cơ bản (giải quyết xung đột bằng ưu tiên elevation cao hơn) để có thể so sánh công bằng với các chiến lược có phối hợp thật sự.")

Q(p5, g,
  "Chiến lược 'weather-aware matching' sử dụng thuật toán Hungarian (linear sum assignment) trên ma trận trọng số âm. Vì sao cần ÉP ràng buộc 'một vệ tinh chỉ phục vụ một trạm' ở đây, trong khi chiến lược cơ bản không ép được điều này?",
  ["Vì thuật toán Hungarian giải bài toán ghép cặp tối ưu TOÀN CỤC (global optimum) trên toàn bộ ma trận cùng lúc, nên có thể đảm bảo ràng buộc một-một một cách chính xác -- khác với chiến lược 'sticky' quyết định độc lập từng trạm một không biết lựa chọn của trạm khác",
   "Ràng buộc này không quan trọng và có thể bỏ qua trong cả hai chiến lược",
   "Thuật toán Hungarian không thể ép bất kỳ ràng buộc nào",
   "Chỉ cần chạy Hungarian nhiều lần là đủ, không cần thiết kế ràng buộc"],
  "Đây chính là cái chiến lược mù-thời-tiết CÒN THIẾU: khả năng phối hợp toàn cục thực sự -- chi phí handover của vệ tinh đang phục vụ được cộng vào trọng số để ưu tiên 'giữ nguyên' khi có thể.")

Q(p5, g,
  "Trong ba biến thể của chiến lược phân bổ khóa cặp trạm (greedy, ILP, maxmin/water-filling), biến thể 'maxmin' ưu tiên giải quyết cho đối tượng nào trước?",
  ["Cặp trạm có khóa khả dụng THẤP NHẤT (tệ nhất) trước tiên -- nguyên tắc water-filling nhằm cải thiện tình trạng của đối tượng yếu nhất trước khi phân bổ thêm cho đối tượng đã mạnh",
   "Cặp trạm có khóa khả dụng CAO NHẤT trước tiên, để tối đa hóa tổng khóa nhanh nhất",
   "Cặp trạm được đăng ký sớm nhất trong hệ thống",
   "Cặp trạm gần trạm trung tâm điều phối nhất"],
  "Nguyên tắc maxmin/water-filling là một chiến lược CÔNG BẰNG (fairness) kinh điển trong phân bổ tài nguyên, ưu tiên nâng cao giá trị tối thiểu thay vì tối đa hóa tổng thể -- phù hợp khi muốn tránh tình trạng một vài cặp quá thiếu khóa.")

Q(p5, g,
  "Vì sao quy tắc greedy cho phân bổ khóa KHÔNG thể dùng tiêu chí đơn giản 'chọn ứng viên có gain trong K_q lớn nhất' ở bước đầu tiên (cold start), mà phải dùng quy tắc 'deficit' (chênh lệch giữa hai phía)?",
  ["Vì K_q = min(sideA, sideB) và ở bước đầu tiên cả hai phía thường đều = 0, nên min(0, x) = 0 với mọi x -- mọi ứng viên đều 'trông vô ích' theo tiêu chí đơn giản, khiến thuật toán loại bỏ NHẦM tất cả ứng viên ngay từ vòng đầu",
   "Quy tắc deficit chỉ là một lựa chọn tùy ý, không có lý do kỹ thuật",
   "Vì tiêu chí gain đơn giản luôn cho kết quả tối ưu hơn",
   "Vì K_q luôn dương ngay từ đầu nên không cần quy tắc đặc biệt"],
  "Đây là một lỗi thực tế từng xảy ra: dùng tiêu chí 'gain<=0 thì loại' đã từng xóa hết mọi ứng viên ở vòng đầu -- sửa bằng quy tắc deficit (ưu tiên phía đang thiếu nhiều nhất) giải quyết đúng bản chất bài toán cold-start.")

g = "Kế toán handover và kết quả thực nghiệm"
Q(p5, g,
  "Một lỗi lập lịch từng phát hiện: chi phí thu nhận (acquisition) 30 giây của handover bị 'kẹp' vào chỉ một đoạn (segment) dữ liệu, trong khi phần lớn (khoảng 91%) các lần handover thực tế TRẢI DÀI qua nhiều đoạn liên tiếp. Hậu quả của lỗi này nếu không sửa là gì?",
  ["Chi phí handover thực tế bị TÍNH THIẾU (ước lượng sai) khoảng 2.7 lần, khiến kết quả so sánh thuật toán trong những điều kiện không công bằng (thuật toán handover nhiều được lợi 'giả' vì chi phí của nó bị hụt)",
   "Lỗi này không ảnh hưởng đến bất kỳ kết quả nào",
   "Lỗi này làm chi phí handover bị tính thừa, không phải thiếu",
   "Lỗi chỉ ảnh hưởng tốc độ chạy chương trình, không ảnh hưởng kết quả"],
  "Sửa lỗi này (cho phép ngân sách 30 giây trải qua nhiều đoạn cùng một vệ tinh) là một ví dụ cụ thể về việc kiểm tra chi tiết triển khai có thể thay đổi đáng kể kết luận so sánh thuật toán.")

Q(p5, g,
  "Một lỗi thứ hai ('phantom key'): khi cùng một cặp (trạm, vệ tinh) xuất hiện nhiều lần trong ngày (nhiều pass khác nhau), một cách tra cứu 'phẳng' (không xét thời gian) có thể nhầm lẫn giữ pass CUỐI CÙNG thay vì pass ĐÚNG. Cách sửa dùng nguyên tắc gì?",
  ["Giải quyết theo 'time-containment': xác định pass đúng bằng cách kiểm tra thời điểm cụ thể có nằm trong khoảng [rise, set] của pass đó hay không, thay vì chỉ tra cứu theo cặp (trạm, vệ tinh) đơn thuần",
   "Chỉ cần luôn lấy pass ĐẦU TIÊN trong ngày thay vì pass cuối",
   "Bỏ qua hoàn toàn các trường hợp trùng (trạm, vệ tinh) xuất hiện nhiều lần",
   "Tăng tần suất lấy mẫu dữ liệu để tránh trùng lặp"],
  "Lỗi này từng gây ra tỷ lệ dữ liệu trùng (~43% khóa bị tính nhầm) trước khi sửa -- đây là ví dụ điển hình về tầm quan trọng của khóa (key) tra cứu đầy đủ thông tin thời gian, không chỉ thông tin danh tính đối tượng.")

Q(p5, g,
  "Kết quả thực nghiệm trên dữ liệu lớn (620 ngày): 'matching gain' (lợi ích của thuật toán phối hợp tốt hơn so với cơ bản) là khoảng +2.5%, nhưng 'weather-info gain' (lợi ích riêng của việc BIẾT thời tiết khi lập lịch) lại là SỐ ÂM nhỏ. Giải thích hợp lý nhất cho kết quả âm này là gì?",
  ["Chiến lược nhận biết thời tiết thực hiện nhiều lần chuyển đổi (re-assign) vệ tinh hơn để bắt kịp điều kiện thời tiết thay đổi, và chi phí handover phát sinh từ đó 'nuốt' gần hết phần lợi ích lý thuyết mà thông tin thời tiết mang lại",
   "Kết quả âm chứng tỏ thông tin thời tiết hoàn toàn vô dụng trong mọi trường hợp",
   "Đây là lỗi tính toán, kết quả đúng phải luôn dương",
   "Kết quả âm chỉ xảy ra trong điều kiện thời tiết mưa, không xảy ra khi trời khô"],
  "Đây là một kết luận quan trọng và PHẢN TRỰC GIÁC: có thêm thông tin (thời tiết) không tự động mang lại lợi ích thực sự nếu chi phí hành động dựa trên thông tin đó (handover) quá lớn -- cần cân nhắc chi phí-lợi ích tổng thể, không chỉ lợi ích lý thuyết đơn thuần.")

Q(p5, g,
  "'Pair-starvation' (tỷ lệ ngày có ít nhất một cặp trạm nhận được 0 khóa) được đo ở mức rất cao (91.6-96.5% số ngày) VÀ hầu như KHÔNG ĐỔI qua mọi vòng sửa lỗi/cải tiến thuật toán. Kết luận chính sách nào phù hợp nhất từ quan sát này?",
  ["Đây là một GIỚI HẠN CẤU TRÚC (do số lượng trạm/cặp quá ít so với nhu cầu), không phải lỗi thuật toán -- đòn bẩy thực sự để cải thiện là THÊM TRẠM MẶT ĐẤT, không phải tiếp tục tối ưu thuật toán lập lịch",
   "Cần tiếp tục cải tiến thuật toán lập lịch vì đây chắc chắn là lỗi thuật toán",
   "Đây là kết quả bình thường, không cần hành động gì thêm",
   "Vấn đề sẽ tự giải quyết khi công nghệ vệ tinh phát triển hơn trong tương lai"],
  "Đây là kết luận trung tâm của toàn bộ nghiên cứu lập lịch: 'đòn bẩy thật = thêm trạm, không phải lập lịch khôn hơn' -- mọi cải tiến thuật toán (matching gain +2.5%) chỉ là cải thiện BIÊN, không phá vỡ được giới hạn cấu trúc do thiếu hạ tầng.")

Q(p5, g,
  "Nếu một nhà quản lý dự án chỉ thấy kết quả 'matching gain +2.47%' mà không đọc thêm phần 'weather-info gain âm' và 'pair-starvation 90%+', kết luận sai lầm họ có thể rút ra là gì?",
  ["Kết luận sai là 'thuật toán lập lịch thông minh đã giải quyết được vấn đề' -- trong khi thực tế vẫn còn một vấn đề cấu trúc lớn (pair-starvation) hoàn toàn chưa được giải quyết bởi bất kỳ cải tiến thuật toán nào",
   "Không có kết luận sai nào có thể rút ra từ một con số duy nhất",
   "Con số +2.47% đã bao hàm đầy đủ mọi thông tin cần thiết",
   "Các con số còn lại chỉ là chi tiết kỹ thuật không quan trọng với quản lý"],
  "Đây là lý do báo cáo kết quả nghiên cứu cần trình bày ĐẦY ĐỦ bộ ba chỉ số (matching gain, weather-info gain, pair-starvation) cùng nhau, thay vì chọn lọc chỉ trưng bày con số 'đẹp' nhất -- tránh dẫn đến quyết định sai lệch về đầu tư tiếp theo.")

Q(p5, g,
  "So sánh 'công bằng' (fair comparison) giữa các thuật toán lập lịch trong nghiên cứu này yêu cầu điều kiện gì phải được GIỮ CỐ ĐỊNH giữa các lần chạy?",
  ["Cùng dữ liệu trạm/vệ tinh, cùng cửa sổ thời gian quan sát, và cùng quy tắc tính chi phí handover (ví dụ 30 giây) -- chỉ thay đổi CHÍNH thuật toán lập lịch đang được so sánh",
   "Không cần giữ cố định gì cả, chỉ cần so sánh con số cuối cùng",
   "Chỉ cần giữ cố định số lượng trạm, các yếu tố khác có thể thay đổi tự do",
   "Cần thay đổi cả dữ liệu lẫn thuật toán để có kết quả đa dạng hơn"],
  "Đây là nguyên tắc thiết kế thực nghiệm cơ bản (kiểm soát biến nhiễu): nếu không giữ cố định các điều kiện nền, sự khác biệt về kết quả có thể đến từ sự khác biệt DỮ LIỆU/CẤU HÌNH thay vì từ chính thuật toán -- làm vô hiệu kết luận so sánh.")

g = "Độ phức tạp tính toán"
Q(p5, g,
  "Trong bài toán lập lịch hai tầng, tại sao tầng 1 (matching) thường được giải bằng thuật toán chính xác (Hungarian, đa thức), trong khi tầng 2 (phân bổ khóa) cần nhiều lựa chọn (greedy/ILP/maxmin) tùy tình huống?",
  ["Matching (ghép cặp song phương đơn giản) có thuật toán đa thức chính xác đã biết (Hungarian); phân bổ khóa có thêm cấu trúc ràng buộc phức tạp hơn (min của hai phía, nhiều đối tượng cạnh tranh) khiến bài toán tối ưu chính xác (ILP) có thể tốn chi phí tính toán cao hơn ở quy mô lớn, nên cần lựa chọn xấp xỉ (greedy/maxmin) khi cần tốc độ",
   "Cả hai tầng đều có thể giải chính xác trong thời gian đa thức như nhau, không có sự khác biệt",
   "Tầng 2 luôn dễ giải hơn tầng 1",
   "Việc chọn thuật toán chỉ là sở thích cá nhân, không có lý do kỹ thuật"],
  "Hiểu rõ độ phức tạp tính toán của từng tầng giúp nhà thiết kế chọn đúng công cụ (chính xác vs xấp xỉ) phù hợp với ràng buộc thời gian tính toán thực tế của hệ thống vận hành.")

g = "Thiết kế trọng số và độ nhạy tham số"
Q(p5, g,
  "Nếu trọng số w_{g,s} trong hàm mục tiêu matching chỉ dùng elevation (thay vì SKR hiệu dụng đầy đủ, đã gồm thời tiết), thuật toán 'weather-aware' có còn xứng đáng với tên gọi đó không?",
  ["Không, vì elevation chỉ phản ánh hình học chứ không phản ánh điều kiện thời tiết thực tế -- 'weather-aware' đòi hỏi trọng số phải bao gồm cả xác suất mây/mưa ảnh hưởng đến SKR thực tế mong đợi, không chỉ hình học thuần túy",
   "Vẫn xứng đáng, vì elevation là yếu tố quan trọng nhất quyết định hiệu năng",
   "Không có sự khác biệt giữa dùng elevation và dùng SKR hiệu dụng đầy đủ",
   "Weather-aware chỉ là một cái tên, không liên quan đến nội dung trọng số thực tế"],
  "Đây là một điểm kiểm tra tính nhất quán quan trọng: một thuật toán được đặt tên 'nhận biết thời tiết' phải THỰC SỰ có thông tin thời tiết trong hàm mục tiêu của nó, nếu không chỉ là 'nhận biết hình học' được đặt tên gây hiểu lầm.")

Q(p5, g,
  "Chi phí handover c_h là một tham số thiết kế (không phải hằng số vật lý cố định). Nếu c_h được đặt QUÁ CAO (so với thực tế 30 giây acquisition), hệ quả cho hành vi thuật toán matching là gì?",
  ["Thuật toán sẽ trở nên quá 'bảo thủ', giữ nguyên vệ tinh cũ ngay cả khi có cơ hội tốt hơn rõ rệt xuất hiện, làm mất đi lợi ích phối hợp mà thuật toán weather-aware lẽ ra mang lại",
   "c_h cao không có ảnh hưởng gì đến hành vi thuật toán",
   "c_h cao luôn cải thiện hiệu năng bất kể giá trị thực tế của acquisition",
   "Chi phí handover chỉ ảnh hưởng đến tốc độ tính toán, không ảnh hưởng quyết định ghép cặp"],
  "Đây là lý do việc HIỆU CHỈNH ĐÚNG tham số chi phí (dựa trên đo đạc thực tế thời gian acquisition) quan trọng không kém việc thiết kế đúng cấu trúc thuật toán -- một tham số sai có thể vô hiệu hóa lợi ích của một thiết kế đúng.")

Q(p5, g,
  "Phân tích độ nhạy (sensitivity analysis) MIP-gap cho thuật toán ILP (phân bổ khóa chính xác) kiểm tra điều gì, và tại sao nó cần thiết cho các bài toán tối ưu quy mô lớn?",
  ["Kiểm tra xem nghiệm tìm được có gần với nghiệm tối ưu tuyệt đối hay không khi thuật toán ILP dừng sớm (do giới hạn thời gian tính toán) thay vì chạy đến hội tụ hoàn toàn -- cần thiết vì ILP có thể tốn thời gian mũ ở quy mô lớn, buộc phải chấp nhận nghiệm 'đủ tốt' trong thời gian thực tế",
   "MIP-gap chỉ liên quan đến độ chính xác số học của máy tính, không liên quan đến chất lượng nghiệm",
   "MIP-gap luôn bằng 0 cho mọi bài toán ILP, không cần kiểm tra",
   "Phân tích độ nhạy chỉ áp dụng cho thuật toán greedy, không áp dụng cho ILP"],
  "Đây là kiến thức thực hành quan trọng khi triển khai tối ưu chính xác (ILP) trong hệ thống vận hành thời gian thực: cần biết giới hạn sai lệch tối đa so với tối ưu tuyệt đối để đánh giá độ tin cậy của quyết định lập lịch.")

Q(p5, g,
  "So sánh thời gian chạy giữa ba chiến lược (greedy, ILP, maxmin) khi quy mô bài toán tăng (nhiều trạm/vệ tinh/cặp hơn). Xu hướng tổng quát nào đúng nhất?",
  ["Greedy thường có thời gian chạy tăng chậm nhất (gần tuyến tính) theo quy mô, trong khi ILP (giải chính xác) có thể tăng nhanh hơn đáng kể ở quy mô lớn -- đây là lý do các hệ thống thời gian thực thường ưu tiên greedy/heuristic khi quy mô lớn, dùng ILP chủ yếu để kiểm chứng chất lượng nghiệm ở quy mô nhỏ",
   "Cả ba chiến lược luôn có thời gian chạy giống hệt nhau bất kể quy mô",
   "ILP luôn nhanh hơn greedy ở mọi quy mô bài toán",
   "Thời gian chạy không liên quan gì đến quy mô bài toán, chỉ phụ thuộc phần cứng máy tính"],
  "Hiểu đánh đổi giữa TỐC ĐỘ và TÍNH TỐI ƯU của từng thuật toán giúp lựa chọn đúng công cụ tùy tình huống: vận hành thời gian thực quy mô lớn (greedy/maxmin) vs phân tích ngoại tuyến kiểm chứng chất lượng (ILP).")

Q(p5, g,
  "Nếu một hệ thống lập lịch chỉ chạy chiến lược greedy (không bao giờ so sánh với ILP để kiểm chứng), rủi ro tiềm ẩn nào có thể không được phát hiện?",
  ["Có thể không biết được khoảng cách thực sự giữa nghiệm greedy và nghiệm tối ưu tuyệt đối -- nếu khoảng cách này lớn, hệ thống đang bỏ lỡ đáng kể tiềm năng hiệu năng mà không hề hay biết, vì không có điểm tham chiếu để so sánh",
   "Không có rủi ro nào, greedy luôn cho nghiệm tối ưu tuyệt đối",
   "Rủi ro chỉ tồn tại nếu hệ thống có ít hơn 10 trạm",
   "ILP không bao giờ cho kết quả khác greedy nên không cần so sánh"],
  "Đây là lý do các nghiên cứu nghiêm túc thường chạy CẢ hai (greedy cho vận hành thực tế, ILP cho kiểm chứng ở quy mô có thể giải được) -- việc chỉ tin vào một phương pháp duy nhất mà không đối chiếu là một rủi ro phương pháp luận.")

Q(p5, g,
  "Nếu 'matching gain' đo được là +2.47% trong điều kiện khô và +2.48% trong điều kiện ướt (gần như giống hệt nhau), điều này gợi ý gì về việc liệu điều kiện thời tiết (khô/ướt) có phải là yếu tố chính chi phối lợi ích của phối hợp thuật toán hay không?",
  ["Gợi ý rằng lợi ích matching KHÔNG phụ thuộc nhiều vào điều kiện thời tiết mùa -- đây là dấu hiệu của một hiệu ứng VỮNG CHẮC (robust), có khả năng phản ánh một đặc tính cấu trúc sâu (ví dụ liên quan đến số lượng trạm/vệ tinh) hơn là một hiện tượng chỉ đúng trong một mùa cụ thể",
   "Gợi ý rằng thời tiết là yếu tố chi phối duy nhất của lợi ích phối hợp",
   "Hai con số gần nhau chỉ là trùng hợp ngẫu nhiên không có ý nghĩa gì",
   "Kết quả này chứng tỏ mô hình thời tiết hoàn toàn không được sử dụng trong tính toán"],
  "Đây là một ứng dụng thực hành của khái niệm 'robustness' đã học: khi một kết quả không đổi qua các điều kiện khác nhau, đó là bằng chứng cho một quy luật cấu trúc sâu hơn là một hiệu ứng ngẫu nhiên phụ thuộc điều kiện cụ thể.")

Q(p5, g,
  "Nếu hệ thống mở rộng từ 8 trạm lên 16 trạm (giữ nguyên số vệ tinh và thuật toán), dự đoán hợp lý nhất về xu hướng của 'pair-starvation' (tỷ lệ ngày có cặp thiếu khóa) là gì, dựa trên kết luận về giới hạn cấu trúc đã học?",
  ["Pair-starvation có khả năng GIẢM đáng kể, vì kết luận trước đó đã xác định 'thêm trạm' (không phải cải tiến thuật toán) mới là đòn bẩy thực sự giải quyết vấn đề này -- tăng gấp đôi số trạm trực tiếp tăng số cơ hội ghép cặp thành công",
   "Pair-starvation sẽ không đổi bất kể số lượng trạm, vì đây là hằng số cố định của hệ thống",
   "Pair-starvation sẽ tăng lên khi có nhiều trạm hơn vì phức tạp hơn",
   "Không thể dự đoán được xu hướng nếu không chạy lại toàn bộ mô phỏng từ đầu"],
  "Đây là ứng dụng trực tiếp của kết luận trung tâm đã học ('đòn bẩy thật = thêm trạm') để đưa ra dự đoán có cơ sở về một thay đổi hạ tầng cụ thể -- một kỹ năng suy luận quan trọng hơn việc chỉ ghi nhớ con số.")

Q(p5, g,
  "Trong một cuộc họp đánh giá dự án, nếu ai đó hỏi 'Tại sao không đơn giản là giao cho AI/machine learning tự học ra lịch tối ưu, thay vì dùng các thuật toán tường minh như Hungarian/greedy?', lập luận hợp lý nhất dựa trên các kết luận đã học ở đây là gì?",
  ["Giới hạn hiệu năng chính đến từ RÀNG BUỘC CẤU TRÚC (hình học, số trạm) chứ không phải từ chất lượng thuật toán ra quyết định -- một mô hình học máy phức tạp hơn cũng bị chặn bởi cùng giới hạn hình học đó (K_q=min(...), DUAL/SF cứng), nên khó có khả năng cải thiện vượt trội so với thuật toán tường minh đã gần tối ưu (Hungarian là chính xác cho tầng 1)",
   "AI/machine learning luôn vượt trội hoàn toàn so với thuật toán tường minh trong mọi bài toán tối ưu",
   "Không có lý do gì để không dùng AI/machine learning, chỉ là do dự án chưa thử",
   "Thuật toán tường minh luôn tốt hơn AI trong mọi trường hợp không có ngoại lệ"],
  "Đây là một ứng dụng tổng hợp then chốt: hiểu đúng NGUỒN GỐC của giới hạn hiệu năng (cấu trúc/hạ tầng, không phải thuật toán) giúp đưa ra quyết định đầu tư đúng đắn, tránh lãng phí nguồn lực vào việc cải tiến thuật toán khi vấn đề thực sự nằm ở tầng khác.")

Q(p5, g,
  "Nếu một thuật toán lập lịch mới được đề xuất và người đề xuất chỉ báo cáo rằng nó 'cho SKR tổng cao hơn 5% so với ALG-0', những câu hỏi bổ sung nào NÊN được đặt ra trước khi chấp nhận đây là một cải tiến thực sự đáng kể (dựa theo khung đánh giá đã học)?",
  ["Có so sánh theo kiểu ghép cặp (paired test) trên cùng dữ liệu không? Chi phí handover có được tính đầy đủ và công bằng không? Pair-starvation có cải thiện tương ứng hay vẫn giữ nguyên mức cấu trúc? Kết quả có vững chắc qua nhiều tham số/mùa không?",
  "Chỉ cần tin vào con số 5% là đủ, không cần đặt thêm câu hỏi nào",
   "Chỉ cần hỏi về tốc độ chạy chương trình của thuật toán mới",
   "Chỉ cần so sánh với một bài báo quốc tế bất kỳ có kết quả tương tự"],
  "Đây là ứng dụng tổng hợp của toàn bộ khung đánh giá khoa học đã xây dựng xuyên suốt phần lập lịch: so sánh công bằng, chi phí đầy đủ, chỉ số toàn diện (không chỉ một con số đẹp), và kiểm tra độ vững chắc -- bốn trụ cột để đánh giá một tuyên bố cải tiến hiệu năng.")

g = "Ứng dụng vận hành mạng lưới (tiếp)"
Q(p5, g,
  "Nếu một trạm mặt đất bị hỏng đột ngột (ngừng hoạt động do bảo trì khẩn cấp), thuật toán matching (tầng 1) cần xử lý tình huống này như thế nào để không làm sập toàn bộ lịch trình?",
  ["Loại trạm hỏng khỏi tập ứng viên hợp lệ cho ma trận ghép cặp (đặt trọng số/khả dụng = 0 hoặc loại hàng/cột tương ứng), để thuật toán tự động phân bổ lại các vệ tinh còn khả dụng cho các trạm còn hoạt động mà không cần thiết kế lại toàn bộ hệ thống",
   "Toàn bộ hệ thống phải dừng hoạt động cho đến khi trạm hỏng được sửa xong",
   "Thuật toán không thể xử lý tình huống trạm hỏng, cần viết lại từ đầu mỗi lần",
   "Trạm hỏng chỉ cần được bỏ qua thủ công bởi người vận hành, thuật toán không cần biết"],
  "Đây là một yêu cầu thiết kế thực tế quan trọng cho vận hành hệ thống: một kiến trúc lập lịch tốt cần có khả năng THÍCH ỨNG với thay đổi trạng thái hạ tầng (trạm hỏng, bảo trì) mà không cần can thiệp thủ công phức tạp mỗi lần.")

Q(p5, g,
  "Trong thực tế vận hành, quyết định lập lịch cho bước thời gian TIẾP THEO thường phải được đưa ra TRƯỚC KHI biết chắc chắn điều kiện thời tiết chính xác tại thời điểm đó (chỉ có dự báo, không phải quan sát thực). Điều này ảnh hưởng thế nào đến khái niệm 'weather-aware' đã học?",
  ["'Weather-aware' trong vận hành thực tế phải dựa trên DỰ BÁO thời tiết (có độ bất định) chứ không phải quan sát hoàn hảo -- sai số dự báo có thể làm giảm lợi ích thực tế so với kịch bản lý tưởng đã phân tích (dùng dữ liệu lịch sử/quan sát chính xác), cần tính thêm yếu tố độ tin cậy dự báo vào đánh giá hiệu năng thực tế",
   "Không có sự khác biệt nào giữa dùng dự báo và dùng dữ liệu quan sát hoàn hảo",
   "Vận hành thực tế luôn có thể biết chính xác thời tiết trước khi cần quyết định",
   "Dự báo thời tiết không có bất kỳ vai trò nào trong lập lịch thực tế"],
  "Đây là một khoảng cách quan trọng giữa PHÂN TÍCH (dùng dữ liệu lịch sử hoàn hảo để đánh giá tiềm năng) và VẬN HÀNH THỰC TẾ (phải quyết định dựa trên dự báo không hoàn hảo) -- một dự án nghiêm túc cần nêu rõ giới hạn này khi chuyển từ nghiên cứu sang triển khai.")

Q(p5, g,
  "Nếu chi phí handover thực tế khác nhau tùy loại vệ tinh (ví dụ vệ tinh mới có hệ thống trỏ hướng nhanh hơn, acquisition chỉ 10 giây thay vì 30 giây), mô hình chi phí handover CỐ ĐỊNH (30 giây cho mọi trường hợp) có còn phù hợp không?",
  ["Không hoàn toàn phù hợp: một chòm sao không đồng nhất (nhiều thế hệ vệ tinh khác nhau) cần mô hình chi phí handover PHỤ THUỘC LOẠI VỆ TINH, vì áp dụng một hằng số chung có thể đánh giá sai lợi ích của việc chuyển sang vệ tinh mới có tốc độ acquisition nhanh hơn",
   "Mô hình cố định luôn chính xác bất kể sự khác biệt phần cứng giữa các vệ tinh",
   "Chi phí handover không bao giờ phụ thuộc vào loại vệ tinh trong thực tế",
   "Chỉ cần dùng giá trị trung bình của mọi loại vệ tinh là đủ chính xác"],
  "Đây là một hướng mở rộng mô hình hợp lý khi hệ thống thực tế có tính không đồng nhất (heterogeneous constellation) -- một điểm cần lưu ý khi áp dụng các kết luận từ mô hình đơn giản hóa (chi phí cố định) vào tình huống phức tạp hơn.")

Q(p5, g,
  "Xét mối quan hệ giữa tầng 1 (matching) và tầng 2 (phân bổ khóa): nếu tầng 1 chọn ghép cặp KHÔNG tối ưu cho tầng 2 (ví dụ ưu tiên SKR cao nhất tức thời mà không xét cân bằng giữa các cặp trạm), điều gì có thể xảy ra ở tầng 2?",
  ["Một số cặp trạm có thể liên tục bị 'bỏ đói' (không bao giờ được ưu tiên ghép nối vì SKR tức thời luôn thấp hơn các lựa chọn khác), làm trầm trọng thêm pair-starvation ở tầng 2 dù tầng 1 đang tối ưu hóa đúng theo tiêu chí riêng của nó",
   "Tầng 2 luôn hoạt động độc lập hoàn toàn không bị ảnh hưởng bởi quyết định của tầng 1",
   "Không có bất kỳ tương tác nào giữa hai tầng trong toàn bộ hệ thống",
   "Tầng 1 luôn tự động tối ưu cho cả tầng 2 mà không cần thiết kế phối hợp gì thêm"],
  "Đây là một nhận thức quan trọng về TÍNH KHÔNG TÁCH RỜI của hai tầng: tối ưu cục bộ ở tầng 1 (theo tiêu chí riêng) không đảm bảo tối ưu toàn cục cho mục tiêu cuối cùng (khóa cân bằng cho mọi cặp) -- đây là một hướng nghiên cứu mở để phối hợp tốt hơn giữa hai tầng thay vì xử lý tuần tự độc lập.")

Q(p5, g,
  "Trong bối cảnh giảng dạy môn 'Các công nghệ truyền thông cho IoT', bài toán lập lịch hai tầng này minh họa nguyên lý tổng quát nào có thể áp dụng cho các hệ thống mạng IoT khác (không chỉ vệ tinh QKD)?",
  ["Nguyên lý phân tầng bài toán tối ưu phức tạp thành các bài toán con dễ giải hơn (matching rồi phân bổ tài nguyên), kết hợp với việc phân biệt RÕ RÀNG giữa giới hạn CẤU TRÚC/HẠ TẦNG (không thể vượt qua bằng thuật toán) và giới hạn THUẬT TOÁN (có thể cải thiện) -- một nguyên lý áp dụng được cho bất kỳ hệ thống mạng IoT nào có ràng buộc tài nguyên (băng thông, thời gian kết nối, năng lượng)",
   "Nguyên lý này chỉ áp dụng riêng cho vệ tinh QKD, không liên quan đến bất kỳ hệ thống IoT nào khác",
   "Không có nguyên lý tổng quát nào có thể rút ra từ bài toán cụ thể này",
   "Nguyên lý duy nhất là luôn dùng thuật toán Hungarian cho mọi bài toán mạng"],
  "Đây là câu hỏi kết nối kiến thức chuyên sâu (SIKD vệ tinh) với bối cảnh rộng hơn của môn học (IoT nói chung): các nguyên lý phân tầng bài toán, phân biệt giới hạn cấu trúc vs thuật toán, và đánh đổi chi phí-lợi ích là những bài học tổng quát có giá trị vượt ra ngoài ứng dụng cụ thể này.")

# ============================================================================
# P6 -- Relay lien-ve-tinh (ISL), toi uu phan chia cong suat, khung thong ke
# ============================================================================
p6 = P(6, "Relay liên-vệ-tinh, tối ưu phân chia công suất & khung kiểm định thống kê")

g = "Relay đa chặng qua liên kết liên-vệ-tinh"
Q(p6, g,
  "Khoảng cách chặng (hop distance) nhỏ nhất trên một đồ thị ISL tĩnh (mesh nối các vệ tinh cùng/kề mặt phẳng quỹ đạo) được tính bằng thuật toán tìm kiếm theo chiều rộng (BFS). Vì sao BFS phù hợp cho bài toán này?",
  ["Vì tất cả các cạnh của đồ thị (mỗi liên kết liên-vệ-tinh) được coi là có 'chi phí' như nhau (một chặng), nên BFS (tìm đường đi ít cạnh nhất) chính là tìm đường đi tối ưu về số chặng -- không cần thuật toán trọng số phức tạp hơn (như Dijkstra)",
   "Vì BFS là thuật toán duy nhất có thể chạy trên máy tính",
   "Vì đồ thị ISL luôn có chu trình nên cần BFS để tránh vòng lặp",
   "BFS không liên quan gì đến bài toán tìm đường đi ngắn nhất"],
  "Chọn đúng thuật toán phù hợp với cấu trúc bài toán (cạnh đồng trọng số) giúp tính toán đơn giản và nhanh hơn nhiều so với áp dụng thuật toán tổng quát hơn không cần thiết.")

Q(p6, g,
  "Chiến lược relay 'time-optimal' chọn điểm giao dữ liệu SỚM NHẤT có thể (dựa vào điều kiện thời điểm rise của vệ tinh đích >= thời điểm nhận + số chặng * 30 giây), trong khi 'capacity-optimal' cho phép trễ hơn (trong ngân sách gấp 3 lần time-optimal) để chọn elevation cao hơn. Mục tiêu khác nhau giữa hai chiến lược này là gì?",
  ["Time-optimal ưu tiên TỐC ĐỘ GIAO (độ trễ thấp nhất), còn capacity-optimal ưu tiên CHẤT LƯỢNG LIÊN KẾT (SKR/khóa cao hơn nhờ elevation tốt hơn), chấp nhận đổi lấy một chút độ trễ",
   "Cả hai chiến lược đều có cùng mục tiêu, chỉ khác tên gọi",
   "Time-optimal luôn cho kết quả tối ưu hơn capacity-optimal trong mọi tình huống",
   "Capacity-optimal không liên quan gì đến elevation"],
  "Đây là một lựa chọn đánh đổi rõ khác (latency-vs-throughput) mà nhà vận hành hệ thống có thể chọn tùy ưu tiên ứng dụng: dữ liệu cần tới khẩn cấp (time-optimal) hay dữ liệu cần tối đa lượng khóa/thông tin (capacity-optimal).")

Q(p6, g,
  "Vì sao 30 giây/chặng trong mô hình relay được gán cho 'xử lý trên trạm' (on-board processing) thay vì thời gian LAN TRUYỀN tín hiệu (propagation) giữa các vệ tinh?",
  ["Vì thời gian lan truyền tín hiệu quang/RF giữa các vệ tinh gần nhau chỉ mất vài mili-giây (không đáng kể), trong khi thời gian xử lý/xác nhận trên trạm (thu, giải mã, chuyển tiếp) mới là yếu tố chi phối độ trễ thực tế của mỗi chặng",
   "Vì 30 giây là thời gian ánh sáng đi hết một vòng Trái Đất",
   "Vì đây là thời gian bắt buộc theo quy định viễn thông quốc tế",
   "Không có lý do vật lý cụ thể, đây chỉ là một số ngẫu nhiên"],
  "Phân biệt đúng nguồn gốc độ trễ (xử lý vs lan truyền) quan trọng để xây dựng mô hình đúng: nếu nhầm lẫn hai loại độ trễ này sẽ dẫn đến ước lượng sai khả năng của hệ thống relay đa chặng.")

Q(p6, g,
  "Relay ISL đa chặng được mô tả là giải pháp thay thế cho SF đơn-chặng (single-hop store-and-forward, có trường hợp mất tới 711 phút cho một cặp thành phố xa). Lợi ích chính của relay đa chặng ở đây là gì?",
  ["Giao dữ liệu GẦN NHƯ TỨC THỜI (thay vì chờ cả vòng quỹ đạo tiếp theo của CÙNG một vệ tinh như SF đơn-chặng) bằng cách chuyển tiếp qua nhiều vệ tinh KHÁC nhau trong mạng lưới ngay lập tức",
   "Giảm chi phí phần cứng của trạm mặt đất",
   "Loại bỏ hoàn toàn nhu cầu về các trạm mặt đất",
   "Tăng độ phân giải ảnh chụp của vệ tinh"],
  "Đây là minh chứng rõ ràng cho kiến trúc 'mesh trên trời': tận dụng kết nối liên-vệ-tinh để biến một trường hợp tồi tệ (711 phút chờ) thành một trường hợp khả thi trong phạm vi giây/phút.")

Q(p6, g,
  "Tại sao đồ thị ISL có thể coi là 'tĩnh' (topology cố định trong tính toán) mặc dù bản thân các vệ tinh đang chuyển động liên tục với tốc độ quỹ đạo rất cao?",
  ["Vì thời gian cần để hoàn thành một chuỗi relay (số chặng * 30 giây) NHỎ HƠN NHIỀU so với chu kỳ quỹ đạo (khoảng 95 phút cho LEO) -- trong khoảng thời gian ngắn đó, cấu trúc láng giềng giữa các vệ tinh (ai kề ai) hầu như không đổi",
   "Vì vệ tinh thực sự đứng yên một chỗ trong không gian",
   "Vì đồ thị ISL được cập nhật lại mỗi giây nên luôn chính xác",
   "Đây chỉ là một xấp xỉ đơn giản hóa không có cơ sở vật lý"],
  "Đây là một biện luận quy mô thời gian (timescale argument) quan trọng: so sánh thời gian đặc trưng của quá trình đang xét (vài chặng, vài phút) với thời gian đặc trưng của hệ thống thay đổi (chu kỳ quỹ đạo, ~95 phút) để biện minh cho giả định đơn giản hóa 'tĩnh'.")

g = "Tối ưu phân chia công suất khóa/dữ liệu"
Q(p6, g,
  "Trong bài toán tối ưu phân chia công suất (power-split) giữa kênh khóa và kênh dữ liệu, crosstalk được mô hình hóa là HAI CHIỀU (cả data->key lẫn key->data). Vì sao chiều key->data (m_K gây nhiễu cho kênh dữ liệu) thường NHỎ HƠN nhiều so với chiều ngược lại?",
  ["Vì độ sâu điều chế khóa m_K thường được thiết kế NHỎ HƠN nhiều so với độ sâu điều chế dữ liệu m_D (ưu tiên dành phần lớn công suất điều chế cho kênh dữ liệu cổ điển), nên năng lượng 'rò rỉ' từ kênh khóa sang kênh dữ liệu tự nhiên cũng nhỏ hơn",
   "Vì kênh khóa luôn được đặt ở một bước sóng hoàn toàn khác kênh dữ liệu",
   "Vì kênh khóa không bao giờ gây nhiễu cho kênh dữ liệu trong bất kỳ trường hợp nào",
   "Vì máy thu dữ liệu có bộ lọc hoàn hảo loại bỏ mọi nhiễu từ kênh khóa"],
  "Sự bất đối xứng này (m_K << m_D trong thiết kế thông thường) giải thích vì sao crosstalk 'ngược' (key->data) thường là yếu tố phụ, trong khi crosstalk 'thuận' (data->key) là yếu tố chính chi phối QBER của kênh khóa.")

Q(p6, g,
  "Ràng buộc m_K + m_D <= 1 trong bài toán phân chia công suất có ý nghĩa vật lý gì?",
  ["Tổng độ sâu điều chế của cả hai kênh không thể vượt quá giới hạn vật lý của bộ điều chế quang (không thể điều chế quá 100% biên độ mang của sóng mang), nên hai kênh phải 'chia sẻ' một ngân sách điều chế chung",
   "Đây chỉ là một quy ước toán học, không có ý nghĩa vật lý cụ thể",
   "Ràng buộc này chỉ áp dụng khi trời có mây",
   "Tổng hai độ sâu điều chế phải luôn bằng chính xác 1"],
  "Đây là cơ sở vật lý của bài toán tối ưu đa mục tiêu: tăng m_D (lợi cho dữ liệu) bắt buộc phải giảm 'không gian' còn lại cho m_K nếu muốn giữ tổng dưới giới hạn vật lý, hoặc chấp nhận crosstalk tăng nếu không giảm.")

Q(p6, g,
  "Đường Pareto (Pareto frontier) trong không gian (SKR, thông lượng dữ liệu) biểu diễn tập hợp những điểm (m_K, m_D) nào?",
  ["Những điểm 'không bị thống trị' (non-dominated): tại đó KHÔNG THỂ cải thiện một chỉ số (ví dụ SKR) mà không làm xấu đi chỉ số còn lại (thông lượng) -- đây là tập hợp các lựa chọn tối ưu thực sự, phân biệt với các lựa chọn 'lãng phí' (có thể cải thiện cả hai đồng thời)",
   "Tất cả các điểm (m_K, m_D) có thể có, không loại trừ điểm nào",
   "Chỉ điểm có SKR tối đa duy nhất",
   "Chỉ điểm có m_K = m_D (chia đều)"],
  "Đường Pareto là công cụ chuẩn để trình bày đánh đổi đa mục tiêu cho người ra quyết định: họ có thể chọn điểm trên đường này phù hợp ưu tiên ứng dụng (ưu tiên bảo mật khóa hay ưu tiên thông lượng dữ liệu) mà không lãng phí tài nguyên công suất.")

Q(p6, g,
  "Chiến lược 'adaptive split' chọn m_K NHỎ NHẤT sao cho vẫn đủ khóa cần thiết (SKR * số kênh * thời gian pass >= K_req). Lợi ích của chiến lược 'tối thiểu cần thiết' này so với chiến lược cố định m_K là gì?",
  ["Dành phần công suất điều chế còn lại (sau khi đủ K_req) cho kênh dữ liệu, tối đa hóa thông lượng dữ liệu MÀ VẪN đảm bảo đủ khóa theo yêu cầu -- thích ứng với từng pass có điều kiện khác nhau (elevation, thời tiết) thay vì một mức cố định cho mọi trường hợp",
   "Chiến lược này luôn cho SKR cao hơn chiến lược cố định trong mọi trường hợp",
   "Chiến lược này không liên quan gì đến thông lượng dữ liệu",
   "m_K luôn được đặt bằng 0 trong chiến lược này"],
  "Đây là một ví dụ về tối ưu hóa THÍCH ỨNG (adaptive) theo điều kiện thực tế của từng pass, thay vì áp dụng một cấu hình 'một cho tất cả' -- tận dụng tối đa tài nguyên công suất điều chế trong từng tình huống cụ thể.")

g = "Khung thống kê và kiểm định"
Q(p6, g,
  "Phương pháp 'full enumeration' (liệt kê toàn bộ, ví dụ 620 ngày dữ liệu thực thay vì lấy mẫu ngẫu nhiên) mang lại lợi thế gì so với phương pháp lấy mẫu (sampling) khi báo cáo giá trị TRUNG BÌNH?",
  ["Không có sai số mẫu (sampling error) ở giá trị trung bình, vì đã tính trên TOÀN BỘ tập dữ liệu có sẵn chứ không phải ước lượng từ một mẫu con",
   "Full enumeration luôn nhanh hơn lấy mẫu về mặt tính toán",
   "Full enumeration chỉ áp dụng được cho dữ liệu giả lập, không áp dụng cho dữ liệu thực",
   "Không có sự khác biệt nào giữa hai phương pháp"],
  "Khi dữ liệu sẵn có đủ đầy đủ (ví dụ toàn bộ lịch sử nhiều năm), tính toán trên TOÀN BỘ thay vì lấy mẫu loại bỏ hoàn toàn một nguồn sai số thống kê -- kết quả trung bình là con số CHÍNH XÁC cho tập dữ liệu đó, không phải ước lượng.")

Q(p6, g,
  "Phương pháp 'paired test' (kiểm định theo cặp, so sánh CÙNG một ngày giữa hai thuật toán, chỉ đổi thuật toán mà giữ nguyên thời tiết/hình học) giúp loại bỏ nguồn sai lệch nào khi phát hiện một hiệu ứng nhỏ (ví dụ ~2.5%)?",
  ["Loại bỏ phương sai GIỮA CÁC NGÀY (ngày này có thể thời tiết tốt hơn ngày kia một cách ngẫu nhiên) -- nếu so sánh hai thuật toán trên hai TẬP ngày khác nhau, sự khác biệt đó có thể bị nhầm lẫn với sự khác biệt do thời tiết, không phải do thuật toán",
   "Loại bỏ hoàn toàn mọi loại sai số có thể có",
   "Chỉ áp dụng khi có ít hơn 10 ngày dữ liệu",
   "Không có tác dụng gì nếu cả hai thuật toán đều tốt"],
  "Đây là nguyên tắc thiết kế thí nghiệm cơ bản: so sánh 'cùng điều kiện, chỉ đổi biến cần đo' giúp phát hiện được một hiệu ứng THẬT sự nhỏ (vài phần trăm) mà nếu so sánh thô (không ghép cặp) sẽ bị 'chìm' trong nhiễu ngày-đối-ngày lớn hơn nhiều.")

Q(p6, g,
  "'Block bootstrap' (tái chọn mẫu theo KHỐI nhiều ngày liên tiếp, thay vì từng ngày riêng lẻ) được dùng khi kiểm định ý nghĩa thống kê. Vì sao không nên coi từng ngày là một mẫu độc lập khi làm bootstrap thông thường?",
  ["Vì thời tiết có TƯƠNG QUAN THEO THỜI GIAN (autocorrelation): điều kiện hôm nay thường tương tự hôm qua/ngày mai (ví dụ một đợt mây kéo dài nhiều ngày) -- coi các ngày là độc lập sẽ PHÓNG ĐẠI độ tin cậy thống kê (significance) một cách giả tạo",
   "Vì số ngày dữ liệu quá ít để áp dụng bất kỳ phương pháp bootstrap nào",
   "Vì block bootstrap luôn cho kết quả giống hệt bootstrap thông thường",
   "Vì thời tiết thay đổi hoàn toàn ngẫu nhiên từng ngày không có quy luật"],
  "Đây là áp dụng nguyên tắc thống kê chuẩn cho dữ liệu chuỗi thời gian có tương quan (time-series autocorrelation) -- bỏ qua nó là một lỗi phổ biến khi phân tích dữ liệu khí hậu/môi trường, dễ dẫn đến kết luận 'có ý nghĩa thống kê' sai lệch.")

Q(p6, g,
  "Một kết luận được gọi là 'vững chắc' (robust) khi dấu (+ hay -) của nó KHÔNG ĐỔI qua nhiều giá trị tham số khác nhau (ví dụ m_K thay đổi từ 0.10 đến 0.20) và qua nhiều điều kiện khác nhau (ví dụ cả hai mùa khô/ướt). Vì sao kiểm tra độ vững chắc này quan trọng trước khi công bố một kết luận (ví dụ 'weather-info gain là âm')?",
  ["Để đảm bảo kết luận không phải là một hiện tượng 'tình cờ' chỉ đúng với MỘT lựa chọn tham số cụ thể, mà phản ánh một đặc tính cấu trúc sâu của bài toán -- tăng độ tin cậy và tính tổng quát của phát hiện",
   "Kiểm tra vững chắc chỉ cần thiết cho các bài báo khoa học, không cần cho ứng dụng thực tế",
   "Nếu kết quả đúng với một giá trị tham số là đủ, không cần kiểm tra thêm",
   "Kiểm tra vững chắc làm kết luận yếu đi, nên thường được bỏ qua"],
  "Đây là một bước kiểm chứng khoa học quan trọng: một phát hiện phản trực giác (như 'weather-info gain âm') cần được kiểm tra qua nhiều kịch bản để phân biệt giữa một QUY LUẬT thực sự với một sự trùng hợp ngẫu nhiên của một bộ tham số cụ thể.")

Q(p6, g,
  "Trong một chuỗi phân tích dữ liệu khám phá (EDA) nhiều lớp (từ quỹ đạo, ngân sách liên kết, khả dụng, lập lịch, đến kiểm định thống kê cắt ngang), thứ tự được đề xuất là: kiểm tra nguồn gốc/chất lượng dữ liệu (provenance) TRƯỚC, rồi mới phân tích một biến, rồi phân tích chéo nhiều lớp, rồi kiểm định giả thuyết, rồi kiểm tra độ nhạy. Vì sao 'kiểm tra nguồn gốc dữ liệu' phải là bước ĐẦU TIÊN?",
  ["Vì bất kỳ phân tích nào xây dựng trên dữ liệu có vấn đề (sai nguồn, thiếu trạm, đơn vị sai) sẽ cho kết luận sai bất kể thuật toán phân tích phía sau có tinh vi đến đâu -- kiểm tra nền tảng trước giúp tránh lãng phí công sức phân tích trên dữ liệu lỗi",
   "Thứ tự không quan trọng, có thể làm theo bất kỳ trình tự nào",
   "Vì đây là bước dễ làm nhất nên làm trước cho nhanh",
   "Kiểm tra nguồn gốc dữ liệu chỉ cần thiết cho dữ liệu thời tiết, không cần cho dữ liệu quỹ đạo"],
  "Đây là một nguyên tắc làm việc với dữ liệu chuyên nghiệp: 'garbage in, garbage out' -- mọi kết luận (kể cả các fix vật lý quan trọng như hệ số Rytov hay crosstalk đã thảo luận ở các phần trước) đều vô nghĩa nếu dữ liệu đầu vào không được kiểm chứng nguồn gốc trước.")

Q(p6, g,
  "Câu kết luận tổng hợp 'mây quyết định khả dụng, hình học quyết định khả thi cặp, phối hợp giúp khiêm tốn, nhận biết thời tiết chỉ vừa đủ trả chi phí handover, và giới hạn là SỐ TRẠM MẶT ĐẤT' tóm tắt toàn bộ hệ thống phân tầng nào?",
  ["Từ lớp VẬT LÝ (kênh, thời tiết) lên lớp HÌNH HỌC (vùng phủ, khả thi cặp), rồi lớp THUẬT TOÁN (lập lịch, phối hợp), và cuối cùng là lớp HẠ TẦNG (số lượng trạm) -- mỗi lớp có vai trò và giới hạn riêng, không lớp nào thay thế được lớp khác",
   "Chỉ một lớp duy nhất (thuật toán) quyết định toàn bộ hiệu năng hệ thống",
   "Các lớp này hoàn toàn độc lập, không liên quan đến nhau",
   "Kết luận này chỉ áp dụng cho hệ thống quang, không áp dụng hệ thống RF"],
  "Đây là bút tích tổng hợp toàn bộ các bước phân tích đã đi qua: hiểu được VAI TRÒ và GIỚI HẠN của từng lớp (vật lý, hình học, thuật toán, hạ tầng) là kiến thức hệ thống quan trọng hơn bất kỳ con số riêng lẻ nào, giúp định hướng đúng nơi cần đầu tư cải thiện thực sự.")

g = "Tổng hợp ứng dụng nâng cao"
Q(p6, g,
  "Nếu một chòm sao vệ tinh KHÔNG có liên kết liên-vệ-tinh (ISL) nào (mọi vệ tinh chỉ giao tiếp trực tiếp với mặt đất), điều gì xảy ra với các cặp trạm được phân loại SF (quá xa để DUAL)?",
  ["Các cặp SF sẽ phải chờ đến khi CHÍNH vệ tinh đó bay vòng quỹ đạo tiếp theo và đi qua trạm còn lại (độ trễ có thể lên tới hàng trăm phút, như trường hợp cực đoan 711 phút đã đề cập) -- không có cách nào rút ngắn độ trễ này nếu thiếu ISL",
   "Các cặp SF sẽ tự động trở thành DUAL nếu không có ISL",
   "Không có ISL không ảnh hưởng gì đến các cặp SF, chỉ ảnh hưởng cặp DUAL",
   "Thiếu ISL chỉ ảnh hưởng đến kênh dữ liệu, không ảnh hưởng kênh khóa"],
  "Đây là lý do ISL được coi là một nâng cấp hạ tầng quan trọng: nó không cải thiện các cặp DUAL (vốn đã kết nối trực tiếp tốt) mà mang lại lợi ích chủ yếu cho các cặp SF vốn bị giới hạn nặng nề bởi thiếu kết nối trực tiếp.")

Q(p6, g,
  "Nếu một cặp trạm cần relay qua 5 chặng ISL để đến đích, tổng thời gian xử lý (không tính lan truyền) theo mô hình 30 giây/chặng là bao nhiêu, và con số này so với chu kỳ quỹ đạo ~95 phút thế nào?",
  ["150 giây (2.5 phút), chỉ chiếm khoảng 2.6% chu kỳ quỹ đạo -- đủ nhỏ để giả định topology 'tĩnh' trong suốt quá trình relay vẫn hợp lý",
   "150 phút, gần gấp đôi chu kỳ quỹ đạo, khiến giả định tĩnh không còn hợp lý",
   "15 giây, quá nhỏ để có ý nghĩa thực tế",
   "Không thể tính được nếu không biết khoảng cách vật lý giữa các vệ tinh"],
  "Đây là một phép tính áp dụng trực tiếp: với số chặng thực tế (thường ít hơn 10 cho hầu hết các cặp trong một chòm sao dày đặc), tổng thời gian relay luôn nhỏ hơn nhiều so với chu kỳ quỹ đạo, xác nhận tính hợp lý của giả định topology tĩnh.")

Q(p6, g,
  "Nếu m_D (độ sâu điều chế dữ liệu) được đặt bằng 0 hoàn toàn (không truyền dữ liệu, chỉ dùng kênh khóa), điều gì xảy ra với crosstalk lên kênh khóa và với SKR so với trường hợp có cả hai kênh?",
  ["Crosstalk (tỷ lệ với m_D^2) giảm về 0, giúp SKR đạt giá trị TỐI ĐA có thể (không bị kênh dữ liệu gây nhiễu) -- đây là giới hạn trên lý thuyết của SKR khi hy sinh hoàn toàn thông lượng dữ liệu",
   "SKR sẽ giảm về 0 nếu không có kênh dữ liệu",
   "Crosstalk không đổi bất kể giá trị m_D",
   "SKR không phụ thuộc vào m_D trong bất kỳ trường hợp nào"],
  "Đây là điểm biên hữu ích để hiểu đường Pareto: một đầu của đường Pareto (m_D=0) cho SKR tối đa/thông lượng dữ liệu=0, đầu kia (m_K tối thiểu) cho thông lượng dữ liệu tối đa/SKR thấp -- mọi điểm vận hành thực tế nằm giữa hai cực trị này.")

Q(p6, g,
  "Trong chiến lược adaptive split, nếu K_req (lượng khóa yêu cầu) tăng lên gấp đôi cho cùng một pass (cùng thời gian T_pass), điều gì xảy ra với m_K tối thiểu cần thiết, và hệ quả cho thông lượng dữ liệu khả dụng?",
  ["m_K tối thiểu cần thiết phải TĂNG (cần điều chế khóa sâu hơn để đạt đủ khóa trong cùng thời gian), làm giảm phần công suất điều chế còn lại cho m_D -- thông lượng dữ liệu khả dụng GIẢM tương ứng",
   "m_K tối thiểu không đổi bất kể K_req thay đổi",
   "Thông lượng dữ liệu sẽ tăng lên khi K_req tăng",
   "K_req không có bất kỳ liên hệ nào với m_K hay thông lượng dữ liệu"],
  "Đây là minh họa trực tiếp cơ chế thích ứng: yêu cầu khóa cao hơn (ví dụ ứng dụng bảo mật nghiêm ngặt hơn) trực tiếp 'ăn vào' ngân sách công suất điều chế còn lại cho dữ liệu -- một đánh đổi tường minh mà chiến lược adaptive giúp tối thiểu hóa (chỉ lấy đúng phần cần thiết, không nhiều hơn).")

Q(p6, g,
  "Nếu kiểm định robustness cho thấy dấu của 'weather-info gain' đổi từ ÂM sang DƯƠNG khi m_K vượt quá một ngưỡng nhất định (ví dụ m_K > 0.25), kết luận về tính vững chắc của phát hiện ban đầu (ở m_K=0.15) cần được điều chỉnh thế nào?",
  ["Kết luận ban đầu cần được giới hạn phạm vi áp dụng rõ ràng ('đúng trong dải m_K đã kiểm tra, ví dụ 0.10-0.20') thay vì phát biểu như một quy luật tuyệt đối cho mọi giá trị m_K -- đây chính là giá trị của việc kiểm tra robustness: phát hiện được ranh giới áp dụng của một kết luận",
   "Phát hiện ban đầu hoàn toàn vô giá trị nếu có bất kỳ trường hợp nào đổi dấu",
   "Không cần điều chỉnh gì, kết luận ban đầu luôn đúng trong mọi trường hợp",
   "Cần loại bỏ hoàn toàn khái niệm weather-info gain khỏi báo cáo"],
  "Đây là cách xử lý đúng đắn khi kiểm tra robustness phát hiện một ranh giới: không phải mọi kết luận đều đúng TUYỆT ĐỐI cho mọi tham số, mà khoa học tốt là biết CHÍNH XÁC phạm vi mà một kết luận còn hiệu lực.")

Q(p6, g,
  "Trong khung thống kê, nếu số ngày dữ liệu (620 ngày) giảm xuống chỉ còn 30 ngày (một tháng), phương pháp 'full enumeration' có còn đáng tin cậy như trước để phát hiện một hiệu ứng nhỏ (~2.5%) không?",
  ["Ít đáng tin cậy hơn: dù 'full enumeration' trên 30 ngày vẫn tính đúng CHÍNH XÁC trung bình của chính 30 ngày đó, nhưng 30 ngày có thể không đủ ĐA DẠNG để đại diện cho biến động theo mùa/năm dài hạn -- vấn đề không phải sai số MẪU (vì đã liệt kê hết) mà là ĐỘ ĐẠI DIỆN của tập dữ liệu ngắn hạn",
   "Vẫn đáng tin cậy y hệt như 620 ngày vì full enumeration luôn chính xác tuyệt đối",
   "Không có sự khác biệt nào giữa 30 ngày và 620 ngày trong bất kỳ trường hợp nào",
   "620 ngày và 30 ngày luôn cho kết quả giống hệt nhau về mặt thống kê"],
  "Đây là một phân biệt tinh tế quan trọng: 'full enumeration' loại bỏ SAI SỐ MẪU trong phạm vi tập dữ liệu đang xét, nhưng không đảm bảo tập dữ liệu đó đủ ĐẠI DIỆN cho hiện tượng dài hạn muốn nghiên cứu -- hai khái niệm khác nhau dễ bị nhầm lẫn.")

Q(p6, g,
  "Một sinh viên đề xuất: 'Thay vì dùng block bootstrap phức tạp, chỉ cần lấy trung bình của 620 ngày và báo cáo độ lệch chuẩn thông thường (giả định các ngày độc lập) cho nhanh.' Rủi ro chính của đề xuất đơn giản hóa này là gì?",
  ["Độ lệch chuẩn tính theo giả định độc lập sẽ ĐÁNH GIÁ THẤP khoảng không chắc chắn thực sự (vì bỏ qua tương quan tự nhiên giữa các ngày liên tiếp), dẫn đến kết luận 'có ý nghĩa thống kê' một cách SAI LỆCH khi thực ra chưa đủ bằng chứng chắc chắn",
   "Không có rủi ro nào, cách đơn giản hóa này luôn cho kết quả tương đương",
   "Cách đơn giản hóa này luôn cho kết quả THẬN TRỌNG hơn (bảo thủ hơn) so với block bootstrap",
   "Rủi ro chỉ tồn tại nếu số ngày ít hơn 100"],
  "Đây là ứng dụng trực tiếp của nguyên tắc autocorrelation đã học vào một tình huống ra quyết định thực tế: 'nhanh hơn' không đồng nghĩa với 'đúng hơn' khi bỏ qua một đặc tính quan trọng (tương quan thời gian) của dữ liệu.")

Q(p6, g,
  "Xét toàn bộ chuỗi phân tích từ vật lý kênh (Bậc 1-2) đến hình học/thời tiết (Bậc 3-4) đến lập lịch (Bậc 5) đến các mở rộng nâng cao (Bậc 6): nếu phải chọn MỘT lĩnh vực để đầu tư cải thiện với ngân sách hạn chế nhằm tăng SKR tổng thể của toàn hệ thống nhiều nhất, phân tích tổng hợp gợi ý ưu tiên nào?",
  ["Ưu tiên hạ tầng (thêm trạm mặt đất / cải thiện khẩu độ thu-vật lý kênh), vì đây là hai lớp đã được xác định có TRẦN GIỚI HẠN CỨNG mà không thuật toán nào vượt qua được, trong khi lớp thuật toán lập lịch chỉ mang lại cải thiện biên (~2.5%)",
   "Ưu tiên tuyệt đối cho thuật toán lập lịch vì đây là phần dễ cải thiện nhất (chỉ cần viết code, không cần phần cứng mới)",
   "Ưu tiên thống kê/kiểm định vì đây là bước cuối cùng trong chuỗi phân tích nên quan trọng nhất",
   "Không thể đưa ra bất kỳ ưu tiên nào nếu không có thêm dữ liệu"],
  "Đây là câu hỏi tổng hợp toàn bộ nội dung: khả năng tổng hợp thông tin từ NHIỀU lớp phân tích khác nhau để đưa ra một khuyến nghị đầu tư có căn cứ là kỹ năng ứng dụng cao nhất của toàn bộ kiến thức đã học -- ưu tiên đúng lớp mang lại đòn bẩy lớn nhất, tránh đầu tư nhầm vào lớp chỉ mang lại cải thiện biên.")

g = "Ứng dụng tổng hợp mở rộng"
Q(p6, g,
  "Nếu một mạng lưới vệ tinh IoT mở rộng ISL để hỗ trợ CẢ dữ liệu cảm biến thông thường (không chỉ khóa lượng tử), nguyên tắc BFS/time-optimal/capacity-optimal đã học có thể áp dụng trực tiếp cho định tuyến dữ liệu cảm biến hay không?",
  ["Có thể áp dụng trực tiếp về mặt CẤU TRÚC (đồ thị mesh tĩnh, BFS tìm số chặng ít nhất, đánh đổi tốc độ-vs-chất lượng), vì đây là các nguyên lý định tuyến mạng tổng quát không đặc thù riêng cho tín hiệu lượng tử -- chỉ khác ở tiêu chí 'chất lượng' cụ thể (SKR cho khóa, có thể là độ ưu tiên/độ tươi dữ liệu cho cảm biến)",
   "Hoàn toàn không thể áp dụng vì lượng tử và dữ liệu cảm biến là hai lĩnh vực vật lý khác biệt hoàn toàn",
   "Chỉ có thể áp dụng cho dữ liệu cảm biến, không áp dụng được cho khóa lượng tử",
   "Nguyên tắc BFS chỉ hoạt động trên đồ thị có trọng số khác nhau cho từng cạnh, không dùng được cho ISL"],
  "Đây là một minh chứng cho tính TỔNG QUÁT của các nguyên lý mạng (đồ thị, định tuyến, đánh đổi latency-throughput) học được từ bài toán chuyên sâu (relay khóa lượng tử) sang các ứng dụng IoT rộng hơn -- kỹ năng nhận diện cấu trúc bài toán chung là giá trị cốt lõi của việc học sâu một trường hợp cụ thể.")

Q(p6, g,
  "Trong bối cảnh một hệ thống IoT thực tế phải phân chia băng thông giữa dữ liệu ĐIỀU KHIỂN (control, ưu tiên độ tin cậy) và dữ liệu CẢM BIẾN THÔ (bulk sensor data, ưu tiên thông lượng), bài toán power-split (m_K vs m_D) đã học tương tự với bài toán thiết kế IoT nào?",
  ["Tương tự bài toán phân chia tài nguyên (băng thông/công suất) giữa kênh CONTROL PLANE (cần độ tin cậy cao, dung lượng thấp, tương tự kênh khóa) và kênh DATA PLANE (cần thông lượng cao, tương tự kênh dữ liệu cổ điển) -- cùng một nguyên lý đánh đổi Pareto giữa độ tin cậy và thông lượng",
   "Không có sự tương đồng nào giữa hai bài toán này",
   "Bài toán power-split chỉ áp dụng được cho hệ thống lượng tử, không có tương tự trong IoT thông thường",
   "Control plane và data plane trong IoT không bao giờ cạnh tranh tài nguyên với nhau"],
  "Đây là một kết nối khái niệm quan trọng cho môn học: mẫu hình 'hai kênh cạnh tranh tài nguyên chung, một ưu tiên độ tin cậy một ưu tiên thông lượng' xuất hiện xuyên suốt nhiều hệ thống truyền thông (không chỉ SIKD) -- nhận ra mẫu hình chung giúp áp dụng tư duy Pareto-optimal vào nhiều bài toán thiết kế khác.")

Q(p6, g,
  "Nếu áp dụng nguyên tắc 'paired test' (so sánh cùng điều kiện, chỉ đổi biến cần đo) vào việc đánh giá hai thiết bị cảm biến IoT khác nhau trên thực địa, thiết kế thí nghiệm hợp lý nên là gì?",
  ["Đặt cả hai thiết bị TẠI CÙNG vị trí và THỜI GIAN (đo song song), thay vì đo thiết bị A ở địa điểm/thời gian này rồi đo thiết bị B ở địa điểm/thời gian khác -- đảm bảo mọi khác biệt kết quả đến từ CHÍNH thiết bị, không phải từ khác biệt điều kiện môi trường giữa hai lần đo",
   "Đo hai thiết bị ở hai địa điểm hoàn toàn khác nhau để có kết quả đa dạng hơn",
   "Không cần quan tâm đến việc đo cùng lúc hay khác lúc, kết quả sẽ luôn tương đương",
   "Chỉ cần đo mỗi thiết bị một lần duy nhất là đủ để so sánh chính xác"],
  "Đây là ứng dụng trực tiếp nguyên tắc kiểm định theo cặp đã học vào một tình huống thực nghiệm IoT cụ thể -- một kỹ năng thiết kế thí nghiệm có thể áp dụng rộng rãi trong nghiên cứu và phát triển sản phẩm IoT.")

Q(p6, g,
  "Một nhóm phát triển IoT tuyên bố 'cảm biến mới của chúng tôi cho độ chính xác cao hơn 3% so với thế hệ cũ' nhưng không nêu rõ đã kiểm tra qua bao nhiêu điều kiện môi trường khác nhau (nhiệt độ, độ ẩm, ánh sáng). Áp dụng khái niệm 'robustness' đã học, câu hỏi phản biện quan trọng nhất nên đặt ra là gì?",
  ["'Kết quả cải thiện 3% này có VỮNG CHẮC qua các điều kiện môi trường khác nhau không, hay chỉ đúng trong điều kiện thử nghiệm cụ thể đã chọn?' -- nếu chưa kiểm tra đa dạng điều kiện, tuyên bố cải thiện có thể chỉ là hiện tượng cục bộ chứ không phải một cải tiến tổng quát đáng tin cậy",
   "Không cần đặt câu hỏi gì thêm, con số 3% đã đủ để chấp nhận tuyên bố",
   "Chỉ cần hỏi về giá thành sản xuất của cảm biến mới",
   "Chỉ cần tin tưởng vào thương hiệu của nhà sản xuất cảm biến"],
  "Đây là ứng dụng trực tiếp tư duy phản biện khoa học (kiểm tra robustness) đã xây dựng xuyên suốt tài liệu này vào việc đánh giá các tuyên bố hiệu năng sản phẩm IoT trong thực tế công việc -- một kỹ năng tư duy phản biện có giá trị vượt ra ngoài phạm vi vệ tinh/lượng tử.")

Q(p6, g,
  "Nhìn lại toàn bộ hành trình từ vật lý kênh (photon, nhiễu, suy hao) đến thuật toán mạng (lập lịch, relay) đến thống kê (kiểm định, robustness): bài học PHƯƠNG PHÁP LUẬN tổng quát nhất có thể rút ra để áp dụng cho BẤT KỲ dự án kỹ thuật truyền thông nào khác là gì?",
  ["Luôn kiểm chứng bằng số liệu thực/tính toán trực tiếp thay vì tin tưởng mù quáng vào công thức/giả định có sẵn (nhiều lỗi hệ số quan trọng chỉ được phát hiện qua đối chiếu cẩn thận), đồng thời phân biệt rõ giới hạn CẤU TRÚC (không thể vượt qua bằng kỹ thuật) với giới hạn có thể CẢI THIỆN qua thuật toán/công nghệ tốt hơn",
   "Bài học duy nhất là luôn tin tưởng vào công thức trong sách giáo trình mà không cần kiểm tra lại",
   "Không có bài học phương pháp luận nào có thể tổng quát hóa từ một dự án cụ thể",
   "Chỉ cần chạy mô phỏng một lần và tin ngay kết quả đầu tiên nhận được"],
  "Đây là câu hỏi tổng kết toàn bộ hành trình học tập qua 200 câu hỏi: khả năng rút ra bài học PHƯƠNG PHÁP LUẬN (không chỉ công thức cụ thể) là mục tiêu học tập cao nhất -- áp dụng được tư duy kiểm chứng nghiêm ngặt và phân tầng giới hạn hệ thống vào bất kỳ bài toán truyền thông/IoT nào gặp phải trong tương lai.")

# ============================================================================
# Build, shuffle, validate, write
# ============================================================================
questions = []
qid = 0
persp_meta = []
for persp in PERSPECTIVES:
    count = 0
    for item in persp["items"]:
        qid += 1
        count += 1
        opts = item["options"]
        correct_text = opts[0]
        texts = opts[:]
        rng = random.Random(2000 + qid)
        rng.shuffle(texts)
        letters = ["A", "B", "C", "D"]
        new_opts = [{"key": letters[k], "text": t} for k, t in enumerate(texts)]
        new_answer = next(o["key"] for o in new_opts if o["text"] == correct_text)
        questions.append({
            "id": qid,
            "perspective": persp["num"],
            "perspectiveTitle": persp["title"],
            "group": item["group"],
            "question": item["question"],
            "options": new_opts,
            "answer": new_answer,
            "framework": item["framework"],
        })
    persp_meta.append({"num": persp["num"], "title": persp["title"], "count": count})

if len(questions) != 200:
    sys.exit(f"ERROR: expected 200 questions, got {len(questions)}")
for q in questions:
    if len(set(o["text"] for o in q["options"])) != 4:
        sys.exit(f"ERROR Q{q['id']}: duplicate option text")
    if sorted(o["key"] for o in q["options"]) != ["A", "B", "C", "D"]:
        sys.exit(f"ERROR Q{q['id']}: bad option keys")
    if not any(o["key"] == q["answer"] for o in q["options"]):
        sys.exit(f"ERROR Q{q['id']}: answer key not among options")

payload = {
    "meta": {
        "title": "Truyền thông Vệ tinh cho IoT — 200 câu hỏi ôn tập hệ thống",
        "total": len(questions),
        "perspectives": persp_meta,
        "source": "SIKD_Formula_Guide_v3_Expanded (Tự học/SIKD_Satellite_QKD), tổng hợp cho môn Các công nghệ truyền thông cho IoT (HUST 20251196M)",
    },
    "questions": questions,
}
json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK: {len(questions)} questions across {len(persp_meta)} perspectives -> {OUT}")
for p in persp_meta:
    print(f"  P{p['num']}  n={p['count']:>3}  {p['title']}")
