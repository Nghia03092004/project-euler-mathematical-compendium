# Project Euler Mathematical Compendium

[![Solved](https://img.shields.io/badge/Solved-1%2F1000-blue)](#progress)
[![Languages](https://img.shields.io/badge/Languages-Python%20%7C%20C++%20%7C%20Julia-green)](#repository-structure)
[![License](https://img.shields.io/badge/License-MIT-success)](#license)

A scholarly, code-driven archive of Project Euler solutions. This repository unifies:
- Implementations (multiple languages),
- Mathematical analysis (LaTeX-ready structure),
- Visual analytics (a 1–1000 grid heatmap and a live progress table).

> Index of problems: https://projecteuler.net/archives

---

## Repository Structure


- **metadata/problems.csv** columns:
  - `id,title,difficulty,status,languages,answer,date_solved,field,tags`
  - `status` ∈ { `solved`, `in_progress`, `todo` }
  - Set `languages` like `"python,cpp"` if multiple implementations exist.

---

## Progress

The table below is **auto-generated** from `metadata/problems.csv`.  
Each problem ID links directly to its Project Euler page.

<!-- PROGRESS_TABLE_START -->
| # | Title | Difficulty | Languages | Status | Notes |
|---:|---|---:|---|:---:|---|
| [1](https://projecteuler.net/problem=1) | Multiples of 3 and 5 | Easy | Python | solved | [Folder](solutions/problem-001-multiples-of-3-and-5/) - |
| [2](https://projecteuler.net/problem=2) | Even Fibonacci numbers | Easy |  | todo | [Euler](https://projecteuler.net/problem=2) - |
| [3](https://projecteuler.net/problem=3) | Largest prime factor | Medium |  | todo | [Euler](https://projecteuler.net/problem=3) - |
\3

Legend: ✅ solved · ⏳ in progress · ⬜ todo

---

## 📊 Progress Heatmap

The heatmap is a single 40×25 board (1–1000).  
- Orange = solved  
- Blue = in progress  
- Gray = todo

![Project Euler Heatmap](visualizations/heatmap.png)

🔗 Interactive archive: https://Nghia03092004.github.io/project-euler-mathematical-compendium/visualizations/archive.html

---

## How to Update Locally

1) Edit `metadata/problems.csv` and add/update rows.  
2) Regenerate artifacts:
```bash
python scripts\update_readme.py
python scripts\gen_heatmap.py