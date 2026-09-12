"""Receipt persistence for the demo shop."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demo_shop.orders import Order


def write_receipt(order: Order, destination: Path) -> None:
    """Write a compact receipt for an order.

    Parameters
    ----------
    order : Order
        Order to serialize.
    destination : Path
        File that receives the receipt text.

    Raises
    ------
    OSError
        If the destination cannot be written.

    """
    try:
        destination.write_text(
            f"SKU: {order.sku}\nQuantity: {order.quantity}\nTotal: {order.total_cents} cents\n",
            encoding="utf-8",
        )
    except OSError:
        raise
