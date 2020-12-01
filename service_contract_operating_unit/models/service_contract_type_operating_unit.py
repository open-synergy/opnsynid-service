# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceContractTypeOperatingUnit(models.Model):
    _name = "service.contract_type_operating_unit"
    _description = "Service Contract Type - OU Setting"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="service.contract_type",
        require=True,
        ondelete="cascade",
    )
    operating_unit_id = fields.Many2one(
        string="Operating Unit",
        comodel_name="operating.unit",
    )
    contract_sequence_id = fields.Many2one(
        string="Contract Sequence",
        comodel_name="ir.sequence",
        company_dependent=False,
    )
    fix_item_receivable_journal_id = fields.Many2one(
        string="Fix Item Receivable Journal",
        comodel_name="account.journal",
        company_dependent=False,
    )
    fix_item_receivable_account_id = fields.Many2one(
        string="Fix Item Receivable Account",
        comodel_name="account.account",
        company_dependent=False,
    )
    parent_analytic_account_id = fields.Many2one(
        string="Parent Analytic Account",
        comodel_name="account.analytic.account",
    )
