# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ServiceContractFixItemPaymentTerm(models.Model):
    _name = "service.contract_fix_item_payment_term"
    _inherit = ["service.fix_item_payment_term_mixin"]
    _description = "Service Contract Fix Item Payment Term"

    @api.depends(
        "invoice_id",
        "service_id.state",
    )
    def _compute_state(self):
        for record in self:
            if record.service_id.state in ["draft", "confirm", "approve"]:
                state = "draft"
            elif record.service_id.state in ["open", "done", "terminate"]:
                if record.invoice_id:
                    state = "invoiced"
                else:
                    state = "uninvoiced"
            else:
                state = "cancelled"
            record.state = state

    service_id = fields.Many2one(
        string="Service Contract",
        comodel_name="service.contract",
        ondelete="cascade",
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.move",
        readonly=True,
        ondelete="restrict",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("invoiced", "Invoiced"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_state",
        store=True,
    )
    detail_ids = fields.One2many(
        comodel_name="service.contract_fix_item_payment_term_detail",
    )

    def action_create_invoice(self):
        for record in self:
            record._create_invoice()

    def action_delete_invoice(self):
        for record in self:
            record._delete_invoice()

    def action_disconnect_invoice(self):
        for record in self:
            record._disconnect_invoice()

    def _create_invoice(self):
        self.ensure_one()
        invoice = self.env["account.move"].create(self._prepare_invoice_data())
        self.write(
            {
                "invoice_id": invoice.id,
            }
        )

    def _disconnect_invoice(self):
        self.ensure_one()
        self.write(
            {
                "invoice_id": False,
            }
        )

    def _get_fix_item_receivable_journal(self):
        self.ensure_one()
        contract = self.service_id
        return contract.fix_item_receivable_journal_id

    def _get_fix_item_receivable_account(self):
        self.ensure_one()
        contract = self.service_id
        return contract.fix_item_receivable_account_id

    def _prepare_invoice_data(self):
        self.ensure_one()
        contract = self.service_id
        partner = contract.contact_partner_id or contract.partner_id
        journal = self._get_fix_item_receivable_journal()
        self._get_fix_item_receivable_account()
        lines = []
        for detail in self.detail_ids:
            lines += detail._prepare_invoice_line()
        return {
            "date": fields.Date.today(),
            "ref": contract.name,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "partner_id": partner.id,
            "currency_id": contract.currency_id.id,
            "partner_bank_id": False,  # TODO
            "invoice_user_id": False,
            "invoice_date": fields.Date.today(),
            "invoice_date_due": fields.Date.today(),  # TODO
            "invoice_origin": contract.name,
            "invoice_payment_term_id": False,  # TODO
            "invoice_line_ids": lines,
            "payment_reference": contract.title,
        }

    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        self.detail_ids.write({"invoice_line_id": False})
        self.write(
            {
                "invoice_id": False,
            }
        )
        invoice.unlink()
