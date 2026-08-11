# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ServiceContractFixItem(models.Model):
    _name = "service.contract_fix_item"
    _inherit = "service.contract_fix_item"

    pob_id = fields.Many2one(
        string="# PoB",
        comodel_name="performance_obligation",
        compute="_compute_pob_id",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "service_id.analytic_account_id",
        "product_id",
        "amount_untaxed",
    )
    def _compute_pob_id(self):
        """Find the PoB already created for this line, if any.

        ``service.contract_fix_item`` is a SQL view (see
        ``ssi_service.models.service_contract_fix_item``) that groups the
        underlying payment term detail rows by
        ``product_id, product_category_id, name, price_unit, uom_id`` --
        summing quantity/amounts across matching rows. Two lines that only
        match by ``product_id`` (the previous search criteria here) can
        still be *different* view rows when their ``price_unit`` differs,
        so matching on product alone wrongly linked both to the first
        line's PoB -- silently dropping the second line's amount from the
        contract's total Performance Obligation. Matching on
        ``amount_untaxed`` (the field ``_prepare_pob_data`` actually
        writes into the PoB's own ``price_unit`` -- see that method)
        keeps this search aligned with what a distinct view row's PoB
        actually looks like, so each distinct view row gets its own PoB
        while rows the view already merged (matching product/price)
        keep sharing one.
        """
        for record in self:
            result = False
            if record.service_id.analytic_account_id and record.product_id:
                PoB = self.env["performance_obligation"]
                criteria = [
                    (
                        "source_analytic_account_id",
                        "=",
                        record.service_id.analytic_account_id.id,
                    ),
                    ("product_id", "=", record.product_id.id),
                    ("price_unit", "=", record.amount_untaxed),
                ]
                pobs = PoB.search(criteria)
                if pobs:
                    result = pobs[0]
            record.pob_id = result

    def action_create_pob(self):
        for record in self.sudo():
            record._create_pob()

    def _create_pob(self):
        self.ensure_one()
        if self.pob_id:
            return True
        PoB = self.env["performance_obligation"]
        data = self._prepare_pob_data()
        PoB.create(data)
        # pob_id is compute+store=False with a search() inside (see
        # _compute_pob_id) rather than a real relational field path, so
        # Odoo's @api.depends graph has no way to know that creating this
        # new PoB should invalidate the pob_id already cached (as False)
        # for this record from the `if self.pob_id:` check above -- it
        # would otherwise keep reading stale from cache for the rest of
        # this transaction. Force a fresh compute so callers that keep
        # using this record/transaction (scripts, tests, other lines
        # processed by the same action_create_pob call) see it right away.
        self.invalidate_cache(fnames=["pob_id"], ids=self.ids)

    def _prepare_pob_data(self):
        self.ensure_one()
        xmlid = (
            "ssi_revenue_recognition."
            "field_performance_obligation_acceptance__qty_manual_fulfillment"
        )
        manual_field = self.env.ref(xmlid, raise_if_not_found=False)
        if not manual_field:
            error_message = _(
                """
Context: Create Performance Obligation from service contract fix item
Database ID: %s
Problem: Fulfillment field reference "%s" was not found
Solution: Make sure module ssi_revenue_recognition is installed and up to date
"""
                % (self.id, xmlid)
            )
            raise UserError(error_message)
        result = {
            "source_analytic_account_id": self.service_id.analytic_account_id.id,
            "title": self.name,
            "date": self.service_id.date,
            "product_id": self.product_id.id,
            "currency_id": self.currency_id.id,
            "uom_quantity": self.quantity,
            "uom_id": self.product_id.uom_id.id,
            # Per OFS/26/000026: PoB's Price Unit is deliberately the
            # line's untaxed amount (amount_untaxed), not the per-unit
            # price -- reporter confirmed this is the intended setting
            # after a prior revision (OFS/26/000025) briefly changed it
            # to per-unit price and had to be reverted. Note this means
            # price_subtotal (price_unit * uom_quantity, computed by
            # mixin.product_line_price) will overstate the total for
            # lines with quantity != 1, since amount_untaxed is already
            # quantity-multiplied -- accepted as out of scope here.
            "price_unit": self.amount_untaxed,
            "progress_completion_method": "input",
            "revenue_recognition_timing": "point_in_time",
            "fulfillment_field_id": manual_field.id,
        }
        return result
