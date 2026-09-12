from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from demo_shop import Catalog, Product, create_order, place_order


class OrderTests(TestCase):
    def setUp(self) -> None:
        self.catalog = Catalog([Product("BOOK-1", "A Small Book", 1200, 3)])

    def test_create_order_applies_discount(self) -> None:
        order = create_order(self.catalog, " book-1 ", 2, "WELCOME10")
        self.assertEqual(order.total_cents, 2160)

    def test_place_order_writes_receipt(self) -> None:
        with TemporaryDirectory() as directory:
            receipt = Path(directory) / "receipt.txt"
            order = place_order(self.catalog, "BOOK-1", 1, receipt)

            self.assertEqual(order.total_cents, 1200)
            self.assertIn("SKU: BOOK-1", receipt.read_text(encoding="utf-8"))
