# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ServiceContract(models.Model):
    """Adds the originating quotation link to ``service.contract``.

    Extension point only: the field is set once by
    ``service.quotation._create_contract()`` when a quotation is marked
    as won, and never written elsewhere.
    """

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
