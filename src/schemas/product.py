from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    article: str
    price: float
    rating: float
    total_amount: int


class ProductCreateDB(ProductBase):
    is_subscribed: Optional[bool] = False


class ProductUpdateDB(ProductBase):
    is_subscribed: Optional[bool] = False


class ProductResponse(ProductBase):
    is_subscribed: bool
    created_at: datetime
    updated_at: datetime


class ProductSearch(BaseModel):
    article: str
