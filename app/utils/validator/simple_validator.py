"""
Simple image validation utilities.

This module provides the SimpleImageValidator class for validating image files
including type, size, and format checks.

For detailed documentation, see the module's README.md file.
"""

from typing import Dict
from fastapi import HTTPException, UploadFile, status, Depends
import logging

from app.utils.validator.base_validator import BaseImageValidator
from app.core.dependencies import get_format_extensions


logger = logging.getLogger("simple_validator")

class SimpleImageValidator(BaseImageValidator):
    """
    Simple image validator that checks image type, size, and format.

    Validates that the image file type is within the allowed types (JPEG, PNG by default).
    Ensures the image size does not exceed the maximum allowed size (default 5 MB).
    Checks if the image format is supported (based on the provided format extensions).

    Args:
        format_extensions (Dict[str, str]): A dictionary mapping image formats to
            their file extensions.
        max_size_mb (int): The maximum allowed file size in MB. Defaults to 5.
        allowed_types (tuple): A tuple of allowed MIME types. Defaults to
            ("image/jpeg", "image/png").
    """

    def __init__(self, format_extensions: Dict[str, str], max_size_mb=5, allowed_types=("image/jpeg", "image/png")):
        """
        Initializes the SimpleImageValidator with configuration.

        Args:
            format_extensions (Dict[str, str]): A dictionary mapping image formats
                to their file extensions.
            max_size_mb (int): The maximum allowed file size in MB. Defaults to 5.
            allowed_types (tuple): A tuple of allowed MIME types. Defaults to
                JPEG and PNG.
        """
        self.format_extensions = format_extensions
        self.max_size = max_size_mb * 1024 * 1024 
        self.allowed_types = allowed_types

        logger.info("Initialized SimpleImageValidator with max size %d bytes and allowed types: %s", self.max_size, self.allowed_types)

    def validate(self, image: UploadFile) -> None:
        """
        Validates the image by checking its type, size, and format.

        Performs all validation checks in sequence. Raises HTTPException if
        any validation fails.

        Args:
            image (UploadFile): The image file to validate (FastAPI's UploadFile).

        Raises:
            HTTPException: If any validation fails (type, size, or format).
        """
        try:
            logger.debug("Validating image with content type: %s", image.content_type)
            self.validate_type(image)
            self.validate_size(image)
        except HTTPException as e:
            logger.error("Validation failed: %s", e.detail)
            raise e

    def validate_type(self, image: UploadFile) -> None:
        """
        Validates the MIME type of the image.

        Args:
            image (UploadFile): The image file to validate.

        Raises:
            HTTPException: If the MIME type is not in the allowed types.
        """
        if image.content_type not in self.allowed_types:
            logger.warning("Unsupported file type: %s", image.content_type)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type."
            )
        logger.info("Validated image type: %s", image.content_type)

    def validate_size(self, image: UploadFile) -> None:
        """
        Validates the size of the image file.

        Args:
            image (UploadFile): The image file to validate.

        Raises:
            HTTPException: If the file size exceeds the maximum allowed size.
        """
        if image.file.__sizeof__() > self.max_size:
            logger.warning("File size too large: %d bytes, max allowed: %d bytes", image.file.__sizeof__(), self.max_size)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large. Max size is {} MB.".format(self.max_size // (1024 * 1024))
            )
        logger.info("Validated image size: %d bytes", image.file.__sizeof__())

    def validate_format(self, format: str) -> str:
        """
        Validates the format of the image.

        Args:
            format (str): The format of the image to validate (e.g., "JPEG").

        Returns:
            str: The validated format string (uppercase).

        Raises:
            HTTPException: If the format is not supported.
        """
        format = format.upper()
        if format not in self.format_extensions:
            supported_formats = ", ".join(self.format_extensions.keys())
            logger.warning("Unsupported format: %s. Supported formats: %s", format, supported_formats)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image format: {format}. Supported formats: {supported_formats}"
            )
        logger.info("Validated image format: %s", format)
        return format

    def get_extension(self, format: str) -> str:
        """
        Gets the file extension for the given format.

        Args:
            format (str): The image format to get the extension for (e.g., "JPEG").

        Returns:
            str: The file extension corresponding to the format (e.g., ".jpg").

        Raises:
            HTTPException: If the format is not supported.
        """
        format = self.validate_format(format)
        extension = self.format_extensions[format]
        logger.info("Retrieved file extension for format %s: %s", format, extension)
        return extension


def get_simple_image_validator(format_extensions: Dict[str, str] = Depends(get_format_extensions)) -> SimpleImageValidator:
    """
    Creates an instance of SimpleImageValidator.

    Args:
        format_extensions (Dict[str, str]): A dictionary of format extensions,
            provided by the dependency system.

    Returns:
        SimpleImageValidator: A SimpleImageValidator instance.
    """
    logger.debug("Creating SimpleImageValidator instance with provided format extensions")
    return SimpleImageValidator(format_extensions=format_extensions)
