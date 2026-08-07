# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestServiceContractFixItemPob(TransactionCase):
    """Covers ``service.contract_fix_item.action_create_pob``.

    ``service.contract_fix_item`` is a SQL view (see
    ``ssi_service.models.service_contract_fix_item``) that groups the
    underlying payment term detail rows by
    ``product_id, product_category_id, name, price_unit, uom_id``. Two
    detail lines for the *same* product but *different* price therefore
    surface as two distinct view rows -- but ``_compute_pob_id`` used to
    search for an existing Performance Obligation by ``product_id`` alone,
    so the second row silently linked to the first row's PoB instead of
    getting its own, understating the contract's total Performance
    Obligation by the second row's amount.

    Reported in ticket OFS/26/000023 -- reproduced against real data on
    contract SVC/2026/000001 (two "Jasa Renovasi Ruangan" lines, Rp
    20.975.000 and Rp 398.525.000, both wrongly linked to the same PoB).

    Also covers OFS/26/000025: ``_prepare_pob_data`` used to assign the
    line's ``amount_untaxed`` (a quantity-multiplied, possibly
    cross-term-summed total) to the PoB's own ``price_unit`` field, instead
    of the line's actual per-unit ``price_unit`` -- making the PoB's Price
    Unit never match the contract item's whenever quantity != 1 or several
    payment term lines were merged into one view row.
    """

    def setUp(self):
        super().setUp()
        env = self.env
        admin = env.ref("base.user_admin")
        self.admin = admin

        self.income_account = env["account.account"].search(
            [("user_type_id.internal_group", "=", "income")], limit=1
        )
        self.uom = env.ref("uom.product_uom_unit")

        self.partner = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Partner - PoB", "is_company": True})
        )
        self.pricelist = env.ref("product.list0")
        self.service_type = (
            env["service.type"]
            .with_user(admin)
            .create({"name": "Test Service Type - PoB", "code": "POBT"})
        )
        self.product = (
            env["product.product"]
            .with_user(admin)
            .create(
                {
                    "name": "Test Generic Lumpsum Service - PoB",
                    "type": "service",
                    "uom_id": self.uom.id,
                    "uom_po_id": self.uom.id,
                }
            )
        )
        self.contract = (
            env["service.contract"]
            .with_user(admin)
            .create(
                {
                    "title": "Test Service Contract - PoB",
                    "partner_id": self.partner.id,
                    "type_id": self.service_type.id,
                    "manager_id": admin.id,
                    "salesperson_id": admin.id,
                    "pricelist_id": self.pricelist.id,
                    "currency_id": env.ref("base.USD").id,
                    "date": "2026-01-01",
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                }
            )
        )
        self.contract.with_user(admin).action_confirm()
        self.contract.with_user(admin).with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        self.contract.invalidate_cache()
        assert self.contract.state == "open"
        assert self.contract.analytic_account_id

    def _create_payment_term(self, name, price_unit, quantity=1):
        term = (
            self.env["service.contract_fix_item_payment_term"]
            .with_user(self.admin)
            .create(
                {
                    "service_id": self.contract.id,
                    "name": name,
                    "sequence": 10,
                }
            )
        )
        detail = (
            self.env["service.contract_fix_item_payment_term_detail"]
            .with_user(self.admin)
            .create(
                {
                    "term_id": term.id,
                    "product_id": self.product.id,
                    "name": self.product.name,
                    "account_id": self.income_account.id,
                    "price_unit": price_unit,
                    "quantity": quantity,
                    "uom_quantity": quantity,
                    "uom_id": self.uom.id,
                    "sequence": 10,
                }
            )
        )
        # service.contract_fix_item is a SQL view reading straight from this
        # model's real table (see _get_fix_items below) -- price_subtotal
        # (which the view sums into amount_untaxed) is a stored compute
        # field, and querying the view does not by itself flush *this*
        # model's pending compute writes. Without an explicit flush here,
        # the view sees amount_untaxed as still 0 for a freshly created
        # line.
        detail.flush()
        return term

    def _get_fix_items(self):
        """Fetch every ``service.contract_fix_item`` view row for the test
        contract/product in a single query.

        The underlying view assigns ids via ``ROW_NUMBER() OVER()`` with no
        ``ORDER BY`` (see ``ssi_service.models.service_contract_fix_item``),
        so id numbering is only self-consistent *within one query
        execution* -- fetching each row via a separate, more narrowly
        filtered ``search()`` call (e.g. one call per ``price_unit``) can
        have Postgres assign the *same* id to two different rows across
        those separate executions, making Odoo treat them as one record.
        Always fetch the full set once and split it with ``.filtered()``
        in Python instead.
        """
        return self.env["service.contract_fix_item"].search(
            [
                ("service_id", "=", self.contract.id),
                ("product_id", "=", self.product.id),
            ]
        )

    def test_different_price_lines_get_distinct_pob(self):
        """Same product, different price -> action_create_pob must not
        silently merge the second line's PoB into the first line's."""
        self._create_payment_term("Term 1", 20975000)
        self._create_payment_term("Term 2", 398525000)

        all_items = self._get_fix_items()
        self.assertEqual(len(all_items), 2)
        item_low = all_items.filtered(lambda i: i.price_unit == 20975000)
        item_high = all_items.filtered(lambda i: i.price_unit == 398525000)
        self.assertTrue(item_low)
        self.assertTrue(item_high)
        self.assertFalse(item_low.pob_id)
        self.assertFalse(item_high.pob_id)

        all_items.action_create_pob()

        all_items = self._get_fix_items()
        item_low = all_items.filtered(lambda i: i.price_unit == 20975000)
        item_high = all_items.filtered(lambda i: i.price_unit == 398525000)
        self.assertTrue(item_low.pob_id)
        self.assertTrue(item_high.pob_id)
        self.assertNotEqual(
            item_low.pob_id.id,
            item_high.pob_id.id,
            "lines with different price must not share the same PoB",
        )
        self.assertEqual(item_low.pob_id.price_unit, 20975000)
        self.assertEqual(item_high.pob_id.price_unit, 398525000)

    def test_same_price_lines_share_one_pob(self):
        """Same product, same price across two terms -> the underlying SQL
        view already groups/sums them into a single row (quantity and
        amount summed across the matching lines), so there is only ever
        one PoB to create for it (sanity check of the view's own
        grouping, not just the compute fix)."""
        self._create_payment_term("Term 1", 15000000)
        self._create_payment_term("Term 2", 15000000)

        item = self._get_fix_items()
        self.assertEqual(len(item), 1)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.amount_untaxed, 30000000)

        item.action_create_pob()

        item = self._get_fix_items()
        self.assertTrue(item.pob_id)
        self.assertEqual(item.pob_id.uom_quantity, 2)
        # price_unit must mirror the *per-unit* price shown on the
        # contract's Items list (OFS/26/000026) -- price_subtotal (=
        # price_unit * uom_quantity, computed by mixin.product_line_price)
        # is where the summed total belongs, not price_unit itself.
        self.assertEqual(item.pob_id.price_unit, 15000000)
        self.assertEqual(item.pob_id.price_subtotal, 30000000)

        item.action_create_pob()
        self.assertEqual(
            self.env["performance_obligation"].search_count(
                [
                    (
                        "source_analytic_account_id",
                        "=",
                        self.contract.analytic_account_id.id,
                    ),
                    ("product_id", "=", self.product.id),
                    ("price_unit", "=", 15000000),
                ]
            ),
            1,
            "calling action_create_pob again must not create a duplicate PoB",
        )

    def test_pob_price_unit_matches_item_when_quantity_not_one(self):
        """OFS/26/000026: a single contract item line with quantity != 1
        must produce a PoB whose price_unit still matches the item's own
        price_unit -- not amount_untaxed (price_unit * quantity), which is
        what _prepare_pob_data used to (wrongly) assign to price_unit."""
        self._create_payment_term("Term 1", 5000000, quantity=3)

        item = self._get_fix_items()
        self.assertEqual(len(item), 1)
        self.assertEqual(item.price_unit, 5000000)
        self.assertEqual(item.amount_untaxed, 15000000)

        item.action_create_pob()

        item = self._get_fix_items()
        self.assertEqual(item.pob_id.price_unit, 5000000)
        self.assertEqual(item.pob_id.uom_quantity, 3)
        self.assertEqual(item.pob_id.price_subtotal, 15000000)

        item.action_create_pob()
        self.assertEqual(
            self.env["performance_obligation"].search_count(
                [
                    (
                        "source_analytic_account_id",
                        "=",
                        self.contract.analytic_account_id.id,
                    ),
                    ("product_id", "=", self.product.id),
                    ("price_unit", "=", 5000000),
                ]
            ),
            1,
            "calling action_create_pob again must not create a duplicate PoB",
        )
