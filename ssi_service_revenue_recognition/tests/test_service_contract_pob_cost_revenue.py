# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceContractPobCostRevenue(YamlTransactionCase):
    """Covers ``service.contract.action_open_pob_cost_revenue``.

    OFS/26/000024: revenue recognition journals for a contract's PoBs
    post to each PoB's own, separately auto-created analytic account
    -- never to the contract's own account -- so the contract needs a
    way to see that recap without the user opening its analytic
    account directly. ``pob_cost_revenue_count`` and
    ``action_open_pob_cost_revenue`` delegate to the contract's own
    analytic account (``ssi_revenue_recognition``), which owns the
    aggregation logic since a contract is only one of several document
    types that can be a PoB's source.
    """

    def setUp(self):
        """Create and open a contract, giving it an analytic account."""
        super().setUp()
        env = self.env
        admin = env.ref("base.user_admin")
        self.admin = admin

        self.partner = (
            env["res.partner"]
            .with_user(admin)
            .create({"name": "Test Partner - PoB Cost Revenue", "is_company": True})
        )
        self.pricelist = env.ref("product.list0")
        self.service_type = (
            env["service.type"]
            .with_user(admin)
            .create({"name": "Test Service Type - PoB CR", "code": "POBCR"})
        )
        self.contract = (
            env["service.contract"]
            .with_user(admin)
            .create(
                {
                    "title": "Test Service Contract - PoB Cost Revenue",
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

    def test_pob_cost_revenue_delegates_to_analytic_account(self):
        """Contract's count/action mirror its own analytic account's.

        Pure Python -- trigger P1 (L-01: ``action: call`` in YAML
        discards a method's return value, so the dict returned by
        ``action_open_pob_cost_revenue`` cannot be asserted from YAML
        at all).
        """
        pob_aa = self.env["account.analytic.account"].create(
            {"name": "Test PoB AA - contract delegation"}
        )
        self.env["performance_obligation"].create(
            {
                "title": "Test PoB - contract delegation",
                "source_analytic_account_id": self.contract.analytic_account_id.id,
                "analytic_account_id": pob_aa.id,
            }
        )
        self.env["account.analytic.line"].create(
            {"name": "Test line", "account_id": pob_aa.id, "amount": 1000.0}
        )
        self.contract.invalidate_cache()

        self.assertEqual(self.contract.pob_cost_revenue_count, 1)

        action = self.contract.action_open_pob_cost_revenue()
        self.assertEqual(action["res_model"], "account.analytic.line")
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["domain"], [("account_id", "in", [pob_aa.id])])
