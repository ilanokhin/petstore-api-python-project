from pydantic import BaseModel
from typing import Optional


class TagModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
