# Utils Module

## Overview

The `utils` module provides reusable utility functions and helper classes used throughout the application. Utilities are organized by functionality to maintain clear separation of concerns.

## Architecture

Utilities are organized into submodules:

- **`file_operations/`**: File and directory management
- **`validator/`**: Input validation utilities
- **`system/`**: System-level operations (cleanup, lifespan)

Each utility module is focused on a specific domain of operations.

## Components

### `file_operations/` - File Operations

#### `directory_utils.py` - Directory Management
**DirectoryManager Class**: Manages directory paths and operations.

**Capabilities:**
- Create directories if they don't exist
- Validate folder names
- Retrieve directory paths
- Handle directory errors

**Key Methods:**
- `validate_folder()`: Check if folder name is valid
- `get_directory()`: Get Path object for folder
- `_create_directories()`: Auto-create missing directories

#### `file_utils.py` - File Path Resolution
**FilePathResolver Class**: Resolves file paths across multiple directories.

**Capabilities:**
- Search for files across directories
- Validate file existence
- Find images by name
- Handle file not found errors

**Key Methods:**
- `find_file()`: Find file by name in any directory
- `find_and_validate_image()`: Find and validate image file
- `_get_existing_file_path()`: Internal search method

### `validator/` - Validation Utilities

#### `base_validator.py` - Base Validator Interface
Abstract base class defining validation interface:
- `validate()`: Main validation method
- `validate_type()`: Type validation
- `validate_size()`: Size validation
- `validate_format()`: Format validation

#### `simple_validator.py` - Image Validator
**SimpleImageValidator Class**: Validates image files.

**Capabilities:**
- Validate MIME types (JPEG, PNG by default)
- Check file size limits (5MB default)
- Validate image formats
- Get file extensions for formats

**Key Methods:**
- `validate()`: Full validation pipeline
- `validate_type()`: Check MIME type
- `validate_size()`: Check file size
- `validate_format()`: Validate format string
- `get_extension()`: Get extension for format

**Configuration:**
- Default max size: 5MB
- Default allowed types: `image/jpeg`, `image/png`
- Format extensions: Configurable via dependencies

### `system/` - System Operations

#### `lifespan.py` - Application Lifespan
Manages application startup and shutdown lifecycle.

**Capabilities:**
- Cleanup operations on shutdown
- Context management for FastAPI lifespan

**Function:**
- `lifespan()`: Async context manager for app lifecycle

#### `clean_up.py` - Cleanup Utilities
Handles cleanup of temporary files and caches.

**Capabilities:**
- Remove `__pycache__` directories
- Clean temporary files
- System maintenance operations

## Usage

### Directory Management

```python
from app.utils.file_operations.directory_utils import DirectoryManager

manager = DirectoryManager(directories)
# Validate folder
if manager.validate_folder("uploaded"):
    path = manager.get_directory("uploaded")
```

### File Resolution

```python
from app.utils.file_operations.file_utils import FilePathResolver

resolver = FilePathResolver(directories)
# Find file
file_path = resolver.find_file("image.jpg")
# Validate image
image_path = resolver.find_and_validate_image("image.jpg")
```

### Image Validation

```python
from app.utils.validator.simple_validator import SimpleImageValidator

validator = SimpleImageValidator(format_extensions)
# Validate upload
validator.validate(upload_file)
# Check format
format = validator.validate_format("JPEG")
extension = validator.get_extension("JPEG")
```

### System Operations

```python
from app.utils.system.lifespan import lifespan

# Used in FastAPI app
app = FastAPI(lifespan=lifespan)
```

## Design Patterns

### Dependency Injection
All utilities use dependency injection for configuration:
- Directories provided via dependencies
- Format extensions configurable
- Easy to test with mock dependencies

### Single Responsibility
Each utility class has a focused purpose:
- DirectoryManager: Only directory operations
- FilePathResolver: Only file finding
- SimpleImageValidator: Only validation

## Dependencies

### Internal Dependencies
- **Core**: Configuration and dependencies

### External Dependencies
- `fastapi`: UploadFile type, HTTPException
- `pathlib`: Path operations
- Standard library: `os`, `shutil`, `logging`

## Related Documentation

- [Core Module](../core/README.md)
- [Services](../services/README.md)
- [Main README](../../README.md)



