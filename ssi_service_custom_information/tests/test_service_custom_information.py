# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceCustomInformation(YamlTransactionCase):
    """
    Test custom information support added to ``service.contract``.
    Covers creating a contract and confirming/approving it while the
    custom info template/value fields are present.
    """

    def test_service_custom_information(self):
        """Run the create-confirm-approve custom info scenario."""
        self.run_yaml_scenario("test_data_service_custom_information.yaml")
