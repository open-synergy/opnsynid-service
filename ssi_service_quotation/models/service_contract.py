# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = [
        "service.contract",
    ]

    quotation_id = fields.Many2one(
        string="# Quotation",
        comodel_name="service.quotation",
        readonly=True,
        ondelete="restrict",
    )
