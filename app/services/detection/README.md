# Detection Services Module

## Overview

The `detection` services module provides object detection capabilities using the DETR (DEtection TRansformer) model. This module handles ML model initialization, image processing, and detection result generation.

## Architecture

The detection service uses a pre-trained transformer model:

```
Image Input
    ↓
Image Processor (preprocessing)
    ↓
DETR Model (inference)
    ↓
Post-processing
    ↓
Detection Results (bounding boxes, labels, confidence)
```

## Components

### `detection_service.py` - Object Detection Service

Main service for object detection operations.

**Model**: `facebook/detr-resnet-50` from Hugging Face

**Capabilities:**
- Detect objects in images
- Generate bounding boxes with labels
- Extract detection metadata (labels, confidence scores, coordinates)
- Visualize detections on images

**Key Methods:**

#### `get_bounding_boxes(image_path: str) -> str`
Detects objects and draws bounding boxes on the image.

**Process:**
1. Load and preprocess image
2. Run DETR model inference
3. Post-process results with confidence threshold (0.5)
4. Draw bounding boxes with random colors
5. Add labels with confidence scores
6. Save annotated image to `detected/` folder

**Returns**: Path to image with bounding boxes drawn

#### `get_detected_objects(image_path: str) -> list`
Detects objects and returns metadata without visualization.

**Returns**: List of dictionaries containing:
- `label`: Object class name
- `confidence`: Detection confidence score (0-1)
- `box`: Bounding box coordinates [x1, y1, x2, y2]

**Process:**
1. Load and preprocess image
2. Run DETR model inference
3. Post-process results
4. Extract detection metadata

## Model Details

### DETR (DEtection TRansformer)

**Architecture:**
- Backbone: ResNet-50
- Transformer encoder-decoder
- End-to-end object detection

**Features:**
- No region proposal network needed
- Direct set prediction
- Handles variable number of objects
- Global context understanding

**Configuration:**
- Confidence threshold: 0.5 (configurable)
- Model: `facebook/detr-resnet-50`
- Framework: PyTorch via Hugging Face Transformers

## Usage

### Basic Detection

```python
from app.services.detection.detection_service import ObjectDetectionService

service = ObjectDetectionService(...)

# Get bounding boxes (visualized)
image_path = service.get_bounding_boxes("photo.jpg")

# Get detection metadata
detections = service.get_detected_objects("photo.jpg")
for detection in detections:
    print(f"{detection['label']}: {detection['confidence']:.2f}")
```

### Detection Results Format

```python
[
    {
        "label": "person",
        "confidence": 0.95,
        "box": [100, 150, 300, 400]  # [x1, y1, x2, y2]
    },
    {
        "label": "car",
        "confidence": 0.87,
        "box": [200, 100, 500, 300]
    }
]
```

## Performance Considerations

- **Model Loading**: Model is loaded once at service initialization
- **Inference Time**: Varies by image size (typically 1-5 seconds)
- **Memory**: Model requires GPU or sufficient RAM
- **Rate Limiting**: Detection endpoints have lower rate limits (5-10/min)

## Error Handling

The service handles:
- Invalid image formats
- Model loading failures
- Inference errors
- File I/O errors

All errors are logged and converted to appropriate HTTP exceptions.

## Dependencies

### Internal Dependencies
- **Storage**: `app/services/image/storage/` - Save detection outputs
- **Core**: Logging configuration

### External Dependencies
- `transformers`: Hugging Face transformers library
- `torch`: PyTorch deep learning framework
- `PIL/Pillow`: Image processing
- `numpy`: Numerical operations

## Related Documentation

- [Services README](../README.md)
- [Managers](../../managers/README.md)
- [Main README](../../../README.md)
- [DETR Model Documentation](https://huggingface.co/facebook/detr-resnet-50)



