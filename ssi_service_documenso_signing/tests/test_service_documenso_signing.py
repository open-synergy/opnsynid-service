# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceDocumensoSigning(YamlTransactionCase):
    """Cover the Documenso signing approval flow on ``service.contract``."""

    def test_service_documenso_signing(self):
        """Run the Documenso signing approval scenario."""
        self.run_yaml_scenario("test_data_service_documenso_signing.yaml")
