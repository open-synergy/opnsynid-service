# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceQualityControl(YamlTransactionCase):
    """Cover the ``service.contract`` quality control worksheet mixin.

    Exercises the confirm/approve flow of ``service.contract`` after
    installing ``ssi_service_quality_control``, so the mixin's fields
    stay usable through the base workflow.
    """

    def test_service_quality_control(self):
        """Run the create-confirm-approve scenario for the contract."""
        self.run_yaml_scenario("test_data_service_quality_control.yaml")
