# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so the Pre-Condition fixture below would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceContract(HttpSavepointCase):
    """Tour tests for the ``service.contract`` revenue recognition delta."""

    @classmethod
    def setUpClass(cls):
        """Create an open contract with one fix item, for the edit tour.

        The create tour (E1 delta-only) needs no fixture at all -- it
        opens a blank create form. The edit tour needs an existing
        contract that already reached ``open`` (so it has its own
        Analytic Account, matching how ``action_create_pob`` is meant
        to be used -- see ``docs/service_contract/02-edit.md``) and at
        least one fix item row (from a payment term detail line) for
        the Create PoB gear button to act on.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        income_account = cls.env["account.account"].search(
            [("user_type_id.internal_group", "=", "income")], limit=1
        )
        uom = cls.env.ref("uom.product_uom_unit")
        pricelist = cls.env.ref("product.list0")
        partner = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR RR Partner",
                    "is_company": True,
                }
            )
        )
        service_type = (
            cls.env["service.type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR RR Service Type",
                    "code": "TOURRR",
                }
            )
        )
        product = (
            cls.env["product.product"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR RR Product",
                    "type": "service",
                    "uom_id": uom.id,
                    "uom_po_id": uom.id,
                }
            )
        )
        cls.contract = (
            cls.env["service.contract"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "TOUR SC RR Edit",
                    "partner_id": partner.id,
                    "type_id": service_type.id,
                    "manager_id": cls.admin.id,
                    "salesperson_id": cls.admin.id,
                    "pricelist_id": pricelist.id,
                    "currency_id": cls.env.ref("base.USD").id,
                    "date": "2026-01-01",
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                }
            )
        )
        cls.contract.with_user(cls.admin).action_confirm()
        cls.contract.with_user(cls.admin).with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        cls.contract.invalidate_cache()
        term = (
            cls.env["service.contract_fix_item_payment_term"]
            .with_user(cls.admin)
            .create(
                {
                    "service_id": cls.contract.id,
                    "name": "TOUR RR Term",
                    "sequence": 10,
                }
            )
        )
        cls.env["service.contract_fix_item_payment_term_detail"].with_user(
            cls.admin
        ).create(
            {
                "term_id": term.id,
                "product_id": product.id,
                "name": product.name,
                "account_id": income_account.id,
                "price_unit": 500,
                "quantity": 1,
                "uom_quantity": 1,
                "uom_id": uom.id,
                "sequence": 10,
            }
        )

    def test_create(self):
        """Run the create tour for ``service.contract``.

        IK: docs/service_contract/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_service_revenue_recognition_service_contract_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``service.contract``.

        IK: docs/service_contract/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_service_revenue_recognition_service_contract_edit",
            login="admin",
        )
