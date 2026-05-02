from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from models.category_model import CategoryModel
from models.tag_model import TagModel


class PetModel(BaseModel):
    class Status(str, Enum):
        available = "available"
        pending = "pending"
        sold = "sold"

    id: Optional[int] = None
    category: Optional[CategoryModel] = None
    name: str
    photoUrls: List[str]
    tags: Optional[List[TagModel]] = None
    status: Optional[Status] = None
