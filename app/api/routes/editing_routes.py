"""
Image editing API routes.

This module defines all endpoints for image transformation and editing
operations including resize, rotate, filters, and adjustments.

For detailed documentation, see the module's README.md file.
"""

from fastapi import APIRouter, Depends, Query, Request
from typing import Annotated

from app.managers.edit_manager import EditManager, get_edit_manager
from app.schemas.editing.editing_requests import RotateEditRequest, SharpenEditRequest
from app.schemas.editing.editing_responses import EditResponse
from app.core.rate_limiting import limiter
from app.core.logging_config import get_logger

logger = get_logger("editing_routes")

router = APIRouter(prefix="/images/edit", tags=["Image Editing"])

EditManagerDep = Annotated[EditManager, Depends(get_edit_manager)]


@router.post("/resize", response_model=EditResponse)
@limiter.limit("10/minute")
def resize_image(
    request: Request,
    image_name: str,
    service: EditManagerDep,
    width: int = Query(..., gt=0, description="The target width for resizing (must be greater than 0)."),
    height: int = Query(..., gt=0, description="The target height for resizing (must be greater than 0)."),
):
    """
    Resize the image to the specified width and height.

    This endpoint resizes an image to the exact dimensions specified. The
    resized image is saved to the edited folder with a "_resized" suffix.

    **Parameters:**
    - **image_name** (str): The name of the image file to resize (e.g., "photo.jpg").
        The image must exist in the "uploaded" folder.
    - **width** (int): The target width in pixels. Must be greater than 0.
    - **height** (int): The target height in pixels. Must be greater than 0.

    **Returns:**
    - **EditResponse**: Contains the path to the resized image file.

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If resizing fails.
    """
    path = service.process_image_edit(image_name, service.apply_resize, image_name, width, height)
    return EditResponse(path=path)


@router.post("/grayscale", response_model=EditResponse)
@limiter.limit("20/minute")
def convert_to_grayscale(
    request: Request,
    image_name: str,
    service: EditManagerDep,
):
    """
    Converts the image to grayscale.

    This endpoint converts a color image to grayscale. The converted image
    is saved to the edited folder with a "_gray" suffix.

    **Parameters:**
    - **image_name** (str): The name of the image file to convert (e.g., "photo.jpg").
        The image must exist in the "uploaded" folder.

    **Returns:**
    - **EditResponse**: Contains the path to the grayscale image file.

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If conversion fails.
    """
    path = service.process_image_edit(image_name, service.apply_grayscale, image_name)
    return EditResponse(path=path)


@router.post("/rotate", response_model=EditResponse)
@limiter.limit("15/minute")
def rotate_image(
    request: Request,
    image_name: str,
    rotate_params: RotateEditRequest,
    service: EditManagerDep,
):
    """
    Rotates the image by the specified degrees and expansion settings.

    This endpoint rotates an image by the specified angle. The rotated image
    is saved to the edited folder with a "_rotated_{degrees}" suffix.

    **Parameters:**
    - **image_name** (str): The name of the image file to rotate (e.g., "photo.jpg").
        The image must exist in the "uploaded" folder.
    - **rotate_params** (RotateEditRequest): Request body containing:
        - **degrees** (int): The rotation angle in degrees (can be negative).
        - **expand** (bool, optional): Whether to expand the canvas to fit the
            rotated image. If False, the image may be cropped. Defaults to False.

    **Returns:**
    - **EditResponse**: Contains the path to the rotated image file.

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If rotation fails.
    """
    path = service.process_image_edit(image_name, service.apply_rotation, image_name, rotate_params.degrees, rotate_params.expand)
    return EditResponse(path=path)


@router.post("/blur", response_model=EditResponse)
@limiter.limit("10/minute")
def blur_image(
    request: Request,
    image_name: str,
    service: EditManagerDep,
    radius: float = Query(2.0, gt=0, description="The radius of the blur effect (must be greater than 0)."),
):
    """
    Apply a blur effect to the image with a specified radius.

    This endpoint applies a Gaussian blur filter to the image. The blurred image
    is saved to the edited folder with a "_blurred_{radius}" suffix.

    **Parameters:**
    - **image_name** (str): The name of the image file to blur (e.g., "photo.jpg").
        The image must exist in the "uploaded" folder.
    - **radius** (float, optional): The radius of the blur effect in pixels.
        Must be greater than 0. Larger values create more blur. Defaults to 2.0.

    **Returns:**
    - **EditResponse**: Contains the path to the blurred image file.

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If blurring fails.
    """
    path = service.process_image_edit(image_name, service.apply_blur, image_name, radius)
    return EditResponse(path=path)

@router.post("/sharpen", response_model=EditResponse)
@limiter.limit("10/minute")
def sharpen_image(
    request: Request,
    image_name: str,
    sharpen_params: SharpenEditRequest,
    service: EditManagerDep,
):
    """
    Sharpen the image with the specified parameters.

    This endpoint applies an unsharp mask filter to enhance image sharpness.
    The sharpened image is saved to the edited folder with a "_sharpened" suffix.

    **Parameters:**
    - **image_name** (str): The name of the image file to sharpen (e.g., "photo.jpg").
        The image must exist in the "uploaded" folder.
    - **sharpen_params** (SharpenEditRequest): Request body containing:
        - **factor** (float, optional): The intensity of the sharpening effect.
            Higher values create more sharpening. Defaults to 2.0.
        - **radius** (float, optional): The radius of the sharpening effect in pixels.
            Defaults to 2.0.
        - **threshold** (int, optional): The threshold for sharpening. Only pixels
            with differences above this threshold are sharpened. Defaults to 3.

    **Returns:**
    - **EditResponse**: Contains the path to the sharpened image file.

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If sharpening fails.
    """
    path = service.process_image_edit(image_name, service.apply_sharpen, image_name, sharpen_params.factor, sharpen_params.radius, sharpen_params.threshold)
    return EditResponse(path=path)


@router.post("/brightness", response_model=EditResponse)
@limiter.limit("20/minute")
def adjust_brightness(
    request: Request,
    image_name: str,
    service: EditManagerDep,
    factor: float = Query(..., gt=0, description="The factor by which to adjust brightness (must be greater than 0)."),
):
    """
    Adjusts the brightness of the image by a specified factor.

    This endpoint adjusts the brightness of an image. The adjusted image is
    saved to the edited folder with a "_brightness_{factor}" suffix.

    **Parameters:**
    - **image_name** (str): The name of the image file to adjust (e.g., "photo.jpg").
        The image must exist in the "uploaded" folder.
    - **factor** (float): The brightness adjustment factor. Must be greater than 0.
        - 1.0 = no change
        - < 1.0 = darker
        - > 1.0 = brighter

    **Returns:**
    - **EditResponse**: Contains the path to the brightness-adjusted image file.

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If brightness adjustment fails.
    """
    path = service.process_image_edit(image_name, service.apply_brightness, image_name, factor)
    return EditResponse(path=path)

@router.post("/contrast", response_model=EditResponse)
@limiter.limit("20/minute")
def adjust_contrast(
    request: Request,
    image_name: str,
    service: EditManagerDep,
    factor: float = Query(..., gt=0, description="The factor by which to adjust contrast (must be greater than 0)."),
):
    """
    Adjusts the contrast of the image by a specified factor.

    This endpoint adjusts the contrast of an image. The adjusted image is
    saved to the edited folder with a "_contrast_{factor}" suffix.

    **Parameters:**
    - **image_name** (str): The name of the image file to adjust (e.g., "photo.jpg").
        The image must exist in the "uploaded" folder.
    - **factor** (float): The contrast adjustment factor. Must be greater than 0.
        - 1.0 = no change
        - < 1.0 = lower contrast
        - > 1.0 = higher contrast

    **Returns:**
    - **EditResponse**: Contains the path to the contrast-adjusted image file.

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If contrast adjustment fails.
    """
    path = service.process_image_edit(image_name, service.apply_contrast, image_name, factor)
    return EditResponse(path=path)

