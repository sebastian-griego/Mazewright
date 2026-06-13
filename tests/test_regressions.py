from __future__ import annotations

import pytest

from mazewright import Maze, generate, solve_bfs


def maze_signature(maze: Maze) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(int(cell.walls) for cell in row) for row in maze.grid)


def test_seeded_generation_is_reproducible_for_all_algorithms() -> None:
    for algorithm in ("backtracker", "prim", "kruskal"):
        first = generate(8, 8, algorithm=algorithm, seed=123)
        second = generate(8, 8, algorithm=algorithm, seed=123)
        different = generate(8, 8, algorithm=algorithm, seed=456)

        assert first.is_perfect()
        assert maze_signature(first) == maze_signature(second)
        assert maze_signature(first) != maze_signature(different)


def test_maze_validation_helpers() -> None:
    maze = Maze(2, 2)
    assert maze.carved_edges() == 0
    assert not maze.is_connected()
    assert not maze.is_perfect()

    maze.carve(0, 0, 0, 1)
    maze.carve(0, 1, 1, 1)
    maze.carve(1, 1, 1, 0)

    assert maze.carved_edges() == 3
    assert maze.is_connected()
    assert maze.is_perfect()
    assert set(maze.open_neighbors(0, 1)) == {(0, 0), (1, 1)}


def test_solver_supports_custom_start_and_goal() -> None:
    maze = generate(6, 6, seed=99)
    path = solve_bfs(maze, start=(0, 5), goal=(5, 0))

    assert path is not None
    assert path[0] == (0, 5)
    assert path[-1] == (5, 0)

    for (row, col), (next_row, next_col) in zip(path, path[1:]):
        assert abs(row - next_row) + abs(col - next_col) == 1


def test_solver_rejects_out_of_bounds_endpoints() -> None:
    maze = generate(3, 3, seed=1)

    with pytest.raises(ValueError, match="Start"):
        solve_bfs(maze, start=(-1, 0))
    with pytest.raises(ValueError, match="Goal"):
        solve_bfs(maze, goal=(3, 0))


def test_open_neighbors_rejects_out_of_bounds_cell() -> None:
    maze = Maze(1, 1)

    with pytest.raises(ValueError, match="out of bounds"):
        list(maze.open_neighbors(1, 0))
