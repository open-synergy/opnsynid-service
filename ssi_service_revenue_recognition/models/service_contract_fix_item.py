# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ServiceContractFixItem(models.Model):
    """Add Performance Obligation (PoB) creation to fix item lines.

    Each fix item line can be turned into a Performance Obligation
    for revenue recognition; ``pob_id`` resolves the PoB already
    created for a line (if any), and ``action_create_pob`` creates it.
    """

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
        "quantity",
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
        contract's total Performance Obligation. Matching on the same
        per-unit untaxed price ``_prepare_pob_data`` writes into the
        PoB's own ``price_unit`` (see ``_get_pob_price_unit`` and that
        method) keeps this search aligned with what a distinct view
        row's PoB actually looks like, so each distinct view row gets
        its own PoB while rows the view already merged (matching
        product/price) keep sharing one.

        ``price_unit`` is rounded to the currency's precision before
        the search (OFS/26/000024): ``_get_pob_price_unit()`` is a
        plain division that rarely lands on a round number, while the
        PoB's own ``price_unit`` -- a ``Monetary`` field -- was
        already rounded by Odoo when it got stored. Comparing the raw
        division result against that rounded value with ``=`` silently
        drops the match on any line whose amount does not divide
        evenly by its quantity, making an existing PoB look unlinked.
        """
        for record in self:
            result = False
            if record.service_id.analytic_account_id and record.product_id:
                PoB = self.env["performance_obligation"]
                price_unit = record.currency_id.round(record._get_pob_price_unit())
                criteria = [
                    (
                        "source_analytic_account_id",
                        "=",
                        record.service_id.analytic_account_id.id,
                    ),
                    ("product_id", "=", record.product_id.id),
                    ("price_unit", "=", price_unit),
                ]
                pobs = PoB.search(criteria)
                if pobs:
                    result = pobs[0]
            record.pob_id = result

    def _get_pob_price_unit(self):
        """Compute the per-unit untaxed price to store on the PoB.

        The view's ``amount_untaxed`` is the line's *total* untaxed
        amount (already multiplied by ``quantity``, and possibly summed
        across several payment term lines the view merged -- see
        ``ssi_service.models.service_contract_fix_item``), while the
        PoB's own ``price_subtotal`` is computed as
        ``price_unit * uom_quantity`` (``mixin.product_line_price``).
        Dividing by ``quantity`` here is what keeps that product equal
        to ``amount_untaxed`` again for lines with quantity != 1,
        instead of overstating it (OFS/26/000026). This must not be the
        item's own ``price_unit`` field either -- that is the contract's
        *tax-inclusive* per-unit price, and the reporter confirmed the
        PoB unit price must be untaxed (OFS/26/000025).

        :return: per-unit untaxed price, or ``0.0`` if quantity is zero
        """
        self.ensure_one()
        if not self.quantity:
            return 0.0
        return self.amount_untaxed / self.quantity

    def action_create_pob(self):
        """Create the Performance Obligation for each selected line."""
        for record in self.sudo():
            record._create_pob()

    def _create_pob(self):
        """Create the PoB for this single line, unless one already exists.

        Extension point: override ``_prepare_pob_data`` to change what
        gets written on the created ``performance_obligation`` record.
        """
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
        """Build the ``performance_obligation`` values for this line.

        Extension point: override to add/change fields on the PoB
        created by ``_create_pob``.

        :return: dict of ``performance_obligation`` values
        :raises UserError: if the manual fulfillment field reference
            from ``ssi_revenue_recognition`` cannot be resolved
        """
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
            # See _get_pob_price_unit: per-unit untaxed price, so
            # price_subtotal (price_unit * uom_quantity) matches
            # amount_untaxed again even when quantity != 1.
            "price_unit": self._get_pob_price_unit(),
            "progress_completion_method": "input",
            "revenue_recognition_timing": "point_in_time",
            "fulfillment_field_id": manual_field.id,
        }
        return result
