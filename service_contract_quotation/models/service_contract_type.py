# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceContractType(models.Model):
    _name = "service.contract_type"
    _inherit = "service.contract_type"

    quotation_sequence_id = fields.Many2one(
        string="Quotation Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    quotation_custom_info_template_id = fields.Many2one(
        string="Quotation Custom Info Template",
        comodel_name="custom.info.template",
    )
    service_quotation_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Service Quotation",
        comodel_name="res.groups",
        relation="rel_contract_type_confirm_service_quotation",
        column1="type_id",
        column2="group_id",
    )
    service_quotation_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval Service Quotation",
        comodel_name="res.groups",
        relation="rel_contract_type_restart_approval_service_quotation",
        column1="type_id",
        column2="group_id",
    )
    service_quotation_won_grp_ids = fields.Many2many(
        string="Allow To Mark as Won Service Quotation",
        comodel_name="res.groups",
        relation="rel_contract_type_won_service_quotation",
        column1="type_id",
        column2="group_id",
    )
    service_quotation_lost_grp_ids = fields.Many2many(
        string="Allow To Mark as Lost Service Quotation",
        comodel_name="res.groups",
        relation="rel_contract_type_lost_service_quotation",
        column1="type_id",
        column2="group_id",
    )
    service_quotation_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Service Quotation",
        comodel_name="res.groups",
        relation="rel_contract_type_cancel_service_quotation",
        column1="type_id",
        column2="group_id",
    )
    service_quotation_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Service Quotation",
        comodel_name="res.groups",
        relation="rel_contract_type_restart_service_quotation",
        column1="type_id",
        column2="group_id",
    )
