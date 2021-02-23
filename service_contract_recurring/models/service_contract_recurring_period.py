# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceContractRecurringPeriod(models.Model):
    _name = "service.contract_recurring_period"
    _description = "Service Contract Recurring Period"
    _order = "contract_id, date_start, id"

    @api.depends(
        "invoice_id",
    )
    @api.multi
    def _compute_invoice_state(self):
        for document in self:
            document.invoice_state = "tobeinvoiced"
            if document.invoice_id:
                document.invoice_state = "invoiced"

    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="contract_id.partner_id",
        store=True,
        readonly=True,
    )
    responsible_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        related="contract_id.responsible_id",
        store=True,
        readonly=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="service.contract_type",
        related="contract_id.type_id",
        store=True,
        readonly=True,
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        ondelete="restrict",
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.invoice",
        readonly=True,
        ondelete="restrict",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Unstarted"),
            ("open", "In Progress"),
            ("done", "Done"),
        ],
        required=True,
        readonly=False,
        default="draft",
    )
    invoice_state = fields.Selection(
        string="Invoice State",
        selection=[
            ("tobeinvoiced", "To Be Invoiced"),
            ("invoiced", "Invoiced"),
        ],
        compute="_compute_invoice_state",
        store=True,
        required=False,
        readonly=False,
    )
    contract_state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Ready to Start"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("terminate", "Terminated"),
            ("cancel", "Cancelled"),
        ],
        related="contract_id.state",
        store=True,
        readonly=True,
    )

    @api.multi
    def action_start(self):
        for document in self:
            document.write(document._prepare_start_data())

    @api.multi
    def action_end(self):
        for document in self:
            document.write(document._prepare_end_data())
            document.analytic_account_id.set_close()

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())
            document.analytic_account_id.set_open()

    @api.multi
    def _prepare_start_data(self):
        self.ensure_one()
        return {
            "state": "open",
        }

    @api.multi
    def _prepare_end_data(self):
        self.ensure_one()
        return {
            "state": "done",
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.multi
    def action_create_invoice(self):
        for record in self:
            record._create_invoice()

    @api.multi
    def action_delete_invoice(self):
        for record in self:
            record._delete_invoice()

    @api.multi
    def _create_invoice(self):
        self.ensure_one()
        invoice = self.env["account.invoice"].create(self._prepare_invoice_data())
        self.write(
            {
                "invoice_id": invoice.id,
            }
        )
        for detail in self.contract_id.recurring_item_ids:
            detail._create_invoice_line(invoice, self)
        invoice.button_reset_taxes()

    @api.multi
    def _get_receivable_journal(self):
        self.ensure_one()
        contract = self.contract_id
        return contract.recurring_item_receivable_journal_id

    @api.multi
    def _get_receivable_account(self):
        self.ensure_one()
        contract = self.contract_id
        return contract.recurring_item_receivable_account_id

    @api.multi
    def _prepare_invoice_data(self):
        self.ensure_one()
        contract = self.contract_id
        journal = self._get_receivable_journal()
        account = self._get_receivable_account()
        return {
            "partner_id": contract.partner_id.id,
            "date_invoice": False,
            "journal_id": journal.id,
            "account_id": account.id,
            "currency_id": contract.currency_id.id,
            "origin": contract.name,
            "name": contract.title,
        }

    @api.multi
    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        self.write(
            {
                "invoice_id": False,
            }
        )
        invoice.unlink()

    @api.multi
    def _update_analytic_account(self):
        self.ensure_one()
        if self.analytic_account_id:
            self.analytic_account_id.write(self._prepare_analytic_account())
        else:
            self._create_analytic_account()

    @api.multi
    def _create_analytic_account(self):
        self.ensure_one()
        obj_aa = self.env["account.analytic.account"]
        aa = obj_aa.create(self._prepare_analytic_account())
        self.write(
            {
                "analytic_account_id": aa.id,
            }
        )

    @api.multi
    def _prepare_analytic_account(self):
        self.ensure_one()
        contract = self.contract_id
        parent = contract.analytic_account_id
        name = "{} {} - {}".format(contract.name, self.date_start, self.date_end)
        return {
            "name": name,
            "type": "normal",
            "parent_id": parent and parent.id or False,
            "partner_id": contract.partner_id.id,
            "date_start": self.date_start,
            "date": self.date_end,
        }
