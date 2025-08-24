import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Đọc metadata (chứa status từng bài)
df = pd.read_csv("metadata/problems.csv")

# Chuẩn bị màu sắc
color_map = {
    "solved": "#ff9933",
    "in_progress": "#3399ff",
    "todo": "#eeeeee"
}

# Tổng số problem mặc định = 1000
max_id = 1000

# Cấu hình grid (40 cột × 25 hàng = 1000 ô)
cols = 40
rows = 25

fig, ax = plt.subplots(figsize=(20, 12))

for pid in range(1, max_id + 1):
    info = df[df["id"] == pid]
    status = "todo"
    if not info.empty and info.iloc[0]["status"] in color_map:
        status = info.iloc[0]["status"]

    color = color_map[status]

    # Vị trí trong grid
    x = (pid - 1) % cols
    y = rows - 1 - (pid - 1) // cols

    rect = plt.Rectangle((x, y), 1, 1, facecolor=color, edgecolor="white")
    ax.add_patch(rect)

    # Vẽ số problem
    ax.text(x + 0.5, y + 0.5, str(pid),
            ha="center", va="center", fontsize=6, color="black")

# Cấu hình hiển thị
ax.set_xlim(0, cols)
ax.set_ylim(0, rows)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.set_title("Project Euler Progress (1–1000)", fontsize=16, pad=20)

# Thêm legend
legend_handles = [
    mpatches.Patch(color=color_map["solved"], label="Solved"),
    mpatches.Patch(color=color_map["in_progress"], label="In Progress"),
    mpatches.Patch(color=color_map["todo"], label="Todo")
]
ax.legend(handles=legend_handles, loc="upper center",
          bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=10)

# Lưu ảnh
plt.savefig("visualizations/heatmap.png", dpi=200, bbox_inches="tight")
plt.close()
