# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ServiceContractFixItemPaymentTerm(models.Model):
    """One payment term line of a service contract.

    Child of ``service.contract`` (``fix_item_payment_term_ids``). Each
    line can be linked to a customer invoice, either automatically via
    :meth:`_create_invoice` or manually via :meth:`action_mark_as_manual`;
    :attr:`state` reflects that invoicing status.
    """

    _name = "service.contract_fix_item_payment_term"
    _inherit = ["service.fix_item_payment_term_mixin"]
    _description = "Service Contract Fix Item Payment Term"

    @api.depends(
        "invoice_id",
        "service_id.state",
        "manually_control",
    )
    def _compute_state(self):
        """Derive the invoicing state from the contract and invoice link.

        :return: None, sets ``state`` on each record.
        """
        for record in self:
            if record.service_id.state in ["draft", "confirm", "approve"]:
                state = "draft"
            elif record.service_id.state in ["open", "done", "terminate"]:
                if record.invoice_id:
                    state = "invoiced"
                elif record.manually_control:
                    state = "manual"
                elif not record.invoice_id and not record.manually_control:
                    state = "uninvoiced"
            else:
                state = "cancelled"
            record.state = state

    service_id = fields.Many2one(
        string="Service Contract",
        comodel_name="service.contract",
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        string="Partner",
        related="service_id.partner_id",
        store=True,
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.move",
        readonly=True,
        ondelete="restrict",
    )
    date_invoice = fields.Date(
        string="Date Invoice Estimation",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("invoiced", "Invoiced"),
            ("manual", "Manually Controlled"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_state",
        store=True,
    )
    manually_control = fields.Boolean(
        string="Manually Controlled",
        default=False,
    )
    detail_ids = fields.One2many(
        comodel_name="service.contract_fix_item_payment_term_detail",
    )

    def action_create_invoice(self):
        """Create and link a customer invoice for each selected line.

        :return: None.
        """
        for record in self.sudo():
            record._create_invoice()

    def action_delete_invoice(self):
        """Unlink and delete the invoice tied to each selected line.

        :return: None.
        """
        for record in self.sudo():
            record._delete_invoice()

    def action_disconnect_invoice(self):
        """Detach the invoice from each selected line without deleting it.

        :return: None.
        """
        for record in self.sudo():
            record._disconnect_invoice()

    def action_mark_as_manual(self):
        """Flag each selected line as manually invoiced.

        :return: None.
        """
        for record in self.sudo():
            record._mark_as_manual()

    def action_unmark_as_manual(self):
        """Clear the manual-invoicing flag on each selected line.

        :return: None.
        """
        for record in self.sudo():
            record._unmark_as_manual()

    def _mark_as_manual(self):
        """Set ``manually_control`` to ``True`` on this line."""
        self.ensure_one()
        self.write(
            {
                "manually_control": True,
            }
        )

    def _unmark_as_manual(self):
        """Set ``manually_control`` to ``False`` on this line."""
        self.ensure_one()
        self.write(
            {
                "manually_control": False,
            }
        )

    def _create_invoice(self):
        """Create a customer invoice from :meth:`_prepare_invoice_data`.

        :return: None, links the new ``account.move`` to ``invoice_id``.
        """
        self.ensure_one()
        invoice = self.env["account.move"].create(self._prepare_invoice_data())
        self.write(
            {
                "invoice_id": invoice.id,
            }
        )

    def _disconnect_invoice(self):
        """Clear ``invoice_id`` without deleting the linked invoice."""
        self.ensure_one()
        self.write(
            {
                "invoice_id": False,
            }
        )

    def _get_fix_item_receivable_journal(self):
        """Return the journal used for this line's invoice.

        :return: ``account.journal`` recordset, an extension point that
            modules integrating other journal sources may override.
        """
        self.ensure_one()
        contract = self.service_id
        return contract.fix_item_receivable_journal_id

    def _get_fix_item_receivable_account(self):
        """Return the receivable account used for this line's invoice.

        :return: ``account.account`` recordset, an extension point that
            modules integrating other account sources may override.
        """
        self.ensure_one()
        contract = self.service_id
        return contract.fix_item_receivable_account_id

    def _prepare_invoice_data(self):
        """Build the ``create`` values for this line's invoice.

        :return: dict of values matching ``account.move`` fields.
        """
        self.ensure_one()
        contract = self.service_id
        if contract.contractor_id:
            partner = contract.contact_contractor_id or contract.contractor_id
        else:
            partner = contract.contact_partner_id or contract.partner_id
        journal = self._get_fix_item_receivable_journal()
        self._get_fix_item_receivable_account()
        lines = []
        for detail in self.detail_ids:
            lines += [(0, 0, detail._prepare_invoice_line())]
        return {
            "date": fields.Date.today(),
            "ref": contract.name,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "partner_id": partner.id,
            "currency_id": contract.currency_id.id,
            "invoice_user_id": False,
            "invoice_date": fields.Date.today(),
            "invoice_date_due": fields.Date.today(),  # TODO
            "invoice_origin": contract.name,
            "invoice_payment_term_id": False,  # TODO
            "invoice_line_ids": lines,
            "payment_reference": contract.title,
            "partner_bank_id": (
                contract.partner_bank_id and contract.partner_bank_id.id
            ),
        }

    def _delete_invoice(self):
        """Detach and delete the invoice linked to this line.

        :return: None.
        """
        self.ensure_one()
        invoice = self.invoice_id
        self.detail_ids.write({"invoice_line_id": False})
        self.write(
            {
                "invoice_id": False,
            }
        )
        invoice.unlink()
