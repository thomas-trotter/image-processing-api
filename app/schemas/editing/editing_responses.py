from pydantic import BaseModel 
from typing import List


class EditResponse(BaseModel):
    """
    Represents the response after applying an edit to a single image.
    
    Attributes:
        path (str): The file path to the edited image.
    """
    path: str

