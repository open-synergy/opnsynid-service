# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSvcQuotStateChangeConstrain(YamlTransactionCase):
    """Test the status check / state change constrain integration.

    Covers ``service.quotation`` with ``mixin.state_change_constrain``
    and ``mixin.status_check`` installed: create, confirm, and approve
    still work when no state change constraint template is configured.
    """

    def test_service_quotation_state_change_constrain(self):
        """Run the create-confirm-approve scenario YAML."""
        self.run_yaml_scenario(
            "test_data_service_quotation_state_change_constrain.yaml"
        )
