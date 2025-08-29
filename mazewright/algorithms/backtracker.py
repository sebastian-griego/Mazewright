"""Recursive backtracker maze generation algorithm (iterative DFS)."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazewright.maze import Maze


def generate(maze: Maze) -> None:
    """Generate a maze using recursive backtracker (iterative DFS).

    This algorithm performs a randomized depth-first search through the grid,
    carving passages as it goes and backtracking when it hits dead ends.

    Args:
        maze: The maze to generate into (will be modified in-place)
    """
    # Reset maze to all walls
    maze.reset()

    # Stack for DFS
    stack: list[tuple[int, int]] = []

    # Track visited cells
    visited = [[False] * maze.cols for _ in range(maze.rows)]

    # Start from random cell
    start_row = random.randint(0, maze.rows - 1)
    start_col = random.randint(0, maze.cols - 1)

    # Mark starting cell as visited and push to stack
    visited[start_row][start_col] = True
    stack.append((start_row, start_col))

    while stack:
        current_row, current_col = stack[-1]

        # Get unvisited neighbors
        unvisited_neighbors = []
        for nr, nc, direction, opposite in maze.neighbors(current_row, current_col):
            if not visited[nr][nc]:
                unvisited_neighbors.append((nr, nc, direction, opposite))

        if unvisited_neighbors:
            # Choose random unvisited neighbor
            nr, nc, direction, opposite = random.choice(unvisited_neighbors)

            # Carve passage between current and chosen neighbor
            maze.carve(current_row, current_col, nr, nc)

            # Mark neighbor as visited and push to stack
            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            # Dead end, backtrack
            stack.pop()