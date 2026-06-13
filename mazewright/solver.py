"""Maze solving algorithms."""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazewright.maze import Maze

Position = tuple[int, int]


def solve_bfs(
    maze: Maze,
    start: Position = (0, 0),
    goal: Position | None = None,
) -> list[Position] | None:
    """Solve maze using breadth-first search.
    
    Args:
        maze: The maze to solve
        start: Starting cell coordinates
        goal: Goal cell coordinates. Defaults to bottom-right.
        
    Returns:
        List of (row, col) coordinates representing the solution path,
        or None if no solution exists
    """
    if goal is None:
        goal = (maze.rows - 1, maze.cols - 1)

    if not maze.in_bounds(*start):
        raise ValueError("Start cell is out of bounds")
    if not maze.in_bounds(*goal):
        raise ValueError("Goal cell is out of bounds")

    if start == goal:
        return [start]

    queue = deque([start])
    visited = {start}
    previous: dict[Position, Position | None] = {start: None}
    
    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbor in maze.open_neighbors(*current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            previous[neighbor] = current
            queue.append(neighbor)

    if goal not in previous:
        return None

    path = []
    current: Position | None = goal
    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return path
