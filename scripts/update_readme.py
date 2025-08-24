import csv, re, pathlib

CSV_PATH = "metadata/problems.csv"
README_PATH = "README.md"

def generate_table():
    rows = []
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            url = f"https://projecteuler.net/problem={r['id']}"
            status_icon = {"solved":"✅","todo":"⬜","in_progress":"⏳"}.get(r["status"], "⬜")
            rows.append(
                f"| [{r['id']}]({url}) | {r['title']} | {r['difficulty']} | {r['languages']} | {status_icon} |"
            )
    header = "| # | Title | Difficulty | Language | Status |\n|---|--------|------------|----------|--------|"
    return header + "\n" + "\n".join(rows)

def update_readme():
    readme = pathlib.Path(README_PATH).read_text(encoding="utf-8")
    table = generate_table()
    new = re.sub(
        r"(<!-- PROGRESS_TABLE_START -->)(.*?)(<!-- PROGRESS_TABLE_END -->)",
        r"\1\n" + table + r"\n\3",
        readme,
        flags=re.S
    )
    pathlib.Path(README_PATH).write_text(new, encoding="utf-8")

if __name__ == "__main__":
    update_readme()
