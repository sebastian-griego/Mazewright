"""Tests for maze visualization functions."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from mazewright import generate
from mazewright.visualize import save, save_svg, save_ascii
from mazewright.solver import solve_bfs


class TestVisualization:
    """Test visualization functions."""

    def test_save_png(self) -> None:
        """Test saving maze as PNG."""
        maze = generate(5, 5)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "maze.png"
            save(maze, str(filepath))
            assert filepath.exists()
            assert filepath.stat().st_size > 0

    def test_save_png_with_solution(self) -> None:
        """Test saving maze with solution as PNG."""
        maze = generate(5, 5)
        solution = solve_bfs(maze)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "maze_solved.png"
            save(maze, str(filepath), solution_path=solution)
            assert filepath.exists()
            assert filepath.stat().st_size > 0

    def test_save_svg(self) -> None:
        """Test saving maze as SVG."""
        maze = generate(5, 5)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "maze.svg"
            save_svg(maze, str(filepath))
            assert filepath.exists()
            
            # Check SVG content
            content = filepath.read_text()
            assert "<svg" in content
            assert "</svg>" in content
            assert "line" in content  # Should have wall lines
            assert "circle" in content  # Start marker
            assert "rect" in content  # Finish marker

    def test_save_svg_with_solution(self) -> None:
        """Test saving maze with solution as SVG."""
        maze = generate(5, 5)
        solution = solve_bfs(maze)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "maze_solved.svg"
            save_svg(maze, str(filepath), solution_path=solution)
            assert filepath.exists()
            
            content = filepath.read_text()
            assert "<svg" in content
            assert "polyline" in content  # Solution path

    def test_save_ascii(self) -> None:
        """Test saving maze as ASCII art."""
        maze = generate(3, 3)
        
        # Test returning ASCII string
        ascii_str = save_ascii(maze)
        assert isinstance(ascii_str, str)
        assert "+" in ascii_str
        assert "-" in ascii_str
        assert "|" in ascii_str
        assert "S" in ascii_str  # Start marker
        assert "F" in ascii_str  # Finish marker
        
        # Test saving to file
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "maze.txt"
            save_ascii(maze, str(filepath))
            assert filepath.exists()
            
            content = filepath.read_text()
            assert content == ascii_str

    def test_save_ascii_with_solution(self) -> None:
        """Test saving maze with solution as ASCII art."""
        maze = generate(5, 5)
        solution = solve_bfs(maze)
        
        ascii_str = save_ascii(maze, solution_path=solution)
        assert isinstance(ascii_str, str)
        # Should have asterisks for solution path (except start/finish)
        # Count asterisks - should be len(solution) - 2 (excluding S and F)
        asterisk_count = ascii_str.count("*")
        expected_asterisks = len(solution) - 2 if solution else 0
        assert asterisk_count == expected_asterisks

    def test_ascii_dimensions(self) -> None:
        """Test ASCII output has correct dimensions."""
        rows, cols = 4, 5
        maze = generate(rows, cols)
        
        ascii_str = save_ascii(maze)
        lines = ascii_str.split("\n")
        
        # Each cell is 2 rows + 1 for borders
        expected_height = rows * 2 + 1
        assert len(lines) == expected_height
        
        # Each cell is 4 cols + 1 for borders
        expected_width = cols * 4 + 1
        assert all(len(line) == expected_width for line in lines)

    def test_svg_custom_colors(self) -> None:
        """Test SVG with custom colors."""
        maze = generate(3, 3)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "colored.svg"
            save_svg(
                maze, 
                str(filepath),
                wall_color="blue",
                background_color="yellow",
                solution_color="red"
            )
            
            content = filepath.read_text()
            assert 'stroke="blue"' in content
            assert 'fill="yellow"' in content