# scripts/create_problem.py
import argparse, csv, os, pathlib, datetime, re
from pathlib import Path

SOL_DIR = Path("solutions")
CSV_PATH = Path("metadata/problems.csv")

def slugify(id_num, title):
    s = re.sub(r'[^a-z0-9\-]', '', re.sub(r'\s+', '-', title.lower()))
    return f"problem-{id_num:03d}-{s}"

def create_structure(id_num, title, languages):
    folder = SOL_DIR / slugify(id_num, title)
    folder.mkdir(parents=True, exist_ok=True)
    # create code templates
    if "python" in languages:
        (folder / "solution.py").write_text("#!/usr/bin/env python3\n# Solution for problem {}\n\nif __name__=='__main__':\n    pass\n".format(id_num), encoding="utf-8")
    if "cpp" in languages:
        (folder / "solution.cpp").write_text("// C++ solution stub for problem {}\n#include <bits/stdc++.h>\nusing namespace std;\nint main(){\n    return 0;\n}\n".format(id_num), encoding="utf-8")
    # latex template
    (folder / "solution.tex").write_text(r"""\documentclass{article}
\begin{document}
\section*{Problem %d}
% Write analysis here.
\end{document}
""" % id_num, encoding="utf-8")
    # README inside folder
    (folder / "README.md").write_text(f"# Problem {id_num} — {title}\n\nLink: https://projecteuler.net/problem={id_num}\n\nStatus: todo\n", encoding="utf-8")
    print(f"Created folder: {folder}")
    return folder

def append_csv(id_num, title, difficulty=" ", status="todo", languages="", answer="", date_solved=""):
    header = ["id","title","difficulty","status","languages","answer","date_solved","field","tags"]
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    exists = CSV_PATH.exists()
    with CSV_PATH.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(header)
        writer.writerow([id_num, title, difficulty, status, languages, answer, date_solved, "", ""])
    print(f"Appended metadata for {id_num} to {CSV_PATH}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--title", type=str, required=True)
    parser.add_argument("--languages", type=str, default="python")
    args = parser.parse_args()
    create_structure(args.id, args.title, args.languages.lower().split(","))
    # optional: do not auto-append if already there
    # if ID exists, skip
    if CSV_PATH.exists():
        import csv
        with CSV_PATH.open(encoding="utf-8") as f:
            if any(int(r["id"])==args.id for r in csv.DictReader(f)):
                print("ID already present in CSV; skipping append.")
                return
    append_csv(args.id, args.title, difficulty="", status="todo", languages=args.languages)

if __name__ == "__main__":
    main()
