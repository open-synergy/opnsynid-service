# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceQuotationFixItemPaymentTerm(models.Model):
    _name = "service.quotation_fix_item_payment_term"
    _inherit = [
        "service.common_fix_item_payment_term",
    ]
    _description = "Service Quotation Fix Item Payment Term"

    @api.depends(
        "detail_ids",
        "detail_ids.price_unit",
        "detail_ids.quantity",
        "detail_ids.uom_id",
        "detail_ids.tax_ids",
    )
    @api.multi
    def _compute_total(self):
        _super = super(ServiceQuotationFixItemPaymentTerm, self)
        _super._compute_total()

    contract_id = fields.Many2one(
        comodel_name="service.quotation",
    )
    fix_item_allowed_product_ids = fields.Many2many(
        related="contract_id.fix_item_allowed_product_ids",
        store=False,
    )
    fix_item_allowed_product_categ_ids = fields.Many2many(
        related="contract_id.fix_item_allowed_product_categ_ids",
        store=False,
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="service.quotation_fix_item_payment_term_detail",
        inverse_name="payment_term_id",
    )
    amount_untaxed = fields.Float(
        string="Untaxed",
        required=False,
        compute="_compute_total",
        store=True,
    )
    amount_tax = fields.Float(
        string="Tax",
        required=False,
        compute="_compute_total",
        store=True,
    )
    amount_total = fields.Float(
        string="Total",
        required=False,
        compute="_compute_total",
        store=True,
    )

    @api.multi
    def _prepare_contract_data(self):
        self.ensure_one()
        detail_ids = []
        for detail in self.detail_ids:
            data = detail._prepare_contract_data()
            detail_ids.append((0, 0, data))
        return {
            "name": self.name,
            "sequence": self.sequence,
            "detail_ids": detail_ids,
        }
