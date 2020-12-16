# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class ServiceContract(models.Model):
    _name = "service.quotation"
    _inherit = "service.quotation"

    @api.multi
    def _prepare_contract_data(self):
        _super = super(ServiceContract, self)
        result = _super._prepare_contract_data()
        ou = self.operating_unit_id
        result.update({"operating_unit_id": ou and ou.id or False})
        return result
