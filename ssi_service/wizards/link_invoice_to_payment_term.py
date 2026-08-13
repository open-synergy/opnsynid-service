# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class LinkInvoiceToPaymentTerm(models.TransientModel):
    """Wizard to link an existing invoice to a contract payment term.

    Opened from the **Link Invoice** row button on
    ``service.contract_fix_item_payment_term`` (state ``uninvoiced``);
    lets the user pick an already-posted customer invoice instead of
    generating a new one via ``action_create_invoice``.
    """

    _name = "link_invoice_to_payment_term"
    _description = "Link Invoice To Service Contract Payment Term"

    @api.model
    def _default_contract_id(self):
        """Default ``term_id`` to the record the wizard was opened from.

        :return: int or False, the ``active_id`` from the context.
        """
        return self.env.context.get("active_id", False)

    term_id = fields.Many2one(
        string="Contract Term",
        comodel_name="service.contract_fix_item_payment_term",
        default=lambda self: self._default_contract_id(),
    )
    allowed_invoice_ids = fields.Many2many(
        string="Allowed Invoices",
        comodel_name="account.move",
        compute="_compute_allowed_invoice_ids",
        store=False,
        compute_sudo=True,
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.move",
    )

    @api.depends(
        "term_id",
    )
    def _compute_allowed_invoice_ids(self):
        """Restrict selectable invoices to posted ones of the partner.

        :return: None, sets ``allowed_invoice_ids`` on each record.
        """
        AM = self.env["account.move"]
        for record in self:
            criteria = [
                ("move_type", "=", "out_invoice"),
                ("partner_id", "=", record.term_id.service_id.partner_id.id),
                ("state", "=", "posted"),
            ]
            result = AM.search(criteria).ids
            record.allowed_invoice_ids = result

    def action_confirm(self):
        """Apply the chosen invoice to the payment term (button entry).

        :return: None.
        """
        for record in self.sudo():
            record._confirm()

    def _confirm(self):
        """Write the selected ``invoice_id`` onto ``term_id``."""
        self.ensure_one()
        self.term_id.write(
            {
                "invoice_id": self.invoice_id.id,
            }
        )
