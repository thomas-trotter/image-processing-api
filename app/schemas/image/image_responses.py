from pydantic import BaseModel
from typing import Optional


class StatusResponse(BaseModel):
    """
    Represents a status response with a status message.
    
    Attributes:
        status (str): A string representing the status, such as "success" or "failure".
    """
    status: str 


class ImageMetadata(BaseModel):
    """
    Represents the metadata of an image, such as its format, mode, and dimensions.
    
    Attributes:
        format (str): The format of the image (e.g., JPEG, PNG).
        mode (str): The mode of the image (e.g., RGB, L).
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
    """
    format: str
    mode: str    
    width: int   
    height: int  


class ImageResponse(BaseModel):
    """
    Represents the response for an image operation that includes status, path, and metadata.
    
    Attributes:
        status (str): The status of the operation (e.g., "success").
        path (str): The file path to the image.
        metadata (ImageMetadata): Metadata details of the image (format, mode, dimensions).
    """
    status: str      
    path: str     
    metadata: ImageMetadata  


class ImageListItem(BaseModel):
    """
    Represents a basic image item with essential attributes to be displayed in a list.
    
    Attributes:
        filename (str): The name of the image file.
        format (str): The format of the image (e.g., JPEG, PNG).
        mode (str): The mode of the image (e.g., RGB, L).
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
        size_bytes (int): The size of the image file in bytes.
        path (str): The file path to the image.
        url (Optional[str]): Placeholder for a URL, currently set to None.
        folder (str): The folder where the image is stored.
    """
    filename: str 
    format: str  
    mode: str     
    width: int     
    height: int    
    size_bytes: int  
    path: str      
    url: Optional[str] = None      
    folder: str   


class ImageDetailResponse(BaseModel):
    """
    Represents a detailed response for an image, including its metadata and other details.
    
    Attributes:
        filename (str): The name of the image.
        format (str): The format of the image (e.g., JPEG, PNG).
        mode (str): The mode of the image (e.g., RGB, L).
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
        size_bytes (int): The size of the image file in bytes.
        path (str): The file path to the image.
        url (Optional[str]): Placeholder for a URL, currently set to None.
    """
    filename: str  
    format: str    
    mode: str     
    width: int   
    height: int      
    size_bytes: int  
    path: str        
    url: Optional[str] = None        


class ImageDimensionsResponse(BaseModel):
    """
    Represents the dimensions (width and height) of an image.
    
    Attributes:
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
    """
    width: int    
    height: int   
