"""
Image editing service for transformations and filters.

This module provides the ImageEditService class for performing various image
editing operations including resize, rotate, filters, and adjustments.

For detailed documentation, see the module's README.md file.
"""

from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from pathlib import Path
from typing import Annotated, Dict, Callable, Any, Optional
from fastapi import Depends

import os

from app.services.image.crud_operations import ImageCRUDService, get_image_crud_service
from app.core.dependencies import get_directories
from app.core.logging_config import get_logger


logger = get_logger("image_editor")

ImageCRUDServiceDep = Annotated[ImageCRUDService, Depends(get_image_crud_service)]
DirectoriesDep = Annotated[Dict[str, Path], Depends(get_directories)]


class ImageEditService:
    """
    Service for performing image editing operations.

    Provides methods for image transformations including resizing, rotating,
    applying filters, and adjusting properties like brightness and contrast.
    All edited images are saved to the edited folder.

    Args:
        image_crud (ImageCRUDService): Service for image CRUD operations.
        directories (Dict[str, Path]): Dictionary of directory paths for image storage.
    """
    
    def __init__(self, image_crud: ImageCRUDServiceDep, directories: DirectoriesDep):
        """
        Initializes the ImageEditService with dependencies.

        Args:
            image_crud (ImageCRUDService): Dependency injection for ImageCRUDService.
            directories (Dict[str, Path]): Directories for image storage locations.
        """
        self.image_crud = image_crud
        self.directories = directories

    def _get_output_path(self, image_path: str, suffix: Optional[str] = None) -> str:
        """
        Generates the output file path for a processed image.

        Creates a filename with an optional suffix to indicate the type of
        operation performed. The output is saved to the edited folder.

        Args:
            image_path (str): The path of the original image.
            suffix (str, optional): A suffix to be added to the output filename
                (e.g., "resized", "gray"). Defaults to None.

        Returns:
            str: The output file path for the processed image.
        """
        filename, ext = os.path.splitext(os.path.basename(image_path))
        output_filename = f"{filename}_{suffix}{ext}" if suffix else f"{filename}{ext}"

        output_dir = self.directories["edited"]
        output_path = output_dir / output_filename

        return str(output_path)

    def _process_image(
        self, 
        image_name: str, 
        operation: Callable[[Image.Image, ...], Image.Image], 
        suffix: Optional[str] = None, 
        **kwargs: Any
    ) -> str:
        """
        Applies an image processing operation and saves the result.

        Generic method that applies a given operation function to an image
        and saves the result to the edited folder.

        Args:
            image_name (str): The name of the image to be processed.
            operation (Callable[[Image.Image, ...], Image.Image]): The operation function 
                to be performed on the image. Should accept an Image object and **kwargs, 
                returning a processed Image.
            suffix (Optional[str]): A suffix to indicate the type of operation performed
                (e.g., "resized", "gray"). Defaults to None.
            **kwargs: Additional arguments required for the operation.

        Returns:
            str: The path where the processed image is saved.

        Raises:
            ValueError: If there is an error processing the image.
        """
        image_path = self.image_crud.get_image_path(image_name, "uploaded")
        try:
            with Image.open(image_path) as img:
                processed_img = operation(img, **kwargs)
                output_path = self._get_output_path(image_path, suffix)
                processed_img.save(output_path, quality=95)
                
                logger.info(f"Successfully processed image {image_name} with {suffix} operation.")
                return output_path
        except Exception as e:
            logger.error(f"Error processing image {image_name}: {e}")
            raise ValueError(f"Error processing image {image_path}: {e}")

    def resize_image(self, image_name: str, width: int, height: int) -> str:
        """
        Resizes an image to the specified width and height.

        Args:
            image_name (str): The name of the image to resize.
            width (int): The new width for the image in pixels.
            height (int): The new height for the image in pixels.

        Returns:
            str: The path where the resized image is saved.
        """
        logger.info(f"Resizing image {image_name} to {width}x{height}.")
        return self._process_image(
            image_name,
            lambda img, **kwargs: img.resize((kwargs["width"], kwargs["height"]), Image.LANCZOS),
            suffix="resized",
            width=width,
            height=height,
        )

    def convert_to_grayscale(self, image_name: str) -> str:
        """
        Converts an image to grayscale.

        Args:
            image_name (str): The name of the image to convert.

        Returns:
            str: The path where the grayscale image is saved.
        """
        logger.info(f"Converting image {image_name} to grayscale.")
        return self._process_image(
            image_name,
            lambda img, **_: ImageOps.grayscale(img),
            suffix="gray",
        )

    def rotate_image(self, image_name: str, degrees: int, expand: bool = False) -> str:
        """
        Rotates an image by a specified number of degrees.

        Args:
            image_name (str): The name of the image to rotate.
            degrees (int): The number of degrees to rotate the image (can be negative).
            expand (bool): Whether to expand the canvas to fit the rotated version.
                Defaults to False.

        Returns:
            str: The path where the rotated image is saved.
        """
        logger.info(f"Rotating image {image_name} by {degrees} degrees. Expand: {expand}.")
        return self._process_image(
            image_name,
            lambda img, **kwargs: img.rotate(kwargs["degrees"], expand=kwargs["expand"], resample=Image.BICUBIC),
            suffix=f"rotated_{degrees}",
            degrees=degrees,
            expand=expand,
        )

    def blur_image(self, image_name: str, radius: float = 2.0) -> str:
        """
        Apply a blur effect to an image.

        Args:
            image_name (str): The name of the image to blur.
            radius (float): The radius of the blur effect in pixels. Defaults to 2.0.

        Returns:
            str: The path where the blurred image is saved.
        """
        logger.info(f"Applying blur to image {image_name} with radius {radius}.")
        return self._process_image(
            image_name,
            lambda img, **kwargs: img.filter(ImageFilter.GaussianBlur(kwargs["radius"])),
            suffix=f"blurred_{radius}",
            radius=radius,
        )

    def sharpen_image(self, image_name: str, factor: float = 2.0, radius: float = 2.0, threshold: int = 3) -> str:
        """
        Apply a sharpening filter to an image.

        Args:
            image_name (str): The name of the image to sharpen.
            factor (float): The intensity of the sharpen effect. Defaults to 2.0.
            radius (float): The radius of the sharpening effect in pixels. Defaults to 2.0.
            threshold (int): The threshold for sharpening. Defaults to 3.

        Returns:
            str: The path where the sharpened image is saved.
        """
        logger.info(f"Sharpening image {image_name} with factor {factor}, radius {radius}, threshold {threshold}.")
        return self._process_image(
            image_name,
            lambda img, **kwargs: img.filter(
                ImageFilter.UnsharpMask(
                    radius=kwargs["radius"],
                    percent=int(kwargs["factor"] * 100),
                    threshold=kwargs["threshold"],
                )
            ),
            suffix="sharpened",
            factor=factor,
            radius=radius,
            threshold=threshold,
        )

    def adjust_brightness(self, image_name: str, factor: float) -> str:
        """
        Adjust the brightness of an image.

        Args:
            image_name (str): The name of the image to adjust.
            factor (float): The factor by which to adjust brightness.
                1.0 means no change, < 1.0 makes darker, > 1.0 makes brighter.

        Returns:
            str: The path where the brightness-adjusted image is saved.
        """
        logger.info(f"Adjusting brightness of image {image_name} by factor {factor}.")
        return self._process_image(
            image_name,
            lambda img, **kwargs: ImageOps.autocontrast(
                img.point(lambda p: p * kwargs["factor"])
            ),
            suffix=f"brightness_{factor}",
            factor=factor,
        )

    def adjust_contrast(self, image_name: str, factor: float) -> str:
        """
        Adjust the contrast of an image.

        Args:
            image_name (str): The name of the image to adjust.
            factor (float): The factor by which to adjust contrast.
                1.0 means no change, < 1.0 lowers contrast, > 1.0 increases contrast.

        Returns:
            str: The path where the contrast-adjusted image is saved.
        """
        logger.info(f"Adjusting contrast of image {image_name} by factor {factor}.")
        return self._process_image(
            image_name,
            lambda img, **kwargs: ImageEnhance.Contrast(img).enhance(kwargs["factor"]),
            suffix=f"contrast_{factor}",
            factor=factor,
        )


def get_image_edit_service(
    image_crud: ImageCRUDServiceDep,
    directories: DirectoriesDep
) -> ImageEditService:
    """
    Creates an instance of ImageEditService.

    Args:
        image_crud (ImageCRUDService): Image CRUD service instance.
        directories (Dict[str, Path]): Directories configuration.

    Returns:
        ImageEditService: An instance of the ImageEditService.
    """
    return ImageEditService(
        image_crud=image_crud,
        directories=directories
    )
