"""Command-line interface for mazewright."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mazewright import generate
from mazewright.visualize import save, save_svg, save_ascii
from mazewright.solver import solve_bfs


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
        help="Output file path (default: maze.png). Supports .png, .svg, .txt extensions",
    )
    
    parser.add_argument(
        "--format",
        choices=["auto", "png", "svg", "ascii"],
        default="auto",
        help="Output format (default: auto-detect from file extension)",
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

    parser.add_argument(
        "--solved",
        action="store_true",
        help="Show solution path on the maze",
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

        # Solve maze if requested
        solution_path = None
        if args.solved:
            print("Solving maze...")
            solution_path = solve_bfs(maze)
            if solution_path is None:
                print("Warning: No solution found for this maze!", file=sys.stderr)

        # Determine output format
        output_format = args.format
        if output_format == "auto":
            ext = args.output.suffix.lower()
            if ext == ".svg":
                output_format = "svg"
            elif ext in [".txt", ".ascii"]:
                output_format = "ascii"
            else:
                output_format = "png"
        
        # Save visualization
        print(f"Saving to {args.output} as {output_format.upper()}...")
        
        if output_format == "svg":
            save_svg(
                maze,
                str(args.output),
                cell_size=args.cell_size,
                wall_width=args.wall_width,
                solution_path=solution_path,
            )
        elif output_format == "ascii":
            ascii_output = save_ascii(
                maze,
                str(args.output),
                solution_path=solution_path,
            )
            # Also print to console for ASCII
            print("\nGenerated maze:")
            print(ascii_output)
        else:  # png
            save(
                maze,
                str(args.output),
                cell_size=args.cell_size,
                wall_width=args.wall_width,
                solution_path=solution_path,
            )

        if args.solved and solution_path:
            print(f"Success! Maze with solution saved to {args.output}")
        else:
            print(f"Success! Maze saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()