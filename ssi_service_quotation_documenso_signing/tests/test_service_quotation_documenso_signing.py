# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSvcQuotDocumensoSigning(YamlTransactionCase):
    """Test the Documenso signing mixin on ``service.quotation``."""

    def test_service_quotation_documenso_signing(self):
        """Run the normal-approval-fallback scenario."""
        self.run_yaml_scenario("test_data_service_quotation_documenso_signing.yaml")
