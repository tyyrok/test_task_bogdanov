from fastapi import APIRouter, HTTPException, status

from crud.product import crud_product
from databases.database import master_session
from schemas.product import ProductResponse, ProductSearch
from service import product as product_service
from utilities.exceptions import (
    APIParseError,
    ProductNotFounError,
    ServiceUnavailbleError,
)

router = APIRouter()


@router.get("/products/{article}/", response_model=ProductResponse)
async def read_product(article: str):
    async with master_session() as db:
        if found_product := await crud_product.get_by_article(
            db=db, article=article
        ):
            return found_product

    try:
        return await product_service.import_product(article)
    except ProductNotFounError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ex.message
        ) from ex
    except ServiceUnavailbleError as ex:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=ex.message
        ) from ex
    except APIParseError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ex.message,
        ) from ex


@router.post("/products/", status_code=status.HTTP_201_CREATED)
async def add_product(product_article: ProductSearch):
    try:
        await product_service.import_product(product_article.article)
    except ProductNotFounError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ex.message
        ) from ex
    except ServiceUnavailbleError as ex:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=ex.message
        ) from ex
    except APIParseError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ex.message,
        ) from ex


@router.get("/subscribe/{article}/", status_code=status.HTTP_201_CREATED)
async def subscribe_to_product(article: str):
    async with master_session() as db:
        if found_product := await crud_product.get_by_article(
            db=db, article=article
        ):
            found_product.is_subscribed = True
            return await db.commit()
    try:
        return await product_service.subscribe_to_product(article)
    except ProductNotFounError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ex.message
        ) from ex
    except ServiceUnavailbleError as ex:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=ex.message
        ) from ex
    except APIParseError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ex.message,
        ) from ex
