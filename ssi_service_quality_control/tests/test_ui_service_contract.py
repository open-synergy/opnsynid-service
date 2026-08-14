# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so a Pre-Condition fixture would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceContract(HttpSavepointCase):
    """Tour tests for the ``service.contract`` QC worksheet delta."""

    def test_field_qc_worksheet(self):
        """Run the delta tour for the ``service.contract`` create form.

        IK: docs/service_contract/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_service_quality_control_service_contract_field_qc_worksheet",
            login="admin",
        )
