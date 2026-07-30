from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm


ARTICLE_ROOT = Path(__file__).resolve().parent
ASSETS = ARTICLE_ROOT / "assets"
EXPERIMENT_ROOT = ARTICLE_ROOT.parents[2] / "sdd-exp"
ECONOMICS = EXPERIMENT_ROOT / "reports" / "capability-task-economics.csv"

PAPER = "#ffffff"
PANEL = "#ffffff"
INK = "#17211b"
MUTED = "#667269"
GRID = "#ddd8cd"
GREEN = "#217a65"
RED = "#c4513f"
BLUE = "#1976a3"
PURPLE = "#73599a"
GOLD = "#a27a2c"
SLATE = "#536b78"

ARM_ORDER = ["Bare", "Grill Me", "OpenSpec", "Ponytail", "Superpowers", "MatrixSpec L0"]
ARM_COLORS = {
    "Bare": SLATE,
    "Grill Me": GREEN,
    "OpenSpec": GOLD,
    "Ponytail": PURPLE,
    "Superpowers": RED,
    "MatrixSpec L0": BLUE,
}
CAPABILITY_NAMES = {
    "bare": "Bare",
    "mattpocock-grill-me": "Grill Me",
    "fission-openspec": "OpenSpec",
    "ponytail-16f2980": "Ponytail",
    "superpowers-6.1.1": "Superpowers",
}
TASK_ORDER = [
    "cli_item_list_fields",
    "eslint_preserve_caught_error",
    "pytest_plugin_entry_points",
    "pytest_addini_type_expressions",
    "bat_sanitize",
    "sqlmodel_field_constraints",
    "axum_custom_executor",
    "prometheus_utf8_negotiation",
]
TASK_LABELS = {
    "cli_item_list_fields": "CLI\nfields",
    "eslint_preserve_caught_error": "ESLint\nerror class",
    "pytest_plugin_entry_points": "pytest\nplugin",
    "pytest_addini_type_expressions": "pytest\naddini",
    "bat_sanitize": "bat\nsanitize",
    "sqlmodel_field_constraints": "SQLModel\nconstraints",
    "axum_custom_executor": "Axum\nexecutor",
    "prometheus_utf8_negotiation": "Prometheus\nUTF-8",
}

# MatrixSpec L0 is the representative arm in the article. The historical
# economics CSV contains L1/S1 rows, so L0's published profiled values remain
# explicit here. Source: reports/capability-task-score-matrix.md.
MATRIXSPEC_L0_SCORES = {
    "cli_item_list_fields": 99.83,
    "eslint_preserve_caught_error": 100.00,
    "pytest_plugin_entry_points": 93.33,
    "pytest_addini_type_expressions": 85.50,
    "bat_sanitize": 86.83,
    "sqlmodel_field_constraints": 85.33,
    "axum_custom_executor": 91.50,
    "prometheus_utf8_negotiation": 79.83,
}

# Per-task complete hidden-suite pass counts for the five public capability
# arms, in TASK_ORDER. Sources are the frozen campaign comparison reports.
# L0's published 13/24 aggregate is from the complete profiled 2x2 report.
HIDDEN_PASS_BY_TASK = {
    "Bare": [3, 3, 3, 3, 2, 3, 0, 0],
    "Grill Me": [3, 3, 3, 3, 1, 3, 0, 0],
    "OpenSpec": [3, 3, 3, 3, 3, 1, 0, 0],
    "Ponytail": [3, 3, 2, 3, 3, 2, 0, 0],
    "Superpowers": [3, 3, 2, 3, 1, 3, 1, 0],
}
HIDDEN_PASSES = {arm: sum(values) for arm, values in HIDDEN_PASS_BY_TASK.items()}
HIDDEN_PASSES["MatrixSpec L0"] = 13

# Eight-task means of candidate session-tree tool calls per run. Sources are
# the frozen public-arm comparison reports and MatrixSpec L0 comparison reports.
TOOL_CALLS = {
    "Bare": 29.22,
    "Grill Me": 40.17,
    "OpenSpec": 44.25,
    "Ponytail": 38.15,
    "Superpowers": 157.43,
    "MatrixSpec L0": 123.00,
}

# Mean questions per Grill Me run. Sources: formal campaign summary JSON,
# operator-decisions.jsonl, and five-arm group summaries.
GRILL_QUESTIONS = {
    "cli_item_list_fields": 20.00,
    "eslint_preserve_caught_error": 25.33,
    "pytest_plugin_entry_points": 1.67,
    "pytest_addini_type_expressions": 6.67,
    "bat_sanitize": 6.67,
    "sqlmodel_field_constraints": 3.67,
    "axum_custom_executor": 5.67,
    "prometheus_utf8_negotiation": 7.00,
}

# Ponytail versus Bare task evidence. Source:
# reports/ponytail-deep-analysis.md, table in section 2.
PONYTAIL_TASKS = {
    "CLI": {"score_delta": 0.83, "token_ratio": 1.94, "code_delta": -17.1, "passes": 3},
    "ESLint": {"score_delta": -3.83, "token_ratio": 1.21, "code_delta": -8.8, "passes": 3},
    "pytest plugin": {"score_delta": -4.50, "token_ratio": 1.18, "code_delta": -24.5, "passes": 2},
    "pytest addini": {"score_delta": -1.67, "token_ratio": 1.40, "code_delta": -15.2, "passes": 3},
    "Axum": {"score_delta": -5.66, "token_ratio": 1.44, "code_delta": -36.9, "passes": 0},
    "bat": {"score_delta": 7.16, "token_ratio": 1.21, "code_delta": -7.8, "passes": 3},
    "Prometheus": {"score_delta": 3.00, "token_ratio": 2.23, "code_delta": -33.1, "passes": 0},
    "SQLModel": {"score_delta": -5.83, "token_ratio": 0.86, "code_delta": -24.2, "passes": 2},
}


def configure_style() -> None:
    for font_path in (Path(r"C:\Windows\Fonts\times.ttf"), Path(r"C:\Windows\Fonts\simsun.ttc")):
        if font_path.exists():
            font_manager.fontManager.addfont(str(font_path))
    plt.rcParams.update({
        "font.family": ["Times New Roman", "SimSun"],
        "font.size": 11,
        "axes.unicode_minus": False,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    })


def load_panel() -> dict[str, dict[str, dict[str, float]]]:
    panel: dict[str, dict[str, dict[str, float]]] = {}
    with ECONOMICS.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            name = CAPABILITY_NAMES.get(row["capability"])
            if name is None or row["task"] not in TASK_ORDER:
                continue
            panel.setdefault(name, {})[row["task"]] = {
                "score": float(row["score"]),
                "tokens": float(row["candidate_tokens_per_run"]) / 1_000_000,
            }
    panel["MatrixSpec L0"] = {
        task: {"score": score, "tokens": 8.57}
        for task, score in MATRIXSPEC_L0_SCORES.items()
    }
    expected = set(ARM_ORDER)
    if set(panel) != expected:
        raise ValueError(f"Unexpected panel arms: {sorted(panel)}")
    for arm in ARM_ORDER:
        missing = set(TASK_ORDER) - set(panel[arm])
        if missing:
            raise ValueError(f"Missing tasks for {arm}: {sorted(missing)}")
    return panel


def finish(fig: plt.Figure, name: str) -> None:
    path = ASSETS / name
    fig.savefig(path, dpi=180, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print(path)


def draw_delta_heatmap(panel: dict[str, dict[str, dict[str, float]]]) -> None:
    arms = [arm for arm in ARM_ORDER if arm != "Bare"]
    values = np.array([
        [panel[arm][task]["score"] - panel["Bare"][task]["score"] for task in TASK_ORDER]
        for arm in arms
    ])
    means = values.mean(axis=1, keepdims=True)
    display = np.concatenate([values, means], axis=1)
    cmap = LinearSegmentedColormap.from_list("delta", ["#b9483a", "#ffffff", "#23856d"])
    norm = TwoSlopeNorm(vmin=-46, vcenter=0, vmax=46)

    fig, ax = plt.subplots(figsize=(16, 7.8), dpi=180)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PANEL)
    image = ax.imshow(display, cmap=cmap, norm=norm, aspect="auto")

    labels = [TASK_LABELS[task] for task in TASK_ORDER] + ["Mean"]
    ax.set_xticks(range(len(labels)), labels, fontsize=11)
    ax.set_yticks(range(len(arms)), arms, fontsize=12)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False, length=0, pad=10)

    for row in range(display.shape[0]):
        for col in range(display.shape[1]):
            value = display[row, col]
            color = "white" if abs(value) >= 25 else INK
            weight = "bold" if col == display.shape[1] - 1 else "normal"
            ax.text(col, row, f"{value:+.1f}", ha="center", va="center",
                    fontsize=12, fontweight=weight, color=color)

    ax.axvline(7.5, color="#6f786f", linewidth=2.4)
    ax.set_xticks(np.arange(-0.5, display.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, display.shape[0], 1), minor=True)
    ax.grid(which="minor", color="#eee9df", linewidth=1.4)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title("Task-level blind-score differences relative to Bare", fontsize=20, loc="left", pad=50)
    colorbar = fig.colorbar(image, ax=ax, orientation="horizontal", fraction=0.04, pad=0.13, aspect=45)
    colorbar.set_label("Blind-score difference", fontsize=11, color=MUTED)
    colorbar.outline.set_visible(False)
    finish(fig, "task-arm-delta-heatmap-matplotlib.png")


def draw_three_metric_panel(panel: dict[str, dict[str, dict[str, float]]]) -> None:
    scores = {arm: np.mean([panel[arm][task]["score"] for task in TASK_ORDER]) for arm in ARM_ORDER}
    tokens = {
        arm: np.mean([panel[arm][task]["tokens"] for task in TASK_ORDER])
        for arm in ARM_ORDER if arm != "MatrixSpec L0"
    }
    tokens["MatrixSpec L0"] = 8.57
    metrics = [
        ("Blind score", scores, (68, 93), 70),
        ("Tool calls / run", TOOL_CALLS, (0, 175), 0),
        ("Candidate tokens / run", tokens, (0, 25), 0),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 8.8), dpi=180, sharey=True,
                             gridspec_kw={"wspace": 0.12})
    fig.patch.set_facecolor(PAPER)
    y = np.arange(len(ARM_ORDER))
    for index, (title, values, limits, origin) in enumerate(metrics):
        ax = axes[index]
        ax.set_facecolor(PANEL)
        ax.set_xlim(*limits)
        ax.set_ylim(-0.65, len(ARM_ORDER) - 0.35)
        ax.invert_yaxis()
        ax.grid(axis="x", color=GRID, linewidth=1.0)
        ax.set_axisbelow(True)
        for row, arm in enumerate(ARM_ORDER):
            value = values[arm]
            ax.hlines(row, origin, value, color=ARM_COLORS[arm], linewidth=3.2, alpha=0.68)
            ax.scatter(value, row, s=190, color=ARM_COLORS[arm], edgecolor="white",
                       linewidth=1.5, zorder=3)
            if index == 0:
                label = f"{value:.2f}"
            elif index == 1:
                label = f"{value:.1f}"
            else:
                label = f"{value:.2f}M"
            if index == 0:
                offset = 0.8
            elif index == 1:
                offset = -4.0 if value > 150 else 4.0
            else:
                offset = -0.8 if value > 21 else 0.8
            ha = "left" if offset > 0 else "right"
            ax.text(value + offset, row, label, va="center", ha=ha, fontsize=10.5,
                    color=ARM_COLORS[arm], zorder=4)
        ax.set_title(title, fontsize=16, pad=16)
        for spine in ("top", "right", "left"):
            ax.spines[spine].set_visible(False)
        ax.spines["bottom"].set_color("#69756d")
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(y, ARM_ORDER, fontsize=12)
    for tick, arm in zip(axes[0].get_yticklabels(), ARM_ORDER):
        tick.set_color(ARM_COLORS[arm])

    fig.suptitle("Quality and resource use", fontsize=22, x=0.07, ha="left", y=0.96)
    fig.subplots_adjust(left=0.17, right=0.98, top=0.84, bottom=0.10)
    finish(fig, "score-tools-token-three-metrics-matplotlib.png")


def draw_grill_scatter(panel: dict[str, dict[str, dict[str, float]]]) -> None:
    deltas = {
        task: panel["Grill Me"][task]["score"] - panel["Bare"][task]["score"]
        for task in TASK_ORDER
    }
    ratios = {
        task: panel["Grill Me"][task]["tokens"] / panel["Bare"][task]["tokens"]
        for task in TASK_ORDER
    }
    names = {
        "cli_item_list_fields": "CLI",
        "eslint_preserve_caught_error": "ESLint",
        "pytest_plugin_entry_points": "pytest plugin",
        "pytest_addini_type_expressions": "pytest addini",
        "bat_sanitize": "bat",
        "sqlmodel_field_constraints": "SQLModel",
        "axum_custom_executor": "Axum",
        "prometheus_utf8_negotiation": "Prometheus",
    }
    offsets = {
        "CLI": (-2.2, -4.2), "ESLint": (-4.7, 3.0), "pytest plugin": (0.8, 2.3),
        "pytest addini": (0.8, 2.8), "bat": (0.8, -4.2), "SQLModel": (0.8, -3.5),
        "Axum": (0.8, 2.6), "Prometheus": (0.8, -3.8),
    }

    fig, ax = plt.subplots(figsize=(16, 8.8), dpi=180)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PANEL)
    ax.axhline(0, color="#59665e", linewidth=1.7)
    ax.grid(color=GRID, linewidth=1.0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 29)
    ax.set_ylim(-22, 51)

    for task in TASK_ORDER:
        name = names[task]
        x = GRILL_QUESTIONS[task]
        y = deltas[task]
        ratio = ratios[task]
        size = 170 + 230 * ratio
        color = GREEN if y > 0 else RED
        ax.scatter(x, y, s=size, color=color, alpha=0.88, edgecolor="white",
                   linewidth=1.8, zorder=3)
        dx, dy = offsets[name]
        ax.text(x + dx, y + dy, f"{name}\n{y:+.1f} | {ratio:.2f}× tokens",
                fontsize=10.8, color=color)

    for ratio, x in [(1.0, 18.5), (2.0, 22.0)]:
        ax.scatter(x, -17.2, s=170 + 230 * ratio, color="#9aa49e", alpha=0.65,
                   edgecolor="white", linewidth=1.3)
        ax.text(x + 0.7, -17.2, f"{ratio:.0f}× tokens", va="center", fontsize=9.5, color=MUTED)

    ax.set_title("Grill Me: questions and blind-score differences", fontsize=20, loc="left", pad=24)
    ax.set_xlabel("Operator questions / run", fontsize=13, labelpad=14)
    ax.set_ylabel("Blind-score difference relative to Bare", fontsize=13, labelpad=14)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#59665e")
    fig.subplots_adjust(left=0.09, right=0.97, top=0.84, bottom=0.13)
    finish(fig, "grill-questions-score-delta-matplotlib.png")


def draw_ponytail_evidence() -> None:
    fig, (ax_left, ax_right) = plt.subplots(
        1, 2, figsize=(16, 8.8), dpi=180, gridspec_kw={"width_ratios": [0.86, 1.35], "wspace": 0.24}
    )
    fig.patch.set_facecolor(PAPER)
    for ax in (ax_left, ax_right):
        ax.set_facecolor(PANEL)

    metric_labels = ["Added code", "Candidate tokens", "Tool calls", "Wall time", "Blind score"]
    metric_values = [79.5, 144.5, 130.6, 139.2, 98.2]
    metric_text = ["−20.5%", "+44.5%", "+30.6%", "+39.2%", "−1.8%"]
    metric_colors = [PURPLE, RED, RED, RED, SLATE]
    y = np.arange(len(metric_labels))
    ax_left.axvline(100, color="#4f5c54", linewidth=1.8)
    for row, (value, text_value, color) in enumerate(zip(metric_values, metric_text, metric_colors)):
        ax_left.hlines(row, min(100, value), max(100, value), color=color, linewidth=4, alpha=0.72)
        ax_left.scatter(value, row, s=220, color=color, edgecolor="white", linewidth=1.6, zorder=3)
        offset = 3 if value >= 100 else 2
        ax_left.text(value + offset, row, text_value, va="center",
                     ha="left", fontsize=11.5,
                     fontweight="bold", color=color)
    ax_left.set_yticks(y, metric_labels, fontsize=12)
    ax_left.tick_params(axis="y", pad=12)
    ax_left.invert_yaxis()
    ax_left.set_xlim(70, 154)
    ax_left.set_xlabel("Bare = 100", fontsize=11.5, labelpad=10)
    ax_left.grid(axis="x", color=GRID, linewidth=1.0)
    ax_left.set_axisbelow(True)
    ax_left.set_title("Aggregate metrics", fontsize=16, pad=16)

    for name, item in PONYTAIL_TASKS.items():
        size = 130 + 145 * item["token_ratio"] ** 2
        ax_right.scatter(item["code_delta"], item["score_delta"], s=size,
                         color=PURPLE,
                         edgecolor="white", linewidth=1.6, alpha=0.9, zorder=3)
    label_offsets = {
        "CLI": (-1.2, 1.2), "ESLint": (1.0, 0.5), "pytest plugin": (1.0, 0.5),
        "pytest addini": (-7.8, 1.1), "Axum": (1.0, 0.5), "bat": (1.0, -1.2),
        "Prometheus": (-0.2, 1.3), "SQLModel": (-0.2, -1.3),
    }
    for name, item in PONYTAIL_TASKS.items():
        dx, dy = label_offsets[name]
        ax_right.text(item["code_delta"] + dx, item["score_delta"] + dy, name,
                      fontsize=10.5, color=INK)
    ax_right.axhline(0, color="#59665e", linewidth=1.6)
    ax_right.axvline(0, color="#59665e", linewidth=1.6)
    ax_right.set_xlim(-41, 1)
    ax_right.set_ylim(-8.5, 10.0)
    ax_right.grid(color=GRID, linewidth=1.0)
    ax_right.set_axisbelow(True)
    ax_right.set_xlabel("Added-code difference relative to Bare (%)", fontsize=11.5, labelpad=10)
    ax_right.set_ylabel("Blind-score difference relative to Bare", fontsize=11.5, labelpad=10)
    ax_right.set_title("Task-level results", fontsize=16, pad=16)

    for ratio, x in [(1.0, -38), (2.0, -31.5)]:
        ax_right.scatter(x, 8.1, s=130 + 145 * ratio ** 2, color="#9aa49e", alpha=0.62,
                         edgecolor="white", linewidth=1.2)
        ax_right.text(x + 1.6, 8.1, f"{ratio:.0f}× tokens", va="center", fontsize=9.3, color=MUTED)

    for ax in (ax_left, ax_right):
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color("#59665e")

    fig.suptitle("Ponytail relative to Bare", fontsize=22, x=0.06, ha="left", y=0.96)
    fig.subplots_adjust(left=0.10, right=0.98, top=0.84, bottom=0.12)
    finish(fig, "ponytail-evidence-matplotlib.png")


def main() -> None:
    configure_style()
    ASSETS.mkdir(parents=True, exist_ok=True)
    panel = load_panel()

    assert round(np.mean([panel["Bare"][task]["score"] for task in TASK_ORDER]), 2) == 73.54
    assert round(np.mean([panel["MatrixSpec L0"][task]["score"] for task in TASK_ORDER]), 2) == 90.27
    assert HIDDEN_PASSES["Bare"] == 17 and HIDDEN_PASSES["MatrixSpec L0"] == 13

    draw_three_metric_panel(panel)
    draw_delta_heatmap(panel)
    draw_grill_scatter(panel)
    draw_ponytail_evidence()


if __name__ == "__main__":
    main()
