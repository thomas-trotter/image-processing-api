# Test Suite Documentation

## Overview

This directory contains comprehensive unit and integration tests for the Image Processing API, targeting 80%+ code coverage.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and test configuration
├── unit/                   # Unit tests for individual components
│   ├── services/          # Service layer tests
│   ├── managers/          # Manager layer tests
│   └── utils/             # Utility tests
└── integration/           # Integration tests for API endpoints
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Unit Tests Only
```bash
pytest tests/unit
```

### Run Integration Tests Only
```bash
pytest tests/integration
```

### Run with Coverage Report
```bash
pytest --cov=app --cov-report=html
```

The HTML coverage report will be generated in `htmlcov/index.html`.

### Run Specific Test File
```bash
pytest tests/unit/services/test_image_editor.py
```

### Run Tests with Markers
```bash
pytest -m unit              # Run only unit tests
pytest -m integration      # Run only integration tests
```

## Test Coverage

The test suite includes:

### Unit Tests
- **Services**: image_editor, crud_operations, metadata_handler, local_storage, detection_service
- **Managers**: image_manager, edit_manager, detection_manager
- **Utils**: file_utils, directory_utils, validators

### Integration Tests
- **Image Routes**: Upload, list, get details, delete, move, clear all
- **Editing Routes**: Resize, rotate, grayscale, blur, sharpen, brightness, contrast
- **Detection Routes**: Bounding boxes, detected objects
- **End-to-End**: Complete workflows (upload→edit→detect, upload→move→delete)

## Key Features

- **Isolated Test Environment**: Each test uses temporary directories
- **Mocked Dependencies**: ML models and external services are mocked
- **Comprehensive Coverage**: Tests cover success cases, error cases, and edge cases
- **Fast Execution**: Unit tests run quickly without loading actual ML models

## Dependencies

Test dependencies are listed in `requirements.txt`:
- pytest
- pytest-asyncio
- pytest-cov
- httpx
- pytest-mock
- faker

## Notes

- ML models (DETR) are mocked to avoid loading actual models during testing
- Test images are created programmatically using PIL
- All file operations use temporary directories that are cleaned up after tests
- FastAPI dependency overrides are used for integration tests