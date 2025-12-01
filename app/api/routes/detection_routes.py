"""
Object detection API routes.

This module defines endpoints for object detection operations using the
DETR (DEtection TRansformer) model. Supports both visualization and
metadata extraction.

For detailed documentation, see the module's README.md file.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated
import asyncio

from app.utils.file_operations.file_utils import FilePathResolver, get_file_path_resolver
from app.managers.detection_manager import DetectionManager, get_detection_manager
from app.schemas.detection.detection_responses import BoundingBoxResponse, DetectedObjectsResponse, DetectionBox
from app.core.rate_limiting import limiter
from app.core.logging_config import get_logger

import time

logger = get_logger("detection_routes")

router = APIRouter(prefix="/images/detect", tags=["Image Detections"])

DetectionManagerDep = Annotated[DetectionManager, Depends(get_detection_manager)]
FilePathResolverDep = Annotated[FilePathResolver, Depends(get_file_path_resolver)]

@router.post("/bounding_boxes/", response_model=BoundingBoxResponse)
@limiter.limit("5/minute")
async def bounding_boxes(
    request: Request,
    image_name: str,
    manager: DetectionManagerDep,
    file_resolver: FilePathResolverDep,
):
    """
    Detect objects and draw bounding boxes on the specified image.

    This endpoint performs object detection using the DETR model, draws bounding
    boxes around detected objects, and saves the annotated image. The detection
    uses a confidence threshold of 0.5.

    **Parameters:**
    - **image_name** (str): The name of the image file to process (e.g., "photo.jpg").
        The image must exist in any of the storage folders (uploaded, edited, detected).

    **Returns:**
    - **BoundingBoxResponse**: Contains:
        - **message** (str): Success message.
        - **image_path** (str): Path to the annotated image with bounding boxes drawn.
        - **detections** (List[DetectionBox]): List of detected objects with labels,
            confidence scores, and bounding box coordinates.

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If object detection or image processing fails.

    **Note:**
    This operation may take several seconds depending on image size and system resources.
    The annotated image is saved to the "detected" folder.
    """
    start_time = time.time()
    logger.info(f"Request to detect bounding boxes for image: {image_name}")

    image_path = await asyncio.to_thread(file_resolver.find_and_validate_image, image_name)

    try:
        logger.info(f"Processing image for bounding boxes: {image_name}")
        data = await asyncio.to_thread(manager.process_image_for_detection, image_path)
    except RuntimeError as e:
        logger.error(f"Error processing image: {image_name}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    execution_time = time.time() - start_time
    logger.info(f"Successfully detected bounding boxes for image: {image_name}, Execution Time: {execution_time:.2f}s")
    
    return BoundingBoxResponse(
        message="Bounding boxes drawn successfully",
        image_path=data["image_with_boxes"],
        detections=[DetectionBox(**d) for d in data["detections"]]
    )


@router.get("/detected_objects/", response_model=DetectedObjectsResponse)
@limiter.limit("10/minute")
async def detected_objects(
    request: Request,
    image_name: str,
    manager: DetectionManagerDep,
    file_resolver: FilePathResolverDep,
):
    """
    Retrieves the list of detected objects from the specified image.

    This endpoint performs object detection and returns only the detection
    metadata without creating a visualization. Faster than the bounding boxes
    endpoint as it skips image annotation.

    **Parameters:**
    - **image_name** (str): The name of the image file to process (e.g., "photo.jpg").
        The image must exist in any of the storage folders (uploaded, edited, detected).

    **Returns:**
    - **DetectedObjectsResponse**: Contains:
        - **message** (str): Success message.
        - **detected_objects** (List[dict]): List of detected objects, each containing:
            - **label** (str): Object class name (e.g., "person", "car").
            - **confidence** (float): Detection confidence score (0.0 to 1.0).
            - **box** (List[float]): Bounding box coordinates [x1, y1, x2, y2].

    **Raises:**
    - **HTTPException 404**: If the image is not found.
    - **HTTPException 500**: If object detection fails.

    **Note:**
    This operation may take several seconds depending on image size and system resources.
    """
    start_time = time.time()
    logger.info(f"Request to retrieve detected objects for image: {image_name}")

    image_path = await asyncio.to_thread(file_resolver.find_and_validate_image, image_name)

    try:
        logger.info(f"Retrieving detected objects for image: {image_name}")
        detected = await asyncio.to_thread(manager.get_detected_objects_summary, image_path)
    except RuntimeError as e:
        logger.error(f"Error retrieving detected objects for image: {image_name}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving detected objects: {str(e)}")

    execution_time = time.time() - start_time
    logger.info(f"Successfully retrieved detected objects for image: {image_name}, Execution Time: {execution_time:.2f}s")

    return DetectedObjectsResponse(
        message="Detected objects retrieved successfully",
        detected_objects=detected
    )
