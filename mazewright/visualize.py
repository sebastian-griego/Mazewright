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
) -> plt.Figure:
    """Render a maze as line segments using matplotlib.

    Args:
        maze: The maze to render
        cell_size: Size of each cell in the plot
        wall_width: Width of wall lines
        wall_color: Color of walls
        background_color: Background color

    Returns:
        The matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(maze.cols * cell_size, maze.rows * cell_size))

    # Collect wall segments
    segments = []

    for row in range(maze.rows):
        for col in range(maze.cols):
            cell = maze[row, col]

            # Calculate cell boundaries in plot coordinates
            # Note: matplotlib y-axis is inverted, so we flip it
            x_left = col * cell_size
            x_right = (col + 1) * cell_size
            y_top = (maze.rows - row) * cell_size
            y_bottom = (maze.rows - row - 1) * cell_size

            # Add wall segments based on cell walls
            if cell.has_wall(Wall.NORTH):
                segments.append([(x_left, y_top), (x_right, y_top)])
            if cell.has_wall(Wall.SOUTH):
                segments.append([(x_left, y_bottom), (x_right, y_bottom)])
            if cell.has_wall(Wall.WEST):
                segments.append([(x_left, y_bottom), (x_left, y_top)])
            if cell.has_wall(Wall.EAST):
                segments.append([(x_right, y_bottom), (x_right, y_top)])

    # Create line collection and add to axes
    lc = LineCollection(segments, linewidths=wall_width, colors=wall_color)
    ax.add_collection(lc)

    # Set plot properties
    ax.set_xlim(0, maze.cols * cell_size)
    ax.set_ylim(0, maze.rows * cell_size)
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
) -> None:
    """Save a maze visualization to file.

    Args:
        maze: The maze to save
        filename: Output filename
        cell_size: Size of each cell in pixels
        wall_width: Width of wall lines
        dpi: Dots per inch for output
    """
    # Convert cell_size from pixels to inches for matplotlib
    cell_size_inches = cell_size / dpi

    fig = render(
        maze,
        cell_size=cell_size_inches,
        wall_width=wall_width,
    )

    fig.savefig(filename, dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)