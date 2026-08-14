# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceContractTnc(YamlTransactionCase):
    """YAML scenario test for the ``service.contract`` T&C mixin."""

    def test_service_contract_tnc(self):
        """Run the create/confirm/approve T&C scenario."""
        self.run_yaml_scenario("test_data_service_contract_tnc.yaml")
