# scripts/gen_heatmap_html.py
import csv
import os
import re
from pathlib import Path

CSV_FILE = "metadata/problems.csv"
OUTPUT_FILE = "visualizations/archive.html"

# colors
COLORS = {
    "solved": "#4caf50",       # green
    "in_progress": "#ff9800",  # orange
    "todo": "#9e9e9e"          # gray
}

# grid size for 1000 problems
COLS = 40
MAX_ID = 1000

def slugify_folder(id_num: int, title: str) -> str:
    """
    Create folder name like: problem-001-multiples-of-3-and-5
    """
    # lower, replace spaces with -, remove characters that are not alnum or hyphen
    base = f"problem-{id_num:03d}-" + re.sub(r'[^a-z0-9\-]', '',
                                            re.sub(r'\s+', '-', title.lower()))
    # collapse multiple hyphens
    base = re.sub(r'-{2,}', '-', base).strip('-')
    return base

def read_metadata():
    problems = {}
    if not os.path.exists(CSV_FILE):
        print(f"Warning: {CSV_FILE} not found. All cells will be 'todo'.")
        return problems
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                pid = int(row.get("id", "").strip())
            except:
                continue
            problems[pid] = row
    return problems

def detect_target(pid, row):
    """
    Return tuple (href, link_type) where:
    - href is relative path from visualizations/archive.html
    - link_type is one of "pdf","folder","euler"
    """
    title = row.get("title", f"problem-{pid}")
    folder = slugify_folder(pid, title)
    pdf_path = Path("solutions") / folder / "solution.pdf"
    folder_path = Path("solutions") / folder
    if pdf_path.exists():
        return (f"../solutions/{folder}/solution.pdf", "pdf")
    if folder_path.exists():
        return (f"../solutions/{folder}/", "folder")
    # fallback to Project Euler
    return (f"https://projecteuler.net/problem={pid}", "euler")

def main():
    problems = read_metadata()

    html_parts = []
    html_parts.append("<!doctype html>")
    html_parts.append("<html><head><meta charset='utf-8'><title>Project Euler Interactive Archive</title>")
    html_parts.append("""<meta name="viewport" content="width=device-width, initial-scale=1">""")
    html_parts.append("""
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; background:#fafafa; margin:20px; }
      h1 { text-align:center; margin-bottom:10px; }
      .grid { display: grid; grid-template-columns: repeat(%d, 20px); gap: 3px; justify-content: center; }
      .cell {
        width: 20px; height: 20px; display:flex; align-items:center; justify-content:center;
        font-size:10px; color:white; text-decoration:none; border-radius:3px; line-height:1;
      }
      .cell:hover { transform: scale(1.25); z-index:2; position:relative; }
      .legend { margin-top:18px; text-align:center; font-size:13px; }
      .legend span { display:inline-block; width:14px; height:14px; margin:0 6px; vertical-align:middle; border-radius:3px; }
      .container { max-width:1100px; margin:0 auto; }
      .note { text-align:center; color:#666; margin-bottom:14px; }
    </style>
    """ % COLS)
    html_parts.append("</head><body>")
    html_parts.append("<div class='container'>")
    html_parts.append("<h1>Project Euler Interactive Archive (1–1000)</h1>")
    html_parts.append("<p class='note'>Click a cell to open the solution PDF (if present), otherwise the solution folder, otherwise the Project Euler page.</p>")
    html_parts.append("<div class='grid'>")

    for pid in range(1, MAX_ID+1):
        row = problems.get(pid)
        status = "todo"
        title = f"Problem {pid}"
        if row:
            status = (row.get("status") or "todo").strip().lower()
            title = row.get("title") or title

        color = COLORS.get(status, COLORS["todo"])

        if row:
            href, link_type = detect_target(pid, row)
            tooltip = f"Problem {pid}: {title} [{status}] - links to {link_type}"
            html_parts.append(
                f"<a class='cell' href='{href}' title=\"{tooltip}\" style='background:{color}'>"+str(pid)+"</a>"
            )
        else:
            tooltip = f"Problem {pid}: unsolved"
            html_parts.append(
                f"<div class='cell' title=\"{tooltip}\" style='background:{color}; color:#222'>{pid}</div>"
            )

    html_parts.append("</div>")  # grid
    html_parts.append("<div class='legend'>")
    html_parts.append("<span style='background:%s'></span> Solved &nbsp;&nbsp;" % COLORS["solved"])
    html_parts.append("<span style='background:%s'></span> In Progress &nbsp;&nbsp;" % COLORS["in_progress"])
    html_parts.append("<span style='background:%s'></span> Todo" % COLORS["todo"])
    html_parts.append("</div>")  # legend
    html_parts.append("</div>")  # container
    html_parts.append("</body></html>")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    print(f"✅ Generated {OUTPUT_FILE} (interactive archive).")

if __name__ == "__main__":
    main()
