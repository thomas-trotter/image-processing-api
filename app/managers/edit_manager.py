"""
Image editing coordination layer.

This module provides the EditManager class that orchestrates image transformation
operations by coordinating with the ImageEditService.

For detailed documentation, see the module's README.md file.
"""

from fastapi import Depends, HTTPException
from typing import Annotated

from app.services.image.image_editor import ImageEditService, get_image_edit_service
from app.core.logging_config import get_logger


logger = get_logger("edit_manager")

ImageEditServiceDep = Annotated[ImageEditService, Depends(get_image_edit_service)]

class EditManager:
    """
    Manages image editing operations.

    Coordinates image transformation operations by delegating to the
    ImageEditService. Provides error handling and logging for edit operations.

    Args:
        edit_service (ImageEditService): Instance of ImageEditService providing
            image editing functionalities.
    """
    def __init__(self, edit_service: ImageEditServiceDep):
        """
        Initializes the EditManager with an image editing service.

        Args:
            edit_service (ImageEditService): Instance of ImageEditService providing
                image editing functionalities.
        """
        self.edit_service = edit_service

    def apply_resize(self, image_name: str, width: int, height: int) -> str:
        """
        Resizes an image to the given width and height.

        Args:
            image_name (str): Name of the image file.
            width (int): New width in pixels.
            height (int): New height in pixels.

        Returns:
            str: Path to the resized image.
        """
        logger.info(f"Resizing image '{image_name}' to {width}x{height}")
        return self.edit_service.resize_image(image_name, width, height)

    def apply_grayscale(self, image_name: str) -> str:
        """
        Converts an image to grayscale.

        Args:
            image_name (str): Name of the image file.

        Returns:
            str: Path to the grayscale image.
        """
        logger.info(f"Converting image '{image_name}' to grayscale")
        return self.edit_service.convert_to_grayscale(image_name)

    def apply_rotation(self, image_name: str, degrees: int, expand: bool = False) -> str:
        """
        Rotates an image by a given number of degrees.

        Args:
            image_name (str): Name of the image file.
            degrees (int): Angle to rotate in degrees (can be negative).
            expand (bool): Whether to expand the canvas to fit the rotation.
                Defaults to False.

        Returns:
            str: Path to the rotated image.
        """
        logger.info(f"Rotating image '{image_name}' by {degrees} degrees, expand={expand}")
        return self.edit_service.rotate_image(image_name, degrees, expand)

    def apply_blur(self, image_name: str, radius: float = 2.0) -> str:
        """
        Applies a Gaussian blur to the image.

        Args:
            image_name (str): Name of the image file.
            radius (float): Blur radius in pixels. Defaults to 2.0.

        Returns:
            str: Path to the blurred image.
        """
        logger.info(f"Applying blur to image '{image_name}' with radius={radius}")
        return self.edit_service.blur_image(image_name, radius)

    def apply_sharpen(self, image_name: str, factor: float = 2.0, radius: float = 2.0, threshold: int = 3) -> str:
        """
        Sharpenes the image using an unsharp mask.

        Args:
            image_name (str): Name of the image file.
            factor (float): Sharpening intensity factor. Defaults to 2.0.
            radius (float): Radius for sharpening in pixels. Defaults to 2.0.
            threshold (int): Threshold for sharpening. Defaults to 3.

        Returns:
            str: Path to the sharpened image.
        """
        logger.info(f"Sharpening image '{image_name}' with factor={factor}, radius={radius}, threshold={threshold}")
        return self.edit_service.sharpen_image(image_name, factor, radius, threshold)

    def apply_brightness(self, image_name: str, factor: float) -> str:
        """
        Adjusts the brightness of the image.

        Args:
            image_name (str): Name of the image file.
            factor (float): Brightness adjustment factor. 1.0 = no change,
                < 1.0 = darker, > 1.0 = brighter.

        Returns:
            str: Path to the adjusted image.
        """
        logger.info(f"Adjusting brightness of image '{image_name}' by factor={factor}")
        return self.edit_service.adjust_brightness(image_name, factor)

    def apply_contrast(self, image_name: str, factor: float) -> str:
        """
        Adjusts the contrast of the image.

        Args:
            image_name (str): Name of the image file.
            factor (float): Contrast adjustment factor. 1.0 = no change,
                < 1.0 = lower contrast, > 1.0 = higher contrast.

        Returns:
            str: Path to the adjusted image.
        """
        logger.info(f"Adjusting contrast of image '{image_name}' by factor={factor}")
        return self.edit_service.adjust_contrast(image_name, factor)

    def apply_bulk_edits(self, image_name: str, edits: dict) -> dict:
        """
        Applies a series of edits in bulk based on a dictionary of edit commands.

        Args:
            image_name (str): Name of the image file.
            edits (dict): Dictionary containing the edit operations and parameters.
                Supported keys: "resize", "grayscale", "rotate", "blur", "sharpen",
                "brightness", "contrast".

        Returns:
            dict: Dictionary with results of applied edits and their file paths.
                Keys correspond to edit types (e.g., "resized", "grayscale").
        """
        logger.info(f"Applying bulk edits to '{image_name}': {edits}")
        results = {}

        if "resize" in edits:
            width, height = edits["resize"]
            results["resized"] = self.apply_resize(image_name, width, height)

        if "grayscale" in edits:
            results["grayscale"] = self.apply_grayscale(image_name)

        if "rotate" in edits:
            degrees = edits["rotate"].get("degrees", 0)
            expand = edits["rotate"].get("expand", False)
            results["rotated"] = self.apply_rotation(image_name, degrees, expand)

        if "blur" in edits:
            results["blurred"] = self.apply_blur(image_name, edits["blur"])

        if "sharpen" in edits:
            results["sharpened"] = self.apply_sharpen(image_name, **edits["sharpen"])

        if "brightness" in edits:
            results["brightness_adjusted"] = self.apply_brightness(image_name, edits["brightness"])

        if "contrast" in edits:
            results["contrast_adjusted"] = self.apply_contrast(image_name, edits["contrast"])

        logger.info(f"Completed bulk edits for '{image_name}'")
        return results

    def process_image_edit(self, image_name: str, edit_method, *args, **kwargs):
        """
        Processes an image using a provided edit method.

        Generic method for processing image edits with error handling and logging.
        Wraps edit operations to provide consistent error handling.

        Args:
            image_name (str): Name of the image file.
            edit_method (callable): Callable method to apply an edit.
            *args: Positional arguments for the edit method.
            **kwargs: Keyword arguments for the edit method.

        Returns:
            str: Path to the processed image.

        Raises:
            HTTPException: If image processing fails.
        """
        logger.info(f"Processing '{image_name}' using method '{edit_method.__name__}'")
        try:
            result = edit_method(*args, **kwargs)
            logger.info(f"Successfully processed '{image_name}'. Result path: {result}")
            return result
        except Exception as e:
            logger.error(f"Error processing '{image_name}' with '{edit_method.__name__}': {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

def get_edit_manager(edit_service: ImageEditServiceDep) -> EditManager:
    """
    Injects an EditManager instance with a ImageEditService dependency.

    Args:
        edit_service (ImageEditService): Instance of ImageEditService to use.

    Returns:
        EditManager: Instance of EditManager with dependencies injected.
    """
    return EditManager(edit_service=edit_service)
