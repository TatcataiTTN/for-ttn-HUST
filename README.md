# for-ttn-HUST

Static, browser-only study material (no backend). Hosted on GitHub Pages.

## Integrate-Process-Big-Data-VTT — IT5427 self-study system

Live: **https://tatcataittn.github.io/for-ttn-HUST/Integrate-Process-Big-Data-VTT/**

Self-study site for "IT5427 — Tích hợp và xử lý dữ liệu lớn" (HUST, giảng viên Vũ Tuyết Trinh).
5 modules (1 optional foundations module + 4 lecture modules matching the course's own slide decks:
Data Integration overview, Schema Alignment GAV/LAV/GLAV, Mediation Query & Big Data challenges,
Record Linkage & Entity Resolution), each with an interactive slide-deck, written exercises with
worked solutions, Q&A flashcards, and a self-grading multiple-choice quiz. A references page lists
the course's 4 official textbooks plus 19 verified academic papers backing the slide content.

```bash
cd Integrate-Process-Big-Data-VTT/build && python3 gen_site.py   # regenerate vi/
cd Integrate-Process-Big-Data-VTT && python3 -m http.server 8743   # serve locally
```

## Communication-tech-for-IoT — 200-question practice bank

Live: **https://tatcataittn.github.io/for-ttn-HUST/Communication-tech-for-IoT/**

An interactive, self-grading multiple-choice quiz (200 questions across 7 topics, from
foundational concepts to physical-layer optics, receiver design, weather statistics,
coverage geometry, network scheduling, and advanced extensions) for the course
"Các công nghệ truyền thông cho IoT" (HUST, 20251196M). Content is adapted from the
verified physics/algorithms of a satellite free-space-optical link project (see
`build/gen_questions.py` for full provenance), generalised for the IoT communications
course without referencing specific source-code file/folder names.

- Pick an answer, get instant correct/incorrect grading plus a one-line **theory
  framework** explaining what the formula/algorithm actually means.
- Progress is saved in the browser (`localStorage`) — no server, no account.
- **Review wrong answers** and **framework search/reference** pages for spaced review.

### Regenerating the question bank (never hand-type answers)

Questions are authored with the correct option listed first, then shuffled
deterministically (seed = question id) and re-lettered A-D, so there is no separate
hand-typed answer key:

```bash
python3 Communication-tech-for-IoT/build/gen_questions.py   # -> data/questions.json
```

### Testing

```bash
cd Communication-tech-for-IoT && python3 -m http.server 8933   # serve locally
```
