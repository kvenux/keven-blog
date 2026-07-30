from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "assets" / "quality-token-frontier-matplotlib.png"

for font_path in (Path(r"C:\Windows\Fonts\times.ttf"), Path(r"C:\Windows\Fonts\simsun.ttc")):
    if font_path.exists():
        font_manager.fontManager.addfont(str(font_path))
plt.rcParams.update({
    "font.family": ["Times New Roman", "SimSun"],
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})

points = {
    "Bare": (2.22, 73.54, "#536b78"),
    "Grill Me": (3.31, 80.30, "#217a65"),
    "OpenSpec": (3.91, 71.42, "#a27a2c"),
    "Ponytail": (3.21, 72.23, "#73599a"),
    "MatrixSpec L0": (8.57, 90.27, "#1976a3"),
    "Superpowers": (23.44, 84.08, "#c4513f"),
}

fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

ax.set_xlim(0, 25.5)
ax.set_ylim(67.5, 93.0)
ax.set_xticks([0, 5, 10, 15, 20, 25], ["0", "5M", "10M", "15M", "20M", "25M"])
ax.set_yticks([70, 75, 80, 85, 90])
ax.grid(True, color="#ddd8cd", linewidth=1.0, alpha=0.85)
ax.set_axisbelow(True)

offsets = {
    "Bare": (12, 9),
    "Grill Me": (12, 8),
    "OpenSpec": (12, -18),
    "Ponytail": (12, 8),
    "MatrixSpec L0": (12, 9),
    "Superpowers": (-168, 9),
}

for name, (tokens, score, color) in points.items():
    ax.scatter(tokens, score, s=220, color=color, edgecolor="white", linewidth=1.7, zorder=3)
    dx, dy = offsets[name]
    ax.annotate(
        f"{name}\n{score:.2f} | {tokens:.2f}M tokens",
        (tokens, score),
        xytext=(dx, dy),
        textcoords="offset points",
        fontsize=11.5,
        color=color,
        ha="left",
        va="bottom" if dy >= 0 else "top",
        linespacing=1.25,
    )

ax.set_title("Blind score and candidate-token use", fontsize=21, loc="left", pad=22)
ax.set_xlabel("Candidate tokens / run", fontsize=14, labelpad=14)
ax.set_ylabel("Blind score", fontsize=14, labelpad=14)

for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
for spine in ("left", "bottom"):
    ax.spines[spine].set_color("#435149")
    ax.spines[spine].set_linewidth(1.4)

fig.subplots_adjust(left=0.09, right=0.97, top=0.88, bottom=0.13)
fig.savefig(OUTPUT, facecolor=fig.get_facecolor())
print(OUTPUT)
