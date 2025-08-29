"""Prim's algorithm for maze generation (frontier growth)."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazewright.maze import Maze


def generate(maze: Maze) -> None:
    """Generate a maze using Prim's algorithm.

    This algorithm grows the maze from a starting cell by maintaining a
    frontier of walls between visited and unvisited cells, randomly
    selecting walls to remove.

    Args:
        maze: The maze to generate into (will be modified in-place)
    """
    # Reset maze to all walls
    maze.reset()

    # Track visited cells
    visited = [[False] * maze.cols for _ in range(maze.rows)]

    # Frontier: list of (row, col, neighbor_row, neighbor_col) tuples
    frontier: list[tuple[int, int, int, int]] = []

    # Start from random cell
    start_row = random.randint(0, maze.rows - 1)
    start_col = random.randint(0, maze.cols - 1)

    # Mark starting cell as visited
    visited[start_row][start_col] = True

    # Add all walls of starting cell to frontier
    for nr, nc, _, _ in maze.neighbors(start_row, start_col):
        if not visited[nr][nc]:
            frontier.append((start_row, start_col, nr, nc))

    while frontier:
        # Pick random wall from frontier
        idx = random.randint(0, len(frontier) - 1)
        r1, c1, r2, c2 = frontier.pop(idx)

        # If the neighbor hasn't been visited
        if not visited[r2][c2]:
            # Carve passage
            maze.carve(r1, c1, r2, c2)

            # Mark neighbor as visited
            visited[r2][c2] = True

            # Add neighbor's walls to frontier
            for nr, nc, _, _ in maze.neighbors(r2, c2):
                if not visited[nr][nc]:
                    # Avoid duplicates by checking if wall already in frontier
                    wall = (r2, c2, nr, nc)
                    if wall not in frontier:
                        frontier.append(wall)