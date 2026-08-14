# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass (see odoo-development-ui-test skill,
# structure-and-runner.md, §Base class).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceQuotationStateChangeConstrain(HttpSavepointCase):
    """Tour test for the create-time Status Checks tab."""

    def test_create(self):
        """Run the create tour for ``service.quotation``.

        IK: docs/service_quotation/01-create.md (E1 delta -- Additional
        Fields)
        """
        self.start_tour(
            "/web",
            "ssi_service_quotation_state_change_constrain_service_quotation_create",
            login="admin",
        )
