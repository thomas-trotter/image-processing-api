"""
Cleanup utilities for removing temporary files and cache directories.

This module provides functions for cleaning up temporary files and cache
directories created during application execution.

For detailed documentation, see the module's README.md file.
"""

from pathlib import Path
import shutil

from app.core.logging_config import get_logger

logger = get_logger("clean_up")

def clean_up(directory: Path) -> None:
    """
    Recursively removes __pycache__ directories from the given directory tree.

    Searches for all __pycache__ directories within the specified directory
    and removes them. This is useful for cleaning up Python bytecode cache
    files after application shutdown.

    Args:
        directory (Path): The root directory to search for __pycache__ folders.

    Returns:
        None

    Note:
        Errors during removal are logged but do not stop the cleanup process.
    """
    for pycache in directory.rglob("__pycache__"):
        if pycache.is_dir():
            try:
                shutil.rmtree(pycache)
                logger.info(f"Successfully removed {pycache}")
            except Exception as e:
                logger.error(f"Failed to remove {pycache}: {e}")
