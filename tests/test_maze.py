"""Tests for maze generation and validation."""

from __future__ import annotations

from collections import deque

import pytest

from mazewright import Maze, Wall, generate


def is_perfect_maze(maze: Maze) -> bool:
    """Check if a maze is perfect (all cells reachable, no cycles).

    A perfect maze has exactly rows*cols-1 carved edges and all cells
    are reachable from any starting point.

    Args:
        maze: The maze to validate

    Returns:
        True if maze is perfect
    """
    # Count carved edges
    carved_edges = 0
    for row in range(maze.rows):
        for col in range(maze.cols):
            cell = maze[row, col]
            # Only count edges going right or down to avoid duplicates
            if col < maze.cols - 1 and not cell.has_wall(Wall.EAST):
                carved_edges += 1
            if row < maze.rows - 1 and not cell.has_wall(Wall.SOUTH):
                carved_edges += 1

    expected_edges = maze.rows * maze.cols - 1
    if carved_edges != expected_edges:
        return False

    # Check all cells are reachable using BFS
    visited = [[False] * maze.cols for _ in range(maze.rows)]
    queue = deque([(0, 0)])
    visited[0][0] = True
    reachable_count = 1

    while queue:
        row, col = queue.popleft()
        cell = maze[row, col]

        # Check each direction
        directions = [
            (row - 1, col, Wall.NORTH),
            (row, col + 1, Wall.EAST),
            (row + 1, col, Wall.SOUTH),
            (row, col - 1, Wall.WEST),
        ]

        for nr, nc, wall_dir in directions:
            if (
                maze.in_bounds(nr, nc)
                and not visited[nr][nc]
                and not cell.has_wall(wall_dir)
            ):
                visited[nr][nc] = True
                reachable_count += 1
                queue.append((nr, nc))

    return reachable_count == maze.rows * maze.cols


class TestMazeDataStructure:
    """Test the Maze data structure."""

    def test_maze_creation(self) -> None:
        """Test maze initialization."""
        maze = Maze(5, 5)
        assert maze.rows == 5
        assert maze.cols == 5

        # All walls should be up initially
        for row in range(5):
            for col in range(5):
                cell = maze[row, col]
                assert cell.has_wall(Wall.NORTH)
                assert cell.has_wall(Wall.EAST)
                assert cell.has_wall(Wall.SOUTH)
                assert cell.has_wall(Wall.WEST)

    def test_invalid_dimensions(self) -> None:
        """Test that invalid dimensions raise errors."""
        with pytest.raises(ValueError):
            Maze(0, 5)
        with pytest.raises(ValueError):
            Maze(5, 0)
        with pytest.raises(ValueError):
            Maze(-1, 5)

    def test_carve_passage(self) -> None:
        """Test carving passages between cells."""
        maze = Maze(3, 3)

        # Carve from (0,0) to (0,1)
        maze.carve(0, 0, 0, 1)

        assert not maze[0, 0].has_wall(Wall.EAST)
        assert not maze[0, 1].has_wall(Wall.WEST)

        # Other walls should remain
        assert maze[0, 0].has_wall(Wall.NORTH)
        assert maze[0, 0].has_wall(Wall.SOUTH)
        assert maze[0, 0].has_wall(Wall.WEST)

    def test_carve_invalid(self) -> None:
        """Test that carving non-adjacent cells raises error."""
        maze = Maze(3, 3)

        with pytest.raises(ValueError):
            maze.carve(0, 0, 2, 2)  # Not adjacent

        with pytest.raises(ValueError):
            maze.carve(0, 0, 5, 5)  # Out of bounds


class TestAlgorithms:
    """Test maze generation algorithms."""

    @pytest.mark.parametrize("algorithm", ["backtracker", "prim", "kruskal"])
    def test_algorithm_creates_perfect_maze(self, algorithm: str) -> None:
        """Test that each algorithm creates a perfect maze."""
        maze = generate(10, 10, algorithm=algorithm)
        assert is_perfect_maze(maze)

    @pytest.mark.parametrize("algorithm", ["backtracker", "prim", "kruskal"])
    def test_different_sizes(self, algorithm: str) -> None:
        """Test algorithms with different maze sizes."""
        sizes = [(5, 5), (10, 15), (20, 10), (1, 10), (10, 1)]

        for rows, cols in sizes:
            maze = generate(rows, cols, algorithm=algorithm)
            assert maze.rows == rows
            assert maze.cols == cols
            assert is_perfect_maze(maze)

    @pytest.mark.parametrize("algorithm", ["backtracker", "prim", "kruskal"])
    def test_single_cell(self, algorithm: str) -> None:
        """Test algorithms with single cell maze."""
        maze = generate(1, 1, algorithm=algorithm)
        assert maze.rows == 1
        assert maze.cols == 1
        # Single cell should have all walls (no passages to carve)
        cell = maze[0, 0]
        assert cell.has_wall(Wall.NORTH)
        assert cell.has_wall(Wall.EAST)
        assert cell.has_wall(Wall.SOUTH)
        assert cell.has_wall(Wall.WEST)


class TestAPI:
    """Test the public API."""

    def test_generate_function(self) -> None:
        """Test the main generate function."""
        maze = generate(8, 8)
        assert isinstance(maze, Maze)
        assert is_perfect_maze(maze)

    def test_invalid_algorithm(self) -> None:
        """Test that invalid algorithm raises error."""
        with pytest.raises(ValueError, match="Unknown algorithm"):
            generate(5, 5, algorithm="invalid")  # type: ignore