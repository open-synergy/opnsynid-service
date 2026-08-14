# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceContractFixItemPob(YamlTransactionCase):
    """Covers the ``auto_create_project`` default on PoB creation.

    ``service.contract_fix_item._prepare_pob_data`` (this module) adds
    ``auto_create_project`` to the Performance Obligation values, sourced
    from ``service_id.type_id.pob_auto_create_project``. Both branches of
    that boolean default are covered here (``True`` and the ``False``
    default); this module does not add any ``@api.constrains``, so there
    is no negative ``expect_error`` path to cover.
    """

    def test_service_contract_fix_item_pob(self):
        """Run the ``auto_create_project`` default scenarios."""
        self.run_yaml_scenario("test_data_service_contract_fix_item_pob.yaml")
