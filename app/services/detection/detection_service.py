"""
Object detection service using DETR model.

This module provides the ObjectDetectionService class for performing object
detection on images using the DETR (DEtection TRansformer) model.

For detailed documentation, see the module's README.md file.
"""

from transformers import DetrImageProcessor, DetrForObjectDetection
from typing import List, Dict, Tuple, Annotated, Union
from PIL import Image, ImageDraw, ImageFont
from tempfile import SpooledTemporaryFile 
from fastapi import Depends, UploadFile
from random import randint
from io import BytesIO 

import warnings
import torch 
import os 


from app.services.image.storage.local_storage import LocalImageStorage, get_local_image_storage
from app.core.logging_config import get_logger


LocalImageStorageDep = Annotated[LocalImageStorage, Depends(get_local_image_storage)]


logger = get_logger("detection_service")

class ObjectDetectionService:
    """
    Service for performing object detection on images using the DETR model.

    Uses the facebook/detr-resnet-50 model to detect objects in images and
    generate bounding boxes with labels and confidence scores.

    Args:
        local_storage (LocalImageStorage): A service for saving and retrieving
            images from local storage.
    """
    def __init__(self, local_storage: LocalImageStorageDep):
        warnings.filterwarnings("ignore", category=UserWarning, module='torch')  # Ignore PyTorch warnings
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
        self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", ignore_mismatched_sizes=True)
        self.confidence_threshold = 0.5 
        self.local_storage = local_storage
    
    def _get_font(self, size: int) -> ImageFont:
        """
        Returns a font for drawing text on the image.

        Attempts to load Arial font, falls back to default font if not available.

        Args:
            size (int): The size of the font in points.

        Returns:
            ImageFont: An ImageFont object for text rendering.
        """
        try:
            return ImageFont.truetype("arial.ttf", size)
        except IOError:
            logger.warning("Arial font not found, using default font.")
            return ImageFont.load_default()

    def _get_random_colour(self) -> Tuple[str, Tuple[int, int, int]]:
        """
        Generates a random color in both hex and RGB formats.

        Returns:
            Tuple[str, Tuple[int, int, int]]: A tuple containing:
                - hex color code (str): Hex string like "#ff0000"
                - RGB tuple (Tuple[int, int, int]): RGB values (r, g, b)
        """
        r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        return hex_color, (r, g, b)

    def _get_text_colour(self, rgb: Tuple[int, int, int]) -> str:
        """
        Determines an appropriate text color based on background brightness.

        Uses luminance calculation to choose black or white text for optimal
        readability against the background color.

        Args:
            rgb (Tuple[int, int, int]): The RGB color of the background.

        Returns:
            str: A hex string representing either "#000000" (black) or
                "#ffffff" (white), depending on the background brightness.
        """
        r, g, b = rgb
        brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255 
        return "#ffffff" if brightness < 0.5 else "#000000"  # Return black or white text based on brightness

    def _pillow_to_uploadfile(self, image: Image.Image, filename: str = "image.png") -> UploadFile:
        """
        Converts a Pillow image object to a FastAPI UploadFile.

        Args:
            image (Image.Image): The image to convert.
            filename (str): The desired filename for the uploaded image.
                Defaults to "image.png".

        Returns:
            UploadFile: An UploadFile object that can be used with FastAPI.
        """
        img_byte_arr = BytesIO()  # Create a byte stream for the image
        image.save(img_byte_arr, format=image.format or "PNG")  # Save image in memory
        img_byte_arr.seek(0)  # Reset byte stream pointer

        temp_file = SpooledTemporaryFile()  # Create a temporary file
        temp_file.write(img_byte_arr.read())  # Write the image bytes to the file
        temp_file.seek(0)  # Reset file pointer

        return UploadFile(filename=filename, file=temp_file)

    def get_bounding_boxes(self, image_path: str) -> str:
        """
        Detects objects in an image and draw bounding boxes around them.

        Performs object detection using the DETR model, draws bounding boxes
        with random colors, and adds labels with confidence scores.

        Args:
            image_path (str): The path to the image on which to perform object detection.

        Returns:
            str: The path to the new image with bounding boxes drawn on it.
                Saved to the "detected" folder.
        """
        image = Image.open(image_path)  
        image_copy = image.copy() 
        draw = ImageDraw.Draw(image_copy)  
        font = self._get_font(16)

        # Process the image with the DETR model
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        # Post-process the output and extract bounding boxes
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(
            outputs, target_sizes=target_sizes, threshold=self.confidence_threshold
        )[0]

        # Draw bounding boxes and labels
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(coord) for coord in box.tolist()]  # Round the box coordinates
            x, y, x2, y2 = box 

            class_name = self.model.config.id2label[label.item()]
            confidence = score.item()

            # Generate random color for the bounding box and label text
            colour, rgb = self._get_random_colour()
            draw.rectangle([x, y, x2, y2], outline=colour, width=3) 

            # Prepare text and draw it
            text = f"{class_name}: {confidence:.2f}"
            text_bbox = draw.textbbox((x, y - 20), text, font=font)
            draw.rectangle(text_bbox, fill=colour)  # Draw background for text
            draw.text((x, y - 20), text, fill=self._get_text_colour(rgb), font=font)  # Draw text

        # Save the output image with bounding boxes drawn
        original_filename = os.path.basename(image_path)
        name, ext = os.path.splitext(original_filename)
        new_filename = f"{name}_bounding_boxes{ext}"

        output_path = self.local_storage.save(
            file=self._pillow_to_uploadfile(image_copy, filename=new_filename),
            folder="detected",
            filename=new_filename,
            format=image.format
        )
        
        logger.info(f"Bounding boxes saved to: {output_path}")
        return output_path 

    def get_detected_objects(self, image_path: str) -> List[Dict[str, Union[str, float, List[int]]]]:
        """
        Detects objects in an image and return detection metadata.

        Performs object detection and returns only the detection results
        without creating a visualization.

        Args:
            image_path (str): The path to the image on which to perform object detection.

        Returns:
            List[Dict[str, Union[str, float, List[int]]]]: A list of dictionaries representing detected objects,
                each containing:
                - "label" (str): Object class name
                - "confidence" (float): Detection confidence score (0.0 to 1.0)
                - "box" (List[int]): Bounding box coordinates [x1, y1, x2, y2]
        """
        image = Image.open(image_path)

        # Process the image with the DETR model
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        # Post-process the output and extract bounding boxes
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(
            outputs, target_sizes=target_sizes, threshold=self.confidence_threshold
        )[0]

        detections = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            detections.append({
                "label": self.model.config.id2label[label.item()],
                "confidence": score.item(), 
                "box": box.tolist()
            })
        
        logger.info(f"Detected {len(detections)} objects.")
        return detections 

def get_object_detection_service(local_storage: LocalImageStorageDep) -> ObjectDetectionService:
    """
    Creates an instance of ObjectDetectionService.

    Args:
        local_storage (LocalImageStorage): A service for saving and retrieving
            images from local storage.

    Returns:
        ObjectDetectionService: An instance of the ObjectDetectionService class.
    """
    return ObjectDetectionService(local_storage=local_storage)
