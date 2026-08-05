from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ARTICLE = Path(__file__).resolve().parent
ASSETS = ARTICLE / "assets"
PLAYGROUND = ARTICLE.parents[2]
EXPERIMENT = PLAYGROUND / "sdd-exp"
PROFILED_REPORT = (
    EXPERIMENT
    / "archive"
    / "historical-matrixspec"
    / "aggregate-reports"
    / "matrixspec-profiled-8task-2x2-full-report.json"
)
LEAN_REPORT = EXPERIMENT / "reports" / "matrixspec-lean-v1-8task.json"

INK = "#111111"
MUTED = "#555555"
PAPER = "#FFFFFF"
LINE = "#D0D0D0"
GREEN = "#177653"
GREEN_SOFT = "#DDEEE5"
RED = "#B24736"
RED_SOFT = "#F6E2DC"
BLUE = "#3B6F91"
BLUE_SOFT = "#E2EDF4"
GOLD = "#A97917"
GOLD_SOFT = "#F5EBCF"
PURPLE = "#6E5A92"


def configure_style() -> None:
    for path in (
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/msyhbd.ttc"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ):
        if path.exists():
            font_manager.fontManager.addfont(str(path))
    plt.rcParams.update(
        {
            "font.family": ["Microsoft YaHei", "SimSun", "DejaVu Sans"],
            "axes.unicode_minus": False,
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "text.color": INK,
            "axes.labelcolor": INK,
            "axes.edgecolor": LINE,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "font.size": 9.5,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "axes.linewidth": 0.8,
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "legend.fontsize": 8.5,
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    fig.savefig(ASSETS / name, dpi=190, bbox_inches="tight", pad_inches=0.16)
    plt.close(fig)


def load_reports() -> tuple[dict, dict]:
    return (
        json.loads(PROFILED_REPORT.read_text(encoding="utf-8")),
        json.loads(LEAN_REPORT.read_text(encoding="utf-8")),
    )


def rounded_box(ax, x, y, width, height, text, face, edge=LINE, fontsize=11, weight="normal"):
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.025,rounding_size=0.04",
        facecolor=face,
        edgecolor=edge,
        linewidth=1.35,
    )
    ax.add_patch(patch)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=fontsize, weight=weight)
    return patch


def build_self_evolution_loop() -> None:
    fig, ax = plt.subplots(figsize=(13.6, 7.3))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.3)
    ax.axis("off")
    ax.text(0.35, 6.86, "MatSpec 的 Harness 自进化闭环", fontsize=22, weight="bold")
    ax.text(
        0.35,
        6.46,
        "优化对象不是单次代码补丁，而是下一次仍会运行 Agent 的工作流、上下文接口与控制逻辑",
        fontsize=11,
        color=MUTED,
    )

    nodes = [
        (0.45, 3.55, 2.05, "当前 Harness  Hₜ\nworkflow · commands · context", BLUE_SOFT, BLUE),
        (3.05, 3.55, 2.05, "真实任务运行\nCandidate Agent", GOLD_SOFT, GOLD),
        (5.65, 3.55, 2.05, "冻结 trajectory\ndiff · tests · usage", GREEN_SOFT, GREEN),
        (8.25, 3.55, 2.05, "Evolver Agent\n归因并修改 Harness", RED_SOFT, RED),
        (10.85, 3.55, 2.05, "候选 Harness\nHₜ + ΔHₜ", BLUE_SOFT, BLUE),
    ]
    for x, y, width, text, face, edge in nodes:
        rounded_box(ax, x, y, width, 1.28, text, face, edge=edge, fontsize=11, weight="bold")
    for left, right in zip(nodes, nodes[1:]):
        ax.add_patch(
            FancyArrowPatch(
                (left[0] + left[2] + 0.05, 4.19),
                (right[0] - 0.05, 4.19),
                arrowstyle="-|>",
                mutation_scale=14,
                linewidth=1.45,
                color=INK,
            )
        )

    rounded_box(
        ax,
        8.25,
        1.35,
        4.65,
        1.12,
        "外部评测\n两次盲评 · 聚焦测试 · 完成率 · 时间 · Token · Tool calls",
        "#F0EFEA",
        edge=INK,
        fontsize=10.5,
        weight="bold",
    )
    ax.add_patch(
        FancyArrowPatch(
            (11.9, 3.5),
            (11.55, 2.48),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.45,
            color=INK,
        )
    )
    ax.add_patch(
        FancyArrowPatch(
            (8.2, 1.91),
            (1.45, 3.5),
            connectionstyle="arc3,rad=-0.19",
            arrowstyle="-|>",
            mutation_scale=15,
            linewidth=1.8,
            color=GREEN,
        )
    )
    ax.text(4.35, 1.45, "接受：成为 Hₜ₊₁", color=GREEN, fontsize=11, weight="bold")
    ax.add_patch(
        FancyArrowPatch(
            (10.45, 1.33),
            (8.1, 0.74),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.5,
            color=RED,
        )
    )
    ax.text(6.05, 0.58, "拒绝：保存失败版本与反证，不修改当前 Harness", color=RED, fontsize=10.5, weight="bold")

    ax.add_patch(
        FancyBboxPatch(
            (0.35, 5.25),
            12.7,
            0.72,
            boxstyle="round,pad=0.02,rounding_size=0.025",
            facecolor="#F5F4F0",
            edgecolor=LINE,
            linewidth=1.0,
        )
    )
    ax.text(
        6.7,
        5.61,
        "不可由 Evolver 修改：冻结任务 · 代码起点 · 模型与推理强度 · Ground Truth · 评测器 · 权限边界",
        ha="center",
        va="center",
        fontsize=10.3,
        color=INK,
    )
    fig.text(
        0.06,
        0.025,
        "闭环中的 operator、candidate、trajectory reviewer/evolver 与 blind judge 均由独立 Agent 执行；评测证据和权限位于可编辑 Harness 之外。",
        fontsize=9.5,
        color=MUTED,
    )
    save(fig, "self-evolution-loop-matplotlib.png")


def cell_map(profiled: dict) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for arm in profiled["aggregateArms"]:
        result[arm["code"]] = arm
    return result


def task_values(profiled: dict, code: str, field: str) -> np.ndarray:
    values = []
    for task in profiled["tasks"]:
        cell = next(item for item in task["cells"] if item["code"] == code)
        values.append(float(cell[field]))
    return np.asarray(values, dtype=float)


def bootstrap_ci(values: np.ndarray, seed: int = 20260805, samples: int = 20000) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    draws = rng.choice(values, size=(samples, len(values)), replace=True).mean(axis=1)
    low, high = np.quantile(draws, [0.025, 0.975])
    return float(low), float(high)


def build_profile_baseline_interaction(profiled: dict) -> None:
    codes = {"H1 / Light": ("L0", "L1", BLUE), "H0 / Standard": ("S0", "S1", RED)}
    x = np.array([0, 1])
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.8), constrained_layout=True)
    metric_specs = [
        ("blindScore", "Blind score", "(A) Product quality"),
        ("tokensPerRun", "Agent tokens / run (M)", "(B) Context cost"),
    ]
    for ax, (field, ylabel, panel_title) in zip(axes, metric_specs):
        for label, (without_code, with_code, color) in codes.items():
            means = []
            lower = []
            upper = []
            for index, code in enumerate((without_code, with_code)):
                values = task_values(profiled, code, field)
                if field == "tokensPerRun":
                    values = values / 1_000_000
                mean = float(values.mean())
                lo, hi = bootstrap_ci(values, seed=20260805 + index + (0 if label == "Light" else 10))
                means.append(mean)
                lower.append(mean - lo)
                upper.append(hi - mean)
            means_array = np.asarray(means)
            ax.errorbar(
                x,
                means_array,
                yerr=np.asarray([lower, upper]),
                marker="o",
                markersize=5.5,
                linewidth=1.7,
                capsize=3.5,
                elinewidth=1.1,
                color=color,
                label=label,
            )
            for index, value in enumerate(means):
                ax.annotate(
                    f"{value:.1f}",
                    (index, value),
                    xytext=(6, 4),
                    textcoords="offset points",
                    fontsize=8,
                    color=color,
                )
        ax.set_xticks(x, ["No baseline", "Full baseline"])
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Project-level specification")
        ax.set_title(panel_title, loc="left", weight="semibold", pad=8)
        ax.grid(axis="y", color=LINE, alpha=0.5, linewidth=0.7)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].legend(frameon=False, loc="lower left")
    save(fig, "profile-baseline-interaction-matplotlib.png")


def build_quality_cost_evolution(profiled: dict, lean: dict) -> None:
    arms = cell_map(profiled)
    labels = ["Standard", "Light", "Lean"]
    scores = [arms["S1"]["blindScore"], arms["L0"]["blindScore"], lean["macro"]["leanScore"]]
    tokens = [arms["S1"]["tokensPerRun"] / 1_000_000, arms["L0"]["tokensPerRun"] / 1_000_000, lean["macro"]["agentTokensPerRun"] / 1_000_000]
    minutes = [arms["S1"]["activeMinutes"], arms["L0"]["activeMinutes"], lean["macro"]["agentMinutesPerRun"]]
    tools = [arms["S1"]["toolCallsPerRun"], arms["L0"]["toolCallsPerRun"], lean["macro"]["agentToolCallsPerRun"]]
    completion = [arms["S1"]["workflowCompleted"] / 24 * 100, arms["L0"]["workflowCompleted"] / 24 * 100, lean["macro"]["workflowCompleted"] / 24 * 100]
    labels = ["H0", "H1", "H12"]
    colors = [RED, BLUE, GREEN]

    fig, (ax_scatter, ax_cost) = plt.subplots(1, 2, figsize=(10.2, 4.1), constrained_layout=True)
    ax_scatter.plot(tokens, scores, color="#8A8A8A", linewidth=1.0, linestyle="--", zorder=1)
    ax_scatter.scatter(tokens, scores, s=82, c=colors, edgecolor="black", linewidth=0.6, zorder=3)
    for index, label in enumerate(labels):
        offset = (7, 5) if label != "H0" else (7, -15)
        ax_scatter.annotate(
            f"{label}  ({scores[index]:.1f}, {tokens[index]:.1f}M)",
            (tokens[index], scores[index]),
            xytext=offset,
            textcoords="offset points",
            fontsize=8.5,
            color=colors[index],
            weight="semibold",
        )
    ax_scatter.set_xlabel("Agent tokens / run (M)")
    ax_scatter.set_ylabel("Blind score")
    ax_scatter.set_xlim(2.7, 12.7)
    ax_scatter.set_ylim(70, 95.5)
    ax_scatter.grid(color=LINE, alpha=0.45, linewidth=0.7)
    ax_scatter.spines[["top", "right"]].set_visible(False)
    ax_scatter.set_title("(A) Quality–token position", loc="left", weight="semibold", pad=8)

    metric_labels = ["Tokens", "Active time", "Tool calls"]
    normalized = np.asarray(
        [
            np.asarray(tokens) / tokens[0] * 100,
            np.asarray(minutes) / minutes[0] * 100,
            np.asarray(tools) / tools[0] * 100,
        ]
    ).T
    x = np.arange(len(metric_labels))
    width = 0.23
    for index, (label, color) in enumerate(zip(labels, colors)):
        bars = ax_cost.bar(x + (index - 1) * width, normalized[index], width, label=label, color=color, edgecolor="black", linewidth=0.45)
        for bar, value in zip(bars, normalized[index]):
            ax_cost.text(bar.get_x() + bar.get_width() / 2, value + 2.5, f"{value:.0f}", ha="center", va="bottom", fontsize=7.5)
    ax_cost.axhline(100, color="#777777", linewidth=0.8, linestyle="--")
    ax_cost.set_xticks(x, metric_labels)
    ax_cost.set_ylabel("Cost relative to H0 (%)")
    ax_cost.set_ylim(0, 118)
    ax_cost.grid(axis="y", color=LINE, alpha=0.45, linewidth=0.7)
    ax_cost.spines[["top", "right"]].set_visible(False)
    ax_cost.set_title("(B) Resource use", loc="left", weight="semibold", pad=8)
    ax_cost.legend(frameon=False, ncol=3, loc="upper right")
    save(fig, "quality-cost-evolution-matplotlib.png")


def build_task_paired_scores(lean: dict) -> None:
    tasks = lean["tasks"]
    labels = [task["label"] for task in tasks]
    light_scores = np.asarray([task["l0Score"] for task in tasks], dtype=float)
    lean_scores = np.asarray([task["leanScore"] for task in tasks], dtype=float)
    differences = lean_scores - light_scores
    order = np.argsort(differences)
    labels = [labels[index] for index in order]
    light_scores = light_scores[order]
    lean_scores = lean_scores[order]
    differences = differences[order]

    low, high = bootstrap_ci(differences, seed=20260806)
    fig, ax = plt.subplots(figsize=(8.2, 4.9), constrained_layout=True)
    y = np.arange(len(labels))
    for index, (before, after, diff) in enumerate(zip(light_scores, lean_scores, differences)):
        color = GREEN if diff > 0 else (RED if diff < 0 else MUTED)
        ax.plot([before, after], [index, index], color=color, linewidth=1.8, alpha=0.75)
        ax.scatter(before, index, color=BLUE, s=42, edgecolor="black", linewidth=0.45, zorder=3)
        ax.scatter(after, index, color=GREEN if diff >= 0 else RED, s=42, edgecolor="black", linewidth=0.45, zorder=3)
        ax.text(max(before, after) + 0.45, index, f"{diff:+.1f}", va="center", fontsize=8, color=color)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Blind score (0–100)")
    ax.set_xlim(min(light_scores.min(), lean_scores.min()) - 4, 104)
    ax.grid(axis="x", color=LINE, alpha=0.45, linewidth=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.scatter([], [], color=BLUE, s=42, edgecolor="black", linewidth=0.45, label="H1")
    ax.scatter([], [], color=GREEN, s=42, edgecolor="black", linewidth=0.45, label="H12 gain / tie")
    ax.scatter([], [], color=RED, s=42, edgecolor="black", linewidth=0.45, label="H12 decline")
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("Task-level blind score", loc="left", weight="semibold", pad=18)
    ax.text(
        0,
        1.015,
        f"Mean Δ = {differences.mean():+.1f}; 95% task-bootstrap CI [{low:.1f}, {high:.1f}]",
        transform=ax.transAxes,
        fontsize=8.5,
        color=MUTED,
        va="bottom",
    )
    save(fig, "lean-light-task-paired-scores-matplotlib.png")


def main() -> None:
    configure_style()
    profiled, lean = load_reports()
    build_self_evolution_loop()
    build_profile_baseline_interaction(profiled)
    build_quality_cost_evolution(profiled, lean)
    build_task_paired_scores(lean)
    print(f"Figures written to {ASSETS}")


if __name__ == "__main__":
    main()
