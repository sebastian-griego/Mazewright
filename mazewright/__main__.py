"""Command-line interface for mazewright."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mazewright import generate
from mazewright.visualize import save


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="mazewright",
        description="Generate and visualize mazes",
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=10,
        help="Number of rows (default: 10)",
    )

    parser.add_argument(
        "--cols",
        type=int,
        default=10,
        help="Number of columns (default: 10)",
    )

    parser.add_argument(
        "--algo",
        "--algorithm",
        dest="algorithm",
        choices=["backtracker", "prim", "kruskal"],
        default="backtracker",
        help="Generation algorithm (default: backtracker)",
    )

    parser.add_argument(
        "--out",
        "--output",
        dest="output",
        type=Path,
        default=Path("maze.png"),
        help="Output file path (default: maze.png)",
    )

    parser.add_argument(
        "--cell-size",
        type=float,
        default=20.0,
        help="Cell size in pixels (default: 20)",
    )

    parser.add_argument(
        "--wall-width",
        type=float,
        default=2.0,
        help="Wall width in pixels (default: 2)",
    )

    args = parser.parse_args()

    # Validate arguments
    if args.rows <= 0 or args.cols <= 0:
        print("Error: Maze dimensions must be positive", file=sys.stderr)
        sys.exit(1)

    try:
        # Generate maze
        print(f"Generating {args.rows}x{args.cols} maze using {args.algorithm}...")
        maze = generate(args.rows, args.cols, algorithm=args.algorithm)

        # Save visualization
        print(f"Saving to {args.output}...")
        save(
            maze,
            str(args.output),
            cell_size=args.cell_size,
            wall_width=args.wall_width,
        )

        print(f"Success! Maze saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()