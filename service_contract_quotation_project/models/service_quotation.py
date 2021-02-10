# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class ServiceContract(models.Model):
    _name = "service.quotation"
    _inherit = "service.quotation"

    @api.multi
    def _compute_contract_onchange(self, temp_record):
        _super = super(ServiceContract, self)
        result = _super._compute_contract_onchange(temp_record)
        temp_record.onchange_auto_create_project_ok()
        return result
