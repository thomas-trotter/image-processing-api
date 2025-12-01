from abc import ABC, abstractmethod
from fastapi import UploadFile

class BaseImageValidator(ABC):
    """
    Abstract base class for validating image files.
    
    This class defines the structure for image validation logic. Subclasses should implement
    the `validate` method to provide their own image validation logic.
    """

    @abstractmethod
    def validate(self, image: UploadFile) -> None:
        """
        Validate the given image file.

        Args:
            image (UploadFile): The image file to be validated, provided as an `UploadFile` instance from FastAPI.
        """
        pass
