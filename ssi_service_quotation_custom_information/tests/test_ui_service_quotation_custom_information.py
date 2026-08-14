# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so the Pre-Condition fixture below would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceQuotationCustomInformation(HttpSavepointCase):
    """Tour test for the ``service.quotation`` custom info delta IK."""

    @classmethod
    def setUpClass(cls):
        """Set the admin user so the tour session has access.

        No extra record is created: the delta tour only opens the
        create form and asserts the additional tab, it never saves.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

    def test_create(self):
        """Run the create delta tour for ``service.quotation``.

        IK: docs/service_quotation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_service_quotation_custom_information_service_quotation_create",
            login="admin",
        )
