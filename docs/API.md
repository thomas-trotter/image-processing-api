# API Documentation

[← Back to Main README](../README.md)

Complete API reference for the Image Processing API.

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

Access the interactive Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

The Swagger UI provides:
- Complete endpoint documentation
- Try-it-out functionality
- Request/response schemas
- Authentication (when implemented)

## Endpoints Overview

### System Routes

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| GET | `/` | Root endpoint with welcome message | None |
| GET | `/health` | Health check endpoint for monitoring | None |

### Image Management (`/images`)

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| POST | `/images/upload` | Upload a new image | 10/min |
| GET | `/images/` | List images with pagination | 60/min |
| GET | `/images/{image_name}/detail` | Get image metadata | 30/min |
| GET | `/images/{image_name}/metadata/dimensions` | Get image dimensions | 20/min |
| DELETE | `/images/{image_name}/delete` | Delete an image | 10/min |
| POST | `/images/{image_name}/move` | Move image between folders | 20/min |
| DELETE | `/images/clear_all` | Delete all images in folder | 2/hour |

### Image Editing (`/images/edit`)

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| POST | `/images/edit/resize` | Resize image | 10/min |
| POST | `/images/edit/grayscale` | Convert to grayscale | 20/min |
| POST | `/images/edit/rotate` | Rotate image | 15/min |
| POST | `/images/edit/blur` | Apply blur filter | 10/min |
| POST | `/images/edit/sharpen` | Sharpen image | 10/min |
| POST | `/images/edit/brightness` | Adjust brightness | 20/min |
| POST | `/images/edit/contrast` | Adjust contrast | 20/min |

### Object Detection (`/images/detect`)

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| POST | `/images/detect/bounding_boxes/` | Detect objects with visualization | 5/min |
| GET | `/images/detect/detected_objects/` | Get detection metadata | 10/min |

## Example Requests

### Upload an Image

```bash
curl -X POST "http://localhost:8000/images/upload" \
  -F "file=@photo.jpg" \
  -F "filename=my_photo" \
  -F "format=JPEG"
```

**Response:**
```json
{
  "message": "Image uploaded successfully",
  "filename": "my_photo.jpg",
  "format": "JPEG"
}
```

### List Images

```bash
curl http://localhost:8000/images/
```

**Response:**
```json
{
  "images": [
    {
      "name": "my_photo.jpg",
      "format": "JPEG",
      "size": 1234567,
      "uploaded_at": "2024-01-01T12:00:00"
    }
  ],
  "total": 1
}
```

### Get Image Details

```bash
curl http://localhost:8000/images/my_photo.jpg/detail
```

### Get Image Dimensions

```bash
curl http://localhost:8000/images/my_photo.jpg/metadata/dimensions
```

### Resize an Image

```bash
curl -X POST "http://localhost:8000/images/edit/resize?image_name=photo.jpg&width=800&height=600"
```

**Query Parameters:**
- `image_name` (required): Name of the image to resize
- `width` (required): New width in pixels
- `height` (required): New height in pixels

### Rotate an Image

```bash
curl -X POST "http://localhost:8000/images/edit/rotate?image_name=photo.jpg&angle=90"
```

**Query Parameters:**
- `image_name` (required): Name of the image to rotate
- `angle` (required): Rotation angle in degrees (90, 180, 270)

### Convert to Grayscale

```bash
curl -X POST "http://localhost:8000/images/edit/grayscale?image_name=photo.jpg"
```

### Apply Blur Filter

```bash
curl -X POST "http://localhost:8000/images/edit/blur?image_name=photo.jpg&radius=5"
```

**Query Parameters:**
- `image_name` (required): Name of the image
- `radius` (optional): Blur radius (default: 2)

### Sharpen Image

```bash
curl -X POST "http://localhost:8000/images/edit/sharpen?image_name=photo.jpg"
```

### Adjust Brightness

```bash
curl -X POST "http://localhost:8000/images/edit/brightness?image_name=photo.jpg&factor=1.5"
```

**Query Parameters:**
- `image_name` (required): Name of the image
- `factor` (required): Brightness factor (1.0 = no change, >1.0 = brighter, <1.0 = darker)

### Adjust Contrast

```bash
curl -X POST "http://localhost:8000/images/edit/contrast?image_name=photo.jpg&factor=1.2"
```

**Query Parameters:**
- `image_name` (required): Name of the image
- `factor` (required): Contrast factor (1.0 = no change, >1.0 = more contrast)

### Detect Objects

```bash
curl -X POST "http://localhost:8000/images/detect/bounding_boxes/?image_name=photo.jpg"
```

**Response:**
```json
{
  "image_name": "photo.jpg",
  "detections": [
    {
      "label": "person",
      "confidence": 0.95,
      "bbox": [100, 150, 200, 300]
    }
  ],
  "output_image": "detected_photo.jpg"
}
```

**Note**: The first detection request will take 1-3 minutes as the DETR model downloads. Subsequent requests will be faster.

### Get Detection Metadata

```bash
curl http://localhost:8000/images/detect/detected_objects/?image_name=photo.jpg
```

### Move Image Between Folders

```bash
curl -X POST "http://localhost:8000/images/my_photo.jpg/move?source_folder=uploaded&target_folder=edited"
```

**Query Parameters:**
- `source_folder` (required): Current folder (uploaded, edited, detected)
- `target_folder` (required): Destination folder (uploaded, edited, detected)

### Delete an Image

```bash
curl -X DELETE "http://localhost:8000/images/my_photo.jpg/delete"
```

### Clear All Images

```bash
curl -X DELETE "http://localhost:8000/images/clear_all?folder=uploaded"
```

**Query Parameters:**
- `folder` (optional): Folder to clear (uploaded, edited, detected). Defaults to all folders.

## Rate Limiting

The API implements rate limiting to ensure fair usage and prevent abuse. Rate limits are applied per endpoint and are reset periodically. If you exceed the rate limit, you'll receive a `429 Too Many Requests` response.

Rate limits are specified in the endpoint tables above. Common limits:
- Image upload: 10 requests per minute
- Image listing: 60 requests per minute
- Object detection: 5 requests per minute
- Image editing: 10-20 requests per minute depending on operation

## Error Responses

The API uses standard HTTP status codes:

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Image Formats

Supported image formats:
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)

Maximum file size: 5MB per image

## Additional Resources

- [Quick Start Guide](QUICKSTART.md) - Get started quickly
- [Installation Guide](INSTALLATION.md) - Detailed setup instructions
- [Architecture Overview](ARCHITECTURE.md) - System design and architecture

---

[← Back to Main README](../README.md) | [Documentation Index](README.md)

