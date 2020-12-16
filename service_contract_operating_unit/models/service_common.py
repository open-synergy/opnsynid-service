# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceCommon(models.AbstractModel):
    _name = "service.common"
    _inherit = "service.common"

    operating_unit_id = fields.Many2one(
        string="Default Operating Unit",
        comodel_name="operating.unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self._uid
        ),
    )
