# Architecture Overview

[← Back to Main README](../README.md)

System architecture, design patterns, and technical details of the Image Processing API.

## Architecture Pattern

The Image Processing API follows a layered architecture pattern:

```
┌─────────────────────────────────────┐
│         API Routes Layer            │  (FastAPI endpoints)
├─────────────────────────────────────┤
│         Managers Layer              │  (Business logic coordination)
├─────────────────────────────────────┤
│         Services Layer              │  (Core business logic)
├─────────────────────────────────────┤
│         Utils & Core                │  (Infrastructure)
└─────────────────────────────────────┘
```

### Layer Responsibilities

- **API Routes Layer**: Handles HTTP requests, validation, and responses
- **Managers Layer**: Coordinates business logic across multiple services
- **Services Layer**: Implements core business logic (image processing, detection, storage)
- **Utils & Core Layer**: Provides infrastructure (configuration, logging, utilities)

## Module Organization

The codebase is organized into focused modules:

- **[Core Module](../app/core/README.md)**: Configuration, dependencies, logging, rate limiting
- **[API Module](../app/api/README.md)**: Route handlers and endpoint definitions
- **[Managers Module](../app/managers/README.md)**: Business logic coordination layer
- **[Services Module](../app/services/README.md)**: Core business logic implementation
- **[Schemas Module](../app/schemas/README.md)**: Request/response validation models
- **[Utils Module](../app/utils/README.md)**: Utility functions and helpers

For detailed information about each module, see their respective README files.

## AI Model: DETR (DEtection TRansformer)

This project uses the **DEtection TRansformer (DETR)** model for object detection. DETR combines a Transformer architecture with a ResNet-50 backbone, enabling efficient and accurate object detection in images.

### Key Components

- **Model**: `facebook/detr-resnet-50`
  - A pre-trained object detection model that uses Transformers to understand the global context.
  - Fine-tuned for detecting a wide variety of objects.

### Initialization

The processor and model are loaded as follows:

```python
from transformers import DetrImageProcessor, DetrForObjectDetection

# Initialise the image processor and model
self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", ignore_mismatched_sizes=True)
```

- **`DetrImageProcessor`**: Pre-processes images for model input (resizing, normalisation, etc.).
- **`DetrForObjectDetection`**: Performs object detection and outputs bounding boxes and class predictions.

### Benefits

- **End-to-End Pipeline**: Simplifies detection without the need for separate components like region proposal networks.
- **High Flexibility**: Can detect a wide variety of objects and is easily adaptable to custom datasets.
- **Transformer-Based**: Captures global image context, improving detection accuracy.

### Example Usage

```python
# Process image and run object detection
inputs = self.processor(images=image, return_tensors="pt")
outputs = self.model(**inputs)

# Post-process to extract detections
results = self.processor.post_process_object_detection(outputs, target_sizes=[image.size[::-1]], threshold=0.9)[0]
```

### Model Information

- **Model Name**: `facebook/detr-resnet-50`
- **Source**: [Hugging Face Model Hub](https://huggingface.co/facebook/detr-resnet-50)

### Model Download

The DETR model is automatically downloaded from Hugging Face on the first object detection request. This is a one-time download that typically takes 1-3 minutes depending on your internet connection. The model files (~500MB-1GB) are cached in your Hugging Face cache directory (usually `~/.cache/huggingface/` on Linux/Mac or `C:\Users\<username>\.cache\huggingface\` on Windows) for subsequent use.

**Note**: The first detection request will be slower as it needs to download and load the model. Subsequent requests will be faster as the model is cached locally.

## Performance & Asynchronous Processing

### Asynchronous Processing

The API is built with **fully asynchronous route handlers** to maximize performance and concurrency:

- All route handlers use `async def` for non-blocking request handling
- Synchronous operations (file I/O, image processing, ML inference) are wrapped in `asyncio.to_thread()` to prevent event loop blocking
- This allows the API to handle multiple concurrent requests efficiently
- CPU-intensive tasks (image processing, object detection) run in thread pools without blocking other requests

### Architecture Benefits

- **High Concurrency**: Multiple requests can be processed simultaneously
- **Non-Blocking I/O**: File operations don't block the event loop
- **Scalable**: Efficient resource utilization for handling large workloads
- **Responsive**: The API remains responsive even during heavy processing tasks

## Design Patterns

### Dependency Injection

The architecture uses dependency injection throughout:
- Services receive dependencies through constructor injection
- Configuration is injected rather than accessed globally
- Makes testing easier and code more maintainable

### Separation of Concerns

Each layer has a clear responsibility:
- Routes handle HTTP concerns
- Managers coordinate business logic
- Services implement core functionality
- Utils provide reusable helpers

### Single Responsibility Principle

Each module and class has a focused purpose:
- Image services handle image operations
- Detection services handle object detection
- Storage services handle file operations
- Validators handle input validation

## Data Flow

### Image Upload Flow

1. Request received at API route
2. File validated by validator
3. Image stored via storage service
4. Metadata saved via CRUD operations
5. Response returned to client

### Image Processing Flow

1. Request received at API route
2. Image retrieved via storage service
3. Processing applied via image editor service
4. Processed image saved
5. Response returned to client

### Object Detection Flow

1. Request received at API route
2. Image retrieved via storage service
3. Detection performed via detection service (using DETR model)
4. Results processed and visualized
5. Output saved and response returned

## Storage Architecture

The API uses a local file-based storage system:

- **Uploaded Images**: Stored in `app/static/uploaded/`
- **Edited Images**: Stored in `app/static/edited/`
- **Detection Outputs**: Stored in `app/static/detected/`

The storage system is abstracted through a base storage interface, allowing for future migration to cloud storage (S3, Azure Blob, etc.) without changing business logic.

## Logging & Monitoring

- **Logging**: Structured logging to `logs/app.log`
- **Health Checks**: `/health` endpoint for monitoring
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Rate Limiting**: Per-endpoint rate limiting to prevent abuse

## Future Architecture Considerations

- **Authentication**: Planned addition of authentication layer
- **Caching**: Potential Redis integration for frequently accessed data
- **Message Queue**: For batch processing operations
- **Cloud Storage**: Migration path for cloud-based storage
- **Microservices**: Potential split into separate services for scaling

## Related Documentation

- [Installation Guide](INSTALLATION.md) - Setup and configuration
- [Development Guide](DEVELOPMENT.md) - Development practices
- [Deployment Guide](DEPLOYMENT.md) - Production deployment
- [API Documentation](API.md) - API reference

---

[← Back to Main README](../README.md) | [Documentation Index](README.md)

