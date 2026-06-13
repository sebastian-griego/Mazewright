"""Mazewright: A Python package for generating and visualizing mazes."""

from __future__ import annotations

import random
from typing import Literal

from mazewright.maze import Cell, Maze, Wall
from mazewright.algorithms import backtracker, kruskal, prim
from mazewright.solver import solve_bfs

__version__ = "0.2.0"
__all__ = ["Maze", "Cell", "Wall", "generate", "solve_bfs"]

AlgorithmType = Literal["backtracker", "prim", "kruskal"]
SeedType = int | float | str | bytes | bytearray | None


def generate(
    rows: int,
    cols: int,
    algorithm: AlgorithmType = "backtracker",
    seed: SeedType = None,
) -> Maze:
    """Generate a maze using the specified algorithm.

    Args:
        rows: Number of rows in the maze
        cols: Number of columns in the maze
        algorithm: Algorithm to use ("backtracker", "prim", or "kruskal")
        seed: Optional random seed for reproducible maze generation

    Returns:
        Generated maze

    Raises:
        ValueError: If algorithm is not recognized

    Example:
        >>> from mazewright import generate
        >>> maze = generate(10, 10, algorithm="prim")
    """
    # Create empty maze
    maze = Maze(rows, cols)

    # Select and run algorithm
    algorithms = {
        "backtracker": backtracker.generate,
        "prim": prim.generate,
        "kruskal": kruskal.generate,
    }

    if algorithm not in algorithms:
        raise ValueError(
            f"Unknown algorithm: {algorithm}. "
            f"Choose from: {', '.join(algorithms.keys())}"
        )

    rng = random.Random(seed) if seed is not None else None
    algorithms[algorithm](maze, rng=rng)
    return maze
