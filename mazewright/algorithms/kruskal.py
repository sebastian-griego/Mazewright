"""Kruskal's algorithm for maze generation using union-find."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazewright.maze import Maze


class UnionFind:
    """Lightweight union-find (disjoint set) data structure."""

    def __init__(self, size: int) -> None:
        """Initialize union-find for given number of elements.

        Args:
            size: Number of elements (cells in maze)
        """
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        """Find root of element with path compression.

        Args:
            x: Element to find root of

        Returns:
            Root element
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union two sets by rank.

        Args:
            x: First element
            y: Second element

        Returns:
            True if sets were merged, False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same set

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


def generate(maze: Maze) -> None:
    """Generate a maze using Kruskal's algorithm.

    This algorithm treats the maze as a graph where cells are nodes and
    walls are edges. It randomly selects walls to remove, only removing
    a wall if it connects two disconnected regions.

    Args:
        maze: The maze to generate into (will be modified in-place)
    """
    # Reset maze to all walls
    maze.reset()

    # Create union-find structure
    num_cells = maze.rows * maze.cols
    uf = UnionFind(num_cells)

    # Helper to convert (row, col) to single index
    def cell_index(row: int, col: int) -> int:
        return row * maze.cols + col

    # Collect all possible walls (edges between cells)
    walls: list[tuple[int, int, int, int]] = []

    for row in range(maze.rows):
        for col in range(maze.cols):
            # Only add walls to neighbors that come after in iteration order
            # to avoid duplicates
            if col < maze.cols - 1:  # East wall
                walls.append((row, col, row, col + 1))
            if row < maze.rows - 1:  # South wall
                walls.append((row, col, row + 1, col))

    # Shuffle walls for random selection
    random.shuffle(walls)

    # Process walls
    for r1, c1, r2, c2 in walls:
        idx1 = cell_index(r1, c1)
        idx2 = cell_index(r2, c2)

        # If cells are in different sets, carve passage and union
        if uf.find(idx1) != uf.find(idx2):
            maze.carve(r1, c1, r2, c2)
            uf.union(idx1, idx2)