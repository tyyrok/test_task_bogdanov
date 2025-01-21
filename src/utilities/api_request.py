import httpx

from configs.loggers import logger
from utilities.exceptions import ServiceUnavailbleError


async def make_request(
    url: str,
    method: str,
) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            r = await client.request(method=method, url=url)
            r.raise_for_status()
            return r.json()
        except httpx.RequestError as ex:
            logger.exception(ex)
            raise ServiceUnavailbleError(ex.request.url) from ex
