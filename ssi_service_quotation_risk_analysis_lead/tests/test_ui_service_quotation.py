# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so a Pre-Condition fixture would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceQuotation(HttpSavepointCase):
    """Tour test for the lead-driven risk analysis carryover delta."""

    def test_create(self):
        """Run the delta create tour asserting both delta fields.

        IK: docs/service_quotation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_service_quotation_risk_analysis_lead_service_quotation_create",
            login="admin",
        )
