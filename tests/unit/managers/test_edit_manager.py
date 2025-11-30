"""
Unit tests for EditManager.
"""

import pytest
from fastapi import HTTPException

from app.managers.edit_manager import EditManager


@pytest.mark.unit
class TestEditManager:
    """Test cases for EditManager."""

    @pytest.fixture
    def edit_manager(self, mock_image_edit_service):
        """Create EditManager with mocked dependencies."""
        return EditManager(edit_service=mock_image_edit_service)

    def test_apply_resize(self, edit_manager):
        """Test applying resize operation."""
        result = edit_manager.apply_resize("test.jpg", 400, 300)
        
        assert result is not None
        edit_manager.edit_service.resize_image.assert_called_once_with("test.jpg", 400, 300)

    def test_apply_grayscale(self, edit_manager):
        """Test applying grayscale conversion."""
        result = edit_manager.apply_grayscale("test.jpg")
        
        assert result is not None
        edit_manager.edit_service.convert_to_grayscale.assert_called_once_with("test.jpg")

    def test_apply_rotation(self, edit_manager):
        """Test applying rotation."""
        result = edit_manager.apply_rotation("test.jpg", 90, True)
        
        assert result is not None
        edit_manager.edit_service.rotate_image.assert_called_once_with("test.jpg", 90, True)

    def test_apply_blur(self, edit_manager):
        """Test applying blur filter."""
        result = edit_manager.apply_blur("test.jpg", 5.0)
        
        assert result is not None
        edit_manager.edit_service.blur_image.assert_called_once_with("test.jpg", 5.0)

    def test_apply_sharpen(self, edit_manager):
        """Test applying sharpen filter."""
        result = edit_manager.apply_sharpen("test.jpg", 2.0, 2.0, 3)
        
        assert result is not None
        edit_manager.edit_service.sharpen_image.assert_called_once_with("test.jpg", 2.0, 2.0, 3)

    def test_apply_brightness(self, edit_manager):
        """Test applying brightness adjustment."""
        result = edit_manager.apply_brightness("test.jpg", 1.5)
        
        assert result is not None
        edit_manager.edit_service.adjust_brightness.assert_called_once_with("test.jpg", 1.5)

    def test_apply_contrast(self, edit_manager):
        """Test applying contrast adjustment."""
        result = edit_manager.apply_contrast("test.jpg", 1.2)
        
        assert result is not None
        edit_manager.edit_service.adjust_contrast.assert_called_once_with("test.jpg", 1.2)

    def test_process_image_edit_success(self, edit_manager):
        """Test successful image edit processing."""
        edit_manager.edit_service.resize_image.return_value = "/path/to/resized.jpg"
        
        result = edit_manager.process_image_edit("test.jpg", edit_manager.edit_service.resize_image, "test.jpg", 400, 300)
        
        assert result == "/path/to/resized.jpg"

    def test_process_image_edit_error(self, edit_manager):
        """Test error handling in process_image_edit."""
        edit_manager.edit_service.resize_image.side_effect = Exception("Processing failed")
        
        with pytest.raises(HTTPException) as exc_info:
            edit_manager.process_image_edit("test.jpg", edit_manager.edit_service.resize_image, "test.jpg", 400, 300)
        
        assert exc_info.value.status_code == 500

    def test_apply_bulk_edits(self, edit_manager):
        """Test applying multiple edits."""
        edits = {
            "resize": {"width": 400, "height": 300},
            "grayscale": True
        }
        
        result = edit_manager.apply_bulk_edits("test.jpg", edits)
        
        assert result is not None
        assert "resize" in result
        assert "grayscale" in result

