# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceContractWorkLog(YamlTransactionCase):
    """Cover the work log integration added to ``service.contract``.

    Exercises the contract lifecycle (draft -> confirm -> open) that
    ``ssi_service_contract_work_log`` relies on to expose the Work Log
    tab, without asserting on ``hr.work_log`` records themselves.
    """

    def test_service_contract_work_log(self):
        """Run the create-confirm-approve scenario for the contract."""
        self.run_yaml_scenario("test_data_service_contract_work_log.yaml")
