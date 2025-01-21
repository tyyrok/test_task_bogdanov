from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from crud.async_crud import BaseAsyncCRUD
from models import Product
from schemas.product import ProductCreateDB, ProductUpdateDB


class CRUDProduct(
    BaseAsyncCRUD[Product, ProductCreateDB, ProductUpdateDB],
):
    async def get_by_article(
        self, db: AsyncSession, article: str
    ) -> Optional[Product]:
        statement = select(self.model).where(self.model.article == article)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_multi_subscribed(
        self, db: AsyncSession
    ) -> Sequence[Product]:
        statement = select(self.model).where(
            self.model.is_subscribed.is_(True)
        )
        result = await db.execute(statement)
        return result.scalars().all()


crud_product = CRUDProduct(Product)
