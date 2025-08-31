"""Maze solving algorithms."""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazewright.maze import Maze

from mazewright.maze import Wall


def solve_bfs(maze: Maze) -> list[tuple[int, int]] | None:
    """Solve maze using breadth-first search.
    
    Args:
        maze: The maze to solve
        
    Returns:
        List of (row, col) coordinates representing the solution path,
        or None if no solution exists
    """
    start = (0, 0)  # Top-left corner
    end = (maze.rows - 1, maze.cols - 1)  # Bottom-right corner
    
    if not maze.in_bounds(*start) or not maze.in_bounds(*end):
        return None
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        (row, col), path = queue.popleft()
        
        if (row, col) == end:
            return path
            
        cell = maze[row, col]
        
        # Check all four directions
        directions = [
            (-1, 0, Wall.NORTH),  # North
            (0, 1, Wall.EAST),    # East
            (1, 0, Wall.SOUTH),   # South
            (0, -1, Wall.WEST),   # West
        ]
        
        for dr, dc, wall_dir in directions:
            new_row, new_col = row + dr, col + dc
            
            if (new_row, new_col) in visited:
                continue
                
            if not maze.in_bounds(new_row, new_col):
                continue
                
            # Check if there's a wall blocking this direction
            if cell.has_wall(wall_dir):
                continue
                
            visited.add((new_row, new_col))
            queue.append(((new_row, new_col), path + [(new_row, new_col)]))
    
    return None  # No solution found