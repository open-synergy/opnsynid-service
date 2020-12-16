# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceContractTypeOperatingUnit(models.Model):
    _name = "service.contract_type_operating_unit"
    _inherit = "service.contract_type_operating_unit"

    quotation_sequence_id = fields.Many2one(
        string="Quotation Sequence",
        comodel_name="ir.sequence",
        company_dependent=False,
    )
