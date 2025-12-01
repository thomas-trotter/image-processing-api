# Image Services Module

## Overview

The `image` services module provides all business logic related to image processing, storage, metadata extraction, and CRUD operations. This module is the core of the image processing functionality.

## Architecture

Image services are organized by responsibility:

- **Storage**: File system operations (`storage/`)
- **Editing**: Image transformations (`image_editor.py`)
- **CRUD**: Database-like operations (`crud_operations.py`)
- **Metadata**: Information extraction (`metadata_handler.py`)

## Components

### `image_editor.py` - Image Editing Service

Performs image transformations using PIL (Pillow).

**Capabilities:**
- Resize images to specific dimensions
- Rotate images with optional expansion
- Convert to grayscale
- Apply filters (blur, sharpen)
- Adjust properties (brightness, contrast)

**Key Methods:**
- `resize_image()`: Resize to width x height
- `rotate_image()`: Rotate by degrees
- `convert_to_grayscale()`: Convert to grayscale
- `blur_image()`: Apply Gaussian blur
- `sharpen_image()`: Apply unsharp mask
- `adjust_brightness()`: Adjust brightness factor
- `adjust_contrast()`: Adjust contrast factor

**Output**: All edited images are saved to the `edited/` folder with descriptive suffixes.

### `crud_operations.py` - Image CRUD Service

Handles Create, Read, Update, Delete operations for images.

**Capabilities:**
- List images with pagination and filtering
- Get image metadata by ID
- Delete single or multiple images
- Move images between folders
- Validate image existence

**Key Methods:**
- `list_images()`: List with pagination (limit, offset)
- `get_image_by_id()`: Get full metadata
- `get_image_path()`: Get file path
- `delete_image()`: Delete single image
- `delete_all_images()`: Batch delete
- `move_image()`: Move between folders

**Folder Support**: Works with `uploaded/`, `edited/`, `detected/`, or `all` folders.

### `metadata_handler.py` - Metadata Extraction

Extracts metadata from image files.

**Capabilities:**
- Get image dimensions (width, height)
- Extract format, mode, file size
- Provide file path information

**Key Methods:**
- `get_dimensions()`: Returns (width, height) tuple
- `get_metadata()`: Returns complete metadata dictionary

**Metadata Includes:**
- Filename
- Format (JPEG, PNG, etc.)
- Mode (RGB, RGBA, etc.)
- Dimensions (width, height)
- File size in bytes
- File path

### `storage/` - Storage Services

#### `base_storage.py`
Abstract base class defining storage interface:
- `save()`: Save image file
- `get_url()`: Get file URL/path
- `delete()`: Delete file

#### `local_storage.py`
Local filesystem storage implementation:
- Saves images to configured directories
- Validates image formats
- Generates unique filenames
- Handles file operations

**Features:**
- Format validation
- Automatic filename generation (UUID if not provided)
- Image integrity checking
- Error handling for invalid images

## Usage

### Image Editing

```python
from app.services.image.image_editor import ImageEditService

service = ImageEditService(...)
# Resize image
path = service.resize_image("photo.jpg", 800, 600)
# Apply filter
path = service.blur_image("photo.jpg", radius=3.0)
```

### CRUD Operations

```python
from app.services.image.crud_operations import ImageCRUDService

service = ImageCRUDService(...)
# List images
images = service.list_images(folder="uploaded", limit=10, offset=0)
# Get metadata
metadata = service.get_image_by_id("photo.jpg", folder="uploaded")
# Delete image
result = service.delete_image("photo.jpg", folder="uploaded")
```

### Metadata Extraction

```python
from app.services.image.metadata_handler import ImageMetadataExtractor

extractor = ImageMetadataExtractor()
# Get dimensions
width, height = extractor.get_dimensions(image_path)
# Get full metadata
metadata = extractor.get_metadata(image_path)
```

### Storage

```python
from app.services.image.storage.local_storage import LocalImageStorage

storage = LocalImageStorage(...)
# Save image
path = storage.save(file, folder="uploaded", filename="photo.jpg")
# Get URL
url = storage.get_url("photo.jpg")
# Delete
success = storage.delete("uploaded", "photo.jpg")
```

## Supported Formats

- JPEG/JPG
- PNG
- GIF
- BMP
- TIFF
- WEBP

## Dependencies

### Internal Dependencies
- **Utils**: File operations, validators
- **Core**: Configuration, directories

### External Dependencies
- `PIL/Pillow`: Image processing library
- `fastapi`: UploadFile handling

## Related Documentation

- [Services README](../README.md)
- [Managers](../../managers/README.md)
- [Main README](../../../README.md)



