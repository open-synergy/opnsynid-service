# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceContract(YamlTransactionCase):
    """Cover ``service.type`` and ``service.contract`` YAML scenarios."""

    def test_service_contract(self):
        """Run the service contract create/confirm/approve/done scenario."""
        self.run_yaml_scenario("test_data_service_contract.yaml")
