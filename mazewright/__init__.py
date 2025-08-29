"""Mazewright: A Python package for generating and visualizing mazes."""

from __future__ import annotations

from typing import Literal

from mazewright.maze import Cell, Maze, Wall
from mazewright.algorithms import backtracker, kruskal, prim

__version__ = "0.1.0"
__all__ = ["Maze", "Cell", "Wall", "generate"]

AlgorithmType = Literal["backtracker", "prim", "kruskal"]


def generate(
    rows: int,
    cols: int,
    algorithm: AlgorithmType = "backtracker",
) -> Maze:
    """Generate a maze using the specified algorithm.

    Args:
        rows: Number of rows in the maze
        cols: Number of columns in the maze
        algorithm: Algorithm to use ("backtracker", "prim", or "kruskal")

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

    algorithms[algorithm](maze)
    return maze