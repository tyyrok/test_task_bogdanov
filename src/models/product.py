from datetime import datetime

from sqlalchemy import Boolean, BigInteger, DateTime, DECIMAL, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from models.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str]
    article: Mapped[str] = mapped_column(String, index=True, unique=True)
    price: Mapped[float] = mapped_column(DECIMAL)
    rating: Mapped[float]
    total_amount: Mapped[int] = mapped_column(BigInteger, default=0)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"{self.title} id:{self.id}"
