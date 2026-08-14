# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceProject(YamlTransactionCase):
    """Cover the ``service.contract`` auto project creation feature."""

    def test_service_project(self):
        """Run the auto create project scenario."""
        self.run_yaml_scenario("test_data_service_project.yaml")
