"""A tiny shop used by the DocMeThis playground."""

from demo_shop.catalog import Catalog, OutOfStockError, Product, ProductNotFound
from demo_shop.orders import Order, create_order, place_order

__all__ = [
    "Catalog",
    "Order",
    "OutOfStockError",
    "Product",
    "ProductNotFound",
    "create_order",
    "place_order",
]
