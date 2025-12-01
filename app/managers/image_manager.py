"""
Image management coordination layer.

This module provides the ImageManager class that orchestrates image storage,
retrieval, and metadata operations by coordinating multiple service classes.

For detailed documentation, see the module's README.md file.
"""

from typing import Dict, List, Optional, Annotated, Tuple, Any
from fastapi import UploadFile, Depends
from pathlib import Path


from app.utils.file_operations.directory_utils import DirectoryManager, get_directory_manager
from app.services.image.storage.local_storage import LocalImageStorage, get_local_image_storage
from app.services.image.crud_operations import ImageCRUDService, get_image_crud_service
from app.services.image.metadata_handler import ImageMetadataExtractor, get_image_metadata_extractor
from app.core.logging_config import get_logger


logger = get_logger("image_manager")

DirectoryManagerDep = Annotated[DirectoryManager, Depends(get_directory_manager)]
LocalImageStorageDep = Annotated[LocalImageStorage, Depends(get_local_image_storage)]
ImageCRUDServiceDep = Annotated[ImageCRUDService, Depends(get_image_crud_service)]
ImageMetadataExtractorDep = Annotated[ImageMetadataExtractor, Depends(get_image_metadata_extractor)]

class ImageManager:
    """
    Manages image storage, retrieval, and metadata extraction.

    Coordinates various services including LocalImageStorage, ImageCRUDService,
    and ImageMetadataExtractor to provide a unified interface for image
    management operations.

    Args:
        directory_manager (DirectoryManager): Manages directory paths and folder operations.
        local_storage (LocalImageStorage): Handles file saving and storage.
        image_CRUD (ImageCRUDService): Handles CRUD operations for images.
        metadata_extractor (ImageMetadataExtractor): Extracts metadata from images.
    """
    
    
    def __init__(
        self,
        directory_manager: DirectoryManagerDep,
        local_storage: LocalImageStorageDep,
        image_CRUD: ImageCRUDServiceDep,
        metadata_extractor: ImageMetadataExtractorDep
    ):
        """
        Initializes the ImageManager with necessary services.

        Args:
            directory_manager (DirectoryManager): Manages directory paths and folder operations.
            local_storage (LocalImageStorage): Handles file saving and storage.
            image_CRUD (ImageCRUDService): Handles CRUD operations for images.
            metadata_extractor (ImageMetadataExtractor): Extracts metadata from images.
        """
        self.directory_manager = directory_manager
        self.local_storage = local_storage
        self.image_CRUD = image_CRUD
        self.metadata_extractor = metadata_extractor

    def save_uploaded_image(self, file: UploadFile, filename: Optional[str] = None, format: str = "JPEG") -> str:
        """
        Saves an uploaded image file to local storage.

        Args:
            file (UploadFile): The uploaded image file.
            filename (Optional[str]): Optional custom filename. If not provided,
                a UUID-based filename is generated.
            format (str): Image format to save as. Defaults to "JPEG".

        Returns:
            str: Path to the saved image file.
        """
        logger.info(f"Saving uploaded image: {filename or file.filename}")
        return self.local_storage.save(file=file, folder="uploaded", filename=filename, format=format)

    def get_image_path(self, image_name: str, folder: str = "uploaded") -> str:
        """
        Retrieves the full path of an image by its name.

        Args:
            image_name (str): Name of the image file.
            folder (str): Folder where the image is stored. Defaults to "uploaded".

        Returns:
            str: Path to the image file.
        """
        logger.debug(f"Getting image path for: {image_name} in folder: {folder}")
        image_path = self.image_CRUD.get_image_path(image_name, folder)
        return str(image_path)

    def get_image_dimensions(self, image_path: Path) -> Tuple[int, int]:
        """
        Retrieves the width and height of the image.

        Args:
            image_path (Path): Path to the image file.

        Returns:
            Tuple[int, int]: Tuple containing (width, height) in pixels.
        """
        logger.debug(f"Getting image dimensions for: {image_path}")
        return self.metadata_extractor.get_dimensions(image_path)

    def get_image_metadata(self, image_path: Path) -> Dict[str, Any]:
        """
        Retrieves metadata from an image file.

        Args:
            image_path (Path): Path to the image file.

        Returns:
            Dict[str, Any]: Dictionary containing image metadata including filename,
                format, mode, dimensions, size_bytes, and path.
        """
        logger.debug(f"Getting metadata for image: {image_path}")
        return self.metadata_extractor.get_metadata(image_path)

    def get_image_by_id(self, image_id: str, folder: str = "uploaded") -> Dict[str, Any]:
        """
        Retrieves image information by its ID.

        Args:
            image_id (str): Unique identifier for the image (filename).
            folder (str): Folder where the image is stored. Defaults to "uploaded".

        Returns:
            Dict[str, Any]: Dictionary containing complete image metadata.
        """
        logger.debug(f"Getting image by ID: {image_id}")
        return self.image_CRUD.get_image_by_id(image_id, folder)

    def list_images(self, folder: str = "uploaded", limit: int = 100, offset: int = 0, subdirectory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lists images in a folder with optional pagination and subdirectory filtering.

        Args:
            folder (str): Folder to search in. Options: "uploaded", "edited",
                "detected", or "all". Defaults to "uploaded".
            limit (int): Maximum number of images to return. Defaults to 100.
            offset (int): Number of images to skip for pagination. Defaults to 0.
            subdirectory (Optional[str]): Optional subfolder name to search within.

        Returns:
            List[Dict[str, Any]]: List of image metadata dictionaries.
        """
        logger.debug(f"Listing images in folder: {folder}, subdirectory: {subdirectory}")
        return self.image_CRUD.list_images(folder, limit, offset, subdirectory)

    def delete_image(self, image_id: str, folder: str = "uploaded") -> Dict[str, Any]:
        """
        Deletes a single image by ID.

        Args:
            image_id (str): Unique identifier for the image (filename).
            folder (str): Folder from which to delete the image. Defaults to "uploaded".

        Returns:
            Dict[str, Any]: Dictionary containing status, message, and deleted image metadata.
        """
        logger.info(f"Deleting image with ID: {image_id} from folder: {folder}")
        return self.image_CRUD.delete_image(image_id, folder)

    def delete_all_images(self, folder: str) -> Dict[str, str]:
        """
        Deletes all images in a specified folder.

        Args:
            folder (str): Folder to delete all images from. Options: "uploaded",
                "edited", "detected", or "all".

        Returns:
            Dict[str, str]: Dictionary containing status and message with deletion count.
        """
        logger.warning(f"Deleting all images in folder: {folder}")
        return self.image_CRUD.delete_all_images(folder)

    def move_image(self, image_id: str, source_folder: str, target_folder: str) -> Dict[str, Any]:
        """
        Moves an image from one folder to another.

        Args:
            image_id (str): Unique identifier for the image (filename).
            source_folder (str): Folder to move the image from.
            target_folder (str): Folder to move the image to.

        Returns:
            Dict[str, Any]: Dictionary containing the metadata of the moved image.
        """
        logger.info(f"Moving image {image_id} from {source_folder} to {target_folder}")
        return self.image_CRUD.move_image(image_id, source_folder, target_folder)


def get_image_manager(
    directory_manager: DirectoryManagerDep,
    local_storage: LocalImageStorageDep,
    image_CRUD: ImageCRUDServiceDep,
    metadata_extractor: ImageMetadataExtractorDep
) -> ImageManager:
    """
    Injects an ImageManager instance with a DirectoryManager, LocalImageStorage, ImageCRUDService, and ImageMetadataExtractor dependency.

    Args:
        directory_manager (DirectoryManager): DirectoryManager dependency.
        local_storage (LocalImageStorage): LocalImageStorage dependency.
        image_CRUD (ImageCRUDService): ImageCRUDService dependency.
        metadata_extractor (ImageMetadataExtractor): ImageMetadataExtractor dependency.

    Returns:
        ImageManager: Instance of ImageManager with all dependencies injected.
    """
    return ImageManager(
        directory_manager=directory_manager,
        local_storage=local_storage,
        image_CRUD=image_CRUD,
        metadata_extractor=metadata_extractor
    )
