"""
Image metadata extraction service.

This module provides the ImageMetadataExtractor class for extracting metadata
and dimensions from image files.

For detailed documentation, see the module's README.md file.
"""

from typing import Dict, Tuple, Any
from pathlib import Path
from fastapi import HTTPException, status
from PIL import Image

import os

from app.core.logging_config import get_logger


logger = get_logger("metadata_handler")

class ImageMetadataExtractor:
    """
    A class for extracting metadata and dimensions from image files.

    Provides static methods for extracting image information including
    dimensions, format, mode, and file size.
    """

    @staticmethod
    def get_dimensions(image_path: Path) -> Tuple[int, int]:
        """
        Gets the dimensions (width and height) of an image.

        Args:
            image_path (Path): The path to the image file.

        Returns:
            Tuple[int, int]: A tuple (width, height) representing the image's
                dimensions in pixels.

        Raises:
            HTTPException: If there is an error while getting image dimensions.
        """
        try:
            with Image.open(image_path) as img:
                return img.width, img.height
        except Exception as e:
            logger.error(f"Error getting image dimensions: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get image dimensions: {str(e)}"
            )
    
    @staticmethod
    def get_metadata(image_path: Path) -> Dict[str, Any]:
        """
        Gets the metadata of an image.

        Extracts comprehensive metadata including filename, format, mode,
        dimensions, file size, and path information.

        Args:
            image_path (Path): The path to the image file.

        Returns:
            Dict[str, Any]: A dictionary containing the image metadata with keys:
                - filename: Image filename
                - format: Image format (JPEG, PNG, etc.)
                - mode: Image mode (RGB, RGBA, etc.)
                - width: Image width in pixels
                - height: Image height in pixels
                - size_bytes: File size in bytes
                - path: Full file path
                - url: URL (currently None)

        Raises:
            HTTPException: If the image is not found or metadata extraction fails.
        """
        try:
            with Image.open(image_path) as img:
                return {
                    "filename": Path(image_path).name,  
                    "format": img.format,               
                    "mode": img.mode,                   
                    "width": img.width,               
                    "height": img.height,             
                    "size_bytes": os.path.getsize(image_path), 
                    "path": str(image_path),           
                    "url": None                     
                }
        except FileNotFoundError:
            logger.error(f"Image not found: {image_path}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
        except Exception as e:
            logger.error(f"Error getting image info: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get image info: {str(e)}"
            )
    
def get_image_metadata_extractor() -> ImageMetadataExtractor:
    """
    Creates an instance of ImageMetadataExtractor.

    Returns:
        ImageMetadataExtractor: An instance of the ImageMetadataExtractor class.
    """
    return ImageMetadataExtractor()