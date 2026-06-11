from fastapi import APIRouter

from app.services.price_collector_service import PriceCollectorService
from app.database.session import async_session_factory
from app.database.models.product import Product

router = APIRouter()


@router.post("/products/parse")
async def parse_product(data: dict):

    product_id = data["product_id"]

    async with async_session_factory() as db:

        product = Product(
            id=product_id,
            external_id=product_id,
            marketplace=data.get("marketplace", "ozon")
        )

        service = PriceCollectorService(db)

        await service.collect_product(product)

        return {
            "product_id": product_id,
            "status": "parsed"
        }