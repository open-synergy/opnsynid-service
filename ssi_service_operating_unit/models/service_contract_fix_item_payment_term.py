# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ServiceContractFixItemPaymentTerm(models.Model):
    _name = "service.contract_fix_item_payment_term"
    _inherit = ["service.contract_fix_item_payment_term"]

    def _prepare_invoice_data(self):
        _super = super(ServiceContractFixItemPaymentTerm, self)

        result = _super._prepare_invoice_data()
        result.update(
            {
                "operating_unit_id": self.service_id.operating_unit_id.id,
            }
        )
        return result
