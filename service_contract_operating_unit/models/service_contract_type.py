# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceContractType(models.Model):
    _name = "service.contract_type"
    _inherit = "service.contract_type"

    ou_setting_ids = fields.One2many(
        string="OU Setting",
        comodel_name="service.contract_type_operating_unit",
        inverse_name="type_id",
    )
