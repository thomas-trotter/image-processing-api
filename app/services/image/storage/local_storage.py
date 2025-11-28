"""
Local filesystem image storage implementation.

This module provides the LocalImageStorage class for saving, retrieving,
and deleting images on the local filesystem.

For detailed documentation, see the module's README.md file.
"""

from fastapi import UploadFile, HTTPException, Depends, status
from PIL import Image, UnidentifiedImageError
from typing import Optional, Annotated
from pathlib import Path
import uuid
import os

from app.core.logging_config import get_logger
from app.services.image.storage.base_storage import BaseImageStorage
from app.utils.file_operations.directory_utils import DirectoryManager, get_directory_manager
from app.utils.validator.simple_validator import SimpleImageValidator, get_simple_image_validator
from app.utils.file_operations.file_utils import FilePathResolver, get_file_path_resolver

logger = get_logger("local_storage")


DirectoryManagerDep = Annotated[DirectoryManager, Depends(get_directory_manager)]
SimpleImageValidatorDep = Annotated[SimpleImageValidator, Depends(get_simple_image_validator)]
FilePathResolverDep = Annotated[FilePathResolver, Depends(get_file_path_resolver)]


class LocalImageStorage(BaseImageStorage):
    """
    Local image storage implementation.

    Saves, retrieves, and deletes images in a specified directory on the
    local filesystem. Validates image formats and handles file operations.

    Args:
        directory_manager (DirectoryManager): Handles directory operations like
            fetching the correct folder paths.
        image_validator (SimpleImageValidator): Validates the image formats and extensions.
        file_resolver (FilePathResolver): Helps in finding a file in the local system.
    """
    
    def __init__(self,
                 directory_manager: DirectoryManagerDep,
                 image_validator: SimpleImageValidatorDep,
                 file_resolver: FilePathResolverDep):
        """
        Initializes LocalImageStorage with required dependencies.

        Args:
            directory_manager (DirectoryManager): Handles directory operations like
                fetching the correct folder paths.
            image_validator (SimpleImageValidator): Validates the image formats and extensions.
            file_resolver (FilePathResolver): Helps in finding a file in the local system.
        """
        self.directory_manager = directory_manager
        self.image_verifier = image_validator
        self.file_resolver = file_resolver

    def _get_file_name(self, filename: Optional[str], format: str = "JPEG") -> str:
        """
        Generates a unique filename for the image.

        Args:
            filename (Optional[str]): Optional filename provided by the user.
            format (str): The desired format for the image. Defaults to "JPEG".

        Returns:
            str: A valid file name with the appropriate extension. If no filename
                is provided, generates a UUID-based filename.
        """
        format = self.image_verifier.validate_format(format)
        ext = self.image_verifier.get_extension(format)

        if filename is None:
            return f"{uuid.uuid4()}{ext}"

        filename = Path(filename).stem
        return f"{filename}{ext}"

    def save(self, file: UploadFile, folder: Optional[str] = "uploaded", filename: Optional[str] = None, format: str = "JPEG") -> str:
        """
        Saves an uploaded image to the local storage.

        Validates the image, generates a filename if needed, and saves it to
        the specified folder. Removes invalid files if saving fails.

        Args:
            file (UploadFile): The image file uploaded by the user.
            folder (Optional[str]): The folder where the image will be saved.
                Defaults to "uploaded".
            filename (Optional[str]): The optional name to save the file as.
                If not provided, a UUID-based filename is generated.
            format (str): The format to save the file as. Defaults to "JPEG".

        Returns:
            str: The storage path of the saved image.

        Raises:
            HTTPException: If the file is not a valid image or saving fails.
        """
        filename = self._get_file_name(filename, format)
        directory = self.directory_manager.get_directory(folder)
        file_path = directory / filename

        try:
            with Image.open(file.file) as img:
                img.save(file_path, format=format.upper())
            logger.info(f"Saved image: {file_path}")
            return str(file_path)

        except UnidentifiedImageError:
            if file_path.exists():
                os.remove(file_path)
            logger.error(f"Uploaded file is not a valid image: {file_path}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is not a valid image")

        except Exception as e:
            if file_path.exists():
                os.remove(file_path)
            logger.error(f"Failed to save image {file_path}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save image")

    def get_url(self, filename: str) -> str:
        """
        Gets the URL for a saved image.

        Args:
            filename (str): The name of the file for which the URL is needed.

        Returns:
            str: The URL or path to the file.

        Raises:
            HTTPException: If the file is not found.
        """
        url = self.file_resolver.find_file(filename=filename)
        return url

    def delete(self, directory: str, filename: str) -> bool:
        """
        Deletes a file from the local storage.

        Args:
            directory (str): The folder where the image is located.
            filename (str): The name of the image to delete.

        Returns:
            bool: True if the file was deleted successfully, False otherwise.
        """
        directory = self.directory_manager.get_directory(directory)
        file_path = directory / filename

        try:
            os.remove(file_path)
            logger.info(f"Deleted image: {file_path}")
            return True
        except FileNotFoundError:
            logger.warning(f"Tried to delete missing file: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False


def get_local_image_storage(
    directory_manager: DirectoryManagerDep,
    image_validator: SimpleImageValidatorDep,
    file_resolver: FilePathResolverDep
) -> LocalImageStorage:
    """
    Creates an instance of LocalImageStorage.

    Args:
        directory_manager (DirectoryManager): Handles directory-related operations.
        image_validator (SimpleImageValidator): Validates the image formats.
        file_resolver (FilePathResolver): Helps to find files in the storage.

    Returns:
        LocalImageStorage: An instance of LocalImageStorage.
    """
    return LocalImageStorage(
        directory_manager=directory_manager,
        image_validator=image_validator,
        file_resolver=file_resolver
    )
