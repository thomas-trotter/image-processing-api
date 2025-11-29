"""
Image management API routes.

This module defines all endpoints for image CRUD operations including
upload, retrieval, listing, deletion, and movement between folders.

For detailed documentation, see the module's README.md file.
"""

from fastapi import APIRouter, Request, UploadFile, HTTPException, status, Depends, Query
from typing import Optional, List, Annotated
import asyncio

from app.schemas.image.image_responses import (
    ImageDetailResponse,
    ImageDimensionsResponse,
    ImageListItem,
    ImageResponse,
    StatusResponse
)
from app.schemas.image.image_requests import MoveImageRequest
from app.managers.image_manager import ImageManager, get_image_manager
from app.core.rate_limiting import limiter
from app.core.logging_config import get_logger

logger = get_logger("image_routes")

router = APIRouter(
    prefix="/images",
    tags=["CRUD Images"],
    responses={404: {"description": "Not found"}},
)


ImageManagerDep = Annotated[ImageManager, Depends(get_image_manager)]


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=ImageResponse)
@limiter.limit("10/minute")
async def upload_image(
    request: Request,
    service: ImageManagerDep,
    file: UploadFile,
    filename: Optional[str] = None,
    format: str = "JPEG"
):
    """
    Uploads an image file.

    This endpoint allows users to upload an image file. Optionally, users can
    provide a custom filename and choose the desired format (default is JPEG).
    The endpoint validates the image, saves it to storage, and returns metadata.

    **Parameters:**
    - **file** (UploadFile): The image file being uploaded. Must be a valid image format.
    - **filename** (str, optional): The desired filename for the uploaded image.
        If not provided, a UUID-based filename is generated.
    - **format** (str, optional): The format to save the image as. Defaults to "JPEG".
        Supported formats: JPEG, PNG, GIF, BMP, TIFF, WEBP.

    **Returns:**
    - **ImageResponse**: Contains the status, file path, and complete metadata
        of the uploaded image including dimensions, format, and file size.

    **Raises:**
    - **HTTPException 400**: If the uploaded file is not a valid image.
    - **HTTPException 500**: If the upload or processing fails.
    """
    try:
        logger.info(f"Uploading image: {file.filename} as {filename or file.filename} with format {format}")
        file_path = await asyncio.to_thread(service.save_uploaded_image, file, filename, format)
        metadata = await asyncio.to_thread(service.get_image_metadata, file_path)
        logger.info(f"Image uploaded successfully: {file_path}")
        return ImageResponse(
            status="success",
            path=file_path,
            metadata=metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading image: {file.filename} - {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/", response_model=List[ImageListItem])
@limiter.limit("60/minute")
async def get_images(
    request: Request,
    service: ImageManagerDep,
    folder: str = Query("all", description="Filter images by folder (defaults to 'all')."),
    limit: int = Query(100, ge=1, le=1000, description="Limit the number of images to retrieve (between 1 and 1000)."),
    offset: int = Query(0, ge=0, description="Offset for pagination, skip the first N images.")
):
    """
    Gets a list of images with optional filtering, pagination, and limits.

    This endpoint retrieves a paginated list of images from the specified folder.
    Supports filtering by folder type and pagination using limit and offset parameters.

    **Parameters:**
    - **folder** (str, optional): The folder to fetch images from. Options: "uploaded",
        "edited", "detected", or "all". Defaults to "all".
    - **limit** (int, optional): The maximum number of images to return. Must be
        between 1 and 1000. Defaults to 100.
    - **offset** (int, optional): The number of images to skip for pagination.
        Must be >= 0. Defaults to 0.

    **Returns:**
    - **List[ImageListItem]**: A list of image metadata objects containing filename,
        format, dimensions, size, path, and folder information.

    **Raises:**
    - **HTTPException 400**: If the folder name is invalid.
    - **HTTPException 500**: If listing fails.
    """
    logger.info(f"Fetching image list from folder: {folder}, limit={limit}, offset={offset}")
    return await asyncio.to_thread(service.list_images, folder, limit, offset)


@router.get("/{image_name}/detail", response_model=ImageDetailResponse)
@limiter.limit("30/minute")
async def get_image(
    request: Request,
    service: ImageManagerDep,
    image_name: str,
    folder: str = Query("uploaded", description="The folder to fetch the image from (defaults to 'uploaded')."),
):
    """
    Gets detailed metadata of a specific image by its name.

    This endpoint retrieves comprehensive metadata for a specified image including
    dimensions, format, mode, file size, and path information.

    **Parameters:**
    - **image_name** (str): The name of the image file to retrieve (e.g., "photo.jpg").
    - **folder** (str, optional): The folder containing the image. Options: "uploaded",
        "edited", or "detected". Defaults to "uploaded".

    **Returns:**
    - **ImageDetailResponse**: Contains complete image metadata including filename,
        format, mode, width, height, size_bytes, and path.

    **Raises:**
    - **HTTPException 404**: If the image is not found in the specified folder.
    - **HTTPException 500**: If metadata extraction fails.
    """
    logger.info(f"Fetching details for image: {image_name} in folder: {folder}")
    return await asyncio.to_thread(service.get_image_by_id, image_name, folder)


@router.get("/{image_name}/metadata/dimensions", response_model=ImageDimensionsResponse)
@limiter.limit("20/minute")
async def get_dimensions(
    request: Request,
    service: ImageManagerDep,
    image_name: str,
    folder: str = Query("uploaded", description="The folder containing the image (defaults to 'uploaded')."),
):
    """
    Gets the dimensions (width and height) of a specific image.

    This endpoint retrieves only the width and height dimensions of an image,
    which is useful for display calculations or processing requirements.

    **Parameters:**
    - **image_name** (str): The name of the image file (e.g., "photo.jpg").
    - **folder** (str, optional): The folder where the image is stored. Options:
        "uploaded", "edited", or "detected". Defaults to "uploaded".

    **Returns:**
    - **ImageDimensionsResponse**: Contains the width and height of the image in pixels.

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If dimension extraction fails.
    """
    logger.info(f"Fetching dimensions for image: {image_name} in folder: {folder}")
    image_path = await asyncio.to_thread(service.get_image_path, image_name, folder)
    width, height = await asyncio.to_thread(service.get_image_dimensions, image_path)
    return ImageDimensionsResponse(width=width, height=height)

# Delete a specific image by its name
@router.delete("/{image_name}/delete", response_model=StatusResponse)
@limiter.limit("10/minute")
async def delete_image(
    request: Request,
    service: ImageManagerDep,
    image_name: str,
    folder: str = Query("uploaded", description="The folder from which to delete the image (defaults to 'uploaded')."),
):
    """
    Deletes a specific image identified by its name.

    This endpoint permanently deletes an image file and its associated metadata
    from the specified folder. This operation cannot be undone.

    **Parameters:**
    - **image_name** (str): The name of the image file to delete (e.g., "photo.jpg").
    - **folder** (str, optional): The folder from which to delete the image. Options:
        "uploaded", "edited", or "detected". Defaults to "uploaded".

    **Returns:**
    - **StatusResponse**: Contains status and message confirming deletion, along with
        metadata of the deleted image.

    **Raises:**
    - **HTTPException 404**: If the image is not found in the specified folder.
    - **HTTPException 500**: If deletion fails.
    """
    logger.info(f"Deleting image: {image_name} from folder: {folder}")
    return await asyncio.to_thread(service.delete_image, image_name, folder)


@router.post("/{image_name}/move", response_model=ImageDetailResponse)
@limiter.limit("20/minute")
async def move_image(
    request: Request,
    service: ImageManagerDep,
    image_name: str,
    move_params: MoveImageRequest,
):
    """
    Moves an image from one folder to another.

    This endpoint moves an image file and its metadata from a source folder to
    a target folder. Useful for organizing images after processing.

    **Parameters:**
    - **image_name** (str): The name of the image file to move (e.g., "photo.jpg").
    - **move_params** (MoveImageRequest): Request body containing:
        - **source_folder** (str): The folder to move from. Options: "uploaded",
            "edited", or "detected".
        - **target_folder** (str): The folder to move to. Options: "uploaded",
            "edited", or "detected".

    **Returns:**
    - **ImageDetailResponse**: Contains the metadata of the moved image with
        updated path information.

    **Raises:**
    - **HTTPException 400**: If source and target folders are the same, or if
        folder names are invalid.
    - **HTTPException 404**: If the image is not found in the source folder.
    - **HTTPException 409**: If an image with the same name already exists in
        the target folder.
    - **HTTPException 500**: If the move operation fails.
    """
    logger.info(f"Moving image: {image_name} from {move_params.source_folder} to {move_params.target_folder}")
    return await asyncio.to_thread(service.move_image, image_name, move_params.source_folder, move_params.target_folder)


@router.delete("/clear_all", response_model=StatusResponse)
@limiter.limit("2/hour")
async def clear_images(
    request: Request,
    service: ImageManagerDep,
    folder: str = Query("all", description="The folder from which to delete all images (defaults to 'all')."),
):
    """
    Deletes all images in a specified folder.

    This endpoint permanently deletes all image files and their metadata from
    the specified folder. This is a destructive operation that cannot be undone.
    Use with caution.

    **Parameters:**
    - **folder** (str, optional): The folder to clear. Options: "uploaded",
        "edited", "detected", or "all" (clears all folders). Defaults to "all".

    **Returns:**
    - **StatusResponse**: Contains status and message with the count of deleted images.

    **Raises:**
    - **HTTPException 400**: If the folder name is invalid.
    - **HTTPException 500**: If the deletion operation fails.

    **Warning:**
    This operation is irreversible. All images in the specified folder(s) will
    be permanently deleted.
    """
    logger.warning(f"Clearing all images in folder: {folder}")
    return await asyncio.to_thread(service.delete_all_images, folder)
