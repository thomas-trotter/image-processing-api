"""
Dependency injection functions for core application dependencies.

This module provides FastAPI dependency functions for commonly used
configuration and utility objects throughout the application.

For detailed documentation, see the module's README.md file.
"""

from typing import Dict
from pathlib import Path
from app.core.config import settings
from app.core.logging_config import get_logger


logger = get_logger("dependencies")


def get_directories() -> Dict[str, Path]:
    """
    Retrieves the configured storage directories.

    Returns a dictionary mapping directory keys to their Path objects.
    This is used as a FastAPI dependency to provide directory paths
    to route handlers and services.

    Returns:
        Dict[str, Path]: Mapping directory keys to their Path objects:
            - "uploaded": folder for uploaded images
            - "edited": folder for edited images
            - "detected": folder for detection output
    """
    dirs = {
        "uploaded": settings.UPLOADED_FOLDER,
        "edited": settings.EDITED_FOLDER,
        "detected": settings.DETECTED_FOLDER
    }
    logger.debug(f"Configured directories: {dirs}")
    return dirs

def get_format_extensions() -> Dict[str, str]:
    """
    Retrieves the mapping from image format names to file extensions.

    Returns a dictionary that maps image format strings to their
    corresponding file extensions. Used for format validation and
    file naming operations.

    Returns:
        Dict[str, str]: Mapping format strings (e.g., "JPEG", "PNG") to their
            corresponding file extension (e.g., ".jpg", ".png").
            Supported formats: JPEG, JPG, PNG, GIF, BMP, TIFF, WEBP.
    """
    fmt_ext = {
        "JPEG": ".jpg",
        "JPG": ".jpg",
        "PNG": ".png",
        "GIF": ".gif",
        "BMP": ".bmp",
        "TIFF": ".tiff",
        "WEBP": ".webp"
    }
    logger.debug(f"Supported format extensions: {fmt_ext}")
    return fmt_ext
