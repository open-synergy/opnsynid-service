# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = "service.contract"

    operating_unit_id = fields.Many2one(
        string="Default Operating Unit",
        comodel_name="operating.unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self._uid
        ),
    )

    @api.multi
    def _prepare_analytic_account(self):
        _super = super(ServiceContract, self)
        result = _super._prepare_analytic_account()
        ou = self.operating_unit_id
        if ou:
            result.update({"operating_unit_ids": [(6, 0, [ou.id])]})
        return result
