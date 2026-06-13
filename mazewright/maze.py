"""Core maze data structure and utilities."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import IntFlag
from typing import Iterator


class Wall(IntFlag):
    """Wall flags for each cell."""

    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL = NORTH | EAST | SOUTH | WEST


@dataclass
class Cell:
    """A single cell in the maze grid."""

    row: int
    col: int
    walls: Wall = field(default_factory=lambda: Wall.ALL)

    def remove_wall(self, direction: Wall) -> None:
        """Remove a wall in the given direction."""
        self.walls &= ~direction

    def has_wall(self, direction: Wall) -> bool:
        """Check if a wall exists in the given direction."""
        return bool(self.walls & direction)


class Maze:
    """A rectangular grid maze."""

    def __init__(self, rows: int, cols: int) -> None:
        """Initialize a maze with all walls intact.

        Args:
            rows: Number of rows in the maze
            cols: Number of columns in the maze
        """
        if rows <= 0 or cols <= 0:
            raise ValueError("Maze dimensions must be positive")

        self.rows = rows
        self.cols = cols
        self.grid: list[list[Cell]] = [
            [Cell(r, c) for c in range(cols)] for r in range(rows)
        ]

    def __getitem__(self, pos: tuple[int, int]) -> Cell:
        """Get cell at position (row, col)."""
        row, col = pos
        return self.grid[row][col]

    def in_bounds(self, row: int, col: int) -> bool:
        """Check if position is within maze boundaries."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def neighbors(self, row: int, col: int) -> Iterator[tuple[int, int, Wall, Wall]]:
        """Yield valid neighbors with their directions.

        Yields:
            (neighbor_row, neighbor_col, direction_to_neighbor, opposite_direction)
        """
        directions = [
            (row - 1, col, Wall.NORTH, Wall.SOUTH),  # North
            (row, col + 1, Wall.EAST, Wall.WEST),  # East
            (row + 1, col, Wall.SOUTH, Wall.NORTH),  # South
            (row, col - 1, Wall.WEST, Wall.EAST),  # West
        ]

        for nr, nc, direction, opposite in directions:
            if self.in_bounds(nr, nc):
                yield nr, nc, direction, opposite

    def open_neighbors(self, row: int, col: int) -> Iterator[tuple[int, int]]:
        """Yield neighboring cells connected by carved passages."""
        if not self.in_bounds(row, col):
            raise ValueError("Cell position out of bounds")

        cell = self[row, col]
        for nr, nc, direction, _ in self.neighbors(row, col):
            if not cell.has_wall(direction):
                yield nr, nc

    def carve(self, r1: int, c1: int, r2: int, c2: int) -> None:
        """Carve a passage between two adjacent cells.

        Args:
            r1, c1: First cell position
            r2, c2: Second cell position

        Raises:
            ValueError: If cells are not adjacent
        """
        if not (self.in_bounds(r1, c1) and self.in_bounds(r2, c2)):
            raise ValueError("Cell positions out of bounds")

        # Check if cells are adjacent
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            raise ValueError("Cells must be adjacent")

        # Determine direction and carve
        if r2 == r1 - 1:  # r2 is north of r1
            self.grid[r1][c1].remove_wall(Wall.NORTH)
            self.grid[r2][c2].remove_wall(Wall.SOUTH)
        elif r2 == r1 + 1:  # r2 is south of r1
            self.grid[r1][c1].remove_wall(Wall.SOUTH)
            self.grid[r2][c2].remove_wall(Wall.NORTH)
        elif c2 == c1 + 1:  # c2 is east of c1
            self.grid[r1][c1].remove_wall(Wall.EAST)
            self.grid[r2][c2].remove_wall(Wall.WEST)
        else:  # c2 is west of c1
            self.grid[r1][c1].remove_wall(Wall.WEST)
            self.grid[r2][c2].remove_wall(Wall.EAST)

    def all_cells(self) -> Iterator[Cell]:
        """Iterate over all cells in the maze."""
        for row in self.grid:
            yield from row

    def carved_edges(self) -> int:
        """Count carved passages between adjacent cells."""
        edges = 0
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self[row, col]
                if col < self.cols - 1 and not cell.has_wall(Wall.EAST):
                    edges += 1
                if row < self.rows - 1 and not cell.has_wall(Wall.SOUTH):
                    edges += 1
        return edges

    def is_connected(self) -> bool:
        """Return True if every cell is reachable through carved passages."""
        visited = {(0, 0)}
        queue = deque([(0, 0)])

        while queue:
            row, col = queue.popleft()
            for neighbor in self.open_neighbors(row, col):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return len(visited) == self.rows * self.cols

    def is_perfect(self) -> bool:
        """Return True if the maze is connected and has no cycles."""
        return self.carved_edges() == self.rows * self.cols - 1 and self.is_connected()

    def reset(self) -> None:
        """Reset maze to initial state with all walls."""
        for cell in self.all_cells():
            cell.walls = Wall.ALL
