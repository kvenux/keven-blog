"""Render an article-ready comparison with trajectory-visualizer.

The upstream plotter places right-aligned step counts partly over the final
trajectory cell. This wrapper adds display-only right padding while preserving
the parser, lane layout, stage classification, colors, and plotter itself.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--visualizer-root", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sys.path.insert(0, str(args.visualizer_root.resolve()))
    from matplotlib.axes import Axes
    from src import load_config
    from src.render.plotter import plot_session_tree
    from src.render.style import apply_style

    app_config = load_config(str(args.config))
    style_config = apply_style(app_config.get("style", {}))
    tree = json.loads(args.tree.read_text(encoding="utf-8"))

    original_set_xlim = Axes.set_xlim
    original_text = Axes.text

    def set_xlim_with_count_margin(self, left=None, right=None, *positional, **keyword):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)) and left < 0 < 40 < right:
            right += 0.9
        return original_set_xlim(self, left, right, *positional, **keyword)

    def text_with_separate_step_count(self, x, y, value, *positional, **keyword):
        if isinstance(value, str) and value.isdigit() and isinstance(x, (int, float)) and x > 40:
            x += 0.65
        return original_text(self, x, y, value, *positional, **keyword)

    Axes.set_xlim = set_xlim_with_count_margin
    Axes.text = text_with_separate_step_count
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        plot_session_tree(tree, str(args.output), style_cfg=style_config)
    finally:
        Axes.set_xlim = original_set_xlim
        Axes.text = original_text


if __name__ == "__main__":
    main()
