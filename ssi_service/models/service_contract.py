# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = [
        "service.mixin",
        "mixin.transaction_terminate",
    ]
    _description = "Service Contract"

    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_confirm",
        "action_open",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_terminate",
        "dom_cancel",
    ]

    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    analytic_group_id = fields.Many2one(
        string="Analytic Group",
        comodel_name="account.analytic.group",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    fix_item_payment_term_ids = fields.One2many(
        comodel_name="service.contract_fix_item_payment_term",
    )

    # Invocing related fields
    fix_item_receivable_journal_id = fields.Many2one(
        string="Fix Item Receivable Journal",
        comodel_name="account.journal",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    fix_item_receivable_account_id = fields.Many2one(
        string="Fix Item Receivable Account",
        comodel_name="account.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.model
    def _get_policy_field(self):
        res = super(ServiceContract, self)._get_policy_field()
        policy_field = [
            "open_ok",
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def action_open(self):
        _super = super(ServiceContract, self)
        _super.action_open()
        for record in self.sudo():
            record._create_analytic_account()

    def _create_analytic_account(self):
        self.ensure_one()
        if self.analytic_account_id:
            self._update_analytic_account()
        else:
            AA = self.env["account.analytic.account"]
            aa = AA.create(self._prepare_analytic_account())
            self.write(
                {
                    "analytic_account_id": aa.id,
                }
            )

    def _update_analytic_account(self):
        self.ensure_one()
        self.analytic_account_id.write(self._prepare_update_analytic_account())

    def _prepare_update_analytic_account(self):
        self.ensure_one()
        group_id = self.analytic_group_id and self.analytic_group_id.id or False
        return {
            "name": self.title,
            "code": self.name,
            "partner_id": self.partner_id.id,
            "group_id": group_id,
        }

    def _prepare_analytic_account(self):
        self.ensure_one()
        group_id = self.analytic_group_id and self.analytic_group_id.id or False
        return {
            "name": self.title,
            "code": self.name,
            "partner_id": self.partner_id.id,
            "group_id": group_id,
        }