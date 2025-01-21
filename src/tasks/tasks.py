from databases.database import master_session
from project_celery import celery_app
from service.product import update_subscribed_products
from utilities.async_utils import run_async


@celery_app.task
def update_subcribed_products_task() -> None:
    async def task() -> None:
        async with master_session() as db:
            return await update_subscribed_products(db)

    return run_async(task())
