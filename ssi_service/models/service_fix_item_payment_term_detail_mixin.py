# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ServiceFixItemPaymentTermDetailMixin(models.AbstractModel):
    _name = "service.fix_item_payment_term_detail_mixin"
    _description = "Service Fix Item Payment Term Detail Mixin"
    _order = "sequence, id"
    _inherit = [
        "mixin.product_line_account",
    ]

    term_id = fields.Many2one(
        string="Service Payment Term",
        comodel_name="service.fix_item_payment_term_mixin",
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        required=True,
    )
