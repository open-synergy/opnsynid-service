# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceRiskAnalysis(YamlTransactionCase):
    """YAML scenario test for the ``service.contract`` risk analysis link."""

    def test_service_risk_analysis(self):
        """Run the create/confirm/approve risk analysis scenario."""
        self.run_yaml_scenario("test_data_service_risk_analysis.yaml")
