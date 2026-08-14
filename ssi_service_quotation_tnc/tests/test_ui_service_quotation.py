# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so the Pre-Condition fixture below would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceQuotation(HttpSavepointCase):
    """Tour tests for the ``service.quotation`` T&C delta."""

    def test_field_tnc(self):
        """Run the delta tour for the ``service.quotation`` create form.

        IK: docs/service_quotation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_service_quotation_tnc_service_quotation_field_tnc",
            login="admin",
        )
