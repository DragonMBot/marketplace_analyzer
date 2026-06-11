from dataclasses import dataclass


@dataclass
class ProductPriceData:
    external_id: str

    title: str | None

    current_price: float | None

    old_price: float | None

    marketplace: str