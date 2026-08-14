# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSvcQuotProject(YamlTransactionCase):
    """Cover the ``service.quotation`` create/confirm/approve flow.

    Exercises the base workflow provided by ``ssi_service_quotation``
    with this module installed, to guard against regressions in the
    ``_compute_contract_onchange`` override it adds.
    """

    def test_service_quotation_project(self):
        """Run the create/confirm/approve YAML scenario."""
        self.run_yaml_scenario("test_data_service_quotation_project.yaml")
