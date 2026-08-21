# for-ttn-HUST

Static, browser-only study material (no backend). Hosted on GitHub Pages.

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
