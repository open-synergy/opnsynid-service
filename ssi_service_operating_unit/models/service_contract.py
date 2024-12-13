# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.single_operating_unit",
    ]
