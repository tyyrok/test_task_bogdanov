from typing import Optional

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.product import crud_product
from databases.database import master_session
from models import Product
from schemas.product import ProductCreateDB
from utilities.api_request import make_request
from utilities.exceptions import (
    APIParseError,
    ProductNotFounError,
)


BASE_URL = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30"


async def subscribe_to_product(article: str) -> None:
    await import_product(article=article, is_subscribed=True)


async def import_product(
    article: str, is_subscribed: Optional[bool] = False
) -> Product:
    res = await make_request(url=f"{BASE_URL}&nm={article}", method="GET")
    res = await parse_response(res, article)
    try:
        schema = ProductCreateDB.model_validate(res)
    except ValidationError as ex:
        raise APIParseError(str(ex)) from ex

    if is_subscribed:
        schema.is_subscribed = True

    async with master_session() as db:  # noqa: SIM117
        async with db.begin():
            if found_product := await crud_product.get_by_article(
                db=db, article=article
            ):
                found_product = await crud_product.update(
                    db=db,
                    db_obj=found_product,
                    update_data=schema,
                    commit=False,
                )
            else:
                found_product = await crud_product.create(
                    db=db, create_schema=schema, commit=False
                )
    return found_product


async def parse_response(res: dict, article: str) -> dict:
    parsed_res = {}
    if data := res.get("data"):
        if products := data.get("products"):
            product = products[0]
            parsed_res["title"] = product.get("name", "")
            parsed_res["article"] = article
            parsed_res["price"] = product.get("salePriceU")
            parsed_res["rating"] = product.get("rating")
            parsed_res["total_amount"] = product.get("totalQuantity")
            return parsed_res

        msg = f"Product with article {article} not found"
        raise ProductNotFounError(msg)
    msg = "Response API error for product article"
    raise APIParseError(msg)


async def update_subscribed_products(db: AsyncSession) -> str:
    if found_products := await crud_product.get_multi_subscribed(db):
        for product in found_products:
            await import_product(product.article)
    return f"Updated {len(found_products)} products"
