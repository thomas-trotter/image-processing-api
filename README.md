
# 🖼️ Image Processing API

A **FastAPI**-powered RESTful service designed for efficient image management, processing, and object detection. Ideal for handling image uploads, applying transformations, and detecting objects in images.

## ✨ Key Features

- **🗂️ Image Management**  
  - Upload, retrieve, list, and delete images  
  - Store and manage images in a scalable way

- **🛠️ Image Processing**  
  - Apply various image filters (e.g., grayscale, sepia)  
  - Resize, rotate with expanding  
  - Adjust brightness, contrast, and other image properties  
  - Validate uploaded images for format and integrity

- **🔍 Object Detection**  
  - Detect objects within images using bounding boxes  
  - Return confidence scores for each detected object

- **🧹 Cleanup and Maintenance**  
  - Automatically clean up `__pycache__` folders when the API is shut down
    
---

## AI Model: DETR (DEtection TRansformer)

This project uses the **DEtection TRansformer (DETR)** model for object detection. DETR combines a Transformer architecture with a ResNet-50 backbone, enabling efficient and accurate object detection in images.

### Key Components:
- **Model**: `facebook/detr-resnet-50`
  - A pre-trained object detection model that uses Transformers to understand the global context.
  - Fine-tuned for detecting a wide variety of objects.

### Initialisation:
The processor and model are loaded as follows:

```python
from transformers import DetrImageProcessor, DetrForObjectDetection

# Initialise the image processor and model
self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", ignore_mismatched_sizes=True)
```

- **`DetrImageProcessor`**: Pre-processes images for model input (resizing, normalisation, etc.).
- **`DetrForObjectDetection`**: Performs object detection and outputs bounding boxes and class predictions.

### Benefits:
- **End-to-End Pipeline**: Simplifies detection without the need for separate components like region proposal networks.
- **High Flexibility**: Can detect a wide variety of objects and is easily adaptable to custom datasets.
- **Transformer-Based**: Captures global image context, improving detection accuracy.

### Example Usage:

```python
# Process image and run object detection
inputs = self.processor(images=image, return_tensors="pt")
outputs = self.model(**inputs)

# Post-process to extract detections
results = self.processor.post_process_object_detection(outputs, target_sizes=[image.size[::-1]], threshold=0.9)[0]
```

### Model Information:
- **Model Name**: `facebook/detr-resnet-50`
- **Source**: [Hugging Face Model Hub](https://huggingface.co/facebook/detr-resnet-50)

---

## 🚀 Getting Started

Follow these steps to set up and run the Image Processing API on your local machine:

### 1. Clone the Repository & Set Up a Virtual Environment

Clone the repository and create a virtual environment for isolating dependencies:

```
git clone https://github.com/Climber1705/image-processing-api.git
cd image-processing-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Configure the Environment

Copy the environment variables template and modify it to match your local setup:

```bash
cp .env.example .env
# Edit .env with the appropriate values (e.g., development, logging type)
```

### 4. Run the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Once the server is running, access the interactive API documentation at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🏗️ Architecture

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

### Module Organization

- **[Core Module](app/core/README.md)**: Configuration, dependencies, logging, rate limiting
- **[API Module](app/api/README.md)**: Route handlers and endpoint definitions
- **[Managers Module](app/managers/README.md)**: Business logic coordination layer
- **[Services Module](app/services/README.md)**: Core business logic implementation
- **[Schemas Module](app/schemas/README.md)**: Request/response validation models
- **[Utils Module](app/utils/README.md)**: Utility functions and helpers

For detailed information about each module, see their respective README files.

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive Documentation
Access the interactive Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Endpoints Overview

#### Image Management (`/images`)

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| POST | `/images/upload` | Upload a new image | 10/min |
| GET | `/images/` | List images with pagination | 60/min |
| GET | `/images/{image_name}/detail` | Get image metadata | 30/min |
| GET | `/images/{image_name}/metadata/dimensions` | Get image dimensions | 20/min |
| DELETE | `/images/{image_name}/delete` | Delete an image | 10/min |
| POST | `/images/{image_name}/move` | Move image between folders | 20/min |
| DELETE | `/images/clear_all` | Delete all images in folder | 2/hour |

#### Image Editing (`/images/edit`)

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| POST | `/images/edit/resize` | Resize image | 10/min |
| POST | `/images/edit/grayscale` | Convert to grayscale | 20/min |
| POST | `/images/edit/rotate` | Rotate image | 15/min |
| POST | `/images/edit/blur` | Apply blur filter | 10/min |
| POST | `/images/edit/sharpen` | Sharpen image | 10/min |
| POST | `/images/edit/brightness` | Adjust brightness | 20/min |
| POST | `/images/edit/contrast` | Adjust contrast | 20/min |

#### Object Detection (`/images/detect`)

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| POST | `/images/detect/bounding_boxes/` | Detect objects with visualization | 5/min |
| GET | `/images/detect/detected_objects/` | Get detection metadata | 10/min |

### Example Requests

#### Upload an Image
```bash
curl -X POST "http://localhost:8000/images/upload" \
  -F "file=@photo.jpg" \
  -F "filename=my_photo" \
  -F "format=JPEG"
```

#### Resize an Image
```bash
curl -X POST "http://localhost:8000/images/edit/resize?image_name=photo.jpg&width=800&height=600"
```

#### Detect Objects
```bash
curl -X POST "http://localhost:8000/images/detect/bounding_boxes/?image_name=photo.jpg"
```

For complete API documentation with request/response schemas, visit the [interactive docs](http://localhost:8000/docs).

---

## 🧪 Testing

The project includes a comprehensive test suite with unit and integration tests, targeting 80%+ code coverage.

### Test Structure

The test suite is organized into two main categories:

- **Unit Tests** (`tests/unit/`): Test individual components in isolation
  - Services: image_editor, crud_operations, metadata_handler, local_storage, detection_service
  - Managers: image_manager, edit_manager, detection_manager
  - Utils: file_utils, directory_utils, validators

- **Integration Tests** (`tests/integration/`): Test API endpoints and end-to-end workflows
  - Image routes: upload, list, get details, delete, move, clear all
  - Editing routes: resize, rotate, grayscale, blur, sharpen, brightness, contrast
  - Detection routes: bounding boxes, detected objects
  - End-to-end workflows: complete user scenarios

### Running Tests

Run all tests:
```bash
pytest
```

Run unit tests only:
```bash
pytest tests/unit
```

Run integration tests only:
```bash
pytest tests/integration
```

Run with coverage report:
```bash
pytest --cov=app --cov-report=html
```

The HTML coverage report will be generated in `htmlcov/index.html`.

Run a specific test file:
```bash
pytest tests/unit/services/test_image_editor.py
```

### Test Coverage

The test suite maintains 80%+ code coverage. Coverage reports are generated automatically when running tests with the `--cov` flag. The project uses pytest-cov for coverage tracking and HTML report generation.

For comprehensive test documentation, including detailed test descriptions, fixtures, and testing strategies, see the [Test Suite Documentation](tests/README.md).

---

## 📂 **Repository Structure**
Here's a quick overview of the project file structure:
```graphql
image-processing-api/
│
├── app/
│   ├── api/
│   |   ├── routes/
│   |   |   ├── __init__.py
│   |   |   ├── detection_routes.py
│   |   |   ├── editing_routes.py
│   |   |   └── image_routes.py
│   |   └── __init__.py          
│   ├── core/
│   |   ├── __init__.py
│   |   ├── config.py
│   |   ├── dependencies.py
│   |   ├── logging_config.py
│   |   └── rate_limiting.py      
│   ├── managers/
│   |   ├── __init__.py
│   |   ├── detection_manager.py
│   |   ├── edit_manager.py
│   |   └── image_manager.py 
|   ├── schemas/
│   |   ├── detection/
│   |   |   ├── __init__.py
│   |   |   └── detection_responses.py
│   |   ├── editing/
│   |   |   ├── __init__.py
│   |   |   ├── editing_requests.py
│   |   |   └── editing_responses.py
│   |   ├── image/
│   |   |   ├── __init__.py
│   |   |   ├── image_requests.py
│   |   |   └── image_responses.py
│   |   └── __init__.py 
|   ├── services/
│   |   ├── detection/
│   |   |   ├── __init__.py
│   |   |   └── detection_service.py
│   |   ├── image/
│   |   |   ├── storage/
│   |   |   |   ├── __init__.py
│   |   |   |   ├── base_storage.py
│   |   |   |   └── local_storage.py
│   |   |   ├── __init__.py
│   |   |   ├── crud_operations.py
│   |   |   ├── image_editor.py
│   |   |   └── metadata_handler.py
│   |   └── __init__.py   
|   ├── utils/
│   |   ├── file_operations/
│   |   |   ├── __init__.py.py
│   |   |   ├── directory_utils.py
│   |   |   └── file_utils.py
│   |   ├── system/
│   |   |   ├── __init__.py.py
│   |   |   ├── clean_up.py
│   |   |   └── lifespan.py
│   |   ├── validator/
│   |   |   ├── __init__.py.py
│   |   |   ├── base_validator.py
│   |   |   └── simple_validator.py
│   |   └── __init__.py   
|   ├── __init__.py             
│   └── main.py          
│── logs/ 
│   └── app.log    
│── .env-example
├── LICENSE      
├── README.md             
└── requirements.txt             
```

## ⚡ Performance & Architecture

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

## 🛠️ Future Improvements

Stay tuned for these upcoming features:

- 🔒 **Authentication**:  
  Secure the API with user authentication.

- 🖼️ **Batch Operations**:  
  Enable batch processing for uploading and processing multiple images at once.

- 🎨 **Extended Format & Filters**:  
  Support more image file formats (e.g., WebP, BMP) and advanced image effects (e.g crop, watermarks)

- 📄 **Pagination Support**:  
  Efficiently handle large image collections by paginating through the results.

---

## 📖 Module Documentation

For detailed documentation on specific modules:

- [Core Module](app/core/README.md) - Configuration and infrastructure
- [API Routes](app/api/README.md) - Endpoint definitions
- [Managers](app/managers/README.md) - Business logic coordination
- [Services](app/services/README.md) - Core business logic
  - [Image Services](app/services/image/README.md) - Image processing services
  - [Detection Services](app/services/detection/README.md) - Object detection services
- [Schemas](app/schemas/README.md) - Request/response models
- [Utils](app/utils/README.md) - Utility functions

---

## 📄 License

This project is licensed under the terms of the [GNU License](https://github.com/Climber1705/image-processing-api/blob/main/LICENSE).

