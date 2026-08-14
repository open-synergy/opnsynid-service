# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSvcQuotCustomInfo(YamlTransactionCase):
    """Cover custom info on ``service.quotation`` end to end.

    Exercises creating a quotation, confirming and approving it, and
    verifying the custom info flow via the YAML scenario below.
    """

    def test_service_quotation_custom_information(self):
        """Run the create/confirm/approve custom info scenario."""
        self.run_yaml_scenario("test_data_service_quotation_custom_information.yaml")
