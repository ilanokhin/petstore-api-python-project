from pydantic import BaseModel
from typing import Optional


class CategoryModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
