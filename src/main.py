import uvicorn
from fastapi import FastAPI

from api.v1.router import router as v1_router


app = FastAPI(
    title="Product Service",
    openapi_url="/openapi.json/",
    docs_url="/docs/",
)

app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=True,
        forwarded_allow_ips="*",
    )
