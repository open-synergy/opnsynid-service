# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceContractFixItemPobOperatingUnit(YamlTransactionCase):
    """Covers ``service.contract_fix_item._prepare_pob_data`` OU stamp.

    Verifies that a Performance Obligation created from a contract's
    fix item (``action_create_pob``) is stamped with the source
    contract's own Operating Unit, instead of falling back to the
    acting user's default Operating Unit.
    """

    def test_service_contract_fix_item_pob_operating_unit(self):
        """Run the PoB operating unit propagation scenario."""
        self.run_yaml_scenario(
            "test_data_service_contract_fix_item_pob_operating_unit.yaml"
        )
