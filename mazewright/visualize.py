"""Maze visualization using matplotlib, SVG, and ASCII."""

from __future__ import annotations

from typing import TYPE_CHECKING
from io import StringIO

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
    # Start at top-left corner (green circle)
    start_x = 0.5 * cell_size
    start_y = (maze.rows - 0.5) * cell_size
    ax.plot(start_x, start_y, 'o', color='green', markersize=cell_size * 12, label='Start')
    
    # Finish at bottom-right corner (red square)
    finish_x = (maze.cols - 0.5) * cell_size
    finish_y = 0.5 * cell_size
    ax.plot(finish_x, finish_y, 's', color='red', markersize=cell_size * 12, label='Finish')

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


def save_svg(
    maze: Maze,
    filename: str,
    cell_size: float = 20.0,
    wall_width: float = 2.0,
    wall_color: str = "black",
    background_color: str = "white",
    start_finish_color: str = "red",
    solution_path: list[tuple[int, int]] | None = None,
    solution_color: str = "blue",
) -> None:
    """Save a maze as an SVG file.
    
    Args:
        maze: The maze to save
        filename: Output filename (should end with .svg)
        cell_size: Size of each cell in pixels
        wall_width: Width of wall lines
        wall_color: Color of walls
        background_color: Background color
        start_finish_color: Color for start/finish markers
        solution_path: Optional path coordinates to highlight
        solution_color: Color for solution path
    """
    width = maze.cols * cell_size
    height = maze.rows * cell_size
    
    svg_content = StringIO()
    svg_content.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')
    svg_content.write(f'  <rect width="{width}" height="{height}" fill="{background_color}"/>\n')
    
    # Draw solution path first (so it appears under walls)
    if solution_path and len(solution_path) > 1:
        path_points = []
        for row, col in solution_path:
            x = (col + 0.5) * cell_size
            y = (row + 0.5) * cell_size
            path_points.append(f"{x},{y}")
        
        points_str = " ".join(path_points)
        svg_content.write(f'  <polyline points="{points_str}" fill="none" stroke="{solution_color}" '
                         f'stroke-width="{wall_width * 1.5}" opacity="0.8"/>\n')
    
    # Draw walls
    svg_content.write(f'  <g stroke="{wall_color}" stroke-width="{wall_width}" stroke-linecap="square">\n')
    
    # Draw outer borders
    svg_content.write(f'    <line x1="0" y1="0" x2="{width}" y2="0"/>\n')  # Top
    svg_content.write(f'    <line x1="0" y1="{height}" x2="{width}" y2="{height}"/>\n')  # Bottom
    svg_content.write(f'    <line x1="0" y1="0" x2="0" y2="{height}"/>\n')  # Left
    svg_content.write(f'    <line x1="{width}" y1="0" x2="{width}" y2="{height}"/>\n')  # Right
    
    # Draw internal walls
    for row in range(maze.rows):
        for col in range(maze.cols):
            cell = maze[row, col]
            
            x_left = col * cell_size
            x_right = (col + 1) * cell_size
            y_top = row * cell_size
            y_bottom = (row + 1) * cell_size
            
            # Only draw internal walls to avoid duplicates
            if row > 0 and cell.has_wall(Wall.NORTH):
                svg_content.write(f'    <line x1="{x_left}" y1="{y_top}" x2="{x_right}" y2="{y_top}"/>\n')
            
            if row < maze.rows - 1 and cell.has_wall(Wall.SOUTH):
                svg_content.write(f'    <line x1="{x_left}" y1="{y_bottom}" x2="{x_right}" y2="{y_bottom}"/>\n')
            
            if col > 0 and cell.has_wall(Wall.WEST):
                svg_content.write(f'    <line x1="{x_left}" y1="{y_top}" x2="{x_left}" y2="{y_bottom}"/>\n')
            
            if col < maze.cols - 1 and cell.has_wall(Wall.EAST):
                svg_content.write(f'    <line x1="{x_right}" y1="{y_top}" x2="{x_right}" y2="{y_bottom}"/>\n')
    
    svg_content.write('  </g>\n')
    
    # Draw start and finish markers
    start_x = 0.5 * cell_size
    start_y = 0.5 * cell_size
    svg_content.write(f'  <circle cx="{start_x}" cy="{start_y}" r="{cell_size * 0.3}" '
                     f'fill="green" opacity="0.8"/>\n')
    
    finish_x = (maze.cols - 0.5) * cell_size
    finish_y = (maze.rows - 0.5) * cell_size
    svg_content.write(f'  <rect x="{finish_x - cell_size * 0.3}" y="{finish_y - cell_size * 0.3}" '
                     f'width="{cell_size * 0.6}" height="{cell_size * 0.6}" '
                     f'fill="red" opacity="0.8"/>\n')
    
    svg_content.write('</svg>\n')
    
    with open(filename, 'w') as f:
        f.write(svg_content.getvalue())


def save_ascii(
    maze: Maze,
    filename: str | None = None,
    solution_path: list[tuple[int, int]] | None = None,
) -> str:
    """Save or return a maze as ASCII art.
    
    Args:
        maze: The maze to render
        filename: Optional output filename. If None, returns the ASCII string
        solution_path: Optional path coordinates to mark with asterisks
        
    Returns:
        The ASCII representation of the maze (also written to file if filename provided)
    """
    # Create a 2D grid for the ASCII representation
    # Each cell needs 3x3 characters to show walls and paths
    ascii_height = maze.rows * 2 + 1
    ascii_width = maze.cols * 4 + 1
    grid = [[' ' for _ in range(ascii_width)] for _ in range(ascii_height)]
    
    # Convert solution path to set for quick lookup
    solution_set = set(solution_path) if solution_path else set()
    
    # Draw the maze
    for row in range(maze.rows):
        for col in range(maze.cols):
            cell = maze[row, col]
            
            # Calculate position in ASCII grid
            ascii_row = row * 2
            ascii_col = col * 4
            
            # Draw corners
            grid[ascii_row][ascii_col] = '+'
            grid[ascii_row][ascii_col + 4] = '+'
            grid[ascii_row + 2][ascii_col] = '+'
            grid[ascii_row + 2][ascii_col + 4] = '+'
            
            # Draw walls
            if cell.has_wall(Wall.NORTH):
                for i in range(1, 4):
                    grid[ascii_row][ascii_col + i] = '-'
            
            if cell.has_wall(Wall.SOUTH):
                for i in range(1, 4):
                    grid[ascii_row + 2][ascii_col + i] = '-'
            
            if cell.has_wall(Wall.WEST):
                grid[ascii_row + 1][ascii_col] = '|'
            
            if cell.has_wall(Wall.EAST):
                grid[ascii_row + 1][ascii_col + 4] = '|'
            
            # Mark solution path
            if (row, col) in solution_set:
                grid[ascii_row + 1][ascii_col + 2] = '*'
            
            # Mark start and finish
            if row == 0 and col == 0:
                grid[ascii_row + 1][ascii_col + 2] = 'S'
            elif row == maze.rows - 1 and col == maze.cols - 1:
                grid[ascii_row + 1][ascii_col + 2] = 'F'
    
    # Convert grid to string
    ascii_str = '\n'.join(''.join(row) for row in grid)
    
    if filename:
        with open(filename, 'w') as f:
            f.write(ascii_str)
    
    return ascii_str