# Core Module

## Overview

The `core` module provides foundational configuration, dependency injection, logging, and rate limiting functionality for the Image Processing API. This module sets up the application's core infrastructure and manages cross-cutting concerns.

## Architecture

The core module follows a configuration-based architecture where:

- **Settings** are loaded from environment variables using Pydantic
- **Dependencies** are provided through FastAPI's dependency injection system
- **Logging** is centralized with configurable levels and handlers
- **Rate limiting** is applied globally using slowapi

## Components

### `config.py` - Application Configuration
- **Settings Class**: Manages application-wide settings including:
  - Debug mode flag
  - Log level configuration
  - Directory paths for uploaded, edited, and detected images
- **Directory Setup**: Automatically creates required directories on initialization

### `dependencies.py` - Dependency Injection
- **get_directories()**: Provides directory path mappings for image storage
- **get_format_extensions()**: Maps image format names to file extensions

### `logging_config.py` - Logging Configuration
- **Centralized Logging**: Sets up rotating file handlers and optional console handlers
- **Configurable Levels**: Supports DEBUG, INFO, WARNING, ERROR, CRITICAL
- **get_logger()**: Factory function for creating module-specific loggers

### `rate_limiting.py` - Rate Limiting
- **Global Limiter**: Uses slowapi to enforce rate limits based on client IP address
- **Applied via Decorators**: Rate limits are applied to endpoints using `@limiter.limit()` decorator

## Usage

### Configuration

Settings are loaded from `.env` file or environment variables:

```python
from app.core.config import settings

# Access configuration
debug_mode = settings.DEBUG
log_level = settings.LOG_LEVEL
upload_path = settings.UPLOADED_FOLDER
```

### Dependencies

Dependencies are injected automatically in FastAPI routes:

```python
from app.core.dependencies import get_directories

@router.get("/example")
async def example(directories: dict = Depends(get_directories)):
    uploaded_dir = directories["uploaded"]
    # Use directories...
```

### Logging

Create module-specific loggers:

```python
from app.core.logging_config import get_logger

logger = get_logger("my_module")
logger.info("Log message")
```

### Rate Limiting

Apply rate limits to endpoints:

```python
from app.core.rate_limiting import limiter

@router.get("/endpoint")
@limiter.limit("10/minute")
async def limited_endpoint(request: Request):
    # Endpoint logic...
```

## Dependencies

### Internal Dependencies
- None (this is the foundation module)

### External Dependencies
- `pydantic` and `pydantic-settings`: Configuration management
- `slowapi`: Rate limiting
- Python `logging`: Logging infrastructure

## Related Documentation

- [Main README](../README.md)
- [API Routes](../api/README.md)
- [Services](../services/README.md)



