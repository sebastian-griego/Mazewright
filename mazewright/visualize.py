"""Maze visualization using matplotlib."""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

if TYPE_CHECKING:
    from mazewright.maze import Maze

from mazewright.maze import Wall


def render(
    maze: Maze,
    cell_size: float = 1.0,
    wall_width: float = 2.0,
    wall_color: str = "black",
    background_color: str = "white",
    start_finish_color: str = "red",
    solution_path: list[tuple[int, int]] | None = None,
    solution_color: str = "blue",
) -> plt.Figure:
    """Render a maze as line segments using matplotlib.

    Args:
        maze: The maze to render
        cell_size: Size of each cell in the plot
        wall_width: Width of wall lines
        wall_color: Color of walls
        background_color: Background color
        start_finish_color: Color for start/finish markers
        solution_path: Optional path coordinates to highlight
        solution_color: Color for solution path

    Returns:
        The matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(maze.cols * cell_size, maze.rows * cell_size))

    # Collect wall segments
    segments = []
    
    # Add outer border walls (always present)
    # Top border
    segments.append([(0, maze.rows * cell_size), (maze.cols * cell_size, maze.rows * cell_size)])
    # Bottom border
    segments.append([(0, 0), (maze.cols * cell_size, 0)])
    # Left border
    segments.append([(0, 0), (0, maze.rows * cell_size)])
    # Right border
    segments.append([(maze.cols * cell_size, 0), (maze.cols * cell_size, maze.rows * cell_size)])

    for row in range(maze.rows):
        for col in range(maze.cols):
            cell = maze[row, col]

            # Calculate cell boundaries in plot coordinates
            # Note: matplotlib y-axis is inverted, so we flip it
            x_left = col * cell_size
            x_right = (col + 1) * cell_size
            y_top = (maze.rows - row) * cell_size
            y_bottom = (maze.rows - row - 1) * cell_size

            # Only add internal walls to avoid duplicates at borders
            # North wall (only if not at top edge)
            if row > 0 and cell.has_wall(Wall.NORTH):
                segments.append([(x_left, y_top), (x_right, y_top)])
            
            # South wall (only if not at bottom edge)
            if row < maze.rows - 1 and cell.has_wall(Wall.SOUTH):
                segments.append([(x_left, y_bottom), (x_right, y_bottom)])
            
            # West wall (only if not at left edge)
            if col > 0 and cell.has_wall(Wall.WEST):
                segments.append([(x_left, y_bottom), (x_left, y_top)])
            
            # East wall (only if not at right edge)
            if col < maze.cols - 1 and cell.has_wall(Wall.EAST):
                segments.append([(x_right, y_bottom), (x_right, y_top)])

    # Create line collection and add to axes
    lc = LineCollection(segments, linewidths=wall_width, colors=wall_color)
    ax.add_collection(lc)
    
    # Draw solution path if provided
    if solution_path and len(solution_path) > 1:
        path_x = []
        path_y = []
        for row, col in solution_path:
            # Convert maze coordinates to plot coordinates
            x = (col + 0.5) * cell_size
            y = (maze.rows - row - 0.5) * cell_size
            path_x.append(x)
            path_y.append(y)
        
        ax.plot(path_x, path_y, color=solution_color, linewidth=wall_width * 1.5, 
                linestyle='-', alpha=0.8, zorder=10)
    
    # Add start and finish markers
    # Start at top-left corner
    start_x = 0.5 * cell_size
    start_y = (maze.rows - 0.5) * cell_size
    ax.plot(start_x, start_y, 'o', color=start_finish_color, markersize=cell_size * 8, label='Start')
    
    # Finish at bottom-right corner
    finish_x = (maze.cols - 0.5) * cell_size
    finish_y = 0.5 * cell_size
    ax.plot(finish_x, finish_y, 's', color=start_finish_color, markersize=cell_size * 8, label='Finish')

    # Set plot properties with padding to ensure border walls are fully visible
    padding = wall_width / 50  # Padding based on wall width to prevent clipping
    ax.set_xlim(-padding, maze.cols * cell_size + padding)
    ax.set_ylim(-padding, maze.rows * cell_size + padding)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(background_color)
    fig.patch.set_facecolor(background_color)

    # Remove margins
    plt.tight_layout(pad=0)

    return fig


def save(
    maze: Maze,
    filename: str,
    cell_size: float = 20.0,
    wall_width: float = 2.0,
    dpi: int = 100,
    start_finish_color: str = "red",
    solution_path: list[tuple[int, int]] | None = None,
    solution_color: str = "blue",
) -> None:
    """Save a maze visualization to file.

    Args:
        maze: The maze to save
        filename: Output filename
        cell_size: Size of each cell in pixels
        wall_width: Width of wall lines
        dpi: Dots per inch for output
        start_finish_color: Color for start/finish markers
        solution_path: Optional path coordinates to highlight
        solution_color: Color for solution path
    """
    # Convert cell_size from pixels to inches for matplotlib
    cell_size_inches = cell_size / dpi

    fig = render(
        maze,
        cell_size=cell_size_inches,
        wall_width=wall_width,
        start_finish_color=start_finish_color,
        solution_path=solution_path,
        solution_color=solution_color,
    )

    fig.savefig(filename, dpi=dpi, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)