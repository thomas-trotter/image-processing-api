"""
Object detection coordination layer.

This module provides the DetectionManager class that orchestrates object
detection operations by coordinating with the ObjectDetectionService.

For detailed documentation, see the module's README.md file.
"""

from fastapi import Depends, HTTPException
from typing import List, Annotated

from app.services.detection.detection_service import ObjectDetectionService, get_object_detection_service
from app.core.logging_config import get_logger


logger = get_logger("detection_manager")


ObjectDetectionServiceDep = Annotated[ObjectDetectionService, Depends(get_object_detection_service)]

class DetectionManager:
    """
    Handles image processing tasks related to object detection.

    Delegates object detection operations to the ObjectDetectionService and
    provides error handling and logging for detection operations.

    Args:
        detection_service (ObjectDetectionService): Instance of ObjectDetectionService
            providing object detection functionalities.
    """
    def __init__(self, detection_service: ObjectDetectionServiceDep):
        """
        Initialize the DetectionManager with a detection service.

        Args:
            detection_service (ObjectDetectionService): Instance of ObjectDetectionService
                providing object detection functionalities.
        """
        self.detection_service = detection_service

    def process_image_for_detection(self, image_path: str) -> dict:
        """
        Process an image to generate bounding boxes and detect objects.

        Performs object detection and creates a visualization with bounding boxes
        drawn on the image. Also extracts detection metadata.

        Args:
            image_path (str): Path to the image file.

        Returns:
            dict: Dictionary containing:
                - "image_with_boxes" (str): Path to annotated image
                - "detections" (List[dict]): List of detected objects with labels,
                    confidence scores, and bounding box coordinates.

        Raises:
            HTTPException: If object detection fails.
        """
        try:
            logger.info(f"Starting object detection on image: {image_path}")
            output_image_path = self.detection_service.get_bounding_boxes(image_path)
            detected_objects = self.detection_service.get_detected_objects(image_path)
            logger.info(f"Detection completed for image: {image_path}")
            return {
                "image_with_boxes": output_image_path,
                "detections": detected_objects
            }
        except Exception as e:
            logger.error(f"Object detection failed for {image_path}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Object detection failed: {str(e)}")

    def get_detected_objects_summary(self, image_path: str) -> List[dict]:
        """
        Retrieves only the list of detected objects from an image.

        Performs object detection and returns metadata without creating a
        visualization. Faster than process_image_for_detection.

        Args:
            image_path (str): Path to the image file.

        Returns:
            List[dict]: List of detected objects, each containing:
                - "label" (str): Object class name
                - "confidence" (float): Detection confidence score (0.0 to 1.0)
                - "box" (List[float]): Bounding box coordinates [x1, y1, x2, y2]

        Raises:
            RuntimeError: If detection fails.
        """
        try:
            logger.info(f"Fetching detection summary for image: {image_path}")
            return self.detection_service.get_detected_objects(image_path)
        except Exception as e:
            logger.error(f"Detection summary failed for {image_path}: {str(e)}")
            raise RuntimeError(f"Detection summary failed: {str(e)}")

def get_detection_manager(detection_service: ObjectDetectionServiceDep) -> DetectionManager:
    """
    Injects a DetectionManager instance with a ObjectDetectionService dependency.

    Args:
        detection_service (ObjectDetectionService): Instance of ObjectDetectionService to use.

    Returns:
        DetectionManager: Instance of DetectionManager with dependencies injected.
    """
    return DetectionManager(detection_service=detection_service)
