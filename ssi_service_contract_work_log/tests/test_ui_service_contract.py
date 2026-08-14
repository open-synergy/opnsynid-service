# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so Pre-Condition fixtures below would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceContract(HttpSavepointCase):
    """Tour test for the work log delta on ``service.contract``."""

    @classmethod
    def setUpClass(cls):
        """Set up the class; no extra fixtures are needed.

        The tour only opens a blank create form and checks that the
        Work Log tab this module adds is visible — it never saves the
        record, so no partner/type/contract fixtures are required.
        """
        super().setUpClass()

    def test_create(self):
        """Run the create tour asserting the Work Log tab appears.

        IK: docs/service_contract/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_service_contract_work_log_service_contract_create",
            login="admin",
        )
