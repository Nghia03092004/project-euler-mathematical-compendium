# scripts/update_readme.py
import csv, re, pathlib, os
from pathlib import Path

CSV_PATH = Path("metadata/problems.csv")
README_PATH = Path("README.md")
SOLUTIONS_DIR = Path("solutions")

def slugify_folder(id_num: int, title: str) -> str:
    import re
    base = f"problem-{id_num:03d}-" + re.sub(r'[^a-z0-9\-]', '',
                                            re.sub(r'\s+', '-', title.lower()))
    base = re.sub(r'-{2,}', '-', base).strip('-')
    return base

def detect_resources(id_num, title):
    folder = SOLUTIONS_DIR / slugify_folder(id_num, title)
    pdf = folder / "solution.pdf"
    # detect languages by file extensions present
    langs = []
    for ext, lang in [(".py","Python"), (".cpp","C++"), (".jl","Julia"), (".rs","Rust")]:
        if any(folder.glob(f"*{ext}")):
            langs.append(lang)
    lang_str = ", ".join(langs) if langs else ""
    has_folder = folder.exists()
    has_pdf = pdf.exists()
    return {
        "folder": str(folder).replace("\\","/"),
        "has_folder": has_folder,
        "has_pdf": has_pdf,
        "langs": lang_str
    }

def read_csv():
    rows = []
    if not CSV_PATH.exists():
        print("Warning: metadata/problems.csv not found.")
        return rows
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def make_table(rows):
    header = "| # | Title | Difficulty | Languages | Status | Notes |\n|---:|---|---:|---|:---:|---|\n"
    lines = []
    for r in rows:
        pid = int(r["id"])
        title = r.get("title","").strip() or f"Problem {pid}"
        difficulty = r.get("difficulty","")
        status = (r.get("status") or "todo").strip()
        # detect resources
        res = detect_resources(pid, title)
        langs = res["langs"] or (r.get("languages") or "")
        # solution link preference: pdf -> folder -> project euler
        if res["has_pdf"]:
            sol_link = f"[PDF]({res['folder']}/solution.pdf)"
        elif res["has_folder"]:
            sol_link = f"[Folder]({res['folder']}/)"
        else:
            sol_link = f"[Euler](https://projecteuler.net/problem={pid})"
        # notes: if solution.tex exists
        notes_link = ""
        folder = Path(res["folder"])
        if (folder / "solution.tex").exists():
            notes_link = f"[LaTeX]({res['folder']}/solution.tex)"
        elif (folder / "notes.md").exists():
            notes_link = f"[Notes]({res['folder']}/notes.md)"
        else:
            notes_link = "-"
        # row markdown
        lines.append(f"| [{pid}](https://projecteuler.net/problem={pid}) | {title} | {difficulty} | {langs} | {status} | {sol_link} {notes_link} |")
    return header + "\n".join(lines)

def update_badge_and_table(table_md, rows):
    readme = README_PATH.read_text(encoding="utf-8")
    solved = sum(1 for r in rows if (r.get("status") or "").strip().lower()=="solved")
    total_cap = 1000
    # update badge (Solved-X%2F1000)
    readme = re.sub(r"(Solved-)\d+%2F\d+", f"Solved-{solved}%2F{total_cap}", readme)
    # replace table block
    readme = re.sub(
        r"(<!-- PROGRESS_TABLE_START -->)(.*?)(<!-- PROGRESS_TABLE_END -->)",
        r"\1\n" + table_md + r"\n\\3",
        readme,
        flags=re.S
    )
    README_PATH.write_text(readme, encoding="utf-8")
    print(f"Updated README: {solved}/{total_cap} solved.")

def main():
    rows = read_csv()
    if not rows:
        print("No rows in CSV; README not updated.")
        return
    table_md = make_table(rows)
    update_badge_and_table(table_md, rows)

if __name__ == "__main__":
    main()
