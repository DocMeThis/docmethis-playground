"""Products and catalog lookups for the demo shop."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


class ProductNotFound(LookupError):
    """Raised when a requested SKU is not present in the catalog."""


class OutOfStockError(RuntimeError):
    """Raised when an order requests more units than are available."""


@dataclass(frozen=True, slots=True)
class Product:
    """A product that can be ordered from the demo catalog.

    Attributes
    ----------
    sku : str
        Stable stock-keeping unit used to find the product.
    name : str
        Human-readable product name.
    price_cents : int
        Unit price in the smallest currency unit.
    stock : int
        Number of units currently available.

    """

    sku: str
    name: str
    price_cents: int
    stock: int


class Catalog:
    """An in-memory product catalog.

    Attributes
    ----------
    _products : dict[str, Product]
        Products indexed by their normalized SKU.

    Parameters
    ----------
    products : Iterable[Product]
        Products to make available for lookup.

    Raises
    ------
    ProductNotFound
        If a lookup requests a SKU that is not in the catalog.

    """

    def __init__(self, products: Iterable[Product]) -> None:
        """Create a catalog from an iterable of products.

        Parameters
        ----------
        products : Iterable[Product]
            Products to make available for lookup.

        """
        self._products = {_normalize_sku(product.sku): product for product in products}

    def find(self, sku: str) -> Product:
        """Return the product identified by a SKU.

        Parameters
        ----------
        sku : str
            Product SKU, with surrounding whitespace and case ignored.

        Returns
        -------
        Product
            The matching product.

        Raises
        ------
        ProductNotFound
            If the SKU is not in the catalog.

        """
        product = self._products.get(_normalize_sku(sku))
        if product is None:
            raise ProductNotFound(f"Unknown SKU: {sku}")
        return product


def _normalize_sku(sku: str) -> str:
    """Normalize a SKU for internal catalog lookup.

    Parameters
    ----------
    sku : str
        SKU to normalize.

    Returns
    -------
    str
        Uppercase SKU without surrounding whitespace.

    """
    return sku.strip().upper()
