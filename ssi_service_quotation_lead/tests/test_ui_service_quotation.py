# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so Pre-Condition fixtures below would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceQuotationLead(HttpSavepointCase):
    """Tour test for the ``lead_id`` delta on ``service.quotation``."""

    @classmethod
    def setUpClass(cls):
        """Set up nothing extra: the delta tour only opens a new form.

        No partner/type/quotation fixture is required because the
        delta tour under test stops at asserting the ``# Lead`` field
        is present on the create form — it does not fill in or save
        the record (that flow belongs to the base module's own
        01-create tour).
        """
        super().setUpClass()

    def test_create(self):
        """Run the delta create tour asserting the ``# Lead`` field.

        IK: docs/service_quotation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_service_quotation_lead_service_quotation_create",
            login="admin",
        )
