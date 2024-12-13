# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _inherit = [
        "service.quotation",
        "mixin.single_operating_unit",
    ]
