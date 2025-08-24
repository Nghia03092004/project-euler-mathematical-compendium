# scripts/gen_heatmap_html.py
import csv
import os

CSV_FILE = "metadata/problems.csv"
OUTPUT_FILE = "visualizations/archive.html"

# màu cho status
COLORS = {
    "solved": "#4caf50",       # xanh
    "in_progress": "#ff9800",  # cam
    "unsolved": "#9e9e9e"      # xám
}

def main():
    problems = {}
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = int(row["id"])
            problems[pid] = row

    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html><head><meta charset='UTF-8'><title>Project Euler Archive</title>")
    html.append("""
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }
      h1 { text-align: center; }
      .grid { display: grid; grid-template-columns: repeat(50, 22px); gap: 2px; justify-content: center; }
      .cell {
        width: 22px; height: 22px;
        display: flex; align-items: center; justify-content: center;
        font-size: 10px; color: white; text-decoration: none; border-radius: 4px;
      }
      .cell:hover { transform: scale(1.2); z-index: 2; position: relative; }
      .legend { margin-top: 20px; text-align: center; }
      .legend span {
        display: inline-block; width: 20px; height: 20px; margin: 0 5px; vertical-align: middle; border-radius: 4px;
      }
    </style>
    """)
    html.append("</head><body>")
    html.append("<h1>Project Euler Interactive Archive</h1>")
    html.append("<div class='grid'>")

    for i in range(1, 1001):
        if i in problems:
            row = problems[i]
            status = row.get("status", "unsolved")
            color = COLORS.get(status, COLORS["unsolved"])
            title = row.get("title", f"Problem {i}")
            link = f"../solutions/problem-{i:03d}-{title.lower().replace(' ', '-').replace(',', '')}/"
            html.append(
                f"<a class='cell' href='{link}' title='Problem {i}: {title} [{status}]' style='background:{color}'>{i}</a>"
            )
        else:
            color = COLORS["unsolved"]
            html.append(f"<div class='cell' style='background:{color}' title='Problem {i}: unsolved'>{i}</div>")

    html.append("</div>")
    html.append("<div class='legend'>")
    html.append("<span style='background:#4caf50'></span> Solved ")
    html.append("<span style='background:#ff9800'></span> In Progress ")
    html.append("<span style='background:#9e9e9e'></span> Unsolved ")
    html.append("</div>")
    html.append("</body></html>")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"✅ HTML archive generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
