from abc import ABC, abstractmethod
from typing import Optional
from fastapi import UploadFile

class BaseImageStorage(ABC):
    """
    Abstract Base Class for image storage operations.
    This class defines the required methods for saving, retrieving, and deleting images.
    Subclasses should implement these methods with their specific storage logic.
    """
    
    @abstractmethod
    def save(self, file: UploadFile, folder: Optional[str] = None, filename: Optional[str] = None, format: Optional[str] = "JPEG") -> str:
        """
        Save an image and return the storage path or URL.
        
        Args:
            file (UploadFile): The image file to be saved.
            folder (Optional[str]): The optional folder where the image should be stored (default is None).
            filename (Optional[str]): The optional filename to save the image as (default is None).
            format (Optional[str]): The format of the image (e.g., "JPEG", "PNG") to save the image as (default is "JPEG").
        
        Returns:
            str: The storage path or URL of the saved image.
        """
        pass
    
    @abstractmethod
    def get_url(self, filename: str) -> str:
        """
        Return a public URL or path to the stored image.
        
        Args:
            filename (str): The name of the image file.
        
        Returns:
            str: The URL or path to the stored image.
        """
        pass
    
    @abstractmethod
    def delete(self, directory: str, filename: str) -> bool:
        """
        Delete the image and return success status.
        
        Args:
            directory (str): The folder where the image is located.
            filename (str): The name of the image file to be deleted.
        
        Returns:
            bool: True if deletion is successful, False otherwise.
        """
        pass
