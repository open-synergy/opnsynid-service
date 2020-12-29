# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceQuotationFixItemPaymentTermDetail(models.Model):
    _name = "service.quotation_fix_item_payment_term_detail"
    _inherit = [
        "service.common_fix_item_payment_term_detail",
    ]
    _description = "Service Quotation Fix Item Payment Term Detail"

    payment_term_id = fields.Many2one(
        comodel_name="service.quotation_fix_item_payment_term",
    )
    tax_ids = fields.Many2many(
        relation="rel_service_quotation_fix_item_payment_term_detail_2_tax",
        column1="fix_item_id",
        column2="tax_id",
    )

    @api.multi
    def _prepare_contract_data(self):
        self.ensure_one()
        return {
            "name": self.name,
            "product_id": self.product_id.id,
            "price_unit": self.price_unit,
            "quantity": self.quantity,
            "uom_id": self.uom_id.id,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
        }
