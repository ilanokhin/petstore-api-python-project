from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime


class OrderModel(BaseModel):
    class Status(str, Enum):
        placed = "placed"
        approved = "approved"
        delivered = "delivered"

    id: Optional[int] = None
    petId: Optional[int] = None
    quantity: Optional[int] = None
    shipDate: Optional[datetime] = None
    status: Optional[Status] = None
    complete: Optional[bool] = None
