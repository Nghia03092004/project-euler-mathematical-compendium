import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

CSV_PATH = "metadata/problems.csv"
OUT_PATH = "visualizations/heatmap.png"

df = pd.read_csv(CSV_PATH)

n = 30  # mỗi hàng 30 problem
colors = {"solved":"#ff9933", "todo":"#eeeeee", "in_progress":"#66ccff"}

plt.figure(figsize=(15, 30))
for idx, row in df.iterrows():
    x, y = (row["id"]-1) % n, -(row["id"]-1)//n
    c = colors.get(row["status"], "#eeeeee")
    plt.gca().add_patch(plt.Rectangle((x, y), 1, 1, color=c))
    plt.text(x+0.5, y+0.5, str(row["id"]), ha="center", va="center", fontsize=6)

plt.axis("equal")
plt.axis("off")
patches = [mpatches.Patch(color=v, label=k) for k,v in colors.items()]
plt.legend(handles=patches, loc="lower right")
plt.savefig(OUT_PATH, bbox_inches="tight")
