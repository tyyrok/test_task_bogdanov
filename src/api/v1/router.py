from fastapi import APIRouter

from api.v1.endpoints.product import router as product_router

router = APIRouter(prefix="/api/v1")

router.include_router(product_router, prefix="", tags=["Product"])
