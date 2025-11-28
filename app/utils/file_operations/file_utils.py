"""
File path resolution utilities.

This module provides the FilePathResolver class for locating and validating
files across multiple directories.

For detailed documentation, see the module's README.md file.
"""

from pathlib import Path
from typing import Dict, Optional
from fastapi import HTTPException, status, Depends
from app.core.logging_config import get_logger
from app.core.dependencies import get_directories


logger = get_logger("file_utils")

class FilePathResolver:
    """
    File path resolver for locating files across directories.

    Resolves file paths across provided directories. Locates files by name
    and validates their existence.

    Args:
        directories (Dict[str, Path]): A dictionary of directories to search
            for files (e.g., {"uploaded": Path("/path/to/uploads")}).
    """

    def __init__(self, directories: Dict[str, Path]):
        """
        Initializes the FilePathResolver with the directories to search.

        Args:
            directories (Dict[str, Path]): A dictionary of directories to search
                for files (e.g., {"uploaded": Path("/path/to/uploads")}).
        """
        self.directories = directories
        logger.info("FileFinder initialized with directories: %s", self.directories)

    def _get_existing_file_path(self, filename: str) -> Optional[Path]:
        """
        Search through all directories for the specified file.

        Args:
            filename (str): The name of the file to search for.

        Returns:
            Optional[Path]: The path to the file if found, otherwise None.
        """
        for directory in self.directories.values():
            file_path = directory / filename
            if file_path.is_file():
                logger.debug(f"File found: {file_path}")
                return file_path
        logger.debug(f"File not found: {filename}")
        return None

    def find_file(self, filename: str) -> Path:
        """
        Finds a file by its name in the provided directories.

        Args:
            filename (str): The name of the file to search for.

        Returns:
            Path: The path to the file if found.

        Raises:
            HTTPException: If the file is not found in any directory.
        """
        file_path = self._get_existing_file_path(filename)
        if not file_path:
            logger.warning(f"No file named '{filename}' exists in any of the directories")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No file named '{filename}' exists"
            )
        logger.info(f"File found: {file_path}")
        return file_path

    def find_and_validate_image(self, image_name: str) -> str:
        """
        Finds and validates the existence of an image file by name.

        Args:
            image_name (str): The name of the image file to search for.

        Returns:
            str: The path to the image if found.

        Raises:
            HTTPException: If the image is not found.
        """
        image_path = self.find_file(image_name)
        if not image_path.exists():
            logger.warning(f"Image not found: {image_name}")
            raise HTTPException(status_code=404, detail="Image not found")
        logger.info(f"Image validated: {image_path}")
        return str(image_path)

def get_file_path_resolver(directories: Dict[str, Path] = Depends(get_directories)) -> FilePathResolver:
    """
    Creates an instance of FilePathResolver.

    Args:
        directories (Dict[str, Path]): A dictionary of directories provided by
            the dependency system.

    Returns:
        FilePathResolver: An instance of FilePathResolver.
    """
    logger.debug("Creating FilePathResolver instance with directories: %s", directories)
    return FilePathResolver(directories=directories)
