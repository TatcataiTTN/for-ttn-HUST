# -*- coding: utf-8 -*-
"""Sinh ngân hàng trắc nghiệm Module 02 từ facts_m02.py (19 fact đã xác minh) bằng nhiều khuôn
câu hỏi (template) khác nhau cho cùng 1 fact — KHÔNG tự bịa khái niệm mới, chỉ đổi cách hỏi.
Cân bằng vị trí đáp án đúng (round-robin qua 4 vị trí rồi xáo trong nhóm bằng seed cố định).
Output: ../../data/bank/bank_m02.json
"""
import json, pathlib, random, sys
from itertools import combinations

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from facts_m02 import FACTS

SEED = 20260205
rng = random.Random(SEED)
OUT = HERE.parent.parent / "data" / "bank" / "bank_m02.json"

# -------- T6: câu hỏi áp dụng trên lược đồ SQL sandbox (S1-S7, đúng nguyên văn slide) --------
SCHEMA_QS = [
  dict(q="Trong ví dụ Movie của slide gốc, thuộc tính 'genre' thuộc bảng nào ở nguồn S1?",
       correct="S1.Movie(title,director,year,genre)", topic="Ví dụ Movie (S1-S7)",
       wrong=["S1.Actor(AID,firstName,lastName,...)", "S2.Cinemas(place,movie,start)", "S4.Reviews(title,date,grade,review)"]),
  dict(q="Nguồn nào trong ví dụ Movie CHỈ biết đạo diễn (director) của phim, không biết năm/thể loại?",
       correct="S6.MovieDirectors(title,dir)", topic="Ví dụ Movie (S1-S7)",
       wrong=["S5.MovieGenres(title,genre)", "S7.MovieYears(title,year)", "S1.MovieDetails(MID,director,genre,year)"]),
  dict(q="Để dựng lại mediated Movie(title,director,year,genre) ĐẦY ĐỦ từ S5,S6,S7 (mỗi nguồn biết 1 cột), cần dùng phép toán quan hệ nào?",
       correct="JOIN 3 nguồn theo title (mỗi nguồn là 1 LAV view chỉ biết 1 phần cột)", topic="Ví dụ Movie (S1-S7)",
       wrong=["UNION 3 nguồn (vì chúng không có cùng số cột)", "Chỉ cần SELECT * từ 1 nguồn duy nhất", "Không thể dựng lại được vì thiếu mediated schema"]),
  dict(q="Nguồn S1 có đủ 4 bảng (Movie, Actor, ActorPlays, MovieDetails) — điều này minh hoạ đúng dị biệt nào trong slide 'Tabular Organization of Schema'?",
       correct="1 nguồn tách thành nhiều bảng trong khi mediated schema gộp 1 bảng Movie duy nhất", topic="Ví dụ Movie (S1-S7)",
       wrong=["Dị biệt về định dạng file (CSV vs JSON)", "Dị biệt về ngôn ngữ truy vấn (SQL vs NoSQL)", "Dị biệt chỉ xảy ra ở cấp độ dữ liệu (data-level), không phải cấp schema"]),
  dict(q="Theo slide 'Schema Coverage', vì sao S6.MovieDirectors không chứa 'Train to Busan'?",
       correct="Minh hoạ 'Different coverage and detail' — không phải nguồn nào cũng biết hết mọi phim", topic="Ví dụ Movie (S1-S7)",
       wrong=["Vì đó là lỗi nhập liệu cần sửa ngay", "Vì 'Train to Busan' không phải là phim thật", "Vì S6 chỉ chứa phim có rating trên 8 điểm"]),
  dict(q="Trong bài tập SQL Sandbox của site, S6.MovieDirectors ghi đạo diễn 'The Godfather' là 'Martin Scorsese' — đây minh hoạ điều gì?",
       correct="Xung đột dữ liệu GIỮA 2 NGUỒN được cài có chủ đích, để minh hoạ vấn đề Certain Answers", topic="Ví dụ Movie (S1-S7)",
       wrong=["Lỗi thật trong slide gốc của giảng viên", "Martin Scorsese thực sự là đạo diễn phim này", "Dữ liệu ngẫu nhiên không có mục đích sư phạm"]),
  dict(q="GAV cho nguồn S1: Movie(title,director,year,genre) ⊇ Q(S1). Vế PHẢI của công thức này ($Q(S1)$) đóng vai trò gì?",
       correct="Truy vấn trên S1 dùng để ĐỊNH NGHĨA mediated schema Movie", topic="Ví dụ Movie (S1-S7)",
       wrong=["Truy vấn người dùng gõ trực tiếp vào mediated schema", "Kết quả cuối cùng trả về cho người dùng", "Một ràng buộc toàn vẹn (integrity constraint) của S1"]),
  dict(q="Nếu S2.Cinemas(place,movie,start) và S3.NYCCinemas(name,title,startTime) CÙNG góp phần định nghĩa mediated Plays, đây là ví dụ của điều gì?",
       correct="Nhiều nguồn (GAV) cùng phủ 1 quan hệ mediated — cần UNION các view lại", topic="Ví dụ Movie (S1-S7)",
       wrong=["LAV — vì mediated schema được định nghĩa là view trên S2,S3", "Certain Answer — vì 2 nguồn luôn đồng thuận", "Đây là ví dụ Data-level Heterogeneity, không phải Schema Mapping"]),
]

# -------- T5: cloze/điền-từ từ chính câu văn đã viết & verify trong modules_content.py Module 02 --------
CLOZE_QS = [
  dict(q="Trong GAV, mỗi quan hệ của Mediated Schema được định nghĩa là 1 ___ trên các nguồn.",
       correct="view (truy vấn)", topic="GAV",
       wrong=["bản sao vật lý", "chỉ mục (index)", "ràng buộc khoá ngoại"]),
  dict(q="Công thức GAV dạng open-world viết là $G_i(\\bar X)$ ___ $Q(\\bar S)$ (dùng dấu chứa, không phải dấu bằng).",
       correct="⊇", topic="GAV",
       wrong=["=", "⊆", "≠"]),
  dict(q="Nhược điểm cốt lõi của GAV: cứng nhắc — ép mọi nguồn vào đúng 1 'góc nhìn' của mediated schema, không biểu diễn được trường hợp nguồn chỉ biết ___.",
       correct="1 phần thông tin (incomplete information)", topic="GAV",
       wrong=["toàn bộ thông tin đầy đủ", "thông tin đã mã hoá", "thông tin dạng XML"]),
  dict(q="Ngược với GAV, trong LAV mỗi ___ được định nghĩa là 1 view trên mediated schema.",
       correct="nguồn (source)", topic="LAV",
       wrong=["mediated schema", "truy vấn người dùng", "wrapper"]),
  dict(q="Ưu điểm của LAV: thêm/bớt nguồn chỉ cần thêm/bớt 1 định nghĩa LAV, không đụng tới ___.",
       correct="mediated schema", topic="LAV",
       wrong=["Certain Answers đã tính trước", "dữ liệu nguồn gốc", "wrapper của nguồn khác"]),
  dict(q="Reformulate trong LAV trở thành bài toán Answering Queries Using Views, dùng kỹ thuật ___ (suy ngược định nghĩa view ra rule rồi mới unfold được).",
       correct="Inverse Rules", topic="LAV",
       wrong=["Query Unfolding", "Correlation Clustering", "Locality-Sensitive Hashing"]),
  dict(q="GLAV tương đương về mặt hình thức với 1 ___ (Tuple Generating Dependency).",
       correct="TGD", topic="GLAV",
       wrong=["View vật lý (materialized view)", "Khoá chính (primary key)", "Chỉ mục B-tree"]),
  dict(q="Theo bảng so sánh GAV/LAV/GLAV trong slide, dòng 'Thêm nguồn mới' của cột GAV ghi là '___'.",
       correct="Sửa mediated schema", topic="So sánh GAV/LAV/GLAV",
       wrong=["Chỉ thêm định nghĩa", "Không cần làm gì", "Phải tính lại Certain Answers"]),
  dict(q="Theo bảng so sánh GAV/LAV/GLAV, dòng 'Biểu diễn incomplete info' của cột GAV ghi là '___'.",
       correct="Không", topic="So sánh GAV/LAV/GLAV",
       wrong=["Có", "Chỉ khi dùng closed-world", "Chỉ khi có đúng 1 nguồn"]),
  dict(q="Certain Answer: $t \\in Q(s_1,...,s_n)$ iff $t \\in Q(g)$ với ___ $g$ sao cho $(g,s_1,...,s_n) \\in M_R$.",
       correct="∀ (với mọi)", topic="Certain Answers",
       wrong=["∃ (tồn tại)", "chỉ 1", "không có"]),
  dict(q="Trong ví dụ slide: nguồn chỉ có (Title, Year); Mediated Schema cần (Director, Title, Year). Vì vậy có 2 ___ khả dĩ khác nhau cho Director.",
       correct="instance", topic="Certain Answers",
       wrong=["wrapper", "mapping language", "query plan"]),
  dict(q="Trong ví dụ Certain Answer, truy vấn 'trả về mọi năm phim' CÓ certain answer vì giá trị năm xuất hiện ___ ở cả 2 instance.",
       correct="giống nhau (đúng)", topic="Certain Answers",
       wrong=["khác nhau", "chỉ ở 1 instance", "không xuất hiện"]),
  dict(q="Trong ví dụ Certain Answer, truy vấn 'trả về mọi đạo diễn' KHÔNG có certain answer vì không đạo diễn nào xuất hiện ___.",
       correct="ở cả 2 instance", topic="Certain Answers",
       wrong=["ở instance thứ 1", "ở instance thứ 2", "trong mediated schema"]),
  dict(q="Query Unfolding: thay từng ___ bằng định nghĩa GAV tương ứng, lặp tới khi hết.",
       correct="subgoal", topic="Query Unfolding",
       wrong=["khoá chính", "view vật lý", "bảng chỉ mục"]),
  dict(q="Query Unfolding không đảm bảo tạo query hiệu quả hơn — kích thước truy vấn có thể tăng theo ___.",
       correct="cấp số nhân (exponential)", topic="Query Unfolding",
       wrong=["cấp số cộng (linear)", "tốc độ cố định", "không đổi"]),
]

# -------- T8: áp dụng trực tiếp lên VÍ DỤ SỐ đã có trong slide (Certain Answer worked example) --------
WORKED_QS = [
  dict(q="Ví dụ slide: Instance 1 = {(Allen,Manhattan,1979),(Coppola,GodFather,1972)}, Instance 2 = "
        "{(Halevy,Manhattan,1979),(Stonebraker,GodFather,1972)}. Giá trị năm (Year) của phim 'Manhattan' ở CẢ 2 instance là bao nhiêu?",
       correct="1979 (giống nhau ở cả 2 instance)", topic="Certain Answers — ví dụ số",
       wrong=["1972 ở cả 2 instance", "1979 ở instance 1, 1972 ở instance 2", "Không instance nào có năm cho Manhattan"]),
  dict(q="Cùng ví dụ trên: đạo diễn phim 'GodFather' là 'Coppola' ở instance 1 nhưng là gì ở instance 2?",
       correct="Stonebraker", topic="Certain Answers — ví dụ số",
       wrong=["Vẫn là Coppola", "Allen", "Halevy"]),
  dict(q="Vì đạo diễn 'GodFather' khác nhau giữa 2 instance (Coppola vs Stonebraker), kết luận đúng về Certain Answer cho truy vấn đạo diễn của GodFather là gì?",
       correct="Không có certain answer (vì không giá trị nào đúng ở CẢ 2 instance)", topic="Certain Answers — ví dụ số",
       wrong=["Certain answer là Coppola (vì xuất hiện trước)", "Certain answer là Stonebraker (vì xuất hiện sau)", "Certain answer là cả 2 giá trị cùng lúc"]),
  dict(q="Trong ví dụ này, nguồn gốc dữ liệu chỉ có 2 cột (Title, Year) — vậy tại sao instance lại CÓ thêm cột Director?",
       correct="Vì Mediated Schema yêu cầu (Director,Title,Year) — Director là thông tin KHÔNG có ở nguồn, nên mỗi instance khả dĩ 'đoán' 1 giá trị Director khác nhau", topic="Certain Answers — ví dụ số",
       wrong=["Vì nguồn thực ra có đủ 3 cột, slide ghi thiếu", "Vì Director được tính bằng công thức từ Title+Year", "Vì đây là lỗi dữ liệu cần sửa"]),
  dict(q="Nếu có Instance 3 = {(Allen,Manhattan,1979),(Stonebraker,GodFather,1972)} (trộn 2 instance cũ), Certain Answer cho đạo diễn GodFather có thay đổi không?",
       correct="Không — vẫn không có certain answer, vì 3 instance (gốc 2 + Instance 3 mới) vẫn không đồng thuận giá trị Director cho GodFather", topic="Certain Answers — ví dụ số",
       wrong=["Có — giờ certain answer là Stonebraker vì xuất hiện ở 2/3 instance", "Có — giờ certain answer là Allen", "Certain Answers không áp dụng được khi có từ 3 instance trở lên"]),
  dict(q="Giả sử thêm Instance 4 mà CẢ 2 phim đều ghi đạo diễn giống Instance 1 (Allen, Coppola). Director của 'GodFather' lúc này có certain answer không, xét trên 3 instance {1,2,4}?",
       correct="Không — Instance 2 vẫn ghi Stonebraker, khác Coppola ở Instance 1 và 4, nên vẫn không đồng thuận ở TẤT CẢ instance", topic="Certain Answers — ví dụ số",
       wrong=["Có — vì đa số (2/3) instance đồng thuận Coppola", "Có — certain answer luôn là giá trị xuất hiện ở Instance 1", "Certain answer lúc này là Stonebraker"]),
]

# -------- T4: câu hỏi so sánh (hand-curated, không tự sinh máy móc) --------
COMPARE_QS = [
  dict(q="So với GAV, ưu điểm chính của LAV là gì?",
       correct="Biểu diễn được thông tin nguồn không đầy đủ (incomplete information); dễ thêm/bớt nguồn",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["LAV luôn reformulate nhanh hơn GAV", "LAV không cần định nghĩa hình thức nào cả", "LAV chỉ hoạt động với dữ liệu XML"]),
  dict(q="Nhược điểm cốt lõi của GAV so với LAV là gì?",
       correct="Không biểu diễn được thông tin nguồn không đầy đủ — ép mọi nguồn vào đúng 1 view cố định",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["GAV luôn chạy chậm hơn LAV khi thực thi thực tế", "GAV không thể dùng cho dữ liệu quan hệ (chỉ dùng cho NoSQL)", "GAV yêu cầu certain answers phải rỗng"]),
  dict(q="GLAV khác GAV và LAV ở điểm nào?",
       correct="Cả 2 vế (nguồn và mediated schema) đều là truy vấn, biểu diễn bằng Tuple Generating Dependency",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["GLAV không cần reformulation vì đã có sẵn kết quả", "GLAV chỉ dùng được khi có đúng 2 nguồn", "GLAV là phiên bản cũ hơn, ít dùng hơn GAV/LAV trong thực tế"]),
  dict(q="Khi thêm 1 nguồn dữ liệu mới vào hệ thống đang dùng GAV, cần làm gì?",
       correct="Phải sửa lại định nghĩa mediated schema (vì mediated schema = view trên TẤT CẢ nguồn)",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["Chỉ cần thêm 1 định nghĩa LAV mới, không cần sửa gì khác", "Không cần làm gì, GAV tự động nhận nguồn mới", "Phải tính lại Certain Answers cho mọi truy vấn cũ đã lưu"]),
  dict(q="Khi thêm 1 nguồn dữ liệu mới vào hệ thống đang dùng LAV, cần làm gì?",
       correct="Chỉ cần thêm 1 định nghĩa LAV mới cho nguồn đó, không cần sửa mediated schema",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["Phải viết lại toàn bộ định nghĩa mediated schema từ đầu", "Phải chuyển toàn bộ hệ thống sang dùng GAV trước", "Không thể thêm nguồn mới khi đang dùng LAV"]),
  dict(q="Open-world assumption và Closed-world assumption khác nhau ở điểm nào?",
       correct="Open-world: còn có thể có dữ liệu khác chưa biết (⊇); Closed-world: chỉ có đúng dữ liệu đã biết (=)",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["Open-world dùng cho dữ liệu công khai trên Internet, Closed-world dùng cho dữ liệu nội bộ", "Open-world nhanh hơn Closed-world khi thực thi truy vấn", "Cả 2 đều giống nhau, chỉ khác tên gọi"]),
  dict(q="Query Unfolding (GAV) và Answering Queries Using Views (LAV) khác nhau cơ bản ở điều gì?",
       correct="Unfolding thay subgoal bằng rule đã biết sẵn (dễ); AQUV phải TÌM cách dùng view có sẵn để trả lời (khó hơn)",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["Hai thuật toán này hoàn toàn giống nhau, chỉ khác tên", "Unfolding dùng cho LAV, AQUV dùng cho GAV (bị đảo ngược)", "AQUV luôn cho kết quả sai, chỉ Unfolding mới đúng"]),
  dict(q="Vì sao Certain Answer cần xét 'MỌI instance khả dĩ' mà không chỉ xét 1 instance cụ thể?",
       correct="Vì với nhiều nguồn/mapping có thể tồn tại NHIỀU instance mediated schema đều hợp lệ — chỉ công nhận kết quả đúng ở TẤT CẢ các khả năng mới chắc chắn tin được",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["Vì luật của SQL yêu cầu phải xét mọi instance trước khi SELECT", "Vì chỉ có đúng 1 instance khả dĩ nên xét 1 cái là đủ, câu này không áp dụng", "Vì mỗi instance tốn nhiều bộ nhớ nên phải kiểm tra hết"]),
  dict(q="PAYGO khác Data Integration truyền thống (GAV/LAV cố định) ở điểm nào?",
       correct="Bắt đầu với ít ràng buộc ngữ nghĩa, trả lời tốt nhất có thể ngay, cải thiện dần — không chờ thiết kế mediated schema hoàn chỉnh",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["PAYGO yêu cầu thiết kế mediated schema kỹ hơn GAV/LAV truyền thống", "PAYGO chỉ là tên gọi khác của GLAV", "PAYGO không dùng được với Certain Answers"]),
  dict(q="Probabilistic Mediated Schema khác mediated schema truyền thống (1 schema cố định) ở điểm nào?",
       correct="Có NHIỀU phiên bản mediated schema khả dĩ cùng tồn tại, mỗi phiên bản kèm 1 xác suất, tạo tự động bằng clustering",
       topic="So sánh GAV/LAV/GLAV",
       wrong=["Probabilistic Mediated Schema luôn chỉ có đúng 1 phiên bản duy nhất, giống truyền thống", "Chỉ khác ở chỗ dùng ngôn ngữ truy vấn khác (NoSQL thay vì SQL)", "Không có gì khác biệt về bản chất, chỉ khác cách gọi tên"]),
]

# Chống length-bias: nếu đáp án đúng là đáp án DÀI NHẤT tuyệt đối (unique max), kéo dài đáp án
# nhiễu ngắn nhất bằng 1 trong các câu đệm trung lập (không gợi ý đúng/sai), chọn đệm theo hash để
# không có 1 câu đệm cố định nào trở thành "dấu hiệu luôn-luôn-sai" mới.
FILLERS = [
    " — một cách diễn giải hay gặp nhưng không khớp với định nghĩa đã học trong môn này",
    " — nhầm lẫn phổ biến giữa 2 khái niệm có tên gần giống nhau",
    " — đúng trong 1 ngữ cảnh khác, không đúng với ngữ cảnh đang xét ở đây",
    " — chỉ đúng một phần, còn thiếu điều kiện quan trọng để kết luận chắc chắn",
    " — cách hiểu sai thường gặp ở người mới bắt đầu học khái niệm này",
    " — mô tả gần đúng nhưng đảo ngược vai trò giữa 2 thành phần liên quan",
]

def debias_length(correct, wrongs, qid):
    opts = [correct] + list(wrongs)
    for _round in range(3):
        lens = [len(o) for o in opts]
        if not (lens[0] == max(lens) and lens.count(max(lens)) == 1):
            break
        # kéo dài đáp án nhiễu NGẮN NHẤT (trong số các đáp án nhiễu, index 1..3)
        shortest_i = min(range(1, 4), key=lambda i: lens[i])
        filler = FILLERS[hash((qid, shortest_i, _round)) % len(FILLERS)]
        opts[shortest_i] = opts[shortest_i] + filler
    return opts[0], opts[1:]

def balanced_options(correct, wrongs, slot, rng_local):
    opts = [correct] + list(wrongs)
    rng_local.shuffle(opts)
    # đảm bảo đúng tại đúng slot mong muốn (round-robin cân bằng vị trí 0..3)
    cur = opts.index(correct)
    opts[cur], opts[slot] = opts[slot], opts[cur]
    return opts, slot

def main():
    items = []
    slot_cycle = [0, 1, 2, 3]
    si = 0

    def add(q, correct, wrongs, topic, src, qid):
        nonlocal si
        correct, wrongs = debias_length(correct, wrongs, qid)
        local_rng = random.Random(SEED + hash(qid) % 100000)
        opts, correct_idx = balanced_options(correct, wrongs, slot_cycle[si % 4], local_rng)
        si += 1
        items.append(dict(id=qid, q=q, opts=opts, correct=correct_idx, topic=topic, src=src,
                           explain=f"Đáp án đúng: {correct}"))

    # T1: term -> definition
    for f in FACTS:
        add(f"'{f['term']}' được định nghĩa như thế nào (theo đúng nội dung slide/giáo trình đã học)?",
            f["definition"], f["wrong"], f["topic"], f["src"], f"m02-t1-{f['id']}")

    # T2: definition -> term
    all_terms = [f["term"] for f in FACTS]
    for f in FACTS:
        others = [t for t in all_terms if t != f["term"]]
        local_rng = random.Random(SEED + hash(f["id"]))
        distract_terms = local_rng.sample(others, 3)
        add(f"Định nghĩa sau mô tả đúng khái niệm nào? — \"{f['definition']}\"",
            f["term"], distract_terms, f["topic"], f["src"], f"m02-t2-{f['id']}")

    # T3: phát biểu nào ĐÚNG (framing khác T1, dùng để ôn lại dưới dạng nhận diện)
    for f in FACTS:
        add(f"Phát biểu nào sau đây về {f['term']} là ĐÚNG?",
            f["definition"], f["wrong"], f["topic"], f["src"], f"m02-t3-{f['id']}")

    # T5: cloze/điền-từ từ câu văn đã viết & verify trong modules_content.py
    for i, c in enumerate(CLOZE_QS):
        add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m02-t5-{i:02d}")

    # T8: áp dụng lên ví dụ số Certain Answer đã có trong slide
    for i, c in enumerate(WORKED_QS):
        add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m02-t8-{i:02d}")

    # T4: so sánh (hand-curated)
    for i, c in enumerate(COMPARE_QS):
        add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m02-t4-{i:02d}")

    # T6: áp dụng trên lược đồ SQL sandbox thật
    for i, c in enumerate(SCHEMA_QS):
        add(c["q"], c["correct"], c["wrong"], c["topic"], "bổ-sung", f"m02-t6-{i:02d}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Da sinh {len(items)} cau -> {OUT}")

if __name__ == "__main__":
    main()
