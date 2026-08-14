# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so the Pre-Condition fixture below would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceQuotation(HttpSavepointCase):
    """Tour tests for the ``service.quotation`` operating unit delta."""

    @classmethod
    def setUpClass(cls):
        """Grant admin the group needed to see the Operating Unit field.

        The multi operating unit group is required for the Operating
        Unit field itself to be rendered on the create form.
        """
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )

    def test_field_ou(self):
        """Run the delta tour for the ``service.quotation`` create form.

        IK: docs/service_quotation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_service_quotation_operating_unit_service_quotation_field_ou",
            login="admin",
        )
