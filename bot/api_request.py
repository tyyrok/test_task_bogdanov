import httpx

from exceptions import ProductNotFounError, ServiceUnavailbleError

URL = "https://32d0-31-146-89-127.ngrok-free.app/api/v1/products"


async def make_request(article: str) -> dict:
    async with httpx.AsyncClient() as client:
        url = f"{URL}/{article}/"
        r = await client.request(
            method="GET",
            url=url,
        )
        if r.status_code in [404]:
            msg = f"Product with article {article} not found"
            raise ProductNotFounError(msg)
        if r.status_code in [500, 503]:
            msg = "Service unavailble"
            raise ServiceUnavailbleError(msg)
        return r.json()
