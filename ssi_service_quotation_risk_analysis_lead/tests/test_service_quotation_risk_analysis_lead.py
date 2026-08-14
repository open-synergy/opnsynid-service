# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSvcQuotRiskAnalysisLead(YamlTransactionCase):
    """YAML scenario test for the lead-driven risk analysis carryover."""

    def test_service_quotation_risk_analysis_lead(self):
        """Run the create-confirm-approve scenario."""
        self.run_yaml_scenario("test_data_service_quotation_risk_analysis_lead.yaml")
