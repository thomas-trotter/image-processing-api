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

## 🚀 5-Minute Quickstart

### Get Started with Docker (Recommended)

```bash
docker-compose -f docker-compose.dev.yml up --build
```

Access the API at [http://localhost:8000](http://localhost:8000)  
Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Try It Out

Upload an image:
```bash
curl -X POST "http://localhost:8000/images/upload" \
  -F "file=@photo.jpg" \
  -F "filename=my_photo" \
  -F "format=JPEG"
```

For more examples and detailed setup, see the [Quick Start Guide](docs/QUICKSTART.md).

---

## 📋 Prerequisites

- **Python 3.12+** (for manual setup)
- **Docker & Docker Compose** (for Docker setup)
- **Internet Connection** (for initial model download)
- **Disk Space**: ~3-4GB minimum
- **Memory**: 4GB RAM minimum, 8GB+ recommended

For detailed system requirements, see the [Installation Guide](docs/INSTALLATION.md).

---

## ⚡ Quick Installation

### Docker (Recommended)

**Development:**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

**Production:**
```bash
docker-compose -f docker-compose.yml up --build -d
```

### Manual Setup

```bash
git clone https://github.com/Climber1705/image-processing-api.git
cd image-processing-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env-example .env
uvicorn app.main:app --reload
```

For detailed installation instructions, see the [Installation Guide](docs/INSTALLATION.md).

---

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/README.md) directory:

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get running in minutes
- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup and configuration
- **[API Documentation](docs/API.md)** - Complete API reference
- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design and DETR model details
- **[Development Guide](docs/DEVELOPMENT.md)** - Testing and development guidelines
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment best practices
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

---

## 📂 Repository Structure

```
image-processing-api/
│
├── app/
│   ├── api/              # API routes and endpoints
│   ├── core/             # Configuration and infrastructure
│   ├── managers/         # Business logic coordination
│   ├── schemas/          # Request/response models
│   ├── services/         # Core business logic
│   └── utils/            # Utility functions
│
├── docs/                 # Documentation
├── tests/                # Test suite
├── logs/                 # Application logs
│
├── docker-compose.yml    # Production Docker config
├── docker-compose.dev.yml # Development Docker config
├── Dockerfile            # Docker image definition
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

For detailed structure, see the [Architecture Overview](docs/ARCHITECTURE.md).

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

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

For detailed testing instructions, see the [Development Guide](docs/DEVELOPMENT.md).

---

## 📄 License

This project is licensed under the terms of the [GNU License](https://github.com/Climber1705/image-processing-api/blob/main/LICENSE).

---

## 🔗 Quick Links

- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs) (when running)
- **Documentation**: [docs/README.md](docs/README.md)
- **Quick Start**: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
