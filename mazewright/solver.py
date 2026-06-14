"""Maze solving algorithms."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from mazewright.maze import Maze

Position = tuple[int, int]
SolverName = Literal["bfs", "astar"]


@dataclass(frozen=True)
class SolveResult:
    """Path and search-effort metrics for a solver run."""

    path: list[Position] | None
    explored: int
    visited: int

    @property
    def path_length(self) -> int | None:
        """Number of cells in the path, or None when the maze is unsolved."""
        return None if self.path is None else len(self.path)


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
    return solve_with_metrics(maze, start=start, goal=goal, algorithm="bfs").path


def solve_astar(
    maze: Maze,
    start: Position = (0, 0),
    goal: Position | None = None,
) -> list[Position] | None:
    """Solve maze using A* search with Manhattan-distance guidance."""
    return solve_with_metrics(maze, start=start, goal=goal, algorithm="astar").path


def solve_with_metrics(
    maze: Maze,
    start: Position = (0, 0),
    goal: Position | None = None,
    algorithm: SolverName = "bfs",
) -> SolveResult:
    """Solve a maze and return both the path and search-effort metrics."""
    goal = _normalize_goal(maze, goal)
    _validate_endpoint(maze, start, "Start")
    _validate_endpoint(maze, goal, "Goal")

    if algorithm == "bfs":
        return _solve_bfs_result(maze, start, goal)
    if algorithm == "astar":
        return _solve_astar_result(maze, start, goal)
    raise ValueError("Unknown solver: {0}. Choose from: bfs, astar".format(algorithm))


def _solve_bfs_result(maze: Maze, start: Position, goal: Position) -> SolveResult:
    queue = deque([start])
    visited = {start}
    previous: dict[Position, Position | None] = {start: None}
    explored = 0

    while queue:
        current = queue.popleft()
        explored += 1

        if current == goal:
            break

        for neighbor in maze.open_neighbors(*current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            previous[neighbor] = current
            queue.append(neighbor)

    if goal not in previous:
        return SolveResult(path=None, explored=explored, visited=len(visited))

    return SolveResult(
        path=_reconstruct_path(previous, goal),
        explored=explored,
        visited=len(visited),
    )


def _solve_astar_result(maze: Maze, start: Position, goal: Position) -> SolveResult:
    open_heap: list[tuple[int, int, int, Position]] = []
    counter = 0
    heappush(
        open_heap, (_manhattan(start, goal), _manhattan(start, goal), counter, start)
    )
    previous: dict[Position, Position | None] = {start: None}
    g_score = {start: 0}
    closed: set[Position] = set()
    explored = 0

    while open_heap:
        _, _, _, current = heappop(open_heap)
        if current in closed:
            continue

        closed.add(current)
        explored += 1
        if current == goal:
            break

        for neighbor in maze.open_neighbors(*current):
            tentative = g_score[current] + 1
            if tentative >= g_score.get(neighbor, 10**12):
                continue
            previous[neighbor] = current
            g_score[neighbor] = tentative
            counter += 1
            heuristic = _manhattan(neighbor, goal)
            heappush(open_heap, (tentative + heuristic, heuristic, counter, neighbor))

    if goal not in previous:
        return SolveResult(path=None, explored=explored, visited=len(g_score))

    return SolveResult(
        path=_reconstruct_path(previous, goal),
        explored=explored,
        visited=len(g_score),
    )


def _normalize_goal(maze: Maze, goal: Position | None) -> Position:
    return (maze.rows - 1, maze.cols - 1) if goal is None else goal


def _validate_endpoint(maze: Maze, position: Position, label: str) -> None:
    if not maze.in_bounds(*position):
        raise ValueError(f"{label} cell is out of bounds")


def _reconstruct_path(
    previous: dict[Position, Position | None],
    goal: Position,
) -> list[Position]:
    path: list[Position] = []
    current: Position | None = goal
    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return path


def _manhattan(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
