# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceOperatingUnit(YamlTransactionCase):
    """Scenario tests for ``service.contract`` with Operating Unit."""

    def test_service_operating_unit(self):
        """Run the create-and-verify scenario for Operating Unit."""
        self.run_yaml_scenario("test_data_service_operating_unit.yaml")
