# Mazewright

Mazewright is a Python package for generating, solving, and visualizing perfect
rectangular mazes.

## Features

- Recursive Backtracker, Prim's, and Kruskal's generation algorithms
- Reproducible maze generation with `seed=...`
- Built-in maze validation helpers for connected/perfect mazes
- Breadth-first and A* solvers with custom start/goal cells and search metrics
- PNG, SVG, and ASCII rendering
- Command-line interface

## Installation

```bash
pip install mazewright
```

For development:

```bash
git clone https://github.com/sebastian-griego/Mazewright.git
cd Mazewright
python -m pip install -e ".[dev]"
python -m pytest
```

## Quick Start

```python
from mazewright import generate, solve_astar, solve_with_metrics
from mazewright.visualize import save

maze = generate(20, 20, algorithm="prim", seed=123)
assert maze.is_perfect()

path = solve_astar(maze)
result = solve_with_metrics(maze, algorithm="astar")
print(result.path_length, result.explored, result.visited)
save(maze, "my_maze.png", solution_path=path)
```

## Command Line

```bash
python -m mazewright
python -m mazewright --rows 30 --cols 30 --algo kruskal --seed 123 --out maze.png
python -m mazewright --out maze.svg
python -m mazewright --out maze.txt
python -m mazewright --format ascii
python -m mazewright --rows 15 --cols 20 --cell-size 25 --wall-width 3 --solved
python -m mazewright --rows 25 --cols 25 --solved --solver astar --stats
```

## API

```python
from mazewright import Maze, Wall, generate, solve_astar, solve_bfs, solve_with_metrics

maze = generate(rows=10, cols=10, algorithm="backtracker", seed=123)

cell = maze[0, 0]
if cell.has_wall(Wall.NORTH):
    print("Wall to the north")

maze.carve(0, 0, 0, 1)
print(maze.carved_edges())
print(maze.is_connected())
print(maze.is_perfect())

path = solve_bfs(maze, start=(0, 0), goal=(9, 9))
astar_path = solve_astar(maze)
metrics = solve_with_metrics(maze, algorithm="astar")
print(metrics.path_length, metrics.explored, metrics.visited)
```

Available algorithms:

- `backtracker`: randomized depth-first search
- `prim`: randomized frontier growth
- `kruskal`: randomized union-find spanning tree

## Rendering

```python
from mazewright.visualize import render, save, save_svg, save_ascii

fig = render(maze, cell_size=1.0, wall_width=2.0)
save(maze, "output.png", cell_size=20, wall_width=2, dpi=100)
save_svg(maze, "output.svg", cell_size=20, wall_width=2)

ascii_str = save_ascii(maze)
save_ascii(maze, "output.txt")
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
black mazewright tests
ruff check mazewright tests
```

## Architecture

```text
mazewright/
|-- __init__.py         # Public API
|-- maze.py             # Core data structures
|-- solver.py           # BFS/A* path solving and metrics
|-- visualize.py        # Rendering engine
|-- algorithms/
|   |-- backtracker.py  # Recursive backtracker
|   |-- prim.py         # Prim's algorithm
|   `-- kruskal.py      # Kruskal's with union-find
`-- __main__.py         # CLI entry point
```

## License

MIT
