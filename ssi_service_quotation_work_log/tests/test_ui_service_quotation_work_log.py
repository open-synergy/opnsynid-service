# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass; kept for consistency even though this tour needs
# no Pre-Condition fixture beyond the admin login already provided by
# start_tour().
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceQuotationWorkLog(HttpSavepointCase):
    """Tour test for the work log delta on ``service.quotation``."""

    def test_create(self):
        """Run the create tour asserting the Work Log tab is shown.

        IK: docs/service_quotation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_service_quotation_work_log_service_quotation_create",
            login="admin",
        )
