# Schemas Module

## Overview

The `schemas` module contains Pydantic models for request validation and response serialization. Schemas ensure type safety, automatic validation, and consistent API contracts across all endpoints.

## Architecture

Schemas are organized by domain, mirroring the route structure:

- **`image/`**: Image management schemas
- **`editing/`**: Image editing schemas
- **`detection/`**: Object detection schemas

Each domain contains:
- **Request schemas**: Input validation models
- **Response schemas**: Output serialization models

## Components

### `image/` - Image Schemas

#### Request Schemas (`image_requests.py`)
- **MoveImageRequest**: Request body for moving images between folders
  - `source_folder`: Source folder name
  - `target_folder`: Target folder name

#### Response Schemas (`image_responses.py`)
- **ImageResponse**: Standard image operation response
  - `status`: Operation status
  - `path`: File path
  - `metadata`: Image metadata dictionary

- **ImageListItem**: Image list item with metadata
  - `filename`, `format`, `mode`
  - `width`, `height`, `size_bytes`
  - `path`, `folder`

- **ImageDetailResponse**: Detailed image information
  - Full metadata including all image properties

- **ImageDimensionsResponse**: Image dimensions only
  - `width`: Image width in pixels
  - `height`: Image height in pixels

- **StatusResponse**: Generic status response
  - `status`: Success/failure status
  - `message`: Status message

### `editing/` - Editing Schemas

#### Request Schemas (`editing_requests.py`)
- **RotateEditRequest**: Rotation parameters
  - `degrees`: Rotation angle
  - `expand`: Whether to expand canvas

- **SharpenEditRequest**: Sharpening parameters
  - `factor`: Sharpening intensity
  - `radius`: Sharpening radius
  - `threshold`: Sharpening threshold

#### Response Schemas (`editing_responses.py`)
- **EditResponse**: Standard editing operation response
  - `path`: Path to edited image

### `detection/` - Detection Schemas

#### Response Schemas (`detection_responses.py`)
- **DetectionBox**: Individual detection result
  - `label`: Object class name
  - `confidence`: Confidence score (0-1)
  - `box`: Bounding box coordinates [x1, y1, x2, y2]

- **BoundingBoxResponse**: Bounding box detection response
  - `message`: Success message
  - `image_path`: Path to annotated image
  - `detections`: List of DetectionBox objects

- **DetectedObjectsResponse**: Detection summary response
  - `message`: Success message
  - `detected_objects`: List of detection dictionaries

## Usage

### Request Validation

Schemas automatically validate request data:

```python
from app.schemas.editing.editing_requests import RotateEditRequest

@router.post("/rotate")
async def rotate_image(
    params: RotateEditRequest  # Automatically validated
):
    # params.degrees and params.expand are validated
    pass
```

### Response Serialization

Schemas ensure consistent response formats:

```python
from app.schemas.image.image_responses import ImageResponse

@router.post("/upload", response_model=ImageResponse)
async def upload_image(...):
    return ImageResponse(
        status="success",
        path=file_path,
        metadata=metadata
    )
```

### Type Safety

Pydantic provides:
- Type checking at runtime
- Automatic type conversion
- Validation error messages
- IDE autocomplete support

## Validation Rules

### Image Requests
- Folder names must be valid (`uploaded`, `edited`, `detected`)
- Filenames must be valid strings

### Editing Requests
- Rotation degrees: Any integer
- Expand: Boolean
- Sharpening parameters: Positive floats/integers

### Detection Responses
- Confidence scores: 0.0 to 1.0
- Bounding boxes: List of 4 coordinates

## Benefits

1. **Type Safety**: Catch errors at request time
2. **Documentation**: Auto-generated API docs from schemas
3. **Consistency**: Uniform response formats
4. **Validation**: Automatic input validation
5. **Serialization**: Automatic JSON conversion

## Dependencies

### Internal Dependencies
- None (schemas are self-contained)

### External Dependencies
- `pydantic`: Schema definition and validation

## Related Documentation

- [API Routes](../api/README.md)
- [Main README](../../README.md)
- [Pydantic Documentation](https://docs.pydantic.dev/)



