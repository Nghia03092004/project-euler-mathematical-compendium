import csv, re, pathlib

CSV_PATH = "metadata/problems.csv"
README_PATH = "README.md"

def generate_table_and_counts():
    rows_md = []
    total = 0
    solved = 0
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            total += 1
            url = f"https://projecteuler.net/problem={r['id']}"
            st = (r["status"] or "").strip().lower()
            icon = {"solved":"✅","in_progress":"⏳","todo":"⬜"}.get(st, "⬜")
            if st == "solved":
                solved += 1
            rows_md.append(
                f"| [{r['id']}]({url}) | {r['title']} | {r['difficulty']} | {r['languages']} | {icon} |"
            )
    header = "| # | Title | Difficulty | Languages | Status |\n|---:|---|---|---|:---:|"
    table_md = header + "\n" + "\n".join(rows_md) if rows_md else "_No entries yet._"
    return table_md, solved, max(total, 1000)  # cap at 1000 for the badge

def update_readme(table_md, solved, total_cap):
    readme = pathlib.Path(README_PATH).read_text(encoding="utf-8")
    # update the progress table block
    readme = re.sub(
        r"(<!-- PROGRESS_TABLE_START -->)(.*?)(<!-- PROGRESS_TABLE_END -->)",
        r"\1\n" + table_md + r"\n\3",
        readme,
        flags=re.S
    )
    # update the Solved badge "Solved-X%2F1000"
    readme = re.sub(
        r"(Solved-)\d+%2F\d+",
        fr"Solved-{solved}%2F{total_cap}",
        readme
    )
    pathlib.Path(README_PATH).write_text(readme, encoding="utf-8")

if __name__ == "__main__":
    table, solved, total_cap = generate_table_and_counts()
    update_readme(table, solved, total_cap)
    print(f"Updated README: solved {solved}/{total_cap}")
